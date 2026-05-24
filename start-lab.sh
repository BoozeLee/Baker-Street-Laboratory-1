#!/bin/bash
# Baker Street Laboratory - Master Launcher
# Starts all components: Ollama, API, TUI Chat

set -e

cd /home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1
export PATH="$HOME/bin:$PATH"
export OLLAMA_MODELS=/home/kilisan/ollama-models

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${BLUE}🔬 Baker Street Laboratory - Master Launcher${NC}"
echo "============================================"

# 1. Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null 2>&1; then
    echo -e "${YELLOW}Starting Ollama server...${NC}"
    nohup ollama serve > /tmp/ollama-serve.log 2>&1 &
    sleep 3
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}Ollama running on port 11434${NC}"
    else
        echo -e "${RED}Ollama failed to start${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Ollama already running${NC}"
fi

# 2. Start API server if not running
if ! ss -tlnp 2>/dev/null | grep -q ":5000"; then
    echo -e "${YELLOW}Starting API server...${NC}"
    source .venv/bin/activate
    cp .env.example .env 2>/dev/null || true
    nohup gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 "api.app:app" > /tmp/bsl-api.log 2>&1 &
    sleep 2
    if curl -s http://127.0.0.1:5000/api/v1/system/info > /dev/null 2>&1; then
        echo -e "${GREEN}API running on port 5000${NC}"
    else
        echo -e "${RED}API failed to start${NC}"
    fi
else
    echo -e "${GREEN}API already running on port 5000${NC}"
fi

# 3. Launch llama-chat TUI
echo -e "${BLUE}Launching llama-chat TUI...${NC}"
export PATH="$HOME/.cargo/bin:$PATH"
llama-chat --server local

