# Claude Code Session Guide - Trip Planner AI

This document contains essential information for working on this project in Claude Code sessions.

## Project Overview

Trip Planner AI - A Python application that uses the Claude API to recommend travel destinations based on date ranges and user preferences.

## Environment Setup

### Critical: Python Environment Issues

**IMPORTANT**: The system `pytest` command does NOT have access to installed Python packages. You MUST use `python3 -m pytest` instead.

```bash
# ❌ DON'T use this - will fail with import errors
pytest

# ✅ DO use this - works correctly
python3 -m pytest
```

### Installing Dependencies

On first setup or when dependencies are missing:

```bash
# Install all dependencies (core + testing)
pip install -r requirements.txt

# Or install individually if needed
pip install anthropic python-dotenv pytest pytest-cov pytest-mock
```

**Note**: You may see warnings about running pip as root - these are expected in this environment and can be ignored.

## Running Tests

### Basic Test Commands

```bash
# Run all tests (MUST use python3 -m)
python3 -m pytest

# Run with verbose output
python3 -m pytest -v

# Run with coverage report
python3 -m pytest --cov=trip_planner --cov-report=term-missing

# Run specific test file
python3 -m pytest test_trip_planner.py -v

# Run specific test class
python3 -m pytest test_trip_planner.py::TestDateValidation -v

# Run specific test method
python3 -m pytest test_trip_planner.py::TestDateValidation::test_valid_date -v
```

### Using Make Commands

The Makefile provides shortcuts, but note they internally use pytest (not python3 -m pytest), so ensure dependencies are properly accessible:

```bash
make test           # Run all tests
make test-verbose   # Run with verbose output
make test-coverage  # Run with coverage report
make clean          # Clean up test artifacts
```

## Project Structure

```
trip-planner-ai/
├── .claude/
│   └── claude.md           # This file - session guide
├── trip_planner.py         # Main application
├── test_trip_planner.py    # Test suite (39 tests)
├── example_usage.py        # Usage examples
├── requirements.txt        # Dependencies
├── pytest.ini              # Pytest configuration
├── Makefile                # Test shortcuts
├── TESTING.md              # Testing documentation
├── BUGFIXES.md             # Bug fix documentation
├── README.md               # User documentation
├── .env.example           # Environment variable template
└── .gitignore             # Git ignore rules
```

## Common Tasks

### Running the Application

```bash
# Set API key (required)
export ANTHROPIC_API_KEY='your-api-key-here'

# Run interactively
python3 trip_planner.py

# Run examples
python3 example_usage.py
```

### Testing Workflow

```bash
# 1. Make code changes
# 2. Run tests to verify
python3 -m pytest -v

# 3. Check coverage
python3 -m pytest --cov=trip_planner --cov-report=term-missing

# 4. If all pass, commit changes
git add .
git commit -m "Description of changes"
git push -u origin claude/travel-recommendations-api-01BRncuaM6ktWvyNoHhV9EmS
```

## Known Issues & Solutions

### Issue 1: ModuleNotFoundError when running pytest

**Symptom**:
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution**:
Use `python3 -m pytest` instead of `pytest`, or ensure dependencies are installed:
```bash
pip install anthropic python-dotenv pytest pytest-cov pytest-mock
python3 -m pytest
```

### Issue 2: pytest configuration errors about coverage

**Symptom**:
```
pytest: error: unrecognized arguments: --cov=trip_planner
```

**Solution**:
Install pytest-cov:
```bash
pip install pytest-cov
```

The pytest.ini file has been configured to work without coverage by default to avoid this issue.

### Issue 3: API key warnings in tests

**Note**: Tests use mocked API calls, so no real API key is needed for testing. The tests create mock API keys like "test-key".

## Test Suite Information

- **Total Tests**: 39
- **Test Categories**:
  - Initialization (4)
  - Date Validation (7)
  - Travel Recommendations (14)
  - Prompt Building (8)
  - Integration (2)
  - Edge Cases (5)
- **Coverage**: 60% overall, 95%+ for core TripPlanner class

## Git Branch

Always work on and push to:
```
claude/travel-recommendations-api-01BRncuaM6ktWvyNoHhV9EmS
```

## Quick Reference

```bash
# Environment check
python3 --version          # Should show Python 3.11+
which python3              # Verify Python location
pip list | grep anthropic  # Check if anthropic is installed

# Run full test suite
python3 -m pytest -v

# Run with coverage
python3 -m pytest --cov=trip_planner --cov-report=term-missing --cov-report=html

# View HTML coverage report
# Generated at: htmlcov/index.html

# Clean up
make clean
rm -rf __pycache__ .pytest_cache htmlcov .coverage
```

## Important Files to Review

Before making changes, review:
- `trip_planner.py` - Main application logic
- `test_trip_planner.py` - Test suite
- `BUGFIXES.md` - Known bugs and fixes
- `TESTING.md` - Detailed testing guide

## Code Quality Standards

### When Adding New Features

1. **Write tests first** or alongside the feature
2. **Ensure all tests pass**: `python3 -m pytest -v`
3. **Check coverage**: Aim for 90%+ on new code
4. **Validate inputs**: Add type checking and validation
5. **Document in docstrings**: Follow existing style
6. **Update TESTING.md** if adding new test categories

### Bug Fixes

See `BUGFIXES.md` for examples of bugs that were fixed. Common patterns:
- Validate None/null inputs
- Check types before operations
- Handle empty strings/lists
- Provide clear error messages
- Add tests for the bug before fixing

## Dependencies

### Core Dependencies
- `anthropic>=0.39.0` - Claude API client
- `python-dotenv>=1.0.0` - Environment variable management

### Testing Dependencies
- `pytest>=8.0.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `pytest-mock>=3.12.0` - Mocking utilities

## Troubleshooting Commands

```bash
# Check installed packages
pip list

# Verify imports work
python3 -c "from trip_planner import TripPlanner; print('OK')"

# Check if tests are discoverable
python3 -m pytest --collect-only

# Run tests with more debug info
python3 -m pytest -vv --tb=long

# Run a single test with full output
python3 -m pytest test_trip_planner.py::TestDateValidation::test_valid_date -vv -s
```

## Session Checklist

At the start of each session:
- [ ] Verify Python environment: `python3 --version`
- [ ] Check dependencies: `pip list | grep -E "anthropic|pytest"`
- [ ] Verify tests pass: `python3 -m pytest`
- [ ] Check current branch: `git branch --show-current`
- [ ] Pull latest changes: `git pull origin claude/travel-recommendations-api-01BRncuaM6ktWvyNoHhV9EmS`

## Additional Resources

- [TESTING.md](../TESTING.md) - Comprehensive testing guide
- [BUGFIXES.md](../BUGFIXES.md) - Bug fix documentation
- [README.md](../README.md) - User-facing documentation
- [Pytest Documentation](https://docs.pytest.org/)
- [Anthropic API Docs](https://docs.anthropic.com/)
