# Testing Quick Start Guide

Get up and running with ProjectHub tests in minutes!

## Quick Setup

### Backend Tests

⚠️ **IMPORTANT:** The application uses old package versions that require **Python 3.7 or 3.8**  
They will NOT work with Python 3.9+ or 3.13.

**With Python 3.8 (Recommended):**

```powershell
# Windows - Create Python 3.8 virtual environment
py -3.8 -m venv venv38
.\venv38\Scripts\Activate.ps1

# Navigate to backend and install
cd backend
pip install -r requirements-test.txt

# Run tests
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

> **Note:** See `backend/PYTHON-COMPATIBILITY.md` for detailed Python version information and upgrade options.

### Frontend Tests

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Run tests
npm test -- --watchAll=false
```

## Run All Tests (One Command)

### Linux/macOS

```bash
# Make script executable (first time only)
chmod +x run-tests.sh

# Run all tests
./run-tests.sh
```

### Windows (PowerShell)

```powershell
# Run all tests
.\run-tests.ps1
```

## Generate Coverage Reports

### Linux/macOS

```bash
chmod +x run-tests-coverage.sh
./run-tests-coverage.sh
```

Then open:
- Backend: `backend/htmlcov/index.html`
- Frontend: `frontend/coverage/lcov-report/index.html`

### Windows (PowerShell)

```powershell
# Backend coverage
cd backend
pytest --cov=. --cov-report=html
# Open: backend\htmlcov\index.html

# Frontend coverage
cd ..\frontend
npm run test:coverage
# Open: frontend\coverage\lcov-report\index.html
```

## What's Being Tested?

### Backend (Python/Flask)
✅ **Models** - User, Project, Task, Message, Document  
✅ **Authentication** - JWT tokens, login, permissions  
✅ **API Routes** - Projects, Tasks, Documents  
✅ **Utilities** - Date formatting, file handling, logging  

**Test Files:**
- `backend/tests/test_models.py`
- `backend/tests/test_auth.py`
- `backend/tests/test_routes_projects.py`
- `backend/tests/test_routes_tasks.py`
- `backend/tests/test_utils.py`

### Frontend (React)
✅ **Components** - Dashboard, Login, TaskList, ProjectDetail  
✅ **API Service** - HTTP requests, token management  
✅ **User Interactions** - Clicks, form submissions, navigation  
✅ **Error Handling** - API errors, loading states  

**Test Files:**
- `frontend/src/components/__tests__/Dashboard.test.js`
- `frontend/src/components/__tests__/Login.test.js`
- `frontend/src/components/__tests__/TaskList.test.js`
- `frontend/src/components/__tests__/ProjectDetail.test.js`
- `frontend/src/services/__tests__/api.test.js`

## Common Commands

### Backend

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=. --cov-report=term

# Run in verbose mode
pytest -v

# Run specific test
pytest tests/test_models.py::TestUserModel::test_create_user
```

### Frontend

```bash
# Run tests (watch mode)
npm test

# Run tests once
npm test -- --watchAll=false

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- Dashboard.test.js

# Update snapshots
npm test -- -u
```

## Troubleshooting

### Backend: "ModuleNotFoundError"
```bash
cd backend
pip install -r requirements-test.txt
```

### Backend: "No module named 'pytest'"
```bash
pip install pytest pytest-cov pytest-flask
```

### Frontend: "Cannot find module"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Frontend: Tests timeout
Increase timeout in test:
```javascript
jest.setTimeout(10000); // 10 seconds
```

## Next Steps

- Read the full [Testing Guide](TESTING.md)
- Check out [Backend Test README](backend/tests/README.md)
- Check out [Frontend Test README](frontend/src/components/__tests__/README.md)

## Test Statistics

### Backend
- **Test Files**: 5
- **Test Classes**: ~15
- **Test Functions**: ~50+
- **Coverage Goal**: >80%

### Frontend
- **Test Files**: 5
- **Test Suites**: 5
- **Test Cases**: ~40+
- **Coverage Goal**: >70%

## Need Help?

1. Check the full [TESTING.md](TESTING.md) documentation
2. Review example tests in the test directories
3. Consult the official documentation:
   - [pytest docs](https://docs.pytest.org/)
   - [React Testing Library](https://testing-library.com/react)

---

**Happy Testing! 🧪**

