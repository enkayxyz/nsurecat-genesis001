# NsureCat Hackathon MVP - Setup & Run Guide

A FastAPI backend with vanilla JavaScript frontend for insurance savings discovery.

## Quick Start

```bash
# Setup environment and dependencies
./nsurecat.sh setup

# Start the application
./nsurecat.sh start

# Open in browser: http://localhost:8001/scan.html
```

## Architecture

- **Backend**: FastAPI (Python) with Uvicorn server
- **Frontend**: Static HTML/CSS/Vanilla JS served by Python http.server
- **AI Agent**: Mocked shopping logic
- **Blockchain**: Web3.py integration with Arc Testnet
- **Environment**: Conda for Python environment management

## Control Script

Use the main control script for all operations:

### Unix/Mac (nsurecat.sh)

```bash
./nsurecat.sh [command]
```

### Windows (nsurecat.bat)

```cmd
nsurecat.bat [command]
```

### Available Commands

| Command | Description |
|---------|-------------|
| `setup` | Create conda environment and install dependencies |
| `start` | Start both backend and frontend servers |
| `stop` | Stop all running servers |
| `test` | Run pytest test suite |
| `check` | Check connectivity to services and dependencies |
| `status` | Show current status of all components |
| `clean` | Clean up environment, caches, and stop services |
| `help` | Show help message |

### Examples

```bash
# Complete setup and startup
./nsurecat.sh setup
./nsurecat.sh start

# Check status
./nsurecat.sh status

# Run tests
./nsurecat.sh test

# Stop everything
./nsurecat.sh stop

# Clean up
./nsurecat.sh clean
```

## Services

- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Frontend**: `http://localhost:8001`
- **Scan Page**: `http://localhost:8001/scan.html`

## Project Structure

```
├── src/
│   ├── backend/          # FastAPI application
│   ├── frontend/         # Static web files
│   ├── api_routes/       # API endpoints
│   ├── agent/           # AI agent logic
│   ├── services/        # External service integrations
│   └── contracts/       # Smart contracts
├── tests/               # Unit tests
├── utils/               # Utility scripts and tools
│   ├── setup/          # Environment setup scripts
│   ├── scripts/        # Operational scripts
│   └── config/         # Configuration and status scripts
├── nsurecat.sh         # Unix/Mac main control script
├── nsurecat.bat        # Windows main control script
└── requirements.txt    # Python dependencies
```
