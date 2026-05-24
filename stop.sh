#!/bin/bash
# Stop all running BSL+Brain services

set -e

echo "🛑 Stopping Baker Street Laboratory services..."

# Kill direct-mode processes
if [ -f .bsl_api.pid ]; then
  kill $(cat .bsl_api.pid) 2>/dev/null && rm .bsl_api.pid
  echo "✓ BSL API stopped"
fi

if [ -f .brain.pid ]; then
  kill $(cat .brain.pid) 2>/dev/null && rm .brain.pid
  echo "✓ Brain stopped"
fi

if [ -f .gateway.pid ]; then
  kill $(cat .gateway.pid) 2>/dev/null && rm .gateway.pid
  echo "✓ Gateway stopped"
fi

# Stop Docker
if command -v docker-compose &>/dev/null; then
  docker-compose down 2>/dev/null && echo "✓ Docker containers stopped"
fi

echo "All services stopped."
