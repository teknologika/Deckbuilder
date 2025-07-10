from .slide_builder import SlideBuilder
from .content_formatter import ContentFormatter
from .table_builder import TableBuilder
from .image_placeholder_handler import ImagePlaceholderHandler
from .image_handler import ImageHandler
from .placekitten_integration import PlaceKittenIntegration


class PresentationBuilder:
    """Orchestrates slide creation, content placement, and formatting for PowerPoint presentations."""

    def __init__(self, path_manager, layout_mapping=None):
        """
        Initialize the presentation builder.

        Args:
            path_manager: PathManager instance for handling file paths
            layout_mapping: Optional layout mapping dictionary
        """
        self.path_manager = path_manager
        self._layout_mapping = layout_mapping

        # Initialize components
        self.slide_builder = SlideBuilder(layout_mapping)
        self.content_formatter = ContentFormatter()
        self.table_builder = TableBuilder(self.content_formatter)

        # Initialize image handling components with cache in output directory
        cache_dir = str(self.path_manager.get_output_folder() / "temp" / "image_cache")
        self.image_handler = ImageHandler(cache_dir)
        self.placekitten = PlaceKittenIntegration(self.image_handler)
        self.image_placeholder_handler = ImagePlaceholderHandler(self.image_handler, self.placekitten)

    @property
    def layout_mapping(self):
        """Get the current layout mapping."""
        return self._layout_mapping

    @layout_mapping.setter
    def layout_mapping(self, value):
        """Set the layout mapping and update all components."""
        self._layout_mapping = value
        if hasattr(self, "slide_builder"):
            self.slide_builder.layout_mapping = value

    def clear_slides(self, prs):
        """Clear all slides from the presentation."""
        return self.slide_builder.clear_slides(prs)

    def add_slide(self, prs, slide_data: dict):
        """
        Add a single slide to the presentation based on slide data.

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
        """
        # Show progress message
        from .logging_config import progress_print

        slide_number = len(prs.slides) + 1
        layout_name = slide_data.get("layout", "Unknown Layout")
        progress_print(f"Slide {slide_number}: {layout_name}")

        slide = self.slide_builder.add_slide(prs, slide_data, self.content_formatter, self.image_placeholder_handler)

        # Add table if provided
        if "table" in slide_data:
            self.table_builder.add_table_to_slide(slide, slide_data["table"])

        return slide

    def add_slide_with_direct_mapping(self, prs, slide_data: dict):
        """
        Add slide using direct field mapping (no markdown conversion).

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
        """
        return self.slide_builder.add_slide_with_direct_mapping(prs, slide_data, self.content_formatter, self.image_placeholder_handler)
