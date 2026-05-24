# Baker Street Laboratory — Merged Architecture

## Overview

Baker Street Laboratory (BSL) + Baker Street Project merge brings **conversational AI agent capabilities** to your existing multi-model research platform.

```
Before: Research Pipeline Only
  User → Submit query → Batch analysis → PDF report

After: Conversational Agent + Research Pipeline
  User ↔ Chat with agent ↔ Real-time tool use ↔ Hybrid mode (agent + auto-research)
```

---

## Component Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                              │
│  • Web UI (React on :8080)                                        │
│  • CLI / API curl                                                │
│  • Telegram / Discord (gateway)                                  │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────────┐
│                         GATEWAY SERVICE                             │
│  Multi-channel adapter, routing, door policies                    │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────────┐
│                         BRAIN AGENT                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐  │
│  │Conversational│ │   Tool     │  │   Memory                │  │
│  │   Loop       │ │Dispatcher  │  │ (SQLite + Qdrant)       │  │
│  └─────────────┘  └──────────────┘  └─────────────────────────┘  │
│         │                  │                     │                │
│         │  System Prompt (SOUL.md + BRAIN.md) │                │
│         └─────────────────┼─────────────────────┘                │
│                           ▼                                       │
│                  ┌────────────────────┐                           │
│                  │   MODEL ROUTER     │  ← 4 roles               │
│                  │ agent|conversational│  ← different models     │
│                  └─────────┬──────────┘                           │
│                            │                                       │
│           ┌────────────────┼────────────────┐                     │
│           │                │                │                     │
│           ▼                ▼                ▼                     │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│    │ Anthropic│    │  OpenAI  │    │  Ollama  │                 │
│    │ Claude   │    │ GPT-4    │    │ Llama    │                 │
│    └──────────┘    └──────────┘    └──────────┘                 │
└───────────────────────────┬───────────────────────────────────────┘
                            │ Tool calls
                            ▼
┌───────────────────────────────────────────────────────────────────┐
│                     TOOL ADAPTER LAYER                              │
│  BSLToolAdapter → BSL API (Flask) → AI Models (8× Ollama)        │
└───────────────────────────────────────────────────────────────────┘
```

---

## Data Flows

### 1. Chat Request (Streaming)

```
User → POST /api/v1/chat/stream
  ↓
Brain:
  1. Load conversation history from SQLite
  2. Semantic-search Qdrant for relevant memories
  3. Build system prompt (SOUL + BRAIN + context)
  4. Classify role → pick model
  5. Stream LLM tokens while detecting tool calls
  6. Execute tools via BSLToolAdapter
  7. Append tool results & continue (loop ≤10)
  8. Persist conversation + fire observer
  ↓
SSE stream: text chunks → tool_use → done
```

### 2. Research Pipeline (Async)

```
User: "Research quantum cryptography"
   ↓
Brain: message_classifier → 'agent' role
   ↓
Tool picker: "conduct_research"
   ↓
BSL API: /api/v1/research/conduct
   ↓
BSL ResearchOrchestrator:
  ├─ analyze_query
  ├─ collect_data (calls vision, embed, scientific, coder)
  ├─ synthesize
  └─ generate_report
   ↓
Job status: "running" → "completed"
   ↓
Brain polls / receives NATS notification
   ↓
Response: "Research complete. Summary: ..."
```

### 3. Memory Consolidation

```
Every conversation end → Observer extracts observations
Observations stored in Qdrant + SQLite

When observation_log > 200 items → Reflector runs
Refractor groups by type+date → creates summaries
Old items deleted, summaries kept
```

---

## Service Map

| Service | Port | Role | Tech |
|---------|------|------|------|
| **bsl-api** | 5000 | Existing research API (Flask) | Python |
| **brain** | 30000 | Agent orchestrator (new) | TypeScript |
| **gateway** | 8080 | Multi-channel adapter (new) | TypeScript |
| **worker** | 30001 | Job execution pool (future) | TypeScript |
| **nats** | 4222 | Message bus | Go |
| **qdrant** | 6333 | Vector memory | Rust |
| **ollama** | 11434 | Local LLM provider | Go |

---

## Configuration

### operating_system/ — The Prompt Layer

```
operating_system/
├── SOUL.md              # Identity, principles, ethics
├── BRAIN.md             # Tool documentation + decision trees
├── CRONS.json           # Scheduled tasks (daily digest, health checks)
├── TRIGGERS.json        # Event-driven automation
├── PLUGINS.json         # MCP plugin registry
└── personalities/       # Optional: alternate personas
    ├── detective.md    # Sherlock-style
    ├── scientist.md    # Research scientist
    └── engineer.md     # DevOps engineer
