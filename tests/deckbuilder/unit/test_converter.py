"""
Unit tests for the converter module.
"""

import pytest

# Test imports with graceful handling
try:
    from deckbuilder.converter import markdown_to_canonical_json
    HAS_CONVERTER = True
except ImportError:
    HAS_CONVERTER = False


@pytest.mark.skipif(not HAS_CONVERTER, reason="Converter not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestConverter:
    """Test cases for the markdown_to_canonical_json function."""

    def test_convert_four_columns_structured_to_placeholders(
        self, sample_structured_frontmatter
    ):
        """Test converting four columns structured frontmatter."""
        markdown_input = """---
layout: Four Columns With Titles
title: Feature Comparison
columns:
  - title: Performance
    content: Fast processing with optimized algorithms
  - title: Security
    content: Enterprise-grade encryption and compliance
  - title: Usability
    content: Intuitive interface with minimal learning curve
  - title: Cost
    content: Competitive pricing with flexible plans
---
"""
        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Four Columns With Titles"
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Feature Comparison"
        assert "title_col1" in placeholders

    def test_convert_comparison_structured_to_placeholders(self):
        """Test converting comparison structured frontmatter."""
        markdown_input = """---
layout: Comparison
title: Solution Analysis
comparison:
  left:
    title: Current Solution
    content: Proven reliability
  right:
    title: New Solution
    content: Enhanced features
---
"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Comparison"
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Solution Analysis"
        assert "title_left_1" in placeholders
        assert "content_right_1" in placeholders

    def test_convert_unsupported_layout(self):
        """Test conversion for unsupported layout."""
        markdown_input = """---
layout: Unsupported Layout
title: Test Title
---
"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Unsupported Layout"
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"

    def test_convert_missing_layout(self):
        """Test conversion when layout field is missing."""
        markdown_input = """---
title: Test Title
content: Test Content
---
"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Title and Content" # Should default
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"
