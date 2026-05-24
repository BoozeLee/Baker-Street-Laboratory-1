# 🏪 Baker Street Laboratory — v2.1 (Merged)

> **AI Research Platform** × **Conversational Agent**

This repository contains the merged implementation of **Baker Street Laboratory** (multi-model AI research platform) with the **Baker Street Project** (agent orchestration architecture).

## 🚀 Quick Start (3 commands)

```bash
# 1. Setup Python environment
./deploy-all.sh setup

# 2. Start all services (direct mode)
./deploy-all.sh local

# 3. Test chat
curl -X POST http://localhost:30000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello! What can you help me research today?"}'
```

**Endpoints**:
- BSL API: http://localhost:5000/api/v1/docs
- Brain Chat: http://localhost:30000/api/v1/chat
- Web UI (coming soon): http://localhost:8080

## 📦 What's New

### Brain Agent (Port 30000)

The Brain is a **conversational AI agent** that sits in front of your research pipeline. It understands natural language, maintains conversation history, selects appropriate tools (your 8 AI models), and streams responses in real-time.

**Key features**:
- **Tool orchestration**: Automatically picks vision, embed, scientific, creative, coder, legal, audio models
- **Memory**: Remembers past conversations and important facts
- **Reasoning**: Step-by-step thinking before acting
- **Streaming**: Real-time text generation via SSE

### Operating System Prompts (`operating_system/`)

The agent's personality and knowledge live in markdown files:
- `SOUL.md` — identity, ethics, communication style
- `BRAIN.md` — complete tool reference with examples
- `CRONS.json` — scheduled tasks
- `TRIGGERS.json` — automation rules

Edit these files to change how the agent thinks — no code recompilation needed.

### Unified Access

| Mode | How to use |
|------|------------|
| **Direct API** | `curl http://localhost:30000/api/v1/chat` |
| **Docker Compose** | `./deploy-all.sh docker` |
| **Kubernetes** | `./deploy-all.sh k8s` |
| **Web UI** | `./deploy-all.sh local` → http://localhost:8080 |
| **Telegram** | Set `TELEGRAM_BOT_TOKEN` in .env |
| **Discord** | Set `DISCORD_BOT_TOKEN` in .env |

---

## 🏗️ Architecture

```
User → Gateway → Brain → [ToolDispatcher → BSL API → Ollama Models]
          │          │
          │          ├─ MemoryStore (SQLite + Qdrant)
          │          ├─ Observer (extract observations)
          │          ├─ Reflector (compress memories)
          │          └─ ModelRouter (pick Claude/GPT/Ollama)
          │
          └─ Channels: HTTP / Telegram / Discord
```

Read full details in [ARCHITECTURE_MERGED.md](ARCHITECTURE_MERGED.md).

---

## 📁 Directory Structure (New/Created)

```
Baker-Street-Laboratory-1/
├── operating_system/           # NEW — Prompt layer (SOUL.md, BRAIN.md, CRONS.json)
├── brain/                      # NEW — Agent orchestrator (TypeScript)
│   ├── src/
│   │   ├── agent/
│   │   │   ├── Brain.ts        # Main agent loop
│   │   │   ├── MessageClassifier.ts
│   │   │   ├── ModelRouter.ts
│   │   │   └── ModelClient.ts  # Unified OpenAI/Anthropic/Ollama client
│   │   ├── memory/
│   │   │   ├── MemoryStore.ts  # SQLite + Qdrant
│   │   │   ├── Observer.ts     # Extract observations
│   │   │   └── Reflector.ts    # Consolidate memories
│   │   ├── tools/
│   │   │   ├── ToolDispatcher.ts
│   │   │   ├── ToolRegistry.ts
│   │   │   └── BSLToolAdapter.ts  # Bridge to Python API
│   │   ├── prompts/
│   │   │   └── SystemPromptBuilder.ts  # SOUL+BRAIN assembler
│   │   └── nats/
│   │       └── NATSClient.ts   # Message bus
│   ├── package.json
│   └── tsconfig.json
├── gateway/                    # NEW — Multi-channel gateway
├── worker/                     # NEW — Background job pool
├── k8s/                        # NEW — Kubernetes manifests
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml    # BSL API
│   │   ├── service.yaml
│   │   ├── pvc.yaml
│   │   └── secrets.yaml
│   └── overlays/
│       └── merged/
│           ├── kustomization.yaml
│           ├── brain-deployment.yaml
│           ├── brain-service.yaml
│           └── patches/
├── docker-compose.yml          # NEW — All-in-one local dev
├── Dockerfile.brain
├── Dockerfile.gateway
├── Dockerfile.worker
├── Dockerfile.api
├── deploy-all.sh               # NEW — Unified deployment CLI
├── stop.sh                     # NEW — Stop all services
├── test-integration.sh         # NEW — Smoke tests
├── BSL_BAKER_STREET_MERGE_PLAN.md   # Full technical plan
├── ARCHITECTURE_MERGED.md      # High-level architecture
└── [existing BSL files]
```

---

## 🔧 Development

### Prerequisites

