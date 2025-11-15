#!/usr/bin/env python3
"""
Trip Planner AI - Find the best places to visit based on date ranges
Uses Claude API to generate personalized travel recommendations
"""

import os
import sys
from datetime import datetime
from anthropic import Anthropic


class TripPlanner:
    """Main class for trip planning using Claude AI"""

    def __init__(self, api_key: str = None):
        """
        Initialize the trip planner with Claude API

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter"
            )
        self.client = Anthropic(api_key=self.api_key)

    def validate_date(self, date_string: str) -> bool:
        """
        Validate date string format (YYYY-MM-DD)

        Args:
            date_string: Date string to validate

        Returns:
            True if valid, False otherwise
        """
        if date_string is None or not isinstance(date_string, str):
            return False

        if not date_string.strip():
            return False

        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

    def get_travel_recommendations(
        self,
        start_date: str,
        end_date: str,
        preferences: dict = None,
        stream: bool = False
    ):
        """
        Get travel recommendations from Claude based on date range

        Args:
            start_date: Trip start date (YYYY-MM-DD)
            end_date: Trip end date (YYYY-MM-DD)
            preferences: Optional dict with user preferences like:
                - budget: low, medium, high
                - interests: list of interests (e.g., culture, nature, adventure)
                - region: preferred region (e.g., Europe, Asia, Americas)
                - climate: preferred climate (warm, cold, moderate)
            stream: If True, yields text chunks as they arrive. If False, returns complete string.

        Returns:
            Generator yielding text chunks if stream=True, or complete string if stream=False
        """
        # Validate dates
        if not self.validate_date(start_date):
            raise ValueError(f"Invalid start date format: {start_date}. Use YYYY-MM-DD")
        if not self.validate_date(end_date):
            raise ValueError(f"Invalid end date format: {end_date}. Use YYYY-MM-DD")

        # Calculate trip duration
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        duration = (end - start).days

        if duration < 0:
            raise ValueError("End date must be on or after start date")

        # Validate preferences if provided
        if preferences is not None:
            if not isinstance(preferences, dict):
                raise ValueError("Preferences must be a dictionary")

            # Validate interests is a list if provided
            if "interests" in preferences and preferences["interests"] is not None:
                if not isinstance(preferences["interests"], list):
                    raise ValueError("Interests must be a list of strings")
                if not all(isinstance(i, str) for i in preferences["interests"]):
                    raise ValueError("All interests must be strings")

        # Build the prompt with date range and preferences
        prompt = self._build_prompt(start_date, end_date, duration, preferences)

        # Call Claude API
        try:
            if stream:
                # Return a generator for streaming
                return self._stream_response(prompt)
            else:
                # Return complete response
                message = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=2048,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return message.content[0].text

        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def _stream_response(self, prompt: str):
        """
        Internal method to stream the response from Claude API

        Args:
            prompt: The prompt to send to Claude

        Yields:
            Text chunks as they arrive from the API
        """
        try:
            with self.client.messages.stream(
                model="claude-3-5-haiku-20241022",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def _build_prompt(
        self,
        start_date: str,
        end_date: str,
        duration: int,
        preferences: dict = None
    ) -> str:
        """
        Build the prompt for Claude API

        Args:
            start_date: Trip start date
            end_date: Trip end date
            duration: Trip duration in days
            preferences: User preferences dict

        Returns:
            Formatted prompt string
        """
        # Parse the dates to get month and season info
        start = datetime.strptime(start_date, "%Y-%m-%d")
        start_month = start.strftime("%B")

        prompt = f"""I'm planning a trip from {start_date} to {end_date} ({duration} days).

Please recommend the best places to visit during this time period. Consider:
- The travel dates are in {start_month}, so recommend destinations with good weather and seasonal activities during this time
- The trip duration is {duration} days
"""

        # Add preferences if provided
        if preferences:
            prompt += "\nAdditional preferences:\n"

            if preferences.get("budget"):
                prompt += f"- Budget: {preferences['budget']}\n"

            if preferences.get("interests") and len(preferences["interests"]) > 0:
                interests = ", ".join(preferences["interests"])
                prompt += f"- Interests: {interests}\n"

            if preferences.get("region"):
                prompt += f"- Preferred region: {preferences['region']}\n"

            if preferences.get("climate"):
                prompt += f"- Preferred climate: {preferences['climate']}\n"

        prompt += """
Please provide:
1. Top 3-5 destination recommendations with brief explanations
2. Why each destination is ideal for the specified dates
3. Key attractions and activities for each destination
4. Any important travel considerations (weather, crowds, events, etc.)

Format the response in a clear, organized way."""

        return prompt


def main():
    """Main entry point for the script"""
    print("=" * 60)
    print("Trip Planner AI - Powered by Claude")
    print("=" * 60)
    print()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    try:
        planner = TripPlanner()

        # Get user input
        print("Enter your travel dates:")
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()

        # Optional preferences
        print("\nOptional preferences (press Enter to skip):")

        budget = input("Budget (low/medium/high): ").strip()
        interests_input = input("Interests (comma-separated, e.g., culture,nature,adventure): ").strip()
        region = input("Preferred region (e.g., Europe, Asia, Americas): ").strip()
        climate = input("Preferred climate (warm/cold/moderate): ").strip()

        # Build preferences dict
        preferences = {}
        if budget:
            preferences["budget"] = budget
        if interests_input:
            preferences["interests"] = [i.strip() for i in interests_input.split(",")]
        if region:
            preferences["region"] = region
        if climate:
            preferences["climate"] = climate

        # Get recommendations
        print("\n" + "=" * 60)
        print("Analyzing your travel dates and generating recommendations...")
        print("=" * 60)
        print()

        # Stream the recommendations
        for chunk in planner.get_travel_recommendations(
            start_date,
            end_date,
            preferences if preferences else None,
            stream=True
        ):
            print(chunk, end='', flush=True)

        print("\n" + "=" * 60)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
