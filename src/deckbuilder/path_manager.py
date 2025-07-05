#!/usr/bin/env python3
"""
Centralized Path Management for Deckbuilder

Handles all template and asset path resolution in a single location
to eliminate inconsistent path handling across the codebase.
"""

import os
from pathlib import Path
from typing import Optional, Literal


class PathManager:
    """Context-aware centralized path management for Deckbuilder

    Supports different path resolution strategies based on usage context:
    - CLI: template args > env vars > current dir, output always current dir
    - MCP: env vars > failure (no fallbacks)
    - Library: constructor args > env vars > current dir
    """

    def __init__(
        self,
        context: Literal["cli", "mcp", "library"] = "library",
        template_folder: Optional[str] = None,
        output_folder: Optional[str] = None,
        template_name: Optional[str] = None,
    ):
        """
        Initialize PathManager with context-aware behavior

        Args:
            context: Usage context (cli, mcp, library)
            template_folder: Explicit template folder path (overrides env vars)
            output_folder: Explicit output folder path (overrides env vars)
            template_name: Explicit template name (overrides env vars)
        """
        self._context = context
        self._template_folder = template_folder
        self._output_folder = output_folder
        self._template_name = template_name
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
        # Try package location first (for installed package)
        package_assets = Path(__file__).parent / "assets" / "templates"
        if package_assets.exists():
            return package_assets

        # Fallback to project root (for development)
        return self.get_project_root() / "assets" / "templates"

    def get_template_folder(self) -> Path:
        """Get template folder based on context-aware precedence rules"""

        # CLI Context: explicit args > env vars > current directory
        if self._context == "cli":
            if self._template_folder:
                return Path(self._template_folder).resolve()

            env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()

            # CLI defaults to current directory
            return Path.cwd()

        # MCP Context: env vars > failure (no fallbacks)
        elif self._context == "mcp":
            env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()

            # MCP requires explicit configuration
            raise ValueError(
                "MCP context requires DECK_TEMPLATE_FOLDER environment variable to be set"
            )

        # Library Context: constructor args > env vars > assets/templates
        else:  # library
            if self._template_folder:
                return Path(self._template_folder).resolve()

            env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()

            # Library defaults to package assets/templates
            return self.get_assets_templates_path()

    def get_output_folder(self) -> Path:
        """Get output folder based on context-aware precedence rules"""

        # CLI Context: always current directory (no args, no env vars)
        if self._context == "cli":
            return Path.cwd()

        # MCP Context: env vars > failure (no fallbacks)
        elif self._context == "mcp":
            env_folder = os.getenv("DECK_OUTPUT_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()

            # MCP requires explicit configuration
            raise ValueError(
                "MCP context requires DECK_OUTPUT_FOLDER environment variable to be set"
            )

        # Library Context: constructor args > env vars > current directory
        else:  # library
            if self._output_folder:
                return Path(self._output_folder).resolve()

            env_folder = os.getenv("DECK_OUTPUT_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()

            # Library defaults to current directory
            return Path.cwd()

    def get_template_name(self) -> str:
        """Get template name based on context-aware precedence rules"""

        # All contexts: explicit args > env vars > "default"
        if self._template_name:
            return self._template_name

        env_name = os.getenv("DECK_TEMPLATE_NAME")
        if env_name:
            return env_name

        return "default"

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


# Factory functions for different contexts
def create_cli_path_manager(template_folder: Optional[str] = None) -> PathManager:
    """Create PathManager for CLI usage (template args > env > current dir, output current dir)"""
    return PathManager(context="cli", template_folder=template_folder)


def create_mcp_path_manager() -> PathManager:
    """Create PathManager for MCP usage (env vars > failure)"""
    return PathManager(context="mcp")


def create_library_path_manager(
    template_folder: Optional[str] = None,
    output_folder: Optional[str] = None,
    template_name: Optional[str] = None,
) -> PathManager:
    """Create PathManager for library usage (args > env > current dir)"""
    return PathManager(
        context="library",
        template_folder=template_folder,
        output_folder=output_folder,
        template_name=template_name,
    )


# Global instance for backward compatibility (library context)
path_manager = PathManager(context="library")