- **Python 3.10+** (for BSL core)
- **Node.js 20+** (for Brain/Gateway/Worker)
- **Docker** (optional but recommended)
- **kubectl + kustomize** (for K8s)

### Setup

```bash
# Install Python deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Install Node deps
npm install -g pnpm
pnpm install

# Build TypeScript
pnpm build

# Create .env
cp .env.merged .env  # then edit with your API keys
```

### Run (Direct Mode)

```bash
# Terminal 1: BSL API
source .venv/bin/activate
python3 implementation/src/main.py --mode api

# Terminal 2: Brain
cd brain && npm start

# Terminal 3: Gateway (optional)
cd gateway && npm start
```

### Run (Docker Compose)

```bash
docker-compose up -d
```

### Deploy to Kubernetes

```bash
# Build images
./docker-deploy.sh build

# Deploy
./deploy-all.sh k8s

# Check
kubectl -n bakerst get pods
kubectl -n bakerst logs -f deployment/brain
```

---

## 🧪 Testing

```bash
# Automated integration tests
./deploy-all.sh test

# Manual curl test
curl http://localhost:30000/health
curl -X POST http://localhost:30000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Search for recent CRISPR gene editing papers"}'

# Monitor logs
tail -f logs/brain.log
```

---

## 🎛️ Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI access | (none) |
| `ANTHROPIC_API_KEY` | Claude access | (none) |
| `BSL_API_URL` | Brain → BSL routing | `http://localhost:5000` |
| `NATS_URL` | Message bus address | `nats://localhost:4222` |
| `QDRANT_URL` | Vector DB | `http://localhost:6333` |
| `CONFIG_PATH` | operating_system dir | `/app/operating_system` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot | (none) |
| `DISCORD_BOT_TOKEN` | Discord bot | (none) |

Full list: See `.env.merged`.

### Prompt Customisation

Edit `operating_system/SOUL.md` to change agent personality:

```markdown
You are **MyAgent**, a curious research assistant...

## Communication Style
- Be concise
- Use bullet points
- Add emoji occasionally ✅🔬
```

Restart Brain to load changes.

---

## 📊 Monitoring

### Local (Direct Mode)

```bash
# Check system status
curl http://localhost:5000/api/v1/system/status

# Tool availability
curl http://localhost:30000/api/v1/tools/status

# Conversation history
curl http://localhost:30000/api/v1/conversations/<id>
```

### Docker Compose

```bash
docker-compose ps
docker-compose logs -f brain
docker-compose exec bsl-api python3 -c "from core.logger import get_logger; print('OK')"
```

### Kubernetes

```bash
kubectl -n bakerst get pods
kubectl -n bakerst logs -f deployment/brain
kubectl -n bakerst exec -it deployment/brain -- sh
```

---

## 🛠️ Troubleshooting

| Problem | Check | Fix |
|---------|-------|-----|
| Brain 500 error | `logs/brain.log` | Verify BSL API up: `curl http://localhost:5000/health` |
| Tools unavailable | `GET /api/v1/tools/status` | Start Ollama, load models (`ollama pull ...`) |
| No memory recall | Check Qdrant | `curl http://localhost:6333/collections` |
| Docker network issues | `docker network ls` | Recreate: `docker-compose down && docker-compose up -d` |
| K8s pod pending | `kubectl describe pod` | Increase resources or add GPU nodes |

Full troubleshooting: See [ARCHITECTURE_MERGED.md](ARCHITECTURE_MERGED.md#troubleshooting).

---

## 📚 Documentation

- **[ARCHITECTURE_MERGED.md](ARCHITECTURE_MERGED.md)** — system design, data flows, component details
- **[BSL_BAKER_STREET_MERGE_PLAN.md](BSL_BAKER_STREET_MERGE_PLAN.md)** — complete technical implementation plan
- **[operating_system/README.md](operating_system/README.md)** *(create if needed)* — prompt engineering guide

---

## 🔮 Future Roadmap

- [ ] Worker pool for async job execution (scalable)
- [ ] Task Pods (isolated Kubernetes Jobs)
- [ ] Extension auto-discovery (MCP servers)
- [ ] Web UI (React chat interface)
- [ ] Voice input/output
- [ ] Multi-agent teams (delegate research phases)
- [ ] Active learning loop (agent asks clarifying questions)
- [ ] Collaborative filtering (combine multiple model outputs)
- [ ] Enterprise auth (SPIFFE / OIDC)
- [ ] SOC2 compliance tooling

See `ENHANCEMENT_ROADMAP.md`.

---

## 🤝 Contributing

This is a merged proprietary project. For internal modifications:

1. Edit prompts in `operating_system/` for behaviour changes
2. Add tools in `brain/src/tools/ToolDispatcher.ts`
3. Extend memory in `brain/src/memory/`
4. Follow existing code style (TypeScript with strict mode)
5. Run tests before commit: `./deploy-all.sh test`

---

## 📄 License

PROPRIETARY — See [LICENSE](LICENSE) for terms.

---

**Baker Street Laboratory** — Where AI agents never sleep 🔬
