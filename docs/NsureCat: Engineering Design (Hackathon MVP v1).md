NsureCat: Engineering Design (v1)
Purpose: This document translates the hackathon_reqs.md into a specific engineering plan. It defines our "responsible rebel" architecture and component-level design for the sprint.
Core Architecture: The "Hybrid Stack"
This architecture is designed to meet all hackathon requirements, specifically the JS-based Circle Wallets SDK and ElevenLabs, while keeping our powerful Python AI agent logic.
Frontend (FE): React.js (using npm/Node.js for development).
Backend (BE): FastAPI (Python/Conda).
Separation: The FE and BE are two separate applications.
The React app (FE) runs on its own server (e.g., port 3000).
The FastAPI app (BE) runs on its own Uvicorn server (e.g., port 8000).
The FE makes fetch calls to the BE's API.
High-Level Architecture Diagram
This diagram shows how our components will be built and interact, based on our project_architecture.md file.



Shutterstock
graph TD
    subgraph User's Browser
        A[React Frontend<br/>(src/frontend)]
    end

    subgraph Hackathon Services (Cloud)
        B(Circle Wallets SDK)
        C(ElevenLabs API<br/>Speech-to-Text API)
        D(Arc Testnet Blockchain)
    end

    subgraph Our Backend (Uvicorn Server)
        E[API Routes<br/>(src/api_routes)]
        F[AI Agent<br/>(src/agent/mock_shopper.py)]
        G[Arc/USDC Service<br/>(src/services/arc_service.py)]
        H[Smart Contract<br/>(src/contracts/NsureCatFee.sol)]
    end

    A -- "1. User speaks" --> C
    C -- "2. Text" --> A
    A -- "3. POST /v1/shop<br/>(with Key 6 data)" --> E
    E -- "4. Calls agent" --> F
    F -- "5. Returns MOCKED savings" --> E
    E -- "6. Returns JSON to FE" --> A
    A -- "7. User signs in" --> B
    A -- "8. POST /v1/save" --> E
    E -- "9. Calls service" --> G
    G -- "10. Calls contract (web3.py)" --> D
    H -- "Deployed on" --> D


Component Design & Tech Stack
This maps our hackathon_reqs.md features to our project_architecture.md folders.
src/frontend (React)
Tech: React.js, npm, ethers.js, Circle Wallets SDK.
Scan.js (Component):
Renders the "Key 6" form and "Call the Cat" button.
Handles the ElevenLabs & Speech-to-Text integration for the voice interview.
On submit, calls fetch('POST /v1/shop', ...) to our backend.
Results.js (Component):
Receives the savings JSON.
Renders the "You Save: $246..."
Renders the mockup of the "Community Benchmark."
Handles the "Save Now" click.
Checkout.js (Component):
Manages the "2-Step Checkout."
Integrates Circle Wallets SDK for the "Create Wallet" flow.
Integrates ethers.js for the "Connect Wallet" (MetaMask) flow.
On "Confirm & Pay," calls fetch('POST /v1/save', ...) to our backend.
Success.js (Component):
Renders the "Success!" message.
Renders the mockup of the "Fee Refund Hook."
src/backend & src/api_routes (FastAPI)
Tech: FastAPI, Uvicorn, Pydantic.
POST /v1/shop:
Receives the "Key 6" data (as a Pydantic model).
Calls the mock_shopper.py module.
Returns the hardcoded "savings" JSON.
POST /v1/save:
Receives the user's wallet address.
Calls the arc_service.py module.
Returns "status": "success" or "status": "error".
src/agent (Python)
Tech: Standard Python.
mock_shopper.py:
Contains one function: find_savings(data).
This function will time.sleep(2) and return a hardcoded dictionary: {"savings_6mo": 246.00, "new_carrier": "Rebel Mutual"}.
src/services (Python)
Tech: web3.py.
arc_service.py:
This is the real blockchain "glue."
It connects to the Arc Testnet RPC.
It loads our deployed Smart Contract ABI (from /docs/tech/).
It has one function: process_fee(user_wallet) that calls the payFee() function on our smart contract.
src/contracts (Solidity)
Tech: Solidity.
NsureCatFee.sol:
A real, simple contract we will deploy to the Arc Testnet.
It will have one function: payFee() that transfers a tiny fixed amount (e.g., 0.01 USDC) from the msg.sender (the user's wallet) to our NsureCat treasury wallet.
