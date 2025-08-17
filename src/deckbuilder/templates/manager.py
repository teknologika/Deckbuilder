import json
import os
import shutil


class TemplateManager:
    """Handles template loading, validation, and layout mapping management."""

    def __init__(self, path_manager):
        """
        Initialize the template manager.

        Args:
            path_manager: PathManager instance for handling file paths
        """
        self.path_manager = path_manager
        self.template_path = str(self.path_manager.get_template_folder())
        self.template_name = self.path_manager.get_template_name()
        self.layout_mapping = None

    def check_template_exists(self, template_name: str = None):
        """Check if template exists in the templates folder and copy if needed."""

        # Use provided template_name or fall back to instance template_name
        if not template_name or template_name == "default":
            template_name = self.template_name or "default"

        # Ensure template_name ends with .pptx
        if not template_name.endswith(".pptx"):
            template_name += ".pptx"

        if self.template_path:
            try:
                # Create templates folder if it doesn't exist
                os.makedirs(self.template_path, exist_ok=True)

                # Check if template exists in templates folder
                default_template = os.path.join(self.template_path, template_name)
                if not os.path.exists(default_template):
                    # Copy from assets/templates/default.pptx
                    assets_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "templates")
                    src_template = os.path.join(assets_path, "default.pptx")
                    if os.path.exists(src_template):
                        shutil.copy2(src_template, default_template)

                # Legacy JSON mapping file copying removed - no longer needed
            except OSError:
                # Handle file operation errors silently
                pass  # nosec - Continue with setup if template copy fails

    def load_layout_mapping(self, template_name: str):
        """Load layout mapping from JSON file."""
        if not template_name.endswith(".json"):
            template_name += ".json"

        # Try to load from template folder first
        if self.template_path:
            mapping_path = os.path.join(self.template_path, template_name)
            if os.path.exists(mapping_path):
                try:
                    with open(mapping_path, "r", encoding="utf-8") as f:
                        self.layout_mapping = json.load(f)
                        return
                except Exception:
                    pass  # nosec - Continue if layout mapping fails to load

        # Fallback to src folder
        src_mapping_path = os.path.join(os.path.dirname(__file__), template_name)
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

    def ensure_layout_mapping(self):
        """Ensure layout mapping is loaded, using default template if not already loaded"""
        if self.layout_mapping is None:
            template_name = self.template_name or "default"
            self.load_layout_mapping(template_name)

    def get_layout_mapping(self):
        """Get the current layout mapping, ensuring it's loaded first."""
        self.ensure_layout_mapping()
        return self.layout_mapping

    def get_template_path(self, template_name: str = None) -> str:
        """
        Get the full path to a template file.

        Args:
            template_name: Name of the template (defaults to instance template_name)

        Returns:
            Full path to the template file, or None if not found
        """
        if not template_name:
            template_name = self.template_name or "default"

        if not template_name.endswith(".pptx"):
            template_name += ".pptx"

        template_path = None
        if self.template_path:
            template_path = os.path.join(self.template_path, template_name)

        # Fallback to src folder if template not found in template_path
        if not template_path or not os.path.exists(template_path):
            src_template_path = os.path.join(os.path.dirname(__file__), template_name)
            if os.path.exists(src_template_path):
                template_path = src_template_path

        return template_path if template_path and os.path.exists(template_path) else None

    def prepare_template(self, template_name: str = "default") -> tuple:
        """
        Prepare a template for use by checking existence and loading layout mapping.

        Args:
            template_name: Name of the template to prepare

        Returns:
            tuple: (template_path, layout_mapping) where template_path may be None if not found
        """
        # Check and copy template if needed
        self.check_template_exists(template_name)

        # Load layout mapping
        base_name = template_name.replace(".pptx", "") if template_name.endswith(".pptx") else template_name
        self.load_layout_mapping(base_name)

        # Get template path
        template_path = self.get_template_path(template_name)

        return template_path, self.layout_mapping
