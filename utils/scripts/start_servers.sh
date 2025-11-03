#!/bin/bash

# Server startup utility
# Starts backend and frontend servers

ENV_NAME="nsurecat-env"
BACKEND_PORT=8000
FRONTEND_PORT=8001
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

echo "Starting NsureCat servers..."

# Check if environment exists
if ! conda env list | grep -q "$ENV_NAME"; then
    echo "ERROR: Environment '$ENV_NAME' does not exist. Run setup first."
    exit 1
fi

cd "$PROJECT_ROOT"

# Check if backend is already running
if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat $BACKEND_PID_FILE)" 2>/dev/null; then
    echo "WARNING: Backend appears to be already running (PID: $(cat $BACKEND_PID_FILE))"
else
    echo "Starting FastAPI backend on port $BACKEND_PORT"
    conda run -n "$ENV_NAME" uvicorn src.backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
    echo $! > "$BACKEND_PID_FILE"
    echo "SUCCESS: Backend started (PID: $(cat $BACKEND_PID_FILE))"
fi

# Check if frontend is already running
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat $FRONTEND_PID_FILE)" 2>/dev/null; then
    echo "WARNING: Frontend appears to be already running (PID: $(cat $FRONTEND_PID_FILE))"
else
    echo "Starting frontend server on port $FRONTEND_PORT"
    cd src/frontend && python -m http.server $FRONTEND_PORT &
    echo $! > "../$FRONTEND_PID_FILE"
    cd ..
    echo "SUCCESS: Frontend started (PID: $(cat $FRONTEND_PID_FILE))"
fi

echo "SUCCESS: Servers started"
echo "Backend: http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"