#!/bin/bash

# Server stop utility
# Stops backend and frontend servers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

echo "Stopping NsureCat servers..."

# Stop backend
if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat $BACKEND_PID_FILE)" 2>/dev/null; then
    echo "Stopping backend (PID: $(cat $BACKEND_PID_FILE))"
    kill "$(cat $BACKEND_PID_FILE)"
    rm "$BACKEND_PID_FILE"
    echo "SUCCESS: Backend stopped"
else
    echo "WARNING: Backend does not appear to be running"
fi

# Stop frontend
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat $FRONTEND_PID_FILE)" 2>/dev/null; then
    echo "Stopping frontend (PID: $(cat $FRONTEND_PID_FILE))"
    kill "$(cat $FRONTEND_PID_FILE)"
    rm "$FRONTEND_PID_FILE"
    echo "SUCCESS: Frontend stopped"
else
    echo "WARNING: Frontend does not appear to be running"
fi

echo "SUCCESS: Servers stopped"