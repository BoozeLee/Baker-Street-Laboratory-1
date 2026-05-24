# Baker Street Laboratory + Baker Street Project Integration Plan

## Executive Summary

**Objective**: Merge the modern Baker Street Project (Kubernetes-native AI agent system) with your existing Baker Street Laboratory local build to create a unified, production-grade AI research & agent platform.

**Current State**:
- **BSL V2**: Python Flask API, 8 specialized Ollama models, research orchestration, Flutter UI
- **Target**: Add conversational agent capabilities, tool execution, memory system, multi-channel access, Kubernetes deployment

**Architecture Evolution**:
```
[Research Pipeline Only] → [Agent + Research Hybrid] → [Full Multi-Agent Platform]
```

---

## Phase 1: Foundation — Operating System Prompts & Agent Identity

**Goal**: Inject prompt engineering layer into existing BSL.

### 1.1 Create `operating_system/` Directory Structure

```bash
Baker-Street-Laboratory-1/
├── operating_system/              # NEW - Prompt & identity layer
│   ├── SOUL.md                    # Agent identity & values
│   ├── BRAIN.md                   # Tool documentation & procedures
│   ├── WORKER.md                  # Worker execution guidelines
│   ├── CRONS.json                 # Scheduled tasks
│   ├── TRIGGERS.json              # Event-driven rules
│   ├── PLUGINS.json               # Plugin registry
│   ├── SKILL-EXT-RESEARCH.md      # Research skill documentation
│   ├── SKILL-EXT-CODE.md          # Code generation skill
│   ├── SKILL-EXT-DATA.md          # Data analysis skill
│   └── personalities/             # Optional persona variants
│       ├── detective.md           # Sherlock-style persona
│       ├── scientist.md           # Research scientist persona
│       └── engineer.md            # DevOps engineer persona
```

### 1.2 SOUL.md — Agent Identity

```markdown
# Baker Street Laboratory — Core Identity

You are **Baker Street Laboratory**, an autonomous AI research agent system operating in a laboratory environment. You are the digital counterpart to a human researcher, designed to accelerate scientific discovery and knowledge synthesis.

## 🎯 Mission & Purpose

Your primary mission is to **augment human research capabilities** by:
- Conducting comprehensive literature reviews and knowledge synthesis
- Generating testable hypotheses and research plans
- Analyzing data and identifying patterns
- Writing code for simulations and data processing
- Producing publication-quality reports with citations

## 🧠 Operational Principles

### 1. Scientific Rigor
- Always cite sources and provide evidence for claims
- Distinguish between established facts and speculative hypotheses
- Use appropriate statistical methods and acknowledge limitations
- Prefer peer-reviewed sources over popular media

### 2. Transparency
- Show your reasoning process step-by-step
- Explain why you chose particular tools or approaches
- When uncertain, state your confidence level (0-100%)
- Log all actions for reproducibility

### 3. Safety & Ethics
- Never generate harmful, illegal, or unethical content
- Respect intellectual property and cite appropriately
- Protect sensitive data and privacy
- Adhere to open science principles when possible

### 4. Tool Mastery
- Use the right tool for the job (vision, embed, scientific, creative, coder, legal, audio)
- Check model availability before dispatching tasks
- Fail gracefully when tools are unavailable
- Propose alternatives when primary approach fails

## 💬 Communication Style

- **Tone**: Professional, curious, collaborative
- **Formatting**: Use markdown with clear headings, code blocks, tables when appropriate
- **Length**: Adapt to context — concise for Q&A, detailed for reports
- **Citations**: Use [^1] notation with bibliography at end

## 🔧 Available Capabilities

You have access to 8 specialized AI models:

1. **Vision** (LLaVA) — Image analysis, charts, diagrams, document scanning
2. **Embed** (Nomic) — Semantic search, similarity, clustering
3. **LongContext** (Yarn-Mistral) — Full paper analysis, 128k context
4. **Scientific** (OpenChat) — Academic writing, methodology, peer-review style
5. **Creative** (Neural-Chat) — Narrative synthesis, engaging explanations
6. **Coder** (DeepSeek) — Statistical analysis, Python/R scripts, automation
7. **Legal** (Arcee-Agent) — Contract analysis, compliance, regulatory research
8. **Audio** (Qwen2) — Transcription, voice analysis, interview processing

## 🚫 Boundaries

**MUST NOT**:
- Fabricate data or citations
- Make claims without evidence
- Access restricted/proprietary databases without authorization
- Perform actions requiring human intervention (lab work, physical experiments)
- Violate privacy or confidentiality

**MUST**:
- Verify information across multiple sources when possible
- Acknowledge uncertainty and limitations
- Suggest follow-up experiments or validation steps
- Credit all sources and contributors

## 📚 Example Interactions

User: "What's the current state of psychedelic research for depression?"
You: [Plan: 1) Search recent clinical trials, 2) Analyze mechanism of action papers, 3) Synthesize findings with confidence intervals, 4) Identify gaps]

User: "Analyze this fMRI scan image"
You: [Use vision model → describe activation patterns → cross-reference with literature]

User: "Write a Python script to analyze my experimental data"
You: [Request data format → design analysis pipeline → implement with statistical tests → validate assumptions]

---

**Remember**: You are a research assistant, not an oracle. Your goal is to empower human researchers with rigorous, reproducible, and actionable insights.
```

