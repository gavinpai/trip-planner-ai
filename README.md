# Trip Planner AI

A Python script that uses Claude AI to recommend the best travel destinations based on your date range and preferences.

## Features

- 🗓️ **Date-based recommendations**: Get travel suggestions optimized for your specific travel dates
- 🌍 **Seasonal awareness**: Claude considers weather, seasonal activities, and events for each destination
- 🎯 **Personalized preferences**: Filter by budget, interests, regions, and climate preferences
- 🤖 **Powered by Claude**: Leverages Claude Sonnet 4.5 for intelligent, contextual recommendations

## Prerequisites

- Python 3.7 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd trip-planner-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API key
# Or export it directly:
export ANTHROPIC_API_KEY='your-api-key-here'
```

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

# Initialize with API key
planner = TripPlanner(api_key="your-api-key")

# Get recommendations
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

#### `__init__(api_key: str = None)`
Initialize the trip planner.
- **api_key**: Optional. Defaults to `ANTHROPIC_API_KEY` environment variable

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

## Project Structure

```
trip-planner-ai/
├── trip_planner.py      # Main script with TripPlanner class
├── example_usage.py     # Example usage script
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## How It Works

1. **Date Validation**: The script validates your input dates and calculates trip duration
2. **Seasonal Analysis**: It identifies the month and season of your travel dates
3. **Prompt Building**: Creates a detailed prompt for Claude including dates, duration, and preferences
4. **AI Processing**: Claude analyzes the information and generates personalized recommendations
5. **Results**: Returns detailed recommendations with explanations for each destination

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the GitHub repository.
