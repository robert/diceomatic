# Tests for SumChef

This directory contains unit tests for the SumChef library.

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_core.py
```

To run a specific test:

```bash
pytest tests/test_core.py::test_variable_creation
```

## Test Files

- `test_core.py`: Basic tests for core functionality (variables, operations, constraints)
- `test_solver.py`: Tests for constraint solving capabilities with more complex scenarios
- `conftest.py`: Common fixtures shared across test files

## Writing Tests

When adding new tests, consider:

1. Using the fixtures provided in `conftest.py`
2. Following the pattern of arranging tests into logical groups
3. Adding clear docstrings to describe what each test is verifying
4. Making sure each test is independent and doesn't rely on state from other tests