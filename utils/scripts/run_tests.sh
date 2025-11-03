#!/bin/bash

# Test runner utility
# Runs pytest test suite

ENV_NAME="nsurecat-env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "Running tests..."

# Check if environment exists
if ! conda env list | grep -q "$ENV_NAME"; then
    echo "ERROR: Environment '$ENV_NAME' does not exist. Run setup first."
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Installing Playwright browsers..."
conda run -n "$ENV_NAME" python -m playwright install chromium

echo "Activating environment and running pytest"
conda run -n "$ENV_NAME" pytest tests/ -v --browser chromium

echo "SUCCESS: Tests completed"