```

These files are mounted as a Kubernetes ConfigMap and loaded by Brain at startup. Edit them to customise agent personality and behaviour without code changes.

### Role-based Model Routing

Configured in `brain/src/agent/ModelRouter.ts`:

```typescript
{
  agent:         { provider: 'anthropic', model: 'claude-3-opus' },   // complex tasks
  conversational:{ provider: 'openai',    model: 'gpt-3.5-turbo' }, // chit-chat
  observer:      { provider: 'openai',    model: 'gpt-4o-mini' },   // extraction
  reflector:     { provider: 'anthropic', model: 'claude-3-sonnet'},// compression
  reasoner:      { provider: 'anthropic', model: 'claude-3-opus' }  // deep think
}
```

Adjust to use local Ollama models for cost savings.

---

## Tool Execution Tiers

| Tier | Tool | Transport | Latency | Example |
|------|------|-----------|---------|---------|
| 0 | `semantic_search`, `query_database` | Local function | Instant | Vector search |
| 1 | `generate_code`, `review_code` | Python subprocess | <5s | Code without network |
| 2 | `conduct_research`, `batch_analyze_images` | HTTP → BSL API | 2min | Multi-model pipeline |
| 3 | `execute_code`, `create_visualization` | Worker job (future) | async | Heavy/long-running |

---

## Memory System

### SQLite (`bakerst.db`)

- `conversations` — sessions, metadata
- `messages` — full history
- `observations` — extracted facts/decisions/preferences

### Qdrant (`bakerst_memories` collection)

- 1024-dim vectors (Nomic Embed)
- Cosine similarity
- Automatic dedup (>92% similarity)
- Serves RAG retrieval for all conversations

### Observer + Reflector

**Observer** (runs after each turn):
- Extracts: `{type: "decision"|"preference"|"fact"|...}`  
- Stores in SQLite + Qdrant

**Reflector** (runs when >200 observations):
- Compacts old entries into summaries
- Removes superseded/duplicate observations
- Keeps context window lean

---

## Extending with New Tools

Add a tool in `brain/src/tools/ToolDispatcher.ts`:

```typescript
this.registry.register('my_tool', {
  description: 'What this tool does',
  parameters: {
    type: 'object',
    properties: {
      param: { type: 'string', description: 'Parameter' },
    },
    required: ['param'],
  },
  handler: async (params) => {
    // Call BSL API or external service
    const response = await fetch('...');
    return response.json();
  },
});
```

Or expose a BSL endpoint directly:
- Add new route in `api/app.py`
- Add wrapper in `BSLToolAdapter.ts`
- Register in ToolDispatcher init

---

## Deployment Options

### Option A: Direct (development)

```bash
./deploy-all.sh local
# BSL API on :5000, Brain on :30000, Gateway on :8080
```

### Option B: Docker Compose

```bash
./deploy-all.sh docker
```

### Option C: Kubernetes

```bash
./deploy-all.sh k8s
# Uses k8s/overlays/merged with Kustomize
```

Set environment:
```bash
export KUSTOMIZE_OVERLAY=staging   # or production
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-...
```

---

## Monitoring

### Health Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` (brain) | Liveness probe |
| `GET /api/v1/tools/status` | Tool availability |
| `GET /api/v1/system/status` (BSL) | Model status, GPU memory |
| `:8222` (NATS) | NATS monitoring UI |
| `:6333/dashboard` (Qdrant) | Vector store stats |

### Logs

```bash
# Direct mode
tail -f logs/bsl_api.log logs/brain.log logs/gateway.log

# Docker
docker-compose logs -f brain

# K8s
kubectl -n bakerst logs -f deployment/brain
```

### Metrics (enable with monitoring profile)

```bash
docker-compose --profile monitoring up -d
# Prometheus on :9090, Grafana on :3001
```

---

## Troubleshooting

### Brain can't connect to BSL API

Check:
```bash
curl http://localhost:5000/api/v1/system/status
# If down: source .venv/bin/activate && python3 implementation/src/main.py
```

### Tools show unavailable

Run `GET /api/v1/tools/status` and check `error` field. Usually:
- Ollama not running: `ollama serve`
- Model not loaded: `ollama pull <model>`
- API key missing: check `.env`

### Memory search returns nothing

Vector store empty. Ingest documents first:
```bash
curl -X POST http://localhost:30000/api/v1/tools/execute \
  -d '{"name":"ingest_document","parameters":{"file_path":"/path/to/paper.pdf"}}'
```

### Conversations not persisting

Check SQLite file exists: `ls data/bakerst.db`. Ensure write permissions.

### GPU not detected

Ollama uses CUDA automatically if NVIDIA drivers installed. Verify with:
```bash
docker exec bsl-ollama ollama run llama2
# Should show GPU layers
```

---

## Development Workflow

1. Edit prompts → restart Brain (direct mode) or `kubectl rollout restart deployment/brain`
2. Add tool → modify `ToolDispatcher.ts` → rebuild (`pnpm build`) → restart
3. Debug conversation → check SQLite: `sqlite3 data/bakerst.db "SELECT * FROM messages LIMIT 10"`
4. View memories → Qdrant dashboard: `http://localhost:6333/dashboard`

---

## What Changed — Before vs After

| Aspect | Before (BSL only) | After (Merged) |
|--------|-------------------|----------------|
| Interface | Batch research API | Streaming chat + tools |
| Memory | File outputs only | Persistent vector store + SQLite |
| Multi-modal | Single query → report | Multi-turn conversation + follow-ups |
| Automation | Manual runs | Scheduled + event-driven |
| Access | curl only | Web UI + Telegram + Discord |
| Extensibility | Add new Python scripts | MCP plugins + dynamic tool registry |
| Deployment | Single Python app | Microservices (brain, gateway, workers) |

---

## License

Same as existing Baker Street Laboratory (PROPRIETARY / Enterprise).

---

**Ready to chat?** `./deploy-all.sh local` then `curl -X POST http://localhost:30000/api/v1/chat -d '{"message":"Hello!"}'`
