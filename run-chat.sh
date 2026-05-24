#!/bin/bash
# Baker Street Laboratory - TUI Chat Launcher
# Launches parllama with the Ollama backend

cd /home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1
source .venv/bin/activate

# Ensure Ollama is running
if ! pgrep -x ollama > /dev/null 2>&1; then
    echo "Starting Ollama..."
    export PATH="$HOME/bin:$PATH"
    export OLLAMA_MODELS=/home/kilisan/ollama-models
    nohup ollama serve > /tmp/ollama-serve.log 2>&1 &
    sleep 3
fi

# Launch parllama TUI
echo "🚀 Launching Baker Street Chat TUI..."
parllama --ollama-url http://127.0.0.1:11434 --theme-name monokai --theme-mode dark
