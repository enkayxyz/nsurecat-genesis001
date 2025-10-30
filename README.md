NsureCat (AI Agents on Arc Hackathon)

NsureCat is your personal AI agent (Always-working Insurance Agent) that autonomously shops, monitors, and manages your insurance, saving you time and money.

You just call the cat.

🧩 The Problem

It takes a user 1-3 hours of "comparison hell" to shop for auto/home insurance. They are forced to become part-time experts, navigating confusing bundles and complex liability choices, just to save money.

🎯 Our Hackathon MVP: The "Apples-to-Apples" Agent

We are building a "savings discovery engine" that eliminates this pain.

Step 1: "Policy Scan" (The Input)

User uploads their current policy doc (e.g., their AAA or Geico PDF).

Our agent extracts the "Key 6" coverage points (Liability limits, Deductibles, etc.).

Step 2: The "NsureCat Agent" (The Core Logic)

This is our AI Agent. It takes the "Key 6" and autonomously queries carrier APIs (e.g., Progressive) for new quotes.

It forces an identical "apples-to-apples" comparison, rejecting all carrier upselling.

Step 3: The "One-Number" Dashboard (The Output)

The user sees a dead-simple UI:

Current Policy (AAA): $338/mo
NsureCat Found (Progressive): $297/mo
You Save: $41/mo
[Click to Save $492/year]

v2 Vision (Mockup): We will also mock up our "Community" feature, which shows the user how their rate compares to an anonymized average in their zip code, adding a powerful transparency layer.

🛠️ Hackathon Tech Stack

AI Agents: This is our core Step 2 logic. It's the autonomous shopper that does the 1-3 hours of work in seconds.

Arc with USDC: This is our "Go-Live" payment rail.

Our 'Responsible Rebel' Path: We are not a broker. We partner with a licensed API-first broker to legally bind the policy.

The Flow: When the user clicks "Save," our partner binds the policy. A smart contract on Arc then automatically transfers our 10% success fee (e.g., $49.20) in USDC from the partner to us. It's instant, transparent, and compliant.
