#!/bin/bash
# NsureCat Configuration
# This file defines all environment variables and configuration used across the project
# Source this file in all scripts to ensure consistency

export NSURECAT_ENV_NAME="nsurecat"
export PYTHON_VERSION="3.10"

# Ports
export BACKEND_PORT=8000
export FRONTEND_PORT=8001

# URLs (derived from ports)
export BACKEND_URL="http://localhost:${BACKEND_PORT}"
export FRONTEND_URL="http://localhost:${FRONTEND_PORT}"

# API Configuration
export API_BASE_URL="${BACKEND_URL}"

## Directories are set by each CLI script, not here

# Testing
export TEST_TIMEOUT=30000
export PYTEST_ARGS="-v --tb=short"

# Development
export UVICORN_RELOAD="--reload"
export LOG_LEVEL="info"

# Display configuration (useful for debugging)
show_config() {
    echo "=== NsureCat Configuration ==="
    echo "Environment: ${NSURECAT_ENV_NAME}"
    echo "Python: ${PYTHON_VERSION}"
    echo "Backend: ${BACKEND_URL}"
    echo "Frontend: ${FRONTEND_URL}"
    echo "Project Root: ${PROJECT_ROOT}"
    echo "============================="
}

# Export marker to detect if config is loaded
export NSURECAT_CONFIG_LOADED=1
