import { EventEmitter } from 'events';
import { SystemPromptBuilder } from '../prompts/SystemPromptBuilder.js';
import { ToolDispatcher } from '../tools/ToolDispatcher.js';
import { MemoryStore } from '../memory/MemoryStore.js';
import { MessageClassifier } from './MessageClassifier.js';
import { ModelRouter } from './ModelRouter.js';
import { UnifiedModelClient } from './ModelClient.js';
import { Observer } from '../memory/Observer.js';
import { Reflector } from '../memory/Reflector.js';
import { NATSClient } from '../nats/NATSClient.js';
import { CronJob } from 'cron';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export interface ChatOptions {
  message: string;
  conversationId: string;
  onText: (chunk: string) => void;
  onToolUse: (tool: any) => void;
  onDone: () => void;
  onError: (err: Error) => void;
}

export interface BrainConfig {
  bslApiUrl: string;
  natsUrl: string;
  qdrantUrl: string;
  sqlitePath: string;
  configPath: string;
}

export class Brain extends EventEmitter {
  private config: BrainConfig;
  private toolDispatcher: ToolDispatcher;
  private memory: MemoryStore;
  private systemPromptBuilder: SystemPromptBuilder;
  private messageClassifier: MessageClassifier;
  private observer: Observer;
  private reflector: Reflector;
  private nats: NATSClient;

  private loadedPrompts: { soul: string; brain: string } | null = null;
  private cronJobs: CronJob[] = [];
  private modelRouter!: ModelRouter; // initialized in initialize()

  constructor(config: BrainConfig) {
    super();
    this.config = config;
    this.toolDispatcher = new ToolDispatcher();
    this.memory = new MemoryStore(config.sqlitePath, config.qdrantUrl);
    this.systemPromptBuilder = new SystemPromptBuilder(config.configPath);
    this.messageClassifier = new MessageClassifier();
    this.observer = new Observer(this.memory);
    this.reflector = new Reflector(this.memory);
    this.nats = new NATSClient(config.natsUrl);
    // ModelRouter will be initialized in initialize() after discovering Ollama models
  }

  async initialize(): Promise<void> {
    console.log('[Brain] Initializing...');

    // 1. Load SOUL.md and BRAIN.md
    this.loadedPrompts = await this.systemPromptBuilder.loadPrompts();
    console.log('[Brain] Prompts loaded');

    // 2. Initialize memory
    await this.memory.initialize();
    console.log('[Brain] Memory store ready');

    // 3. Connect to NATS
    try {
      await this.nats.connect();
      console.log('[Brain] NATS connected');
    } catch (err) {
      console.warn('[Brain] NATS unavailable — continuing without message bus');
    }

    // 4. Discover Ollama models (with retry)
    const availableModels = await this.discoverOllamaModels();
    this.modelRouter = new ModelRouter(undefined, availableModels);
    console.log(`[Brain] Model router ready — ${availableModels.length} Ollama models available`);

    // 5. Register BSL tools
    this.toolDispatcher.registerBSLTools(this.config.bslApiUrl);
    console.log('[Brain] Tools registered');

    // 6. Start background reflector
    this.reflector.startCompactionCycle();

    // 7. Load cron schedules
    this.loadCronSchedules();

    console.log('[Brain] Initialization complete');
  }

  private async discoverOllamaModels(retries = 5, delay = 2000): Promise<string[]> {
    const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await fetch(`${ollamaHost}/api/tags`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data: any = await response.json();
        const models = data.models || data.names || [];
        const modelNames = models.map((m: any) => m.name || m);
        console.log(`[Brain] Discovered Ollama models: ${modelNames.join(', ')}`);
        return modelNames;
      } catch (err: any) {
        console.warn(`[Brain] Ollama not ready (attempt ${attempt}/${retries}):`, err);
        if (attempt < retries) await new Promise(r => setTimeout(r, delay));
      }
    }

