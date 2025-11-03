#!/bin/bash

# Connectivity check utility
# Checks connectivity to services and dependencies

ENV_NAME="nsurecat-env"
BACKEND_PORT=8000
FRONTEND_PORT=8001
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "Checking connectivity..."

# Check backend
if curl -s http://localhost:$BACKEND_PORT/ > /dev/null 2>&1; then
    echo "SUCCESS: Backend server is accessible on port $BACKEND_PORT"
else
    echo "ERROR: Backend server is not accessible on port $BACKEND_PORT"
fi

# Check frontend
if curl -s http://localhost:$FRONTEND_PORT/ > /dev/null 2>&1; then
    echo "SUCCESS: Frontend server is accessible on port $FRONTEND_PORT"
else
    echo "ERROR: Frontend server is not accessible on port $FRONTEND_PORT"
fi

# Check Arc Testnet
if curl -s --max-time 10 https://rpc-testnet.arbitrum.io > /dev/null 2>&1; then
    echo "SUCCESS: Arc Testnet RPC is accessible"
else
    echo "WARNING: Arc Testnet RPC is not accessible (may be temporary)"
fi

# Check if environment is set up
if conda env list | grep -q "$ENV_NAME"; then
    echo "SUCCESS: Conda environment '$ENV_NAME' exists"
else
    echo "ERROR: Conda environment '$ENV_NAME' does not exist"
fi

# Check Python dependencies
if conda env list | grep -q "$ENV_NAME"; then
    if conda run -n "$ENV_NAME" python -c "import fastapi, uvicorn, pydantic" 2>/dev/null; then
        echo "SUCCESS: Python dependencies are installed"
    else
        echo "ERROR: Python dependencies are not properly installed"
    fi
fi

echo "Connectivity check completed"