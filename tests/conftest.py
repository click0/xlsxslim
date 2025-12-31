"""Pytest configuration for xlsxslim tests."""

import sys
import shutil
from pathlib import Path

import pytest


# Add parent directory to sys.path so we can import xlsxslim
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Local tmp directory (in tests folder)
LOCAL_TMP_DIR = Path(__file__).parent / "tmp"


def pytest_addoption(parser):
    """Add custom pytest options."""
    parser.addoption(
        "--use-system-temp",
        action="store_true",
        default=False,
        help="Use system temp directory instead of local ./tests/tmp",
    )


@pytest.fixture(scope="function")
def tmp_dir(request, tmp_path):
    """
    Provide temporary directory for tests.
    
    By default uses ./tests/tmp directory.
    With --use-system-temp flag uses system temp directory.
    """
    use_system_temp = request.config.getoption("--use-system-temp", default=False)
    
    if use_system_temp:
        # Use pytest's built-in tmp_path (system temp)
        yield tmp_path
    else:
        # Use local ./tests/tmp directory
        LOCAL_TMP_DIR.mkdir(exist_ok=True)
        
        # Create unique subdirectory for this test
        test_name = request.node.name
        test_tmp = LOCAL_TMP_DIR / test_name
        if test_tmp.exists():
            shutil.rmtree(test_tmp, ignore_errors=True)
        test_tmp.mkdir(exist_ok=True)
        
        yield test_tmp
        
        # Cleanup after test
        try:
            shutil.rmtree(test_tmp, ignore_errors=True)
        except Exception:
            pass  # Ignore cleanup errors on Windows


@pytest.fixture(scope="session", autouse=True)
def cleanup_local_tmp():
    """Clean up local tmp directory after all tests."""
    yield
    # After all tests complete
    if LOCAL_TMP_DIR.exists():
        try:
            shutil.rmtree(LOCAL_TMP_DIR, ignore_errors=True)
        except Exception:
            pass
