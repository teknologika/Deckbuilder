"""
SlideCoordinator Module

High-level orchestration of slide creation using the enhanced modular architecture.
Replaces the bloated legacy add_slide() method with clean dependency injection
and simplified orchestration flow.

DESIGN PRINCIPLES:
- Clean orchestration without complex branching
- Dependency injection for all enhanced modules
- Clear error handling throughout
- Simple, predictable workflow
- Single responsibility for slide coordination
"""

from typing import Dict, Any
from ..utils.logging import error_print, debug_print


class SlideCoordinator:
    """
    Orchestrates slide creation using the enhanced modular architecture.

    Replaces the legacy SlideBuilder with clean separation of concerns:
    - LayoutResolver: Layout resolution and validation
    - PlaceholderManager: Field-to-placeholder mapping with hybrid approach
    - ContentProcessor: Content application with template font preservation
    - TableHandler: Table processing with plain text and font logic

    WORKFLOW:
    1. Validate slide data and resolve layout
    2. Create slide with proper layout
    3. Normalize placeholder names (hybrid approach)
    4. Map fields to placeholders using patterns
    5. Apply content using ContentProcessor and TableHandler
    6. Add speaker notes if present
    7. Return completed slide
    """

    def __init__(self, layout_resolver=None, placeholder_manager=None, content_processor=None, table_handler=None):
        """
        Initialize SlideCoordinator with dependency injection.

        Args:
            layout_resolver: LayoutResolver instance (optional - will create if None)
            placeholder_manager: PlaceholderManager instance (optional - will create if None)
            content_processor: ContentProcessor instance (optional - will create if None)
            table_handler: TableHandler instance (optional - will create if None)
        """
        # Dependency injection with lazy loading
        self._layout_resolver = layout_resolver
        self._placeholder_manager = placeholder_manager
        self._content_processor = content_processor
        self._table_handler = table_handler

        # Initialize slide tracking
        self._current_slide_index = 0

    @property
    def layout_resolver(self):
        """Lazy-loaded LayoutResolver."""
        if self._layout_resolver is None:
            from ..refactor.layout_resolver import LayoutResolver as RefactorLayoutResolver

            self._layout_resolver = RefactorLayoutResolver()
        return self._layout_resolver

    @property
    def placeholder_manager(self):
        """Lazy-loaded PlaceholderManager."""
        if self._placeholder_manager is None:
            from ..refactor.placeholder_manager import PlaceholderManager

            self._placeholder_manager = PlaceholderManager()
        return self._placeholder_manager

    @property
    def content_processor(self):
        """Lazy-loaded ContentProcessor."""
        if self._content_processor is None:
            from .content_processor import ContentProcessor

            self._content_processor = ContentProcessor()
        return self._content_processor

    @property
    def table_handler(self):
        """Lazy-loaded TableHandler."""
        if self._table_handler is None:
            from .table_handler import TableHandler

            self._table_handler = TableHandler()
        return self._table_handler

    def create_slide(self, prs, slide_data: Dict[str, Any], content_formatter, image_placeholder_handler):
        """
        Create a single slide using clean orchestration flow.

        REPLACES: Bloated legacy add_slide() method with clean architecture.

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
            content_formatter: ContentFormatter instance for content handling
            image_placeholder_handler: ImagePlaceholderHandler for images

        Returns:
            Created slide object

        Raises:
            TypeError: If slide_data is not a dictionary
            ValueError: If layout cannot be resolved
            RuntimeError: If slide creation fails
        """
        try:
            # Step 1: Validate and prepare slide data
            slide_data = self._validate_and_prepare_slide_data(slide_data, content_formatter)

            # Step 2: Resolve layout and create slide
            layout_name = slide_data.get("layout", slide_data.get("type", "Title and Content"))
            slide = self._create_slide_with_layout(prs, layout_name)

            # Step 3: Normalize placeholder names using hybrid approach
            self._normalize_placeholder_names(slide, layout_name)

            # Step 4: Process content using enhanced modules
            self._process_slide_content(slide, slide_data, layout_name, content_formatter, image_placeholder_handler)

            # Step 5: Add speaker notes if present
            self._add_speaker_notes_if_present(slide, slide_data, content_formatter)

            # Step 6: Track slide completion
            self._current_slide_index += 1
            # Slide creation completed successfully

            return slide

        except Exception as e:
            error_print(f"Failed to create slide: {e}")
            raise RuntimeError(f"Slide creation failed: {e}") from e

    def clear_slides(self, prs):
        """
        Clear all slides from presentation.

        ENHANCED: Clean implementation with proper error handling.

        Args:
            prs: PowerPoint presentation object
        """
        try:
            # Clear slides in reverse order to avoid index issues
            slide_count = len(prs.slides)
            for i in range(slide_count - 1, -1, -1):
                rId = prs.slides._sldIdLst[i].rId
                prs.part.drop_rel(rId)
                del prs.slides._sldIdLst[i]

            # Slides cleared from presentation
            debug_print(f"Cleared {slide_count} slides from presentation")
            self._current_slide_index = 0

        except Exception as e:
            error_print(f"Failed to clear slides: {e}")
            raise RuntimeError(f"Failed to clear slides: {e}") from e

    def add_speaker_notes(self, slide, notes_content: str, content_formatter):
        """
        Add speaker notes to slide with proper formatting.

        ENHANCED: Clean implementation with error handling.

        Args:
            slide: PowerPoint slide object
            notes_content: Speaker notes text content
            content_formatter: ContentFormatter for text processing
        """
        if not notes_content or not notes_content.strip():
            return

        try:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.clear()

            # Add speaker notes with proper formatting
            paragraph = text_frame.paragraphs[0] if text_frame.paragraphs else text_frame.add_paragraph()
            content_formatter.apply_inline_formatting(notes_content, paragraph)

            # Speaker notes added to slide
            debug_print(f"Added speaker notes: {len(notes_content)} characters")

        except Exception as e:
            error_print(f"Failed to add speaker notes: {e}")
            # Don't raise - speaker notes failure shouldn't break slide creation

    # ===== PRIVATE ORCHESTRATION METHODS =====

    def _validate_and_prepare_slide_data(self, slide_data: Any, content_formatter) -> Dict[str, Any]:
        """Validate slide data and prepare for processing."""
        if not isinstance(slide_data, dict):
            raise TypeError(f"slide_data must be a dictionary, got {type(slide_data).__name__}")

        # Auto-parse JSON formatting for inline formatting support
        formatted_data = content_formatter.format_slide_data(slide_data)
        # Slide data validated and formatted

        return formatted_data

    def _create_slide_with_layout(self, prs, layout_name: str):
        """Create slide with resolved layout."""
        try:
            slide_layout = self.layout_resolver.resolve_layout_by_name(prs, layout_name)
            slide = prs.slides.add_slide(slide_layout)
            # Slide created with resolved layout
            return slide

        except Exception as e:
            error_print(f"Layout resolution failed for '{layout_name}': {e}")
            raise ValueError(f"Cannot resolve layout '{layout_name}': {e}") from e

    def _normalize_placeholder_names(self, slide, layout_name: str):
        """Normalize placeholder names using hybrid approach."""
        try:
            # This uses the PlaceholderNormalizer for index-based renaming
            # before name-based mapping (hybrid approach from Phase 2)
            layout = slide.slide_layout

            # Import PlaceholderNormalizer for normalization
            from ..refactor.placeholder_normalizer import PlaceholderNormalizer

            normalizer = PlaceholderNormalizer()

            # Normalize slide placeholder names to match template
            normalizer.normalize_slide_placeholder_names(slide, layout)
            # Placeholder names normalized for layout

        except Exception as e:
            error_print(f"Placeholder normalization failed: {e}")
            # Don't raise - continue with original names

    def _process_slide_content(self, slide, slide_data: Dict[str, Any], layout_name: str, content_formatter, image_placeholder_handler):
        """Process slide content using enhanced modules."""
        try:
            # Map fields to placeholders using PlaceholderManager
            placeholder_mapping = self.placeholder_manager.map_fields_to_placeholders(slide, slide_data, layout_name, slide.slide_layout)

            # BUGFIX: Extract placeholder data for content application
            placeholder_data = slide_data.get("placeholders", slide_data)

            # Apply content to each mapped placeholder
            for field_name, placeholder in placeholder_mapping.items():
                if field_name in placeholder_data:
                    field_value = placeholder_data[field_name]

                    # Use ContentProcessor for content application
                    self.content_processor.apply_content_to_placeholder(slide, placeholder, field_name, field_value, slide_data, content_formatter, image_placeholder_handler)

        except Exception as e:
            error_print(f"Content processing failed: {e}")
            raise RuntimeError(f"Content processing failed: {e}") from e

    def _add_speaker_notes_if_present(self, slide, slide_data: Dict[str, Any], content_formatter):
        """Add speaker notes if present in slide data."""
        # Check for speaker notes in multiple locations
        speaker_notes = None

        if "speaker_notes" in slide_data:
            speaker_notes = slide_data["speaker_notes"]
        elif "placeholders" in slide_data and "speaker_notes" in slide_data["placeholders"]:
            speaker_notes = slide_data["placeholders"]["speaker_notes"]

        if speaker_notes:
            self.add_speaker_notes(slide, speaker_notes, content_formatter)
