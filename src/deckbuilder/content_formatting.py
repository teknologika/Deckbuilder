#!/usr/bin/env python3
"""
Universal Content Formatting Module

Handles ALL formatting types independently of structure processing.
This module can be used by both JSON and Markdown processing without circular dependencies.

Supports:
- Inline formatting: **bold**, *italic*, ___underline___, ***bold italic***
- Rich content blocks: headings, paragraphs, bullets with levels
- Table cell formatting: maintaining structure while applying formatting
- Complex combinations: mixed formatting within same text

Separated from structure handling to enable clean architecture.
"""

import re
from typing import List, Dict, Any, Union


class ContentFormatter:
    """Universal content formatting processor."""

    def __init__(self):
        """Initialize the content formatter."""
        pass

    def parse_inline_formatting(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse inline formatting and return structured formatting data.

        Args:
            text: Text with inline formatting markers

        Returns:
            List of segments with text and formatting attributes
        """
        if not text:
            return [{"text": "", "format": {}}]

        # Patterns in order of precedence (longest patterns first to avoid conflicts)
        patterns = [
            (
                r"\*\*\*___(.*?)___\*\*\*",
                {"bold": True, "italic": True, "underline": True},
            ),  # ***___text___***
            (
                r"___\*\*\*(.*?)\*\*\*___",
                {"bold": True, "italic": True, "underline": True},
            ),  # ___***text***___
            (r"\*\*\*(.*?)\*\*\*", {"bold": True, "italic": True}),  # ***text***
            (r"___(.*?)___", {"underline": True}),  # ___text___
            (r"\*\*(.*?)\*\*", {"bold": True}),  # **text**
            (r"\*(.*?)\*", {"italic": True}),  # *text*
        ]

        # Find all matches and their positions
        all_matches = []
        for pattern, format_dict in patterns:
            for match in re.finditer(pattern, text):
                all_matches.append((match.start(), match.end(), match.group(1), format_dict))

        # Sort matches by position
        all_matches.sort(key=lambda x: x[0])

        # Remove overlapping matches (keep the first one found)
        filtered_matches = []
        last_end = 0
        for start, end, content, format_dict in all_matches:
            if start >= last_end:
                filtered_matches.append((start, end, content, format_dict))
                last_end = end

        # Build the formatted text segments
        segments = []
        last_pos = 0

        for start, end, content, format_dict in filtered_matches:
            # Add plain text before the formatted text
            if start > last_pos:
                plain_text = text[last_pos:start]
                if plain_text:
                    segments.append({"text": plain_text, "format": {}})

            # Add formatted text
            segments.append({"text": content, "format": format_dict})
            last_pos = end

        # Add any remaining plain text
        if last_pos < len(text):
            remaining_text = text[last_pos:]
            if remaining_text:
                segments.append({"text": remaining_text, "format": {}})

        # If no formatting found, return the original text
        if not segments:
            segments = [{"text": text, "format": {}}]

        return segments

    def format_simple_content_list(self, content_list: List[str]) -> List[Dict[str, Any]]:
        """
        Convert simple content list to rich content with formatting.

        Args:
            content_list: List of strings with possible inline formatting

        Returns:
            Rich content list with formatting preserved
        """
        if not content_list:
            return []

        rich_content = []
        for item in content_list:
            if isinstance(item, str):
                # Treat as paragraph text with inline formatting
                rich_content.append(
                    {"paragraph": item, "formatted": self.parse_inline_formatting(item)}
                )
            else:
                # Keep non-string items as-is
                rich_content.append(item)

        return rich_content

    def format_field_content(
        self, content: Union[str, List[str], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Format any field content type with inline formatting preservation.

        Args:
            content: Content to format (string, list, or dict)

        Returns:
            Formatted content with structure preserved
        """
        if isinstance(content, str):
            return {"text": content, "formatted": self.parse_inline_formatting(content)}
        elif isinstance(content, list):
            return {
                "list": content,
                "formatted_list": [
                    {
                        "text": item,
                        "formatted": (
                            self.parse_inline_formatting(item) if isinstance(item, str) else item
                        ),
                    }
                    for item in content
                ],
            }
        elif isinstance(content, dict):
            # Recursively format dict content
            formatted_dict = {}
            for key, value in content.items():
                if isinstance(value, str):
                    formatted_dict[key] = {
                        "text": value,
                        "formatted": self.parse_inline_formatting(value),
                    }
                else:
                    formatted_dict[key] = value
            return formatted_dict
        else:
            # Return non-string/list/dict content as-is
            return {"raw": content}

    def format_table_data(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format table data while preserving structure.

        Args:
            table_data: Table configuration with data

        Returns:
            Table data with formatting applied to cells
        """
        if not isinstance(table_data, dict) or "data" not in table_data:
            return table_data

        formatted_table = table_data.copy()

        if isinstance(table_data["data"], list):
            formatted_data = []
            for row in table_data["data"]:
                if isinstance(row, list):
                    formatted_row = []
                    for cell in row:
                        if isinstance(cell, str):
                            formatted_row.append(
                                {"text": cell, "formatted": self.parse_inline_formatting(cell)}
                            )
                        else:
                            # Keep non-string cells as-is
                            formatted_row.append(cell)
                    formatted_data.append(formatted_row)
                else:
                    # Keep non-list rows as-is
                    formatted_data.append(row)
            formatted_table["data"] = formatted_data

        return formatted_table

    def format_rich_content_blocks(
        self, rich_content: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Format rich content blocks (headings, paragraphs, bullets).

        Args:
            rich_content: List of rich content blocks

        Returns:
            Rich content with formatting applied
        """
        if not rich_content:
            return []

        formatted_blocks = []

        for block in rich_content:
            if not isinstance(block, dict):
                formatted_blocks.append(block)
                continue

            formatted_block = block.copy()

            # Format headings
            if "heading" in block:
                formatted_block["heading_formatted"] = self.parse_inline_formatting(
                    block["heading"]
                )

            # Format paragraphs
            if "paragraph" in block:
                formatted_block["paragraph_formatted"] = self.parse_inline_formatting(
                    block["paragraph"]
                )

            # Format bullets
            if "bullets" in block and isinstance(block["bullets"], list):
                formatted_bullets = []
                for bullet in block["bullets"]:
                    if isinstance(bullet, str):
                        formatted_bullets.append(
                            {"text": bullet, "formatted": self.parse_inline_formatting(bullet)}
                        )
                    else:
                        formatted_bullets.append(bullet)
                formatted_block["bullets_formatted"] = formatted_bullets

            formatted_blocks.append(formatted_block)

        return formatted_blocks

    def format_slide_data(self, slide_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format complete slide data with ALL formatting types preserved.

        This is the main entry point for slide formatting.

        Args:
            slide_data: Raw slide data dictionary

        Returns:
            Slide data with all formatting applied
        """
        if not isinstance(slide_data, dict):
            raise TypeError(f"slide_data must be a dictionary, got {type(slide_data).__name__}")

        # Create a copy to avoid modifying original
        formatted_data = slide_data.copy()

        # Format title and subtitle
        for field in ["title", "subtitle"]:
            if field in formatted_data and formatted_data[field]:
                formatted_data[f"{field}_formatted"] = self.parse_inline_formatting(
                    formatted_data[field]
                )

        # Format simple content lists to rich content
        if "content" in formatted_data and isinstance(formatted_data["content"], list):
            formatted_data["rich_content"] = self.format_simple_content_list(
                formatted_data["content"]
            )
            # Keep original for compatibility
            # del formatted_data["content"]

        # Format rich content blocks
        if "rich_content" in formatted_data:
            formatted_data["rich_content_formatted"] = self.format_rich_content_blocks(
                formatted_data["rich_content"]
            )

        # Format table data
        if "table" in formatted_data:
            formatted_data["table_formatted"] = self.format_table_data(formatted_data["table"])

        # Format all field content (for semantic field names like content_left, content_col1)
        content_fields = [
            key
            for key in formatted_data.keys()
            if key.startswith(("content_", "title_")) and not key.endswith("_formatted")
        ]

        for field in content_fields:
            content = formatted_data[field]
            if content:  # Only format non-empty content
                formatted_data[f"{field}_formatted"] = self.format_field_content(content)

        return formatted_data


# Global formatter instance
content_formatter = ContentFormatter()


def format_slide_content(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for formatting slide content.

    Args:
        slide_data: Raw slide data

    Returns:
        Formatted slide data
    """
    return content_formatter.format_slide_data(slide_data)


def format_inline_text(text: str) -> List[Dict[str, Any]]:
    """
    Convenience function for formatting inline text.

    Args:
        text: Text with inline formatting

    Returns:
        List of formatted segments
    """
    return content_formatter.parse_inline_formatting(text)
