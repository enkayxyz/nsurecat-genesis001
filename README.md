# NsureCat Hackathon MVP

A FastAPI backend with vanilla JavaScript frontend for insurance savings discovery.

## Architecture

- **Backend**: FastAPI (Python) with Uvicorn server
- **Frontend**: Static HTML/CSS/Vanilla JS served by Python http.server
- **AI Agent**: Mocked shopping logic
- **Blockchain**: Web3.py integration with Arc Testnet
- **Environment**: Conda for Python environment management

## Setup

1. Run `./setup.sh` to create conda environment and install dependencies.
2. Run `./start.sh` to start both backend (port 8000) and frontend (port 8001) servers.
3. Open `http://localhost:8001/scan.html` in your browser.

## Testing

Run `./test.sh` to execute pytest tests.

## Project Structure

- `src/backend/`: FastAPI application
- `src/frontend/`: Static web files
- `src/api_routes/`: API endpoints
- `src/agent/`: AI agent logic
- `src/services/`: External service integrations
- `tests/`: Unit tests
Hackathon-Specific Requirements
These are the non-negotiable features required to meet the hackathon's technical judging criteria.
AI Agent (Must-Have):
The system must have a distinct AI Agent component (in the code) that is triggered by Step 2.
For the hackathon, this agent's logic will be mocked (it returns a hardcoded JSON).
Account Abstraction (Must-Have):
We must use one of the "Account Abstraction" tools.
We will use the Circle Wallets SDK on the frontend to provide a "seamless wallet creation" flow (e.g., "Sign in with Google").
We will also support connecting an existing wallet to satisfy power users.
Arc / USDC (Must-Have):
We must deploy a real, simple Smart Contract to the Arc Testnet.
When the user completes the "2-Step Checkout," our backend will call this contract to transfer a small amount of Testnet USDC (simulating our 10% fee).
Voice AI (Must-Have):
We must integrate ElevenLabs to hit the prize category.
This will be the "Call the Cat" voice-driven interview for our "Step 1" input.
v2 Vision (Mockup-Only):
The "Results" page will feature a visual-only mockup of our "Community Benchmark" feature.
The final "Success!" page will feature a visual-only mockup of our "Fee Refund Hook" (e.g., "We've applied your $24.60 fee as a credit. Let NsureCat shop for your next policy, and it's on us!").
Out of Scope (The "Rebel Discipline")
To ensure we finish, the following are explicitly out of scope for the hackathon:
NO traditional email/password database (the Circle Wallet is the user's login and identity).
NO real-world carrier API integrations (all quotes are mocked).
NO real-world bank account linking (we will use the Testnet Faucet).