    console.error('[Brain] Ollama unavailable after retries — using fallback model list');
    return [
      'llava:7b-v1.6-mistral-q4_K_M',
      'nomic-embed-text',
      'yarn-mistral:7b-128k-q4_K_M',
      'openchat:3.5-0106-q4_K_M',
      'neural-chat:7b-v3-3-q4_K_M',
      'deepseek-coder:6.7b-instruct-q4_K_M',
      'arcee-ai/arcee-agent',
      'qwen2-audio:7b-instruct',
      'hermes-3-llama-3b',
      'qwen3-1.7b',
    ];
  }

  async chatStream(options: ChatOptions): Promise<void> {
    const { message, conversationId, onText, onToolUse, onDone, onError } = options;

    try {
      // Load conversation history
      const history = await this.memory.getConversation(conversationId);

      // Classify to determine model/role
      const role = this.messageClassifier.classify(message, history);
      const model = this.modelRouter.getModel(role);

       // Search memory
       const rawMemories = await this.memory.search(message, 5);
       const memories = rawMemories.map(m => ({
         content: m.content,
         confidence: m.metadata.confidence,
         source: m.metadata.source,
         timestamp: m.metadata.timestamp,
       }));

       // Get observations
       const observations = await this.memory.getRecentObservations(conversationId, 20);

      // Build system prompt
      const now = new Date().toISOString();
      const systemPrompt = this.systemPromptBuilder.build({
        role,
        memories,
        observations,
        activeSkills: ['research', 'code', 'vision', 'memory'],
        currentTime: now,
      });

      let fullResponse = '';
      let messages = [...history, { role: 'user' as const, content: message }];

      // Iteration loop
      for (let iteration = 0; iteration < 10; iteration++) {
        const stream = model.streamChat({
          system: systemPrompt,
          messages,
          tools: this.toolDispatcher.getToolSchemas(),
        });

        let currentToolCall: any = null;
        let currentText = '';

        for await (const chunk of stream) {
          if (chunk.type === 'text') {
            currentText += chunk.content;
            onText(chunk.content);
          } else if (chunk.type === 'tool_use') {
            currentToolCall = chunk.tool;
            onToolUse(chunk.tool);
          }
        }

        // Append assistant message with optional tool call
        messages.push({
          role: 'assistant',
          content: currentText,
          tool_calls: currentToolCall ? [currentToolCall] : undefined,
        });

        if (!currentToolCall) break;

        // Execute tool
        const results = await this.toolDispatcher.executeAll([
          { id: `call_${Date.now()}`, name: currentToolCall.name, arguments: currentToolCall.arguments },
        ]);

        messages.push({
          role: 'tool',
          content: JSON.stringify(results[0].result),
          tool_call_id: results[0].tool_call_id,
        });
      }

      await this.memory.saveConversation(conversationId, messages);
      this.observer.extractObservations(conversationId, messages[messages.length - 1]?.content || '', messages);

      onDone();
     } catch (err: any) {
       console.error('[Brain.chatStream] error:', err);
       onError(err instanceof Error ? err : new Error(String(err)));
     }
  }

  async chat({ message, conversationId }: { message: string; conversationId?: string }) {
    const conversationId_ = conversationId || Date.now().toString(36);
    let fullResponse = '';

    await this.chatStream({
      message,
      conversationId: conversationId_,
      onText: (chunk) => { fullResponse += chunk; },
      onToolUse: (tool) => { console.log('[Tool]', tool.name, tool.arguments); },
      onDone: () => {},
      onError: (err) => { throw err; },
    });

    return {
      conversation_id: conversationId_,
      response: fullResponse,
    };
  }

  async executeTool(name: string, parameters: any): Promise<any> {
    return this.toolDispatcher.execute(name, parameters);
  }

  async searchMemory(query: string, limit: number = 10): Promise<any[]> {
    return this.memory.search(query, limit);
  }

  async getConversation(conversationId: string): Promise<any[]> {
    return this.memory.getConversation(conversationId);
  }

  getToolStatus(): any {
    return this.toolDispatcher.getStatus();
  }

  private loadCronSchedules(): void {
    try {
      const cronsPath = path.join(__dirname, '..', '..', 'operating_system', 'CRONS.json');
      const crons = JSON.parse(fs.readFileSync(cronsPath, 'utf-8'));

      for (const schedule of crons.schedules) {
        if (!schedule.enabled) continue;
        const job = new CronJob(
          schedule.cron,
           async () => {
             console.log(`[Cron] Executing ${schedule.id}`);
             try {
               await this.toolDispatcher.execute(schedule.tool, schedule.parameters);
             } catch (err: any) {
               console.error(`[Cron] ${schedule.id} failed:`, err);
             }
           }
        );
        job.start();
        this.cronJobs.push(job);
      }
    } catch (err: any) {
      console.warn('[Cron] Could not load CRONS.json:', err.message);
    }
  }

  async shutdown(): Promise<void> {
    for (const job of this.cronJobs) {
      job.stop();
    }
    await this.nats.disconnect();
    await this.memory.close();
  }
}
