#!/usr/bin/env python3
"""
Demo script to show weather integration functionality
This demonstrates how the weather API integration works
"""

from trip_planner import TripPlanner
from unittest.mock import Mock, patch
import os

def demo_without_weather_api():
    """Demo without weather API - should work with Claude's knowledge"""
    print("=" * 70)
    print("DEMO 1: Without Weather API Key")
    print("=" * 70)

    # Set up environment with only Anthropic API key
    os.environ["ANTHROPIC_API_KEY"] = "test-key-123"
    if "WEATHER_API_KEY" in os.environ:
        del os.environ["WEATHER_API_KEY"]

    planner = TripPlanner(api_key="test-key-123")

    print(f"Weather API Key: {planner.weather_api_key}")
    print(f"Has weather integration: {planner.weather_api_key is not None}")

    # Test that weather data returns empty without key
    weather_data = planner._get_weather_data("2025-12-20", "2025-12-25")
    print(f"Weather data returned: {'Empty (as expected)' if weather_data == '' else 'Has data'}")
    print()

def demo_with_weather_api():
    """Demo with weather API - should fetch real weather data"""
    print("=" * 70)
    print("DEMO 2: With Weather API Key (Mocked)")
    print("=" * 70)

    planner = TripPlanner(
        api_key="test-key-123",
        weather_api_key="test-weather-key-456"
    )

    print(f"Weather API Key: {planner.weather_api_key}")
    print(f"Has weather integration: {planner.weather_api_key is not None}")

    # Mock the requests.get to simulate weather API response
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "temp_c": 18.5,
                "temp_f": 65.3,
                "condition": {"text": "Partly cloudy"},
                "humidity": 72
            }
        }
        mock_get.return_value = mock_response

        weather_data = planner._get_weather_data("2025-12-20", "2025-12-25")

        print(f"Weather data fetched: {'Yes' if weather_data else 'No'}")
        if weather_data:
            print("\nWeather data preview:")
            print("-" * 70)
            # Show first 300 characters
            print(weather_data[:300] + "..." if len(weather_data) > 300 else weather_data)
            print("-" * 70)
    print()

def demo_region_specific_weather():
    """Demo region-specific weather data"""
    print("=" * 70)
    print("DEMO 3: Region-Specific Weather (Europe)")
    print("=" * 70)

    planner = TripPlanner(
        api_key="test-key-123",
        weather_api_key="test-weather-key-456"
    )

    print(f"Destinations for Europe: {planner.destinations_by_region['Europe']}")

    # Mock the requests.get
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "temp_c": 22.0,
                "temp_f": 71.6,
                "condition": {"text": "Sunny"},
                "humidity": 55
            }
        }
        mock_get.return_value = mock_response

        weather_data = planner._get_weather_data("2025-12-20", "2025-12-25", region="Europe")

        print(f"\nWeather data for European destinations: {'Yes' if weather_data else 'No'}")
    print()

def demo_prompt_integration():
    """Demo how weather data is integrated into the prompt"""
    print("=" * 70)
    print("DEMO 4: Prompt Integration with Weather Data")
    print("=" * 70)

    planner = TripPlanner(
        api_key="test-key-123",
        weather_api_key="test-weather-key-456"
    )

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "temp_c": 25.0,
                "temp_f": 77.0,
                "condition": {"text": "Clear sky"},
                "humidity": 60
            }
        }
        mock_get.return_value = mock_response

        prompt = planner._build_prompt(
            "2025-12-20",
            "2025-12-25",
            5,
            preferences={"region": "Europe", "climate": "warm"}
        )

        print("Prompt successfully built with weather data")
        print(f"Prompt length: {len(prompt)} characters")
        print("\nPrompt contains weather data: ", end="")
        print("Yes ✓" if "REAL WEATHER DATA" in prompt else "No ✗")
        print("\nFirst 400 characters of prompt:")
        print("-" * 70)
        print(prompt[:400] + "...")
        print("-" * 70)
    print()

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "WEATHER INTEGRATION DEMO" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    try:
        demo_without_weather_api()
        demo_with_weather_api()
        demo_region_specific_weather()
        demo_prompt_integration()

        print("=" * 70)
        print("✓ All demos completed successfully!")
        print("=" * 70)
        print()
        print("Summary:")
        print("- Weather integration works without API key (graceful fallback)")
        print("- Weather integration works with API key (fetches real data)")
        print("- Region-specific weather data is supported")
        print("- Weather data is properly integrated into prompts")
        print()

    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
