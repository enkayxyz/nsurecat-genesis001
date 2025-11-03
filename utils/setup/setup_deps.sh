#!/bin/bash

# Dependencies installation utility
# Installs Python requirements in conda environment

ENV_NAME="nsurecat-env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "Installing Python dependencies..."

# Check if environment exists
if ! conda env list | grep -q "$ENV_NAME"; then
    echo "ERROR: Environment '$ENV_NAME' does not exist. Run setup_env.sh first."
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Activating environment and installing requirements"
conda run -n "$ENV_NAME" pip install -r requirements.txt

echo "SUCCESS: Dependencies installed"