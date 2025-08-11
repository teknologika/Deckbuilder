"""
Table Parser Module

Pure table markdown parsing and formatting functionality.
Handles detection, parsing, and inline formatting of markdown tables.

This module is focused solely on table parsing without any slide integration logic.
"""

from typing import List, Dict, Any


def is_table_content(content: str) -> bool:
    """Check if content contains table markdown syntax"""
    if not isinstance(content, str):
        return False

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # A table needs at least 2 lines and contain pipe characters
    if len(lines) < 2:
        return False

    # Check if we have lines that look like table rows
    table_lines = 0
    for line in lines:
        # Count lines that have multiple pipe characters (table rows)
        if line.count("|") >= 2:
            table_lines += 1

    # Need at least 2 rows to be considered a table
    return table_lines >= 2


def extract_table_markdown(content: str) -> str:
    """
    Extract just the table markdown from content, preserving surrounding text.

    Args:
        content: Full content string that may contain table + other text

    Returns:
        The table markdown portion only, or empty string if not found
    """
    if not isinstance(content, str):
        return ""

    lines = content.split("\n")
    table_lines = []
    table_start = -1

    # Find table boundaries
    for i, line in enumerate(lines):
        line = line.strip()
        if "|" in line and not all(c in "|-:= \t" for c in line.strip()):
            # This is a table row
            if table_start == -1:
                table_start = i
            table_lines.append(lines[i])
        elif table_start != -1 and "|" in line and all(c in "|-:= \t" for c in line.replace("|", "").strip()):
            # This is a separator line within table
            table_lines.append(lines[i])
        elif table_start != -1 and line == "":
            # Empty line might be within table
            continue
        elif table_start != -1:
            # Non-table line after table started - table might be ended
            break

    if table_lines:
        return "\n".join(table_lines)
    return ""


def parse_markdown_table(content: str) -> Dict[str, Any]:
    """Extract table from markdown and apply default styling config"""
    table_data = {
        "type": "table",
        "data": [],
        "header_style": "dark_blue_white_text",
        "row_style": "alternating_light_gray",
        "border_style": "thin_gray",
        "custom_colors": {},
    }

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # Extract table rows
    for i, line in enumerate(lines):
        # Skip separator lines (contain only dashes, pipes, colons, spaces, tabs, and equals)
        if all(c in "-|:=\t " for c in line.strip()):
            continue

        # Parse table row - handle both formats: |cell|cell| and cell|cell
        has_pipes = "|" in line
        if has_pipes:
            if line.strip().startswith("|") and line.strip().endswith("|"):
                # Format: |cell|cell|
                raw_cells = [cell.strip() for cell in line.strip("|").split("|")]
            else:
                # Format: cell|cell or mixed
                raw_cells = [cell.strip() for cell in line.split("|")]

            # Filter out empty cells that might result from splitting
            raw_cells = [cell for cell in raw_cells if cell.strip()]

            if len(raw_cells) >= 2:  # Must have at least 2 columns to be a valid table row
                # Convert each cell to the expected format with text and formatted fields
                formatted_cells = []
                for cell_content in raw_cells:
                    # Parse inline formatting in cell content
                    cell_segments = parse_cell_formatting(cell_content)
                    cell_data = {"text": cell_content, "formatted": cell_segments}
                    formatted_cells.append(cell_data)
                table_data["data"].append(formatted_cells)

    return table_data


