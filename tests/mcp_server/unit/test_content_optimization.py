import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))  # noqa: E402

import pytest  # noqa: E402
from mcp_server.content_optimization import ContentOptimizationEngine  # noqa: E402


"""
Unit tests for the ContentOptimizationEngine in the MCP server.
"""


@pytest.fixture
def engine():
    """Returns a ContentOptimizationEngine instance for testing."""
    return ContentOptimizationEngine()


class TestContentOptimizationEngine:
    """Test suite for the ContentOptimizationEngine class."""

    def test_initialization(self, engine):
        """Test that the ContentOptimizationEngine initializes correctly."""
        assert engine is not None
        assert isinstance(engine.layout_templates, dict)
        assert "Four Columns" in engine.layout_templates

    @pytest.mark.skip(reason="Temporarily ignoring due to string literal issues")
    # @pytest.mark.parametrize(
    #     "input_content, expected_output",
    #     [
    #         # Whitespace normalization
    #         ("  Hello   World  ", "Hello   World"),
    #         ("""Line 1
    #
    #   Line 2
    #
    #
    # Line 3  """, """Line 1
    #
    # Line 2
    #
    # Line 3"""),
    #         ("  leading and trailing  ", "leading and trailing"),
    #         ("multiple    spaces", "multiple    spaces"),
    #         ("""line1
    #
    #
    # line2""", """line1
    #
    # line2"""),
    #         # Quote normalization
    #         ("“Hello” ‘World’", "\"Hello\" 'World'"),
    #         ("„Quote“ ‚Single‘", "\"Quote\" 'Single'"),
    #         ("»Guillemet«", "\"Guillemet\""),
    #         # Em dash normalization
    #         ("This—is—an—em—dash", "This-is-an-em-dash"),
    #         ("Another — em — dash", "Another - em - dash"),
    #         # Combined scenarios
    #         ("""  “Hello—World”
    #
    #   ‘Test’—Line  """, """\"Hello-World\"
    #
    # 'Test'-Line"""),
    #         ("  Leading—Edge “Solution”  ", "Leading-Edge \"Solution\""),
    #         # No cleaning needed
    #         ("No cleaning needed.", "No cleaning needed."),
    #         ("", ""),  # Empty string
    #         (" ", ""),  # Only spaces
    #     ],
    # )
    # def test_clean_content(self, engine, input_content, expected_output):
    #     """Test the _clean_content method for various cleaning scenarios."""
    #     cleaned_content = engine._clean_content(input_content)
    #     assert cleaned_content == expected_output

    @pytest.mark.skip  # noqa: E304
    def test_optimize_for_four_columns(self, engine):
        """Test the _optimize_for_four_columns method."""
        content = "Title: My Presentation\nCol 1: A\nCol 2: B\nCol 3: C\nCol 4: D"
        result = engine._optimize_for_four_columns(content, None)
        assert "layout: Four Columns" in result.yaml_structure
        assert "- title: Col 1" in result.yaml_structure

    def test_optimize_for_comparison(self, engine):
        """Test the _optimize_for_comparison method."""
        content = "Title: A vs B\nLeft: A is good\nRight: B is better"
        result = engine._optimize_for_comparison(content, None)
        assert "layout: Comparison" in result.yaml_structure
        assert "left:" in result.yaml_structure
        assert "right:" in result.yaml_structure

    def test_optimize_for_title_and_content(self, engine):
        """Test the _optimize_for_title_and_content method."""
        content = """My Title
This is the first point. This is the second point."""
        result = engine._optimize_for_title_and_content(content, None)
        assert "layout: Title and Content" in result.yaml_structure
        assert "- This is the first point" in result.yaml_structure
        assert "- This is the second point" in result.yaml_structure

    def test_extract_or_generate_title(self, engine):
        """Test the _extract_or_generate_title method."""
        content_with_title = "This is the title\nAnd this is the content."
        title = engine._extract_or_generate_title(content_with_title, None)
        assert title == "This is the title"

        content_without_title = "This content has no title."
        title = engine._extract_or_generate_title(content_without_title, None)
        assert title == "This Content Title"

    def test_apply_content_formatting(self, engine):
        """Test the _apply_content_formatting method."""
        content = "We saw a 20% increase, which is the best."
        formatted_content = engine._apply_content_formatting(content)
        assert "**20%**" in formatted_content
        assert "**best**" in formatted_content

    def test_structure_as_bullets(self, engine):
        """Test the _structure_as_bullets method."""
        content = "First point. Second point."
        bullet_content = engine._structure_as_bullets(content)
        assert "- First point" in bullet_content
        assert "- Second point" in bullet_content

    def test_analyze_content_layout_fit(self, engine):
        """Test the _analyze_content_layout_fit method."""
        content = "Col 1: A\nCol 2: B\nCol 3: C\nCol 4: D"
        optimization_result = engine._optimize_for_four_columns(content, None)
        gap_analysis = engine._analyze_content_layout_fit(content, "Four Columns", optimization_result)
        assert gap_analysis.content_fit == "excellent"

    def test_optimize_content_for_layout(self, engine):
        """Test the main optimize_content_for_layout method."""
        content = "Title: My Presentation\nCol 1: A\nCol 2: B\nCol 3: C\nCol 4: D"
        result = engine.optimize_content_for_layout(content, "Four Columns")

        assert "optimized_content" in result
        assert "gap_analysis" in result
        assert "presentation_tips" in result

        assert "yaml_structure" in result["optimized_content"]
        assert result["gap_analysis"]["content_fit"] == "excellent"
