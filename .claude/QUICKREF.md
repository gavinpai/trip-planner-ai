# Quick Reference Card

## Critical Commands

```bash
# ⚠️ ALWAYS use python3 -m pytest (NOT just pytest)
python3 -m pytest -v

# Run with coverage
python3 -m pytest --cov=trip_planner --cov-report=term-missing
```

## Setup

```bash
# First time setup
./setup.sh

# Or manually
pip install -r requirements.txt
python3 -m pytest -v
```

## Git Branch

```bash
# Always work on this branch
claude/travel-recommendations-api-01BRncuaM6ktWvyNoHhV9EmS

# Push changes
git add .
git commit -m "Description"
git push -u origin claude/travel-recommendations-api-01BRncuaM6ktWvyNoHhV9EmS
```

## Test Commands

```bash
# All tests
python3 -m pytest -v

# Specific test file
python3 -m pytest test_trip_planner.py -v

# Specific test
python3 -m pytest test_trip_planner.py::TestDateValidation::test_valid_date -v

# With coverage
python3 -m pytest --cov=trip_planner --cov-report=term-missing
```

## Run Application

```bash
export ANTHROPIC_API_KEY='your-key'
python3 trip_planner.py
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: anthropic` | Use `python3 -m pytest` not `pytest` |
| `pytest: error: unrecognized arguments: --cov` | `pip install pytest-cov` |
| Tests fail | Ensure dependencies installed: `pip install -r requirements.txt` |

## File Structure

- `trip_planner.py` - Main code
- `test_trip_planner.py` - Tests (39 tests)
- `.claude/claude.md` - Full documentation
- `TESTING.md` - Testing guide
- `BUGFIXES.md` - Bug fixes

## Test Stats

- 39 tests, 100% passing
- 60% overall coverage
- 95%+ core class coverage
