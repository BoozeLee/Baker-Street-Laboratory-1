#!/bin/bash
# Baker Street Laboratory — Full System Deployment & Startup
# Supports: Local (docker-compose), K8s (kustomize), Direct (Python)

set -e

echo "🔬 Baker Street Laboratory — Unified Deployment"
echo "==============================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

log()    { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()     { echo -e "${GREEN}[✓]${NC} $1"; }
warn()   { echo -e "${YELLOW}[⚠]${NC} $1"; }
error()  { echo -e "${RED}[✗]${NC} $1"; }
header() { echo -e "\n${MAGENTA}=== $1 ===${NC}\n"; }

# Check prerequisites
check_prereqs() {
  header "Prerequisites Check"

  local missing=0

  # Python
  if command -v python3 &>/dev/null; then
    ok "Python 3 found: $(python3 --version)"
  else
    error "Python 3 required"
    missing=1
  fi

  # Node.js 20+
  if command -v node &>/dev/null; then
    local NODE_VER=$(node --version | sed 's/v//')
    if (( $(echo "$NODE_VER >= 20.0" | bc -l) )); then
      ok "Node.js $NODE_VER found"
    else
      error "Node.js 20+ required"
      missing=1
    fi
  else
    error "Node.js required"
    missing=1
  fi

  # pnpm
  if command -v pnpm &>/dev/null; then
    ok "pnpm found"
  else
    warn "pnpm not found — installing..."
    npm install -g pnpm
  fi

  # Docker (optional)
  if command -v docker &>/dev/null; then
    ok "Docker found"
    DOCKER_AVAILABLE=1
  else
    warn "Docker not found — local services will use direct Python/Node mode"
    DOCKER_AVAILABLE=0
  fi

  # kubectl (optional)
  if command -v kubectl &>/dev/null; then
    ok "kubectl found"
    K8S_AVAILABLE=1
  else
    warn "kubectl not found — K8s deployment disabled"
    K8S_AVAILABLE=0
  fi

  if [ $missing -eq 1 ]; then
    error "Missing required dependencies. Install them and retry."
    exit 1
  fi
}

# Setup Python environment
setup_python() {
  header "Setting Up Python Environment"

  if [ ! -d ".venv" ]; then
    log "Creating virtual environment..."
    python3 -m venv .venv
    ok "Virtual environment created"
  else
    ok "Virtual environment exists"
  fi

  source .venv/bin/activate
  log "Installing Python dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
  ok "Python dependencies installed"

  # Create .env if missing
  if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || true
    cp .env.merged .env 2>/dev/null || true
    warn "Created .env from template — please edit with your API keys"
  fi
}

# Build TypeScript services
build_ts() {
  header "Building TypeScript Services"

  log "Installing Node dependencies..."
  pnpm install --frozen-lockfile

  log "Building all services..."
  pnpm -r build

  ok "TypeScript build complete"
}

# Start local services
start_local() {
  header "Starting Local Services (Direct Mode)"

  log "Starting BSL API in background..."
  source .venv/bin/activate
  nohup python3 implementation/src/main.py --mode api > logs/bsl_api.log 2>&1 &
  echo $! > .bsl_api.pid
  ok "BSL API started (PID $(cat .bsl_api.pid))"

  sleep 2

  log "Starting Brain service..."
  cd brain && npm start > ../logs/brain.log 2>&1 &
  echo $! > ../.brain.pid
  cd ..
  ok "Brain started (PID $(cat .brain.pid))"

  # Start Gateway
  log "Starting Gateway service..."
  cd gateway && npm start > ../logs/gateway.log 2>&1 &
  echo $! > ../.gateway.pid
  cd ..
  ok "Gateway started (PID $(cat .gateway.pid))"

  # Wait for health
  log "Waiting for services to become ready..."
  sleep 5

  echo ""
  ok "All services started!"
  echo ""
  echo "Endpoints:"
  echo "  BSL API:  http://localhost:5000/api/v1/docs"
  echo "  Brain:    http://localhost:30000/health"
  echo "  Chat:     http://localhost:30000/api/v1/chat"
  echo "  Gateway:  http://localhost:8080"
  echo ""
  echo "To stop: ./stop.sh"
  echo "To view logs: tail -f logs/*.log"
}

# Start with Docker Compose
start_docker() {
  header "Starting Services with Docker Compose"

  if [ $DOCKER_AVAILABLE -ne 1 ]; then
    error "Docker not available. Use 'local' mode instead."
    exit 1
  fi

  # Create directories
  mkdir -p data/vector_store data/cache logs

  log "Building Docker images..."
  ./docker-deploy.sh build

  log "Starting containers..."
  docker-compose up -d

  # Wait for health
  log "Waiting for health checks..."
  sleep 15

  # Check status
  docker-compose ps

  ok "Services started via Docker Compose"
  echo ""
  echo "Endpoints same as above."
  echo "Logs: docker-compose logs -f [service]"
}

# Deploy to Kubernetes
deploy_k8s() {
  header "Deploying to Kubernetes"

  if [ $K8S_AVAILABLE -ne 1 ]; then
    error "kubectl not available."
    exit 1
  fi

  # Ensure Docker images built
  if [ "$(docker images -q bsl-brain 2>/dev/null)" = "" ]; then
    warn "Brain image not built. Building..."
    ./docker-deploy.sh build
  fi

  # Load images into K8s nodes if needed (kind/minikube)
  # kind load docker-image bsl-brain:latest

  local KUSTOMIZE_OVERLAY="${KUSTOMIZE_OVERLAY:-merged}"

  log "Applying Kustomize overlay: $KUSTOMIZE_OVERLAY"
  kubectl apply -k "k8s/overlays/${KUSTOMIZE_OVERLAY}"

  # Wait for rollout
  log "Waiting for deployments..."
  kubectl -n bakerst rollout status deployment/bsl-api
  kubectl -n bakerst rollout status deployment/brain

  ok "Deployment complete"
  echo ""
  echo "Access via port-forward:"
  echo "  kubectl port-forward -n bakerst svc/bsl-api 5000:5000"
  echo "  kubectl port-forward -n bakerst svc/brain 30000:30000"
}

# Stop all services
stop_services() {
  header "Stopping Services"

  if [ -f .bsl_api.pid ]; then
    kill $(cat .bsl_api.pid) 2>/dev/null && rm .bsl_api.pid
    ok "BSL API stopped"
  fi

  if [ -f .brain.pid ]; then
    kill $(cat .brain.pid) 2>/dev/null && rm .brain.pid
    ok "Brain stopped"
  fi

  if [ -f .gateway.pid ]; then
    kill $(cat .gateway.pid) 2>/dev/null && rm .gateway.pid
    ok "Gateway stopped"
  fi

  # Stop Docker
  if [ $DOCKER_AVAILABLE -eq 1 ]; then
    docker-compose down 2>/dev/null || true
    ok "Docker containers stopped"
  fi

  ok "All services stopped"
}

# Test integration
test_integration() {
  header "Running Integration Tests"

  chmod +x test-integration.sh
  ./test-integration.sh
}

# Main menu
main() {
  MODE="${1:-local}"

  case "$MODE" in
    check)
      check_prereqs
      ;;
    setup)
      check_prereqs
      setup_python
      build_ts
      ;;
    local)
      check_prereqs
      setup_python
      build_ts
      start_local
      ;;
    docker)
      check_prereqs
      build_ts
      start_docker
      ;;
    k8s|kubectl)
      check_prereqs
      build_ts
      deploy_k8s
      ;;
    stop)
      stop_services
      ;;
    rebuild)
      stop_services
      setup_python
      build_ts
      start_local
      ;;
    test)
      test_integration
      ;;
    *)
      echo "Usage: $0 {check|setup|local|docker|k8s|stop|rebuild|test}"
      echo ""
      echo "Modes:"
      echo "  check    — Verify prerequisites"
      echo "  setup    — Install Python deps, build TS (no start)"
      echo "  local    — Start BSL API + Brain + Gateway directly (default)"
      echo "  docker   — Start via docker-compose"
      echo "  k8s      — Deploy to Kubernetes cluster"
      echo "  stop     — Stop all running services"
      echo "  rebuild  — Stop, rebuild, and restart"
      echo "  test     — Run integration test suite"
      echo ""
      echo "K8s Overlay: export KUSTOMIZE_OVERLAY=staging|production"
      exit 1
      ;;
  esac
}

main "$@"