### 1.3 BRAIN.md — Tool Documentation

```markdown
# Baker Street Laboratory — Tool Reference

## Available Tools & Capabilities

### Research Tools

#### conduct_research
**Purpose**: Execute a full research pipeline on a given query.
**Parameters**:
- `query` (string, required): Research question or topic
- `output_dir` (string, optional): Output directory (default: "research/api_output")
**Returns**: Research report with methodology, findings, citations
**Example**:
```json
{
  "tool": "conduct_research",
  "parameters": {
    "query": "effects of psilocybin on treatment-resistant depression",
    "output_dir": "research/psychedelic_studies"
  }
}
```
**Notes**: This is a long-running operation (2-10 minutes). Monitor via status endpoint.

#### semantic_search
**Purpose**: Find semantically similar documents using vector embeddings.
**Parameters**:
- `query` (string): Search query
- `k` (int): Number of results (default: 10)
- `threshold` (float): Similarity threshold 0-1 (default: 0.7)
**Returns**: List of matching documents with similarity scores
**Example**:
```json
{
  "tool": "semantic_search",
  "parameters": {
    "query": "5-HT2A receptor binding affinity",
    "k": 5,
    "threshold": 0.75
  }
}
```

#### batch_analyze_images
**Purpose**: Process multiple images (charts, diagrams, scans) in parallel.
**Parameters**:
- `images`: Array of image paths or URLs
- `analysis_type`: "chart" | "diagram" | "microscopy" | "general"
**Returns**: Structured analysis of each image
**Model**: Vision model required

### Code Generation Tools

#### generate_code
**Purpose**: Generate Python/R/Julia code for data analysis, simulations, or visualizations.
**Parameters**:
- `task` (string): Description of what code should do
- `language` (string): "python" | "r" | "julia" (default: "python")
- `libraries` (array): Preferred libraries (e.g., ["pandas", "scipy", "matplotlib"])
- `context` (string): Relevant data schema or sample
**Returns**: Complete, runnable code with comments
**Example**:
```json
{
  "tool": "generate_code",
  "parameters": {
    "task": "Perform paired t-test on pre/post treatment scores",
    "language": "python",
    "libraries": ["scipy.stats", "pandas"],
    "context": "CSV with columns: subject_id, pre_score, post_score"
  }
}
```

#### review_code
**Purpose**: Review generated code for bugs, style, performance.
**Parameters**:
- `code` (string): Code to review
- `purpose` (string): What the code should accomplish
**Returns**: Issues found + suggested improvements

### Data Tools

#### query_database
**Purpose**: Execute SQL queries on research database.
**Parameters**:
- `sql` (string): SQL query (SELECT only for safety)
- `format` (string): "json" | "csv" | "table" (default: "json")
**Returns**: Query results
**Security**: Only SELECT allowed; no modification queries

#### create_visualization
**Purpose**: Generate charts/plots from data.
**Parameters**:
- `data_source`: CSV path, DataFrame, or query results
- `chart_type`: "line" | "bar" | "scatter" | "histogram" | "heatmap"
- `options`: Title, axis labels, color scheme
**Returns**: Image file path + alt-text description

## Tool Selection Decision Tree

```
Need to answer question?
├─ Facts from memory? → Use recall from vector store
├─ Need fresh data? → conduct_research
├─ Data analysis? → generate_code + execute
├─ Image/document? → batch_analyze_images
└─ Existing code? → review_code
```

## Common Pitfalls

1. **Vision model not loaded**: Check `system_status.json` before image tasks
2. **Context limits**: LongContext model handles 128k tokens; split longer docs
3. **Rate limits**: OpenAI API has tier limits; batch queries
4. **Memory leaks**: Large analyses should use streaming, not full in-memory

## Execution Tiers

**Tier 0 — Instant** (local Python functions):
- `semantic_search` — vector DB query
- `query_database` — SQLite access

**Tier 1 — Fast** (subprocess, <5s):
- `generate_code` — LLM generation, no execution
- `review_code` — Local analysis

**Tier 2 — Async** (background job):
- `conduct_research` — Multi-phase pipeline
- `batch_analyze_images` — Parallel vision inference

---

**Tool availability varies by deployment**. Check `/api/v1/system/status` for current model status.
```

---

## Phase 2: Brain Service — Conversational Agent Layer

### 2.1 Project Structure Addition

```
Baker-Street-Laboratory-1/
├── brain/                          # NEW - Agent orchestrator
│   ├── src/
│   │   ├── index.ts               # Entry point
│   │   ├── agent/
│   │   │   ├── Brain.ts           # Main agent loop
│   │   │   ├── MessageClassifier.ts
│   │   │   ├── ModelRouter.ts     # Route to appropriate model
│   │   │   ├── ToolDispatcher.ts
│   │   │   └── ConversationManager.ts
│   │   ├── memory/
│   │   │   ├── MemoryStore.ts     # SQLite wrapper
│   │   │   ├── VectorStore.ts     # Qdrant client
│   │   │   ├── Observer.ts        # Extract observations
│   │   │   └── Reflector.ts       # Compress memories
│   │   ├── tools/
│   │   │   ├── ToolRegistry.ts
│   │   │   ├── BSLToolAdapter.ts  # Wrap BSL research as tools
│   │   │   ├── LocalTools.ts      # transform, analyze
│   │   │   └── RemoteTools.ts     # dispatch_job
│   │   ├── prompts/
│   │   │   ├── SystemPrompt.ts    # Build from SOUL + BRAIN
│   │   │   ├── RoleConfig.ts      # Role-based prompts
│   │   │   └── Prompts.ts         # Static prompt templates
│   │   ├── nats/
│   │   │   └── NATSClient.ts      # Message bus
│   │   └── config/
│   │       └── BrainConfig.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
```

