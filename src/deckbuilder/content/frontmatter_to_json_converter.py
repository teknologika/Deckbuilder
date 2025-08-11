"""
Frontmatter to JSON Converter Module

Main frontmatter → canonical JSON transformation pipeline.
Handles the complete conversion from markdown with frontmatter to presentation slide data.

This module orchestrates the other specialized modules to create the final JSON structure.
"""

from typing import Dict, Any
from .table_parser import is_table_content
from .content_segmenter import split_mixed_content_intelligently
from .table_integration import extract_table_from_content, apply_frontmatter_styling_to_table, process_markdown_content


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
                    content_blocks.append(
                        {
                            "type": "heading",
                            "text": block["heading"],
                            "level": block.get("level", 2),
                        }
                    )
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
        table_properties = [
            "column_widths",
            "row_height",
            "table_width",
            "row_style",
            "border_style",
            "style",
        ]
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
                table_data = extract_table_from_content(content_field, slide_data)
            elif isinstance(table_data_field, str):
                # table_data field contains raw table markdown - parse it
                table_data = extract_table_from_content(table_data_field, slide_data)

            # Apply frontmatter styling properties to the table data
            if table_data:
                table_data = apply_frontmatter_styling_to_table(table_data, slide_data)

        # CRITICAL FIX: Make dynamic vs static paths MUTUALLY EXCLUSIVE
        # Check if content should use dynamic multi-shape creation
        should_use_dynamic_shapes = (
            table_data 
            and "content" in slide_data 
            and isinstance(slide_data["content"], str)
            and is_table_content(slide_data["content"])
        )

        if should_use_dynamic_shapes:
            # DYNAMIC MULTI-SHAPE PATH - Use this path EXCLUSIVELY
            content_text = slide_data["content"]
            content_segments = split_mixed_content_intelligently(content_text, table_data or {})

            if content_segments["segments"]:
                # Store content segments for dynamic shape creation by slide_builder
                slide_obj["_content_segments"] = content_segments["segments"]
                slide_obj["_requires_dynamic_shapes"] = True

                # Set first text segment as main content placeholder (if exists)
                first_text_segment = next((seg for seg in content_segments["segments"] if seg["type"] == "text"), None)
                if first_text_segment:
                    slide_obj["placeholders"]["content"] = first_text_segment["content"].strip()

                # DO NOT create separate table objects when using dynamic shapes
                # The dynamic system will handle table creation from segments
            else:
                # Fallback if splitting failed - use static path
                slide_obj["placeholders"]["content"] = table_data

        elif table_data:
            # STATIC TABLE PATH - Traditional table processing
            # Ensure table data has proper formatting (not just raw markdown strings)
            if "data" in table_data:
                formatted_data = []
                for row in table_data["data"]:
                    formatted_row = []
                    for cell in row:
                        if isinstance(cell, str):
                            # Parse markdown formatting in cell
                            from .formatter import content_formatter

                            formatted_segments = content_formatter.parse_inline_formatting(cell)
                            formatted_row.append({"text": cell, "formatted": formatted_segments})
                        else:
                            # Cell already formatted
                            formatted_row.append(cell)
                    formatted_data.append(formatted_row)
                table_data["data"] = formatted_data

            # Put table in placeholders.content for static processing
            slide_obj["placeholders"]["content"] = table_data

        # Add speaker_notes to slide level if present
        if "speaker_notes" in slide_data:
            slide_obj["speaker_notes"] = slide_data["speaker_notes"]

        # Add other placeholder fields from frontmatter (exclude internal fields and table properties)
        excluded_fields = [
            "type",
            "rich_content",
            "style",
            "layout",
            "title_formatted",
            "subtitle_formatted",
            "speaker_notes",  # Handle at slide level, not as placeholder
        ]

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
                        processed_value = process_markdown_content(value)
                        slide_obj["placeholders"][key] = processed_value
                    else:
                        slide_obj["placeholders"][key] = value

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}