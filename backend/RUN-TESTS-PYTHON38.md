# Running Tests with Python 3.8

## Why Python 3.8?

The ProjectHub application uses legacy package versions (Flask 1.1.4, Jinja2 2.11.3, etc.) that are **not compatible with Python 3.9+**.

These packages require **Python 3.7 or 3.8** to work correctly.

## Installing Python 3.8

### Windows

1. **Download Python 3.8.10:**
   - Go to https://www.python.org/downloads/release/python-3810/
   - Download "Windows installer (64-bit)"

2. **Install:**
   - Run the installer
   - ✅ Check "Add Python 3.8 to PATH"
   - Click "Install Now"

3. **Verify:**
   ```powershell
   py -3.8 --version
   # Should show: Python 3.8.10
   ```

### Linux (Ubuntu/Debian)

```bash
# Add deadsnakes PPA (if not already added)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.8
sudo apt install python3.8 python3.8-venv python3.8-dev

# Verify
python3.8 --version
```

### macOS

```bash
# Using Homebrew
brew install python@3.8

# Or using pyenv (recommended)
brew install pyenv
pyenv install 3.8.10
pyenv local 3.8.10

# Verify
python3.8 --version
```

## Running Tests with Python 3.8

### Option 1: Virtual Environment (Recommended)

**Windows:**
```powershell
# Create virtual environment with Python 3.8
py -3.8 -m venv venv38

# Activate
.\venv38\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements-test.txt

# Run tests
pytest -v

# Deactivate when done
deactivate
```

**Linux/macOS:**
```bash
# Create virtual environment
python3.8 -m venv venv38

# Activate
source venv38/bin/activate

# Install dependencies
cd backend
pip install -r requirements-test.txt

# Run tests
pytest -v

# Deactivate when done
deactivate
```

### Option 2: Direct Python 3.8 Command

**Windows:**
```powershell
cd backend

# Install to user directory
py -3.8 -m pip install --user -r requirements-test.txt

# Run tests
py -3.8 -m pytest -v
```

**Linux/macOS:**
```bash
cd backend

# Install to user directory
python3.8 -m pip install --user -r requirements-test.txt

# Run tests
python3.8 -m pytest -v
```

## Checking Your Python Versions

### Windows
```powershell
# List all installed Python versions
py --list

# Example output:
# -3.13-64 *
# -3.8-64
# -3.7-64
```

### Linux/macOS
```bash
# Check available Python versions
ls /usr/bin/python*

# Or with pyenv
pyenv versions
```

## Common Issues

### "py: No such file or directory" (Windows)

**Solution:** Add Python Launcher to PATH or use full path:
```powershell
C:\Users\YourName\AppData\Local\Programs\Python\Python38\python.exe
```

### "python3.8: command not found" (Linux/macOS)

**Solution:** Install Python 3.8:
```bash
# Ubuntu/Debian
sudo apt install python3.8

# macOS
brew install python@3.8
```

### Tests fail with import errors

**Solution:** Make sure you're in the virtual environment:
```bash
# Check Python version being used
python --version

# Should show Python 3.8.x
```

## Verifying Setup

Run this to verify everything is set up correctly:

```bash
cd backend
pytest tests/test_python_version.py -v
```

This test checks:
- ✅ Python version is 3.7 or 3.8
- ✅ Flask version is 1.1.x
- ✅ SQLAlchemy version is 1.4.x

## Next Steps

Once Python 3.8 is working:

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

## Future: Upgrading to Modern Versions

To avoid Python version constraints, consider upgrading the application:

1. Update `requirements.txt` to modern versions (Flask 2.x, SQLAlchemy 2.x)
2. Fix breaking changes in code
3. Test thoroughly
4. Use Python 3.11 or 3.12

See `PYTHON-COMPATIBILITY.md` for more details.

