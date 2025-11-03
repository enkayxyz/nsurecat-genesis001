#!/bin/bash

# Status display utility
# Shows current status of all components

ENV_NAME="nsurecat-env"
BACKEND_PORT=8000
FRONTEND_PORT=8001
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

echo "Application status:"

# Environment status
if conda env list | grep -q "$ENV_NAME"; then
    echo "Environment: SUCCESS ($ENV_NAME)"
else
    echo "Environment: ERROR (Not set up)"
fi

# Backend status
if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat $BACKEND_PID_FILE)" 2>/dev/null; then
    echo "Backend: SUCCESS (PID: $(cat $BACKEND_PID_FILE), Port: $BACKEND_PORT)"
else
    echo "Backend: ERROR (Stopped)"
fi

# Frontend status
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat $FRONTEND_PID_FILE)" 2>/dev/null; then
    echo "Frontend: SUCCESS (PID: $(cat $FRONTEND_PID_FILE), Port: $FRONTEND_PORT)"
else
    echo "Frontend: ERROR (Stopped)"
fi

echo ""
echo "URLs:"
echo "  Backend API: http://localhost:$BACKEND_PORT"
echo "  API Docs: http://localhost:$BACKEND_PORT/docs"
echo "  Frontend: http://localhost:$FRONTEND_PORT"
echo "  Scan Page: http://localhost:$FRONTEND_PORT/scan.html"