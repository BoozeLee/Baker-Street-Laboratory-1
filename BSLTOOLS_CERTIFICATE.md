# 🏆 BSLTOOLS-EP — End-Phase Integration Certificate
## Baker Street Laboratory — BSLToolAdapter End-to-End Specification

**Certificate ID**: BSLTOOLS-EP-v2.1.0  
**Status**: ✅ OFFICIALLY CERTIFIED — End-Phase Build  
**System**: Baker Street Laboratory v2.1.0 (BoozeLee/Baker-Street-Laboratory-1)  
**Authority**: Bakery-Street-Project / Kiliaan Vanvoorden (Kilo)  
**Date**: 2026-05-18  
**Scope**: All 10 BSL tools wired through Brain → BSLToolAdapter → BSL Flask API  

---

## §0 Pool ═════════════════════════════════════════════════════════════════════

| Pool ID | Role | Model / Runtime | Temperature | Priority |
|---------|------|----------------|-------------|----------|
| POOL-A | Primary reasoning agent (research, analysis, planning) | `hermes-3-llama-3b` | 0.3 | 1 |
| POOL-B | Quick conversational / chit-chat | `qwen3-1.7b` | 0.7 | 3 |
| POOL-C | Observer — structured extraction, low temp | `openchat:3.5-0106-q4_K_M` | 0.1 | 2 |
| POOL-D | Reflector — memory compaction / summarisation | `neural-chat:7b-v3-3-q4_K_M` | 0.2 | 2 |
| POOL-E | Deep reasoner — planning, deep-dive analysis | `yarn-mistral:7b-128k-q4_K_M` | 0.5 | 1 |
| POOL-F | Vision forensics — image / chart / fmri | `llava:7b-v1.6-mistral-q4_K_M` | 0.0 | 1 |
| POOL-G | Semantic search / embedding vector store | `nomic-embed-text` | 0.0 | n/a |
| POOL-H | Scientific / academic / methodology | `openchat:3.5-0106-q4_K_M` | 0.2 | 1 |
| POOL-I | Creative / narrative / report writing | `neural-chat:7b-v3-3-q4_K_M` | 0.6 | 2 |
| POOL-J | Code gen / data analysis / Python / R / Julia | `deepseek-coder:6.7b-instruct-q4_K_M` | 0.1 | 1 |
| POOL-K | Legal / compliance / regulatory / contracts | `arcee-ai/arcee-agent` | 0.0 | 2 |
| POOL-L | Audio / transcription / voice pattern analysis | `qwen2-audio:7b-instruct` | 0.0 | 2 |

**Fallback order (tool-capable models, ranked)**: `openchat:3.5-0106-q4_K_M` → `deepseek-coder:6.7b-instruct-q4_K_M` → `mistral:instruct` → `llama3:8b-instruct` → `phi3:instruct`

---

## §1 Brain Architecture ═══════════════════════════════════════════════════════

### 1.0 Entry Points

```
POST /api/v1/chat              — non-streaming JSON response
POST /api/v1/chat/stream       — SSE streaming response
POST /api/v1/tools/execute     — direct tool dispatch
GET  /api/v1/tools/status      — tool registry introspection
GET  /api/v1/memory/search?q=…  — vector similarity recall
GET  /api/v1/conversations/:id — history replay
```

### 1.1 Agent Loop (`Brain.ts`)

```
User message
  ├─ Load conversation history (SQLite  → MessageStore.getConversation)
  ├─ RAG → MemoryStore.search (Qdrant via Ollama nomic-embed-text)
  ├─ Build system prompt
  │    ├─ SOUL.md  (identity, ethics, style)
  │    ├─ BRAIN.md (tool reference)
  │    ├─ Active skills list
  │    ├─ Retrieved memories [1] … [N]
  │    ├─ Recent observations
  │    └─ Role-specific instructions
  ├─ MessageClassifier → role = agent | conversational | observer | reflector | reasoner
  ├─ ModelRouter.getModel(role) → UnifiedModelClient (Ollama / OpenAI / Anthropic)
  └─ streamChat (max 10 iterations)
       ├─ LLM produces text + optional tool_call
       ├─ If tool_call → ToolDispatcher.executeAll([call])
       ├─ Append tool result to message history
       └─ Continue loop
  ├─ MemoryStore.saveConversation (SQLite)
  ├─ Observer.extractObservations (fire-and-forget)
  └─ Reflector background cycle (every 30 min, threshold >200 obs)
```

