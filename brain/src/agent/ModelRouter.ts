import { UnifiedModelClient } from './ModelClient.js';

// ─── Baker Street Laboratory — Model routing ─────────────────────────────────
// Brain can route conversation roles to either Ollama (local) or NIM (free cloud).
// Adding 'nim' provider just requires NGC_API_KEY in env; same OpenAI-compatible API.
const defaultConfig: Record<string, { provider: 'ollama' | 'nim'; model: string; temperature?: number; max_tokens?: number; priority: number }> = {
  // Primary reasoning engine — local Ollama first, NIM cloud as fallback
  agent:         { provider: 'ollama', model: 'hermes-3-llama-3b',           temperature: 0.3, max_tokens: 4096, priority: 1 },
  // Quick, lightweight conversational responses
  conversational:{ provider: 'ollama', model: 'qwen3-1.7b',                   temperature: 0.7, max_tokens: 1024, priority: 3 },
  // Observer mode — extract structured observations from exchanges
  observer:      { provider: 'ollama', model: 'openchat:3.5-0106-q4_K_M',     temperature: 0.1, max_tokens:  512, priority: 2 },
  // Reflector mode — compress and consolidate memories
  reflector:     { provider: 'ollama', model: 'neural-chat:7b-v3-3-q4_K_M',   temperature: 0.2, max_tokens: 2048, priority: 2 },
  // Deep reasoning and planning mode
  reasoner:      { provider: 'ollama', model: 'yarn-mistral:7b-128k-q4_K_M',  temperature: 0.5, max_tokens: 8192, priority: 1 },
};

// ─── Free NIM endpoint models (no GPU / no credits required) ─────────────────
// Source: https://build.nvidia.com/explore/discover
// Auth:   Authorization: Bearer <NGC_API_KEY>  (latest NIM specs are registered
//         at `integrate.api.nvidia.com/v1`; the NIM_agent tool sink references this)
const nimFallbacks = [
  'nvidia/llama-3.1-nemotron-nano-8b-v1',
  'nvidia/nvidia-nemotron-nano-9b-v2',
  'nvidia/nemotron-mini-4b-instruct',
  'nvidia/nemotron-3-nano-30b-a3b',
  'meta/llama-3.3-70b-instruct',
  'deepseek-ai/deepseek-v4-flash',
  'qwen/qwen3-coder-480b-a35b-instruct',
  'stepfun-ai/step-3-5-flash',
];

// ─── Ollama models known to support tool / function calling ──────────────────
const toolCapableFallbacks = [
  'mistral:instruct',
  'llama3:8b-instruct',
  'phi3:instruct',
  'openchat:3.5-0106-q4_K_M',
  'deepseek-coder:6.7b-instruct-q4_K_M',
];

export class ModelRouter {
  private clients: Map<string, UnifiedModelClient> = new Map();
  private config: Record<string, any>;
  private availableModels: Set<string>;

  constructor(customConfig?: Partial<Record<string, any>>, availableModels?: string[]) {
    this.config = { ...defaultConfig, ...customConfig };
    // Pre-populate with Ollama model names; NIM keys are added at discovery time
    this.availableModels = availableModels ? new Set(availableModels) : new Set(Object.values(this.config).map(c => c.model));
  }

  /**
   * getModel — resolves a conversation role to a ready-to-use UnifiedModelClient.
   *
   * Availability chain:
   *  1. Preferred Ollama model (per defaultConfig)
   *  2. Known tool-capable Ollama fallback
   *  3. Free NIM endpoint cloud model
   *  4. ANY available model (last resort)
   */
  getModel(role: string): UnifiedModelClient {
    const roleKey = role as keyof typeof defaultConfig;
    let modelConfig = this.config[roleKey] || this.config.agent;

    const isAvailable = (name: string) =>
      this.availableModels.has(name) || this.availableModels.has(`nim:${name}`);

    if (!isAvailable(modelConfig.model)) {
      // ── Stage 2: known Ollama tool-capable fallbacks ────────────────────
      for (const fallback of toolCapableFallbacks) {
        if (this.availableModels.has(fallback)) {
          modelConfig = { ...modelConfig, model: fallback };
          console.log(`[ModelRouter] ${modelConfig.model} not available, using tool-capable: ${fallback}`);
          break;
        }
      }

      // ── Stage 3: NIM free cloud endpoint ────────────────────────────────
      if (!isAvailable(modelConfig.model)) {
        for (const nimModel of nimFallbacks) {
          const nimKey = `nim:${nimModel}`;
          if (this.availableModels.has(nimKey)) {
            modelConfig = { ...modelConfig, provider: 'nim', model: nimModel };
            console.log(`[ModelRouter] Ollama exhausted, using NIM free cloud: ${nimModel}`);
            break;
          }
        }
      }

      // ── Stage 4: first available model of any kind ──────────────────────
      if (!isAvailable(modelConfig.model)
          && !nimFallbacks.find((m) => this.availableModels.has(`nim:${m}`))) {
        const any = Array.from(this.availableModels)[0];
        if (any) {
          modelConfig = { ...modelConfig, model: any };
          console.log(`[ModelRouter] Using any available model: ${any}`);
        }
      }
    }

    const cacheKey = `${modelConfig.provider}:${modelConfig.model}`;
    if (!this.clients.has(cacheKey)) {
      this.clients.set(cacheKey, new UnifiedModelClient(modelConfig));
    }

    return this.clients.get(cacheKey)!;
  }

  setAvailableModels(models: string[]): void {
    this.availableModels = new Set(models);
  }
}
