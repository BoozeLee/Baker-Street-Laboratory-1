# 🔬 Baker Street Laboratory - System Documentation

Welcome to the Baker Street Laboratory, an autonomous, multi-agent research platform designed for psychedelic detectives, independent coders, and research-focused creators.

## 🚀 The 'Bakery' CLI
The 'Bakery' CLI is your command center. It simplifies the installation and execution of the Laboratory TUI.

### Installation
To install the Laboratory globally, you can use the npm-based installer:
```bash
npm install -g bakery-cli
bakery install
```

### Commands
- **`bakery install`**: Clones the repository, sets up local Flutter dependencies, and prepares the environment.
- **`bakery run`**: Launches the Psychedelic Research TUI.

## 🧠 System Architecture
The system follows a 'Cloud Brain, Local Body' architecture:
1. **Cloud Brain (Codespace):** Runs the 'Swarm' of AI agents (Open Interpreter, Aider, Oracle, etc.) and the FastAPI orchestrator.
2. **Local Body (TUI):** A lightweight Flutter TUI on your laptop that handles visualization and command input.
3. **Bridge:** Connects via secure WebSocket/API over port 5000 (Forwarded).

## 🤖 Agent Swarm
Your laboratory features specialized agents for every task:
- **Aider:** Pair programming, git-native refactoring, and code management.
- **Open Interpreter:** Autonomous OS/Data control and Python automation.
- **The Oracle (DeepSeek-R1):** Deep logical validation and verification of research claims.
- **Amphetamemes Engine:** Psychedelic art generation and data visualization.

## 🛠 Monetization & Scaling
- **Phase I:** Research TUI & Agent Swarm.
- **Phase II:** SaaS Subscription (Supabase Auth).
- **Phase III:** Cloud Migration (Google Cloud Run).
- **Phase IV:** Mobile Transition (Flutter Mobile Adaptive UI).
