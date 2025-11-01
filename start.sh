#!/bin/bash

# Start script for NsureCat MVP
# Activates conda env, starts backend and frontend servers

ENV_NAME="nsurecat-env"
BACKEND_PORT=8000
FRONTEND_PORT=8001

echo "Activating conda environment: $ENV_NAME"
conda activate $ENV_NAME

echo "Starting FastAPI backend on port $BACKEND_PORT"
uvicorn src.backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &

echo "Starting frontend server on port $FRONTEND_PORT"
cd src/frontend && python -m http.server $FRONTEND_PORT &

echo "Servers started. Backend: http://localhost:$BACKEND_PORT, Frontend: http://localhost:$FRONTEND_PORT"
echo "Press Ctrl+C to stop"

# Wait for background processes
wait</content>
<parameter name="filePath">/Users/enkay/src/dev/nsurecat-genesis001/start.sh