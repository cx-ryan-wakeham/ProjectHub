"""
Test to verify Python version compatibility
"""
import sys
import pytest


def test_python_version_compatibility():
    """Verify tests are running on compatible Python version"""
    major = sys.version_info.major
    minor = sys.version_info.minor
    
    # These old package versions require Python 3.7 or 3.8
    assert major == 3, f"Python {major}.x is not supported. Requires Python 3.7 or 3.8"
    
    if minor >= 9:
        pytest.fail(
            f"Python 3.{minor} is not compatible with the old package versions used in this project.\n"
            f"Current Python: {sys.version}\n"
            f"Required: Python 3.7 or 3.8\n"
            f"See backend/PYTHON-COMPATIBILITY.md for more information."
        )
    
    # Warn if using Python < 3.7
    if minor < 7:
        pytest.skip(f"Python 3.{minor} is too old. Requires Python 3.7 or 3.8")


def test_package_versions():
    """Verify key packages are the expected old versions"""
    import flask
    import sqlalchemy
    
    # Check Flask version
    assert flask.__version__.startswith('1.1'), \
        f"Expected Flask 1.1.x, got {flask.__version__}"
    
    # Check SQLAlchemy version  
    assert sqlalchemy.__version__.startswith('1.4'), \
        f"Expected SQLAlchemy 1.4.x, got {sqlalchemy.__version__}"
    
    print(f"✓ Flask {flask.__version__}")
    print(f"✓ SQLAlchemy {sqlalchemy.__version__}")
    print(f"✓ Python {sys.version}")

