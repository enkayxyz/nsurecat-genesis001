# NsureCat Frontend - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### 1. Start Backend (Terminal 1)
```bash
cd /Users/enkay/src/dev/nsurecat-genesis001
python -m uvicorn src.backend.main:app --reload --port 8000
```

### 2. Start Frontend (Terminal 2)
```bash
cd /Users/enkay/src/dev/nsurecat-genesis001/src/frontend
python -m http.server 3000
```

### 3. Open Browser
Navigate to: **http://localhost:3000/index.html**

---

## 📋 What You'll See

1. **Chat greeting from Cat** 🐱
2. **Two quick reply buttons**: Form | Voice
3. Click **"Form"** to test the flow

---

## ✅ Test the Happy Path (2 minutes)

### Step 1: Click "Form"
- Modal opens with policy form

### Step 2: Fill Form
- **State**: NJ
- **Carrier**: Geico
- **Amount**: 975
- **Bodily Injury**: 100/300
- **Property Damage**: 50000
- **Uninsured Motorist**: 50/100
- **Collision**: 500
- **Comprehensive**: 500
- **Personal Injury Protection**: 50000

### Step 3: Submit
- Click "Submit"
- See summary message
- See loading animation
- See result card with savings

### Step 4: Choose Result
- Click "Choose This" button
- Wallet modal opens

### Step 5: Test Without MetaMask
- If no MetaMask: See error message ✅
- With MetaMask: Connect and complete payment ✅

---

## 🎨 Test Other Features

### Theme Toggle
- Click 🌙 icon in header
- Page switches to dark mode
- Click ☀️ to switch back

### Voice Button
- Click 🎤 in footer
- Note: Requires browser support (Chrome/Edge)

### Chat Persistence
- Send some messages
- Refresh page
- Messages are restored ✅

---

## 🧪 Run Automated Tests

```bash
# Install dependencies (first time only)
pip install pytest playwright pytest-playwright
playwright install

# Run tests
pytest tests/frontend/test_chat_flow.py -v
```

---

## 📁 New Files Created

- ✅ `src/frontend/index.html` - Main chat page
- ✅ `src/frontend/chat.js` - Complete app logic (600+ lines)
- ✅ `src/frontend/styles.css` - Full redesign with dark mode
- ✅ `tests/frontend/test_chat_flow.py` - 13 comprehensive tests
- ✅ `tests/frontend/INTEGRATION_VERIFICATION.md` - Detailed guide

---

## 🔧 Files Modified

- ✅ `src/backend/main.py` - Added router includes
- ✅ `src/frontend/README.md` - Updated docs

---

## ❓ Issues?

### Backend not connecting?
```bash
# Check if running:
curl http://localhost:8000/docs
```

### Frontend not loading?
```bash
# Check if running:
curl http://localhost:3000/index.html
```

### Port already in use?
```bash
# Kill process on port 8000:
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000:
lsof -ti:3000 | xargs kill -9
```

---

## 📖 Full Documentation

- **README**: `src/frontend/README.md`
- **Integration Tests**: `tests/frontend/INTEGRATION_VERIFICATION.md`
- **Implementation Summary**: `FRONTEND_IMPLEMENTATION_SUMMARY.md`

---

## ✨ What's Working

✅ Complete chat interface with Cat
✅ Policy form with validation
✅ API integration (Shop & Save)
✅ Loading states & error handling
✅ Theme toggle (light/dark)
✅ Voice input (Web Speech API)
✅ Voice output (ElevenLabs TTS)
✅ Wallet modal (MetaMask ready)
✅ Responsive design (mobile/tablet/desktop)
✅ LocalStorage persistence
✅ Accessibility (ARIA labels, keyboard nav)
✅ Comprehensive test suite

---

## 🎯 Architecture

**Vanilla JavaScript** (No React/Node.js as per requirements)
- HTML5 + CSS3 + ES6+ JavaScript
- Python http.server for frontend
- FastAPI for backend
- 2-layer architecture

---

**Ready to go! 🚀**
