from typing import Dict, Any, Optional

# Import structured frontmatter classes from content package
from .frontmatter import StructuredFrontmatterConverter


# Legacy alias for backward compatibility
class FrontmatterConverter(StructuredFrontmatterConverter):
    """Converter to be used in the new converter module"""

    def _process_content_field(self, content: str) -> str:
        """Process content field for basic formatting and return as-is for now."""
        if not isinstance(content, str):
            return str(content) if content is not None else ""
        return content.strip()

    def _is_table_content(self, content: str) -> bool:
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

    def _parse_markdown_table(self, content: str) -> dict:
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
                        cell_segments = self._parse_cell_formatting(cell_content)
                        cell_data = {"text": cell_content, "formatted": cell_segments}
                        formatted_cells.append(cell_data)
                    table_data["data"].append(formatted_cells)

        return table_data

    def _parse_cell_formatting(self, cell_content: str) -> list:
        """Parse inline formatting in table cell content.

        Args:
            cell_content: Raw cell content string with markdown formatting

        Returns:
            List of formatted segments matching expected test format:
            [{"text": "segment", "format": {"bold": bool, "italic": bool, "underline": bool}}]
        """
        if not isinstance(cell_content, str) or not cell_content.strip():
            return [{"text": cell_content, "format": {"bold": False, "italic": False, "underline": False}}]

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
                        segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})

                # Add the bold italic text
                segments.append({"text": match.group(1), "format": {"bold": True, "italic": True, "underline": False}})
                last_end = match.end()

            # Add remaining text
            if last_end < len(remaining_text):
                plain_text = remaining_text[last_end:]
                if plain_text:
                    segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})
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
                        segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})

                # Add the underlined text
                segments.append({"text": match.group(1), "format": {"bold": False, "italic": False, "underline": True}})
                last_end = match.end()

            # Add remaining text
            if last_end < len(remaining_text):
                plain_text = remaining_text[last_end:]
                if plain_text:
                    segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})
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
                        segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})

                # Add the bold text
                segments.append({"text": match.group(1), "format": {"bold": True, "italic": False, "underline": False}})
                last_end = match.end()

            # Add remaining text
            if last_end < len(remaining_text):
                plain_text = remaining_text[last_end:]
                if plain_text:
                    segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})
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
                        segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})

                # Add the italic text
                segments.append({"text": match.group(1), "format": {"bold": False, "italic": True, "underline": False}})
                last_end = match.end()

            # Add remaining text
            if last_end < len(remaining_text):
                plain_text = remaining_text[last_end:]
                if plain_text:
                    segments.append({"text": plain_text, "format": {"bold": False, "italic": False, "underline": False}})
            return segments

        # No formatting found - return as plain text
        return [{"text": cell_content, "format": {"bold": False, "italic": False, "underline": False}}]


def _extract_table_from_content(content: str, slide_data: dict) -> Optional[dict]:
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
    table_obj = {"data": table_data, "header_style": "dark_blue_white_text", "row_style": "alternating_light_gray", "border_style": "thin_gray", "custom_colors": {}}  # default  # default  # default

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


