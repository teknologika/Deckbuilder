"""
Comprehensive tests for table functionality in deckbuilder.

Tests cover:
- Table parsing in converter
- Table building/rendering
- End-to-end table integration
- Various table formats and edge cases
"""

import pytest
from unittest.mock import Mock

# Test imports with graceful handling
try:
    from deckbuilder.converter import FrontmatterConverter, markdown_to_canonical_json
    from deckbuilder.table_builder import TableBuilder

    HAS_TABLE_MODULES = True
except ImportError:
    HAS_TABLE_MODULES = False


@pytest.mark.skipif(not HAS_TABLE_MODULES, reason="Table modules not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestTableParser:
    """Test table parsing functionality in converter."""

    def test_simple_table_detection(self):
        """Test detection of simple markdown tables."""
        converter = FrontmatterConverter()

        # Test table content
        table_content = "| Header 1 | Header 2 |\n|---|---|\n| Cell 1 | Cell 2 |"
        assert converter._is_table_content(table_content) is True

        # Test non-table content
        non_table_content = "This is just regular text"
        assert converter._is_table_content(non_table_content) is False

        # Test content with single pipe (not a table)
        single_pipe = "This | is not a table"
        assert converter._is_table_content(single_pipe) is False

    def test_table_parsing_basic(self):
        """Test basic table parsing functionality."""
        converter = FrontmatterConverter()

        table_content = "| Header 1 | Header 2 |\n|---|---|\n| Cell 1 | Cell 2 |"
        result = converter._parse_markdown_table(table_content)

        assert result["type"] == "table"
        assert "data" in result
        assert len(result["data"]) == 2  # Header + 1 data row
        assert len(result["data"][0]) == 2  # 2 columns

        # Check cell structure
        first_cell = result["data"][0][0]
        assert "text" in first_cell
        assert "formatted" in first_cell
        assert first_cell["text"] == "Header 1"

    def test_table_parsing_with_formatting(self):
        """Test table parsing with formatted content."""
        converter = FrontmatterConverter()

        table_content = "| **Bold** | *Italic* | ___Underline___ |\n|---|---|---|\n| Regular | **Bold** | *Italic* |"
        result = converter._parse_markdown_table(table_content)

        assert result["type"] == "table"
        assert len(result["data"]) == 2

        # Check formatted header
        bold_cell = result["data"][0][0]
        assert bold_cell["text"] == "**Bold**"
        assert bold_cell["formatted"][0]["format"]["bold"] is True

        italic_cell = result["data"][0][1]
        assert italic_cell["text"] == "*Italic*"
        assert italic_cell["formatted"][0]["format"]["italic"] is True

        underline_cell = result["data"][0][2]
        assert underline_cell["text"] == "___Underline___"
        assert underline_cell["formatted"][0]["format"]["underline"] is True

    def test_table_parsing_without_outer_pipes(self):
        """Test parsing tables without outer pipe characters."""
        converter = FrontmatterConverter()

        table_content = "Header 1 | Header 2\n---|---\nCell 1 | Cell 2"
        result = converter._parse_markdown_table(table_content)

        assert result["type"] == "table"
        assert len(result["data"]) == 2
        assert len(result["data"][0]) == 2

        # Check content
        assert result["data"][0][0]["text"] == "Header 1"
        assert result["data"][1][0]["text"] == "Cell 1"

    def test_table_parsing_skips_separators(self):
        """Test that table parsing correctly skips separator lines."""
        converter = FrontmatterConverter()

        table_content = "| Header 1 | Header 2 |\n|---|---|\n| Cell 1 | Cell 2 |\n|===|===|\n| Cell 3 | Cell 4 |"
        result = converter._parse_markdown_table(table_content)

        assert result["type"] == "table"
        # Should have 3 rows: header + 2 data rows (separator lines skipped)
        assert len(result["data"]) == 3

    def test_table_in_markdown_conversion(self):
        """Test table conversion in full markdown processing."""
        markdown_content = """---
layout: Title and Content
title: Table Test
content: "| Feature | Status |\\n|---|---|\\n| Auth | Complete |\\n| API | In Progress |"
---"""

        result = markdown_to_canonical_json(markdown_content)

        assert len(result["slides"]) == 1
        slide = result["slides"][0]

        # Content should be a table object
        content = slide["placeholders"]["content"]
        assert isinstance(content, dict)
        assert content["type"] == "table"
        assert len(content["data"]) == 3  # Header + 2 data rows


@pytest.mark.skipif(not HAS_TABLE_MODULES, reason="Table modules not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestTableBuilder:
    """Test table building/rendering functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_slide = Mock()
        self.mock_slide.placeholders = []
        self.mock_slide.shapes = Mock()

        # Mock table creation
        self.mock_table = Mock()
        self.mock_table.cell = Mock()
        self.mock_slide.shapes.add_table.return_value.table = self.mock_table

    def test_table_builder_initialization(self):
        """Test TableBuilder initialization."""
        builder = TableBuilder()
        assert builder.content_formatter is None

        mock_formatter = Mock()
        builder_with_formatter = TableBuilder(mock_formatter)
        assert builder_with_formatter.content_formatter is mock_formatter

    def test_add_table_to_slide_basic(self):
        """Test adding a basic table to a slide."""
        builder = TableBuilder()

        # Mock slide setup
        mock_slide = Mock()
        mock_slide.placeholders = []
        mock_slide.shapes = Mock()
        mock_table = Mock()
        mock_slide.shapes.add_table.return_value.table = mock_table

        # Mock table columns and rows for styling
        mock_table.columns = [Mock(), Mock()]
        mock_table.rows = [Mock(), Mock()]

        # Mock cell with text_frame structure
        mock_cell = Mock()
        mock_cell.text_frame.paragraphs = []
        mock_cell.fill = Mock()
        mock_table.cell.return_value = mock_cell

        # Test data
        table_data = {
            "type": "table",
            "data": [
                [
                    {"text": "Header 1", "formatted": [{"text": "Header 1", "format": {}}]},
                    {"text": "Header 2", "formatted": [{"text": "Header 2", "format": {}}]},
                ],
                [
                    {"text": "Cell 1", "formatted": [{"text": "Cell 1", "format": {}}]},
                    {"text": "Cell 2", "formatted": [{"text": "Cell 2", "format": {}}]},
                ],
            ],
            "header_style": "dark_blue_white_text",
            "row_style": "alternating_light_gray",
            "border_style": "thin_gray",
        }

        builder.add_table_to_slide(mock_slide, table_data)

        # Verify table was created
        mock_slide.shapes.add_table.assert_called_once()
        # Verify cells were accessed (data writing + styling)
        assert mock_table.cell.call_count > 0

    def test_add_table_empty_data(self):
        """Test handling of empty table data."""
        builder = TableBuilder()
        mock_slide = Mock()

        # Empty table data
        table_data = {"data": []}

        builder.add_table_to_slide(mock_slide, table_data)

        # Should not create table for empty data
        mock_slide.shapes.add_table.assert_not_called()

    def test_add_table_with_content_formatter(self):
        """Test table creation with content formatter."""
        mock_formatter = Mock()
        builder = TableBuilder(mock_formatter)

        # Mock slide setup
        mock_slide = Mock()
        mock_slide.placeholders = []
        mock_slide.shapes = Mock()
        mock_table = Mock()
        mock_slide.shapes.add_table.return_value.table = mock_table

        # Mock table columns and rows for styling
        mock_table.columns = [Mock()]
        mock_table.rows = [Mock()]

        # Mock cell with text_frame structure
        mock_cell = Mock()
        mock_cell.text_frame.paragraphs = []
        mock_cell.fill = Mock()
        mock_table.cell.return_value = mock_cell

        # Test data with formatted content
        table_data = {
            "type": "table",
            "data": [
                [{"text": "**Bold**", "formatted": [{"text": "Bold", "format": {"bold": True}}]}]
            ],
        }

        builder.add_table_to_slide(mock_slide, table_data)

        # Verify formatter was called
        mock_formatter.apply_formatted_segments_to_cell.assert_called_once()

    def test_backward_compatibility_string_cells(self):
        """Test backward compatibility with old string cell format."""
        builder = TableBuilder()

        # Mock slide setup
        mock_slide = Mock()
        mock_slide.placeholders = []
        mock_slide.shapes = Mock()
        mock_table = Mock()
        mock_slide.shapes.add_table.return_value.table = mock_table

        # Mock table columns and rows for styling
        mock_table.columns = [Mock(), Mock()]
        mock_table.rows = [Mock(), Mock()]

        # Mock cell with text_frame structure
        mock_cell = Mock()
        mock_cell.text_frame.paragraphs = []
        mock_cell.fill = Mock()
        mock_table.cell.return_value = mock_cell

        # Old format with string cells
        table_data = {"data": [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]}

        builder.add_table_to_slide(mock_slide, table_data)

        # Verify table was created and cells were set
        mock_slide.shapes.add_table.assert_called_once()
        assert mock_table.cell.call_count > 0

    def test_custom_colors_support(self):
        """Test custom color support in table styling."""
        builder = TableBuilder()

        # Test color parsing
        red_color = builder._parse_custom_color("#FF0000")
        assert red_color is not None
        # RGBColor is iterable and returns RGB values
        r, g, b = red_color
        assert r == 255
        assert g == 0
        assert b == 0

        # Test invalid color
        invalid_color = builder._parse_custom_color("invalid")
        assert invalid_color is None

        # Test None color
        none_color = builder._parse_custom_color(None)
        assert none_color is None


@pytest.mark.skipif(not HAS_TABLE_MODULES, reason="Table modules not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestTableIntegration:
    """Test end-to-end table integration."""

    def test_table_pipeline_markdown_to_table(self):
        """Test complete pipeline from markdown to table object."""
        markdown_content = """---
layout: Title and Content
title: Feature Status
content: "| Feature | Status | Priority |\\n|---|---|---|\\n| **Authentication** | Complete | *High* |\\n| User Management | ***In Progress*** | ___Medium___ |\\n| Reporting | Planned | **Low** |"
---"""

        # Convert markdown to canonical JSON
        result = markdown_to_canonical_json(markdown_content)

        # Verify structure
        assert len(result["slides"]) == 1
        slide = result["slides"][0]
        assert slide["layout"] == "Title and Content"
        assert slide["placeholders"]["title"] == "Feature Status"

        # Verify table structure
        table_data = slide["placeholders"]["content"]
        assert table_data["type"] == "table"
        assert len(table_data["data"]) == 4  # Header + 3 data rows

        # Verify formatting preservation
        auth_cell = table_data["data"][1][0]  # "Authentication" cell
        assert auth_cell["text"] == "**Authentication**"
        assert auth_cell["formatted"][0]["format"]["bold"] is True

        progress_cell = table_data["data"][2][1]  # "In Progress" cell
        assert progress_cell["text"] == "***In Progress***"
        assert progress_cell["formatted"][0]["format"]["bold"] is True
        assert progress_cell["formatted"][0]["format"]["italic"] is True

    def test_table_with_mixed_content_layout(self):
        """Test table in Two Content layout with mixed content."""
        markdown_content = """---
layout: Two Content
title: Mixed Content Test
content_left: "- Bullet point 1\\n- Bullet point 2\\n- Bullet point 3"
content_right: "| Feature | Status |\\n|---|---|\\n| Auth | Complete |\\n| API | Progress |"
---"""

        result = markdown_to_canonical_json(markdown_content)

        assert len(result["slides"]) == 1
        slide = result["slides"][0]

        # Left content should be plain text
        left_content = slide["placeholders"]["content_left"]
        assert isinstance(left_content, str)
        assert "Bullet point 1" in left_content

        # Right content should be table
        right_content = slide["placeholders"]["content_right"]
        assert isinstance(right_content, dict)
        assert right_content["type"] == "table"
        assert len(right_content["data"]) == 3  # Header + 2 data rows

    def test_table_with_complex_formatting(self):
        """Test table with complex formatting combinations."""
        markdown_content = """---
layout: Title and Content
title: Complex Table
content: "| ***Bold Italic*** | ___Underline___ | **Bold** *Italic* |\\n|---|---|---|\\n| Regular text | **Bold** text | *Italic* text |\\n| ___Underlined___ | ***Combined*** | Normal |"
---"""

        result = markdown_to_canonical_json(markdown_content)
        table_data = result["slides"][0]["placeholders"]["content"]

        # Check complex formatting in header
        bold_italic_cell = table_data["data"][0][0]
        assert bold_italic_cell["formatted"][0]["format"]["bold"] is True
        assert bold_italic_cell["formatted"][0]["format"]["italic"] is True

        underline_cell = table_data["data"][0][1]
        assert underline_cell["formatted"][0]["format"]["underline"] is True

    def test_table_error_handling(self):
        """Test table parsing error handling."""
        # Test malformed table
        malformed_markdown = """---
layout: Title and Content
title: Malformed Table
content: "| Header 1 | Header 2\\n| Cell 1 | Cell 2 | Cell 3 |"
---"""

        result = markdown_to_canonical_json(malformed_markdown)
        table_data = result["slides"][0]["placeholders"]["content"]

        # Should still create table even with malformed structure
        assert table_data["type"] == "table"
        assert len(table_data["data"]) > 0

    def test_table_default_styling(self):
        """Test that tables get default styling applied."""
        markdown_content = """---
layout: Title and Content
title: Default Style Table
content: "| A | B |\\n|---|---|\\n| 1 | 2 |"
---"""

        result = markdown_to_canonical_json(markdown_content)
        table_data = result["slides"][0]["placeholders"]["content"]

        # Check default styling
        assert table_data["header_style"] == "dark_blue_white_text"
        assert table_data["row_style"] == "alternating_light_gray"
        assert table_data["border_style"] == "thin_gray"
        assert "custom_colors" in table_data
