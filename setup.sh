#!/bin/bash

# Setup script for NsureCat MVP
# Creates conda environment and installs dependencies

ENV_NAME="nsurecat-env"

echo "Creating conda environment: $ENV_NAME"
conda create -n $ENV_NAME python=3.10 -y

echo "Activating environment and installing requirements"
conda run -n $ENV_NAME pip install -r requirements.txt

echo "Setup complete. Activate with: conda activate $ENV_NAME"</content>
<parameter name="filePath">/Users/enkay/src/dev/nsurecat-genesis001/setup.sh