#!/bin/bash

# Test runner utility
# Runs pytest test suite

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source configuration
source "$PROJECT_ROOT/utils/config/config.sh"

echo "Running tests..."
show_config

# Check if environment exists
if ! conda env list | grep -q "$NSURECAT_ENV_NAME"; then
    echo "ERROR: Environment '$NSURECAT_ENV_NAME' does not exist. Run setup first."
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Installing/updating Python dependencies from requirements.txt..."
conda run -n "$NSURECAT_ENV_NAME" pip install -r requirements.txt

echo "Installing Playwright browsers..."
conda run -n "$NSURECAT_ENV_NAME" python -m playwright install chromium

echo "Activating environment and running pytest (all tests)"
PYTHONPATH=src conda run -n "$NSURECAT_ENV_NAME" pytest tests/ $PYTEST_ARGS --browser chromium

echo "SUCCESS: Tests completed"