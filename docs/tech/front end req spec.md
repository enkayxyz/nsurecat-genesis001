# NsureCat Frontend Requirements Specification (MVP v1) - Chat Interface

## What is NsureCat?

NsureCat is a cutting-edge web application designed to revolutionize insurance shopping. It empowers users to input their current auto insurance policy details, leverages AI-powered agents to compare quotes from multiple carriers, and provides personalized savings recommendations. Users can interact via text forms or voice input (integrated with ElevenLabs for natural speech synthesis and recognition), and securely pay a small fee via blockchain (Arc Testnet) to unlock their savings. The app aims to make insurance shopping transparent, efficient, and accessible, with a focus on user experience through modern web technologies.

## Purpose

The purpose of NsureCat is to democratize insurance shopping by using AI to identify better, cheaper policies tailored to users' needs. It reduces the friction of manual quote comparisons, incorporates voice accessibility for inclusivity, and ensures secure, decentralized payments. For the MVP, it demonstrates a seamless flow from policy input to savings realization, setting the stage for a full-fledged fintech platform.

## Overview

NsureCat is a web app/website for insurance shoppers to input their current policy details, get AI-powered savings quotes, and pay a fee via blockchain to unlock the savings. The app uses voice input for accessibility and ElevenLabs for text-to-speech.

**Goal**: Build a compact React SPA with a single chat interface. The app should feel like a modern conversational AI tool—clean, secure, and user-friendly. Total estimated components: ~10-15 React components.

**User Flow** (Conversational Chat):

1. Cat greets user, offers form/dropdowns or voice input for policy details.
2. Processes input, asks for missing info if needed (or reads policy if uploaded).
3. Shows summary: "I see you have [carrier] policy in [state] paying $[amount] per six months. It's not bad, but let's see if we can do better."
4. Lists carriers, animates "reaching out" via agents, calls Shop API, produces results.
5. Nudges user to choose one result.
6. Prompts wallet connection (Circle or MetaMask with USDC).
7. Handles policy switching, calculates refund from current policy, charges wallet with payment + fees (10% of savings), shows "You have saved 90% of savings."

**Tech Stack**: React 18+, TypeScript (for type safety), Tailwind CSS (for styling, to keep it compact), Axios for API calls, React Router for navigation (minimal, as it's mostly single-page chat).

**API Endpoints** (Super Specific—Developer Must Use These Exact Calls):

- **Shop API**: `POST http://localhost:8000/v1/shop`
  - Request Body: JSON object with keys: `bodily_injury` (string), `property_damage` (string), `uninsured_motorist` (string), `collision` (string), `comprehensive` (string), `personal_injury_protection` (string). All are required strings (e.g., "100/300").
  - Response: JSON `{ "savings_6mo": number, "new_carrier": string }` (e.g., `{ "savings_6mo": 246.00, "new_carrier": "Rebel Mutual" }`).
  - Error: 500 with `{ "detail": string }`.

- **Save API**: `POST http://localhost:8000/v1/save`
  - Request Body: JSON `{ "wallet_address": string }` (e.g., "0x123...").
  - Response: JSON `{ "status": "success" }`.
  - Error: 500 with `{ "detail": string }`.

- **Text-to-Speech API**: `POST http://localhost:8000/api/text-to-speech`
  - Request Body: JSON `{ "text": string, "voice_id": string }` (voice_id defaults to "21m00Tcm4TlvDq8ikWAM").
  - Response: Audio stream (MPEG).
  - Error: 400/500 with `{ "detail": string }`.

- **Voices API**: `GET http://localhost:8000/api/voices`
  - Response: JSON array of voice objects.
  - Error: 500 with `{ "detail": string }`.

**Global Requirements**:

- **CORS/Origins**: Backend allows all origins, so no issues.
- **Authentication**: None—public app.
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari) with Web Speech API support for voice.
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support.
- **Performance**: Lazy-load components, optimize images/icons.
- **Security**: No sensitive data stored client-side; use HTTPS in production.
- **Themes**: Toggle between light (default) and dark mode. Persist in localStorage (`theme: 'light'|'dark'`). Apply via `document.documentElement.classList.toggle('dark')`.
- **Responsiveness**: Mobile-first (320px+), tablet (768px+), desktop (1024px+). Use Tailwind breakpoints. Chat bubbles stack vertically, touch-friendly.
- **Voice Integration**: Full ElevenLabs integration for TTS and voice selection. Use Web Audio API for playback. Cat speaks responses via TTS, user inputs via Web Speech API.
- **Error Handling**:
  - Network errors: Show "Network error. Please check your connection and try again."
  - API 500 errors: Show "Server error. Please try again later."
  - Validation errors: Inline messages (e.g., "This field is required").
  - Loading states: Spinners/buttons disabled during API calls.
  - Unexpected errors: Generic "Something went wrong. Please refresh the page."

