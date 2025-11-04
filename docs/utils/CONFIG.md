# NsureCat Configuration System

## Overview

This project uses a centralized configuration system to ensure consistency across all scripts, tests, and code. **All ports, environment names, and URLs are defined in configuration files** - never hardcoded.

**Location**: All configuration files are in `utils/config/`

## Configuration Files

### 1. `utils/config/config.sh` (Bash/Shell Scripts)
Used by all `.sh` scripts in the project.

```bash
# Source this at the top of any bash script
source "$PROJECT_ROOT/utils/config/config.sh"

# Access variables
echo $BACKEND_PORT      # 8000
echo $FRONTEND_PORT     # 8001
echo $BACKEND_URL       # http://localhost:8000
echo $FRONTEND_URL      # http://localhost:8001
echo $NSURECAT_ENV_NAME # nsurecat
```

### 2. `config.bat` (Windows Scripts)
Used by all `.bat` scripts in the project.

```batch
REM Source this at the top of any batch script
call "%~dp0config.bat"

REM Access variables
echo %BACKEND_PORT%
echo %FRONTEND_PORT%
```

### 3. `config.py` (Python Scripts & Tests)
Used by Python code, pytest tests, and backend.

```python
# Import at the top of any Python file
from config import BACKEND_PORT, FRONTEND_PORT, BACKEND_URL, FRONTEND_URL

# Or import specific values
from config import NSURECAT_ENV_NAME, PROJECT_ROOT

# Display configuration
from config import show_config
show_config()
```

### 4. `config.js` (Frontend JavaScript)
Used by frontend code in the browser.

```javascript
// Include in HTML before your scripts
<script src="../../config.js"></script>

// Access in JavaScript
const API_URL = NsureCatConfig.API_BASE_URL;  // http://localhost:8000
const FRONTEND_PORT = NsureCatConfig.FRONTEND_PORT;  // 8001
```

## Configuration Values

### Current Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `NSURECAT_ENV_NAME` | `nsurecat` | Conda environment name |
| `PYTHON_VERSION` | `3.10` | Python version |
| `BACKEND_PORT` | `8000` | FastAPI backend port |
| `FRONTEND_PORT` | `8001` | Frontend server port |
| `BACKEND_URL` | `http://localhost:8000` | Backend full URL |
| `FRONTEND_URL` | `http://localhost:8001` | Frontend full URL |
| `API_BASE_URL` | `http://localhost:8000` | API base URL (same as backend) |

### Changing Configuration

**To change any port or environment name:**

1. Edit **only** the configuration files in the project root:
   - `config.sh`
   - `config.bat`
   - `config.py`
   - `config.js`

2. All scripts, tests, and code will automatically use the new values.

**Example: Change frontend port to 3000**

```bash
# In config.sh
export FRONTEND_PORT=3000

# In config.bat
set FRONTEND_PORT=3000

# In config.py
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))

# In config.js
FRONTEND_PORT: 3000,
```

That's it! No need to update dozens of files.

## Usage in Scripts

### Shell Scripts (utils/scripts/*.sh, utils/setup/*.sh)

```bash
#!/bin/bash

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source configuration
source "$PROJECT_ROOT/config.sh"

# Now use config variables
echo "Starting backend on port $BACKEND_PORT"
conda run -n "$NSURECAT_ENV_NAME" uvicorn main:app --port $BACKEND_PORT
```

### Python Tests (tests/*)

```python
import pytest
from config import FRONTEND_URL, BACKEND_URL

def test_frontend_loads(page):
    """Test uses config for URL"""
    page.goto(f"{FRONTEND_URL}/index.html")
    # ... test code
```

### Frontend JavaScript (src/frontend/*.js)

```javascript
// config.js is loaded in HTML, so use it:
const API_BASE_URL = NsureCatConfig.API_BASE_URL;

async function fetchData() {
    const response = await fetch(`${API_BASE_URL}/api/shop`);
    // ... rest of code
}
```

## Benefits

✅ **Single Source of Truth** - Change port once, applies everywhere  
✅ **No Port Mismatches** - Tests, scripts, and code always use same values  
✅ **Easy Environment Names** - Change `nsurecat` to `nsurecat-dev` in one place  
✅ **Clear Documentation** - Anyone can see current config with `./nsurecat.sh config`  
✅ **Cross-Platform** - Works on macOS, Linux, and Windows  

## Commands

### View Current Configuration

```bash
# From project root
./nsurecat.sh config

# Or directly
source config.sh && show_config

# Or in Python
python config.py
```

Output:
```
=== NsureCat Configuration ===
Environment: nsurecat
Python: 3.10
Backend: http://localhost:8000
Frontend: http://localhost:8001
Project Root: /Users/enkay/src/dev/nsurecat-genesis001
=============================
```

## Files Updated to Use Config

### Shell Scripts
- ✅ `utils/setup/setup_env.sh`
- ✅ `utils/setup/setup_deps.sh`
- ✅ `utils/scripts/start_servers.sh`
- ✅ `utils/scripts/run_tests.sh`
- ✅ `nsurecat.sh`

### Python Files
- ✅ `tests/conftest.py`
- ✅ `tests/frontend/test_chat_flow.py`

### JavaScript Files
- ✅ `src/frontend/chat.js`
- ✅ `src/frontend/index.html` (includes config.js)

## Troubleshooting

### "Command not found" or config not loading

Make sure scripts have execute permissions:
```bash
chmod +x config.sh
chmod +x nsurecat.sh
chmod +x utils/**/*.sh
```

### Config variables are empty

Check that you're sourcing the config file:
```bash
source config.sh
echo $BACKEND_PORT  # Should show 8000
```

### Tests still fail with wrong URL

Make sure `config.py` is in project root and importable:
```bash
# From project root
python -c "from config import FRONTEND_URL; print(FRONTEND_URL)"
# Should print: http://localhost:8001
```

## Best Practices

1. **Never hardcode ports or URLs** - Always use config variables
2. **Update config files together** - Keep all 4 files in sync
3. **Test after config changes** - Run `./nsurecat.sh test` to verify
4. **Document custom values** - If you change defaults, note why
5. **Use show_config()** - Display config at script start for debugging

---

**Last Updated**: November 2025  
**Version**: 1.0
