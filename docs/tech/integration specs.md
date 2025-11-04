# NsureCat Integration Specifications

This document details how the frontend (React chat interface) interacts with the backend, agent code, API routes, voice components, and other parts of the system. It ensures seamless integration for the AI agent or developer building the frontend.

## Overall Architecture

- **Frontend**: Single-page React app (chat UI) running on `http://localhost:3000`. It uses Axios to make HTTP requests to the backend.
- **Backend**: FastAPI server on `http://localhost:8000`, handling API routes, voice synthesis, and CORS.
- **Agent Code**: Python modules in `src/agent/` (e.g., `mock_shopper.py`) for AI logic.
- **API Routes**: FastAPI routers in `src/api_routes/` (e.g., `shop.py`, `save.py`) that connect frontend to backend/agent.
- **Voice**: ElevenLabs for TTS (backend), Web Speech API for user input (frontend).
- **Blockchain/Services**: `src/services/arc_service.py` for payments.

Interactions are API-driven: Frontend sends data → Backend processes → Calls agent/services → Returns response → Frontend updates chat.

## Chat Flow and Interactions

### Step 1: Greeting & Data Collection

- **Frontend Action**: User starts chat. Cat (frontend logic) sends greeting message. User selects "Form" or "Voice" input.
  - If form: Shows embedded `NsureCatQuickForm` (dropdowns for policy fields: bodily_injury, etc.).
  - If voice: Triggers Web Speech API (`webkitSpeechRecognition`), transcribes speech.
- **Backend/Agent Interaction**: None yet—data collected client-side. If voice fails, fallback to text.
- **API Calls**: None.
- **Voice**: User speaks → Frontend transcribes → Cat confirms via ElevenLabs TTS (see below).

### Step 2: Processing & Asking for Missing Info

- **Frontend Action**: On form submit or voice result, validates data. If missing (e.g., no bodily_injury), Cat asks in chat: "What's your bodily injury coverage?"
- **Backend/Agent Interaction**: None—validation is client-side.
- **API Calls**: None.
- **Voice**: Cat's question played via TTS if enabled.

### Step 3: Summary & Confirmation

- **Frontend Action**: Once data complete, Cat displays summary in chat: "I see you have Geico policy in NJ paying $975 per six months. It's not bad, but let's see if we can do better."
- **Backend/Agent Interaction**: None—summary is frontend-generated from collected data.
- **API Calls**: None.
- **Voice**: Summary spoken via TTS.

### Step 4: Agent Processing & Results

- **Frontend Action**: Cat lists carriers (e.g., "Progressive, Allstate..."), shows `NsureCatAgentAnimation` (e.g., "Reaching out to carriers..."), calls Shop API.
- **Backend/Agent Interaction**:
  - Frontend POSTs to `http://localhost:8000/v1/shop` with policy data (JSON: {bodily_injury: "100/300", ...}).
  - Backend's `shop.py` router receives → Calls `agent.mock_shopper.find_savings(data)` → Agent simulates AI (sleeps 2s, returns mock savings: {savings_6mo: 246.00, new_carrier: "Rebel Mutual"}).
  - Backend returns JSON to frontend.
- **API Calls**: 1x POST /v1/shop (triggers agent).
- **Voice**: Animation message spoken via TTS.

### Step 5: Selection

- **Frontend Action**: Results appear as chat bubbles (e.g., "Rebel Mutual: Save $246/6mo"). Cat nudges: "Which one looks good?" User clicks button in bubble.
- **Backend/Agent Interaction**: None—selection client-side.
- **API Calls**: None.
- **Voice**: Nudge spoken via TTS.

### Step 6: Wallet & Payment

- **Frontend Action**: On selection, Cat opens `NsureCatWalletModal` for Circle/MetaMask. User connects (calls `window.ethereum.request({ method: 'eth_requestAccounts' })`), Cat calculates refund/payment/fees, calls Save API.
- **Backend/Agent Interaction**:
  - Frontend POSTs to `http://localhost:8000/v1/save` with {wallet_address: "0x123..."}.
  - Backend's `save.py` router receives → Calls `services.arc_service.process_fee(wallet)` → Service connects to Arc Testnet, calls smart contract (NsureCatFee.sol) to transfer USDC fee.
  - Backend returns {status: "success"}.
- **API Calls**: 1x POST /v1/save (triggers blockchain service).
- **Voice**: Payment confirmation spoken via TTS.

### Step 7: Success

- **Frontend Action**: Cat shows final message: "You have saved 90% of savings." (Calculates: savings - 10% fee).
- **Backend/Agent Interaction**: None.
- **API Calls**: None.
- **Voice**: Success spoken via TTS.

## Voice Integration Details

- **ElevenLabs (Backend)**: Frontend calls POST /api/text-to-speech (from backend.main) with {text: "message", voice_id: "21m00Tcm4TlvDq8ikWAM"} → Backend streams MPEG audio → Frontend plays via `<audio>` element.
- **Web Speech API (Frontend)**: For user input—transcribes speech to text, fills form/chat.
- **Voices List**: Optional GET /api/voices → Frontend populates dropdown for voice selection.
- **Errors**: Audio load fails → Fallback to text-only.

## Error Handling & Edge Cases

- **Network/API Errors**: Frontend shows in chat (e.g., "Server error. Try again."). Retries once on 500.
- **Agent Failures**: If Shop API fails, Cat says "Agents couldn't reach carriers. Try again."
- **Voice Failures**: "Voice not supported" → Disable button.
- **Wallet Failures**: "MetaMask not detected" → Prompt install.

## Data Flow Summary

- **Frontend → Backend**: JSON payloads via Axios.
- **Backend → Agent/Services**: Direct Python calls (e.g., `find_savings()`).
- **Agent/Services → Backend**: Return dicts/JSON.
- **Backend → Frontend**: JSON responses.
- **Persistence**: Chat history in localStorage; no server-side storage.
