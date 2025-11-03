#!/bin/bash

# Cleanup utility
# Cleans up environment, caches, and stops services

ENV_NAME="nsurecat-env"
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

# Remove conda environment
if conda env list | grep -q "$ENV_NAME"; then
    echo "Removing conda environment '$ENV_NAME'"
    conda env remove -n "$ENV_NAME" -y
fi

echo "SUCCESS: Cleanup completed"