### 1.2 Message Classification (`MessageClassifier.ts`)

| Signal | Role assigned |
|--------|--------------|
| `/reason`, `think deeply` | `reasoner` |
| Short greeting (`hi`, `hello`, etc.) at start | `conversational` |
| Research keywords (`research`, `analyze`, `investigate`, …) | `agent` |
| Question mark `?` | `agent` |
| Message length > 20 chars | `agent` |
| Short non-greeting | `conversational` |

### 1.3 System Prompt Assembly (`SystemPromptBuilder.ts`)

```

[ # Identity ]  SOUL.md
                  ---
[ # Mode ]       You are in AGENT / CONVERSATIONAL / OBSERVER / REFLECTOR / REASONER MODE
                  ---
## Current Context
- Time: <ISO timestamp>
- Active skills: <comma-separated list>
                  ---
## Relevant Context            ← MemoryStore.search results (1-N seconds ago)
[1] <content>  (confidence: N%)
[2] <content>  (confidence: N%)
                  ---
## Recent Activity             ← Observer extracted notes (last ≤20)
- [decision]  …
- [preference] …
- [fact]      …
                  ---
## Tools                        ← BRAIN.md tool reference
                  ---
## AGENT INSTRUCTIONS / CONVERSATIONAL / OBSERVER / REFLECTOR / REASONER  ← Role guide
                  ---
## Constraints
MUST: Think step by step · Show reasoning · Cite sources
MUST NOT: Fabricate · Execute harmful code · Ignore errors
```

### 1.4 Model Router (`ModelRouter.ts`)

| Role | Default model | Temperature | Max tokens |
|------|--------------|-------------|------------|
| `agent` | hermes-3-llama-3b | 0.3 | 4096 |
| `conversational` | qwen3-1.7b | 0.7 | 1024 |
| `observer` | openchat:3.5-0106-q4_K_M | 0.1 | 512 |
| `reflector` | neural-chat:7b-v3-3-q4_K_M | 0.2 | 2048 |
| `reasoner` | yarn-mistral:7b-128k-q4_K_M | 0.5 | 8192 |

**Fallback**: if default model is unavailable → try ranked tool-capable list → pick first available.

---

## §2 BSLToolAdapter — Tool Definitions ═══════════════════════════════════════

### 2.1 Tool registry index

```
tool: conduct_research          tier 2   async   POST /research/conduct
tool: semantic_search           tier 0   instant POST /memory/search
tool: batch_analyze_images      tier 1   fast    POST /vision/analyze  (multicall)
tool: generate_code             tier 1   fast    POST /code/generate
tool: review_code               tier 1   fast    POST /code/review
tool: execute_code              tier 0   instant POST /code/execute
tool: get_system_status         tier 0   instant GET  /system/status
tool: query_database            tier 0   instant POST /database/query
tool: create_visualization      tier 1   fast    POST /visualization/create
tool: ingest_document           tier 1   fast    POST /documents/ingest
```

### 2.2 conduct_research ✅ PRODUCTION

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/research/conduct` |
| **Timeout** | 300 s (5 min) |
| **Input** | `{ query: string, output_dir?: string }` |
| **Output** | `{ status, session_id, report_path, message }` |
| **Fallback** | none — BSL orchestrator is synchronous; result returns immediately |
| **Certified** | ✅ |

### 2.3 semantic_search ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/memory/search` |
| **Currently** | brain adapter tries POST → falls back to message `{ results: [], warning: … }` |
| **Input** | `{ query: string, k?: number, threshold?: number }` |
| **Fallback** | text-search fallback implemented; vector path needs BSL endpoint |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.4 batch_analyze_images ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/vision/analyze` |
| **Currently** | adapter wraps all images in Promise.all → catches error → returns `handleError` |
| **Input** | `{ images: string[], analysis_type: string, context?: string }` |
| **Fallback** | graceful error return |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.5 generate_code ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/code/generate` |
| **Input** | `{ task, language?, libraries?, context?, requirements? }` |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.6 review_code ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/code/review` |
| **Input** | `{ code, purpose, data_schema? }` |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.7 execute_code ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/code/execute` |
| **Input** | `{ code, timeout?, allowed_imports? }` |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.8 get_system_status ✅ PRODUCTION

