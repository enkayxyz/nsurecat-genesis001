"""
NsureCat Configuration
Python configuration module - import this in Python scripts and tests
"""
import os
from pathlib import Path

# Environment
NSURECAT_ENV_NAME = os.getenv("NSURECAT_ENV_NAME", "nsurecat")
PYTHON_VERSION = os.getenv("PYTHON_VERSION", "3.10")

# Ports
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8001"))

# URLs
BACKEND_URL = os.getenv("BACKEND_URL", f"http://localhost:{BACKEND_PORT}")
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:{FRONTEND_PORT}")
API_BASE_URL = os.getenv("API_BASE_URL", BACKEND_URL)

# Directories (config.py is in utils/config, so go up two levels to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "src" / "backend"
FRONTEND_DIR = PROJECT_ROOT / "src" / "frontend"
TESTS_DIR = PROJECT_ROOT / "tests"

# Testing
TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "30000"))
PYTEST_ARGS = os.getenv("PYTEST_ARGS", "-v --tb=short")

# Development
UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "--reload")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")


def show_config():
    """Display current configuration"""
    print("=== NsureCat Configuration ===")
    print(f"Environment: {NSURECAT_ENV_NAME}")
    print(f"Python: {PYTHON_VERSION}")
    print(f"Backend: {BACKEND_URL}")
    print(f"Frontend: {FRONTEND_URL}")
    print(f"Project Root: {PROJECT_ROOT}")
    print("=============================")


def get_config_dict():
    """Return configuration as dictionary"""
    return {
        "env_name": NSURECAT_ENV_NAME,
        "python_version": PYTHON_VERSION,
        "backend_port": BACKEND_PORT,
        "frontend_port": FRONTEND_PORT,
        "backend_url": BACKEND_URL,
        "frontend_url": FRONTEND_URL,
        "api_base_url": API_BASE_URL,
        "project_root": str(PROJECT_ROOT),
        "backend_dir": str(BACKEND_DIR),
        "frontend_dir": str(FRONTEND_DIR),
        "tests_dir": str(TESTS_DIR),
        "test_timeout": TEST_TIMEOUT,
    }


if __name__ == "__main__":
    show_config()
