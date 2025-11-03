# NsureCat (Genesis) 🐱 | AI Agents on Arc Hackathon

Welcome to the nsurecat-genesis repository. This is our "responsible rebel" submission for the AI Agents on Arc with USDC Hackathon.

## Our Hook: "1 minute with the 'Cat' can save you 10% or more."

## Our Ethos: "You just call the cat."

NsureCat is your personal AI agent that autonomously shops for insurance, transforming a 3-hour nightmare into a 1-minute conversation.

## 🚀 The Hackathon MVP Flow

We are building a "working prototype" that demonstrates the entire AI-driven payment flow.

### Step 1: "Call the Cat" (Input)

A user lands on our app and provides their 6 key policy details.

**Hackathon Tech**: We provide two ways: a simple form or a "Call the Cat" button that uses the ElevenLabs Voice AI for a guided interview.

### Step 2: "AI Agent Shop" (Processing)

The user clicks "Find My Savings."

**Hackathon Tech**: Our frontend calls our FastAPI (Python) backend, which triggers our AI Agent to find the best "apples-to-apples" quote. (For the sprint, this agent's external calls are mocked).

### Step 3: "On-Chain Checkout" (Action)

The user sees their savings (e.g., "$246 for 6 months!") and clicks "Save Now."

**Hackathon Tech (Account Abstraction)**: The user creates a new, seamless wallet in seconds using the Circle Wallets SDK OR connects an existing wallet.

**Hackathon Tech (Arc / USDC)**: After funding from the Arc Testnet Faucet, the user's wallet executes a real Smart Contract on the Arc Testnet, transferring our 10% fee (e.g., 0.01 USDC) to the NsureCat treasury.

## 🛠️ Core Technology Stack

This project uses a hybrid, "responsible rebel" architecture to meet all hackathon requirements.

- **Frontend**: HTML5, CSS3 & Vanilla JavaScript (to support the required wallet and voice SDKs)
- **Backend**: Python 3.10+ with FastAPI & Uvicorn
- **AI Agent**: Python modules using AI logic (mocked for sprint)
- **Voice**: ElevenLabs (for voice interview) & Speech-to-Text
- **Wallets**: Circle Wallets SDK & ethers.js
- **Blockchain**: Arc Testnet
- **Smart Contracts**: Solidity
- **Payment**: USDC (on Arc Testnet)
- **Environment**: Conda (for backend)

## 📁 Project Structure

This project follows our Standard Python Web Stack Architecture.

```text
/src/frontend/: All static HTML, CSS & Vanilla JS source code.
/src/backend/: Main FastAPI (Python) application logic.
/src/api_routes/: FastAPI routers that connect the FE and BE.
/src/agent/: Core Python logic for the NsureCat AI agent.
/src/services/: Python modules for external calls (e.g., Arc, ElevenLabs).
/src/contracts/: Solidity smart contract source.
/tests/: Pytest test suite.
/docs/: All product and technical documentation.
/utils/: Utility scripts and tools.
```

## 🚀 Quick Start

See [run.md](run.md) for detailed setup and run instructions.

```bash
# Setup and start the application
./nsurecat.sh setup
./nsurecat.sh start

# Open: http://localhost:8001/scan.html
```

## 📚 Documentation

- **[run.md](run.md)** - Setup and run instructions
- **[docs/](docs/)** - Product requirements and technical documentation
