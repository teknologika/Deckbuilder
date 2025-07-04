import json
import os
import re
import shutil
from pathlib import Path

import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import PP_PLACEHOLDER_TYPE
from pptx.util import Cm, Pt

from .placeholder_types import (
    is_content_placeholder,
    is_media_placeholder,
    is_subtitle_placeholder,
    is_title_placeholder,
)
from .image_handler import ImageHandler
from .placekitten_integration import PlaceKittenIntegration
from .path_manager import path_manager, PathManager

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


try:
    from .table_styles import TABLE_BORDER_STYLES, TABLE_HEADER_STYLES, TABLE_ROW_STYLES
except ImportError:
    # Fallback values if modules don't exist
    TABLE_HEADER_STYLES = {
        "dark_blue_white_text": {"bg": RGBColor(46, 89, 132), "text": RGBColor(255, 255, 255)}
    }
    TABLE_ROW_STYLES = {
        "alternating_light_gray": {
            "primary": RGBColor(255, 255, 255),
            "alt": RGBColor(240, 240, 240),
        }
    }
    TABLE_BORDER_STYLES = {
        "thin_gray": {"width": Pt(1), "color": RGBColor(128, 128, 128), "style": "all"}
    }


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    def reset():
        """Reset the singleton instance for testing purposes"""
        instances.clear()

    # Allow external access to clear instances for testing
    get_instance._instances = instances
    get_instance.reset = reset
    cls._instances = instances
    cls.reset = reset

    return get_instance