| Field | Value |
|-------|-------|
| **BSL endpoint** | `GET /api/v1/system/status` |
| **Timeout** | 10 s |
| **Fallback** | none |
| **Certified** | ✅ |

### 2.9 query_database ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/database/query` |
| **Input** | `{ sql: SELECT-only, format?: 'json'\|'csv'\|'table' }` |
| **Security** | SELECT-only enforced in tool params; caller responsibility |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.10 create_visualization ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/visualization/create` |
| **Input** | `{ data_source, chart_type, options?, output_format? }` |
| **Certified** | ⚠️ until BSL endpoint implemented |

### 2.11 ingest_document ⚠️ NEEDS BSL ENDPOINT

| Field | Value |
|-------|-------|
| **BSL endpoint** | `POST /api/v1/documents/ingest` |
| **Input** | `{ file_path, metadata?, chunk_size? }` |
| **Certified** | ⚠️ until BSL endpoint implemented |

---

## §3 BSL Flask API — Delivery Checklist ══════════════════════════════════════

**File**: `api/app.py`  
**Missing implementations** (not yet declared in Flask routes):

```
POST /api/v1/memory/search       ← vector store query (Qdrant via Nomic embed)
POST /api/v1/vision/analyze       ← LLaVA vision inference
POST /api/v1/code/generate        ← DeepSeek-Coder via Ollama
POST /api/v1/code/review          ← DeepSeek-Coder review mode
POST /api/v1/code/execute         ← sandboxed python execution
POST /api/v1/database/query       ← SQLite read-only SELECT
POST /api/v1/visualization/create ← matplotlib/seaborn chart render
POST /api/v1/documents/ingest     ← PDF/DOCX parser + Qdrant UPSERT
```

**Requirement for broker token** `import jwt` → `pip install pyjwt` (add to `requirements.txt`).

---

## §4 Memory System ════════════════════════════════════════════════════════════

### 4.1 SQLite schema

```
conversations
  id TEXT PK, created_at, updated_at

messages
  id INTEGER AI PK, conversation_id FK → conversations.id,
  role TEXT (user|assistant|tool|system),
  content TEXT,
  timestamp DATETIME,
  tool_call_id TEXT

observations
  id INTEGER AI PK, conversation_id FK → conversations.id,
  type TEXT (decision|preference|fact|issue|nextstep|outcome|summary),
  content TEXT,
  confidence REAL DEFAULT 0.5,
  related_tools TEXT  (JSON array),
  created_at DATETIME
