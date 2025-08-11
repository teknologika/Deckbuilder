"""
Table Integration Module

Table + frontmatter styling integration and slide data assembly.
Handles extracting tables from content and applying frontmatter styling configurations.

This module bridges table parsing with slide presentation requirements.
"""

from typing import Dict, Any, Optional
from .table_parser import parse_markdown_table, is_table_content


def extract_table_from_content(content: str, slide_data: dict) -> Optional[dict]:
    """
    Extract table data from content and combine with frontmatter styling properties.

    Args:
        content: The content string which may contain markdown tables
        slide_data: The slide data containing frontmatter properties

    Returns:
        Dictionary with table data and styling, or None if no table found
    """
    if not content or not isinstance(content, str):
        return None

    # Check if content contains table markdown
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # Find table lines
    table_lines = []
    for line in lines:
        # Skip separator lines and non-table lines
        if line.startswith("|") and line.endswith("|"):
            table_lines.append(line)
        elif "|" in line and not line.startswith("---") and not line.startswith("==="):
            table_lines.append(line)

    if len(table_lines) < 2:  # Need at least header + 1 data row
        return None

    # Parse table data
    table_data = []
    for line in table_lines:
        # Clean up separators
        clean_line = line.replace("|", "").replace("-", "").replace(":", "").replace("=", "").strip()
        if clean_line == "" or all(c in "|-:= " for c in line):
            continue  # Skip separator lines

        # Parse cells
        if line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line[1:-1].split("|")]
        else:
            cells = [cell.strip() for cell in line.split("|")]

        table_data.append(cells)

    if not table_data:
        return None

    # Create table object with styling from frontmatter
    table_obj = {
        "data": table_data,
        "header_style": "dark_blue_white_text",  # default
        "row_style": "alternating_light_gray",  # default
        "border_style": "thin_gray",  # default
        "custom_colors": {},
    }

    # Apply frontmatter styling properties
    if "style" in slide_data:
        table_obj["header_style"] = slide_data["style"]
    if "row_style" in slide_data:
        table_obj["row_style"] = slide_data["row_style"]
    if "border_style" in slide_data:
        table_obj["border_style"] = slide_data["border_style"]

    # Apply dimension properties
    if "column_widths" in slide_data:
        table_obj["column_widths"] = slide_data["column_widths"]
    if "row_height" in slide_data:
        table_obj["row_height"] = slide_data["row_height"]
    if "table_width" in slide_data:
        table_obj["table_width"] = slide_data["table_width"]

    return table_obj


def apply_frontmatter_styling_to_table(table_data: dict, slide_data: dict) -> dict:
    """
    Apply frontmatter styling properties to an existing table data structure.

    Args:
        table_data: Existing table data dictionary
        slide_data: Slide data containing frontmatter styling properties

    Returns:
        Updated table data with styling applied
    """
    if not table_data or not isinstance(table_data, dict):
        return table_data

    # Create a copy to avoid modifying the original
    styled_table = table_data.copy()

    # Apply styling properties from frontmatter
    if "style" in slide_data:
        styled_table["header_style"] = slide_data["style"]
    if "row_style" in slide_data:
        styled_table["row_style"] = slide_data["row_style"]
    if "border_style" in slide_data:
        styled_table["border_style"] = slide_data["border_style"]

    # Apply dimension properties
    if "column_widths" in slide_data:
        styled_table["column_widths"] = slide_data["column_widths"]
    if "row_height" in slide_data:
        styled_table["row_height"] = slide_data["row_height"]
    if "table_width" in slide_data:
        styled_table["table_width"] = slide_data["table_width"]

    # Apply custom colors if present
    if "custom_colors" in slide_data:
        styled_table["custom_colors"] = slide_data["custom_colors"]

    return styled_table


def process_markdown_content(content: str) -> Any:
    """Process markdown content to convert dash bullets to bullet symbols and detect tables"""
    if not isinstance(content, str):
        return content

    # First check if this content contains a table
    if is_table_content(content):
        # Convert to table object
        return parse_markdown_table(content)

    # Convert dash bullets to bullet symbols
    # Match lines that start with "- " (dash followed by space)
    import re

    processed = re.sub(r"^- ", "• ", content, flags=re.MULTILINE)
    return processed


class FrontmatterConverter:
    """Legacy alias for backward compatibility during refactoring"""

    def _process_content_field(self, content: str) -> str:
        """Process content field for basic formatting and return as-is for now."""
        if not isinstance(content, str):
            return str(content) if content is not None else ""
        return content.strip()

    def _is_table_content(self, content: str) -> bool:
        """Check if content contains table markdown syntax"""
        return is_table_content(content)

    def _parse_markdown_table(self, content: str) -> dict:
        """Extract table from markdown and apply default styling config"""
        return parse_markdown_table(content)