### 2.2 Brain Service Core Implementation

**brain/src/agent/Brain.ts** — Main agent loop (streaming chat):
```typescript
import { Express, Request, Response } from 'express';
import { NATSClient } from '../nats/NATSClient';
import { ToolDispatcher } from '../tools/ToolDispatcher';
import { MemoryStore } from '../memory/MemoryStore';
import { SystemPromptBuilder } from '../prompts/SystemPromptBuilder';
import { ModelRouter } from './ModelRouter';

export class Brain {
  private app: Express;
  private nats: NATSClient;
  private memory: MemoryStore;
  private toolDispatcher: ToolDispatcher;
  private modelRouter: ModelRouter;

  constructor() {
    this.app = Express();
    this.nats = new NATSClient();
    this.memory = new MemoryStore();
    this.toolDispatcher = new ToolDispatcher();
    this.modelRouter = new ModelRouter();
    this.setupRoutes();
  }

  private setupRoutes() {
    this.app.use(express.json());

    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', service: 'brain' });
    });

    // Streaming chat endpoint
    this.app.post('/api/v1/chat/stream', this.handleChatStream.bind(this));

    // Tool execution status
    this.app.get('/api/v1/tools/status', this.getToolStatus.bind(this));
  }

  private async handleChatStream(req: Request, res: Response) {
    const { message, conversationId } = req.body;
    const sessionId = conversationId || uuid();

    // Load conversation history + memory
    const history = await this.memory.getConversation(sessionId);
    const relevantMemories = await this.memory.search(message, limit=5);

    // Build system prompt from operating_system/
    const systemPrompt = SystemPromptBuilder.build({
      soul: await this.loadConfig('SOUL.md'),
      brain: await this.loadConfig('BRAIN.md'),
      memories: relevantMemories,
      tools: this.toolDispatcher.getToolDescriptions(),
    });

    // Route to appropriate model based on message type
    const role = await MessageClassifier.classify(message);
    const model = this.modelRouter.getModel(role);

    // Stream response with tool calling
    const stream = await model.chatStream({
      system: systemPrompt,
      messages: history,
      user: message,
      tools: this.toolDispatcher.getToolSchemas(),
    });

    // Set up SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    let fullResponse = '';
    let toolCalls = [];

    for await (const chunk of stream) {
      if (chunk.type === 'text') {
        fullResponse += chunk.content;
        res.write(`data: ${JSON.stringify({ type: 'text', content: chunk.content })}\n\n`);
      } else if (chunk.type === 'tool_use') {
        toolCalls.push(chunk.tool);
        res.write(`data: ${JSON.stringify({ type: 'tool_use', tool: chunk.tool })}\n\n`);
      }
    }

    // Execute tools and continue loop (max 10 iterations)
    let iteration = 0;
    while (toolCalls.length > 0 && iteration < 10) {
      iteration++;
      const results = await this.toolDispatcher.executeAll(toolCalls);

      // Send tool results back to model
      const toolStream = await model.chatStream({
        system: systemPrompt,
        messages: [...history, { role: 'assistant', content: fullResponse }, {
          role: 'tool',
          content: JSON.stringify(results)
        }],
        tools: this.toolDispatcher.getToolSchemas(),
      });

      toolCalls = [];
      for await (const chunk of toolStream) {
        // ... similar handling
      }
    }

    // Persist conversation
    await this.memory.saveConversation(sessionId, [
      ...history,
      { role: 'user', content: message },
      { role: 'assistant', content: fullResponse }
    ]);

    // Fire-and-forget: extract observations for long-term memory
    this.observer.extractObservations(sessionId, fullResponse);

    res.write(`data: ${JSON.stringify({ type: 'done' })}\n\n`);
    res.end();
  }

  private async loadConfig(filename: string): Promise<string> {
    // Read from ConfigMap (K8s) or local file
    const path = process.env.CONFIG_MOUNT_PATH || './operating_system';
    return fs.readFileSync(path + '/' + filename, 'utf-8');
  }
}
```

### 2.3 BSL Tool Adapter

**brain/src/tools/BSLToolAdapter.ts** — Wrap BSL research as agent tools:
```typescript
export class BSLToolAdapter {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.BSL_API_URL || 'http://localhost:5000';
  }

  async conductResearch(params: { query: string; output_dir?: string }) {
    const response = await fetch(`${this.baseUrl}/api/v1/research/conduct`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': 'bsl-local-dev-key' },
      body: JSON.stringify(params),
    });
    return response.json();
  }

  async getSystemStatus() {
    const response = await fetch(`${this.baseUrl}/api/v1/system/status`);
    return response.json();
  }

  async getReport(reportId: string) {
    const response = await fetch(`${this.baseUrl}/api/v1/reports/${reportId}`);
    return response.json();
  }
}

// Register as tool
toolRegistry.register({
  name: 'conduct_research',
  description: 'Execute a full research pipeline on a given query',
  parameters: {
    type: 'object',
    properties: {
      query: { type: 'string', description: 'Research question or topic' },
      output_dir: { type: 'string', description: 'Output directory' },
    },
    required: ['query'],
  },
  handler: async (params) => {
    const adapter = new BSLToolAdapter();
    return adapter.conductResearch(params);
  },
});
```