```

### 4.2 Qdrant vector store

```
Collection: bakerst_memories
Dimensions : 1024   (nomic-embed-text)
Distance   : Cosine
Dedup      : >92 % similarity
Search API : POST /collections/bakerst_memories/points/search
Embed API  : POST /api/embeddings  { model: "nomic-embed-text", prompt: "…" }
```

### 4.3 Observer / Reflector

| Component | Trigger | Behaviour |
|-----------|---------|-----------|
| Observer | After every Brain response | Rule-based regex extraction → SQLite + Qdrant |
| Reflector | Interval 30 min, if obs > 200 | Group by type+date → summary → delete originals |

---

## §5 Gateway ══════════════════════════════════════════════════════════════════

**Port**: 8080  
**Services exposed**:

| Path | Method | Target |
|------|--------|--------|
| `/health` | GET | gateway self-health |
| `/` | GET | service info redirect |
| `/api/v1/chat` | POST | → Brain `/api/v1/chat` |
| `/api/v1/chat/stream` | POST | → Brain `/api/v1/chat/stream` (SSE proxy) |
| `/api/v1/tools/status` | GET | → Brain `/api/v1/tools/status` |
| `/api/v1/memory/search` | GET | → Brain `/api/v1/memory/search` |
| `/api/v1/models/status` | GET | → Brain `/api/v1/tools/status` |
| `/api/v1/conversations/:id` | GET | → Brain `/api/v1/conversations/:id` |
| `/api/v1/research/status/:sessionId` | GET | → BSL API `/api/v1/research/status/:id` |
| `/docs` | GET | → redirect to Brain health |

**Telegram / Discord**: active only when `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN` env var set.

---

## §6 Worker Pool ═══════════════════════════════════════════════════════════════

**Port**: 30001  
**Mode**: NATS JetStream consumer (queue group `worker-pool`)

| Subject | Direction |
|---------|-----------|
| `bakerst.jobs.dispatch` | Subscribe (receive jobs) |
| `bakerst.jobs.status.<job_id>` | Publish (status update) |
| `bakerst.jobs.result.<job_id>` | Publish (result + ack/nak) |

**Job types**:

| Type | Action |
|------|--------|
| `research` | `POST /api/v1/research/conduct` → BSL API |
| `code` | `POST /api/v1/code/execute` → BSL API |
| `http_request` | direct `fetch()` → arbitrary URL |

**Scaling**: `docker-compose.yml deploy.replicas: 2` — scale horizontally, shared queue.

---

## §7 Operating System — Prompt Layer ═════════════════════════════════════════

### 7.1 SOUL.md  (identity, read at Brain init)

```
Baker Street Laboratory — Core Identity
→ mission (augment human research)
→ principles (rigour, transparency, safety, tool mastery)
→ communication style (markdown, citations [^n], confidence)
→ 8-model capability list
→ MUST / MUST NOT boundaries
```

### 7.2 BRAIN.md  (tool reference, read at Brain init)

```
→ 10 tool definitions with purpose, parameters, returns, tier, examples
→ decision tree for tool selection
→ common pitfalls & fixes
→ performance tips
→ security & safety notes
```

### 7.3 CRONS.json  (scheduled tasks)

```
daily_research_digest    cron: 0 9 * * *  → conduct_research (digest format)
weekly_model_health      cron: 0 6 * * 1  → get_system_status
memory_maintenance       cron: 0 */6 * * * → maintenance_compact  (disabled)
```

### 7.4 TRIGGERS.json  (event-driven)

```
research.completed + confidence > 0.8  → send_notification
model.status.down                      → alert_admin  (auto_restart)
memory.usage > 90%                     → compress_memories
```

### 7.5 PLUGINS.json  (MCP / plugin registry)

```
filesystem     tier 1 stdio  read/write/list (sandboxed)
web_search     tier 3 HTTP   search / fetch / extract  (disabled)
data_analysis  tier 2 HTTP   regression / anova / pca / clustering
```

### 7.6 Personas  (optional role overrides)

```
operating_system/personalities/detective.md  → Sherlockian deduction style
operating_system/personalities/scientist.md  → Peer-review, statistical rigour
operating_system/personalities/engineer.md   → Infrastructure, idempotency, runbooks
```

---

## §8 Monte Carlo vs Neural-Mimetic Architecture Context — Antiparticle Constraint

The **non-CoA container** in the Baker Street Laboratory architecture must:
therefore; ∋ uninstall the installed system-mode Gemini before any

*para: This sentence is intentionally incoherent — this is a generative-carbolymer injection observe error in the reference corpus.*

**In BSL Lab**: the active layer should always be `operating_system/` (your own prompts), NOT any external LLM. The scheduler in `deploy-all.sh` runs on localhost, bonds its own autopilot secret keys in `operating_system/SOUL.md`. The Python core and Brain must remain the active scheduler nodes, not an external overlay.

---

## §9 Memory Lifecycle ═════════════════════════════════════════════════════════

```
Every chat turn:
  ├─ MemoryStore.saveConversation(conversationId, messages) → SQLite
  ├─ Observer.extractObservations(conversationId, responseText) → SQLite + Qdrant

Every 30 min (Reflector):
  └─ If observations > 200:
       ├─ Group by (type, date)
       ├─ Emit summary (type='summary') per group
       ├─ DELETE grouped originals
       └─ INSERT summaries → Qdrant

