#!/bin/bash

# Cleanup utility
# Cleans up environment, caches, and stops services

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
# Source configuration
source "$PROJECT_ROOT/utils/config/config.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

echo "Cleaning up..."

# Stop services first
"$SCRIPT_DIR/stop_servers.sh"

cd "$PROJECT_ROOT"

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

if conda env list | grep -q "$NSURECAT_ENV_NAME"; then
    echo "Removing conda environment '$NSURECAT_ENV_NAME'"
    conda env remove -n "$NSURECAT_ENV_NAME" -y
fi

echo "SUCCESS: Cleanup completed"