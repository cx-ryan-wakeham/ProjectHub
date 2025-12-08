# ProjectHub Testing - Quick Reference

This file provides a quick reference for running the test suite in the ProjectHub application.

## 📋 What Was Created

### Backend Tests (Python/unittest)
- ✅ 17 tests across 3 test files
- ✅ No additional packages required (uses built-in unittest)
- ✅ Tests for models, app configuration, and utilities

### Frontend Tests (JavaScript/Jest)
- ✅ 14 tests across 4 test files  
- ✅ Uses Jest (included with react-scripts)
- ✅ Tests for components and API service

## 🚀 Quick Start

### Run ALL Tests (Backend + Frontend)

```powershell
.\run_all_tests.ps1
```

### Run Backend Tests Only

```powershell
cd backend
python -m unittest discover -v tests
```

Or use the PowerShell script:

```powershell
cd backend
.\run_tests.ps1
```

### Run Frontend Tests Only

```powershell
cd frontend
npm test -- --watchAll=false
```

Or use the PowerShell script:

```powershell
cd frontend
.\run_tests.ps1
```

## 📁 Test File Locations

### Backend Tests
```
backend/tests/
├── __init__.py
├── test_models.py      (6 tests - User, Project, Task, Message models)
├── test_app.py         (6 tests - Configuration and route imports)
├── test_utils.py       (5 tests - Datetime and string utilities)
└── README.md
```

### Frontend Tests
```
frontend/src/
├── components/__tests__/
│   ├── Login.test.js       (4 tests - Login component)
│   ├── Dashboard.test.js   (3 tests - Dashboard component)
│   ├── TaskList.test.js    (3 tests - TaskList component)
│   └── README.md
├── services/__tests__/
│   └── api.test.js         (4 tests - API service)
└── setupTests.js           (Jest configuration)
```

## 📝 Test Runner Scripts

### PowerShell Scripts (Windows)
- `run_all_tests.ps1` - Run all tests (backend + frontend)
- `backend/run_tests.ps1` - Run backend tests only
- `frontend/run_tests.ps1` - Run frontend tests only
- `backend/tests/run_single_test.ps1` - Run a single backend test file

### Python Scripts
- `backend/run_tests.py` - Python test runner for backend

## 🔍 Running Individual Tests

### Backend - Run Single Test File

```powershell
cd backend
python tests/test_models.py
python tests/test_app.py
python tests/test_utils.py
```

### Frontend - Run Single Test File

```powershell
cd frontend
npm test Login.test.js
npm test Dashboard.test.js
npm test TaskList.test.js
npm test api.test.js
```

## ✅ Current Test Status

**Backend:** ✅ All 17 tests passing  
**Frontend:** ⚠️ Requires `npm install` in frontend directory if not already done

## 📚 Documentation Files

- **TESTING.md** - Comprehensive testing guide with detailed instructions
- **TEST_SUMMARY.md** - Detailed summary of all tests and coverage
- **README_TESTS.md** - This file (quick reference)
- **backend/tests/README.md** - Backend-specific test documentation
- **frontend/src/components/__tests__/README.md** - Frontend-specific test documentation

## 🎯 Test Philosophy

These tests are:
- **Simple** - Easy to understand and maintain
- **Basic** - Cover fundamental functionality only
- **Non-comprehensive** - Not aiming for full coverage
- **Demonstrative** - Show that testing infrastructure works

## 💡 Examples

### Example 1: Run all tests with detailed output

```powershell
# From project root
.\run_all_tests.ps1
```

### Example 2: Run backend tests with verbose output

```powershell
cd backend
python -m unittest discover -v tests
```

### Example 3: Run frontend tests with coverage

```powershell
cd frontend
npm test -- --coverage --watchAll=false
```

### Example 4: Run a specific backend test class

```powershell
cd backend
python -m unittest tests.test_models.TestUserModel
```

### Example 5: Run a specific backend test method

```powershell
cd backend
python -m unittest tests.test_models.TestUserModel.test_user_password_hashing
```

## ⚙️ No Package Upgrades

As requested, **no existing packages were upgraded**. The tests use:
- Backend: Python's built-in `unittest` framework (no additional dependencies)
- Frontend: Jest and React Testing Library (already included with react-scripts 3.0.1)

## 🔧 Troubleshooting

### Backend tests fail with import errors
- Make sure you're in the `backend` directory
- Check that Python can find the modules: `python -c "import models; print('OK')"`

### Frontend tests don't run
- Make sure dependencies are installed: `npm install` (in frontend directory)
- Check that node_modules exists: `ls node_modules` (should not be empty)

### PowerShell script won't run
- Enable script execution: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- Or run with: `powershell -ExecutionPolicy Bypass -File .\run_all_tests.ps1`

## 📞 Getting Help

For more detailed information:
- Read `TESTING.md` for comprehensive guide
- Read `TEST_SUMMARY.md` for detailed test coverage
- Check individual README files in test directories

---

**Created:** December 8, 2025  
**Purpose:** Demonstrate basic testing capability for ProjectHub application  
**Framework:** Python unittest (backend), Jest (frontend)

