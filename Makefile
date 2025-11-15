.PHONY: help install test test-verbose test-coverage clean lint

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make clean         - Clean up generated files"
	@echo "  make lint          - Run code linting (if configured)"

install:
	pip install -r requirements.txt

test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=trip_planner --cov-report=term-missing --cov-report=html

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

lint:
	@echo "Install flake8 or pylint for linting support"
	@echo "Example: pip install flake8"
	@echo "Then run: flake8 trip_planner.py"
