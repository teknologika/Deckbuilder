"""
Content Segmenter Module

Mixed content analysis and intelligent splitting for dynamic shape creation.
Handles detection of text + table + text patterns and creates typed content segments.

This module is focused on content boundary detection and segmentation logic.
"""

from typing import Dict, Any, List
from .table_parser import parse_markdown_table


def split_mixed_content_intelligently(content: str, base_table_styling: dict) -> dict:
    """
    Split mixed content (text + tables) into typed segments for dynamic shape creation.

    Args:
        content: Full content string that may contain mixed text and tables
        base_table_styling: Base styling configuration for tables

    Returns:
        Dictionary with:
        - segments: List of typed content segments (text or table)
        - has_mixed_content: Boolean indicating if content was actually mixed
    """
    if not isinstance(content, str):
        return {"segments": [], "has_mixed_content": False}

    lines = content.split("\n")
    segments = []
    current_text_block = []
    current_table = []
    table_start = -1
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check if this line starts or continues a table
        if "|" in line and not all(c in "|-:= \t" for c in line.strip()):
            # This is a table data row
            if table_start == -1:
                # Starting a new table - save any accumulated text first
                if current_text_block:
                    text_content = "\n".join(current_text_block).strip()
                    if text_content:
                        segments.append({"type": "text", "content": text_content})
                    current_text_block = []
                table_start = i
            current_table.append(lines[i])
        elif table_start != -1 and "|" in line and all(c in "|-:= \t" for c in line.replace("|", "").strip()):
            # This is a separator line within table
            current_table.append(lines[i])
        elif table_start != -1 and (line == "" or "|" not in line):
            # End of table found - process the table
            if current_table:
                table_markdown = "\n".join(current_table)
                parsed_table = parse_markdown_table(table_markdown)

                if parsed_table and parsed_table.get("data"):
                    # Apply base styling to parsed table
                    complete_table_data = {**base_table_styling, **parsed_table}
                    segments.append({"type": "table", "table_data": complete_table_data, "markdown": table_markdown})

            # Reset for next content
            current_table = []
            table_start = -1

            # Start accumulating text again (if this line has content)
            if line:
                current_text_block.append(lines[i])
        elif table_start == -1:
            # Regular content line, not in a table
            current_text_block.append(lines[i])

        i += 1

    # Handle case where table is at the end of content
    if current_table and table_start != -1:
        table_markdown = "\n".join(current_table)
        parsed_table = parse_markdown_table(table_markdown)

        if parsed_table and parsed_table.get("data"):
            complete_table_data = {**base_table_styling, **parsed_table}
            segments.append({"type": "table", "table_data": complete_table_data, "markdown": table_markdown})

    # Handle any remaining text
    if current_text_block:
        text_content = "\n".join(current_text_block).strip()
        if text_content:
            segments.append({"type": "text", "content": text_content})

    # Determine if we actually have mixed content (text + table combination)
    has_mixed_content = len([s for s in segments if s["type"] == "text"]) > 0 and len([s for s in segments if s["type"] == "table"]) > 0

    return {"segments": segments, "has_mixed_content": has_mixed_content}


def extract_all_tables_from_content(content: str) -> Dict[str, Any]:
    """
    Extract ALL tables from content, replace with numbered placeholders, preserve surrounding text.

    Args:
        content: Full content string that may contain multiple tables + other text

    Returns:
        Dictionary with:
        - content_with_placeholders: Content with [TABLE_PLACEHOLDER_1], [TABLE_PLACEHOLDER_2], etc.
        - tables: List of table info dicts with markdown and parsed data
    """
    if not isinstance(content, str):
        return {"content_with_placeholders": content, "tables": []}

    lines = content.split("\n")
    tables = []
    content_with_placeholders = content

    current_table = []
    table_start = -1
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check if this line starts or continues a table
        if "|" in line and not all(c in "|-:= \t" for c in line.strip()):
            # This is a table data row
            if table_start == -1:
                table_start = i
            current_table.append(lines[i])
        elif table_start != -1 and "|" in line and all(c in "|-:= \t" for c in line.replace("|", "").strip()):
            # This is a separator line within table
            current_table.append(lines[i])
        elif table_start != -1 and (line == "" or "|" not in line):
            # End of table found
            if current_table:
                table_markdown = "\n".join(current_table)
                parsed_table = parse_markdown_table(table_markdown)

                if parsed_table and parsed_table.get("data"):
                    placeholder = f"[TABLE_PLACEHOLDER_{len(tables) + 1}]"
                    tables.append({"markdown": table_markdown, "parsed_data": parsed_table["data"], "placeholder": placeholder})

                    # Replace table markdown with placeholder in content
                    content_with_placeholders = content_with_placeholders.replace(table_markdown, placeholder)

            # Reset for next table
            current_table = []
            table_start = -1
        elif table_start == -1:
            # Regular content line, not in a table
            pass

        i += 1

    # Handle case where table is at the end of content
    if current_table and table_start != -1:
        table_markdown = "\n".join(current_table)
        parsed_table = parse_markdown_table(table_markdown)

        if parsed_table and parsed_table.get("data"):
            placeholder = f"[TABLE_PLACEHOLDER_{len(tables) + 1}]"
            tables.append({"markdown": table_markdown, "parsed_data": parsed_table["data"], "placeholder": placeholder})
            content_with_placeholders = content_with_placeholders.replace(table_markdown, placeholder)

    return {"content_with_placeholders": content_with_placeholders, "tables": tables}