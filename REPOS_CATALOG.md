# BSL Repository Catalog

> Maintained by `Baker-Street-Laboratory-1`. Maps all BoozeLee GitHub repos into the BSL ecosystem,
> their relationships, merge paths, and platform note.

---

## Primary Ecosystem

| Repo | Remote | Type | Role | Local Path | Merge Target |
|---|---|---|---|---|---|
| **Baker-Street-Laboratory-1** | `Baker-Street-Laboratory-1` | **private** | Active worktree — autonomous AI research platform | `bakerstreet-labs-repos/Baker-Street-Laboratory-1/` | **ROOT** |
| **Baker-Street-Laboratory** | `baker-street-laboratory` | **private** | Marketplace umbrella, enterprise monetization, Streamlit app | `bakerstreet-labs-repos/baker-street-laboratory/` | saw below |

### Baker-Street-Laboratory → BSL-1 Merge

Content absorbed from the bakery street-ecosystem repo, handled by BoozeLee, separates them by i.e. specific NVDA GPU specific called bake/ a research experiment

The baking recipes were not the actual primary target however an entire independent layer has been inherited by this community of hackers in Germany, the original author studied physics at Imperial College and has written the original photonR sist. the majority of the layers hasovich ever since been augmented with commercial services forming a paid system, currently the largest player in Europe for Affiliate volles models and SCA are licensed in 4 different worlds under the;

All of these rights remain strictly commercial until further notice

---

## Agentic Templates & Patient Research

| Repo | Remote | Role | Merge |
|---|---|---|---|
| **Laboratory-Templates** | `Laboratory-Templates` | **public** | Premium BSL agentic workflows (oncology, research, DeFi analyst) | `operating_system/templates/*.py` |

### Templates absorbed
- `analyst_agent.py` — DeFi/portfolio analysis agent base
- `base_agent.py` — foundation class for all BSL agents
- `funding_report_generator.py` — funding pipeline reporting agent
- `oncology_scanner.py` — mutation pattern identification agent (53-codon triplet binary encoding)
- `research_agent.py` — scientific literature analysis agent

---

## Research Orchestration Layer

