from ..content.formatter import ContentFormatter
from ..image.image_handler import ImageHandler
from ..image.placeholder import ImagePlaceholderHandler
from ..image.placekitten_integration import PlaceKittenIntegration
from .slide_builder import SlideBuilder
from .table_builder import TableBuilder


class PresentationBuilder:
    """Orchestrates slide creation, content placement, and formatting for PowerPoint presentations."""

    def __init__(self, path_manager):
        """
        Initialize the presentation builder.

        Args:
            path_manager: PathManager instance for handling file paths
        """
        self.path_manager = path_manager

        # Initialize components
        self.slide_builder = SlideBuilder()
        self.content_formatter = ContentFormatter()
        self.table_builder = TableBuilder(self.content_formatter)

        # Formatting options (set later via set_formatting_options)
        self.language_code = None
        self.font_name = None

        # Initialize image handling components with cache in output directory
        cache_dir = str(self.path_manager.get_output_folder() / "temp" / "image_cache")
        self.image_handler = ImageHandler(cache_dir)
        self.placekitten = PlaceKittenIntegration(self.image_handler)
        self.image_placeholder_handler = ImagePlaceholderHandler(self.image_handler, self.placekitten)

    def set_formatting_options(self, language_code=None, font_name=None):
        """Set formatting options for language and font."""
        self.language_code = language_code
        self.font_name = font_name

        # Update ContentFormatter with formatting parameters
        if language_code is not None or font_name is not None:
            self.content_formatter = ContentFormatter(language_code=language_code, font_name=font_name)
            # Update table builder with new formatter
            self.table_builder = TableBuilder(self.content_formatter)

    # TODO: Refactor and remove this pass through method
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
        from ..utils.logging import progress_print

        slide_number = len(prs.slides) + 1
        layout_name = slide_data.get("layout", "Unknown Layout")
        progress_print(f"Slide {slide_number}: {layout_name}")

        slide = self.slide_builder.add_slide(prs, slide_data, self.content_formatter, self.image_placeholder_handler)

        # Add table if provided
        if "table" in slide_data:
            self.table_builder.add_table_to_slide(slide, slide_data["table"])

        return slide

    # TODO: Refactor and remove this pass through method
    def add_slide_with_direct_mapping(self, prs, slide_data: dict):
        """
        Add slide using direct field mapping (no markdown conversion).

        Args:
            prs: PowerPoint presentation object
            slide_data: Dictionary containing slide information
        """
        return self.slide_builder.add_slide_with_direct_mapping(prs, slide_data, self.content_formatter, self.image_placeholder_handler)