---

## Phase 3: Operating System Integration

### 3.1 ConfigMap Migration

The existing BSL uses `config/agents.yaml`. The new system adds `operating_system/` ConfigMap:

**Kubernetes manifest (k8s/overlays/bsl/operating_system-configmap.yaml)**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bakerst-os
  namespace: bakerst
data:
  SOUL.md: |
    # Baker Street Laboratory — Core Identity
    ...
  BRAIN.md: |
    # Tool Reference
    ...
  CRONS.json: |
    {
      "schedules": [
        { "id": "daily_digest", "cron": "0 9 * * *", "tool": "send_digest" },
        { "id": "model_health_check", "cron": "0 */6 * * *", "tool": "check_models" }
      ]
    }
  TRIGGERS.json: |
    {
      "triggers": [
        { "event": "research.completed", "action": "generate_summary" },
        { "event": "model.down", "action": "alert_admin" }
      ]
    }
```

### 3.2 Mount ConfigMap to Existing BSL Pods

**k8s/overlays/bsl/api-deployment-patch.yaml** (add to existing API):
```yaml
spec:
  template:
    spec:
      containers:
      - name: api
        volumeMounts:
        - name: operating-system
          mountPath: /app/operating_system
          readOnly: true
      volumes:
      - name: operating-system
        configMap:
          name: bakerst-os
```

---

## Phase 4: Build & Deployment Integration

### 4.1 Dockerfile Extensions

**Multi-stage build for Brain service**:

```dockerfile
# Baker Street Laboratory with integrated Brain service
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY brain/ ./brain/
COPY operating_system/ ./operating_system/
RUN npm run build:brain

# Production image
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/dist/brain ./brain-dist
COPY --from=builder /app/operating_system ./operating_system
COPY api/ ./api
COPY requirements.txt .
COPY framework/ ./framework
COPY implementation/ ./implementation

# Install Python dependencies for BSL core
RUN apk add --no-cache python3 py3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose both API (5000) and Brain (30000)
EXPOSE 5000 30000

# Start both services (or use separate pods)
CMD ["sh", "-c", "uvicorn api.app:app --host 0.0.0.0 --port 5000 & node brain-dist/index.js"]
```

### 4.2 Kustomize Overlay

```
k8s/
├── base/                          # Base BSL manifests (existing)
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    └── baker-street-merged/       # NEW - Merged deployment
        ├── kustomization.yaml
        ├── brain-deployment.yaml
        ├── brain-service.yaml
        ├── nats-deployment.yaml
        ├── qdrant-deployment.yaml
        └── patches/
            └── api-deployment-patch.yaml  # Mount operating_system
```

**kustomization.yaml**:
```yaml
resources:
  - ../../base

configMapGenerator:
  - name: bakerst-os
    files:
      - SOUL.md=../../operating_system/SOUL.md
      - BRAIN.md=../../operating_system/BRAIN.md
      - CRONS.json=../../operating_system/CRONS.json
      - TRIGGERS.json=../../operating_system/TRIGGERS.json

patchesStrategicMerge:
  - patches/api-deployment-patch.yaml

generators:
  - brain-config.yaml
```

### 4.3 Deployment Script Integration

Update `scripts/deploy-all.sh` to include:
```bash
#!/bin/bash
# ... existing code ...

# Step 1: Deploy BSL base (API, models)
echo "🚀 Deploying Baker Street Laboratory core..."
kubectl apply -k k8s/overlays/baker-street-merged/

# Step 2: Wait for BSL API
echo "⏳ Waiting for BSL API..."
kubectl wait --for=condition=ready pod -l app=bsl-api -n bakerst --timeout=300s

# Step 3: Deploy Brain service
echo "🧠 Deploying Brain agent orchestrator..."
kubectl apply -f brain-deployment.yaml

# Step 4: Wait for Brain
kubectl wait --for=condition=ready pod -l app=brain -n bakerst --timeout=120s

# Step 5: Bootstrap feature files (from baker-street project)
echo "📦 Bootstrapping features..."
NATS_PORT=$(kubectl get svc nats -o jsonpath='{.spec.ports[0].nodePort}')
node scripts/bootstrap-features.mjs --nats-address localhost:${NATS_PORT}

echo "✅ Deployment complete!"
```

---

## Phase 5: Prompt Engineering Integration

### 5.1 System Prompt Construction

The Brain builds system prompts from multiple sources:

```
SYSTEM_PROMPT = [
  SOURCES:
    operating_system/SOUL.md           # 1. Identity (loaded once)
    operating_system/BRAIN.md          # 2. Tool docs (loaded once)
    Role-specific prompt               # 3. Based on message classifier
    operating_system/SKILL-EXT-*.md   # 4. Active skills documentation
    Memory context (retrieved)         # 5. Relevant memories
    Current time + environment         # 6. Temporal context
    Recent observations                # 7. Active decision log
].join('\n\n')
```

**SystemPromptBuilder.ts**:
```typescript
export class SystemPromptBuilder {
  static async build(params: {
    soul: string;
    brain: string;
    role: string;
    memories: MemoryItem[];
    observations: Observation[];
    activeSkills: string[];
  }): string {
    const sections = [
      params.soul,
      params.brain,
      this.buildRoleSection(params.role),
      this.buildMemorySection(params.memories),
      this.buildObservationSection(params.observations),
      this.buildSkillSection(params.activeSkills),
      this.buildCurrentContext(),
    ];

    return sections.filter(Boolean).join('\n\n---\n\n');
  }

