"""
Unit tests for TripPlanner class
Run with: pytest test_trip_planner.py -v
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from trip_planner import TripPlanner


class TestTripPlannerInit:
    """Test TripPlanner initialization"""

    def test_init_with_api_key(self):
        """Test initialization with API key parameter"""
        planner = TripPlanner(api_key="test-key-123")
        assert planner.api_key == "test-key-123"
        assert planner.client is not None

    def test_init_with_env_var(self, monkeypatch):
        """Test initialization with environment variable"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key-456")
        planner = TripPlanner()
        assert planner.api_key == "env-key-456"

    def test_init_without_api_key(self, monkeypatch):
        """Test initialization fails without API key"""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="API key not found"):
            TripPlanner()

    def test_init_api_key_priority(self, monkeypatch):
        """Test that parameter takes priority over env var"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key")
        planner = TripPlanner(api_key="param-key")
        assert planner.api_key == "param-key"


class TestDateValidation:
    """Test date validation functionality"""

    @pytest.fixture
    def planner(self):
        """Create a TripPlanner instance for testing"""
        return TripPlanner(api_key="test-key")

    def test_valid_date(self, planner):
        """Test validation of valid date"""
        assert planner.validate_date("2025-07-15") is True

    def test_invalid_date_format(self, planner):
        """Test validation of invalid date format"""
        assert planner.validate_date("07/15/2025") is False
        assert planner.validate_date("15-07-2025") is False
        assert planner.validate_date("2025/07/15") is False

    def test_invalid_date_values(self, planner):
        """Test validation of invalid date values"""
        assert planner.validate_date("2025-13-01") is False  # Invalid month
        assert planner.validate_date("2025-02-30") is False  # Invalid day

    def test_none_date(self, planner):
        """Test validation of None date"""
        assert planner.validate_date(None) is False

    def test_empty_date(self, planner):
        """Test validation of empty date string"""
        assert planner.validate_date("") is False
        assert planner.validate_date("   ") is False

    def test_non_string_date(self, planner):
        """Test validation of non-string date"""
        assert planner.validate_date(123) is False
        assert planner.validate_date([2025, 7, 15]) is False

    def test_malformed_dates(self, planner):
        """Test validation of malformed dates"""
        assert planner.validate_date("not-a-date") is False
        assert planner.validate_date("2025-07") is False
        assert planner.validate_date("2025-07-15-extra") is False


class TestGetTravelRecommendations:
    """Test the main get_travel_recommendations method"""

    @pytest.fixture
    def planner(self):
        """Create a TripPlanner instance with mocked API"""
        return TripPlanner(api_key="test-key")

    @pytest.fixture
    def mock_api_response(self):
        """Mock API response"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Here are some great destinations..."
        mock_response.content = [mock_content]
        return mock_response

    def test_valid_date_range(self, planner, mock_api_response):
        """Test with valid date range"""
        with patch.object(planner.client.messages, 'create', return_value=mock_api_response):
            result = planner.get_travel_recommendations("2025-07-15", "2025-07-25")
            assert result == "Here are some great destinations..."

    def test_same_day_trip(self, planner, mock_api_response):
        """Test with same start and end date (0-day trip)"""
        with patch.object(planner.client.messages, 'create', return_value=mock_api_response):
            result = planner.get_travel_recommendations("2025-07-15", "2025-07-15")
            assert result == "Here are some great destinations..."

    def test_invalid_start_date(self, planner):
        """Test with invalid start date"""
        with pytest.raises(ValueError, match="Invalid start date format"):
            planner.get_travel_recommendations("invalid-date", "2025-07-25")

    def test_invalid_end_date(self, planner):
        """Test with invalid end date"""
        with pytest.raises(ValueError, match="Invalid end date format"):
            planner.get_travel_recommendations("2025-07-15", "invalid-date")

    def test_end_before_start(self, planner):
        """Test with end date before start date"""
        with pytest.raises(ValueError, match="End date must be on or after start date"):
            planner.get_travel_recommendations("2025-07-25", "2025-07-15")

    def test_none_dates(self, planner):
        """Test with None dates"""
        with pytest.raises(ValueError, match="Invalid start date format"):
            planner.get_travel_recommendations(None, "2025-07-25")

        with pytest.raises(ValueError, match="Invalid end date format"):
            planner.get_travel_recommendations("2025-07-15", None)

    def test_empty_dates(self, planner):
        """Test with empty date strings"""
        with pytest.raises(ValueError, match="Invalid start date format"):
            planner.get_travel_recommendations("", "2025-07-25")

    def test_with_valid_preferences(self, planner, mock_api_response):
        """Test with valid preferences"""
        preferences = {
            "budget": "medium",
            "interests": ["culture", "food"],
            "region": "Europe",
            "climate": "warm"
        }
        with patch.object(planner.client.messages, 'create', return_value=mock_api_response):
            result = planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )
            assert result == "Here are some great destinations..."

    def test_with_invalid_preferences_type(self, planner):
        """Test with invalid preferences type"""
        with pytest.raises(ValueError, match="Preferences must be a dictionary"):
            planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", "not-a-dict"
            )

    def test_with_invalid_interests_type(self, planner):
        """Test with invalid interests type (not a list)"""
        preferences = {"interests": "culture, food"}
        with pytest.raises(ValueError, match="Interests must be a list"):
            planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )

    def test_with_non_string_interests(self, planner):
        """Test with non-string items in interests list"""
        preferences = {"interests": ["culture", 123, "food"]}
        with pytest.raises(ValueError, match="All interests must be strings"):
            planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )

    def test_with_empty_interests_list(self, planner, mock_api_response):
        """Test with empty interests list"""
        preferences = {"interests": []}
        with patch.object(planner.client.messages, 'create', return_value=mock_api_response):
            result = planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )
            assert result == "Here are some great destinations..."

    def test_api_error_handling(self, planner):
        """Test handling of API errors"""
        with patch.object(
            planner.client.messages,
            'create',
            side_effect=Exception("API Error")
        ):
            with pytest.raises(Exception, match="Error calling Claude API"):
                planner.get_travel_recommendations("2025-07-15", "2025-07-25")


