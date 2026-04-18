#!/bin/bash
# Docker & ArangoDB Setup Script
# This script sets up ArangoDB Docker container with proper permissions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"
V3_DIR="$(dirname "$MODULE_DIR")"
ENV_FILE="$SCRIPT_DIR/.env"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.base.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        ArangoDB & Docker Setup for JARVIS V3.0                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# 1. Check Docker installation
echo -e "${BLUE}Step 1: Checking Docker Installation${NC}"
if ! command -v docker &> /dev/null; then
    print_error "Docker not found. Please install Docker first."
    echo "Visit: https://docs.docker.com/engine/install/"
    exit 1
fi
print_status "Docker installed: $(docker --version)"
echo ""

# 2. Check Docker daemon
echo -e "${BLUE}Step 2: Checking Docker Daemon${NC}"
if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running or you don't have permission"
    echo ""
    print_info "Fix permission issues:"
    echo "  Option 1: Add current user to docker group (requires restart)"
    echo "    sudo usermod -aG docker \$USER"
    echo "    newgrp docker"
    echo ""
    echo "  Option 2: Use sudo for docker commands"
    echo "    Remember to prepend 'sudo' to docker and docker-compose commands"
    echo ""
    exit 1
fi
print_status "Docker daemon is running"
echo ""

# 3. Create .env file if it doesn't exist
echo -e "${BLUE}Step 3: Setting up .env Configuration${NC}"
if [ -f "$ENV_FILE" ]; then
    print_warning "File already exists: $ENV_FILE"
    echo "  Skipping creation (modify manually if needed)"
else
    cp "$SCRIPT_DIR/.env.example" "$ENV_FILE"
    print_status "Created: $ENV_FILE"
fi
echo ""

# 4. Check if containers are already running
echo -e "${BLUE}Step 4: Checking for Running Containers${NC}"
if docker ps --format "table {{.Names}}" | grep -q "arangodb-server"; then
    print_warning "ArangoDB container already running"
    echo "  Use 'docker ps' to see all running containers"
    echo "  Use 'docker stop arangodb-server' to stop it"
else
    print_status "No ArangoDB containers running (ready to start)"
fi
echo ""

# 5. Check for existing volumes
echo -e "${BLUE}Step 5: Checking Docker Volumes${NC}"
if docker volume ls --format "table {{.Name}}" | grep -q "arangodb"; then
    print_warning "Existing ArangoDB volumes found:"
    docker volume ls --format "table {{.Name}}" | grep arangodb
else
    print_status "No existing ArangoDB volumes"
fi
echo ""

# 6. Start containers
echo -e "${BLUE}Step 6: Starting Containers${NC}"
read -p "Start ArangoDB containers now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Starting containers from: $COMPOSE_FILE"
    
    if docker-compose -f "$COMPOSE_FILE" up -d; then
        print_status "Containers started successfully"
        echo ""
        echo "  Container: arangodb-server (port 8529)"
        echo "  Container: mcp-arangodb"
    else
        print_error "Failed to start containers"
        exit 1
    fi
else
    print_info "Skipped container startup"
    echo "  To start manually, run:"
    echo "    cd $SCRIPT_DIR"
    echo "    docker-compose -f docker-compose.base.yml up -d"
fi
echo ""

# 7. Health check
echo -e "${BLUE}Step 7: Health Check${NC}"
if docker ps --format "table {{.Names}}" | grep -q "arangodb-server"; then
    print_info "Waiting for ArangoDB to be ready... (this may take 1-2 minutes)"
    
    # Check health status
    max_attempts=30
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if docker exec arangodb-server curl -s -u root:test123 http://localhost:8529/_api/version &> /dev/null; then
            print_status "ArangoDB is ready and responding"
            break
        fi
        echo -ne "\r  Checking... [$((attempt + 1))/$max_attempts]"
        sleep 2
        ((attempt++))
    done
    
    if [ $attempt -ge $max_attempts ]; then
        print_warning "ArangoDB health check timed out"
        echo "  Container may still be initializing"
        echo "  Check logs: docker logs arangodb-server"
    fi
else
    print_warning "Containers not running - skipped health check"
fi
echo ""

# 8. Configuration summary
echo -e "${BLUE}Step 8: Configuration Summary${NC}"
print_info "Docker Module Location: $SCRIPT_DIR"
print_info "Configuration File: $ENV_FILE"
print_info "Compose File: $COMPOSE_FILE"
echo ""

# 9. Usage instructions
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                     Setup Complete!                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Access ArangoDB Web UI:"
echo "   http://localhost:8529"
echo "   User: root"
echo "   Password: test123"
echo ""
echo "2. View container logs:"
echo "   docker logs arangodb-server"
echo ""
echo "3. Stop containers:"
echo "   docker-compose -f $COMPOSE_FILE down"
echo ""
echo "4. Test Python operations:"
echo "   cd $MODULE_DIR/arangodb/python-ops"
echo "   python3 -c 'from ops import arango_http_up; print(arango_http_up())'"
echo ""
echo "5. Use ArangoDB agent:"
echo "   cd $V3_DIR"
echo "   python3 arangodb_agent.py"
echo ""
