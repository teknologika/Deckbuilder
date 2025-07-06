import os
import re

try:
    from .formatting_support import FormattingSupport, get_default_language, get_default_font
except ImportError:
    # Fallback if formatting support is not available
    class FormattingSupport:
        def apply_language_to_run(self, run, language_code):
            return False

        def apply_font_to_run(self, run, font_name):
            return False

    def get_default_language():
        return None

    def get_default_font():
        return None


class ContentFormatter:
    """Handles text formatting, rich content processing, and inline formatting."""

    def __init__(self):
        """Initialize the content formatter."""
        # Initialize formatting support
        self.formatting_support = FormattingSupport()
        self.default_language = get_default_language()
        self.default_font = get_default_font()

    def add_simple_content_to_placeholder(self, placeholder, content):
        """Add content to a placeholder with support for rich content blocks and formatted lists."""
        if not hasattr(placeholder, "text_frame"):
            return

        text_frame = placeholder.text_frame
        text_frame.clear()

        # Debug logging to track content processing pipeline decisions
        content_type = type(content).__name__
        self._debug_log(f"Processing content type: {content_type}")

        # Priority 1: Check for rich content blocks (from content_formatting.py)
        if isinstance(content, dict):
            # Check for formatted content with rich content blocks first
            if "rich_content_blocks" in content:
                self._debug_log("Processing rich content blocks from content_formatting")
                self._add_rich_content_blocks_to_placeholder(
                    text_frame, content["rich_content_blocks"]
                )
                return
            elif "formatted_list" in content:
                self._debug_log("Processing formatted_list from content_formatting")
                # This case means content is a dict like {'formatted_list': [...]}
                # We need to pass the list itself to the handler
                self._add_rich_content_list_to_placeholder(text_frame, content["formatted_list"])
                return
            elif any(key in content for key in ["heading", "paragraph", "bullets"]):
                self._debug_log("Processing direct rich content structure (single block)")
                # Wrap single rich content block in a list for consistent handling
                self._add_rich_content_list_to_placeholder(text_frame, [content])
                return
            elif "text" in content and "formatted" in content:
                self._debug_log("Processing formatted content segments (single text field)")
                formatted_segments = content["formatted"]
                p = text_frame.paragraphs[0]
                self.apply_formatted_segments_to_paragraph(formatted_segments, p)
                return
            else:
                # Fallback for other dict types - avoid string conversion if possible
                self._debug_log(
                    f"Unknown dict content structure, attempting text extraction: {list(content.keys())}"
                )
                p = text_frame.paragraphs[0]
                if "text" in content:
                    self.apply_inline_formatting(content["text"], p)
                else:
                    p.text = str(content)  # Final fallback to string conversion
                return

        # Priority 2: Check for list of content (can be rich content blocks or simple strings)
        elif isinstance(content, list):
            if content and isinstance(content[0], dict):
                # Check if this is a list of formatted segments (e.g., from parse_inline_formatting)
                if "text" in content[0] and "format" in content[0]:
                    self._debug_log("Processing list of formatted segments")
                    p = text_frame.paragraphs[0]
                    self.apply_formatted_segments_to_paragraph(content, p)
                    return
                # Check if this is a list of rich content blocks
                elif any(key in content[0] for key in ["heading", "paragraph", "bullets"]):
                    self._debug_log("Processing list of rich content blocks")
                    self._add_rich_content_list_to_placeholder(text_frame, content)
                    return
                else:
                    # Other dict list - treat as rich content list for now
                    self._debug_log("Processing dict list as rich content (general)")
                    self._add_rich_content_list_to_placeholder(text_frame, content)
                    return
            else:
                # Handle list of simple strings
                self._debug_log("Processing simple string list")
                self._add_rich_content_list_to_placeholder(text_frame, content)
                return

        # Priority 3: Handle plain text strings
        elif isinstance(content, str):
            self._debug_log("Processing plain text string")
            p = text_frame.paragraphs[0]
            self.apply_inline_formatting(content, p)
            return

        # Fallback for unexpected content types
        else:
            self._debug_log(f"Fallback: Converting {content_type} to string")
            p = text_frame.paragraphs[0]
            p.text = str(content)

    def _debug_log(self, message):
        """Debug logging for content processing pipeline"""
        # Only log if debug environment variable is set
        if os.getenv("DECKBUILDER_DEBUG"):
            print(f"[DECKBUILDER DEBUG] {message}")

    def _add_rich_content_list_to_placeholder(self, text_frame, content_list):
        """Add list content with proper formatting and bullet support."""
        paragraph_added = False

        for item in content_list:
            if isinstance(item, str):
                # Simple string item - apply inline formatting
                if not paragraph_added:
                    p = text_frame.paragraphs[0]
                    paragraph_added = True
                else:
                    p = text_frame.add_paragraph()
                self.apply_inline_formatting(item, p)

            elif isinstance(item, dict):
                # Check if this is a rich content block (heading, paragraph, bullets)
                if any(key in item for key in ["heading", "paragraph", "bullets"]):
                    self._debug_log(f"Processing rich content block in list: {list(item.keys())}")
                    # Process as rich content block using the specialized handler
                    self._add_single_rich_content_block_to_placeholder(
                        text_frame, item, paragraph_added
                    )
                    paragraph_added = True
                elif "text" in item:
                    # Simple text item
                    if not paragraph_added:
                        p = text_frame.paragraphs[0]
                        paragraph_added = True
                    else:
                        p = text_frame.add_paragraph()
                    self.apply_inline_formatting(item["text"], p)
                elif "formatted" in item:
                    # Apply formatted content segments
                    if not paragraph_added:
                        p = text_frame.paragraphs[0]
                        paragraph_added = True
                    else:
                        p = text_frame.add_paragraph()
                    self.apply_formatted_segments_to_paragraph(item["formatted"], p)
                else:
                    # Unknown dict structure - extract text if possible
                    self._debug_log(f"Unknown dict in list, keys: {list(item.keys())}")
                    if not paragraph_added:
                        p = text_frame.paragraphs[0]
                        paragraph_added = True
                    else:
                        p = text_frame.add_paragraph()
                    # Try to find any text content to avoid string conversion
                    text_content = item.get("text", str(item))
                    self.apply_inline_formatting(text_content, p)

    def _add_single_rich_content_block_to_placeholder(
        self, text_frame, content_block, paragraph_added
    ):
        """Add a single rich content block (heading, paragraph, or bullets) to placeholder."""
        # Handle heading
        if "heading" in content_block:
            p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
            heading_text = content_block["heading"]
            self.apply_inline_formatting(heading_text, p)
            # Make heading bold by default
            for run in p.runs:
                run.font.bold = True
            self._debug_log(f"Added heading: '{heading_text}'")

        # Handle paragraph
        if "paragraph" in content_block:
            p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
            paragraph_text = content_block["paragraph"]
            self.apply_inline_formatting(paragraph_text, p)
            self._debug_log(f"Added paragraph: '{paragraph_text[:50]}...'")

        # Handle bullets with proper level support
        if "bullets" in content_block and isinstance(content_block["bullets"], list):
            bullet_levels = content_block.get("bullet_levels", [])
            for i, bullet_text in enumerate(content_block["bullets"]):
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                self.apply_inline_formatting(bullet_text, p)

                # Set bullet level from bullet_levels array or default to level 1
                if i < len(bullet_levels):
                    # Convert level (1-based) to PowerPoint level (0-based)
                    p.level = max(0, bullet_levels[i] - 1)
                else:
                    p.level = 0  # Default to top level bullets

                self._debug_log(f"Added bullet: '{bullet_text}' at level {p.level}")
                paragraph_added = True

    def _add_rich_content_blocks_to_placeholder(self, text_frame, content_dict):
        """Add rich content blocks (headings, paragraphs, bullets) to placeholder."""
        # Check if this is formatted content from content_formatting.py
        if "formatted_list" in content_dict:
            # Handle formatted list content
            formatted_list = content_dict["formatted_list"]
            for i, item in enumerate(formatted_list):
                if i == 0:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()

                if "text" in item and "formatted" in item:
                    # Apply formatted segments
                    self.apply_formatted_segments_to_paragraph(item["formatted"], p)
                else:
                    # Fallback to text
                    text = item.get("text", str(item))
                    self.apply_inline_formatting(text, p)
        elif "text" in content_dict and "formatted" in content_dict:
            # Handle single formatted field content like {'text': '...', 'formatted': [...]}
            p = text_frame.paragraphs[0]
            formatted_segments = content_dict["formatted"]
            self.apply_formatted_segments_to_paragraph(formatted_segments, p)
        else:
            # Handle direct rich content blocks
            paragraph_added = False

            # Handle heading
            if "heading" in content_dict:
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                heading_text = content_dict["heading"]
                self.apply_inline_formatting(heading_text, p)
                # Make heading bold by default
                for run in p.runs:
                    run.font.bold = True
                paragraph_added = True

            # Handle paragraph
            if "paragraph" in content_dict:
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                paragraph_text = content_dict["paragraph"]
                self.apply_inline_formatting(paragraph_text, p)
                paragraph_added = True

            # Handle bullets with proper level support
            if "bullets" in content_dict and isinstance(content_dict["bullets"], list):
                bullet_levels = content_dict.get("bullet_levels", [])
                for i, bullet_text in enumerate(content_dict["bullets"]):
                    p = (
                        text_frame.paragraphs[0]
                        if not paragraph_added
                        else text_frame.add_paragraph()
                    )
                    self.apply_inline_formatting(bullet_text, p)

                    # Set bullet level from bullet_levels array or default to level 1
                    if i < len(bullet_levels):
                        # Convert level (1-based) to PowerPoint level (0-based)
                        p.level = max(0, bullet_levels[i] - 1)
                    else:
                        p.level = 0  # Default to top level bullets

                    self._debug_log(f"Added bullet: '{bullet_text}' at level {p.level}")
                    paragraph_added = True

    def apply_formatted_segments_to_paragraph(self, formatted_segments, paragraph):
        """Apply formatted text segments to a paragraph."""
        if not formatted_segments:
            return

        # Clear existing runs
        paragraph.clear()

        for segment in formatted_segments:
            if isinstance(segment, dict) and "text" in segment:
                text = segment["text"]
                format_info = segment.get("format", {})

                run = paragraph.add_run()
                run.text = text

                # Apply formatting
                if format_info.get("bold"):
                    run.font.bold = True
                if format_info.get("italic"):
                    run.font.italic = True
                if format_info.get("underline"):
                    run.font.underline = True

    def parse_inline_formatting(self, text):
        """Parse inline formatting and return structured formatting data"""
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

    def apply_inline_formatting(self, text, paragraph):
        """Apply inline formatting to paragraph using parsed formatting data."""
        # Clear any existing text
        paragraph.text = ""

        # Parse the formatting
        segments = self.parse_inline_formatting(text)

        # Apply each segment to the paragraph
        for segment in segments:
            run = paragraph.add_run()
            run.text = segment["text"]

            # Apply formatting
            format_dict = segment["format"]
            if format_dict.get("bold"):
                run.font.bold = True
            if format_dict.get("italic"):
                run.font.italic = True
            if format_dict.get("underline"):
                run.font.underline = True

            # Apply default language and font settings
            if self.default_language:
                self.formatting_support.apply_language_to_run(run, self.default_language)
            if self.default_font:
                self.formatting_support.apply_font_to_run(run, self.default_font)

    def apply_formatted_segments_to_shape(self, shape, segments):
        """Apply formatted text segments to a shape's text frame."""
        if not hasattr(shape, "text_frame"):
            # For shapes that don't have text_frame, fall back to simple text
            shape.text = "".join(segment["text"] for segment in segments)
            return

        text_frame = shape.text_frame
        text_frame.clear()

        # Use the first paragraph or create one
        if text_frame.paragraphs:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()

        paragraph.text = ""

        # Apply each segment
        for segment in segments:
            run = paragraph.add_run()
            run.text = segment["text"]

            # Apply formatting
            format_dict = segment["format"]
            if format_dict.get("bold"):
                run.font.bold = True
            if format_dict.get("italic"):
                run.font.italic = True
            if format_dict.get("underline"):
                run.font.underline = True

    def apply_formatted_segments_to_cell(self, cell, segments):
        """Apply formatted text segments to a table cell."""
        text_frame = cell.text_frame
        text_frame.clear()

        # Create first paragraph
        paragraph = text_frame.paragraphs[0]
        paragraph.text = ""

        # Apply each segment
        for segment in segments:
            run = paragraph.add_run()
            run.text = segment["text"]

            # Apply formatting
            format_dict = segment["format"]
            if format_dict.get("bold"):
                run.font.bold = True
            if format_dict.get("italic"):
                run.font.italic = True
            if format_dict.get("underline"):
                run.font.underline = True

    def add_rich_content_to_slide(self, slide, rich_content: list):
        """DEPRECATED: Use add_content_to_slide instead"""
        print(
            "Warning: add_rich_content_to_slide is deprecated, using unified add_content_to_slide"
        )

        # Convert legacy rich content format to canonical format
        canonical_content = []
        for block in rich_content:
            if isinstance(block, dict):
                if "heading" in block:
                    canonical_content.append(
                        {
                            "type": "heading",
                            "text": block["heading"],
                            "level": block.get("level", 2),
                        }
                    )
                elif "paragraph" in block:
                    canonical_content.append({"type": "paragraph", "text": block["paragraph"]})
                elif "bullets" in block:
                    # Convert bullets format
                    items = []
                    bullets = block["bullets"]
                    bullet_levels = block.get("bullet_levels", [1] * len(bullets))

                    for bullet, level in zip(bullets, bullet_levels):
                        items.append({"text": bullet, "level": level})

                    canonical_content.append({"type": "bullets", "items": items})

        self.add_content_to_slide(slide, canonical_content)

    def add_content_to_slide(self, slide, content):
        """
        Unified content processing for canonical JSON content blocks only.

        Uses semantic placeholder detection instead of hardcoded indices.
        Expects all content to be in canonical JSON format: [{"type": "...", "text": "..."}, ...]
        """
        from .placeholder_types import is_content_placeholder

        print(f"🔧 DEBUG: add_content_to_slide called with content type: {type(content)}")
        print(f"🔧 DEBUG: content: {content}")

        # Find content placeholders using semantic detection
        content_placeholders = []
        for shape in slide.placeholders:
            placeholder_type = shape.placeholder_format.type
            print(
                f"🔧 DEBUG: Found placeholder - idx: {shape.placeholder_format.idx}, type: {placeholder_type}, is_content: {is_content_placeholder(placeholder_type)}"
            )
            if is_content_placeholder(placeholder_type):
                # Skip if converted to image placeholder
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    content_placeholders.append(shape)
                    print(
                        f"🔧 DEBUG: Added content placeholder idx {shape.placeholder_format.idx} to processing list"
                    )

        print(f"🔧 DEBUG: Found {len(content_placeholders)} content placeholders")

        if not content_placeholders:
            print("Warning: No content placeholders found in slide")
            # For slides without content placeholders (e.g., Title Slide), try to use other placeholder types
            from .placeholder_types import is_subtitle_placeholder

            subtitle_placeholders = []
            for shape in slide.placeholders:
                if is_subtitle_placeholder(shape.placeholder_format.type):
                    if hasattr(shape, "text_frame") and shape.text_frame is not None:
                        # Check if subtitle placeholder already has content (from explicit subtitle field)
                        has_existing_content = False
                        if hasattr(shape, "text_frame") and shape.text_frame.paragraphs:
                            for paragraph in shape.text_frame.paragraphs:
                                if paragraph.text.strip():
                                    has_existing_content = True
                                    break

                        if not has_existing_content:
                            subtitle_placeholders.append(shape)
                            print(
                                f"🔧 DEBUG: Found empty subtitle placeholder idx {shape.placeholder_format.idx} as fallback"
                            )
                        else:
                            print(
                                f"🔧 DEBUG: Subtitle placeholder idx {shape.placeholder_format.idx} already has content, skipping"
                            )

            if subtitle_placeholders:
                print("🔧 DEBUG: Using subtitle placeholder as fallback for content")
                content_placeholders = subtitle_placeholders
            else:
                print("Warning: No suitable placeholders found for content")
                return

        # Expect only canonical JSON content blocks
        if isinstance(content, list) and content:
            # Validate all items are canonical JSON blocks
            for i, item in enumerate(content):
                if not isinstance(item, dict) or "type" not in item:
                    raise ValueError(
                        f"Content item {i} must be canonical JSON block with 'type' field. Got: {item}"
                    )

            print("🔧 DEBUG: Processing canonical JSON content blocks")
            self._process_canonical_content_blocks(content_placeholders, content)
        else:
            print(f"Warning: Expected list of canonical JSON content blocks, got: {type(content)}")

    def _process_canonical_content_blocks(self, content_placeholders, content_blocks):
        """Process canonical JSON content blocks like {"type": "paragraph", "text": "..."}"""
        print(
            f"🔧 DEBUG: _process_canonical_content_blocks called with {len(content_blocks)} blocks"
        )

        # Use first content placeholder for now
        # TODO: Support multi-placeholder layouts (Two Content, Four Columns)
        placeholder = content_placeholders[0]
        text_frame = placeholder.text_frame
        text_frame.clear()

        print(f"🔧 DEBUG: Using placeholder idx {placeholder.placeholder_format.idx} for content")

        first_block = True
        for i, block in enumerate(content_blocks):
            block_type = block.get("type", "")
            print(f"🔧 DEBUG: Processing block {i}: type={block_type}, block={block}")

            if block_type == "paragraph":
                if first_block:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()
                text_content = block.get("text", "")
                print(f"🔧 DEBUG: Adding paragraph text: '{text_content}'")
                self.apply_inline_formatting(text_content, p)

            elif block_type == "heading":
                if first_block:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()
                text_content = block.get("text", "")
                print(f"🔧 DEBUG: Adding heading text: '{text_content}'")
                self.apply_inline_formatting(text_content, p)
                # Make headings bold
                for run in p.runs:
                    run.font.bold = True

            elif block_type == "bullets":
                items = block.get("items", [])
                print(f"🔧 DEBUG: Adding {len(items)} bullet items")
                for item in items:
                    if first_block:
                        p = text_frame.paragraphs[0]
                        first_block = False
                    else:
                        p = text_frame.add_paragraph()

                    # Handle both simple and complex bullet items
                    if isinstance(item, dict):
                        text = item.get("text", "")
                        level = item.get("level", 1) - 1  # Convert to 0-based
                    else:
                        text = str(item)
                        level = 0

                    p.level = level
                    print(f"🔧 DEBUG: Adding bullet: '{text}' at level {level}")
                    self.apply_inline_formatting(text, p)

            elif block_type == "columns":
                columns = block.get("columns", [])
                print(
                    f"🔧 DEBUG: Processing {len(columns)} columns across {len(content_placeholders)} placeholders"
                )

                # Distribute columns across available content placeholders
                for col_idx, column in enumerate(columns):
                    if col_idx < len(content_placeholders):
                        placeholder = content_placeholders[col_idx]
                        text_frame = placeholder.text_frame
                        text_frame.clear()

                        print(
                            f"🔧 DEBUG: Processing column {col_idx} in placeholder idx {placeholder.placeholder_format.idx}"
                        )

                        # Process column content
                        column_content = column.get("content", [])
                        first_item = True
                        for content_item in column_content:
                            if isinstance(content_item, dict) and "type" in content_item:
                                item_type = content_item.get("type", "")
                                item_text = content_item.get("text", "")

                                if first_item:
                                    p = text_frame.paragraphs[0]
                                    first_item = False
                                else:
                                    p = text_frame.add_paragraph()

                                print(
                                    f"🔧 DEBUG: Adding {item_type} to column {col_idx}: '{item_text}'"
                                )
                                self.apply_inline_formatting(item_text, p)

                                # Apply type-specific formatting
                                if item_type == "heading":
                                    for run in p.runs:
                                        run.font.bold = True
                    else:
                        print(f"🔧 DEBUG: No placeholder available for column {col_idx}")

                # Mark that we've processed multi-column content, don't process individual blocks
                return

            else:
                # Unknown block type - treat as paragraph
                print(f"🔧 DEBUG: Unknown block type '{block_type}', treating as paragraph")
                if first_block:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()
                text = str(block.get("text", block))
                print(f"🔧 DEBUG: Adding unknown block text: '{text}'")
                self.apply_inline_formatting(text, p)

            first_block = False

    def _process_simple_content_list(self, placeholder, content_list):
        """Process simple content list (legacy format)"""
        text_frame = placeholder.text_frame
        text_frame.clear()

        for i, line in enumerate(content_list):
            if i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            self.apply_inline_formatting(str(line), p)

    def _process_simple_content_string(self, placeholder, content_string):
        """Process simple string content"""
        text_frame = placeholder.text_frame
        text_frame.clear()

        p = text_frame.paragraphs[0]
        self.apply_inline_formatting(content_string, p)

    def add_simple_content_to_slide(self, slide, content):
        """DEPRECATED: Use add_content_to_slide instead"""
        print(
            "Warning: add_simple_content_to_slide is deprecated, using unified add_content_to_slide"
        )
        self.add_content_to_slide(slide, content)

    def auto_parse_json_formatting(self, slide_data):
        """Auto-parse inline formatting in JSON slide data."""
        # Type validation: ensure slide_data is a dictionary
        if not isinstance(slide_data, dict):
            raise TypeError(
                f"slide_data must be a dictionary, got {type(slide_data).__name__}: {slide_data}"
            )

        # Create a copy to avoid modifying original
        processed_data = slide_data.copy()

        # Parse title if present
        if "title" in processed_data and processed_data["title"]:
            title_text = processed_data["title"]
            processed_data["title_formatted"] = self.parse_inline_formatting(title_text)

        # Parse subtitle if present
        if "subtitle" in processed_data and processed_data["subtitle"]:
            subtitle_text = processed_data["subtitle"]
            processed_data["subtitle_formatted"] = self.parse_inline_formatting(subtitle_text)

        # Parse content list - convert legacy strings to canonical JSON format
        if "content" in processed_data and isinstance(processed_data["content"], list):
            content_list = processed_data["content"]
            canonical_content = []

            for item in content_list:
                if isinstance(item, str):
                    # Convert legacy string to canonical paragraph block
                    canonical_content.append({"type": "paragraph", "text": item})
                    print(
                        "🔧 DEBUG: auto_parse_json_formatting converted legacy string to canonical paragraph"
                    )
                elif isinstance(item, dict) and "type" in item:
                    # Already canonical JSON format - keep as is
                    canonical_content.append(item)
                    print(
                        f"🔧 DEBUG: auto_parse_json_formatting preserved canonical JSON block: {item.get('type')}"
                    )
                else:
                    # Unknown format - convert to paragraph
                    canonical_content.append({"type": "paragraph", "text": str(item)})
                    print(
                        f"🔧 DEBUG: auto_parse_json_formatting converted unknown item to paragraph: {item}"
                    )

            # Replace with canonical format
            processed_data["content"] = canonical_content

        # Parse table data if present
        if "table" in processed_data and "data" in processed_data["table"]:
            table_data = processed_data["table"]
            if isinstance(table_data["data"], list):
                formatted_data = []
                for row in table_data["data"]:
                    if isinstance(row, list):
                        formatted_row = []
                        for cell in row:
                            if isinstance(cell, str):
                                formatted_row.append(
                                    {
                                        "text": cell,
                                        "formatted": self.parse_inline_formatting(cell),
                                    }
                                )
                            else:
                                # Keep non-string cells as-is
                                formatted_row.append(cell)
                        formatted_data.append(formatted_row)
                    else:
                        # Keep non-list rows as-is
                        formatted_data.append(row)
                processed_data["table"]["data"] = formatted_data

        # Note: Removed complex formatting preprocessing - formatting now handled at render time
        return processed_data
