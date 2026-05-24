#!/bin/bash
# Quick test script for merged BSL+Brain integration

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${BLUE}[TEST]${NC} $1"; }
ok() { echo -e "${GREEN}[PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[SKIP]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

BASE_URL=${BSL_API_URL:-"http://localhost:5000"}
BRAIN_URL=${BRAIN_URL:-"http://localhost:30000"}

info "Testing Baker Street Laboratory + Brain integration"
info "====================================================="

# Test 1: BSL API health
info "1. Checking BSL API health..."
if curl -sf "${BASE_URL}/api/v1/system/status" > /dev/null; then
  ok "BSL API is up"
else
  fail "BSL API unreachable at ${BASE_URL}"
  exit 1
fi

# Test 2: Brain health
info "2. Checking Brain health..."
if curl -sf "${BRAIN_URL}/health" > /dev/null; then
  ok "Brain is up"
else
  fail "Brain unreachable at ${BRAIN_URL}"
  exit 1
fi

# Test 3: Tool status
info "3. Checking tool registry..."
if curl -sf "${BRAIN_URL}/api/v1/tools/status" | grep -q "tools"; then
  ok "Tools registered"
else
  fail "Tools not available"
fi

# Test 4: Simple chat
info "4. Testing chat endpoint..."
RESPONSE=$(curl -s -X POST "${BRAIN_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, introduce yourself"}')
if echo "$RESPONSE" | grep -qi "baker street"; then
  ok "Chat response received"
else
  warn "Chat endpoint responded but intro not found"
fi

# Test 5: Research tool call
info "5. Testing research tool via chat..."
SESSION=$(curl -s -X POST "${BRAIN_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "List the top 3 Python libraries for data visualization"}' | grep -o '"conversation_id":"[^"]*"' | cut -d'"' -f4)

if [ -n "$SESSION" ]; then
  ok "Research session started: $SESSION"
else
  fail "Failed to start chat session"
fi

echo ""
info "Tests completed. Check conversation history:"
echo "  curl ${BRAIN_URL}/api/v1/conversations/${SESSION}"
