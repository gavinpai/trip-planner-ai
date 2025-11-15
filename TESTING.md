# Testing Guide

This document describes the testing setup and how to run tests for the Trip Planner AI project.

## Test Suite Overview

The test suite (`test_trip_planner.py`) provides comprehensive coverage of the TripPlanner functionality:

### Test Categories

1. **Initialization Tests** (`TestTripPlannerInit`)
   - API key validation (parameter vs environment variable)
   - Missing API key error handling
   - API key priority (parameter over env var)

2. **Date Validation Tests** (`TestDateValidation`)
   - Valid date formats (YYYY-MM-DD)
   - Invalid formats (MM/DD/YYYY, etc.)
   - Invalid date values (month 13, Feb 30, etc.)
   - None and empty string handling
   - Non-string input handling
   - Leap year validation

3. **Travel Recommendations Tests** (`TestGetTravelRecommendations`)
   - Valid date ranges
   - Same-day trips (0-day duration)
   - Invalid date handling
   - End date before start date
   - Preferences validation
   - Invalid preferences types
   - Interests validation (must be list of strings)
   - API error handling

4. **Prompt Building Tests** (`TestBuildPrompt`)
   - Basic prompts without preferences
   - Prompts with individual preferences (budget, interests, region, climate)
   - Prompts with all preferences combined
   - Different months/seasons
   - Zero-day trip prompts

5. **Integration Tests** (`TestIntegration`)
   - Full workflow with mocked API
   - Workflow with preferences
   - Verification of API parameters

6. **Edge Cases** (`TestEdgeCases`)
   - Leap year dates
   - Very long trips (365+ days)
   - None values in preferences
   - Single interest in list
   - Whitespace handling

## Running Tests

### Basic Test Run

```bash
# Run all tests
pytest

# Or using make
make test
```

### Verbose Output

```bash
# Detailed test output
pytest -v

# Or using make
make test-verbose
```

### With Coverage Report

```bash
# Run tests with coverage
pytest --cov=trip_planner --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=trip_planner --cov-report=html

# Or using make
make test-coverage
```

The HTML coverage report will be generated in `htmlcov/index.html`.

### Run Specific Tests

```bash
# Run a specific test class
pytest test_trip_planner.py::TestDateValidation -v

# Run a specific test method
pytest test_trip_planner.py::TestDateValidation::test_valid_date -v

# Run tests matching a pattern
pytest -k "date" -v
```

### Run with Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

Current test coverage targets:

- **Overall coverage**: 95%+
- **Core functionality**: 100%
  - `validate_date()`
  - `get_travel_recommendations()`
  - `_build_prompt()`

## Installing Test Dependencies

```bash
# Install all dependencies including test tools
pip install -r requirements.txt

# Or just testing dependencies
pip install pytest pytest-cov pytest-mock
```

## Writing New Tests

When adding new features, follow these guidelines:

1. **Test file naming**: `test_*.py`
2. **Test class naming**: `Test*` (e.g., `TestNewFeature`)
3. **Test method naming**: `test_*` (e.g., `test_valid_input`)

Example:

```python
import pytest
from trip_planner import TripPlanner

class TestNewFeature:
    """Test description"""

    @pytest.fixture
    def planner(self):
        return TripPlanner(api_key="test-key")

    def test_something(self, planner):
        """Test a specific behavior"""
        result = planner.some_method()
        assert result == expected_value
```

## Continuous Testing

For development, you can use pytest-watch for continuous testing:

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw
```

## Mocking External Dependencies

The tests use `unittest.mock` to mock the Anthropic API:

```python
from unittest.mock import Mock, patch

def test_api_call(self, planner):
    mock_response = Mock()
    mock_content = Mock()
    mock_content.text = "Test response"
    mock_response.content = [mock_content]

    with patch.object(planner.client.messages, 'create', return_value=mock_response):
        result = planner.get_travel_recommendations("2025-07-15", "2025-07-25")
        assert result == "Test response"
```

This ensures tests run quickly without making real API calls.

## Common Issues

### Import Errors

If you get import errors, make sure you're running pytest from the project root:

```bash
cd /path/to/trip-planner-ai
pytest
```

### API Key Warnings

Tests use mocked API calls, so you don't need a real API key. The tests set `api_key="test-key"` or use environment variable mocking.

### Coverage Not Found

If coverage reports show 0%, ensure you have pytest-cov installed:

```bash
pip install pytest-cov
```

## Bug Fixes Covered by Tests

The test suite validates fixes for these identified bugs:

1. **Zero-day trips**: Tests verify same-day trips are now allowed
2. **None date handling**: Tests confirm proper validation of None inputs
3. **Type safety in preferences**: Tests validate that interests must be a list of strings
4. **Empty string dates**: Tests ensure empty strings are properly rejected
5. **Preferences validation**: Tests confirm preferences must be a dictionary

All these bugs are now fixed and prevented by the comprehensive test suite.