def markdown_to_canonical_json(markdown_content: str) -> Dict[str, Any]:
    """
    Converts a Markdown string with frontmatter into the canonical JSON presentation model.
    This will be the single entry point for all .md files.

    Handles both pure structured frontmatter and frontmatter + content pairs.
    """
    # Import ContentProcessor to handle frontmatter + content parsing
    from .processor import ContentProcessor

    # Use ContentProcessor to properly parse frontmatter + content
    processor = ContentProcessor()
    slides = processor.parse_markdown_with_frontmatter(markdown_content)

    canonical_slides = []

    for slide_data in slides:
        # Convert slide data to canonical format
        slide_layout = slide_data.get("type") or slide_data.get("layout", "Title and Content")

        # Create canonical slide structure
        slide_obj = {
            "layout": slide_layout,
            "style": slide_data.get("style", "default_style"),
            "placeholders": {},
            "content": [],
        }

        # Add title if present
        if "title" in slide_data:
            slide_obj["placeholders"]["title"] = slide_data["title"]

        # Add subtitle if present
        if "subtitle" in slide_data:
            slide_obj["placeholders"]["subtitle"] = slide_data["subtitle"]

        # Convert rich content to canonical format and put it in placeholders
        if "rich_content" in slide_data:
            content_blocks = []
            for block in slide_data["rich_content"]:
                if "heading" in block:
                    content_blocks.append({"type": "heading", "text": block["heading"], "level": block.get("level", 2)})
                elif "paragraph" in block:
                    content_blocks.append({"type": "paragraph", "text": block["paragraph"]})
                elif "bullets" in block:
                    bullet_items = []
                    bullets = block["bullets"]
                    bullet_levels = block.get("bullet_levels", [1] * len(bullets))
                    for bullet, level in zip(bullets, bullet_levels):
                        bullet_items.append({"text": bullet, "level": level})
                    content_blocks.append({"type": "bullets", "items": bullet_items})

            if content_blocks:
                # Put content blocks in the placeholders so slide builder can find them
                slide_obj["placeholders"]["content"] = content_blocks

        # Check for table-related frontmatter properties to determine table handling
        table_properties = ["column_widths", "row_height", "table_width", "row_style", "border_style", "style"]
        has_table_properties = any(key in slide_data for key in table_properties) or "table_data" in slide_data

        # Check if we need to create a table object from content or table_data field
        content_field = slide_data.get("content")
        table_data_field = slide_data.get("table_data")
        table_data = None

        if has_table_properties and (content_field or table_data_field):
            # When table properties exist, we need to create a table object
            if isinstance(content_field, dict) and content_field.get("type") == "table":
                # Content field is already a parsed table structure
                table_data = content_field.copy()
            elif isinstance(content_field, str):
                # Content field is raw text containing table markdown - parse it
                table_data = _extract_table_from_content(content_field, slide_data)
            elif isinstance(table_data_field, str):
                # table_data field contains raw table markdown - parse it
                table_data = _extract_table_from_content(table_data_field, slide_data)

            # Apply frontmatter styling properties to the table data
            if table_data:
                if "style" in slide_data:
                    table_data["header_style"] = slide_data["style"]
                if "row_style" in slide_data:
                    table_data["row_style"] = slide_data["row_style"]
                if "border_style" in slide_data:
                    table_data["border_style"] = slide_data["border_style"]

                # Apply dimension properties
                if "column_widths" in slide_data:
                    table_data["column_widths"] = slide_data["column_widths"]
                if "row_height" in slide_data:
                    table_data["row_height"] = slide_data["row_height"]
                if "table_width" in slide_data:
                    table_data["table_width"] = slide_data["table_width"]

        # Add table object to slide if table data was found
        if table_data:
            slide_obj["table"] = table_data

        # Add other placeholder fields from frontmatter (exclude internal fields and table properties)
        excluded_fields = ["type", "rich_content", "style", "layout", "title_formatted", "subtitle_formatted"]

        # Also exclude table properties from placeholders since they go in the table object
        if has_table_properties:
            excluded_fields.extend(table_properties)

        # NOTE: We do NOT exclude "content" field here anymore to maintain compatibility
        # The content field should go in placeholders.content even when table exists
        # This ensures markdown and JSON processing produce identical placeholder content

        for key, value in slide_data.items():
            if key not in excluded_fields:
                # Don't duplicate title and subtitle since they're already handled above
                if key not in ["title", "subtitle"] or key not in slide_obj["placeholders"]:
                    # Apply markdown formatting to content fields (content, content_left, content_right, etc.)
                    if key.startswith("content") and isinstance(value, str):
                        processed_value = _process_markdown_content(value)
                        slide_obj["placeholders"][key] = processed_value
                    else:
                        slide_obj["placeholders"][key] = value

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}


def _process_markdown_content(content: str):
    """Process markdown content to convert dash bullets to bullet symbols and detect tables"""
    if not isinstance(content, str):
        return content

    # First check if this content contains a table
    converter = FrontmatterConverter()
    if converter._is_table_content(content):
        # Convert to table object
        return converter._parse_markdown_table(content)

    # Convert dash bullets to bullet symbols
    # Match lines that start with "- " (dash followed by space)
    import re

    processed = re.sub(r"^- ", "• ", content, flags=re.MULTILINE)
    return processed
