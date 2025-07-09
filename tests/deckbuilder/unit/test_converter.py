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

    def test_convert_four_columns_structured_to_placeholders(self):
        """Test converting four columns structured frontmatter with direct fields."""
        markdown_input = """---
layout: Four Columns With Titles
title: Feature Comparison
title_col1: Performance
content_col1: Fast processing with optimized algorithms
title_col2: Security
content_col2: Enterprise-grade encryption and compliance
title_col3: Usability
content_col3: Intuitive interface with minimal learning curve
title_col4: Cost
content_col4: Competitive pricing with flexible plans
---"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Four Columns With Titles",
                "style": "default_style",
                "placeholders": {
                    "title": "Feature Comparison",
                    "title_col1": "Performance",
                    "content_col1": "Fast processing with optimized algorithms",
                    "title_col2": "Security",
                    "content_col2": "Enterprise-grade encryption and compliance",
                    "title_col3": "Usability",
                    "content_col3": "Intuitive interface with minimal learning curve",
                    "title_col4": "Cost",
                    "content_col4": "Competitive pricing with flexible plans",
                },
                "content": [],
            }
        ]

        # Compare the generated result with the expected structure
        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["content"] == expected_slides[i]["content"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]

    def test_convert_comparison_structured_to_placeholders(self):
        """Test converting comparison structured frontmatter with direct fields."""
        markdown_input = """---
layout: Comparison
title: Solution Analysis
title_left: Current Solution
content_left: Proven reliability
title_right: New Solution
content_right: Enhanced features
---"""

        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Comparison",
                "style": "default_style",
                "placeholders": {
                    "title": "Solution Analysis",
                    "title_left": "Current Solution",
                    "content_left": "Proven reliability",
                    "title_right": "New Solution",
                    "content_right": "Enhanced features",
                },
                "content": [],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["content"] == expected_slides[i]["content"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]

    def test_convert_simple_markdown_with_headings_paragraphs_bullets(self):
        """Test conversion of title and content with structured frontmatter."""
        markdown_input = """---
layout: Title and Content
title: My Simple Slide
content: "- Bullet 1\\n- Bullet 2\\n- Bullet 3"
---"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Title and Content",
                "style": "default_style",
                "placeholders": {
                    "title": "My Simple Slide",
                    "content": "- Bullet 1\n- Bullet 2\n- Bullet 3",
                },
                "content": [],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]
            assert slide["content"] == expected_slides[i]["content"]

    def test_convert_markdown_with_table(self):
        """Test conversion of structured frontmatter with table content."""
        markdown_input = """---
layout: Title and Content
title: My Table Slide
content: "| Header 1 | Header 2 |\\n|---|---|\\n| Row 1 Col 1 | Row 1 Col 2 |"
---"""
        result = markdown_to_canonical_json(markdown_input)

        # Test structure - content should be JSON table object
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Title and Content"
        assert slide["style"] == "default_style"
        assert slide["placeholders"]["title"] == "My Table Slide"
        assert isinstance(slide["placeholders"]["content"], dict)
        assert slide["placeholders"]["content"]["type"] == "table"
        assert "data" in slide["placeholders"]["content"]
        assert len(slide["placeholders"]["content"]["data"]) == 2  # Header and data row
        assert slide["content"] == []

    def test_convert_two_content_layout(self):
        """Test conversion for Two Content layout with structured frontmatter."""
        markdown_input = """---
layout: Two Content
title: Side by Side
content_left: "- Left bullet 1\\n- Left bullet 2"
content_right: "| A | B |\\n|---|---|\\n| 1 | 2 |"
---"""
        result = markdown_to_canonical_json(markdown_input)

        # Test the structure rather than exact format due to complex processing
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Two Content"
        assert slide["style"] == "default_style"
        assert slide["placeholders"]["title"] == "Side by Side"
        assert slide["content"] == []

        # Test that content_left is plain string with bullet markdown
        assert isinstance(slide["placeholders"]["content_left"], str)
        assert "- Left bullet 1" in slide["placeholders"]["content_left"]

        # Test that content_right is JSON table object
        assert isinstance(slide["placeholders"]["content_right"], dict)
        assert slide["placeholders"]["content_right"]["type"] == "table"
        assert "data" in slide["placeholders"]["content_right"]

    def test_convert_missing_layout(self):
        """Test conversion when layout field is missing."""
        markdown_input = """---
title: Test Title
content: Test Content
---"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Title and Content"  # Should default
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"
        assert placeholders["content"] == "Test Content"
        assert slide["content"] == []

    def test_convert_unsupported_layout(self):
        """Test conversion for unsupported layout."""
        markdown_input = """---
layout: Unsupported Layout
title: Test Title
content: Some content here.
---"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Unsupported Layout"
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"
        assert placeholders["content"] == "Some content here."
        assert slide["content"] == []
