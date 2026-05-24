#!/bin/bash
# Baker Street Laboratory — Full Deployment
# Deploys BSL API + Brain + Gateway + Worker + Message Bus + Vector Store

set -e

echo "🏪 Baker Street Laboratory — Deployment Script"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prereqs() {
  log_info "Checking prerequisites..."

  if ! command -v docker &> /dev/null; then
    log_error "Docker not found. Install from https://docs.docker.com/get-docker/"
    exit 1
  fi

  if ! command -v docker-compose &> /dev/null; then
    log_error "docker-compose not found. Install Docker Compose plugin."
    exit 1
  fi

  # Check .env file
  if [ ! -f .env ]; then
    log_warn ".env file not found. Copying from .env.merged..."
    cp .env.merged .env
    log_warn "Please edit .env with your actual API keys before continuing."
    exit 1
  fi

  log_success "Prerequisites satisfied"
}

# Build all images
build_images() {
  log_info "Building Docker images..."

  # Build BSL API image (if custom Dockerfile.api exists)
  if [ -f Dockerfile.api ]; then
    docker build -t bsl-api:latest -f Dockerfile.api .
    log_success "BSL API image built"
  fi

  # Build Brain image
  if [ -f Dockerfile.brain ]; then
    # Install dependencies for monorepo
    (cd brain && npm ci --only=production)
    docker build -t bsl-brain:latest -f Dockerfile.brain .
    log_success "Brain image built"
  fi

  # Build Gateway
  if [ -f Dockerfile.gateway ]; then
    (cd gateway && npm ci --only=production)
    docker build -t bsl-gateway:latest -f Dockerfile.gateway .
    log_success "Gateway image built"
  fi

  # Build Worker
  if [ -f Dockerfile.worker ]; then
    (cd worker && npm ci --only=production)
    docker build -t bsl-worker:latest -f Dockerfile.worker .
    log_success "Worker image built"
  fi
}

# Start services
start_services() {
  log_info "Starting services with docker-compose..."

  # Create data directories
  mkdir -p data/vector_store data/cache logs

  # Start stack
  docker-compose up -d

  log_success "Services started"
}

# Wait for health
wait_for_health() {
  log_info "Waiting for services to become healthy..."
  sleep 10

  local services=("bsl-api" "brain")
  for svc in "${services[@]}"; do
    log_info "Waiting for $svc..."
    if docker-compose ps | grep -q "$svc.*healthy"; then
      log_success "$svc is healthy"
    else
      log_warn "$svc not yet healthy — checking status..."
      docker-compose logs --tail=20 $svc
    fi
  done
}

# Bootstrap features (Future: Baker Street features)
bootstrap_features() {
  log_info "Bootstrapping features (placeholder)..."
  # Future: upload feature zips to NATS object store
  # node scripts/bootstrap-features.mjs
}

# Show status
show_status() {
  log_info "Deployment Summary"
  echo "===================="
  echo ""
  echo "Service endpoints:"
  echo "  BSL API:        http://localhost:5000/api/v1/docs"
  echo "  Brain Agent:    http://localhost:30000/health"
  echo "  Brain Chat:     http://localhost:30000/api/v1/chat"
  echo "  Gateway (Web):  http://localhost:8080"
  echo "  NATS Monitor:   http://localhost:8222"
  echo "  Qdrant:         http://localhost:6333"
  echo "  Ollama:         http://localhost:11434"
  echo ""
  echo "Next steps:"
  echo "  1. Test API: curl http://localhost:5000/api/v1/system/status"
  echo "  2. Chat:     curl -X POST http://localhost:30000/api/v1/chat ..."
  echo "  3. Deploy to K8s: KUSTOMIZE_OVERLAY=merged scripts/deploy-all.sh"
  echo ""
}

# Main
main() {
  case "${1:-}" in
    build)
      check_prereqs
      build_images
      ;;
    up)
      check_prereqs
      start_services
      wait_for_health
      show_status
      ;;
    down)
      log_info "Stopping all services..."
      docker-compose down
      log_success "Services stopped"
      ;;
    logs)
      docker-compose logs -f "${2:-}"
      ;;
    rebuild)
      check_prereqs
      docker-compose down
      build_images
      start_services
      wait_for_health
      show_status
      ;;
    *)
      echo "Usage: $0 {build|up|down|logs|rebuild}"
      echo ""
      echo "Commands:"
      echo "  build    — Build all Docker images"
      echo "  up       — Start all services (default)"
      echo "  down     — Stop and remove all services"
      echo "  logs     — View logs (optionally specify service)"
      echo "  rebuild  — Rebuild everything and restart"
      echo ""
      echo "Environment:"
      echo "  Set OPENAI_API_KEY, ANTHROPIC_API_KEY in .env"
      exit 1
      ;;
  esac
}

main "$@"