def parse_cell_formatting(cell_content: str) -> List[Dict[str, Any]]:
    """Parse inline formatting in table cell content.

    Args:
        cell_content: Raw cell content string with markdown formatting

    Returns:
        List of formatted segments matching expected test format:
        [{"text": "segment", "format": {"bold": bool, "italic": bool, "underline": bool}}]
    """
    if not isinstance(cell_content, str) or not cell_content.strip():
        return [
            {
                "text": cell_content,
                "format": {"bold": False, "italic": False, "underline": False},
            }
        ]

    import re

    # Handle complex formatting patterns
    segments = []
    remaining_text = cell_content

    # Pattern for ***bold italic*** (3 asterisks on each side)
    bold_italic_pattern = r"\*\*\*([^*]+)\*\*\*"
    matches = list(re.finditer(bold_italic_pattern, remaining_text))

    if matches:
        last_end = 0
        for match in matches:
            # Add text before the match
            if match.start() > last_end:
                plain_text = remaining_text[last_end : match.start()]
                if plain_text:
                    segments.append(
                        {
                            "text": plain_text,
                            "format": {"bold": False, "italic": False, "underline": False},
                        }
                    )

            # Add the bold italic text
            segments.append(
                {
                    "text": match.group(1),
                    "format": {"bold": True, "italic": True, "underline": False},
                }
            )
            last_end = match.end()

        # Add remaining text
        if last_end < len(remaining_text):
            plain_text = remaining_text[last_end:]
            if plain_text:
                segments.append(
                    {
                        "text": plain_text,
                        "format": {"bold": False, "italic": False, "underline": False},
                    }
                )
        return segments

    # Pattern for ___underline___ (3 underscores on each side)
    underline_pattern = r"___([^_]+)___"
    matches = list(re.finditer(underline_pattern, remaining_text))

    if matches:
        last_end = 0
        for match in matches:
            # Add text before the match
            if match.start() > last_end:
                plain_text = remaining_text[last_end : match.start()]
                if plain_text:
                    segments.append(
                        {
                            "text": plain_text,
                            "format": {"bold": False, "italic": False, "underline": False},
                        }
                    )

            # Add the underlined text
            segments.append(
                {
                    "text": match.group(1),
                    "format": {"bold": False, "italic": False, "underline": True},
                }
            )
            last_end = match.end()

        # Add remaining text
        if last_end < len(remaining_text):
            plain_text = remaining_text[last_end:]
            if plain_text:
                segments.append(
                    {
                        "text": plain_text,
                        "format": {"bold": False, "italic": False, "underline": False},
                    }
                )
        return segments

    # Pattern for **bold** (2 asterisks on each side)
    bold_pattern = r"\*\*([^*]+)\*\*"
    matches = list(re.finditer(bold_pattern, remaining_text))

    if matches:
        last_end = 0
        for match in matches:
            # Add text before the match
            if match.start() > last_end:
                plain_text = remaining_text[last_end : match.start()]
                if plain_text:
                    segments.append(
                        {
                            "text": plain_text,
                            "format": {"bold": False, "italic": False, "underline": False},
                        }
                    )

            # Add the bold text
            segments.append(
                {
                    "text": match.group(1),
                    "format": {"bold": True, "italic": False, "underline": False},
                }
            )
            last_end = match.end()

        # Add remaining text
        if last_end < len(remaining_text):
            plain_text = remaining_text[last_end:]
            if plain_text:
                segments.append(
                    {
                        "text": plain_text,
                        "format": {"bold": False, "italic": False, "underline": False},
                    }
                )
        return segments

    # Pattern for *italic* (1 asterisk on each side)
    italic_pattern = r"\*([^*]+)\*"
    matches = list(re.finditer(italic_pattern, remaining_text))

    if matches:
        last_end = 0
        for match in matches:
            # Add text before the match
            if match.start() > last_end:
                plain_text = remaining_text[last_end : match.start()]
                if plain_text:
                    segments.append(
                        {
                            "text": plain_text,
                            "format": {"bold": False, "italic": False, "underline": False},
                        }
                    )

            # Add the italic text
            segments.append(
                {
                    "text": match.group(1),
                    "format": {"bold": False, "italic": True, "underline": False},
                }
            )
            last_end = match.end()

        # Add remaining text
        if last_end < len(remaining_text):
            plain_text = remaining_text[last_end:]
            if plain_text:
                segments.append(
                    {
                        "text": plain_text,
                        "format": {"bold": False, "italic": False, "underline": False},
                    }
                )
        return segments

    # No formatting found - return as plain text
    return [{"text": cell_content, "format": {"bold": False, "italic": False, "underline": False}}]