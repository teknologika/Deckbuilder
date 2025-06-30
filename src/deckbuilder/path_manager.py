#!/usr/bin/env python3
"""
Centralized Path Management for Deckbuilder

Handles all template and asset path resolution in a single location
to eliminate inconsistent path handling across the codebase.
"""

import os
from pathlib import Path
from typing import Optional


class PathManager:
    """Centralized path management for Deckbuilder assets and templates"""

    def __init__(self):
        self._cache = {}

    def get_project_root(self) -> Path:
        """Get the project root directory"""
        if "project_root" not in self._cache:
            # Start from this file and go up to find project root
            current = Path(__file__).parent
            while current.parent != current:
                # Look for project indicators
                if (current / "pyproject.toml").exists() or (current / "setup.py").exists():
                    self._cache["project_root"] = current
                    break
                if (current / "src" / "deckbuilder").exists():
                    self._cache["project_root"] = current
                    break
                current = current.parent
            else:
                # Fallback: go up from src/deckbuilder
                self._cache["project_root"] = Path(__file__).parent.parent.parent

        return self._cache["project_root"]

    def get_assets_templates_path(self) -> Path:
        """Get the path to template assets (default.pptx, default.json)"""
        return self.get_project_root() / "assets" / "templates"

    def get_template_folder(self) -> Path:
        """Get the current template folder from environment or default"""
        template_folder = os.getenv("DECK_TEMPLATE_FOLDER")
        if template_folder:
            return Path(template_folder).resolve()

        # Default to package assets/templates instead of current directory
        return self.get_assets_templates_path()

    def get_output_folder(self) -> Path:
        """Get the current output folder from environment or default"""
        output_folder = os.getenv("DECK_OUTPUT_FOLDER")
        if output_folder:
            return Path(output_folder).resolve()

        # Default to current working directory
        return Path.cwd()

    def get_template_name(self) -> str:
        """Get the current template name from environment or default"""
        return os.getenv("DECK_TEMPLATE_NAME", "default")

    def get_template_file_path(self, template_name: Optional[str] = None) -> Path:
        """Get the full path to a template .pptx file"""
        if not template_name:
            template_name = self.get_template_name()

        # Remove .pptx extension if present
        if template_name.endswith(".pptx"):
            template_name = template_name[:-5]

        template_folder = self.get_template_folder()
        return template_folder / f"{template_name}.pptx"

    def get_template_json_path(self, template_name: Optional[str] = None) -> Path:
        """Get the full path to a template .json mapping file"""
        if not template_name:
            template_name = self.get_template_name()

        # Remove .json extension if present
        if template_name.endswith(".json"):
            template_name = template_name[:-5]

        template_folder = self.get_template_folder()
        return template_folder / f"{template_name}.json"

    def validate_template_exists(self, template_name: Optional[str] = None) -> bool:
        """Check if a template .pptx file exists"""
        template_path = self.get_template_file_path(template_name)
        return template_path.exists()

    def validate_template_folder_exists(self) -> bool:
        """Check if the template folder exists"""
        return self.get_template_folder().exists()

    def validate_assets_exist(self) -> bool:
        """Check if default template assets exist in the package"""
        assets_path = self.get_assets_templates_path()
        default_pptx = assets_path / "default.pptx"
        default_json = assets_path / "default.json"

        return assets_path.exists() and (default_pptx.exists() or default_json.exists())

    def list_available_templates(self) -> list[str]:
        """List all available template names in the template folder"""
        template_folder = self.get_template_folder()
        if not template_folder.exists():
            return []

        templates = []
        for pptx_file in template_folder.glob("*.pptx"):
            templates.append(pptx_file.stem)

        return sorted(templates)

    def get_version(self) -> str:
        """Get the package version from various sources"""
        # Try to get from package metadata first
        try:
            from importlib.metadata import version

            return version("deckbuilder")
        except Exception:  # nosec B110
            # Package not installed or metadata unavailable, try pyproject.toml
            pass

        # Try to get from pyproject.toml
        try:
            import tomllib

            pyproject_path = self.get_project_root() / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "unknown")
        except Exception:  # nosec B110
            # pyproject.toml not available or invalid, use fallback
            pass

        # Fallback version
        return "1.0.2b2"


# Global instance for consistent usage across the codebase
path_manager = PathManager()