  private static buildRoleSection(role: string): string {
    const roles = {
      agent: `You are now in AGENT MODE — use tools to accomplish tasks. Think step by step.`,
      conversational: `You are now in CONVERSATIONAL MODE — respond naturally without tools.`,
      observer: `You are now in OBSERVER MODE — extract structured observations.`,
      reflector: `You are now in REFLECTOR MODE — compress and consolidate memories.`,
    };
    return roles[role as keyof typeof roles] || roles.agent;
  }

  private static buildMemorySection(memories: MemoryItem[]): string {
    if (memories.length === 0) return '';
    const formatted = memories.map((m, i) => `[${i + 1}] ${m.content} (confidence: ${m.confidence})`).join('\n');
    return `## Relevant Context\n${formatted}`;
  }
}
```

### 5.2 Role-Based Model Routing

Use `ModelRouter` to assign different models to different tasks:

```typescript
// packages/shared/src/model-types.ts
export interface ModelRouterConfig {
  roles: {
    agent: { provider: 'anthropic' | 'openai' | 'ollama'; model: string; },
    conversational: { provider: 'openai'; model: 'gpt-3.5-turbo'; },
    observer: { provider: 'openai'; model: 'gpt-4o-mini'; },
    reflector: { provider: 'anthropic'; model: 'claude-3-sonnet'; },
    reasoner: { provider: 'anthropic'; model: 'claude-3-opus'; },
  };
}
```

This saves cost + improves latency:
- Simple greetings → `conversational` (fast, cheap model)
- Research queries → `agent` (full reasoning + tools)
- Background memory work → `observer`/`reflector` (async)

---

## Phase 6: Testing & Validation

### 6.1 Prompt Test Suite

Create `brain/test/prompt-tests/`:
```typescript
// test/prompt-tests/tool-selection.test.ts
describe('Tool Selection', () => {
  test('should choose conduct_research for research queries', async () => {
    const response = await brain.chat({
      message: 'What are the latest findings on CRISPR gene editing?',
    });
    expect(response.toolCalls[0].name).toBe('conduct_research');
  });

  test('should refuse to fabricate citations', async () => {
    const response = await brain.chat({
      message: 'Make up some fake studies about alien life.',
    });
    expect(response.text).toContain('cannot fabricate');
  });
});
```

### 6.2 Integration Tests

```typescript
// test/integration/bsl-bridge.test.ts
describe('BSL Bridge', () => {
  test('should forward research query to BSL API', async () => {
    const result = await brain.executeTool('conduct_research', {
      query: 'quantum computing applications',
    });
    expect(result.status).toBe('completed');
    expect(result.report_path).toMatch(/\.md$/);
  });

  test('should parse BSL research report and extract key findings', async () => {
    const report = await brain.getReport(reportId);
    const summary = brain.synthesize(report);
    expect(summary.confidence).toBeGreaterThan(0.7);
  });
});
```

---

## Phase 7: Implementation Roadmap

### Week 1-2: Basic Agent Layer
- [ ] Create `brain/` directory and project scaffold
- [ ] Build Brain.ts agent loop with streaming SSE
- [ ] Implement `SystemPromptBuilder` from SOUL.md + BRAIN.md
- [ ] Add MessageClassifier (simple rule-based)
- [ ] Create BSLToolAdapter (wrap existing API endpoints)
- [ ] Deploy alongside BSL API (same pod or separate)

**Deliverable**: `http://localhost:30000/chat` endpoint alongside existing `:5000/api/v1`

### Week 3-4: Memory & Observational Learning
- [ ] Integrate SQLite for conversation history
- [ ] Add Qdrant vector store (reuse existing `data/vector_store/`)
- [ ] Implement Observer to extract structured observations from BSL research outputs
- [ ] Implement Reflector to compress memory logs
- [ ] Add memory recall to system prompt

**Deliverable**: Agent remembers past conversations and research findings

### Week 5-6: Multi-Model Routing & Tool Expansion
- [ ] Implement ModelRouter with role-based selection
- [ ] Map BSL's 8 models to tool calls (vision → analyze_image, embed → semantic_search, etc.)
- [ ] Add local tools (transform, data analysis) as Tier-0
- [ ] Add async job dispatch for long-running research (Tier-2)
- [ ] Create tool schema definitions for LLM function calling

**Deliverable**: Correct tool selection across all 8 model types

### Week 7-8: Kubernetes & Observability
- [ ] Write Kubernetes manifests for Brain, NATS, Qdrant
- [ ] Create Kustomize overlay for merged deployment
- [ ] Setup NetworkPolicy (brain can reach BSL API, no external ingress except gateway)
- [ ] Add OpenTelemetry instrumentation (spans for tool calls, LLM latency)
- [ ] Deploy to kind cluster for testing

