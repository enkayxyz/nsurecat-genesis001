NsureCat: Hackathon MVP Requirements (v1)

Purpose: This document defines the high-level functional requirements and "must-haves" for the NsureCat hackathon submission.

Hackathon MVP Flowchart

This diagram outlines the complete user journey for our "working prototype."

graph TD
    A[Start: User lands on scan.html] --> B{User Input Method?};
    B -- Form --> C[User fills 'Key 6' form];
    B -- Voice --> D[User clicks 'Call the Cat'];
    D -- ElevenLabs/Speech-to-Text --> C;
    C --> E[User clicks 'Find My Savings'];
    E --> F[FE calls 'POST /v1/shop'];
    F --> G[BE: AI Agent runs<br/>(Simulated 2-sec shop)];
    G --> H[BE: Agent returns JSON savings];
    H --> I[FE: Show results.html<br/>'You Save: $246 for 6 months!'];
    I --> J{User clicks 'Save Now'};
    J --> K[FE: Display '2-Step Checkout'<br/>1. Create/Connect Wallet<br/>2. Fund & Pay];
    K --> L{User choice};
    L -- Create --> M[FE: User creates wallet via<br/>Circle Wallets SDK (e.g., Google Login)];
    L -- Connect --> N[FE: User connects<br/>existing wallet (e.g., MetaMask)];
    M --> O[FE: User funds new wallet via<br/>Arc Testnet Faucet];
    N --> P[User clicks 'Confirm & Pay 10% Fee'];
    O --> P;
    P --> Q[FE calls 'POST /v1/save'];
    Q --> R[BE: Calls real Arc Smart Contract];
    R --> S[Arc Contract: Transfers Testnet USDC<br/>(e.g., 0.01 USDC) from User to NsureCat];
    S --> T[BE: Returns 'success'];
    T --> U[FE: Show 'Success!' page];
    U --> V[FE: Display 'v2 Refund Hook' mockup on<br/>Success Page];


Core User Flow (The 3-Step Demo)

The MVP will demonstrate the core NsureCat "3-Step Flow" to prove our value.

Step 1: The "Policy Scan" (Input)

A user lands on a simple page.

The user is presented with three input options:

A simple form for the "Key 6" values (e.g., Bodily Injury).

A (mocked) "Upload Policy" button.

A "Call the Cat" button that launches the ElevenLabs Voice Agent to fill the form.

(Note: The exact "Key 6" fields to be defined by Product/Anushka).

Step 2: The "Agent Shop" (Processing)

The user clicks "Find My Savings."

The system will simulate the NsureCat AI Agent shopping for "apples-to-apples" quotes (2-3 second delay).

Step 3: The "Value & Checkout" (Output & Action)

The user is directed to a results page and sees the savings upfront (e.g., "You Save: $246 for 6 months!").

The user clicks "Save Now."

The UI presents a "2-Step Checkout":

Create/Connect Wallet: The user is given two options:

Create: A new, seamless wallet via the Circle Wallets SDK.

Connect: An existing wallet (e.g., MetaMask).

Fund & Pay: The user (if they created a new wallet) is guided to the Arc Testnet Faucet to fund it, then confirms the 10% fee payment.

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