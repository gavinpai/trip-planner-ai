#!/bin/bash
# Setup script for Trip Planner AI development environment

set -e  # Exit on error

echo "=========================================="
echo "Trip Planner AI - Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "Note: You may see warnings about running as root - these can be ignored"
echo ""
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Verify installations
echo "Verifying installations..."
python3 -c "import anthropic; print('✓ anthropic installed')"
python3 -c "import pytest; print('✓ pytest installed')"
python3 -c "import pytest_cov; print('✓ pytest-cov installed')"
python3 -c "import pytest_mock; print('✓ pytest-mock installed')"
echo ""

# Run tests to verify setup
echo "Running test suite to verify setup..."
python3 -m pytest -v --tb=short
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠ Warning: .env file not found"
    echo "  Copy .env.example to .env and add your ANTHROPIC_API_KEY"
    echo "  Run: cp .env.example .env"
    echo ""
fi

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  1. Set your API key: export ANTHROPIC_API_KEY='your-key'"
echo "  2. Run the app: python3 trip_planner.py"
echo "  3. Run tests: python3 -m pytest -v"
echo ""
echo "See .claude/claude.md for detailed documentation"
