# Frontend Integration Verification

This document provides steps to verify that the frontend is properly integrated with the backend.

## Prerequisites

1. **Backend Running**: FastAPI server on `http://localhost:8000`
2. **Frontend Running**: HTTP server on `http://localhost:3000`
3. **Environment**: ELEVENLABS_API_KEY set (optional, for voice features)

## Starting the Servers

### Backend (Terminal 1):
```bash
cd /Users/enkay/src/dev/nsurecat-genesis001
# Activate conda environment first
python -m uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Terminal 2):
```bash
cd /Users/enkay/src/dev/nsurecat-genesis001/src/frontend
python -m http.server 3000
```

## Manual Verification Checklist

### 1. Page Load
- [ ] Navigate to `http://localhost:3000/index.html`
- [ ] Verify Cat's greeting message appears
- [ ] Verify "Form" and "Voice" quick reply buttons appear
- [ ] Check browser console for no JavaScript errors

### 2. Theme Toggle
- [ ] Click theme toggle button (moon/sun icon)
- [ ] Verify page switches to dark mode
- [ ] Click again to verify switch back to light mode
- [ ] Refresh page and verify theme persists

### 3. Policy Form Flow
- [ ] Click "Form" quick reply button
- [ ] Verify modal opens with policy form
- [ ] Fill out all required fields:
  - State: NJ
  - Carrier: Geico
  - Amount: 975
  - Bodily Injury: 100/300
  - Property Damage: 50000
  - Uninsured Motorist: 50/100
  - Collision: 500
  - Comprehensive: 500
  - Personal Injury Protection: 50000
- [ ] Click "Submit"
- [ ] Verify modal closes

### 4. API Integration - Shop Endpoint
- [ ] After form submission, verify summary message appears
- [ ] Verify loading spinner appears with "Reaching out to carriers..." message
- [ ] Verify loading spinner disappears after ~2 seconds
- [ ] Verify result card appears with:
  - Carrier name (e.g., "Rebel Mutual")
  - Savings amount (e.g., "$246.00/6mo")
  - "Choose This" button
- [ ] Check browser network tab for successful POST to `/v1/shop`

### 5. Wallet Connection (Requires MetaMask)
- [ ] Click "Choose This" button on result card
- [ ] Verify wallet modal opens
- [ ] Verify MetaMask and Circle buttons are visible
- [ ] If MetaMask installed:
  - [ ] Click "Connect MetaMask"
  - [ ] Approve connection in MetaMask popup
  - [ ] Verify wallet address appears (truncated)
  - [ ] Verify payment processing occurs
  - [ ] Check browser network tab for POST to `/v1/save`
  - [ ] Verify success message appears with net savings

### 6. Voice Features (Optional - Requires ELEVENLABS_API_KEY)
- [ ] Click microphone button
- [ ] Verify it changes to stop icon
- [ ] Speak a message
- [ ] Verify voice is transcribed to text
- [ ] Verify Cat's response has TTS button (🔊)
- [ ] Click TTS button
- [ ] Verify audio plays

### 7. Error Handling
- [ ] Stop backend server
- [ ] Try to submit form
- [ ] Verify error toast appears
- [ ] Verify Cat shows error message
- [ ] Restart backend

### 8. Responsive Design
- [ ] Open browser DevTools
- [ ] Switch to mobile view (375x667)
- [ ] Verify layout adjusts properly
- [ ] Verify all buttons are clickable
- [ ] Verify chat bubbles stack vertically

### 9. Accessibility
- [ ] Use keyboard only (Tab navigation)
- [ ] Verify can focus and activate all buttons
- [ ] Verify form fields are keyboard accessible
- [ ] Check that focus indicators are visible

### 10. LocalStorage Persistence
- [ ] Send some messages in chat
- [ ] Refresh the page
- [ ] Verify chat history is restored
- [ ] Open browser DevTools > Application > Local Storage
- [ ] Verify `nsurecat_chat_history` exists and contains messages

## Automated Testing

Run Playwright tests:

```bash
# Install dependencies (if not already done)
pip install pytest playwright pytest-playwright

# Install browsers
playwright install

# Run tests with mocked APIs
pytest tests/frontend/test_chat_flow.py -v

# Run integration tests (requires backend running)
pytest tests/frontend/test_chat_flow.py -v -m integration
```

## Common Issues

### Issue: "Cannot connect to backend"
**Solution**: Ensure backend is running on port 8000

### Issue: "CORS error"
**Solution**: Backend already configured with `allow_origins=["*"]`

### Issue: "Voice button disabled"
**Solution**: Browser doesn't support Web Speech API (use Chrome/Edge)

### Issue: "MetaMask not detected"
**Solution**: Install MetaMask browser extension

### Issue: "TTS not working"
**Solution**: Ensure `ELEVENLABS_API_KEY` environment variable is set

### Issue: "Chat history not persisting"
**Solution**: Check browser allows localStorage (not in private/incognito mode)

## API Endpoint Verification

### Test Shop API directly:
```bash
curl -X POST http://localhost:8000/v1/shop \
  -H "Content-Type: application/json" \
  -d '{
    "bodily_injury": "100/300",
    "property_damage": "50000",
    "uninsured_motorist": "50/100",
    "collision": "500",
    "comprehensive": "500",
    "personal_injury_protection": "50000"
  }'
```

Expected response:
```json
{
  "savings_6mo": 246.00,
  "new_carrier": "Rebel Mutual"
}
```

### Test Save API directly:
```bash
curl -X POST http://localhost:8000/v1/save \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"
  }'
```

Expected response:
```json
{
  "status": "success"
}
```

### Test TTS API directly (requires ELEVENLABS_API_KEY):
```bash
curl -X POST http://localhost:8000/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Cat!",
    "voice_id": "21m00Tcm4TlvDq8ikWAM"
  }' \
  --output test.mp3
```

Should download an MP3 file.

## Success Criteria

✅ All manual verification steps pass
✅ All automated tests pass
✅ No console errors in browser
✅ Network requests succeed (200 status)
✅ Chat history persists across refreshes
✅ Theme persists across refreshes
✅ Responsive design works on mobile sizes
✅ Keyboard navigation works

## Next Steps After Verification

1. Deploy to staging environment
2. Conduct user acceptance testing
3. Add more test coverage
4. Optimize performance
5. Add analytics tracking
6. Implement Circle wallet integration
7. Add policy document upload feature
