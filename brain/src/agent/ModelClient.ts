import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { Ollama } from 'ollama';

export interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'ollama' | 'nim';
  model: string;
  temperature?: number;
  max_tokens?: number;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  tool_calls?: any[];
  tool_call_id?: string;
}

export interface ToolSchema {
  name: string;
  description: string;
  parameters: Record<string, any>;
}

export interface TextChunk {
  type: 'text';
  content: string;
}

export interface ToolUseChunk {
  type: 'tool_use';
  tool: { name: string; arguments: any; id?: string };
}

export type StreamChunk = TextChunk | ToolUseChunk;

export class UnifiedModelClient {
  private client: Anthropic | OpenAI | Ollama;
  private config: ModelConfig;

  constructor(config: ModelConfig) {
    this.config = config;

    switch (config.provider) {
       case 'openai':
         this.client = new OpenAI({ 
           apiKey: process.env.OPENAI_API_KEY,
           timeout: 120_000,
         });
         break;
       case 'anthropic':
         this.client = new Anthropic({ 
           apiKey: process.env.ANTHROPIC_API_KEY,
           timeout: 120_000,
         });
         break;
        case 'ollama':
          this.client = new Ollama({ 
            host: process.env.OLLAMA_HOST || 'http://localhost:11434',
          });
          break;
       case 'nim':
         this.client = new OpenAI({
           apiKey: process.env.NVIDIA_API_KEY || process.env.NGC_API_KEY || '',
           baseURL: process.env.NIM_BASE_URL || 'https://integrate.api.nvidia.com/v1',
           timeout: 120_000,
         });
         break;
      default:
        throw new Error(`Unknown provider: ${config.provider}`);
    }
  }

  async *streamChat(params: {
    system: string;
    messages: ChatMessage[];
    tools?: ToolSchema[];
  }): AsyncGenerator<StreamChunk> {
    switch (this.config.provider) {
      case 'anthropic':
        yield* this.streamAnthropic(params);
        break;
      case 'openai':
        yield* this.streamOpenAI(params);
        break;
      case 'ollama':
        yield* this.streamOllama(params);
        break;
      case 'nim':
        yield* this.streamNIM(params);
        break;
    }
  }

