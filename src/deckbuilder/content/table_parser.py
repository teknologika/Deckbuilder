"""
Table Parser Module

Pure table markdown parsing and formatting functionality.
Handles detection of table markdown, parsing table structure, and formatting table cells.

This module is focused on table parsing logic and has no dependencies on slide data or frontmatter.
"""

# Unused imports removed - basic Python types used instead


def is_table_content(content: str) -> bool:
    """
    Check if content contains table markdown.

    Args:
        content: Content string to check

    Returns:
        True if content contains table markdown
    """
    if not isinstance(content, str):
        return False

    # Basic table detection - look for lines with pipe characters
    lines = content.split("\n")
    table_lines = 0

    for line in lines:
        line = line.strip()
        if line and "|" in line:
            # Skip lines that are just separators (containing only |, -, :, =, spaces, tabs)
            if not all(c in "|-:=\t " for c in line):
                table_lines += 1
        elif line and table_lines > 0:
            # If we found table lines but now hit a non-empty non-table line,
            # this indicates mixed content
            pass

    return table_lines >= 2  # Need at least header + 1 data row


def extract_table_markdown(content: str) -> str:
    """
    Extract table markdown from mixed content.

    Args:
        content: Content that may contain table markdown

    Returns:
        Just the table markdown portion
    """
    if not isinstance(content, str):
        return ""

    lines = content.split("\n")
    table_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped and "|" in stripped:
            # This looks like a table line
            table_lines.append(line)
            in_table = True
        elif in_table and not stripped:
            # Empty line in table - might be spacing, include it
            table_lines.append(line)
        elif in_table:
            # Non-table line after table content - table is done
            break

    return "\n".join(table_lines)


def parse_markdown_table(content: str) -> dict:
    """
    Parse table markdown into structured data with formatting preservation.

    Args:
        content: Table markdown content

    Returns:
        Dictionary with structured table data including formatting
    """
    if not isinstance(content, str):
        return {"rows": [], "error": "Invalid content type"}

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    if not lines:
        return {"rows": [], "error": "No content provided"}

    # Table structure
    table_data = {
        "rows": [],
        "headers": [],
        "data": [],
        "row_count": 0,
        "column_count": 0,
    }

    # Extract table rows
    for _, line in enumerate(lines):
        # Skip separator lines (contain only dashes, pipes, colons, spaces, tabs, and equals)
        if all(c in "-|:=\t " for c in line.strip()):
            continue

        # Parse table row
        if "|" in line:
            # Split by pipes and clean up
            cells = [cell.strip() for cell in line.split("|")]
            # Remove empty cells from start/end (due to leading/trailing |)
            while cells and not cells[0]:
                cells.pop(0)
            while cells and not cells[-1]:
                cells.pop()

            if cells:  # Only add non-empty rows
                formatted_cells = []
                for cell_content in cells:
                    formatted_cell = {
                        "text": cell_content,
                        "formatted": parse_cell_formatting(cell_content),
                    }
                    formatted_cells.append(formatted_cell)

                table_data["rows"].append(formatted_cells)

    # Separate headers from data
    if table_data["rows"]:
        table_data["headers"] = table_data["rows"][0]
        table_data["data"] = table_data["rows"][1:] if len(table_data["rows"]) > 1 else []

    # Set dimensions
    table_data["row_count"] = len(table_data["rows"])
    table_data["column_count"] = len(table_data["rows"][0]) if table_data["rows"] else 0

    return table_data


def parse_cell_formatting(cell_content: str) -> list:
    """
    Parse cell content for inline formatting (bold, italic, underline).

    Args:
        cell_content: Raw cell content with markdown formatting

    Returns:
        List of formatted segments
    """
    if not isinstance(cell_content, str):
        return [{"text": str(cell_content), "format": {}}]

    # Handle basic markdown formatting
    formatted_segments = []
    current_text = cell_content

    # Process bold+italic first (***text***)
    import re

    bold_italic_pattern = r"\*\*\*([^*]+)\*\*\*"
    matches = list(re.finditer(bold_italic_pattern, current_text))

    if matches:
        last_end = 0
        for match in matches:
            # Add text before the match
            if match.start() > last_end:
                before_text = current_text[last_end : match.start()]
                if before_text.strip():
                    formatted_segments.extend(parse_simple_formatting(before_text))

            # Add the bold+italic text
            formatted_segments.append({"text": match.group(1), "format": {"bold": True, "italic": True}})
            last_end = match.end()

        # Add remaining text
        if last_end < len(current_text):
            remaining = current_text[last_end:]
            if remaining.strip():
                formatted_segments.extend(parse_simple_formatting(remaining))

        return formatted_segments

    # No complex formatting, use simple parsing
    return parse_simple_formatting(current_text)


def parse_simple_formatting(text: str) -> list:
    """Parse simple formatting (bold, italic, underline) from text."""
    import re

    # Handle underline (___text___)
    if "___" in text and text.count("___") >= 2:
        underline_pattern = r"___([^_]+)___"
        match = re.search(underline_pattern, text)
        if match:
            return [{"text": match.group(1), "format": {"underline": True}}]

    # Handle bold (**text**)
    if "**" in text and text.count("**") >= 2:
        bold_pattern = r"\*\*([^*]+)\*\*"
        match = re.search(bold_pattern, text)
        if match:
            return [{"text": match.group(1), "format": {"bold": True}}]

    # Handle italic (*text*)
    if "*" in text and text.count("*") >= 2:
        italic_pattern = r"\*([^*]+)\*"
        match = re.search(italic_pattern, text)
        if match:
            return [{"text": match.group(1), "format": {"italic": True}}]

    # No formatting
    return [{"text": text, "format": {}}]
