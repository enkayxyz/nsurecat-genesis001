#!/bin/bash

# Environment setup utility
# Creates conda environment for NsureCat

ENV_NAME="nsurecat-env"

echo "Setting up NsureCat environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH"
    exit 1
fi

# Remove existing environment if it exists
if conda env list | grep -q "$ENV_NAME"; then
    echo "Removing existing environment '$ENV_NAME'..."
    conda env remove -n "$ENV_NAME" -y
fi

echo "Creating conda environment: $ENV_NAME"
conda create -n "$ENV_NAME" python=3.10 -y

echo "SUCCESS: Environment setup complete"