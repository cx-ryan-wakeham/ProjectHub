# Python Version Compatibility

## Current Application Dependencies

The ProjectHub application uses **legacy package versions** that are **NOT compatible with Python 3.13**:

- Flask 1.1.4
- Flask-SQLAlchemy 2.3.2
- Werkzeug 1.0.1
- Jinja2 2.11.3
- And others...

## ⚠️ Python Version Requirement

**These packages require Python 3.7 or 3.8**

They will **NOT work** with Python 3.9+ due to:
- `time.clock` removal (Python 3.8+)
- MarkupSafe/Jinja2 incompatibilities
- Other deprecations and breaking changes

## Options

### Option 1: Use Python 3.8 for Testing (Recommended for now)

Install Python 3.8 alongside your current Python installation:

**Windows:**
1. Download Python 3.8.10 from [python.org](https://www.python.org/downloads/release/python-3810/)
2. Install it (check "Add to PATH")
3. Use `py -3.8` to run Python 3.8 specifically

**Using Python 3.8 for tests:**
```powershell
# Create virtual environment with Python 3.8
py -3.8 -m venv venv38

# Activate it
.\venv38\Scripts\Activate.ps1

# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest -v
```

**Linux/macOS:**
```bash
# Install Python 3.8 using pyenv or your package manager
pyenv install 3.8.10
pyenv local 3.8.10

# Create virtual environment
python3.8 -m venv venv38
source venv38/bin/activate

# Install and test
pip install -r requirements-test.txt
pytest -v
```

### Option 2: Upgrade Application to Modern Versions

Update `requirements.txt` to use modern, Python 3.13-compatible versions:

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
SQLAlchemy==2.0.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.0
PyJWT==2.8.0
Werkzeug==2.3.0
python-dotenv==1.0.0
```

**Pros:**
- Works with Python 3.13
- Security updates
- Better performance
- Active support

**Cons:**
- Requires code changes (breaking changes in Flask 2.x, SQLAlchemy 2.x)
- Testing needed
- Migration effort

## Current Test Setup

The `requirements-test.txt` file uses the **same old versions** as production, meaning:

✅ Tests match production environment exactly  
❌ Requires Python 3.7 or 3.8 to run

## Recommendation

**For immediate testing:**
- Use Python 3.8 in a virtual environment

**For long-term:**
- Plan to upgrade the entire application to modern package versions
- Update code for compatibility
- Test thoroughly
- Update to Python 3.11 or 3.12 (3.13 is very new)

## Quick Start with Python 3.8

```powershell
# Windows - Create Python 3.8 virtual environment
py -3.8 -m venv venv38
.\venv38\Scripts\Activate.ps1
cd backend
pip install -r requirements-test.txt
pytest -v
```

```bash
# Linux/macOS
python3.8 -m venv venv38
source venv38/bin/activate
cd backend
pip install -r requirements-test.txt
pytest -v
```

## Checking Python Version

```bash
# Check which Python versions are installed
py --list        # Windows
pyenv versions   # Linux/macOS with pyenv

# Check current Python version
python --version
```

