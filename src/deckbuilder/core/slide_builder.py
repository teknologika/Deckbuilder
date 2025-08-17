"""
SlideBuilder - Backward Compatibility Wrapper

Maintains exact same public API as the legacy SlideBuilder while delegating
to the new enhanced modular architecture via SlideCoordinator.

This ensures zero breaking changes for existing code while providing all
the benefits of the refactored architecture.
"""

from .slide_coordinator import SlideCoordinator
from ..utils.logging import debug_print


class SlideBuilder:
    """
    Backward compatibility wrapper for SlideBuilder.

    DESIGN: Delegates all operations to SlideCoordinator while maintaining
    the exact same public API as the legacy implementation.

    This ensures:
    - Zero breaking changes for existing code
    - All benefits of enhanced modular architecture
    - Seamless migration path
    - Preserved method signatures and behavior
    """

    def __init__(self):
        """Initialize SlideBuilder with SlideCoordinator delegation."""
        # Delegate to SlideCoordinator for actual implementation
        self._coordinator = SlideCoordinator()

        debug_print("SlideBuilder initialized with enhanced modular architecture")

    def clear_slides(self, prs):
        """
        Clear all slides from the presentation.

        DELEGATES to: SlideCoordinator.clear_slides()
        MAINTAINS: Exact same API signature and behavior

        Args:
            prs: PowerPoint presentation object
        """
        return self._coordinator.clear_slides(prs)

    def add_slide(self, prs, slide_data: dict, content_formatter, image_placeholder_handler):
        """
        Add a single slide to the presentation based on slide data.

        DELEGATES to: SlideCoordinator.create_slide()
        MAINTAINS: Exact same API signature and behavior

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
            content_formatter: ContentFormatter instance for handling content
            image_placeholder_handler: ImagePlaceholderHandler instance for handling images

        Returns:
            Created slide object
        """
        return self._coordinator.create_slide(prs, slide_data, content_formatter, image_placeholder_handler)

    def add_speaker_notes(self, slide, notes_content, content_formatter):
        """
        Add speaker notes to the slide.

        DELEGATES to: SlideCoordinator.add_speaker_notes()
        MAINTAINS: Exact same API signature and behavior

        Args:
            slide: The slide to add notes to
            notes_content: The content of the speaker notes
            content_formatter: ContentFormatter instance for handling content
        """
        return self._coordinator.add_speaker_notes(slide, notes_content, content_formatter)

    def add_slide_with_direct_mapping(self, prs, slide_data: dict, content_formatter, image_placeholder_handler):
        """
        Add slide using direct field mapping (no markdown conversion).

        DELEGATES to: SlideCoordinator.create_slide()
        MAINTAINS: Exact same API signature and behavior

        NOTE: In the enhanced architecture, all slides use the same clean processing
        path, so this method delegates to the same create_slide() implementation.

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
            content_formatter: ContentFormatter instance
            image_placeholder_handler: ImagePlaceholderHandler instance

        Returns:
            Created slide object
        """
        # In the enhanced architecture, direct mapping is the default approach
        # So this delegates to the same create_slide method
        return self._coordinator.create_slide(prs, slide_data, content_formatter, image_placeholder_handler)

    # ===== LEGACY PRIVATE METHODS (Preserved for Compatibility) =====

    def _find_placeholder_by_name(self, slide, field_name):
        """
        Find a placeholder by its name (preserved for compatibility).

        LEGACY METHOD: Kept for any existing code that might access it directly.
        NEW ARCHITECTURE: PlaceholderManager handles this functionality.

        Args:
            slide: The slide to search
            field_name: The field name to look for

        Returns:
            The placeholder object if found, None otherwise
        """
        # Delegate to PlaceholderResolver for compatibility
        try:
            from ..refactor.placeholder_resolver import PlaceholderResolver

            resolver = PlaceholderResolver()
            return resolver.get_placeholder_by_name(slide, field_name)
        except Exception:
            # Fallback to legacy implementation for compatibility
            for placeholder in slide.placeholders:
                try:
                    placeholder_name = placeholder.element.nvSpPr.cNvPr.name
                    if placeholder_name == field_name:
                        return placeholder
                except AttributeError:
                    continue
            return None

    # ===== PROPERTY ACCESS FOR ENHANCED MODULES =====

    @property
    def coordinator(self):
        """Access to SlideCoordinator for advanced usage."""
        return self._coordinator

    @property
    def layout_resolver(self):
        """Access to LayoutResolver via coordinator."""
        return self._coordinator.layout_resolver

    @property
    def placeholder_manager(self):
        """Access to PlaceholderManager via coordinator."""
        return self._coordinator.placeholder_manager

    @property
    def content_processor(self):
        """Access to ContentProcessor via coordinator."""
        return self._coordinator.content_processor

    @property
    def table_handler(self):
        """Access to TableHandler via coordinator."""
        return self._coordinator.table_handler