- **Use Cases**:
  - **Happy Path**: User chats with Cat → Inputs details → Gets summary → Sees results → Chooses → Pays → Success.
  - **Edge Cases**: Invalid wallet address → Error on save. No MetaMask → Prompt to install. Voice not supported → Fallback to text input.
  - **Error Scenarios**: API timeout → Retry button. Invalid form → Highlight fields.

## Chat Interface and Components (Super Specific)

### Single Chat Screen (Route: `/`)

- **Purpose**: Entire app is a conversational chat with Cat (the AI assistant).
- **Layout**: Centered chat window with message bubbles (Cat: left, User: right). Header with theme toggle. Footer with input area. Responsive: Bubbles full-width on mobile, max-width on desktop.
- **Components**:
  - `NsureCatChatBubble`: Reusable for messages (text, with optional TTS play button).
  - `NsureCatInputArea`: Text input or voice button at bottom. Embeds `NsureCatQuickForm` (dropdowns for coverage fields) or `NsureCatVoiceInputButton`.
  - `NsureCatAgentAnimation`: Animated spinner/text when "firing up agents" (e.g., "Reaching out to carriers...").
  - `NsureCatResultsDisplay`: Embedded in chat as bubbles showing savings options.
  - `NsureCatWalletModal`: Popup for Circle/MetaMask connection and payment.
  - `NsureCatThemeToggleButton`: Sun/moon icon in header.
- **Conversational Flow**:
  - **Greeting**: Cat says "Hi! I'm Cat. Let's find you better insurance. How would you like to share your policy details? Form, voice, or upload?"
  - **Data Collection**: User selects form → Shows dropdowns (e.g., state: NJ, carrier: Geico, amount: $975). Or voice → Triggers Web Speech API, Cat confirms via TTS. If missing, Cat asks "What's your bodily injury coverage?"
  - **Summary**: Cat says "I see you have Geico policy in NJ paying $975 per six months. It's not bad, but let's see if we can do better."
  - **Processing**: Cat lists carriers (e.g., "Progressive, Allstate..."), animates agents, calls Shop API, shows results as bubbles (e.g., "Rebel Mutual: Save $246/6mo").
  - **Selection**: Cat nudges "Which one looks good? Click to choose."
  - **Payment**: On choice, Cat says "Great! Now connect your wallet to switch and save." Opens modal for Circle/MetaMask. On connect, Cat calculates refund (from current policy), charges payment + 10% fee of savings, shows "You have saved 90% of savings."
- **Buttons/Interactions**:
  - Voice button: Starts/stops recognition, plays Cat's TTS responses.
  - Form button: Toggles quick form in chat.
  - Choose result: Buttons in result bubbles.
  - Wallet connect/pay: In modal, disable during loading.
- **Error Handling**: Form validation in chat. API errors as Cat messages (e.g., "Oops, server issue. Try again."). Voice errors: "Voice failed, type instead."
- **Use Cases**: User chats naturally → Cat guides → Animates processing → Results appear → Payment completes.

## Additional Components

- **NsureCatHeaderNavbar**: Simple header with title "Chat with Cat" and theme toggle.
- **NsureCatFooter**: Input area and voice button.
- **NsureCatLoadingSpinner**: For API calls.
- **NsureCatErrorToast**: For notifications.
- **NsureCatThemeContext**: Global context for theme.
- **Global State**: Context for `chatHistory`, `userData`, `selectedResult`, `walletAddress`, `theme`.

## Expected Behavior and Use Cases (Detailed)

- **On Load**: Start with greeting message. Persist chat history in localStorage for session.
- **Navigation**: Minimal routing; mostly state-driven chat.
- **API Calls**: Triggered by chat actions (e.g., on form submit or voice result).
- **Themes**: Toggle affects chat bubbles (light: white, dark: gray).
- **Responsiveness**: Chat scrolls on mobile, bubbles adapt.
- **Voice Integration**: Cat responds with TTS; user inputs via speech.
- **Component Naming**: All as specified—long names ensure clarity (e.g., `NsureCatChatBubble`).
- **Testing Hooks**: Use data-testid on bubbles/buttons for Playwright.
