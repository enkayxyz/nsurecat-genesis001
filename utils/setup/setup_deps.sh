#!/bin/bash

# Dependencies installation utility
# Installs Python requirements in conda environment

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source configuration
source "$PROJECT_ROOT/utils/config/config.sh"

echo "Installing Python dependencies..."

# Check if environment exists
if ! conda env list | grep -q "$NSURECAT_ENV_NAME"; then
    echo "ERROR: Environment '$NSURECAT_ENV_NAME' does not exist. Run setup_env.sh first."
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Activating environment and installing requirements"
conda run -n "$NSURECAT_ENV_NAME" pip install -r requirements.txt

echo "SUCCESS: Dependencies installed"