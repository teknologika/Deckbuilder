from typing import Dict, Any, Optional


# Legacy alias for backward compatibility
class FrontmatterConverter:
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

    def _extract_table_markdown_from_content(self, content: str) -> str:
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

    def _split_mixed_content_intelligently(self, content: str, base_table_styling: dict) -> dict:
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
                    parsed_table = self._parse_markdown_table(table_markdown)

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
            parsed_table = self._parse_markdown_table(table_markdown)

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

    def _extract_all_tables_from_content(self, content: str) -> dict:
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
                    parsed_table = self._parse_markdown_table(table_markdown)

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
            parsed_table = self._parse_markdown_table(table_markdown)

            if parsed_table and parsed_table.get("data"):
                placeholder = f"[TABLE_PLACEHOLDER_{len(tables) + 1}]"
                tables.append({"markdown": table_markdown, "parsed_data": parsed_table["data"], "placeholder": placeholder})
                content_with_placeholders = content_with_placeholders.replace(table_markdown, placeholder)

        return {"content_with_placeholders": content_with_placeholders, "tables": tables}

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
    table_obj = {
        "data": table_data,
        "header_style": "dark_blue_white_text",
        "row_style": "alternating_light_gray",
        "border_style": "thin_gray",
        "custom_colors": {},
    }  # default  # default  # default

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

        # ENHANCED: Always use Pattern A - put table in placeholders.content, never separate table object
        if table_data:
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

            # ENHANCED: Dynamic Multi-Shape Content Splitting
            if "content" in slide_data and isinstance(slide_data["content"], str):
                content_text = slide_data["content"]
                converter = FrontmatterConverter()

                if converter._is_table_content(content_text):
                    # Split mixed content into typed segments for dynamic shape creation
                    content_segments = converter._split_mixed_content_intelligently(content_text, table_data)

                    if content_segments["segments"]:
                        # Store content segments for dynamic shape creation by slide_builder
                        slide_obj["_content_segments"] = content_segments["segments"]
                        slide_obj["_requires_dynamic_shapes"] = True

                        # Set first text segment as main content placeholder (if exists)
                        first_text_segment = next((seg for seg in content_segments["segments"] if seg["type"] == "text"), None)
                        if first_text_segment:
                            slide_obj["placeholders"]["content"] = first_text_segment["content"].strip()

                        # Add table objects for each table segment
                        table_count = 0
                        for segment in content_segments["segments"]:
                            if segment["type"] == "table":
                                table_key = "table" if table_count == 0 else f"table_{table_count + 1}"
                                # Merge styling with extracted table data
                                complete_table = {**table_data, **segment["table_data"]}
                                slide_obj[table_key] = complete_table
                                table_count += 1

                        slide_obj["_table_count"] = table_count
                    else:
                        # Fallback: put table directly in content if splitting failed
                        slide_obj["placeholders"]["content"] = table_data
                else:
                    # Content doesn't have table, use separate table object
                    slide_obj["table"] = table_data
            else:
                # No content field or not string, put table in placeholders.content
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
