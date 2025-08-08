from typing import Dict, Any, Optional

# Import structured frontmatter classes from content package
from .content.frontmatter import StructuredFrontmatterConverter


# Legacy alias for backward compatibility
class FrontmatterConverter(StructuredFrontmatterConverter):
    """Converter to be used in the new converter module"""

    pass


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
    from .content.processor import ContentProcessor

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
                    slide_obj["placeholders"][key] = value

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}
