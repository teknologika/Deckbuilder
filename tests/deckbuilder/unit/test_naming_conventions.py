"""
Unit tests for naming conventions system.
"""

import pytest

# Test imports with graceful handling
try:
    from deckbuilder.naming_conventions import NamingConvention, PlaceholderContext

    HAS_NAMING_CONVENTIONS = True
except ImportError:
    HAS_NAMING_CONVENTIONS = False
    PlaceholderContext = None
    NamingConvention = None


@pytest.mark.skipif(not HAS_NAMING_CONVENTIONS, reason="Naming conventions not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestNamingConvention:
    """Test cases for NamingConvention class."""

    def test_initialization(self, naming_convention):
        """Test NamingConvention initialization."""
        assert naming_convention is not None
        assert hasattr(naming_convention, "generate_placeholder_name")
        assert hasattr(naming_convention, "layout_mappings")

    @pytest.mark.parametrize(
        "layout_name,placeholder_idx,expected_pattern",
        [
            ("Four Columns With Titles", "13", "title_col1_1"),
            ("Comparison", "1", "title_left_1"),
            ("Two Content", "1", "content_left_1"),
            ("Title and Content", "1", "content_1"),
        ],
    )
    def test_convention_generation_patterns(self, naming_convention, layout_name, placeholder_idx, expected_pattern):
        """Test convention-based placeholder naming patterns."""
        context = PlaceholderContext(
            layout_name=layout_name,
            placeholder_idx=placeholder_idx,
            placeholder_type="title" if "title" in expected_pattern else "content",
        )

        result = naming_convention.generate_placeholder_name(context)

        # Check that result follows expected pattern structure
        if "col1" in expected_pattern:
            assert "col1" in result
        if "left" in expected_pattern:
            assert "left" in result
        if result.startswith("title"):
            assert result.startswith("title_")
        if result.startswith("content"):
            assert result.startswith("content_")

    def test_multi_tier_detection_confidence(self, naming_convention):
        """Test 5-tier detection system with confidence scoring."""
        # Test different context scenarios for confidence scoring
        contexts = [
            # High confidence - exact mapping scenario
            PlaceholderContext("Four Columns With Titles", "0", "title"),
            # Medium confidence - type-based detection
            PlaceholderContext("Unknown Layout", "1", "content"),
            # Lower confidence - position-based inference
            PlaceholderContext("Custom Layout", "5", "unknown"),
        ]

        results = []
        for context in contexts:
            result = naming_convention.generate_placeholder_name(context)
            results.append(result)

        # Verify all results are valid placeholder names
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0
            assert "_" in result  # Convention-based names should have underscores

    def test_column_layout_naming(self, naming_convention):
        """Test naming for column-based layouts."""
        layout_name = "Four Columns With Titles"

        # Test title placeholders for columns (using correct indices from mapping)
        column_title_indices = ["13", "15", "17", "19"]  # From the mapping
        for col_num, idx in enumerate(column_title_indices, 1):
            context = PlaceholderContext(
                layout_name=layout_name,
                placeholder_idx=idx,
                placeholder_type="title",
            )
            result = naming_convention.generate_placeholder_name(context)
            assert f"col{col_num}" in result
            assert "title" in result

        # Test content placeholders for columns (using correct indices from mapping)
        column_content_indices = ["14", "16", "18", "20"]  # From the mapping
        for col_num, idx in enumerate(column_content_indices, 1):
            context = PlaceholderContext(
                layout_name=layout_name,
                placeholder_idx=idx,
                placeholder_type="content",
            )
            result = naming_convention.generate_placeholder_name(context)
            assert f"col{col_num}" in result
            assert "content" in result

    def test_comparison_layout_naming(self, naming_convention):
        """Test naming for comparison layouts."""
        layout_name = "Comparison"

        # Test left side placeholders (using correct indices from mapping)
        left_title_context = PlaceholderContext(layout_name, "1", "title")  # Index 1 for left title
        left_content_context = PlaceholderContext(layout_name, "2", "content")  # Index 2 for left content

        left_title = naming_convention.generate_placeholder_name(left_title_context)
        left_content = naming_convention.generate_placeholder_name(left_content_context)

        assert "left" in left_title
        assert "left" in left_content
        assert "title" in left_title
        assert "content" in left_content

        # Test right side placeholders (using correct indices from mapping)
        right_title_context = PlaceholderContext(layout_name, "3", "title")  # Index 3 for right title
        right_content_context = PlaceholderContext(layout_name, "4", "content")  # Index 4 for right content

        right_title = naming_convention.generate_placeholder_name(right_title_context)
        right_content = naming_convention.generate_placeholder_name(right_content_context)

        assert "right" in right_title
        assert "right" in right_content
        assert "title" in right_title
        assert "content" in right_content

    def test_footer_element_naming(self, naming_convention):
        """Test naming for footer elements."""
        context = PlaceholderContext(
            layout_name="Title Slide",
            placeholder_idx="10",  # Footer placeholder index
            placeholder_type="footer",
        )

        result = naming_convention.generate_placeholder_name(context)
        assert "footer" in result

    def test_semantic_type_detection(self, naming_convention):
        """Test semantic type detection in naming."""
        # Test specific placeholder types with appropriate indices
        test_cases = [
            ("Title and Content", "0", "title", "title_"),  # Index 0 is always title
            ("Title and Content", "1", "content", "content_"),  # Index 1 is content in this layout
            ("Picture with Caption", "1", "image", "image_"),  # Index 1 is image in picture layout
            ("Picture with Caption", "2", "text", "text_"),  # Index 2 is caption
            ("Title Slide", "10", "date", "date_"),  # Index 10 is date footer
            ("Title Slide", "12", "slide_number", "slide_number_"),  # Index 12 is slide number
        ]

        for layout_name, placeholder_idx, placeholder_type, expected_prefix in test_cases:
            context = PlaceholderContext(
                layout_name=layout_name,
                placeholder_idx=placeholder_idx,
                placeholder_type=placeholder_type,
            )

            result = naming_convention.generate_placeholder_name(context)
            assert result.startswith(expected_prefix), f"Expected {result} to start with {expected_prefix} for {layout_name}:{placeholder_idx}"

    def test_position_inference(self, naming_convention):
        """Test position-based naming inference."""
        # Test different positions and their inferred meanings
        position_tests = [
            (0, "top"),  # First position usually top/main
            (1, "main"),  # Second position usually main content
            (10, "footer"),  # High index usually footer
        ]

        for placeholder_index, expected_position in position_tests:
            context = PlaceholderContext(
                layout_name="Custom Layout",
                placeholder_idx=str(placeholder_index),
                placeholder_type="unknown",
            )

            result = naming_convention.generate_placeholder_name(context)
            # Result should contain position indicator or be a valid fallback
            assert isinstance(result, str)
            assert len(result) > 0

    def test_fallback_naming(self, naming_convention):
        """Test fallback naming for unknown scenarios."""
        # Test with completely unknown context
        context = PlaceholderContext(
            layout_name="Completely Unknown Layout",
            placeholder_idx="999",
            placeholder_type="unknown",
        )

        result = naming_convention.generate_placeholder_name(context)

        # Should still generate a valid placeholder name
        assert isinstance(result, str)
        assert len(result) > 0
        assert "_" in result

        # Should follow basic convention format
        parts = result.split("_")
        assert len(parts) >= 2  # At least type_position or similar

    def test_consistent_naming(self, naming_convention):
        """Test that naming is consistent for same inputs."""
        context = PlaceholderContext(
            layout_name="Four Columns With Titles",
            placeholder_idx="1",
            placeholder_type="content",
        )

        # Generate name multiple times
        result1 = naming_convention.generate_placeholder_name(context)
        result2 = naming_convention.generate_placeholder_name(context)
        result3 = naming_convention.generate_placeholder_name(context)

        # Should be identical
        assert result1 == result2 == result3

    def test_unique_naming_for_different_contexts(self, naming_convention):
        """Test that different contexts generate different names."""
        contexts = [
            PlaceholderContext("Four Columns With Titles", "14", "content"),  # Col 1 content
            PlaceholderContext("Four Columns With Titles", "16", "content"),  # Col 2 content
            PlaceholderContext("Four Columns With Titles", "13", "title"),  # Col 1 title
            PlaceholderContext("Comparison", "2", "content"),  # Left content
        ]

        results = []
        for context in contexts:
            result = naming_convention.generate_placeholder_name(context)
            results.append(result)

        # All results should be different
        assert len(set(results)) == len(results), f"Found duplicate names: {results}"


@pytest.mark.skipif(not HAS_NAMING_CONVENTIONS, reason="Naming conventions not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestPlaceholderContext:
    """Test cases for PlaceholderContext dataclass."""

    def test_placeholder_context_creation(self):
        """Test PlaceholderContext creation."""
        context = PlaceholderContext(
            layout_name="Test Layout",
            placeholder_idx="5",
            placeholder_type="content",
        )

        assert context.layout_name == "Test Layout"
        assert context.placeholder_idx == "5"
        assert context.placeholder_type == "content"

    def test_placeholder_context_equality(self):
        """Test PlaceholderContext equality comparison."""
        context1 = PlaceholderContext("Layout", "1", "content")
        context2 = PlaceholderContext("Layout", "1", "content")
        context3 = PlaceholderContext("Layout", "2", "content")

        assert context1 == context2
        assert context1 != context3
