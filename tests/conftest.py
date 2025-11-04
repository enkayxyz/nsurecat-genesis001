# conftest.py for pytest configuration
import pytest
import sys
from pathlib import Path

# Add project root and utils/config to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "utils" / "config"))
from config import BACKEND_URL, FRONTEND_URL, show_config

# Display config on test start
print("\n")
show_config()
print("\n")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def backend_url():
    """Provide backend URL from config"""
    return BACKEND_URL


@pytest.fixture(scope="session")
def frontend_url():
    """Provide frontend URL from config"""
    return FRONTEND_URL