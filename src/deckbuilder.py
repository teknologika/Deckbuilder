import os
import shutil
import json
from pptx import Presentation

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Deckbuilder:

# Default layout mappings if not specified in settings
    DEFAULT_LAYOUTS = {
        "title": "title",                # Title slide with subtitle
        "table": "titleandcontent",      # Slide with title and table
        "content": "titleandcontent",    # Slide with title and bullet points
        "section": "sectionHeader",      # Section divider slide
        "blank": "blank"                 # Blank slide
    }   

    # Standard PowerPoint layout names and their indices
    DEFAULT_PPT_LAYOUTS = {
        "title": 0,                    # Title Slide
        "titleandcontent": 1,          # Title and Content
        "sectionHeader": 2,            # Section Header
        "twoContent": 3,              # Two Content
        "comparison": 4,              # Comparison
        "titleOnly": 5,               # Title Only
        "blank": 6,                   # Blank
        "contentWithCaption": 7,      # Content with Caption
        "pictureWithCaption": 8,      # Picture with Caption
        "titleAndVerticalText": 9,    # Title and Vertical Text
        "verticalTitleAndText": 10    # Vertical Title and Text
        }

    def __init__(self):
        self.template_path = os.getenv('DECK_TEMPLATE_FOLDER')
        self.template_name = os.getenv('DECK_TEMPLATE_NAME')
        self.output_folder = os.getenv('DECK_OUTPUT_FOLDER')
        self.prs = Presentation()
        
        # Ensure default template exists in templates folder
        self._check_template_exists(self.template_name or 'default')
        
    def _check_template_exists(self, templateName: str):
        """Check if template exists in the templates folder and copy if needed."""

        # Use self.template_name if available, otherwise use default
        if not templateName or templateName == 'default':
            templateName = self.template_name or 'default'

        # Ensure templateName ends with .pptx
        if not templateName.endswith('.pptx'):
            templateName += '.pptx'
        
        if self.template_path:
            try:
                # Create templates folder if it doesn't exist
                os.makedirs(self.template_path, exist_ok=True)
                
                # Check if template exists in templates folder
                default_template = os.path.join(self.template_path, templateName)
                if not os.path.exists(default_template):
                    # Copy from src/default.pptx
                    src_template = os.path.join(os.path.dirname(__file__), 'default.pptx')
                    if os.path.exists(src_template):
                        shutil.copy2(src_template, default_template)
            except (OSError, IOError) as e:
                # Handle file operation errors silently
                pass
    
    def create_presentation(self, fileName: str, templateName: str = "default") -> str:
        # Check template exists
        self._check_template_exists(templateName)
        
        # Create deck with template
        if not templateName.endswith('.pptx'):
            templateName += '.pptx'
        template_path = os.path.join(self.template_path, templateName) if self.template_path else None
        self.prs = Presentation(template_path) if template_path and os.path.exists(template_path) else Presentation()
        
        return f"Creating presentation: {fileName}"

    def write_presentation(self, fileName: str = "Sample_Presentation") -> str:
        """Writes the presentation to disk with versioning."""
        # Get output folder from environment or use default
        output_folder = self.output_folder or '.'
        
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Create base filename with .latest.pptx extension
        base_name = f"{fileName}.latest.pptx"
        latest_file = os.path.join(output_folder, base_name)
        
        # Handle versioning if file exists
        if os.path.exists(latest_file):
            # Find the highest version number
            version_num = 1
            while True:
                version_file = os.path.join(output_folder, f"{fileName}.latest.pptx.v{version_num:02d}.pptx")
                if not os.path.exists(version_file):
                    break
                version_num += 1
            
            # Rename current latest to versioned file
            os.rename(latest_file, version_file)
        
        # Write the latest file
        self.prs.save(latest_file)
        
        return f"Successfully created presentation: {os.path.basename(latest_file)}"

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

    def _add_slide(self, slide_data: dict):
        """
        Add a single slide to the presentation based on slide data.
        
        Args:
            slide_data: Dictionary containing slide information
        """
        # Basic slide creation - can be expanded based on slide_data structure
        slide_layout = self.prs.slide_layouts[0]  # Use first layout as default
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Add title if provided
        if "title" in slide_data and slide.shapes.title:
            slide.shapes.title.text = slide_data["title"]
        
        # Add content if provided
        if "content" in slide_data:
            # This is a basic implementation - can be expanded
            # to handle different content types (text, images, etc.)
            for shape in slide.placeholders:
                if shape.placeholder_format.idx == 1:  # Content placeholder
                    if isinstance(slide_data["content"], str):
                        shape.text = slide_data["content"]
                    elif isinstance(slide_data["content"], list):
                        shape.text = "\n".join(slide_data["content"])
                    break

def get_deckbuilder_client():
    # Return singleton instance of Deckbuilder
    return Deckbuilder()