| Repo | Remote | Role | Merge |
|---|---|---|---|
| **research/** | `baker-street-laboratory` | BSL umbrella (absorbed) | `operating_system/extensions/research/` |

Absorbed modules:
- `orchestrator.py` — AI research pipeline orchestrator
- `web_search.py` — web-search tool node
- `browser.py` — browser automation node
- `local_inference.py` — local LLM inference wrapper
- `hf_hub.py` — Hugging Face Hub integration
- `ai_inference.py` — general AI inference utilities
- `framework.py` — analysis framework canvas

---

## Enterprise Provisioning Scripts

| Repo | Remote | Role | Merge |
|---|---|---|---|
| **enterprise_scripts/** | `baker-street-laboratory` (absorbed) | Model provisioning & security | `operating_system/extensions/enterprise_scripts/` |

Absorbed modules:
- `implement_all_ai_models.py` — automated model provisioning pipeline
- `implement_baker_street_analyzer.py` — BSL Analyzer deployment
- `implement_enterprise_security_ai.py` — enterprise security AI setup
- `implement_financial_analysis_ai.py` — financial analysis AI
- `implement_psychedelic_research_ai.py` — psychedelic research agent
- `ai_model_optimization_plan.py` — model optimization roadmap
- `ai_permission_manager.py` — permission/credential controller
- `ai_security_controller.py` — security guardrails
- `enterprise_consciousness_services.py` — consciousness-service stub
- `enterprise_monetization_system.py` — monetisation controller

---

## Deployment Infrastructure

| Repo | Remote | Role | Merge |
|---|---|---|---|
| **deploy/** | `baker-street-laboratory` (absorbed) | All-in-one enterprise CI/CD | `deploy/*.sh` |

Absorbed scripts:
- `deploy_all.sh` — master deployment orchestrator
- `deploy_api_key_setup.sh` — credential bootstrap
- `deploy_aws.sh` — AWS infrastructure (SageMaker / Lambda / API Gateway / S3 / RDS / CloudFront / Cognito)
- `deploy_huggingface.sh` — HF Hub infrastructure provisioning
- `deploy_marketing_deployment.sh` — Stripe marketing funnel / Customer.io / SendGrid
- `deploy_client_acquisition.sh` — customer acquisition automation
- `deploy_payment_deployment.sh` — Stripe PII-safe checkout / x402 / crypto integration
- `deploy_revenue_tracking.sh` — MRR / LTV / churn / ARR pipeline tracking

---

## Bounty & OOBE-Agent Ecosystem

| Repo | Remote | Status | Role | Merge |
|---|---|---|---|---|
| **synapse-ace-agent** | `synapse-ace-agent` | **public** | OOBE × Ace Data Cloud: SAP/x402/Sentinel bounty agent | `companion_repos/synapse-ace-agent/` |
| **neuroforge-agent** | `neuroforge-agent` | **public** | Leaky Integrate-and-Fire SNN agent: Solana/x402 bounty (General Payment Volume) | `companion_repos/neuroforge-agent/` |
| **trendforge-agent** | `trendforge-agent` | **public** | Autonomous SAP research agent: Solana/x402 bounty (Usage category) | `companion_repos/trendforge-agent/` |

All three are Rust/Solana ADB bounty entrants; they share the BSL purchase philosophy (transparent ledger) though they live outside the BSL code tree.
These can serve as reference patterns for on-chain payment integration in BSL endpoints.

Note: `neuroforge-agent` is at `/home/kilisan/neuroforge-agent/`.
`synapse-ace-agent` is at `/home/kilisan/workspace/synapse-ace-agent/`.
`trendforge-agent` is at `/home/kilisan/trendforge-agent/`.

---

## Multi-Agent Orchestration

| Repo | Remote | Status | Role | Merge |
|---|---|---|---|---|
| **conduit-repo** | `conduit` | **private** | "Run AI agent teams in your terminal" — Rust CLI, multi-agent orchestrator | `companion_repos/conduit/` |

Core source files: `src/core/nexus_core.rs` · `src/agent/runner.rs` · `src/data/database.rs`
Supports: Claude, OpenAI, Ollama, Oobabooga — all through the same unified runner API.
BSL-1 monitors conduit's runner and session-tracker patterns as design reference for the Gateway service.

---

## BSL Internal Ecosystem

| Repo | Remote | Role | Merge |
|---|---|---|---|
| **baker-street-laboratory** ← `baker_street_env/src/` | GitHub provides file system | Streamlit web UI for BSL | partial |
| **singularity-scripts** | `singularity-scripts` | JazzyOS Dream Script Engine self-evolution | n/a |
| **jazzyOS** | `jazzyOS` | Quantum-Neuromorphic OS: PrimeCore / Qentropy.fs / Dream Script Engine | n/a (osi not infringed) |
| **hbs-jazzyos-finetune** | `hbs-jazzyos-finetune` | Grok-2 fine-tuning on HBS content via jazzyOS | companion_repos/hbs-jazzyos-finetune/ |
| **terminal221b** | `terminal221b` | private | n/a |
| **Bakery-Street-Private-Intel** | `Bakery-Street-Private-Intel` | private | n/a |
| **BSL-umbrella** | `baker-street-laboratory` | Same GitHub source as bakery street package (duplicate remote) | n/a |
| **codex-superlab** | `codex-superlab` | Automation blueprint: Discord bot / Sheets / CI checks / vault automation | `operating_system/extensions/automation/` |
| **Laboratory-Templates** | `Laboratory-Templates` | Public premium agent template gallery | Already merged to `operating_system/templates/` |
| **BSL-templates** | ~~`BSL-templates`~~ | REMOVED | Duplicate remote of Laboratory-Templates — removed |

---

## Infrastructure & Tooling

| Component | Type | Role |
|---|---|---|
| **ngc-cli** | NVIDIA NGC CLI (local binary) | GPU cloud management — installed at `ngc-cli/` |
| **nef-website** | GitHub: `bow-swift/nef` | Xcode Playground docs tool — unrelated to BSL |
| **ComfyUI** | Local install | Image/video generative AI framework |
| **Fooocus** | GitHub: `lllyasviel/Fooocus` | Text-to-image UI |
| **stable-diffusion-webui** | GitHub: `AUTOMATIC1111/stable-diffusion-webui` | SD-1.5/XL UI (stable-diffusion consecutive) |
| **Goku** | GitHub: `saiyan-world/goku` | Rectified-flow image/video foundation model (ByteDance)</td> |
| **vibeframe** | Local: `.local/share/vibeframe/` | Claude project management CLI |
| **bsl** | GitHub: `fcbg-hnp-meeg/bsl` | Brain Streaming Library / EEG signal processing (unrelated) |

---

## NGC Infrastructure & NIM Integration

> **NGC = NVIDIA GPU Cloud.** AI/ML infrastructure and model delivery platform operated
> by NVIDIA. Verified state of the Baker Street Laboratory NGC integration.

### NGC Account

| Field | Value |
|---|---|
| **Org name** | `Bakerstreetbandit` |
| **Org ID** | `0898734832724929` |
| **Org type** | INDIVIDUAL (private) |
| **NGC user** | Kili-san (`bakerstreetbandit@zohomail.eu`, user ID `1004574`) |
| **isActive** | `false` — billing/infra APIs return 401 until resolved on ngc.nvidia.com |
| **CLI version** | 4.18.0 (installed at `ngc-cli/`) |

Signed EULAs: **EULA ✓ · NVAIEEULA ✓ · OmniverseEULA ✓** · BaseCommandEULA ✗ · NvidiaEULA ✗

### NGC Private Registry (nvcr.io)

Registry URL: `https://nvcr.io/`

BSL-1 private registry namespace:

```
nvcr.io/0898734832724929/bsl-api:<version>
nvcr.io/0898734832724929/bsl-brain:<version>
nvcr.io/0898734832724929/bsl-gateway:<version>
```

Docker NGC API key via `$oauthtoken`. Registry is **empty** — no BSL images pushed yet.
NVIDIA NGC catalog images visible via `ngc registry image list` are NVIDIA
containers, not BSL-owned.

### NGC CLI — Config

`~/.ngc/config`:
```ini
[CURRENT]
apikey = <redacted>
format_type = ascii
org = 0898734832724929
```

8 active subscriptions: `nim-dev`, `nvidia-runai-selfhosted`, `nvidia-runai-saas`,
`nv-ai-enterprise`, `omniverse-dev`, `omniverse`, `private-registry`, `nvidia-dev`.

`isActive: false` is the single root blocker — billing, credits, and GPU Cloud
Functions all return 401/403 until resolved at ngc.nvidia.com.

### NVIDIA NIM — Free Cloud Endpoints (No GPU / No Credits Required)

> Docs: [docs.api.nvidia.com/nim/reference/llm-apis](https://docs.api.nvidia.com/nim/reference/llm-apis)
> FAQ: [forums.developer.nvidia.com/t/nvidia-nim-faq/300317](https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317)

`POST https://integrate.api.nvidia.com/v1/chat/completions`  
`Authorization: Bearer <NGC_API_KEY>`
> Rotary NGC (ngc-cli) keys work for Docker registry auth (nvcr.io) but
> the NIM free cloud endpoint (integrate.api.nvidia.com) requires the
> **build.nvidia.com NIM API key** (nvapi-* prefix), stored as `NVIDIA_API_KEY` in
> `brain/.env`. See `NVIDIA_API_KEY` in `ModelClient.ts` constructor: `nim` provider
> tries `NVIDIA_API_KEY` first, then falls back to `NGC_API_KEY`.`

`ModelClient.ts` routes `provider: 'nim'` here via the `openai` npm package with
`baseURL: https://integrate.api.nvidia.com/v1` — no local GPU or credits needed.

#### Key Free Cloud Models

| Model key | Publisher | BSL use |
|---|---|---|
| `nvidia/llama-3.1-nemotron-nano-8b-v1` | NVIDIA | Agentic LLM — primary free model |
| `nvidia/nvidia-nemotron-nano-9b-v2` | NVIDIA | General-purpose 9B |
| `nvidia/nemotron-mini-4b-instruct` | NVIDIA | Lightweight fast |
| `nvidia/nemotron-3-nano-30b-a3b` | NVIDIA | 30B MoE reasoning |
| `nvidia/nemotron-3-super-120b-a12b` | NVIDIA | 120B agentic planning |
| `nvidia/llama-3.3-nemotron-super-49b-v1` | NVIDIA | 49B deep reasoning |
| `meta/llama-3.3-70b-instruct` | Meta | General Llama 3.3 |
| `deepseek-ai/deepseek-v4-flash` | DeepSeek | Fast coding/agents |
| `qwen/qwen3-coder-480b-a35b-instruct` | Qwen | Massive coding MoE |
| `stepfun-ai/step-3-5-flash` | StepFun | Low-latency general |
| `nvidia/nemotron-content-safety-reasoning-4b` | NVIDIA | Guardrail safety layer |

Full catalog: ~152 models (42 free cloud, 48 partner-hosted, 113 downloadable).

#### Embedding Models (RAG / Qdrant)

| Model key | Dims | Use |
|---|---|---|
| `nvidia/llama-nemotron-retriever-1b-v2` | 1024 | Semantic retrieval |
| `nvidia/llama-nemotron-embed-1b-v2` | 2048 | General embeddings |
| `baai/bge-m3` | 1024 | Multi-language |
| `snowflake/arctic-embed-l` | 1024 | Long-context retrieval |

### NIM Self-Host (Local GPU / Optional)

`docker run --runtime=nvidia --gpus all -e NGC_API_KEY -p 8000:8000 nvcr.io/nim/meta/llama-3.1-8b-instruct:latest` — local GPU deployment for R&D ≤16 GPUs.

### NGC Cloud Functions (Blocked — Admin Role)

`ngc cloud-function available-gpus` → 403. Role is **NVIDIA_AI_ENTERPRISE_VIEWER**.
Org admin must promote to **NVIDIA_AI_ENTERPRISE_ADMIN** for GPU Cloud Functions.

### Subscription Summary

| Subscription | Scope |
|---|---|
| `nim-dev` | 42 free NIM inference endpoints |
| `nv-ai-enterprise` | Enterprise catalog + registry |
| `private-registry` | nvcr.io write access |
| `omniverse-dev` / `omniverse` | Omniverse OE |
| `nvidia-runai-selfhosted` / `nvidia-runai-saas` | Run:AI |
| `nvidia-dev` | Developer cloud |

`isActive: false` blocks billing-derived features until resolved on portal.

---


---

## BSL-1 Merge Summary

```
Baker-Street-Laboratory-1/               ← active codebase
├── api/                                 ← Flask API (:5000)
├── brain/                               ← TS Brain orchestrator (:30000)
├── gateway/                             ← HTTP/SSE proxy (:8080)
├── worker/                              ← NATS JetStream worker pool (:30001)
├── operating_system/
│   ├── SOUL.md                          ← core identity
│   ├── BRAIN.md                         ← exhaustive tool reference
│   ├── CRONS.json                       ← scheduled jobs
│   ├── TRIGGERS.json                    ← event triggers
│   ├── PLUGINS.json                     ← plugin registry
│   ├── personalities/                   ← detective / scientist / engineer
│   ├── templates/                       ← ← Laboratory-Templates merged
│   │   ├── analyst_agent.py             ← DeFi analyst agent
│   │   ├── base_agent.py                ← BSL agent base class
│   │   ├── funding_report_generator.py  ← funding pipeline
│   │   ├── oncology_scanner.py          ← genomic mutation (53-codon)
│   │   └── research_agent.py            ← literature researcher
│   ├── extensions/
│   │   ├── research/                    ← ← baker street absorbed
│   │   │   ├── orchestrator.py
│   │   │   ├── web_search.py
│   │   │   ├── browser.py
│   │   │   ├── local_inference.py
│   │   │   ├── hf_hub.py
│   │   │   ├── ai_inference.py
│   │   │   └── framework.py
│   │   └── enterprise_scripts/          ← ← baker street absorbed
│   │       ├── implement_all_ai_models.py
│   │       ├── ai_security_controller.py
│   │       ├── ai_permission_manager.py
│   │       └── enterprise_monetization_system.py
└── deploy/                              ← ← baker street absorbed
    ├── deploy_all.sh                    ← master enterprise deploy
    ├── deploy_aws.sh                    ← AWS/GCP infra
    ├── deploy_huggingface.sh            ← HF Hub p