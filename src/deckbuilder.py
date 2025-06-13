import os
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
        self.template_path = os.getenv('DECK_TEMPLATE_PATH')
        self.template_name = os.getenv('DECK_TEMPLATE_NAME')
        self.output_folder = os.getenv('DECK_OUTPUT_FOLDER')
        self.prs = Presentation()
        
    def create_presentation(self, fileName: str) -> str:
        # Implementation for creating presentations
        self.prs = Presentation(self.template_path) if self.template_path else Presentation()
        return f"Creating presentation: {fileName}"

def get_deckbuilder_client():
    # Return singleton instance of Deckbuilder
    return Deckbuilder()