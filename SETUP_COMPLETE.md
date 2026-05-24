# 🔬 Baker Street Laboratory - Setup Complete

## Quick Start Commands

```bash
# Universal prefix
export PATH="$HOME/bin:$HOME/.cargo/bin:$PATH"

# Start everything
bsl start

# Chat with AI models
bsl chat

# Run research query
bsl research "your query here"

# Check system status
bsl status

# List models
bsl models

# View reports
bsl reports

# Pull a new model
bsl pull <model-name>

# Or use alias
bakery status
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              BAKER STREET LABORATORY             │
├──────────────┬──────────────┬───────────────────┤
│   API Server │  Ollama      │  TUI Chat Client  │
│   (port 5000)│  (port 11434)│  parllama/llama   │
│              │              │  -chat             │
├──────────────┴──────────────┴───────────────────┤
│  8 Specialized AI Agents:                        │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐           │
│  │Vision   │ │Scientific│ │Creative │           │
│  ├─────────┤├──────────┤├─────────┤           │
│  │Embed    │ │Coder     │ │Legal    │           │
│  ├─────────┤├──────────┤├─────────┤           │
│  │LongCtx  │ │Audio     │ │Hermes3  │           │
│  └─────────┘ └──────────┘ └─────────┘           │
├─────────────────────────────────────────────────┤
│  Research Pipeline → Reports (research/*.md)     │
└─────────────────────────────────────────────────┘
```

## Files & Locations

- `~/bin/bsl` - Main command-line tool
- `~/bin/bakery` - Alias for bsl
- `~/bin/ollama` - Ollama binary
- `~/.cargo/bin/parllama` - TUI chat client
- `~/.cargo/bin/llama-chat` - Alternative Rust TUI
- `~/ollama-models/` - Downloaded model storage
- `config/model-profiles/` - Per-agent configurations
- `research/` - Generated research reports
- `tools/bsl_tools.py` - Custom Python tools
- `parllama-config.json` - Chat client configuration
