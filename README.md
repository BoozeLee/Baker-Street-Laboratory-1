# Baker-Street-Laboratory-1

Autonomous AI research platform with 8 specialized models, multi-agent orchestration, and clinician-reviewed outputs.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-005571?logo=fastapi)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL_%7C_Auth_%7C_Storage-3ecf8e?logo=supabase)
![Stripe](https://img.shields.io/badge/Stripe-Billing-635bff?logo=stripe)
![Flutter](https://img.shields.io/badge/Flutter-3.x-02569b?logo=flutter)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ed?logo=docker)

## Overview

Baker Street Laboratory is a production-grade AI research platform that orchestrates 8 specialized models to perform autonomous research, generate reports, and deliver clinician-reviewed outputs. It operates as a live SaaS with tiered pricing ($299–$2,999/month).

## Key Features

- **8-Model Agent Swarm**: Specialized models for research, analysis, synthesis, and review
- **Multi-Agent Orchestration**: Graph-based workflow coordination with state management
- **RAG Pipeline**: Retrieval-augmented generation over research knowledge base
- **Clinician Review Workflow**: Human-in-the-loop validation for medical/health outputs
- **Stripe Billing**: Subscription management with tiered pricing
- **Flutter Dashboard**: Cross-platform research interface for querying and monitoring

## Tech Stack

- **Backend**: FastAPI, Python 3.12, async/await, Pydantic
- **Database**: Supabase (PostgreSQL with RLS, real-time subscriptions)
- **AI/ML**: OpenAI API, Anthropic Claude, custom fine-tuned models
- **Orchestration**: Custom agent framework with MDP-based task decomposition
- **Frontend**: Flutter (iOS, Android, Web, Desktop)
- **Payments**: Stripe Checkout, webhooks, subscription management
- **Infrastructure**: Docker, Docker Compose, CI/CD with GitHub Actions

## Quick Start

```bash
# Clone the repository
git clone https://github.com/BoozeLee/Baker-Street-Laboratory-1.git
cd Baker-Street-Laboratory-1

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with Supabase and API keys

# Run the backend
uvicorn main:app --reload

# Run the Flutter dashboard (in another terminal)
cd flutter_app
flutter pub get
flutter run
```

## Architecture

### Agent System
```
Research Agent → Analysis Agent → Synthesis Agent → Review Agent → Report Generator
     ↓                  ↓                ↓                ↓                ↓
  Query Parser    Data Extractor   Insight Combiner  Validator    PDF/HTML Output
```

### Data Flow
1. User submits research query via Flutter dashboard
2. Research Agent decomposes query into sub-tasks
3. Agent swarm executes tasks in parallel (where possible)
4. Synthesis Agent combines results into coherent report
5. Review Agent validates accuracy and flags uncertainties
6. Report is delivered to user and stored in knowledge base

## Deployment

Production deployment uses Docker Compose with:
- FastAPI backend on Uvicorn/Gunicorn
- Supabase for database and auth
- Redis for caching and session management
- Celery workers for async agent tasks
- Nginx reverse proxy with SSL

## API Documentation

Interactive API docs available at `/docs` when running locally (FastAPI Swagger UI).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE) for details.

## Contact

**Kiliaan Vanvoorden** — [bakerstreetbandit@zohomail.eu](mailto:bakerstreetbandit@zohomail.eu)
