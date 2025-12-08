# Frontend Tests

This directory contains basic test scripts for React components.

## Test Coverage

The tests are intentionally simple and non-comprehensive, designed to demonstrate that testing is possible:

- **Login.test.js**: Basic tests for the Login component
- **Dashboard.test.js**: Basic tests for the Dashboard component
- **TaskList.test.js**: Basic tests for the TaskList component
- **api.test.js**: Basic tests for the API service (in services/__tests__)

## Running Tests

### Run all tests

```bash
cd frontend
npm test
```

### Run tests in watch mode

```bash
npm test -- --watchAll
```

### Run tests with coverage

```bash
npm test -- --coverage --watchAll=false
```

### Run specific test file

```bash
npm test Login.test.js
```

## Notes

- Tests use Jest and React Testing Library (included with react-scripts)
- Tests are basic and demonstrate functionality only
- Not comprehensive coverage - for demonstration purposes
- Some tests may show warnings - this is expected for basic testing

