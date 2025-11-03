# Frontend Documentation

This folder contains all documentation for the NsureCat frontend implementation.

## Documentation Index

### Getting Started

- **[Quick Start Guide](quick_start.md)** - Get up and running in 5 minutes
- **[Implementation Summary](implementation_summary.md)** - Complete overview of what was built
- **[Integration Verification](integration_verification.md)** - Testing and verification checklist

### Architecture & Design

The NsureCat frontend is a **single-page chat application** built with **Vanilla HTML/CSS/JavaScript** (no React, no Node.js).

**Key Features:**
- Conversational chat interface with AI assistant (Cat)
- Policy form with validation
- Voice input (Web Speech API) and output (ElevenLabs TTS)
- Wallet connection (MetaMask)
- Dark mode support
- Fully responsive design
- Comprehensive test suite

### File Specifications

The following files contain detailed specifications for the original multi-page approach (now deprecated in favor of the single-page chat interface):

#### Legacy Specifications
- [scan.html.md](scan.html.md) - Policy input form page spec
- [scan.js.md](scan.js.md) - Form submission logic spec
- [results.html.md](results.html.md) - Savings display page spec
- [results.js.md](results.js.md) - Results handling logic spec
- [checkout.html.md](checkout.html.md) - Wallet connection page spec
- [checkout.js.md](checkout.js.md) - Checkout logic spec
- [success.html.md](success.html.md) - Payment success page spec
- [voice.html.md](voice.html.md) - AI voice assistant page spec
- [styles.css.md](styles.css.md) - Global styles spec

**Note:** The legacy specifications above were superseded by the new chat interface (`index.html`, `chat.js`), which combines all functionality into a single conversational flow.

## Quick Links

### Implementation Files
- Source Code: `/src/frontend/`
  - `index.html` - Main chat interface
  - `chat.js` - Application logic
  - `styles.css` - Complete styling

### Tests
- Test Suite: `/tests/frontend/test_chat_flow.py`
- 13 comprehensive Playwright tests

### Related Documentation
- [Frontend Requirements Spec](../front%20end%20req%20spec.md)
- [Integration Specs](../integration%20specs.md)
- [Backend API Documentation](../backend/)
- [Agent Documentation](../agent/)

## Project Structure

```
src/frontend/
├── index.html          # Main chat interface (NEW)
├── chat.js            # Complete app logic (NEW)
├── styles.css         # Full styling with dark mode (UPDATED)
├── scan.html          # Legacy form page
├── results.html       # Legacy results page
├── checkout.html      # Legacy checkout page
├── success.html       # Legacy success page
└── voice.html         # Legacy voice page

docs/frontend/
├── README.md                      # This file
├── quick_start.md                 # 5-minute setup guide
├── implementation_summary.md      # Complete implementation details
├── integration_verification.md    # Testing checklist
└── [legacy specs].md             # Original page specifications

tests/frontend/
└── test_chat_flow.py             # Comprehensive test suite
```

## Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript (ES6+)** - No frameworks
- **Web Speech API** - Voice input
- **ElevenLabs API** - Text-to-speech output
- **MetaMask Web3** - Wallet integration
- **Python http.server** - Static file serving

## Getting Started

1. **Read the [Quick Start Guide](quick_start.md)** for immediate setup
2. **Review [Implementation Summary](implementation_summary.md)** for architecture details
3. **Use [Integration Verification](integration_verification.md)** for testing

## Development Workflow

1. Start backend: `python -m uvicorn src.backend.main:app --reload --port 8000`
2. Start frontend: `cd src/frontend && python -m http.server 3000`
3. Open browser: `http://localhost:3000/index.html`
4. Run tests: `pytest tests/frontend/test_chat_flow.py -v`

## API Endpoints Used

- `POST /v1/shop` - Get savings quotes
- `POST /v1/save` - Process payment
- `POST /api/text-to-speech` - Convert text to speech
- `GET /api/voices` - Get available voices

## Support

For issues, questions, or clarifications, refer to:
- Implementation Summary for architecture decisions
- Integration Verification for troubleshooting
- Test suite for usage examples