@singleton
class Deckbuilder:
    def __init__(self, path_manager_instance: PathManager = None):
        # Use provided path manager or default global instance
        self._path_manager = path_manager_instance or path_manager

        self.template_path = str(self._path_manager.get_template_folder())
        self.template_name = self._path_manager.get_template_name()
        self.output_folder = str(self._path_manager.get_output_folder())
        self.prs = Presentation()
        self.layout_mapping = None

        # Initialize formatting support
        self.formatting_support = FormattingSupport()
        self.default_language = get_default_language()
        self.default_font = get_default_font()

        # Initialize image handling components with cache in output directory
        cache_dir = str(self._path_manager.get_output_folder() / "temp" / "image_cache")
        self.image_handler = ImageHandler(cache_dir)
        self.placekitten = PlaceKittenIntegration(self.image_handler)

        # Ensure default template exists in templates folder
        self._check_template_exists(self.template_name or "default")

    def _check_template_exists(self, templateName: str):
        """Check if template exists in the templates folder and copy if needed."""

        # Use self.template_name if available, otherwise use default
        if not templateName or templateName == "default":
            templateName = self.template_name or "default"

        # Ensure templateName ends with .pptx
        if not templateName.endswith(".pptx"):
            templateName += ".pptx"

        if self.template_path:
            try:
                # Create templates folder if it doesn't exist
                os.makedirs(self.template_path, exist_ok=True)

                # Check if template exists in templates folder
                default_template = os.path.join(self.template_path, templateName)
                if not os.path.exists(default_template):
                    # Copy from assets/templates/default.pptx
                    assets_path = os.path.join(
                        os.path.dirname(__file__), "..", "..", "assets", "templates"
                    )
                    src_template = os.path.join(assets_path, "default.pptx")
                    if os.path.exists(src_template):
                        shutil.copy2(src_template, default_template)

                # Also copy the corresponding JSON mapping file
                base_name = templateName.replace(".pptx", "")
                json_template = os.path.join(self.template_path, base_name + ".json")
                if not os.path.exists(json_template):
                    # Copy from assets/templates/default.json
                    assets_path = os.path.join(
                        os.path.dirname(__file__), "..", "..", "assets", "templates"
                    )
                    src_json = os.path.join(assets_path, base_name + ".json")
                    if os.path.exists(src_json):
                        shutil.copy2(src_json, json_template)
            except OSError:
                # Handle file operation errors silently
                pass  # nosec - Continue with setup if template copy fails

    def _load_layout_mapping(self, templateName: str):
        """Load layout mapping from JSON file."""
        if not templateName.endswith(".json"):
            templateName += ".json"

        # Try to load from template folder first
        if self.template_path:
            mapping_path = os.path.join(self.template_path, templateName)
            if os.path.exists(mapping_path):
                try:
                    with open(mapping_path, "r", encoding="utf-8") as f:
                        self.layout_mapping = json.load(f)
                        return
                except Exception:
                    pass  # nosec - Continue if layout mapping fails to load

        # Fallback to src folder
        src_mapping_path = os.path.join(os.path.dirname(__file__), templateName)
        if os.path.exists(src_mapping_path):
            try:
                with open(src_mapping_path, "r", encoding="utf-8") as f:
                    self.layout_mapping = json.load(f)
                    return
            except Exception:
                return  # nosec - Return if fallback layout mapping fails

        # Use fallback mapping if JSON not found
        self.layout_mapping = {
            "layouts": {"Title and Content": {"index": 1}},
            "aliases": {"content": "Title and Content", "title": "Title Slide"},
        }

    def _ensure_layout_mapping(self):
        """Ensure layout mapping is loaded, using default template if not already loaded"""
        if self.layout_mapping is None:
            template_name = self.template_name or "default"
            self._load_layout_mapping(template_name)

    def create_presentation(
        self, templateName: str = "default", fileName: str = "Sample_Presentation"
    ) -> str:
        # Check template exists
        self._check_template_exists(templateName)

        # Load layout mapping
        base_name = (
            templateName.replace(".pptx", "") if templateName.endswith(".pptx") else templateName
        )
        self._load_layout_mapping(base_name)

        # Create deck with template
        if not templateName.endswith(".pptx"):
            templateName += ".pptx"

        template_path = None
        if self.template_path:
            template_path = os.path.join(self.template_path, templateName)

        # Fallback to src folder if template not found in template_path
        if not template_path or not os.path.exists(template_path):
            src_template_path = os.path.join(os.path.dirname(__file__), templateName)
            if os.path.exists(src_template_path):
                template_path = src_template_path

        # Load template or create empty presentation
        if template_path and os.path.exists(template_path):
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()

        self._clear_slides()

        return f"Creating presentation: {fileName}"

    def write_presentation(self, fileName: str = "Sample_Presentation") -> str:
        """Writes the generated presentation to disk with ISO timestamp."""
        from datetime import datetime

        # Get output folder from environment or use default
        output_folder = self.output_folder or "."

        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Create filename with ISO timestamp and .g.pptx extension for generated files
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        generated_filename = f"{fileName}.{timestamp}.g.pptx"
        output_file = os.path.join(output_folder, generated_filename)

        # Save the presentation (overwrites if same timestamp exists)
        self.prs.save(output_file)

        return f"Successfully created presentation: {os.path.basename(output_file)}"

    def add_slide_from_json(self, json_data) -> str:
        """
        Add a slide to the presentation using JSON data.

        Args:
            json_data: JSON string or dictionary containing slide data

        Returns:
            Success message
        """
        try:
            # Handle both string and dictionary inputs
            if isinstance(json_data, str):
                # Parse JSON data - handle potential double encoding
                data = json.loads(json_data)

                # If the result is still a string, parse it again
                if isinstance(data, str):
                    data = json.loads(data)
            else:
                # Already a dictionary
                data = json_data

            # Handle different JSON formats
            if "slides" in data:
                # Multiple slides format
                for slide_data in data["slides"]:
                    self._add_slide(slide_data)
            elif "presentation" in data and "slides" in data["presentation"]:
                # Presentation wrapper format
                for slide_data in data["presentation"]["slides"]:
                    self._add_slide(slide_data)
            else:
                # Single slide format
                self._add_slide(data)

            return "Successfully added slide(s) from JSON data"

        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {str(e)}"
        except Exception as e:
            return f"Error adding slide: {str(e)}"

    def _clear_slides(self):
        """Clear all slides from the presentation."""
        slide_count = len(self.prs.slides)
        for i in range(slide_count - 1, -1, -1):
            rId = self.prs.slides._sldIdLst[i].rId
            self.prs.part.drop_rel(rId)
            del self.prs.slides._sldIdLst[i]

        # Reset slide index for consistent image selection
        self._current_slide_index = 0

    def _add_slide(self, slide_data: dict):
        """
        Add a single slide to the presentation based on slide data.

        Args:
            slide_data: Dictionary containing slide information
        """
        # Type validation: ensure slide_data is a dictionary
        if not isinstance(slide_data, dict):
            raise TypeError(
                f"slide_data must be a dictionary, got {type(slide_data).__name__}: {slide_data}"
            )

        # Track slide index for consistent image selection
        self._current_slide_index = getattr(self, "_current_slide_index", 0) + 1

        # Auto-parse JSON formatting for inline formatting support
        slide_data = self._auto_parse_json_formatting(slide_data)

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

        slide_layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(slide_layout)

        # Copy descriptive placeholder names from template mapping
        self._copy_placeholder_names_from_mapping(slide, layout_name)

        # Add content to placeholders using template mapping + semantic detection
        self._apply_content_to_mapped_placeholders(slide, slide_data, layout_name)

        # Handle rich content
        if "rich_content" in slide_data:
            self._add_rich_content_to_slide(slide, slide_data["rich_content"])
        elif "content" in slide_data:
            # Fallback to simple content (backwards compatibility)
            self._add_simple_content_to_slide(slide, slide_data["content"])

        # Add table if provided
        if "table" in slide_data:
            self._add_table_to_slide(slide, slide_data["table"])

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

    def _apply_content_to_mapped_placeholders(self, slide, slide_data, layout_name):
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
        """
        if not self.layout_mapping:
            # Fallback to basic semantic detection if no mapping available
            self._add_content_to_placeholders_fallback(slide, slide_data)
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
                    target_placeholder, field_name, field_value, slide_data
                )

        # Process nested structures like media.image_path
        self._process_nested_image_fields(slide, slide_data)

    def _add_content_to_placeholders_fallback(self, slide, slide_data):
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
                    self._apply_inline_formatting(slide_data["title"], p)
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
                    self._apply_inline_formatting(slide_data["subtitle"], p)
                else:
                    shape.text = slide_data["subtitle"]

            # Handle main content placeholders (for simple content)
            elif "content" in slide_data and is_content_placeholder(placeholder_type):
                # Only use simple content if rich_content is not available
                if "rich_content" not in slide_data:
                    self._add_simple_content_to_placeholder(shape, slide_data["content"])

    def _apply_content_by_semantic_type(self, placeholder, field_name, field_value, slide_data):
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
                    self._apply_formatted_segments_to_paragraph(field_value, p)
                else:
                    self._apply_inline_formatting(str(field_value), p)
            else:
                # Fallback to simple text
                placeholder.text = str(field_value)

        elif is_content_placeholder(placeholder_type):
            # Content placeholders - handle text, lists, etc. with inline formatting
            self._add_simple_content_to_placeholder(placeholder, field_value)

        elif is_media_placeholder(placeholder_type):
            # Media placeholders - handle images, charts, etc.
            if placeholder_type == PP_PLACEHOLDER_TYPE.PICTURE:
                self._handle_image_placeholder(placeholder, field_name, field_value, slide_data)
            elif placeholder_type == PP_PLACEHOLDER_TYPE.OBJECT and hasattr(
                placeholder, "text_frame"
            ):
                # OBJECT placeholders with text_frame should be treated as content placeholders
                self._add_simple_content_to_placeholder(placeholder, field_value)
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
                        self._apply_formatted_segments_to_paragraph(field_value, p)
                    else:
                        self._apply_inline_formatting(str(field_value), p)

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
                    self._apply_formatted_segments_to_paragraph(field_value, p)
                else:
                    self._apply_inline_formatting(str(field_value), p)
            else:
                placeholder.text = str(field_value)

    def _process_nested_image_fields(self, slide, slide_data):
        """
        Process nested image fields like media.image_path from structured frontmatter.

        Note: This method handles raw frontmatter with nested media structures.
        Structured frontmatter conversion flattens media.image_path to image_1,
        which is already handled by the main field processing loop.

        Args:
            slide: PowerPoint slide object
            slide_data: Dictionary containing slide content
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
                        self._handle_image_placeholder(
                            placeholder, "media.image_path", image_path, slide_data
                        )
                        break

    def _add_simple_content_to_placeholder(self, placeholder, content):
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
                self._add_rich_content_blocks_to_placeholder(text_frame, content)
                return
            elif any(key in content for key in ["heading", "paragraph", "bullets"]):
                self._debug_log("Processing direct rich content structure")
                self._add_rich_content_blocks_to_placeholder(text_frame, content)
                return
            elif "text" in content and "formatted" in content:
                self._debug_log("Processing formatted content segments")
                formatted_segments = content["formatted"]
                p = text_frame.paragraphs[0]
                self._apply_formatted_segments_to_paragraph(formatted_segments, p)
                return
            else:
                # Fallback for other dict types - avoid string conversion
                self._debug_log(f"Unknown dict content structure: {list(content.keys())}")
                # Extract text from the content if available
                if "text" in content:
                    p = text_frame.paragraphs[0]
                    self._apply_inline_formatting(content["text"], p)
                else:
                    p = text_frame.paragraphs[0]
                    p.text = str(content)
                return

        # Priority 2: Check for list of formatted segments (from content_formatting.py)
        elif isinstance(content, list):
            if content and isinstance(content[0], dict):
                # Check if this is formatted segments list
                if "text" in content[0] and "format" in content[0]:
                    self._debug_log("Processing formatted segments list")
                    p = text_frame.paragraphs[0]
                    self._apply_formatted_segments_to_paragraph(content, p)
                    return
                # Check if this is rich content blocks list
                elif any(key in content[0] for key in ["heading", "paragraph", "bullets"]):
                    self._debug_log("Processing rich content blocks list")
                    self._add_rich_content_list_to_placeholder(text_frame, content)
                    return
                else:
                    # Other dict list - handle as rich content
                    self._debug_log("Processing dict list as rich content")
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
            self._apply_inline_formatting(content, p)
            return

        # Fallback for unexpected content types
        else:
            self._debug_log(f"Fallback: Converting {content_type} to string")
            p = text_frame.paragraphs[0]
            p.text = str(content)

    def _debug_log(self, message):
        """Debug logging for content processing pipeline"""
        # Only log if debug environment variable is set
        import os

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
                self._apply_inline_formatting(item, p)

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
                    self._apply_inline_formatting(item["text"], p)
                elif "formatted" in item:
                    # Apply formatted content segments
                    if not paragraph_added:
                        p = text_frame.paragraphs[0]
                        paragraph_added = True
                    else:
                        p = text_frame.add_paragraph()
                    self._apply_formatted_segments_to_paragraph(item["formatted"], p)
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
                    self._apply_inline_formatting(text_content, p)

    def _add_single_rich_content_block_to_placeholder(
        self, text_frame, content_block, paragraph_added
    ):
        """Add a single rich content block (heading, paragraph, or bullets) to placeholder."""
        # Handle heading
        if "heading" in content_block:
            p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
            heading_text = content_block["heading"]
            self._apply_inline_formatting(heading_text, p)
            # Make heading bold by default
            for run in p.runs:
                run.font.bold = True
            self._debug_log(f"Added heading: '{heading_text}'")

        # Handle paragraph
        if "paragraph" in content_block:
            p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
            paragraph_text = content_block["paragraph"]
            self._apply_inline_formatting(paragraph_text, p)
            self._debug_log(f"Added paragraph: '{paragraph_text[:50]}...'")

        # Handle bullets with proper level support
        if "bullets" in content_block and isinstance(content_block["bullets"], list):
            bullet_levels = content_block.get("bullet_levels", [])
            for i, bullet_text in enumerate(content_block["bullets"]):
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                self._apply_inline_formatting(bullet_text, p)

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
                    self._apply_formatted_segments_to_paragraph(item["formatted"], p)
                else:
                    # Fallback to text
                    text = item.get("text", str(item))
                    self._apply_inline_formatting(text, p)
        elif "text" in content_dict and "formatted" in content_dict:
            # Handle single formatted field content like {'text': '...', 'formatted': [...]}
            p = text_frame.paragraphs[0]
            formatted_segments = content_dict["formatted"]
            self._apply_formatted_segments_to_paragraph(formatted_segments, p)
        else:
            # Handle direct rich content blocks
            paragraph_added = False

            # Handle heading
            if "heading" in content_dict:
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                heading_text = content_dict["heading"]
                self._apply_inline_formatting(heading_text, p)
                # Make heading bold by default
                for run in p.runs:
                    run.font.bold = True
                paragraph_added = True

            # Handle paragraph
            if "paragraph" in content_dict:
                p = text_frame.paragraphs[0] if not paragraph_added else text_frame.add_paragraph()
                paragraph_text = content_dict["paragraph"]
                self._apply_inline_formatting(paragraph_text, p)
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
                    self._apply_inline_formatting(bullet_text, p)

                    # Set bullet level from bullet_levels array or default to level 1
                    if i < len(bullet_levels):
                        # Convert level (1-based) to PowerPoint level (0-based)
                        p.level = max(0, bullet_levels[i] - 1)
                    else:
                        p.level = 0  # Default to top level bullets

                    self._debug_log(f"Added bullet: '{bullet_text}' at level {p.level}")
                    paragraph_added = True

    def _apply_formatted_segments_to_paragraph(self, formatted_segments, paragraph):
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

    def _parse_inline_formatting(self, text):
        """Parse inline formatting and return structured formatting data"""
        import re

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

    def _apply_inline_formatting(self, text, paragraph):
        """Apply inline formatting to paragraph using parsed formatting data."""
        # Clear any existing text
        paragraph.text = ""

        # Parse the formatting
        segments = self._parse_inline_formatting(text)

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

    def _apply_formatted_segments_to_shape(self, shape, segments):
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

    def _apply_formatted_segments_to_cell(self, cell, segments):
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

    def _add_rich_content_to_slide(self, slide, rich_content: list):
        """Add rich content blocks to a slide with improved formatting"""
        # Find the content placeholder
        content_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                content_placeholder = shape
                break

        if not content_placeholder:
            return

        # Skip if this placeholder has been converted to an image placeholder
        if not hasattr(content_placeholder, "text_frame") or content_placeholder.text_frame is None:
            print(
                f"Warning: Skipping rich content for placeholder "
                f"{content_placeholder.placeholder_format.idx} - converted to image placeholder"
            )
            return

        # Clear existing content
        text_frame = content_placeholder.text_frame
        text_frame.clear()
        text_frame.word_wrap = True

        # Set margins for better spacing
        text_frame.margin_left = Cm(0.25)
        text_frame.margin_right = Cm(0.25)
        text_frame.margin_top = Cm(0.25)
        text_frame.margin_bottom = Cm(0.25)

        # Add each content block with proper hierarchy
        first_content = True
        for block in rich_content:
            if "heading" in block:
                if first_content:
                    p = text_frame.paragraphs[0]  # Use existing first paragraph
                else:
                    p = text_frame.add_paragraph()
                self._apply_inline_formatting(block["heading"], p)
                # Apply bold to all runs in the heading paragraph
                for run in p.runs:
                    run.font.bold = True
                p.space_after = Pt(6)
                p.space_before = Pt(12) if not first_content else Pt(0)

            elif "paragraph" in block:
                if first_content:
                    p = text_frame.paragraphs[0]  # Use existing first paragraph
                else:
                    p = text_frame.add_paragraph()
                self._apply_inline_formatting(block["paragraph"], p)
                p.space_after = Pt(6)
                p.space_before = Pt(3)

            elif "bullets" in block:
                # Get bullet levels if available, otherwise default to level 1
                bullet_levels = block.get("bullet_levels", [1] * len(block["bullets"]))

                for bullet_idx, bullet in enumerate(block["bullets"]):
                    if first_content and bullet_idx == 0:
                        p = text_frame.paragraphs[
                            0
                        ]  # Use existing first paragraph for first bullet
                    else:
                        p = text_frame.add_paragraph()
                    self._apply_inline_formatting(bullet, p)

                    # Use the parsed bullet level
                    bullet_level = (
                        bullet_levels[bullet_idx] if bullet_idx < len(bullet_levels) else 1
                    )
                    p.level = bullet_level

                    # Set spacing based on level
                    if bullet_level == 1:
                        p.space_after = Pt(3)
                    else:  # Level 2+ (sub-bullets)
                        p.space_after = Pt(2)

            first_content = False

    def _add_simple_content_to_slide(self, slide, content):
        """Add simple content to slide with inline formatting support (backwards compatibility)"""
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                # Skip if this placeholder has been converted to an image placeholder
                if not hasattr(shape, "text_frame") or shape.text_frame is None:
                    print(
                        f"Warning: Skipping content for placeholder "
                        f"{shape.placeholder_format.idx} - converted to image placeholder"
                    )
                    continue

                text_frame = shape.text_frame
                text_frame.clear()

                if isinstance(content, str):
                    p = text_frame.paragraphs[0]
                    self._apply_inline_formatting(content, p)
                elif isinstance(content, list):
                    for i, line in enumerate(content):
                        if i == 0:
                            p = text_frame.paragraphs[0]  # Use existing first paragraph
                        else:
                            p = text_frame.add_paragraph()
                        self._apply_inline_formatting(line, p)
                break

    def _add_table_to_slide(self, slide, table_data):
        """
        Add a styled table to a slide.

        Args:
            slide: The slide to add the table to
            table_data: Dictionary containing table data and styling options
        """
        # Get table data - support both 'data' and 'rows' keys for backwards compatibility
        data = table_data.get("data", table_data.get("rows", []))
        if not data:
            return

        # Get styling options
        header_style = table_data.get("header_style", "dark_blue_white_text")
        row_style = table_data.get("row_style", "alternating_light_gray")
        border_style = table_data.get("border_style", "thin_gray")
        custom_colors = table_data.get("custom_colors", {})

        # Find content placeholder or create table in available space
        content_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                content_placeholder = shape
                break

        if content_placeholder:
            # Remove placeholder and create table in its place
            left = content_placeholder.left
            top = content_placeholder.top
            width = content_placeholder.width
            height = content_placeholder.height

            # Remove the placeholder
            sp = content_placeholder._element
            sp.getparent().remove(sp)
        else:
            # Default positioning if no placeholder found
            left = Cm(2.5)
            top = Cm(5)
            width = Cm(20)
            height = Cm(12)

        # Create the table
        rows = len(data)
        if data:
            # Handle both old (list of strings) and new (list of dicts) formats
            first_row = data[0]
            if isinstance(first_row, list):
                cols = len(first_row)
            else:
                cols = 1  # Fallback
        else:
            cols = 1

        table = slide.shapes.add_table(rows, cols, left, top, width, height).table

        # Apply table data with formatting support
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                cell = table.cell(row_idx, col_idx)

                # Handle both old (string) and new (formatted) cell data
                if isinstance(cell_data, dict) and "formatted" in cell_data:
                    # New formatted cell data
                    self._apply_formatted_segments_to_cell(cell, cell_data["formatted"])
                else:
                    # Old string cell data
                    cell.text = str(cell_data)

        # Apply styling
        self._apply_table_styling(table, header_style, row_style, border_style, custom_colors)

    def _apply_table_styling(self, table, header_style, row_style, border_style, custom_colors):
        """
        Apply styling to a table.

        Args:
            table: The table object to style
            header_style: Header style name
            row_style: Row style name
            border_style: Border style name
            custom_colors: Dictionary of custom color overrides
        """
        # Apply header styling
        if header_style in TABLE_HEADER_STYLES:
            header_colors = TABLE_HEADER_STYLES[header_style]

            # Override with custom colors if provided
            bg_color = (
                self._parse_custom_color(custom_colors.get("header_bg")) or header_colors["bg"]
            )
            text_color = (
                self._parse_custom_color(custom_colors.get("header_text")) or header_colors["text"]
            )

            # Style header row (first row)
            for col_idx in range(len(table.columns)):
                cell = table.cell(0, col_idx)
                # Set background color
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg_color

                # Set text color and formatting
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = text_color
                        run.font.bold = True

        # Apply row styling
        if row_style in TABLE_ROW_STYLES and len(table.rows) > 1:
            row_colors = TABLE_ROW_STYLES[row_style]

            # Override with custom colors if provided
            primary_color = (
                self._parse_custom_color(custom_colors.get("primary_row")) or row_colors["primary"]
            )
            alt_color = self._parse_custom_color(custom_colors.get("alt_row")) or row_colors["alt"]

            # Style data rows (skip header row)
            for row_idx in range(1, len(table.rows)):
                is_alt_row = (row_idx - 1) % 2 == 1
                bg_color = alt_color if is_alt_row else primary_color

                if bg_color is not None:
                    for col_idx in range(len(table.columns)):
                        cell = table.cell(row_idx, col_idx)
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = bg_color

        # Apply border styling
        if border_style in TABLE_BORDER_STYLES:
            self._apply_table_borders(table, TABLE_BORDER_STYLES[border_style], custom_colors)

    def _apply_table_borders(self, table, border_config, custom_colors):
        """
        Apply border styling to a table.

        Args:
            table: The table object
            border_config: Border configuration dictionary
            custom_colors: Custom color overrides
        """
        border_width = border_config["width"]
        border_color = (
            self._parse_custom_color(custom_colors.get("border_color")) or border_config["color"]
        )
        border_style = border_config["style"]

        if border_style == "none" or border_width.cm == 0:
            return

        # Apply borders based on style
        for row_idx in range(len(table.rows)):
            for col_idx in range(len(table.columns)):
                cell = table.cell(row_idx, col_idx)

                if border_style == "all":
                    # All borders
                    self._set_cell_borders(cell, border_width, border_color, all_sides=True)
                elif border_style == "header" and row_idx == 0:
                    # Only header bottom border
                    self._set_cell_borders(cell, border_width, border_color, bottom=True)
                elif border_style == "outer":
                    # Only outer borders
                    is_top = row_idx == 0
                    is_bottom = row_idx == len(table.rows) - 1
                    is_left = col_idx == 0
                    is_right = col_idx == len(table.columns) - 1

                    self._set_cell_borders(
                        cell,
                        border_width,
                        border_color,
                        top=is_top,
                        bottom=is_bottom,
                        left=is_left,
                        right=is_right,
                    )

    def _set_cell_borders(
        self, cell, width, color, all_sides=False, top=False, bottom=False, left=False, right=False
    ):
        """
        Set borders for a table cell.

        Args:
            cell: The table cell
            width: Border width
            color: Border color
            all_sides: Apply to all sides
            top, bottom, left, right: Apply to specific sides
        """
        if color is None:
            return

        if all_sides:
            top = bottom = left = right = True

        # Note: python-pptx has limited border support
        # This is a simplified implementation
        try:
            if hasattr(cell, "border"):
                if top and hasattr(cell.border, "top"):
                    cell.border.top.color.rgb = color
                    cell.border.top.width = width
                if bottom and hasattr(cell.border, "bottom"):
                    cell.border.bottom.color.rgb = color
                    cell.border.bottom.width = width
                if left and hasattr(cell.border, "left"):
                    cell.border.left.color.rgb = color
                    cell.border.left.width = width
                if right and hasattr(cell.border, "right"):
                    cell.border.right.color.rgb = color
                    cell.border.right.width = width
        except Exception:
            # Borders not fully supported in python-pptx, skip silently
            return  # nosec - Skip border styling if not supported

    def _parse_custom_color(self, color_value):
        """
        Parse a custom color value (hex string) to RGBColor.

        Args:
            color_value: Hex color string (e.g., "#FF0000")

        Returns:
            RGBColor object or None if invalid
        """
        if not color_value or not isinstance(color_value, str):
            return None

        try:
            # Remove # if present
            color_value = color_value.lstrip("#")

            # Convert hex to RGB
            if len(color_value) == 6:
                r = int(color_value[0:2], 16)
                g = int(color_value[2:4], 16)
                b = int(color_value[4:6], 16)
                return RGBColor(r, g, b)
        except (ValueError, TypeError):
            pass

        return None

    def parse_markdown_with_frontmatter(self, markdown_content: str) -> list:
        """
        Parse markdown content with frontmatter into slide data.

        Args:
            markdown_content: Markdown string with frontmatter slide definitions

        Returns:
            List of slide dictionaries ready for _add_slide()
        """
        # Ensure layout mapping is loaded
        self._ensure_layout_mapping()

        slides = []

        # Split content by frontmatter boundaries
        slide_blocks = re.split(r"^---\s*$", markdown_content, flags=re.MULTILINE)

        i = 0
        while i < len(slide_blocks):
            # Skip empty blocks
            if not slide_blocks[i].strip():
                i += 1
                continue

            # Look for frontmatter + content pairs
            if i + 1 < len(slide_blocks):
                try:
                    frontmatter_raw = slide_blocks[i].strip()
                    content_raw = slide_blocks[i + 1].strip() if i + 1 < len(slide_blocks) else ""

                    # Parse frontmatter with structured frontmatter support
                    slide_config = self._parse_structured_frontmatter(frontmatter_raw)

                    # Parse markdown content into slide data
                    slide_data = self._parse_slide_content(content_raw, slide_config)
                    slides.append(slide_data)

                    i += 2  # Skip both frontmatter and content blocks
                except yaml.YAMLError:
                    # If YAML parsing fails, treat as regular content
                    content_raw = slide_blocks[i].strip()
                    slide_data = self._parse_slide_content(content_raw, {})
                    slides.append(slide_data)
                    i += 1
            else:
                # Single block without frontmatter
                content_raw = slide_blocks[i].strip()
                slide_data = self._parse_slide_content(content_raw, {})
                slides.append(slide_data)
                i += 1

        return slides

    def _parse_structured_frontmatter(self, frontmatter_content: str) -> dict:
        """Parse structured frontmatter and convert to placeholder mappings"""
        from .structured_frontmatter import (
            StructuredFrontmatterConverter,
            StructuredFrontmatterValidator,
        )

        try:
            parsed = yaml.safe_load(frontmatter_content)
        except yaml.YAMLError:
            # Fallback to safe parsing for special characters
            return self._parse_frontmatter_safe(frontmatter_content)

        # Handle case where YAML parsing returns a string (malformed YAML)
        if not isinstance(parsed, dict):
            return self._parse_frontmatter_safe(frontmatter_content)

        layout_name = parsed.get("layout")
        if not layout_name:
            return parsed

        # Ensure layout mapping is loaded for structured frontmatter conversion
        self._ensure_layout_mapping()

        # Check if this is structured frontmatter
        converter = StructuredFrontmatterConverter(self.layout_mapping)

        if converter.registry.supports_structured_frontmatter(layout_name):
            # Validate structured frontmatter
            validator = StructuredFrontmatterValidator()
            validation_result = validator.validate_structured_frontmatter(parsed, layout_name)
            if not validation_result["valid"]:
                # Log warnings but continue processing
                for error in validation_result["errors"]:
                    print(f"Error in structured frontmatter: {error}")
                for warning in validation_result["warnings"]:
                    print(f"Warning in structured frontmatter: {warning}")

            # Convert to placeholder mappings
            converted = converter.convert_structured_to_placeholders(parsed)
            return converted

        # Regular frontmatter processing
        return parsed

    def _parse_frontmatter_safe(self, frontmatter_raw: str) -> dict:
        """
        Parse frontmatter safely by handling special characters that break YAML.

        This method processes frontmatter line by line to handle values with
        markdown formatting characters (*, _, etc.) that would break YAML parsing.
        """
        config = {}
        for line in frontmatter_raw.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                config[key] = value

        return config

    def _parse_slide_content(self, content: str, config: dict) -> dict:
        """Convert markdown content + config into slide data dict with mixed content support"""
        slide_data = {
            "type": config.get("layout", "content"),
            **config,  # Include all frontmatter as slide properties
        }

        # Apply formatting to frontmatter fields
        if "title" in slide_data and slide_data["title"]:
            slide_data["title_formatted"] = self._parse_inline_formatting(slide_data["title"])
        if "subtitle" in slide_data and slide_data["subtitle"]:
            slide_data["subtitle_formatted"] = self._parse_inline_formatting(slide_data["subtitle"])

        if not content.strip():
            return slide_data

        lines = content.split("\n")

        # Extract title (first # header)
        title_found = False
        content_lines = []

        for line in lines:
            if line.startswith("# ") and not title_found:
                title_text = line[2:].strip()
                # Only use markdown title if no frontmatter title exists
                if "title" not in config or not config.get("title"):
                    slide_data["title"] = title_text
                    slide_data["title_formatted"] = self._parse_inline_formatting(title_text)
                title_found = True
            elif line.startswith("## ") and slide_data["type"] == "title":
                subtitle_text = line[3:].strip()
                slide_data["subtitle"] = subtitle_text
                slide_data["subtitle_formatted"] = self._parse_inline_formatting(subtitle_text)
            else:
                content_lines.append(line)

        # Parse mixed content based on slide type
        if slide_data["type"] == "table":
            slide_data["table"] = self._parse_markdown_table("\n".join(content_lines), config)
        elif slide_data["type"] != "title":  # Content slides get rich content
            rich_content = self._parse_rich_content("\n".join(content_lines))
            if rich_content:
                slide_data["rich_content"] = rich_content

        return slide_data

    def _parse_rich_content(self, content: str) -> list:
        """Parse mixed markdown content into structured content blocks with better hierarchy"""
        blocks = []
        lines = content.split("\n")
        current_block = None

        for line in lines:
            original_line = line
            line = line.strip()
            if not line:
                continue

            # Handle nested bullet points by preserving indentation
            if line.startswith("- ") or line.startswith("* "):
                # Determine indentation level
                indent_level = len(original_line) - len(original_line.lstrip())
                bullet_text = line[2:].strip()

                if not current_block or "bullets" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"bullets": [], "bullet_levels": []}

                current_block["bullets"].append(bullet_text)
                # Map indentation to bullet levels (0 indent = level 1, 2+ spaces = level 2, etc.)
                level = 1 if indent_level < 2 else 2
                current_block["bullet_levels"].append(level)

            elif line.startswith("## "):  # Subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {"heading": line[3:].strip(), "level": 2}

            elif line.startswith("### "):  # Sub-subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {"heading": line[4:].strip(), "level": 3}

            else:  # Regular paragraph
                if not current_block or "paragraph" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"paragraph": line}
                else:
                    current_block["paragraph"] += " " + line

        if current_block:
            blocks.append(current_block)

        return blocks

    def _parse_markdown_table(self, content: str, config: dict) -> dict:
        """Extract table from markdown and apply styling config"""
        table_data = {
            "data": [],
            "header_style": config.get("style", "dark_blue_white_text"),
            "row_style": config.get("row_style", "alternating_light_gray"),
            "border_style": config.get("border_style", "thin_gray"),
            "custom_colors": config.get("custom_colors", {}),
        }

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        for line in lines:
            if line.startswith("|") and line.endswith("|"):
                # Parse table row with inline formatting
                cells = [cell.strip() for cell in line[1:-1].split("|")]
                formatted_cells = []
                for cell in cells:
                    formatted_cells.append(
                        {"text": cell, "formatted": self._parse_inline_formatting(cell)}
                    )
                table_data["data"].append(formatted_cells)
            elif "|" in line and not line.startswith("|"):
                # Handle tables without outer pipes with inline formatting
                cells = [cell.strip() for cell in line.split("|")]
                formatted_cells = []
                for cell in cells:
                    formatted_cells.append(
                        {"text": cell, "formatted": self._parse_inline_formatting(cell)}
                    )
                table_data["data"].append(formatted_cells)
            elif line.startswith("---") or line.startswith("==="):
                # Skip separator lines
                continue

        return table_data

    def _auto_parse_json_formatting(self, slide_data):
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
            processed_data["title_formatted"] = self._parse_inline_formatting(title_text)

        # Parse subtitle if present
        if "subtitle" in processed_data and processed_data["subtitle"]:
            subtitle_text = processed_data["subtitle"]
            processed_data["subtitle_formatted"] = self._parse_inline_formatting(subtitle_text)

        # Parse content list if present
        if "content" in processed_data and isinstance(processed_data["content"], list):
            # Convert simple content to rich content with formatting
            rich_content = []
            for item in processed_data["content"]:
                if isinstance(item, str):
                    # Treat as paragraph text
                    rich_content.append({"paragraph": item})
            processed_data["rich_content"] = rich_content
            # Remove old content key to avoid conflicts
            del processed_data["content"]

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
                                        "formatted": self._parse_inline_formatting(cell),
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

    def create_presentation_from_markdown(
        self,
        markdown_content: str,
        fileName: str = "Sample_Presentation",
        templateName: str = "default",
    ) -> str:
        """Create presentation from formatted markdown with frontmatter"""
        try:
            slides = self.parse_markdown_with_frontmatter(markdown_content)

            # Create presentation
            self.create_presentation(templateName, fileName)

            # Add all slides to the presentation
            for slide_data in slides:
                self._add_slide(slide_data)

            # Automatically save the presentation to disk after creation
            write_result = self.write_presentation(fileName)

            return (
                f"Successfully created presentation with {len(slides)} slides from markdown. "
                f"{write_result}"
            )
        except Exception as e:
            return f"Error creating presentation from markdown: {str(e)}"

    def create_presentation_from_json(
        self,
        json_data: dict,
        fileName: str = "Sample_Presentation",
        templateName: str = "default",
    ) -> str:
        """
        Create presentation directly from JSON data without markdown conversion.

        This method bypasses the markdown structured frontmatter pipeline entirely,
        allowing direct JSON processing with semantic field names.

        Args:
            json_data: JSON presentation data with slides
            fileName: Output file name
            templateName: Template to use

        Returns:
            Success message with slide count and file path
        """
        try:
            # Import the universal formatting module
            from .content_formatting import content_formatter

            # Validate JSON structure
            if not isinstance(json_data, dict):
                raise ValueError(f"JSON data must be a dictionary, got {type(json_data).__name__}")

            if "presentation" not in json_data:
                raise ValueError("JSON must contain 'presentation' key")

            presentation_data = json_data["presentation"]
            if "slides" not in presentation_data:
                raise ValueError("Presentation data must contain 'slides' array")

            slides_data = presentation_data["slides"]
            if not isinstance(slides_data, list):
                raise ValueError("Slides must be an array")

            # Create presentation
            self.create_presentation(templateName, fileName)

            # Process each slide with direct formatting
            processed_slides = []
            for slide_data in slides_data:
                if not isinstance(slide_data, dict):
                    raise ValueError(
                        f"Each slide must be a dictionary, got {type(slide_data).__name__}"
                    )

                # Apply universal formatting to slide data
                formatted_slide = content_formatter.format_slide_data(slide_data)
                processed_slides.append(formatted_slide)

                # Add slide using direct field mapping (no markdown conversion)
                self._add_slide_with_direct_mapping(formatted_slide)

            # Automatically save the presentation to disk after creation
            write_result = self.write_presentation(fileName)

            return (
                f"Successfully created presentation with {len(processed_slides)} slides from JSON. "
                f"{write_result}"
            )
        except Exception as e:
            return f"Error creating presentation from JSON: {str(e)}"

    def _add_slide_with_direct_mapping(self, slide_data: dict):
        """
        Add slide using direct field mapping without markdown conversion.

        This method maps JSON fields directly to PowerPoint placeholders using
        the template mapping, avoiding structured frontmatter validation.

        Args:
            slide_data: Formatted slide data dictionary
        """
        # Get layout from slide data
        layout_name = slide_data.get("type") or slide_data.get("layout", "Title and Content")

        # Get layout mapping
        if not self.layout_mapping:
            self._load_layout_mapping("default")

        layout_info = self.layout_mapping.get("layouts", {}).get(layout_name)
        if not layout_info:
            # Fallback to Title and Content layout
            layout_info = self.layout_mapping.get("layouts", {}).get("Title and Content")
            if not layout_info:
                raise ValueError(f"Layout '{layout_name}' not found and no fallback available")

        # Add slide with the specified layout
        layout_index = layout_info.get("index", 1)
        slide_layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(slide_layout)

        # Get placeholder mappings for this layout
        placeholder_mappings = layout_info.get("placeholders", {})

        # Map slide data fields to placeholders
        for placeholder_id, field_name in placeholder_mappings.items():
            placeholder_id = str(placeholder_id)  # Ensure string comparison

            # Find the placeholder in the slide
            placeholder = None
            for shape in slide.placeholders:
                if str(shape.placeholder_format.idx) == placeholder_id:
                    placeholder = shape
                    break

            if not placeholder:
                continue  # Skip if placeholder not found

            # Get field value from slide data (prioritize formatted versions)
            field_value = None

            # First priority: Check for formatted version (has proper formatting applied)
            if f"{field_name}_formatted" in slide_data:
                field_value = slide_data[f"{field_name}_formatted"]
            # Second priority: Check for direct field match
            elif field_name in slide_data:
                field_value = slide_data[field_name]
            # Third priority: Check for generic field names that map to specific template fields
            else:
                # Map generic JSON field names to specific template field names
                generic_mappings = {
                    "title_top": "title",
                    "subtitle": "subtitle",
                    "content": "content",  # For "Title and Content" layout
                    "text": "content",
                    "text_caption": "caption",
                }

                generic_field = generic_mappings.get(field_name)
                if generic_field and f"{generic_field}_formatted" in slide_data:
                    field_value = slide_data[f"{generic_field}_formatted"]
                elif generic_field and generic_field in slide_data:
                    field_value = slide_data[generic_field]

                # Special handling for rich content mapping to content
                if field_name == "content" and field_value is None:
                    # Check for rich_content_formatted first, then rich_content
                    if "rich_content_formatted" in slide_data:
                        field_value = slide_data["rich_content_formatted"]
                    elif "rich_content" in slide_data:
                        field_value = slide_data["rich_content"]

            if field_value is None:
                continue  # Skip empty fields

            # Apply content to placeholder based on type
            self._apply_content_by_semantic_type(placeholder, field_name, field_value, slide_data)

    def _handle_image_placeholder(self, placeholder, field_name, field_value, slide_data):
        """
        Handle image insertion into PICTURE placeholders with smart fallback.

        Args:
            placeholder: PowerPoint picture placeholder
            field_name: Name of the field (e.g., 'image_path', 'media.image_path')
            field_value: Image path or URL
            slide_data: Complete slide data for context
        """
        try:
            # Get placeholder dimensions for proper image sizing
            width = placeholder.width
            height = placeholder.height
            dimensions = (int(width.inches * 96), int(height.inches * 96))  # Convert to pixels

            # Prepare context for consistent PlaceKitten generation
            context = {
                "layout": slide_data.get("layout", slide_data.get("type", "unknown")),
                "slide_index": getattr(self, "_current_slide_index", 0),
            }

            # Try to use provided image path
            final_image_path = None
            if field_value and isinstance(field_value, str):
                # Validate and process the provided image
                if self.image_handler.validate_image(field_value):
                    final_image_path = self.image_handler.process_image(
                        field_value, dimensions, quality="high"
                    )
                else:
                    print(f"Warning: Invalid image path '{field_value}', using fallback")

            # Generate PlaceKitten fallback if needed
            if not final_image_path:
                final_image_path = self.placekitten.generate_fallback(dimensions, context)

            # Insert image into placeholder if we have a valid path
            if final_image_path and Path(final_image_path).exists():
                try:
                    # Check if placeholder can accept images (not already filled)
                    if hasattr(placeholder, "insert_picture"):
                        # Insert image into the picture placeholder
                        picture = placeholder.insert_picture(final_image_path)

                        # Preserve alt text if provided
                        alt_text = slide_data.get("alt_text") or slide_data.get("media", {}).get(
                            "alt_text"
                        )
                        if alt_text and hasattr(picture, "element"):
                            # Set accessibility description
                            picture.element.nvPicPr.cNvPr.descr = str(alt_text)

                        print(f"✅ Successfully inserted image into placeholder: {field_name}")
                    else:
                        msg = f"Warning: Placeholder {field_name} cannot accept images"
                        print(msg)
                        # Try to replace existing content if it's a picture shape
                        if hasattr(placeholder, "element") and hasattr(
                            placeholder.element, "nvPicPr"
                        ):
                            print("   Placeholder already contains an image, skipping...")
                        elif hasattr(placeholder, "text_frame") and placeholder.text_frame:
                            placeholder.text_frame.text = f"Image: {Path(final_image_path).name}"

                except Exception as e:
                    print(f"Warning: Failed to insert image into placeholder: {e}")
                    # Fallback: add image path as text if insertion fails
                    if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                        placeholder.text_frame.text = f"Image: {Path(final_image_path).name}"

            else:
                print(f"Warning: No valid image available for placeholder {field_name}")
                # Fallback: show placeholder text
                if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                    placeholder.text_frame.text = "Image placeholder"

        except Exception as e:
            print(f"Error handling image placeholder {field_name}: {e}")
            # Fallback: show error message in placeholder
            if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                placeholder.text_frame.text = f"Image error: {field_name}"

    def _get_placeholder_dimensions_pixels(self, placeholder):
        """
        Get placeholder dimensions in pixels for image processing.

        Args:
            placeholder: PowerPoint placeholder object

        Returns:
            tuple: (width, height) in pixels
        """
        try:
            # Convert EMU units to inches, then to pixels (96 DPI)
            width_pixels = int(placeholder.width.inches * 96)
            height_pixels = int(placeholder.height.inches * 96)
            return (width_pixels, height_pixels)
        except Exception:
            # Fallback to common slide dimensions
            return (800, 600)


def get_deckbuilder_client():
    # Return Deckbuilder instance with MCP context
    from .path_manager import create_mcp_path_manager

    return Deckbuilder(path_manager_instance=create_mcp_path_manager())
