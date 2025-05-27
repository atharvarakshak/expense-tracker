# Test Suite for Expense Tracker

This directory contains the test suite for the expense tracker application.

## Test Files

- `test_home_route.py` - Tests for the home page route ("/")
- `conftest.py` - Test configuration and utility functions
- `__init__.py` - Package initialization

## Running Tests

### Option 1: Using the test runner script (Recommended)

```bash
# Run all tests
python run_tests.py

# Run only home route tests
python run_tests.py home
```

### Option 2: Using unittest directly

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_home_route -v
```

### Option 3: Using pytest (if installed)

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_home_route.py -v
```

## Test Coverage

### Home Route Tests (`test_home_route.py`)

The home route tests cover the following scenarios:

1. **Unauthenticated Access** - Verifies that users without authentication are redirected to the login page
2. **Authenticated Access** - Verifies that authenticated users can access the home page successfully
3. **User Data Display** - Verifies that the home page displays correct user information
4. **Invalid Session Handling** - Verifies that users with invalid sessions are redirected appropriately
5. **Template Rendering** - Verifies that the correct template is rendered with proper HTML content

### Test Data

Each test creates:
- A test user with sample credentials
- Sample income and expense statements
- Proper session management for authentication testing

### Database

Tests use a temporary SQLite database that is created and destroyed for each test run, ensuring test isolation.

## Adding New Tests

When adding new tests:

1. Create test files with the naming pattern `test_*.py`
2. Import necessary modules from the app
3. Use the `HomeRouteTestCase` class as a reference for setup and teardown
4. Follow the existing patterns for authentication and database setup
5. Add descriptive docstrings for each test method

## Notes

- Tests automatically handle database creation and cleanup
- Session management is handled through Flask's test client
- The test suite uses temporary files to avoid conflicts with the main application database
- All tests should be independent and not rely on the state from other tests
