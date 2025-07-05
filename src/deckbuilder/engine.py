import json
from datetime import datetime
from pptx import Presentation

from .path_manager import path_manager, PathManager
from .presentation_builder import PresentationBuilder
from .content_processor import ContentProcessor
from .template_manager import TemplateManager


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

        self.output_folder = str(self._path_manager.get_output_folder())
        self.prs = Presentation()

        # Initialize components
        self.template_manager = TemplateManager(self._path_manager)
        self.content_processor = ContentProcessor()
        self.presentation_builder = PresentationBuilder(self._path_manager)

        # Ensure default template exists in templates folder
        template_name = self._path_manager.get_template_name() or "default"
        self.template_manager.check_template_exists(template_name)

    def create_presentation(
        self, templateName: str = "default", fileName: str = "Sample_Presentation"
    ) -> str:
        # Prepare template and get path and layout mapping
        template_path, layout_mapping = self.template_manager.prepare_template(templateName)

        # Update components with layout mapping
        self.content_processor.layout_mapping = layout_mapping
        self.presentation_builder.layout_mapping = layout_mapping

        # Load template or create empty presentation
        if template_path:
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()

        self.presentation_builder.clear_slides(self.prs)

        return f"Creating presentation: {fileName}"

    def write_presentation(self, fileName: str = "Sample_Presentation") -> str:
        """Writes the generated presentation to disk with ISO timestamp."""
        import os

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
                    self.presentation_builder.add_slide(self.prs, slide_data)
            elif "presentation" in data and "slides" in data["presentation"]:
                # Presentation wrapper format
                for slide_data in data["presentation"]["slides"]:
                    self.presentation_builder.add_slide(self.prs, slide_data)
            else:
                # Single slide format
                self.presentation_builder.add_slide(self.prs, data)

            return "Successfully added slide(s) from JSON data"

        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {str(e)}"
        except Exception as e:
            return f"Error adding slide: {str(e)}"

    def _add_slide(self, slide_data: dict):
        """
        DEPRECATED: Use presentation_builder.add_slide instead.
        This method is kept for backwards compatibility.
        """
        return self.presentation_builder.add_slide(self.prs, slide_data)

    def create_presentation_from_markdown(
        self,
        markdown_content: str,
        fileName: str = "Sample_Presentation",
        templateName: str = "default",
    ) -> str:
        """Create presentation from formatted markdown with frontmatter"""
        try:
            slides = self.content_processor.parse_markdown_with_frontmatter(markdown_content)

            # Create presentation
            self.create_presentation(templateName, fileName)

            # Add all slides to the presentation
            for slide_data in slides:
                self.presentation_builder.add_slide(self.prs, slide_data)

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
                self.presentation_builder.add_slide_with_direct_mapping(self.prs, formatted_slide)

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
        DEPRECATED: Use presentation_builder.add_slide_with_direct_mapping instead.
        This method is kept for backwards compatibility.
        """
        return self.presentation_builder.add_slide_with_direct_mapping(self.prs, slide_data)

    def parse_markdown_with_frontmatter(self, markdown_content: str) -> list:
        """
        DEPRECATED: Use content_processor.parse_markdown_with_frontmatter instead.
        This method is kept for backwards compatibility.
        """
        return self.content_processor.parse_markdown_with_frontmatter(markdown_content)


def get_deckbuilder_client():
    # Return Deckbuilder instance with MCP context
    from .path_manager import create_mcp_path_manager

    return Deckbuilder(path_manager_instance=create_mcp_path_manager())