class TestBuildPrompt:
    """Test the prompt building functionality"""

    @pytest.fixture
    def planner(self):
        """Create a TripPlanner instance"""
        return TripPlanner(api_key="test-key")

    def test_basic_prompt(self, planner):
        """Test basic prompt without preferences"""
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, None)
        assert "2025-07-15" in prompt
        assert "2025-07-25" in prompt
        assert "10 days" in prompt
        assert "July" in prompt

    def test_prompt_with_budget(self, planner):
        """Test prompt with budget preference"""
        preferences = {"budget": "medium"}
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, preferences)
        assert "Budget: medium" in prompt

    def test_prompt_with_interests(self, planner):
        """Test prompt with interests"""
        preferences = {"interests": ["culture", "food", "nature"]}
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, preferences)
        assert "Interests: culture, food, nature" in prompt

    def test_prompt_with_region(self, planner):
        """Test prompt with region preference"""
        preferences = {"region": "Asia"}
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, preferences)
        assert "Preferred region: Asia" in prompt

    def test_prompt_with_climate(self, planner):
        """Test prompt with climate preference"""
        preferences = {"climate": "warm"}
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, preferences)
        assert "Preferred climate: warm" in prompt

    def test_prompt_with_all_preferences(self, planner):
        """Test prompt with all preferences"""
        preferences = {
            "budget": "high",
            "interests": ["adventure", "wildlife"],
            "region": "Africa",
            "climate": "hot"
        }
        prompt = planner._build_prompt("2025-07-15", "2025-07-25", 10, preferences)
        assert "Budget: high" in prompt
        assert "adventure, wildlife" in prompt
        assert "Preferred region: Africa" in prompt
        assert "Preferred climate: hot" in prompt

    def test_prompt_different_months(self, planner):
        """Test prompt generation for different months"""
        # January
        prompt = planner._build_prompt("2025-01-15", "2025-01-20", 5, None)
        assert "January" in prompt

        # December
        prompt = planner._build_prompt("2025-12-15", "2025-12-20", 5, None)
        assert "December" in prompt

    def test_zero_day_trip_prompt(self, planner):
        """Test prompt for zero-day trip"""
        prompt = planner._build_prompt("2025-07-15", "2025-07-15", 0, None)
        assert "0 days" in prompt


