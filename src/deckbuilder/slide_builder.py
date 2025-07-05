from pptx.enum.shapes import PP_PLACEHOLDER_TYPE

from .placeholder_types import (
    is_content_placeholder,
    is_media_placeholder,
    is_subtitle_placeholder,
    is_title_placeholder,
)


class SlideBuilder:
    """Handles core slide creation, layout mapping, and placeholder management."""

    def __init__(self, layout_mapping=None):
        """
        Initialize the slide builder.

        Args:
            layout_mapping: Optional layout mapping dictionary
        """
        self.layout_mapping = layout_mapping
        self._current_slide_index = 0

    def clear_slides(self, prs):
        """Clear all slides from the presentation."""
        slide_count = len(prs.slides)
        for i in range(slide_count - 1, -1, -1):
            rId = prs.slides._sldIdLst[i].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[i]

        # Reset slide index for consistent image selection
        self._current_slide_index = 0

    def add_slide(self, prs, slide_data: dict, content_formatter, image_placeholder_handler):
        """
        Add a single slide to the presentation based on slide data.

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
            content_formatter: ContentFormatter instance for handling content
            image_placeholder_handler: ImagePlaceholderHandler instance for handling images
        """
        # Type validation: ensure slide_data is a dictionary
        if not isinstance(slide_data, dict):
            raise TypeError(
                f"slide_data must be a dictionary, got {type(slide_data).__name__}: {slide_data}"
            )

        # Track slide index for consistent image selection
        self._current_slide_index = getattr(self, "_current_slide_index", 0) + 1

        # Auto-parse JSON formatting for inline formatting support
        slide_data = content_formatter.auto_parse_json_formatting(slide_data)

        # Get slide type and determine layout using JSON mapping
        # Prefer explicit "layout" field over "type" field
        layout_or_type = slide_data.get("layout", slide_data.get("type", "content"))

        # Use layout mapping if available
        if self.layout_mapping:
            aliases = self.layout_mapping.get("aliases", {})
            layouts = self.layout_mapping.get("layouts", {})

            # Get layout name from aliases (or use direct layout name if it exists in layouts)
            if layout_or_type in layouts:
                layout_name = layout_or_type
            else:
                layout_name = aliases.get(layout_or_type, layout_or_type)

            # Get layout index
            layout_info = layouts.get(layout_name, {})
            layout_index = layout_info.get("index", 1)
        else:
            # Fallback
            layout_name = layout_or_type  # Use the original layout name as fallback
            layout_index = 1

        slide_layout = prs.slide_layouts[layout_index]
        slide = prs.slides.add_slide(slide_layout)

        # Copy descriptive placeholder names from template mapping
        self._copy_placeholder_names_from_mapping(slide, layout_name)

        # Add content to placeholders using template mapping + semantic detection
        self._apply_content_to_mapped_placeholders(
            slide, slide_data, layout_name, content_formatter, image_placeholder_handler
        )

        # Handle rich content
        if "rich_content" in slide_data:
            content_formatter.add_rich_content_to_slide(slide, slide_data["rich_content"])
        elif "content" in slide_data:
            # Fallback to simple content (backwards compatibility)
            content_formatter.add_simple_content_to_slide(slide, slide_data["content"])

        return slide

    def add_slide_with_direct_mapping(
        self, prs, slide_data: dict, content_formatter, image_placeholder_handler
    ):
        """
        Add slide using direct field mapping (no markdown conversion).

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
            content_formatter: ContentFormatter instance
            image_placeholder_handler: ImagePlaceholderHandler instance
        """
        # Import the universal formatting module
        from .content_formatting import content_formatter as cf

        # Apply universal formatting to slide data
        formatted_slide = cf.format_slide_data(slide_data)

        # Add slide using the standard method
        return self.add_slide(prs, formatted_slide, content_formatter, image_placeholder_handler)

    def _copy_placeholder_names_from_mapping(self, slide, layout_name):
        """
        Copy descriptive placeholder names from template mapping to slide placeholders.

        This enhances the PowerPoint editing experience by providing meaningful placeholder
        names like "Col 1 Title Placeholder 2" instead of generic "Text Placeholder 2".

        Args:
            slide: PowerPoint slide object
            layout_name: Name of the PowerPoint layout
        """
        if not self.layout_mapping:
            return

        # Get layout info from template mapping
        layouts = self.layout_mapping.get("layouts", {})
        layout_info = layouts.get(layout_name, {})
        placeholder_mappings = layout_info.get("placeholders", {})

        # Update placeholder names to match template mapping
        for placeholder in slide.placeholders:
            placeholder_idx = str(placeholder.placeholder_format.idx)
            if placeholder_idx in placeholder_mappings:
                descriptive_name = placeholder_mappings[placeholder_idx]
                try:
                    # Update the placeholder name
                    placeholder.element.nvSpPr.cNvPr.name = descriptive_name
                except Exception:
                    # Fallback: some placeholder types might not allow name changes
                    pass  # nosec - Continue processing other placeholders

    def _apply_content_to_mapped_placeholders(
        self, slide, slide_data, layout_name, content_formatter, image_placeholder_handler
    ):
        """
        Apply content to placeholders using template JSON mappings + semantic detection.

        This unified method works with both JSON input and markdown frontmatter input:
        1. Looks up layout in template JSON mappings
        2. For each field in slide_data, finds corresponding placeholder index
        3. Gets actual placeholder and determines its semantic type
        4. Applies content using appropriate semantic handler

        Args:
            slide: PowerPoint slide object
            slide_data: Dictionary containing slide content (from JSON or markdown)
            layout_name: Name of the PowerPoint layout
            content_formatter: ContentFormatter instance
            image_placeholder_handler: ImagePlaceholderHandler instance
        """
        if not self.layout_mapping:
            # Fallback to basic semantic detection if no mapping available
            self._add_content_to_placeholders_fallback(slide, slide_data, content_formatter)
            return

        # Get layout info from template mapping
        layouts = self.layout_mapping.get("layouts", {})
        layout_info = layouts.get(layout_name, {})
        placeholder_mappings = layout_info.get("placeholders", {})

        # Create reverse mapping: field_name -> placeholder_index
        field_to_index = {}
        for placeholder_idx, field_name in placeholder_mappings.items():
            field_to_index[field_name] = int(placeholder_idx)

        # Process each field in slide_data using semantic detection
        for field_name, field_value in slide_data.items():
            # Skip non-content fields
            if field_name in ["type", "rich_content", "table", "layout"]:
                continue

            # Find placeholder using semantic detection
            target_placeholder = None

            # Handle title placeholders
            if field_name == "title":
                for placeholder in slide.placeholders:
                    if is_title_placeholder(placeholder.placeholder_format.type):
                        target_placeholder = placeholder
                        break

            # Handle subtitle placeholders
            elif field_name == "subtitle":
                for placeholder in slide.placeholders:
                    if is_subtitle_placeholder(placeholder.placeholder_format.type):
                        target_placeholder = placeholder
                        break

            # Handle content placeholders
            elif field_name == "content":
                for placeholder in slide.placeholders:
                    if is_content_placeholder(placeholder.placeholder_format.type):
                        target_placeholder = placeholder
                        break

            # Handle image_path fields and image placeholder fields - find PICTURE placeholders
            elif (
                field_name == "image_path"
                or field_name.endswith(".image_path")
                or "image" in field_name.lower()
            ):
                for placeholder in slide.placeholders:
                    if placeholder.placeholder_format.type == PP_PLACEHOLDER_TYPE.PICTURE:
                        target_placeholder = placeholder
                        break

            # Handle other fields by checking if they match placeholder names in JSON mapping
            else:
                # Try to find by exact field name match in JSON mapping
                if field_name in field_to_index:
                    placeholder_idx = field_to_index[field_name]
                    for placeholder in slide.placeholders:
                        if placeholder.placeholder_format.idx == placeholder_idx:
                            target_placeholder = placeholder
                            break

            if target_placeholder:
                # Apply content based on placeholder's semantic type
                self._apply_content_by_semantic_type(
                    target_placeholder,
                    field_name,
                    field_value,
                    slide_data,
                    content_formatter,
                    image_placeholder_handler,
                )

        # Process nested structures like media.image_path
        self._process_nested_image_fields(slide, slide_data, image_placeholder_handler)

    def _add_content_to_placeholders_fallback(self, slide, slide_data, content_formatter):
        """
        Fallback method for basic semantic placeholder detection when no JSON mapping available.
        Uses inline formatting (**bold**, *italic*, ___underline___) processed at render time.
        """
        for shape in slide.placeholders:
            placeholder_type = shape.placeholder_format.type

            # Handle title placeholders
            if "title" in slide_data and is_title_placeholder(placeholder_type):
                if hasattr(shape, "text_frame") and shape.text_frame:
                    text_frame = shape.text_frame
                    text_frame.clear()
                    p = (
                        text_frame.paragraphs[0]
                        if text_frame.paragraphs
                        else text_frame.add_paragraph()
                    )
                    content_formatter.apply_inline_formatting(slide_data["title"], p)
                else:
                    shape.text = slide_data["title"]

            # Handle subtitle placeholders
            elif "subtitle" in slide_data and is_subtitle_placeholder(placeholder_type):
                if hasattr(shape, "text_frame") and shape.text_frame:
                    text_frame = shape.text_frame
                    text_frame.clear()
                    p = (
                        text_frame.paragraphs[0]
                        if text_frame.paragraphs
                        else text_frame.add_paragraph()
                    )
                    content_formatter.apply_inline_formatting(slide_data["subtitle"], p)
                else:
                    shape.text = slide_data["subtitle"]

            # Handle main content placeholders (for simple content)
            elif "content" in slide_data and is_content_placeholder(placeholder_type):
                # Only use simple content if rich_content is not available
                if "rich_content" not in slide_data:
                    content_formatter.add_simple_content_to_placeholder(
                        shape, slide_data["content"]
                    )

    def _apply_content_by_semantic_type(
        self,
        placeholder,
        field_name,
        field_value,
        slide_data,
        content_formatter,
        image_placeholder_handler,
    ):
        """
        Apply content to a placeholder based on its semantic type and the content type.
        Uses inline formatting (**bold**, *italic*, ___underline___) processed at render time.
        """
        placeholder_type = placeholder.placeholder_format.type

        # Apply content based on placeholder semantic type
        if is_title_placeholder(placeholder_type) or is_subtitle_placeholder(placeholder_type):
            # Title/subtitle placeholders - apply inline formatting directly
            if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                # Use text frame for formatting support
                text_frame = placeholder.text_frame
                text_frame.clear()
                p = (
                    text_frame.paragraphs[0]
                    if text_frame.paragraphs
                    else text_frame.add_paragraph()
                )
                # Handle formatted content properly for titles
                if (
                    isinstance(field_value, list)
                    and field_value
                    and isinstance(field_value[0], dict)
                    and "text" in field_value[0]
                ):
                    content_formatter.apply_formatted_segments_to_paragraph(field_value, p)
                else:
                    content_formatter.apply_inline_formatting(str(field_value), p)
            else:
                # Fallback to simple text
                placeholder.text = str(field_value)

        elif is_content_placeholder(placeholder_type):
            # Content placeholders - handle text, lists, etc. with inline formatting
            content_formatter.add_simple_content_to_placeholder(placeholder, field_value)

        elif is_media_placeholder(placeholder_type):
            # Media placeholders - handle images, charts, etc.
            if placeholder_type == PP_PLACEHOLDER_TYPE.PICTURE:
                image_placeholder_handler.handle_image_placeholder(
                    placeholder, field_name, field_value, slide_data
                )
            elif placeholder_type == PP_PLACEHOLDER_TYPE.OBJECT and hasattr(
                placeholder, "text_frame"
            ):
                # OBJECT placeholders with text_frame should be treated as content placeholders
                content_formatter.add_simple_content_to_placeholder(placeholder, field_value)
            else:
                # Other media types - fallback to text for now
                if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                    text_frame = placeholder.text_frame
                    text_frame.clear()
                    p = (
                        text_frame.paragraphs[0]
                        if text_frame.paragraphs
                        else text_frame.add_paragraph()
                    )
                    if (
                        isinstance(field_value, list)
                        and field_value
                        and isinstance(field_value[0], dict)
                        and "text" in field_value[0]
                    ):
                        content_formatter.apply_formatted_segments_to_paragraph(field_value, p)
                    else:
                        content_formatter.apply_inline_formatting(str(field_value), p)

        else:
            # Other placeholder types - apply inline formatting where possible
            if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                text_frame = placeholder.text_frame
                text_frame.clear()
                p = (
                    text_frame.paragraphs[0]
                    if text_frame.paragraphs
                    else text_frame.add_paragraph()
                )
                if (
                    isinstance(field_value, list)
                    and field_value
                    and isinstance(field_value[0], dict)
                    and "text" in field_value[0]
                ):
                    content_formatter.apply_formatted_segments_to_paragraph(field_value, p)
                else:
                    content_formatter.apply_inline_formatting(str(field_value), p)
            else:
                placeholder.text = str(field_value)

    def _process_nested_image_fields(self, slide, slide_data, image_placeholder_handler):
        """
        Process nested image fields like media.image_path from structured frontmatter.

        Note: This method handles raw frontmatter with nested media structures.
        Structured frontmatter conversion flattens media.image_path to image_1,
        which is already handled by the main field processing loop.

        Args:
            slide: PowerPoint slide object
            slide_data: Dictionary containing slide content
            image_placeholder_handler: ImagePlaceholderHandler instance
        """
        # Skip if this appears to be structured frontmatter that was already converted
        # (indicated by presence of flattened image fields like image_1, image_path)
        has_converted_image_fields = any(
            field_name == "image_path"
            or field_name.endswith("_1")
            and "image" in field_name.lower()
            for field_name in slide_data.keys()
        )

        if has_converted_image_fields:
            # Already processed by structured frontmatter conversion
            return

        # Check for media structure with image_path (raw frontmatter)
        if "media" in slide_data and isinstance(slide_data["media"], dict):
            media_data = slide_data["media"]
            image_path = media_data.get("image_path")

            if image_path:
                # Find the first PICTURE placeholder
                for placeholder in slide.placeholders:
                    if placeholder.placeholder_format.type == PP_PLACEHOLDER_TYPE.PICTURE:
                        image_placeholder_handler.handle_image_placeholder(
                            placeholder, "media.image_path", image_path, slide_data
                        )
                        break
