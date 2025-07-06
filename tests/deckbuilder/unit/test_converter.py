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
        """Test converting four columns structured frontmatter and content."""
        markdown_input = """---
layout: Four Columns With Titles
title: Feature Comparison
---

### Performance
Fast processing with optimized algorithms

### Security
Enterprise-grade encryption and compliance

### Usability
Intuitive interface with minimal learning curve

### Cost
Competitive pricing with flexible plans
"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Four Columns With Titles",
                "style": "default_style",
                "placeholders": {"title": "Feature Comparison"},
                "content": [
                    {"type": "heading", "level": 3, "text": "Performance"},
                    {"type": "paragraph", "text": "Fast processing with optimized algorithms"},
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 3, "text": "Security"},
                    {"type": "paragraph", "text": "Enterprise-grade encryption and compliance"},
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 3, "text": "Usability"},
                    {
                        "type": "paragraph",
                        "text": "Intuitive interface with minimal learning curve",
                    },
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 3, "text": "Cost"},
                    {"type": "paragraph", "text": "Competitive pricing with flexible plans"},
                ],
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
        """Test converting comparison structured frontmatter and content."""
        markdown_input = """---
layout: Comparison
title: Solution Analysis
---

### Current Solution
Proven reliability

### New Solution
Enhanced features
"""

        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Comparison",
                "style": "default_style",
                "placeholders": {"title": "Solution Analysis"},
                "content": [
                    {"type": "heading", "level": 3, "text": "Current Solution"},
                    {"type": "paragraph", "text": "Proven reliability"},
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 3, "text": "New Solution"},
                    {"type": "paragraph", "text": "Enhanced features"},
                ],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["content"] == expected_slides[i]["content"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]

    def test_convert_simple_markdown_with_headings_paragraphs_bullets(self):
        """Test conversion of simple markdown with various content types."""
        markdown_input = """---
layout: Title and Content
title: My Simple Slide
---

# Main Heading
This is a paragraph.

## Sub Heading
- Bullet 1
  - Nested Bullet 1.1
- Bullet 2

Another paragraph here.
"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Title and Content",
                "style": "default_style",
                "placeholders": {"title": "My Simple Slide"},
                "content": [
                    {"type": "heading", "level": 1, "text": "Main Heading"},
                    {"type": "paragraph", "text": "This is a paragraph."},
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 2, "text": "Sub Heading"},
                    {
                        "type": "bullets",
                        "items": [{"level": 1, "text": "Bullet 1"}],
                    },
                    {"type": "paragraph", "text": "  - Nested Bullet 1.1"},
                    {
                        "type": "bullets",
                        "items": [{"level": 1, "text": "Bullet 2"}],
                    },
                    {"type": "paragraph", "text": ""},
                    {"type": "paragraph", "text": "Another paragraph here."},
                ],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]
            assert slide["content"] == expected_slides[i]["content"]

    def test_convert_markdown_with_table(self):
        """Test conversion of markdown with a table."""
        markdown_input = """---
layout: Title and Content
title: My Table Slide
---

# Data Table

| Header 1 | Header 2 |
|---|---|
| Row 1 Col 1 | Row 1 Col 2 |
| Row 2 Col 1 | Row 2 Col 2 |
"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Title and Content",
                "style": "default_style",
                "placeholders": {"title": "My Table Slide"},
                "content": [
                    {"type": "heading", "level": 1, "text": "Data Table"},
                    {"type": "paragraph", "text": ""},
                ],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]
            assert slide["content"] == expected_slides[i]["content"]

    def test_convert_two_content_layout(self):
        """Test conversion for Two Content layout."""
        markdown_input = """---
layout: Two Content
title: Side by Side
---

### Left Section
Content for the left side.

- Left bullet 1

### Right Section
Content for the right side.

| A | B |
|---|---|
| 1 | 2 |
"""
        result = markdown_to_canonical_json(markdown_input)

        expected_slides = [
            {
                "layout": "Two Content",
                "style": "default_style",
                "placeholders": {"title": "Side by Side"},
                "content": [
                    {"type": "heading", "level": 3, "text": "Left Section"},
                    {"type": "paragraph", "text": "Content for the left side."},
                    {"type": "paragraph", "text": ""},
                    {"type": "bullets", "items": [{"level": 1, "text": "Left bullet 1"}]},
                    {"type": "paragraph", "text": ""},
                    {"type": "heading", "level": 3, "text": "Right Section"},
                    {"type": "paragraph", "text": "Content for the right side."},
                    {"type": "paragraph", "text": ""},
                ],
            }
        ]

        assert len(result["slides"]) == len(expected_slides)
        for i, slide in enumerate(result["slides"]):
            assert slide["layout"] == expected_slides[i]["layout"]
            assert slide["style"] == expected_slides[i]["style"]
            assert slide["content"] == expected_slides[i]["content"]
            assert slide["placeholders"] == expected_slides[i]["placeholders"]

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
        assert slide["layout"] == "Title and Content"  # Should default
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"
        assert placeholders["content"] == "Test Content"
        assert slide["content"] == [{"type": "paragraph", "text": ""}]

    def test_convert_unsupported_layout(self):
        """Test conversion for unsupported layout."""
        markdown_input = """---
layout: Unsupported Layout
title: Test Title
---

Some content here.
"""

        result = markdown_to_canonical_json(markdown_input)

        assert "slides" in result
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Unsupported Layout"
        placeholders = slide["placeholders"]
        assert placeholders["title"] == "Test Title"
        assert slide["content"] == [{"type": "paragraph", "text": "Some content here."}]