class TestIntegration:
    """Integration tests"""

    def test_full_workflow_basic(self, monkeypatch):
        """Test complete workflow with mocked API"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        planner = TripPlanner()

        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Visit Paris, Rome, and Barcelona!"
        mock_response.content = [mock_content]

        with patch.object(planner.client.messages, 'create', return_value=mock_response) as mock_create:
            result = planner.get_travel_recommendations("2025-07-15", "2025-07-25")

            # Verify the API was called
            assert mock_create.called
            call_args = mock_create.call_args

            # Verify correct model
            assert call_args.kwargs["model"] == "claude-sonnet-4-5-20250929"

            # Verify result
            assert result == "Visit Paris, Rome, and Barcelona!"

    def test_full_workflow_with_preferences(self, monkeypatch):
        """Test complete workflow with preferences"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        planner = TripPlanner()

        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Budget-friendly beach destinations..."
        mock_response.content = [mock_content]

        preferences = {
            "budget": "low",
            "interests": ["beaches", "relaxation"],
            "climate": "warm"
        }

        with patch.object(planner.client.messages, 'create', return_value=mock_response) as mock_create:
            result = planner.get_travel_recommendations(
                "2025-06-01", "2025-06-10", preferences
            )

            # Verify the prompt contains preferences
            call_args = mock_create.call_args
            prompt = call_args.kwargs["messages"][0]["content"]
            assert "Budget: low" in prompt
            assert "beaches, relaxation" in prompt
            assert "Preferred climate: warm" in prompt

            assert result == "Budget-friendly beach destinations..."


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    @pytest.fixture
    def planner(self):
        """Create a TripPlanner instance"""
        return TripPlanner(api_key="test-key")

    def test_leap_year_date(self, planner):
        """Test with leap year date"""
        assert planner.validate_date("2024-02-29") is True
        assert planner.validate_date("2025-02-29") is False

    def test_very_long_trip(self, planner, monkeypatch):
        """Test with very long trip duration"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "World tour recommendations..."
        mock_response.content = [mock_content]

        with patch.object(planner.client.messages, 'create', return_value=mock_response):
            result = planner.get_travel_recommendations("2025-01-01", "2025-12-31")
            assert result == "World tour recommendations..."

    def test_preferences_with_none_values(self, planner, monkeypatch):
        """Test preferences with None values"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Recommendations..."
        mock_response.content = [mock_content]

        preferences = {
            "budget": "medium",
            "interests": None,
            "region": None
        }

        with patch.object(planner.client.messages, 'create', return_value=mock_response):
            result = planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )
            assert result == "Recommendations..."

    def test_whitespace_in_dates(self, planner):
        """Test that dates with whitespace are handled"""
        # Whitespace-only strings should be invalid
        assert planner.validate_date("  ") is False
        assert planner.validate_date("\t") is False

    def test_single_interest(self, planner, monkeypatch):
        """Test with single interest in list"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Cultural destinations..."
        mock_response.content = [mock_content]

        preferences = {"interests": ["culture"]}

        with patch.object(planner.client.messages, 'create', return_value=mock_response):
            result = planner.get_travel_recommendations(
                "2025-07-15", "2025-07-25", preferences
            )
            assert result == "Cultural destinations..."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
