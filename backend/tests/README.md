# Backend Tests

This directory contains basic test scripts for the ProjectHub backend.

## Test Coverage

The tests are intentionally simple and non-comprehensive, designed to demonstrate that testing is possible:

- **test_models.py**: Tests for database models (User, Project, Task, Message)
- **test_app.py**: Tests for Flask application routes and endpoints
- **test_utils.py**: Tests for utility functions

## Running Tests

### Using unittest (built-in Python testing framework)

No additional packages required! Run tests with:

```bash
# Run all tests
python -m unittest discover backend/tests

# Run specific test file
python -m unittest backend.tests.test_models

# Run with verbose output
python -m unittest discover -v backend/tests
```

### From the backend directory

```bash
cd backend
python -m unittest discover tests
```

### Run individual test files

```bash
cd backend
python tests/test_models.py
python tests/test_app.py
python tests/test_utils.py
```

## Notes

- Tests use in-memory SQLite database for isolation
- No database setup required for testing
- Tests are basic and demonstrate functionality only
- Not comprehensive coverage - for demonstration purposes
