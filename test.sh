#!/bin/bash

# Test script for NsureCat MVP
# Activates conda env and runs pytest

ENV_NAME="nsurecat-env"

echo "Activating conda environment: $ENV_NAME"
conda activate $ENV_NAME

echo "Running tests"
pytest tests/

echo "Tests complete"</content>
<parameter name="filePath">/Users/enkay/src/dev/nsurecat-genesis001/test.sh