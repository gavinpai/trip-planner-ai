# Trip Planner AI

A Python script that uses Claude AI to recommend the best travel destinations based on your date range and preferences.

## Features

- 🗓️ **Date-based recommendations**: Get travel suggestions optimized for your specific travel dates
- 🌤️ **Real weather data**: Uses live weather forecasts from WeatherAPI to provide accurate weather information (optional)
- 🌍 **Seasonal awareness**: Claude considers weather, seasonal activities, and events for each destination
- 🎯 **Personalized preferences**: Filter by budget, interests, regions, and climate preferences
- 🤖 **Powered by Claude**: Leverages Claude Sonnet 4.5 for intelligent, contextual recommendations

## Prerequisites

- Python 3.7 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- Weather API key (Optional - [Get free key here](https://www.weatherapi.com/signup.aspx))

## Quick Start

### Automated Setup (Recommended)

```bash
# Clone and setup in one go
git clone <repository-url>
cd trip-planner-ai
./setup.sh
```

The setup script will install dependencies, run tests, and verify everything works.

### Manual Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd trip-planner-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
# Or export them directly:
export ANTHROPIC_API_KEY='your-api-key-here'

# Optional: Add weather API key for real weather data
export WEATHER_API_KEY='your-weather-api-key-here'
```

**Note**: The weather API key is optional. If not provided, the app will still work but will rely on Claude's knowledge for weather information instead of real-time data.

## Usage

### Interactive Mode

Run the script interactively to get travel recommendations:

```bash
python trip_planner.py
```

You'll be prompted to enter:
- Start date (YYYY-MM-DD)
- End date (YYYY-MM-DD)
- Optional preferences:
  - Budget (low/medium/high)
  - Interests (e.g., culture, nature, adventure, food)
  - Preferred region (e.g., Europe, Asia, Americas)
  - Preferred climate (warm/cold/moderate)

### Example Session

```
============================================================
Trip Planner AI - Powered by Claude
============================================================

Enter your travel dates:
Start date (YYYY-MM-DD): 2025-07-15
End date (YYYY-MM-DD): 2025-07-25

Optional preferences (press Enter to skip):
Budget (low/medium/high): medium
Interests (comma-separated, e.g., culture,nature,adventure): culture, food, beaches
Preferred region (e.g., Europe, Asia, Americas): Europe
Preferred climate (warm/cold/moderate): warm

============================================================
Analyzing your travel dates and generating recommendations...
============================================================

[Claude's personalized travel recommendations will appear here]
```

### Programmatic Use

You can also import and use the `TripPlanner` class in your own Python scripts:

```python
from trip_planner import TripPlanner

# Initialize with API keys (weather API key is optional)
planner = TripPlanner(
    api_key="your-api-key",
    weather_api_key="your-weather-api-key"  # Optional
)

# Get recommendations (with real weather data if weather_api_key is provided)
recommendations = planner.get_travel_recommendations(
    start_date="2025-07-15",
    end_date="2025-07-25",
    preferences={
        "budget": "medium",
        "interests": ["culture", "food", "beaches"],
        "region": "Europe",
        "climate": "warm"
    }
)

print(recommendations)
```

See `example_usage.py` for more examples.

## API Reference

### TripPlanner Class

#### `__init__(api_key: str = None, weather_api_key: str = None)`
Initialize the trip planner.
- **api_key**: Optional. Anthropic API key. Defaults to `ANTHROPIC_API_KEY` environment variable
- **weather_api_key**: Optional. Weather API key for real weather data. Defaults to `WEATHER_API_KEY` environment variable. If not provided, recommendations will be based on Claude's knowledge.

#### `get_travel_recommendations(start_date: str, end_date: str, preferences: dict = None) -> str`
Get travel recommendations from Claude.

**Parameters:**
- **start_date**: Trip start date in YYYY-MM-DD format
- **end_date**: Trip end date in YYYY-MM-DD format
- **preferences**: Optional dictionary with:
  - `budget`: "low", "medium", or "high"
  - `interests`: List of interests (e.g., ["culture", "nature", "adventure"])
  - `region`: Preferred region (e.g., "Europe", "Asia", "Americas")
  - `climate`: Preferred climate ("warm", "cold", "moderate")

**Returns:**
- String with detailed travel recommendations

**Raises:**
- `ValueError`: If dates are invalid or end date is before start date
- `Exception`: If there's an error calling the Claude API

## Testing

The project includes a comprehensive test suite with 95%+ code coverage.

### Running Tests

```bash
# Install dependencies including test tools
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=trip_planner --cov-report=term-missing

# Or use make commands
make test
make test-coverage
```

### Test Coverage

The test suite includes:
- Unit tests for all core functionality
- Integration tests with mocked API calls
- Edge case and boundary condition tests
- Input validation tests
- Error handling tests

See [TESTING.md](TESTING.md) for detailed testing documentation.

## Project Structure

```
trip-planner-ai/
├── .claude/
│   ├── claude.md           # Session guide for Claude Code
│   └── QUICKREF.md         # Quick reference card
├── trip_planner.py         # Main script with TripPlanner class
├── test_trip_planner.py    # Comprehensive test suite
├── example_usage.py        # Example usage script
├── setup.sh                # Automated setup script
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── Makefile                # Test runner shortcuts
├── TESTING.md              # Testing documentation
├── BUGFIXES.md             # Bug fix documentation
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## How It Works

1. **Date Validation**: The script validates your input dates and calculates trip duration
2. **Seasonal Analysis**: It identifies the month and season of your travel dates
3. **Weather Data Fetching** (Optional): If a weather API key is provided, fetches real-time weather forecasts for popular destinations
4. **Prompt Building**: Creates a detailed prompt for Claude including dates, duration, preferences, and real weather data
5. **AI Processing**: Claude analyzes the information and generates personalized recommendations based on actual weather conditions
6. **Results**: Returns detailed recommendations with explanations for each destination

### Weather Integration Details

When a weather API key is provided:
- For trips within the next 14 days: Fetches accurate weather forecasts
- For trips beyond 14 days: Uses current weather as a reference point
- Supports region-specific weather data (when region preference is specified)
- Covers major destinations across Europe, Asia, Americas, Africa, Oceania, and Middle East
- Gracefully falls back to Claude's knowledge if weather API is unavailable

## Developer Documentation

### For Claude Code Sessions

When working on this project in Claude Code, see:
- **[.claude/claude.md](.claude/claude.md)** - Complete session guide with environment setup, common issues, and solutions
- **[.claude/QUICKREF.md](.claude/QUICKREF.md)** - Quick reference card for common commands

**Important**: Always use `python3 -m pytest` instead of `pytest` when running tests in this environment.

### Documentation Files

- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
- **[BUGFIXES.md](BUGFIXES.md)** - Documentation of bugs found and fixed
- **[requirements.txt](requirements.txt)** - All dependencies with versions

### Development Workflow

1. Run setup: `./setup.sh`
2. Make changes to code
3. Run tests: `python3 -m pytest -v`
4. Check coverage: `python3 -m pytest --cov=trip_planner --cov-report=term-missing`
5. Commit changes with descriptive message
6. Push to feature branch

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the GitHub repository.
