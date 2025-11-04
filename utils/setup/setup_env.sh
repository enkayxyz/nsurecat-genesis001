#!/bin/bash

# Environment setup utility
# Creates conda environment for NsureCat

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source configuration
source "$PROJECT_ROOT/utils/config/config.sh"

echo "Setting up NsureCat environment..."
show_config

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH"
    exit 1
fi

# Remove existing environment if it exists
if conda env list | grep -q "$NSURECAT_ENV_NAME"; then
    echo "Removing existing environment '$NSURECAT_ENV_NAME'..."
    conda env remove -n "$NSURECAT_ENV_NAME" -y
fi

echo "Creating conda environment: $NSURECAT_ENV_NAME (Python $PYTHON_VERSION)"
conda create -n "$NSURECAT_ENV_NAME" python=$PYTHON_VERSION -y

echo "SUCCESS: Environment setup complete"