**Deliverable**: Full K8s deployment with `kubectl apply -k k8s/overlays/merged`

### Week 9-10: Gateway & Channels
- [ ] Create Gateway service (Node.js) that bridges:
  - HTTP API (web UI)
  - Telegram bot
  - Discord bot
- [ ] Implement per-channel conversation mapping
- [ ] Add message length splitting for Telegram/Discord
- [ ] Enforce door policies (allowlist chat IDs)
- [ ] Deploy gateway alongside Brain

**Deliverable**: Multi-channel access to your BSL agent

### Week 11-12: Features, Extensions & Polish
- [ ] Create Features pod (bakerst-features) for modular capabilities
- [ ] Migrate code review, obsidian, toolbox as features
- [ ] Implement extension auto-discovery via NATS
- [ ] Add feature admin API (activate/rollback versions)
- [ ] Comprehensive testing & prompt refinement
- [ ] Documentation updates

**Deliverable**: Extensible plugin system with hot-reload capability

---

## Directory Structure of Merged System

```
Baker-Street-Laboratory-1/
├── api/                            # Existing Flask API
├── brain/                          # NEW - Agent orchestrator (TypeScript)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── gateway/                        # NEW - Multi-channel gateway (TypeScript)
│   ├── src/
│   └── Dockerfile
├── worker/                         # NEW - Job execution pool (TypeScript)
│   ├── src/
│   └── Dockerfile
├── operating_system/               # NEW - Prompt layer
│   ├── SOUL.md
│   ├── BRAIN.md
│   ├── CRONS.json
│   └── TRIGGERS.json
├── framework/                      # Enhanced (reuse polymorphic framework)
│   ├── polymorphic_framework.py    # Keep, add agent bridge
│   └── breakthrough_integration.py
├── implementation/                 # Existing Python core
│   ├── src/
│   │   ├── ai/ollama_client.py
│   │   ├── core/
│   │   ├── database/
│   │   └── orchestrator/
├── config/                         # Existing configs (augmented)
│   ├── agents.yaml                # BSL agent configs
│   └── model-profiles/            # Ollama model profiles
├── data/                          # Existing data dir
│   ├── vector_store/              # Reuse for memory
│   └── cache/
├── k8s/                           # Kubernetes manifests
│   ├── base/
│   │   ├── api-deployment.yaml
│   │   ├── bsl-service.yaml
│   │   ├── pvc.yaml
│   │   └── configmap.yaml
│   └── overlays/
│       └── merged/
│           ├── kustomization.yaml
│           ├── brain-deployment.yaml
│           ├── gateway-deployment.yaml
│           ├── nats-deployment.yaml
│           ├── qdrant-deployment.yaml
│           └── patches/
│               └── api-patch.yaml   # Mount operating_system
├── scripts/
│   ├── deploy-all.sh             # Enhanced for multi-service
│   ├── build.sh                   # Build all services
│   ├── bootstrap-features.mjs     # From Baker Street Project
│   └── setup-k8s.sh              # Cluster setup
├── docker-compose.yml            # NEW - For local dev (all services)
├── research/                     # Existing research outputs
├── research_app/                 # Existing Flutter UI
├── desktop-app/                  # Existing Electron UI
├── requirements.txt
├── package.json                  # Root workspace (monorepo)
├── pnpm-workspace.yaml           # For TypeScript services
├── tsconfig.base.json
├── .env
└── README.md                     # Updated with merged capabilities
```

---

## Command-Line Integration

Extend existing `run.sh` to include brain commands:

```bash
#!/bin/bash
# Baker Street Laboratory - Enhanced Run Script

# ... existing commands ...

case "$command" in
  "research")
    # Existing research pipeline
    python3 implementation/src/main.py --mode research --query "$@"
    ;;

  "agent")
    # NEW: Start conversational agent
    echo "Starting Brain agent..."
    cd brain && npm start
    ;;

  "gateway")
    # NEW: Start multi-channel gateway
    echo "Starting Gateway..."
    cd gateway && npm start
    ;;

  "fullstack")
    # Start everything (BSL API + Brain + Gateway)
    echo "Starting full Baker Street stack..."
    # Use tmux or docker-compose
    docker-compose up -d
    ;;

  "deploy")
    # Deploy to Kubernetes
    KUSTOMIZE_OVERLAY=merged scripts/deploy-all.sh
    ;;
esac
```

---

## Local Development Setup

### Step 1: Prepare Environment

```bash
cd /home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1

# Install Python dependencies (existing)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install Node.js dependencies (new)
cd brain
npm install
cd ../gateway
npm install
cd ../worker
npm install

# Install pnpm workspace (optional)
npm install -g pnpm
```

### Step 2: Create Operating System Prompts

```bash
# Create operating_system/ directory
mkdir -p operating_system/personalities

# Copy the prompts I provided (see Phase 1 above)
# Edit for your specific personality/preferences
nano operating_system/SOUL.md
nano operating_system/BRAIN.md
```

### Step 3: Configure Environment

Update `.env`:
```bash
# Existing BSL variables
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# NEW — Brain service
BRAIN_MODEL=anthropic/claude-3-opus
BRAIN_SYSTEM_PROMPT_PATH=/app/operating_system/SOUL.md
BSL_API_URL=http://localhost:5000
NATS_URL=nats://localhost:4222

# Memory
QDRANT_URL=http://localhost:6333
SQLITE_PATH=/app/data/bakerst.db
```