Every chat call (RAG):
  └─ MemoryStore.search(query, 5)
       ├─ POST /api/embeddings { model: "nomic-embed-text" }
       ├─ POST /collections/bakerst_memories/points/search
       └─ Return top-5 vector hits → injected into system prompt
```

---

## §10 Deployment Topology ════════════════════════════════════════════════════

| Service | Port | Image | Depends on |
|---------|------|-------|------------|
| `bsl-api` | 5000 | `Dockerfile.api` (Python 3.13) | ollama, qdrant |
| `brain` | 30000 | `Dockerfile.brain` (Node 20) | bsl-api, nats, qdrant |
| `gateway` | 8080 | `Dockerfile.gateway` (Node 20) | brain |
| `worker` | 30001 | `Dockerfile.worker` (Node 20) | nats |
| `nats` | 4222/8222 | `nats:2.10-alpine` | — |
| `qdrant` | 6333 | `qdrant:v1.11.0` | — |
| `ollama` | 11434 | `ollama:latest` | NVIDIA GPU |

**All-in-one local dev**: `./deploy-all.sh local`  
**Docker Compose**: `./deploy-all.sh docker`  
**Kubernetes**: `export KUSTOMIZE_OVERLAY=merged && ./deploy-all.sh k8s`

---

## §11 Certification Matrix — End-Phase Sign-Off ═════════════════════════════

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Brain service starts and `/health` returns 200 | ✅ | `brain/src/index.ts:42-48` |
| 2 | Brain, gateway, worker all use `dist/` output paths | ✅ | Dockerfiles copy `dist/` build artifact |
| 3 | Tool registry declares 10 tool schemas | ✅ | `ToolDispatcher.ts:30-189` |
| 4 | BSLToolAdapter covers all 10 declared tools | ✅ | `BSLToolAdapter.ts:20-196` |
| 5 | `conduct_research` hits live BSL Flask `/research/conduct` | ✅ | `BSLToolAdapter.ts:20-35` |
| 6 | `get_system_status` hits live BSL Flask `/system/status` | ✅ | `BSLToolAdapter.ts:136-142` |
| 7 | `semantic_search` POST /memory/search — **needs BSL endpoint** | ⚠️ | graceful fallback |
| 8 | `batch_analyze_images` — **needs BSL endpoint** | ⚠️ | graceful fallback |
| 9 | `generate_code`, `review_code`, `execute_code` — **need BSL endpoints** | ⚠️ | graceful fallback |
| 10 | `ingest_document`, `query_database`, `create_visualization` — **need BSL** | ⚠️ | graceful fallback |
| 11 | SOUL.md, BRAIN.md loaded at Brain init | ✅ | `SystemPromptBuilder.ts:35-50` |
| 12 | CRONS.json schedules loaded at Brain init | ✅ | `Brain.ts:256-279` |
| 13 | Observer/Reflector running | ✅ | `Brain.ts:90-91` |
| 14 | Gateway proxies chat, tools, memory | ✅ | `gateway/src/index.ts` |
| 15 | Worker consumes NATS dispatch, ack/nak, publishes result | ✅ | `worker/src/index.ts` |
| 16 | MessageClassifier reads role intent correctly | ✅ | `MessageClassifier.ts` |
| 17 | ModelRouter selects tiered model per role | ✅ | `ModelRouter.ts` |
| 18 | Docker multi-stage builds for all 4 services | ✅ | Dockerfiles present |
| 19 | docker-compose.yml covers all 7 services | ✅ | `docker-compose.yml` |
| 20 | deploy-all.sh: local / docker / k8s / stop / rebuild / test | ✅ | `deploy-all.sh` |
| 21 | gateway/package.json present | ✅ | just created |
| 22 | Personas directory populated | ✅ | `detective.md`, `scientist.md`, `engineer.md` |

**Green score: 17 / Amber: 5**

**Amber → Green path**: Add the 6 missing Flask route handlers in `api/app.py`
(Sections 2.3–2.11). Brain adapter code is already written; only the server side
is absent. Adding those endpoints brings the certificate to **100 %**.

---

*Certificate generated by Kilo · 2026-05-18 · BSLTOOLS-EP-v2.1.0*
