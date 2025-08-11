"""
Content Segmenter Module

Mixed content analysis and intelligent splitting for dynamic shape creation.
Handles detection of text + table + text patterns and creates typed content segments.

This module is focused on content boundary detection and segmentation logic.
"""

# from typing import Dict, Any  # Unused imports removed
from .table_parser import parse_markdown_table


def split_mixed_content_intelligently(content: str, base_table_styling: dict) -> dict:
    """
    Split mixed content (text + tables) into typed segments for dynamic shape creation.

    Args:
        content: Full content string that may contain mixed text and tables
        base_table_styling: Base styling configuration for tables

    Returns:
        Dictionary containing:
        - segments: List of typed content segments (text/table)
        - has_mixed_content: Boolean indicating if mixed content was found
    """
    if not isinstance(content, str):
        return {"segments": [], "has_mixed_content": False}

    # Detect table boundaries and split content
    lines = content.split("\n")
    segments = []
    current_text = []
    current_table_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Check if this line looks like a table line
        if stripped and "|" in stripped and not all(c in "|-:=\t " for c in stripped):
            # This is a table content line
            if not in_table:
                # Starting a new table - save any preceding text
                if current_text:
                    text_content = "\n".join(current_text).strip()
                    if text_content:
                        segments.append({"type": "text", "content": text_content})
                    current_text = []
                in_table = True

            current_table_lines.append(line)

        elif stripped and all(c in "|-:=\t " for c in stripped) and in_table:
            # Table separator line - include in table
            current_table_lines.append(line)

        else:
            # Non-table line
            if in_table:
                # End of table - process the table we've collected
                if current_table_lines:
                    table_content = "\n".join(current_table_lines)
                    table_data = parse_markdown_table(table_content)

                    # Add table styling from base configuration
                    table_data.update(base_table_styling)

                    segments.append({"type": "table", "table_data": table_data, "raw_content": table_content})
                    current_table_lines = []
                in_table = False

            # Add this line to current text
            current_text.append(line)

    # Handle any remaining content
    if in_table and current_table_lines:
        # Content ended with a table
        table_content = "\n".join(current_table_lines)
        table_data = parse_markdown_table(table_content)
        table_data.update(base_table_styling)

        segments.append({"type": "table", "table_data": table_data, "raw_content": table_content})
    elif current_text:
        # Content ended with text
        text_content = "\n".join(current_text).strip()
        if text_content:
            segments.append({"type": "text", "content": text_content})

    # Determine if this is truly mixed content
    text_segments = len([s for s in segments if s["type"] == "text"])
    table_segments = len([s for s in segments if s["type"] == "table"])
    has_mixed_content = (text_segments > 0 and table_segments > 0) or table_segments > 1

    return {"segments": segments, "has_mixed_content": has_mixed_content}


def extract_all_tables_from_content(content: str) -> dict:
    """
    Extract all tables from content and replace with placeholders.

    Args:
        content: Content string that may contain multiple tables

    Returns:
        Dictionary with modified content and extracted tables
    """
    if not isinstance(content, str):
        return {"content": content, "tables": []}

    # Split content into segments to identify all tables
    segments = split_mixed_content_intelligently(content, {})["segments"]

    tables = []
    modified_content = ""
    table_count = 0

    for segment in segments:
        if segment["type"] == "text":
            modified_content += segment["content"]
        elif segment["type"] == "table":
            # Replace table with placeholder
            table_count += 1
            table_placeholder = f"{{{{TABLE_{table_count}}}}}"
            modified_content += table_placeholder

            # Store table data
            tables.append({"placeholder": table_placeholder, "table_data": segment["table_data"], "raw_content": segment.get("raw_content", "")})

    return {"content": modified_content.strip(), "tables": tables, "table_count": len(tables)}
