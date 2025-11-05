# Legacy Frontend Files (Archived)

**Date Archived**: 2025-11-05
**Reason**: Replaced by unified chat interface (index.html)

## What's Here

This directory contains the original multi-page flow that was deprecated in favor of the modern single-page chat interface.

### Archived Files:

1. **scan.html / scan.js**
   - Old policy input form
   - Collected 6 coverage fields in traditional form layout
   - Replaced by: Chat interface policy form modal

2. **results.html / results.js**
   - Old results display page
   - Showed savings quote after form submission
   - Replaced by: Chat message with quote display

3. **checkout.html / checkout.js**
   - Old checkout/payment page
   - Had TODO at line 9: "Wallet creation not implemented yet"
   - Replaced by: Chat flow with wallet modal integration

4. **success.html**
   - Old success confirmation page
   - Replaced by: Chat success message

5. **voice.html**
   - Standalone voice input page
   - Replaced by: Integrated voice button in chat interface

## Why These Were Deprecated

The original design used a traditional multi-page flow:
```
scan.html → results.html → checkout.html → success.html
```

This was replaced with a conversational AI-driven chat interface that:
- ✅ Provides better UX (single page, no navigation)
- ✅ Matches hackathon theme (AI agent interaction)
- ✅ Integrates voice seamlessly
- ✅ Better mobile experience
- ✅ More engaging for insurance shopping

## Current Frontend

The active frontend is:
- **index.html** - Main chat interface (single-page app)
- **chat.js** - Chat logic, API integration, voice, wallet modal
- **styles.css** - Modern responsive styling
- **config.js** - Frontend configuration

## Test Coverage

Legacy pages are not tested. Current chat interface has:
- 17/18 tests passing (94.4%)
- See: `tests/frontend/test_chat_flow.py`

## Should I Delete These?

**Keep for now** if:
- Want reference for how forms/flows worked
- May need to extract specific logic
- Historical record for development

**Delete if**:
- Confident all needed logic is in chat interface
- Want to clean up codebase
- No longer useful for reference

---

**Last Updated**: 2025-11-05
