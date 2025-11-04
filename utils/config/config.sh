#!/bin/bash
# NsureCat Configuration
# This file defines all environment variables and configuration used across the project
# Source this file in all scripts to ensure consistency

# Environment
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

# Directories (config is in utils/config, so go up two levels to reach project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
export BACKEND_DIR="${PROJECT_ROOT}/src/backend"
export FRONTEND_DIR="${PROJECT_ROOT}/src/frontend"
export TESTS_DIR="${PROJECT_ROOT}/tests"

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
