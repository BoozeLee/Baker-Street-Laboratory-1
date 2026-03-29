# 🔬 Baker Street Laboratory

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/baker-street-lab)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://bakerstreetproject.github.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![Bakerstreet Labs](https://img.shields.io/badge/Bakerstreet-Labs-black.svg)](https://github.com/Bakery-street-project)

> **Autonomous AI research platform with 8 specialized models, multi-agent orchestration, and production-grade infrastructure.**

Part of the [Bakerstreet Labs](https://github.com/Bakery-street-project) ecosystem — where agents never sleep.

---

## 💰 Pricing

| Tier | Price | Capacity |
|------|-------|----------|
| **Starter** | $299/month | 1 agent, 100 runs/day |
| **Pro** | $999/month | All agents, 1,000 runs/day |
| **Lab** | $2,999/month | Unlimited, custom integrations |

[**→ Start Free Trial**](https://github.com/Bakery-street-project) · [**→ Enterprise Inquiry**](mailto:iamthatiamresearch@gmail.com)

---

## 🧬 What It Does

Baker Street Laboratory is a sovereign, self-assembling AI research platform. Eight specialized models collaborate on complex research tasks — from visual analysis to legal research to long-context synthesis.

```
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Control Plane                   │
│              Polymorphic Framework Layer                 │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬───────┘
       │      │      │      │      │      │      │
    Vision  Embed  Sci  Creative Coder  Legal Audio LongCtx
    5.0GB  274MB  4.1GB  4.1GB  776MB  2.0GB  4.7GB  4.4GB
```

### 🤖 AI Specialist Team (7/8 Operational)

| Model | Purpose | Size | Status |
|-------|---------|------|--------|
| 🔍 `baker-street-vision` | Visual analysis detective | 5.0 GB | ✅ Operational |
| 🌿 `baker-street-embed` | Semantic search specialist | 274 MB | ✅ Operational |
| 🔬 `baker-street-scientific` | Scientific methodology | 4.1 GB | ✅ Operational |
| ✍️ `baker-street-creative` | Creative writing & reports | 4.1 GB | ✅ Operational |
| 💻 `baker-street-coder` | Data analysis & coding | 776 MB | ✅ Operational |
| ⚖️ `baker-street-legal` | Legal research & compliance | 2.0 GB | ✅ Operational |
| 🎵 `baker-street-audio` | Audio processing | 4.7 GB | ✅ Operational |
| 📚 `baker-street-longcontext` | Long context processor | 4.4 GB | ⚠️ CPU Fallback |

**Total: ~25GB of specialized AI research capabilities**

---

## 🚀 Quick Deploy

```bash
railway up
# Set env vars: STRIPE_SECRET_KEY, SUPABASE_URL
# Configure Stripe webhook: POST /webhook/stripe
```

Or deploy locally:
```bash
git clone https://github.com/BoozeLee/Baker-Street-Laboratory-1.git
cd Baker-Street-Laboratory-1
cp .env.example .env
docker-compose up
```

---

## 🔗 Ecosystem Integration

Baker Street Laboratory is the **hub** of the Bakerstreet Labs ecosystem:

| Signal In | From | Action |
|-----------|------|--------|
| Research data | [`go-research-spider`](https://github.com/BoozeLee/go-research-spider) | RAG ingestion pipeline |
| Agent tasks | [`beeai-hive-999`](https://github.com/BoozeLee/beeai-hive-999) | Multi-model orchestration |
| Code requests | [`go-ai-coder`](https://github.com/Bakery-street-project/go-ai-coder) | Code analysis & review |

```yaml
# Receives repository_dispatch events from:
# - type: research_data_ready  (go-research-spider)
# - type: agent_task           (beeai-hive-999)
```

---

## 🏗️ Architecture

```
baker-street-laboratory/
├── agents/              # 8 specialized AI model configs
├── api/                 # FastAPI control plane
├── auth_middleware.py   # Supabase auth
├── stripe_webhook.py    # Stripe billing integration
├── docker-compose.yml   # Full stack deployment
└── railway.json         # One-click Railway deploy
```

---

## 🛡️ Security

- Supabase Vault for secrets management
- No API keys in code — all via environment variables
- Secret scanning enabled (gitleaks + trufflehog + detect-secrets)

---

## 📄 License

Proprietary — [Enterprise Licensing Available](mailto:iamthatiamresearch@gmail.com) · [Bakerstreet Labs](https://github.com/Bakery-street-project)
