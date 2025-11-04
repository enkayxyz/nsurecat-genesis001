# How to Run Tests - Quick Reference

## 1. Install Test Dependencies (First Time Only)

```bash
pip install pytest playwright pytest-playwright
playwright install chromium
```

## 2. Start Servers (Every Time Before Testing)

### Terminal 1 - Start Backend:
```bash
python -m uvicorn src.backend.main:app --reload --port 8000
```

### Terminal 2 - Start Frontend:
```bash
cd src/frontend
python -m http.server 8001
```

## 3. Run Tests (Terminal 3)

```bash
# Run all frontend tests
pytest tests/frontend/test_chat_flow.py -v

# Run specific test
pytest tests/frontend/test_chat_flow.py::test_page_loads_with_greeting -v

# Run with more details
pytest tests/frontend/test_chat_flow.py -v -s
```

## That's It!

**See full guide:** `docs/frontend/TESTING_GUIDE.md`

**Manual testing checklist:** `docs/frontend/integration_verification.md`
