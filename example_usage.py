#!/usr/bin/env python3
"""
Example usage of the TripPlanner class for programmatic access
"""

import os
from trip_planner import TripPlanner


def example_basic_usage():
    """Example: Basic usage with just dates"""
    print("=" * 60)
    print("Example 1: Basic Usage (dates only)")
    print("=" * 60)

    planner = TripPlanner()

    for chunk in planner.get_travel_recommendations(
        start_date="2025-12-20",
        end_date="2025-12-30",
        stream=True
    ):
        print(chunk, end='', flush=True)

    print("\n")


def example_with_preferences():
    """Example: Using preferences to customize recommendations"""
    print("=" * 60)
    print("Example 2: With Preferences")
    print("=" * 60)

    planner = TripPlanner()

    for chunk in planner.get_travel_recommendations(
        start_date="2025-07-15",
        end_date="2025-07-25",
        preferences={
            "budget": "medium",
            "interests": ["culture", "food", "history"],
            "region": "Europe",
            "climate": "warm"
        },
        stream=True
    ):
        print(chunk, end='', flush=True)

    print("\n")


def example_adventure_trip():
    """Example: Adventure-focused trip"""
    print("=" * 60)
    print("Example 3: Adventure Trip")
    print("=" * 60)

    planner = TripPlanner()

    for chunk in planner.get_travel_recommendations(
        start_date="2025-09-01",
        end_date="2025-09-14",
        preferences={
            "budget": "high",
            "interests": ["adventure", "nature", "hiking", "wildlife"],
            "climate": "moderate"
        },
        stream=True
    ):
        print(chunk, end='', flush=True)

    print("\n")


def example_budget_beach_vacation():
    """Example: Budget beach vacation"""
    print("=" * 60)
    print("Example 4: Budget Beach Vacation")
    print("=" * 60)

    planner = TripPlanner()

    for chunk in planner.get_travel_recommendations(
        start_date="2025-06-01",
        end_date="2025-06-08",
        preferences={
            "budget": "low",
            "interests": ["beaches", "relaxation", "snorkeling"],
            "climate": "warm"
        },
        stream=True
    ):
        print(chunk, end='', flush=True)

    print("\n")


def example_winter_getaway():
    """Example: Winter getaway"""
    print("=" * 60)
    print("Example 5: Winter Getaway")
    print("=" * 60)

    planner = TripPlanner()

    for chunk in planner.get_travel_recommendations(
        start_date="2026-01-10",
        end_date="2026-01-20",
        preferences={
            "budget": "medium",
            "interests": ["skiing", "winter sports", "cozy atmosphere"],
            "climate": "cold"
        },
        stream=True
    ):
        print(chunk, end='', flush=True)

    print("\n")


def main():
    """Run all examples"""
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    print("\n" + "=" * 60)
    print("Trip Planner AI - Example Usage")
    print("=" * 60)
    print("\nThis script demonstrates different ways to use TripPlanner")
    print("Choose an example to run:\n")
    print("1. Basic usage (dates only)")
    print("2. With preferences (Europe summer trip)")
    print("3. Adventure trip")
    print("4. Budget beach vacation")
    print("5. Winter getaway")
    print("6. Run all examples")
    print("0. Exit")

    choice = input("\nEnter your choice (0-6): ").strip()

    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_with_preferences()
    elif choice == "3":
        example_adventure_trip()
    elif choice == "4":
        example_budget_beach_vacation()
    elif choice == "5":
        example_winter_getaway()
    elif choice == "6":
        print("\nRunning all examples...\n")
        example_basic_usage()
        example_with_preferences()
        example_adventure_trip()
        example_budget_beach_vacation()
        example_winter_getaway()
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and select 0-6.")


if __name__ == "__main__":
    main()