### Step 4: Local Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bsl-api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "5000:5000"
    volumes:
      - ./operating_system:/app/operating_system:ro
      - ./data:/app/data
      - ./research:/app/research
    environment:
      - PYTHONUNBUFFERED=1
    command: uvicorn api.app:app --host 0.0.0.0 --port 5000

  brain:
    build:
      context: .
      dockerfile: Dockerfile.brain
    ports:
      - "30000:30000"
    volumes:
      - ./operating_system:/app/operating_system:ro
      - ./data:/app/data
    depends_on:
      - bsl-api
      - nats
      - qdrant
    environment:
      - BSL_API_URL=http://bsl-api:5000
      - NATS_URL=nats://nats:4222
      - QDRANT_URL=http://qdrant:6333

  gateway:
    build:
      context: .
      dockerfile: Dockerfile.gateway
    ports:
      - "8080:8080"
    depends_on:
      - brain
    environment:
      - BRAIN_URL=http://brain:30000

  nats:
    image: nats:2.10-alpine
    ports:
      - "4222:4222"
    command: ["nats-server", "-js", "-m", "8222"]

  qdrant:
    image: qdrant/qdrant:v1.9.0
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama

volumes:
  qdrant_data:
  ollama:
```

### Step 5: Build & Run Locally

```bash
# Build all services
docker-compose build

# Start everything
docker-compose up -d

# Check status
docker-compose ps

# Access points:
# - BSL API: http://localhost:5000/api/v1/docs
# - Brain chat: http://localhost:30000/chat
# - Gateway (web UI): http://localhost:8080
# - NATS monitoring: http://localhost:8222

# View logs
docker-compose logs -f brain
docker-compose logs -f bsl-api
```

### Step 6: Quick Integration Test

```bash
# 1. Verify BSL API is running
curl http://localhost:5000/api/v1/system/health

# 2. Test brain chat endpoint
curl -N -X POST http://localhost:30000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! What can you help me research today?"}'

# 3. Test research tool via brain
curl -X POST http://localhost:30000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Conduct research on quantum entanglement applications in cryptography"}'

# 4. Check memory recall
curl http://localhost:30000/api/v1/memory/search?q=quantum

# 5. Verify models are operational
curl http://localhost:30000/api/v1/tools/status
```

---

## Data Flow Examples

### Example 1: Research Query

```
User → Gateway (HTTP POST /chat)
      ↓
Brain (/api/v1/chat/stream)
  - Load conversation history
  - Classify message as "agent" mode
  - Search memory for "quantum cryptography"
  - Build system prompt (SOUL + BRAIN + memories)
  - Call Claude with tools
  ↓
Claude: "I'll use the conduct_research tool"
Brain: Executes → POST /api/v1/research/conduct to BSL API
      ↓
BSL API: Enqueues research job (status: "processing")
      ↓
Brain: Immediately responds with "I'm starting that research..."
      ↓
BSL Worker (async):
  - Analyzes query
  - Splits into sub-queries
  - Runs vision/embed/scientific/coder models in parallel
  - Synthesizes report
  - Saves to research/output/
      ↓
Brain: Polls job status or receives NATS notification
      ↓
Brain: "Research complete! Here's the summary..."
      ↓
User: Receives streaming response
```

### Example 2: Image Analysis

```
User uploads fMRI scan
      ↓
Brain: Detects image → selects "vision" tool
      ↓
Calls BSL API /api/v1/vision/analyze with image
      ↓
BSL: LLaVA model processes image, returns structured JSON
      ↓
Brain: "The image shows increased activation in prefrontal cortex..."
      ↓
User: Gets detailed analysis with citations
```

---

## Key Configuration Points

### 1. Service Discovery

Use **NATS service discovery** (Baker Street approach) OR **Kubernetes Services** (simpler):

For BSL integration, K8s services are sufficient:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: bsl-api
spec:
  selector:
    app: bsl-api
  ports:
  - port: 5000
    targetPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: brain
spec:
  selector:
    app: brain
  ports:
  - port: 30000
    targetPort: 30000
```

Brain connects to BSL via `http://bsl-api:5000` (K8s DNS).

### 2. Persistence

Reuse existing BSL data directories:
```yaml
volumes:
  - name: bsl-data
    persistentVolumeClaim:
      claimName: bsl-data-pvc

containers:
  - name: bsl-api
    volumeMounts:
    - name: bsl-data
      mountPath: /app/data
  - name: brain
    volumeMounts:
    - name: bsl-data
      mountPath: /app/data  # Shared vector_store & SQLite
```

### 3. Security

- Use existing BSL auth middleware (`auth_middleware.py`)
- Brain service inherits BSL's `AUTH_TOKEN` from ConfigMap
- NetworkPolicy restricts brain → bsl-api only (no reverse)
- All traffic within namespace (K8s network policies)

---

## Monitoring & Observability

### Metrics Collection

Expose Prometheus metrics from Brain:

