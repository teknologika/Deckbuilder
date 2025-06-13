import os
import shutil
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
    def __init__(self):
        self.template_path = os.getenv('DECK_TEMPLATE_FOLDER')
        self.template_name = os.getenv('DECK_TEMPLATE_NAME')
        self.output_folder = os.getenv('DECK_OUTPUT_FOLDER')
        self.prs = Presentation()
        
        # Ensure default template exists in templates folder
        self._check_template_exists()
        
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

def get_deckbuilder_client():
    # Return singleton instance of Deckbuilder
    return Deckbuilder()