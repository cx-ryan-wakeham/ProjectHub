# Testing Guide for ProjectHub

This document provides information about running tests for the ProjectHub application.

## Overview

The ProjectHub application includes basic test scripts for both backend and frontend components. These tests are intentionally simple and non-comprehensive, designed to demonstrate that testing is possible without worrying about full coverage.

## Backend Tests (Python/Flask)

### Test Files

Located in `backend/tests/`:
- `test_models.py` - Tests for database models (User, Project, Task, Message) - 6 tests
- `test_app.py` - Tests for Flask application configuration and route imports - 6 tests
- `test_utils.py` - Tests for utility functions (datetime, string operations) - 5 tests

**Total Backend Tests: 17 tests**

### Running Backend Tests

The backend tests use Python's built-in `unittest` framework, so no additional packages are required.

#### Option 1: Using the test runner script

```bash
cd backend
python run_tests.py
```

#### Option 2: Using unittest discovery

```bash
# From project root
python -m unittest discover backend/tests

# From backend directory
cd backend
python -m unittest discover tests
```

#### Option 3: Run individual test files

```bash
cd backend
python tests/test_models.py
python tests/test_app.py
python tests/test_utils.py
```

#### Verbose output

```bash
python -m unittest discover -v backend/tests
```

## Frontend Tests (React/Jest)

### Test Files

Located in `frontend/src/`:
- `components/__tests__/Login.test.js` - Tests for Login component - 4 tests
- `components/__tests__/Dashboard.test.js` - Tests for Dashboard component - 3 tests
- `components/__tests__/TaskList.test.js` - Tests for TaskList component - 3 tests
- `services/__tests__/api.test.js` - Tests for API service - 4 tests

**Total Frontend Tests: 14 tests**

### Running Frontend Tests

The frontend tests use Jest and React Testing Library, which are included with `react-scripts`.

#### Run all tests

```bash
cd frontend
npm test
```

This will run tests in interactive watch mode.

#### Run tests once (non-interactive)

```bash
cd frontend
npm test -- --watchAll=false
```

#### Run with coverage report

```bash
cd frontend
npm test -- --coverage --watchAll=false
```

#### Run specific test file

```bash
cd frontend
npm test Login.test.js
```

## Test Philosophy

These tests are designed to be:
- **Simple**: Easy to understand and maintain
- **Basic**: Cover fundamental functionality only
- **Non-comprehensive**: Not aiming for full coverage
- **Demonstrative**: Show that testing infrastructure works

## Notes

- Backend tests use in-memory SQLite database for isolation
- Frontend tests mock external dependencies (router, localStorage, etc.)
- Some warnings may appear during test runs - this is expected for basic testing
- Tests are meant to serve as examples and starting points for more comprehensive testing

## Continuous Integration

While not set up in this demo, these tests can easily be integrated into CI/CD pipelines:

```bash
# Backend
python -m unittest discover backend/tests

# Frontend
cd frontend && npm test -- --watchAll=false
```

## Adding New Tests

### Backend (Python)

Create new test files in `backend/tests/` following the pattern `test_*.py`:

```python
import unittest

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)
```

### Frontend (React)

Create new test files in component directories following the pattern `*.test.js`:

```javascript
import { render } from '@testing-library/react';
import MyComponent from '../MyComponent';

test('renders without crashing', () => {
  const { container } = render(<MyComponent />);
  expect(container).toBeTruthy();
});
```