  private async *streamAnthropic(params: { system: string; messages: ChatMessage[]; tools?: ToolSchema[] }) {
    const client = this.client as Anthropic;
    const anthropicMessages = params.messages.map((m) => ({
      role: m.role as 'user' | 'assistant',
      content: m.content,
    }));

    const anthropicTools = params.tools?.map((t) => ({
      name: t.name,
      description: t.description,
      input_schema: t.parameters as any,
    }));

    const stream = await client.messages.stream({
      model: this.config.model,
      max_tokens: this.config.max_tokens || 4096,
      temperature: this.config.temperature || 0.7,
      system: params.system,
      messages: anthropicMessages,
      tools: anthropicTools,
    });

    for await (const event of stream) {
        if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
          yield { type: 'text' as const, content: event.delta.text };
        } else if (event.type === 'content_block_start' && event.content_block.type === 'tool_use') {
          yield {
            type: 'tool_use' as const,
            tool: {
              id: event.content_block.id,
              name: event.content_block.name,
              arguments: event.content_block.input,
            },
          };
        }
    }
  }

  private async *streamOpenAI(params: { system: string; messages: ChatMessage[]; tools?: ToolSchema[] }) {
    const client = this.client as OpenAI;
    const openaiMessages: any = [
      { role: 'system', content: params.system },
      ...params.messages.map((m) => ({
        role: m.role,
        content: m.content,
        tool_call_id: m.tool_call_id,
      })),
    ];

    const openaiTools = params.tools?.map((t) => ({
      type: 'function' as const,
      function: {
        name: t.name,
        description: t.description,
        parameters: t.parameters,
      },
    }));

    const stream = await client.chat.completions.create({
      model: this.config.model,
      max_tokens: this.config.max_tokens || 4096,
      temperature: this.config.temperature || 0.7,
      messages: openaiMessages,
      tools: openaiTools,
      stream: true,
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta;
      if (delta?.content) {
        yield { type: 'text' as const, content: delta.content };
      }
        if (delta?.tool_calls?.[0]) {
          const tc = delta.tool_calls[0];
          let args = tc.function?.arguments;
          if (typeof args === 'string') {
            try {
              args = JSON.parse(args);
            } catch {
              // keep as string if not JSON
            }
          }
          yield {
            type: 'tool_use' as const,
            tool: {
              id: tc.id,
              name: tc.function?.name || '',
              arguments: args,
            },
          };
        }
    }
  }

  private async *streamOllama(params: { system: string; messages: ChatMessage[]; tools?: ToolSchema[] }) {
    const client = this.client as Ollama;
    const ollamaMessages = [
      { role: 'system', content: params.system },
      ...params.messages.map((m) => ({
        role: m.role as 'user' | 'assistant' | 'tool',
        content: m.content,
        tool_calls: m.tool_calls,
        tool_call_id: m.tool_call_id,
      })),
    ];

    const response = await client.chat({
      model: this.config.model,
      messages: ollamaMessages,
      tools: params.tools?.map(t => ({
        type: 'function',
        function: {
          name: t.name,
          description: t.description,
          parameters: t.parameters,
        },
      })),
      stream: true,
      options: {
        temperature: this.config.temperature ?? 0.7,
        num_predict: this.config.max_tokens ?? 4096,
      },
    });

    let accumulatedToolCall: any = null;

    for await (const chunk of response) {
      if (chunk.message?.content) {
        yield { type: 'text' as const, content: chunk.message.content };
      }

      // Check for tool_calls in the chunk (Ollama 0.5+ supports function calling)
      if (chunk.message?.tool_calls && chunk.message.tool_calls.length > 0) {
        // Take the first tool call; we only support one at a time in Brain
        const toolCall = chunk.message.tool_calls[0];
        accumulatedToolCall = {
          id: toolCall.function?.name + '_' + Date.now(),
          name: toolCall.function?.name || '',
          arguments: toolCall.function?.arguments || {},
        };
        yield { type: 'tool_use' as const, tool: accumulatedToolCall };
      }
    }
  }

  /**
   * streamNIM — NVIDIA NIM free cloud endpoints (integrate.api.nvidia.com).
   * Uses the OpenAI-compatible API at $NIM_BASE_URL.
   *
   * Two keys in play:
   *   NVIDIA_API_KEY — build.nvidia.com NIM API key (nvapi-* prefix)  ← use this
   *   NGC_API_KEY    — ngc-cli credential (~/.ngc/config); used for nvcr.io Docker
   *
   * Free endpoint models (no GPU, no credits): https://build.nvidia.com/explore/discover
   * Env vars:
   *   NVIDIA_API_KEY — NIM cloud API key (preferred, from build.nvidia.com)
   *   NGC_API_KEY    — ngc-cli fallback if NVIDIA_API_KEY is absent
   *   NIM_BASE_URL   — override default https://integrate.api.nvidia.com/v1
   */
  private async *streamNIM(params: { system: string; messages: ChatMessage[]; tools?: ToolSchema[] }) {
    const client = this.client as OpenAI;
    const nimMessages: any = [
      { role: 'system', content: params.system },
      ...params.messages.map((m) => ({
        role: m.role,
        content: m.content,
      })),
    ];

    const nimTools = params.tools?.map((t) => ({
      type: 'function' as const,
      function: {
        name: t.name,
        description: t.description,
        parameters: t.parameters,
      },
    }));

    const stream = await client.chat.completions.create({
      model: this.config.model,
      max_tokens: this.config.max_tokens || 4096,
      temperature: this.config.temperature || 0.7,
      messages: nimMessages,
      tools: nimTools,
      stream: true,
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta;
      if (delta?.content) {
        yield { type: 'text' as const, content: delta.content };
      }
      if (delta?.tool_calls?.[0]) {
        const tc = delta.tool_calls[0];
        // NIM tool_calls use OpenAI format — args arrive as JSON string or object
        let args = tc.function?.arguments;
        if (typeof args === 'string') {
          try {
            args = JSON.parse(args);
          } catch {
            // keep as string if not JSON
          }
        }
        yield {
          type: 'tool_use' as const,
          tool: {
            id: tc.id || `${tc.function?.name || 'tool'}_${Date.now()}`,
            name: tc.function?.name || '',
            arguments: args,
          },
        };
      }
    }
  }
}
