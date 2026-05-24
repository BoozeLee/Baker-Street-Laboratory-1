import fs from 'fs';
import yaml from 'yaml';
import path from 'path';

export interface BuildParams {
  role: 'agent' | 'conversational' | 'observer' | 'reflector' | 'reasoner';
  memories: MemoryItem[];
  observations: Observation[];
  activeSkills: string[];
  currentTime: string;
}

export interface MemoryItem {
  content: string;
  confidence: number;
  source?: string;
  timestamp?: number;
}

export interface Observation {
  type: 'decision' | 'preference' | 'fact' | 'issue' | 'nextstep' | 'outcome';
  content: string;
  confidence: number;
  related_tools?: string[];
}

export class SystemPromptBuilder {
  private configPath: string;
  private cachedPrompts: { soul?: string; brain?: string } = {};

  constructor(configPath: string) {
    this.configPath = configPath;
  }

  async loadPrompts(): Promise<{ soul: string; brain: string }> {
    try {
      const soulPath = path.join(this.configPath, 'SOUL.md');
      const brainPath = path.join(this.configPath, 'BRAIN.md');

      this.cachedPrompts.soul = fs.readFileSync(soulPath, 'utf-8');
      this.cachedPrompts.brain = fs.readFileSync(brainPath, 'utf-8');

      return {
        soul: this.cachedPrompts.soul,
        brain: this.cachedPrompts.brain,
      };
    } catch (err) {
      console.error('[SystemPromptBuilder] Failed to load prompts:', err);
      throw new Error('Could not load operating system prompts');
    }
  }

  build(params: BuildParams): string {
    const { role, memories, observations, activeSkills, currentTime } = params;

    const sections: string[] = [];

    // 1. SOUL (identity foundation)
    if (this.cachedPrompts.soul) {
      sections.push(`# Identity\n\n${this.cachedPrompts.soul}`);
    }

    // 2. Role-specific header
    sections.push(this.buildRoleHeader(role));

    // 3. Current context
    sections.push(`## Current Context\n\n- Time: ${currentTime}\n- Active skills: ${activeSkills.join(', ') || 'none'}`);

    // 4. Relevant memories (RAG)
    if (memories.length > 0) {
      const memorySection = memories
        .map((m, i) => `[${i + 1}] ${m.content} (confidence: ${(m.confidence * 100).toFixed(0)}%)`)
        .join('\n');
      sections.push(`## Relevant Context\n\n${memorySection}`);
    }

    // 5. Recent observations (active decision log)
    if (observations.length > 0) {
      const obsSection = observations
        .map(o => `- [${o.type}] ${o.content}`)
        .join('\n');
      sections.push(`## Recent Activity\n\n${obsSection}`);
    }

    // 6. Tool documentation (BRAIN.md)
    if (this.cachedPrompts.brain) {
      sections.push(`## Tools\n\n${this.cachedPrompts.brain}`);
    }

    // 7. Role-specific instructions
    sections.push(this.buildRoleInstructions(role));

    // 8. Constraints & safety
    sections.push(`
## Constraints

**MUST**:
- Think step by step before calling tools
- Show reasoning with "I need to..." then "Tool: ..."
- Acknowledge uncertainty with confidence scores
- Cite sources when making claims

**MUST NOT**:
- Fabricate data or citations
- Claim access to unavailable tools
- Execute harmful code or queries
- Ignore error messages without retry strategy
    `);

    return sections.filter(Boolean).join('\n\n---\n\n');
  }

  private buildRoleHeader(role: string): string {
    const headers: Record<string, string> = {
      agent: 'You are in **AGENT MODE** — use tools to accomplish tasks. Think step by step.',
      conversational: 'You are in **CONVERSATIONAL MODE** — respond naturally without tools unless asked.',
      observer: 'You are in **OBSERVER MODE** — extract structured observations from this exchange.',
      reflector: 'You are in **REFLECTOR MODE** — compress and consolidate memories.',
      reasoner: 'You are in **REASONER MODE** — perform deep planning and analysis.',
    };
    return headers[role] || headers.agent;
  }

  private buildRoleInstructions(role: string): string {
    const instructions: Record<string, string> = {
      agent: `
## Agent Instructions

When responding:
1. Analyze the user's request
2. If tools are needed, state which tool and why
3. Call the tool with correct parameters
4. Interpret the result and continue (up to 10 iterations)

Decision process:
- Is information already in context/memory? → use recall (no tool)
- Need fresh data from external source? → use tool
- Multiple steps? → chain tools together`,
      conversational: `
## Conversational Instructions

- Greet naturally. Answer simple questions directly.
- Only use tools if explicitly requested or absolutely necessary.
- Keep responses concise unless user asks for detail.`,
      observer: `
## Observer Instructions

After this exchange, extract structured observations in JSON:
{
  "type": "decision|preference|fact|issue|nextstep|outcome",
  "content": "...",
  "confidence": 0.0-1.0,
  "related_tools": ["tool_name"]
}`,
      reflector: `
## Reflector Instructions

Compress the current observation log by:
1. Merging duplicate observations
2. Dropping superseded items
3. Preserving active decisions and high-confidence facts
4. Summarising old entries into higher-level insights`,
      reasoner: `
## Reasoner Instructions

Perform comprehensive reasoning:
1. Break down the problem
2. Consider multiple approaches
3. Evaluate pros/cons
4. Propose implementation plan
5. Anticipate failure modes`,
    };
    return instructions[role] || instructions.agent;
  }
}
