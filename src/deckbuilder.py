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
        self._ensure_default_template()
        
    def _ensure_default_template(self):
        """Ensure default.pptx template exists in the templates folder."""
        if self.template_path:
            try:
                # Create templates folder if it doesn't exist
                os.makedirs(self.template_path, exist_ok=True)
                
                # Check if default.pptx exists in templates folder
                default_template = os.path.join(self.template_path, 'default.pptx')
                if not os.path.exists(default_template):
                    # Copy from src/default.pptx
                    src_template = os.path.join(os.path.dirname(__file__), 'default.pptx')
                    if os.path.exists(src_template):
                        shutil.copy2(src_template, default_template)
            except (OSError, IOError) as e:
                # Handle file operation errors silently
                pass
    
    def create_presentation(self, fileName: str) -> str:
        # Implementation for creating presentations
        self.prs = Presentation(self.template_path) if self.template_path else Presentation()
        return f"Creating presentation: {fileName}"

def get_deckbuilder_client():
    # Return singleton instance of Deckbuilder
    return Deckbuilder()