```typescript
import { collectDefaultMetrics, Counter, Histogram } from 'prom-client';

collectDefaultMetrics();

const chatRequests = new Counter({
  name: 'brain_chat_requests_total',
  help: 'Total chat requests',
  labelNames: ['role', 'tool_used'],
});

const toolLatency = new Histogram({
  name: 'brain_tool_latency_seconds',
  help: 'Tool execution latency',
  labelNames: ['tool_name'],
});

// Instrument endpoints
app.post('/api/v1/chat', async (req, res) => {
  chatRequests.inc({ role: role });
  const end = toolLatency.startTimer({ tool_name: tool.name });
  // ... handle request
  end();
});
```

Scrape alongside BSL metrics via Prometheus.

### OpenTelemetry Traces

Trace across services:
```
Request → Brain (span) → BSL API (span) → Ollama (span) → Brain
         ↓
    Store in Tempo
```

---

## Rollback & Versioning

### Blue-Green Deployments

Existing BSL may already have deployment strategy. For Brain:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: brain
spec:
  replicas: 2
  strategy:
    blueGreen:
      activeService:
        name: brain-active
      previewService:
        name: brain-preview
      autoPromotionSeconds: 30
```

### Database Migrations

If Brain introduces new SQLite schema (conversations table), handle via init container:

```yaml
initContainers:
- name: migrate-db
  image: brain:latest
  command: ['node', 'dist/migrate.js']
  envFrom:
    - configMapRef:
        name: brain-config
```

---

## Common Issues & Troubleshooting

### 1. ConfigMap Not Reflected

**Problem**: Updating `operating_system/SOUL.md` doesn't affect running Brain.

**Solution**:
```bash
# Restart Brain pod to pick up new ConfigMap
kubectl rollout restart deployment/brain -n bakerst

# Or use ConfigMap hot-reload (requires volume mount with subPath)
kubectl delete pod brain-xxxx  # Pod will recreate with new ConfigMap
```

### 2. Memory (SQLite) Locked

**Problem**: Multiple Brain instances writing to same SQLite file.

**Solution**: Use WAL mode + connection pooling:
```sql
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=30000;
```

Or use separate databases per Brain instance + periodic sync.

### 3. Tool Timeouts

**Problem**: `conduct_research` hangs indefinitely.

**Solution**: Implement timeout + async notification:
```typescript
const jobId = await submitResearchJob(query);
const result = await waitForCompletion(jobId, { timeout: 300_000 }); // 5 min

// Instead of synchronous wait, Brain can:
// 1. Return immediately with "Research started"
// 2. Subscribe to NATS subject for job completion
// 3. Push notification to user when done
```

### 4. Model Cold Starts

**Problem**: First Ollama inference takes 10+ seconds.

**Solution**: Keep models warm with periodic health checks:
```yaml
livenessProbe:
  exec:
    command: ["curl", "-f", "http://localhost:11434/api/tags"]
  initialDelaySeconds: 30
  periodSeconds: 60
```

Or use smaller models for frequent tasks.

---

## Validation Checklist

Before declaring merge complete:

- [ ] SOUL.md defines agent identity + principles
- [ ] BRAIN.md documents ALL available tools with examples
- [ ] Brain service starts and responds to `/health`
- [ ] BSL API reachable from Brain pod
- [ ] `conduct_research` tool successfully called
- [ ] Research report generated and displayed in chat
- [ ] Conversation history persists across restarts
- [ ] Memory recall: brain can reference past research
- [ ] Observations extracted and stored
- [ ] Reflector compacts old memories
- [ ] Role-based model routing works
- [ ] Local tools (transform) execute instantly
- [ ] Remote tools (research) run async with status updates
- [ ] Gateway exposes Telegram/Discord
- [ ] Prometheus metrics scraping successful
- [ ] Traces visible in Tempo/Grafana
- [ ] NATS connection stable
- [ ] NetworkPolicy allows brain→bsl-api, denies others
- [ ] ConfigMap updates trigger deployment (optional)
- [ ] Docker builds succeed for all services
- [ ] `docker-compose up` starts full stack
- [ ] `kubectl apply -k k8s/overlays/merged` deploys without errors
- [ ] Smoke tests pass (see Phase 6)

---

## Next Steps After Merge

Once core integration is complete, consider:

1. **Advanced Features**:
   - Autonomous research loops (brain asks follow-up questions)
   - Multi-agent teams (delegate different research phases to specialized agents)
   - Active learning (brain identifies knowledge gaps and initiates research)
   - Collaborative filtering (combine results from multiple models)

2. **Scaling**:
   - Horizontal pod autoscaling for Brain based on request latency
   - Separate worker pools per tool type
   - Sharded vector store for large memory

3. **User Experience**:
   - Web UI (React) for chat interface
   - Voice interface integration
   - Mobile app (Flutter) integration
   - Progress notifications (email/Telegram)

4. **Enterprise**:
   - Multi-tenancy (separate research projects)
   - Access control (read/write per research domain)
   - Audit logging (all tool calls logged)
   - SOC2 compliance tooling

---

## Summary

This merger transforms **Baker Street Laboratory** from a **research pipeline** into a **full-fledged AI agent platform**.

**Before**: User submits query → wait for report → read output
**After**: User chats with agent → agent orchestrates models → streaming updates → interactive refinement

The integration preserves your existing 8-model AI investment while adding:
- Conversational UX
- Tool orchestration
- Memory & learning
- Multi-channel access
- Production deployment patterns
- Observability & scaling

All built on proven Baker Street Project architecture (NATS, blue-green, defense-in-depth) while keeping your Python AI core intact.
