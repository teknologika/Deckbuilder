import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

import pytest  # noqa: E402
from mcp_server.content_analysis import ContentAnalyzer  # noqa: E402


"""
Unit tests for the ContentAnalyzer class in the MCP server.
"""


@pytest.fixture
def analyzer():
    """Returns a ContentAnalyzer instance for testing."""
    return ContentAnalyzer()


class TestContentAnalyzer:
    """Test suite for the ContentAnalyzer class."""

    def test_initialization(self, analyzer):
        """Test that the ContentAnalyzer initializes correctly."""
        assert analyzer is not None
        assert isinstance(analyzer.audience_profiles, dict)
        assert "board" in analyzer.audience_profiles

    def test_extract_key_messages(self, analyzer):
        """Test the _extract_key_messages method."""
        user_input = (
            "We saw 20% growth in revenue, but churn is a problem. Our new strategy will fix this."
        )
        messages = analyzer._extract_key_messages(user_input)
        assert "metric: 20% growth" in messages
        assert "challenges/concerns" in messages
        assert "solutions/strategy" in messages
        assert "new initiatives" in messages

    def test_determine_narrative_arc(self, analyzer):
        """Test the _determine_narrative_arc method."""
        user_input_success = (
            "We had great success, but we have a challenge. Our plan is to solve it."
        )
        arc_success = analyzer._determine_narrative_arc(user_input_success, [])
        assert arc_success == "success-challenge-solution"

        user_input_problem = "The main issue is churn. Our solution is a new feature."
        arc_problem = analyzer._determine_narrative_arc(user_input_problem, [])
        assert arc_problem == "problem-solution"

        user_input_compare = "We can either choose option A or option B."
        arc_compare = analyzer._determine_narrative_arc(user_input_compare, [])
        assert arc_compare == "compare-contrast"

    def test_assess_complexity_level(self, analyzer):
        """Test the _assess_complexity_level method."""
        assert analyzer._assess_complexity_level("short input", "board") == "executive"
        assert analyzer._assess_complexity_level("short input", "technical") == "technical"
        long_input = "This is a very long input that should be considered detailed. " * 5
        assert analyzer._assess_complexity_level(long_input, "general") == "detailed"
        assert analyzer._assess_complexity_level("short input", "general") == "overview"

    def test_analyze_data_density(self, analyzer):
        """Test the _analyze_data_density method."""
        assert analyzer._analyze_data_density("1 2 3 4 5") == "metrics-heavy"
        assert analyzer._analyze_data_density("A story about a cat.") == "story-driven"
        assert analyzer._analyze_data_density("A balanced approach.") == "balanced"

    def test_detect_emotional_tone(self, analyzer):
        """Test the _detect_emotional_tone method."""
        assert analyzer._detect_emotional_tone("This is an urgent matter.", []) == "urgent"
        assert analyzer._detect_emotional_tone("I have a concern.", []) == "cautious"
        assert analyzer._detect_emotional_tone("We had great success.", []) == "positive"
        assert analyzer._detect_emotional_tone("This is a neutral statement.", []) == "neutral"

    def test_analyze_audience(self, analyzer):
        """Test the _analyze_audience method."""
        board_profile = analyzer._analyze_audience("board", None)
        assert board_profile["attention_span"] == "short"

        team_profile_constrained = analyzer._analyze_audience("team", "5 minutes")
        assert team_profile_constrained["attention_span"] == "short"

    def test_build_recommended_structure(self, analyzer):
        """Test the _build_recommended_structure method."""
        structure = analyzer._build_recommended_structure([], "problem-solution", {}, "inform")
        assert len(structure) == 3
        assert structure[0]["purpose"] == "set context"

    def test_develop_presentation_strategy(self, analyzer):
        """Test the _develop_presentation_strategy method."""
        strategy = analyzer._develop_presentation_strategy(
            "persuasive", {"attention_span": "medium", "preferred_format": "balanced"}, "persuade"
        )
        assert strategy["opening_approach"] == "story-based"
        assert "storytelling" in strategy["engagement_tactics"]

    def test_analyze_presentation_needs(self, analyzer):
        """Test the main analyze_presentation_needs method."""
        user_input = "Our revenue is up by 15%, but we are facing challenges with user retention. We need a new strategy to address this."
        analysis = analyzer.analyze_presentation_needs(user_input, audience="board")

        assert "content_analysis" in analysis
        assert "audience_considerations" in analysis
        assert "recommended_structure" in analysis
        assert "presentation_strategy" in analysis

        assert analysis["content_analysis"]["narrative_arc"] == "success-challenge-solution"
        assert analysis["audience_considerations"]["expertise_level"] == "expert"
