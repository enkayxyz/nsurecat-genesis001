#!/bin/bash

# Server startup utility
# Starts backend and frontend servers

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source configuration
source "$PROJECT_ROOT/utils/config/config.sh"

BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

echo "Starting NsureCat servers..."
show_config

# Check if environment exists
if ! conda env list | grep -q "$NSURECAT_ENV_NAME"; then
    echo "ERROR: Environment '$NSURECAT_ENV_NAME' does not exist. Run setup first."
    exit 1
fi

cd "$PROJECT_ROOT"

# Check if backend is already running
if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat $BACKEND_PID_FILE)" 2>/dev/null; then
    echo "WARNING: Backend appears to be already running (PID: $(cat $BACKEND_PID_FILE))"
else
    echo "Starting FastAPI backend on port $BACKEND_PORT"
    conda run -n "$NSURECAT_ENV_NAME" uvicorn src.backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
    echo $! > "$BACKEND_PID_FILE"
    echo "SUCCESS: Backend started (PID: $(cat $BACKEND_PID_FILE))"
fi

# Check if frontend is already running
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat $FRONTEND_PID_FILE)" 2>/dev/null; then
    echo "WARNING: Frontend appears to be already running (PID: $(cat $FRONTEND_PID_FILE))"
else
    echo "Starting frontend server on port $FRONTEND_PORT"
    cd src/frontend && python -m http.server $FRONTEND_PORT &
    echo $! > "$PROJECT_ROOT/$FRONTEND_PID_FILE"
    cd "$PROJECT_ROOT"
    echo "SUCCESS: Frontend started (PID: $(cat $FRONTEND_PID_FILE))"
fi

echo "SUCCESS: Servers started"
echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"