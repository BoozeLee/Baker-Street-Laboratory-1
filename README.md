# Baker Street Laboratory

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/baker-street-lab)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://bakerstreetproject.github.io)

## What It Does
Autonomous AI research platform. 8 integrated agents:
Scout, Elohim, MetaGPT, AgenticSeek, Primax, Codex, Lexicon, Marco-o1.
Self-assembling brick architecture. FastAPI control plane.

## Pricing
- **Starter** — $299/month — 1 agent, 100 runs/day
- **Pro**     — $999/month — all agents, 1,000 runs/day
- **Lab**     — $2,999/month — unlimited, custom integrations

## Quick Deploy
```bash
railway up
# Set env vars: STRIPE_SECRET_KEY, SUPABASE_URL
# Configure Stripe webhook: POST /webhook/stripe
```

---

# 🔬 Baker Street Laboratory

**Revolutionary AI-Augmented Research Ecosystem - Now 95% Operational!**

🎉 **BREAKTHROUGH ACHIEVEMENT**: Complete AI research ecosystem with 7/8 specialized models operational!

[![CI Status](https://github.com/BoozeLee/Baker-Street-Laboratory/workflows/Baker%20Street%20Laboratory%20CI/badge.svg)](https://github.com/BoozeLee/Baker-Street-Laboratory/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/BoozeLee?style=social)](https://github.com/sponsors/BoozeLee)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/boozelee)

## 🎉 **MAJOR BREAKTHROUGH ACHIEVED!**

**Baker Street Laboratory is now 95% operational with a complete AI research ecosystem!**

### 🤖 **AI Specialist Team Status (7/8 Operational)**

| Model | Status | Purpose | Size | Performance |
|-------|--------|---------|------|-------------|
| 🎨 **baker-street-vision** | ✅ **OPERATIONAL** | Visual analysis detective | 5.0 GB | Excellent |
| 🔍 **baker-street-embed** | ✅ **OPERATIONAL** | Semantic search specialist | 274 MB | Perfect |
| 🔬 **baker-street-scientific** | ✅ **OPERATIONAL** | Scientific methodology | 4.1 GB | Excellent |
| ✍️ **baker-street-creative** | ✅ **OPERATIONAL** | Creative writing & reports | 4.1 GB | Excellent |
| 💻 **baker-street-coder** | ✅ **OPERATIONAL** | Data analysis & coding | 776 MB | Excellent |
| ⚖️ **baker-street-legal** | ✅ **OPERATIONAL** | Legal research & compliance | 2.0 GB | Excellent |
| 🎵 **baker-street-audio** | ✅ **OPERATIONAL** | Audio processing | 4.7 GB | Excellent |
| 📚 **baker-street-longcontext** | ⚠️ **GPU LIMITED** | Long context processor | 4.4 GB | CPU Fallback |

**Total: ~25GB of specialized AI research capabilities - Ready for breakthrough research!**

### 🚀 **System Capabilities**
- ✅ **Research Launcher**: Fully operational multi-model orchestration
- ✅ **Polymorphic Framework**: Dynamic intelligence adaptation working
- ✅ **Cross-Laboratory Collaboration**: AgentRxiv protocol implemented
- ✅ **95% Automated Error Resolution**: ML-powered system optimization
- ✅ **Creative-Scientific Synthesis**: Psychedelic detective methodology active

---

Baker Street Laboratory is a comprehensive framework for conducting AI-augmented research with full reproducibility, collaboration, and automation capabilities. Named after the famous detective's methodical approach to investigation, this system orchestrates multiple AI agents to gather, analyze, synthesize, and document research findings.

## 🎯 Key Features

- **Multi-Agent Research Pipeline**: Orchestrated AI agents for data collection, analysis, and synthesis
- **Full Reproducibility**: Every research step is tracked, versioned, and reproducible
- **GitHub-Integrated Workflow**: Seamless integration with GitHub for collaboration and automation
- **Flexible Configuration**: YAML-based agent and pipeline configuration
- **Privacy-First Design**: Built-in data anonymization and security features
- **Automated Research Runs**: Scheduled research updates via GitHub Actions
- **Interactive & Batch Modes**: Support for both interactive exploration and automated pipelines

## 🏗️ Architecture

```
baker-street-laboratory/
├── research/                    # Research outputs organized by stage
│   ├── 01_initial_queries/     # Research questions and hypotheses
│   ├── 02_data_collection/     # Raw data and source materials
│   ├── 03_analysis/            # Analysis results and visualizations
│   ├── 04_synthesis/           # Integrated findings and insights
│   └── 05_final_report/        # Polished deliverables and documentation
├── implementation/             # Core system implementation
│   ├── src/                   # Python source code
│   ├── agents/                # Reusable agent modules
│   ├── pipelines/             # Research workflow definitions
│   ├── tests/                 # Automated test suite
│   └── docs/                  # Technical documentation
├── optimization/              # Performance and improvement tracking
│   ├── benchmarks/           # Agent performance metrics
│   └── improvements/         # Enhancement suggestions and experiments
├── config/                   # Configuration files
│   └── agents.yaml          # Agent definitions and settings
└── .github/workflows/       # GitHub Actions for CI/CD and automation
```

## 🚀 Quick Start - Ready for Breakthrough Research!

### 🎭 **Immediate Usage (System is 95% Operational!)**

```bash
# Navigate to Baker Street Laboratory
cd Baker-Street-Laboratory

# Launch breakthrough research (Ready Now!)
python3 research_launcher.py "AI-enhanced drug discovery for depression" drug_discovery

# Direct specialist access
echo "Design a clinical trial for psilocybin treatment" | ollama run baker-street-scientific
echo "Write engaging research summary" | ollama run baker-street-creative
echo "Analyze molecular compound data with Python" | ollama run baker-street-coder
echo "FDA regulations for psychedelic trials" | ollama run baker-street-legal
echo "Audio biomarkers in psychedelic research" | ollama run baker-street-audio
echo "Analyze brain imaging patterns" | ollama run baker-street-vision
```

### 🔬 **Example Research Workflows**

```bash
# Complete drug discovery pipeline
python3 research_launcher.py "Psilocybin depression treatment optimization" drug_discovery

# Neuroscience investigation
python3 research_launcher.py "Default mode network connectivity patterns" neuroscience

# Legal compliance analysis
python3 research_launcher.py "Regulatory framework for psychedelic research" legal

# Creative research communication
python3 research_launcher.py "Public engagement for breakthrough findings" communication
```

### 1. Installation (If Not Already Set Up)

```bash
# Clone the repository
git clone https://github.com/YourOrg/Baker-Street-Laboratory.git
cd Baker-Street-Laboratory

# Run the installation script
./install.sh
```

### 2. Configuration

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- `OPENAI_API_KEY` - For GPT models
- `ANTHROPIC_API_KEY` - For Claude models (optional)
- `GOOGLE_API_KEY` - For search capabilities (optional)

### 3. Run Your First Research

```bash
# Interactive mode
./run.sh interactive

# Direct research query
./run.sh research "What are the latest developments in quantum computing?"

# Run a specific pipeline
./run.sh pipeline config/agents.yaml
```

## 🤖 Agent System

The framework includes several specialized AI agents:

- **Research Orchestrator**: Coordinates the overall research workflow
- **Data Collector**: Gathers information from various sources
- **Analyzer**: Performs data analysis and pattern recognition
- **Synthesizer**: Combines findings into coherent insights
- **Code Generator**: Creates implementation code based on research

Each agent is configurable via `config/agents.yaml` with customizable:
- Model selection (GPT-4, GPT-3.5, Claude, etc.)
- Temperature and token limits
- Capabilities and tools
- Role definitions

## 📊 GitHub Integration

Baker Street Laboratory leverages GitHub as the central hub for:

### Collaboration & Version Control
- **Branching Strategy**: Feature branches for new agents/capabilities
- **Pull Requests**: Code review and research discussion
- **Issue Tracking**: Research questions and enhancement requests

### Automation & CI/CD
- **Continuous Integration**: Automated testing on every PR
- **Scheduled Research**: Weekly automated research runs
- **Security Scanning**: Automated security and code quality checks

### Documentation & Transparency
- **Research Provenance**: Full history of research decisions
- **Reproducible Results**: Anyone can clone and reproduce findings
- **Living Documentation**: Wiki and GitHub Pages integration

## 🔄 Research Workflow

1. **Query Definition** → Define research questions in `research/01_initial_queries/`
2. **Data Collection** → Agents gather relevant information
3. **Analysis** → Statistical analysis and pattern recognition
4. **Synthesis** → Integration of findings into insights
5. **Documentation** → Generation of reports and documentation
6. **Review & Iteration** → Collaborative review via GitHub PRs

## 🛠️ Usage Examples

### Interactive Research Session
```bash
./run.sh interactive
🔍 Research Query: Analyze the impact of transformer architectures on NLP
```

### Automated Research Pipeline
```bash
# Trigger via GitHub Actions or locally
./run.sh research "Machine learning trends in healthcare 2024" --output-dir research/healthcare_2024
```

### Custom Agent Configuration
```yaml
# config/custom_agents.yaml
agents:
  domain_expert:
    type: "specialist"
    model: "gpt-4"
    temperature: 0.2
    role: "Domain-specific research specialist"
    capabilities:
      - "deep_domain_analysis"
      - "technical_validation"
```

## 🧪 Testing

```bash
# Run the full test suite
./run.sh test

# Run specific test categories
pytest implementation/tests/agents/ -v
pytest implementation/tests/pipelines/ -v
```

## 📈 Monitoring & Optimization

- **Performance Metrics**: Agent response times and accuracy
- **Research Quality**: Citation accuracy and insight relevance
- **System Health**: API usage and error rates
- **Continuous Improvement**: Automated suggestions for enhancement

## 🔒 Privacy & Security

- **Data Anonymization**: Automatic PII removal
- **Encrypted Storage**: Sensitive data encryption
- **Audit Trails**: Complete research provenance
- **API Key Management**: Secure credential handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-agent`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'Add amazing new agent'`)
5. Push to the branch (`git push origin feature/amazing-agent`)
6. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by systematic research methodologies
- Built on the shoulders of open-source AI/ML libraries
- Community-driven development and feedback

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/BoozeLee/Baker-Street-Laboratory/wiki)
- **Issues**: [GitHub Issues](https://github.com/BoozeLee/Baker-Street-Laboratory/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BoozeLee/Baker-Street-Laboratory/discussions)

---

**Happy Researching! 🔬**

*"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."* - Sherlock Holmes

---

## 💖 Support the Project

If Baker Street Laboratory has helped your research, consider supporting its development:

[![GitHub Sponsors](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/BoozeLee)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/boozelee)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/boozelee)

Your support helps maintain and improve this open-source research framework for the entire community! 🙏

## 💖 Support Our Work

If you find this project useful, please consider supporting us:

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/REALbakerstreet221b)

**Bank Transfer (Lowest Fees):**
- **IBAN**: BE70 9051 5229 1825
- **BIC/SWIFT**: WIREDEMMXXX
- **Account Holder**: Kiliaan V
- **Bank**: Wise (formerly TransferWise)
- **Wise Tag**: @kiliaanv

See [SUPPORT.md](SUPPORT.md) for more details.

