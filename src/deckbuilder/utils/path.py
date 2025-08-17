#!/usr/bin/env python3
"""
Centralized Path Management for Deckbuilder

This class provides a single, context-aware interface for locating templates
and other assets, whether running from source (dev mode) or from an installed
package (wheel/zip). It ensures consistent path handling across:
- CLI tools
- MCP integrations
- Library usage

Assets are *materialised* to a real directory when needed (some libraries
require a real filesystem path).

Quick starts
------------
# 1) Get a real path to packaged templates (library default)
from deckbuilder.paths import path_manager
templates = path_manager.get_assets_templates_path()
print(list(templates.glob("*.pptx")))

# 2) Resolve a template by name (respects context/env/args)
pm = create_library_path_manager(template_name="default")
pptx = pm.get_template_file_path()        # -> .../default.pptx
# Legacy template mapping JSON files no longer used

# 3) Override via env (CLI/MCP)
#   DECK_TEMPLATE_FOLDER=/my/templates  DECK_TEMPLATE_NAME=corp pm.get_template_file_path()

# 4) Extract packaged assets to a custom cache dir
#   DECK_ASSET_CACHE_DIR=/tmp/db-assets  python -c "from deckbuilder.paths import path_manager; print(path_manager.get_assets_templates_path())"

# 5) List available templates (by .pptx files)
print(path_manager.list_available_templates())  # -> ['default', 'custom1', ...]

# 6) Validate presence
assert path_manager.validate_assets_exist(), "Packaged default templates missing!"
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Literal, Tuple

# Standard library (3.9+) importlib.resources; backport only if needed.
try:
    from importlib.resources import files
except ImportError:  # pragma: no cover
    from importlib_resources import files  # type: ignore


class PathManager:
    """
    Context-aware path resolution:
      - CLI:    args > env vars > CWD/templates ; output always CWD
      - MCP:    env vars only (else error)
      - Library:args > env vars > packaged assets/templates

    Example
    -------
    pm = PathManager(context="library", template_name="default")
    print(pm.get_template_file_path())   # .../default.pptx
    """

    def __init__(
        self,
        context: Literal["cli", "mcp", "library"] = "library",
        template_folder: Optional[str] = None,
        output_folder: Optional[str] = None,
        template_name: Optional[str] = None,
    ):
        self._context = context
        self._template_folder = template_folder
        self._output_folder = output_folder
        self._template_name = template_name
        self._cache: dict[str, Path] = {}

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def get_project_root(self) -> Path:
        """
        Development-only helper.

        Walk upward from this file to find the project root. Useful for tests
        and local tooling, not relied upon in packaged runtime.

        Example
        -------
        root = path_manager.get_project_root()
        print(root / "pyproject.toml")
        """
        if "project_root" not in self._cache:
            current = Path(__file__).resolve().parent
            while current.parent != current:
                if (current / "pyproject.toml").exists() or (current / "setup.py").exists():
                    self._cache["project_root"] = current
                    break
                if (current / "src" / "deckbuilder").exists():
                    self._cache["project_root"] = current
                    break
                current = current.parent
            else:
                # Fallback: assume src/deckbuilder is 3 levels up
                self._cache["project_root"] = Path(__file__).resolve().parents[3]
        return self._cache["project_root"]

    def _assets_traversable(self):
        """
        Get a Traversable pointing to deckbuilder/assets inside the package.

        Works for wheels/zips without assuming a real filesystem path.

        Example
        -------
        t = (files("deckbuilder") / "assets").joinpath("templates")
        for p in t.iterdir(): print(p)
        """
        return files("deckbuilder") / "assets"

    def _materialise_assets_to(self, target: Path) -> Path:
        """
        Copy all assets to a real directory so they can be used by libraries
        that require real paths (e.g., python-pptx, file watchers).

        Idempotent: does nothing if target already exists.

        Example
        -------
        cached = path_manager._materialise_assets_to(Path("/tmp/db-assets"))
        print(cached / "templates" / "default.pptx")
        """
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            assets = self._assets_traversable()
            for entry in assets.rglob("*"):
                rel = Path(*entry.parts[entry.parts.index("assets") + 1 :])
                out = target / rel
                if entry.is_dir():
                    out.mkdir(parents=True, exist_ok=True)
                else:
                    out.parent.mkdir(parents=True, exist_ok=True)
                    with entry.open("rb") as src, open(out, "wb") as dst:
                        dst.write(src.read())
        return target

    def _materialised_assets_root(self) -> Path:
        """
        Resolve the base directory where assets are materialised.

        Defaults to .deckbuilder_assets in the current working directory,
        override with DECK_ASSET_CACHE_DIR.

        Example
        -------
        # Prefer a tmp cache during CI:
        #   DECK_ASSET_CACHE_DIR=/tmp/db-assets pytest
        """
        base = Path(os.getenv("DECK_ASSET_CACHE_DIR", Path.cwd() / ".deckbuilder_assets"))
        return self._materialise_assets_to(base)

    # -------------------------------------------------------------------------
    # Public API: asset locations
    # -------------------------------------------------------------------------

    def get_assets_templates_path(self) -> Path:
        """
        Real filesystem path to assets/templates (materialised if needed).

        Example
        -------
        tmpl_dir = path_manager.get_assets_templates_path()
        for p in tmpl_dir.glob("*.pptx"): print(p)
        """
        return self._materialised_assets_root() / "templates"

    def get_master_presentation_files_path(self) -> Path:
        """
        Real filesystem path to assets/ (where master files live).

        Example
        -------
        assets_root = path_manager.get_master_presentation_files_path()
        print((assets_root / "master_default_presentation.json").is_file())
        """
        return self._materialised_assets_root()

    def get_master_presentation_files(self) -> Tuple[Path, Path]:
        """
        Return real paths to master_default_presentation.md and .json
        for use in examples/tests.

        Example
        -------
        md, js = path_manager.get_master_presentation_files()
        print(md.read_text()[:120], js.read_text()[:120])
        """
        assets = self.get_master_presentation_files_path()
        return (
            assets / "master_default_presentation.md",
            assets / "master_default_presentation.json",
        )

    def get_test_files(self) -> Tuple[Path, Path]:
        """
        Return paths to the test copies of the master files.

        Example
        -------
        md, js = path_manager.get_test_files()
        """
        project_root = self.get_project_root()
        test_dir = project_root / "tests" / "deckbuilder"
        return (
            test_dir / "test_comprehensive_layouts.md",
            test_dir / "test_comprehensive_layouts.json",
        )

    # -------------------------------------------------------------------------
    # Public API: folder and file resolution
    # -------------------------------------------------------------------------

    def get_template_folder(self) -> Path:
        """
        Resolve the template folder path according to context precedence rules.

        Examples
        --------
        # Library default → packaged assets:
        print(create_library_path_manager().get_template_folder())

        # CLI → args beat env
        print(create_cli_path_manager("/path/to/templates").get_template_folder())

        # MCP → env required
        #   DECK_TEMPLATE_FOLDER=/path/to/templates  python -c ...
        """
        if self._context == "cli":
            if self._template_folder:
                return Path(self._template_folder).resolve()
            env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            return Path(env_folder).resolve() if env_folder else (Path.cwd() / "templates")

        if self._context == "mcp":
            env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()
            raise ValueError("MCP context requires DECK_TEMPLATE_FOLDER to be set")

        # library context
        if self._template_folder:
            return Path(self._template_folder).resolve()
        env_folder = os.getenv("DECK_TEMPLATE_FOLDER")
        if env_folder:
            return Path(env_folder).resolve()
        return self.get_assets_templates_path()

    def get_output_folder(self) -> Path:
        """
        Resolve the output folder path according to context precedence rules.

        Examples
        --------
        # CLI → CWD
        print(create_cli_path_manager().get_output_folder())

        # Library → args/env/CWD
        print(create_library_path_manager(output_folder="/tmp/out").get_output_folder())
        """
        if self._context == "cli":
            return Path.cwd()

        if self._context == "mcp":
            env_folder = os.getenv("DECK_OUTPUT_FOLDER")
            if env_folder:
                return Path(env_folder).resolve()
            raise ValueError("MCP context requires DECK_OUTPUT_FOLDER to be set")

        # library context
        if self._output_folder:
            return Path(self._output_folder).resolve()
        env_folder = os.getenv("DECK_OUTPUT_FOLDER")
        return Path(env_folder).resolve() if env_folder else Path.cwd()

    def get_template_name(self) -> str:
        """
        Return the active template name.

        Example
        -------
        # explicit > env > default("default")
        print(create_library_path_manager(template_name="corp").get_template_name())
        """
        return self._template_name or os.getenv("DECK_TEMPLATE_NAME") or "default"

    def get_template_file_path(self, template_name: Optional[str] = None) -> Path:
        """
        Full path to a template .pptx file.

        Example
        -------
        pm = create_library_path_manager(template_name="default")
        print(pm.get_template_file_path())  # .../default.pptx
        """
        name = (template_name or self.get_template_name()).removesuffix(".pptx")
        return self.get_template_folder() / f"{name}.pptx"

    # Legacy get_template_json_path method removed - template mapping JSON files no longer used

    # -------------------------------------------------------------------------
    # Public API: validation / discovery
    # -------------------------------------------------------------------------

    def validate_template_exists(self, template_name: Optional[str] = None) -> bool:
        """
        Check if a template .pptx file exists.

        Example
        -------
        assert path_manager.validate_template_exists("default")
        """
        return self.get_template_file_path(template_name).exists()

    def validate_template_folder_exists(self) -> bool:
        """
        Check if the template folder exists.

        Example
        -------
        assert path_manager.validate_template_folder_exists()
        """
        return self.get_template_folder().exists()

    def validate_assets_exist(self) -> bool:
        """
        Check if packaged default template assets exist.

        Example
        -------
        assert path_manager.validate_assets_exist()
        """
        root = self.get_master_presentation_files_path()
        return (root / "templates").is_dir() and (root / "templates" / "default.pptx").is_file()

    def list_available_templates(self) -> list[str]:
        """
        List template names based on .pptx files in the active template folder.

        Example
        -------
        print(path_manager.list_available_templates())  # ['default', ...]
        """
        folder = self.get_template_folder()
        return sorted(p.stem for p in folder.glob("*.pptx")) if folder.exists() else []

    def get_version(self) -> str:
        """
        Read package version from installed metadata, else from pyproject.toml,
        else return a hardcoded fallback.

        Example
        -------
        print(path_manager.get_version())
        """
        try:
            from importlib.metadata import version

            return version("deckbuilder")
        except Exception:  # nosec B110
            pass
        try:
            import tomllib

            pyproject = self.get_project_root() / "pyproject.toml"
            if pyproject.exists():
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                return data.get("project", {}).get("version", "unknown")
        except Exception:  # nosec B110
            pass
        return "1.3.0"


# Factory helpers for convenience
def create_cli_path_manager(template_folder: Optional[str] = None) -> PathManager:
    """CLI context: args > env > CWD/templates"""
    return PathManager(context="cli", template_folder=template_folder)


def create_mcp_path_manager() -> PathManager:
    """MCP context: env only (else error)"""
    return PathManager(context="mcp")


def create_library_path_manager(
    template_folder: Optional[str] = None,
    output_folder: Optional[str] = None,
    template_name: Optional[str] = None,
) -> PathManager:
    """Library context: args > env > packaged assets/templates"""
    return PathManager("library", template_folder, output_folder, template_name)


# Default global instance (library context)
path_manager = PathManager("library")


def get_placekitten():
    """Import and return PlaceKitten class with proper path setup.

    This utility function ensures DRY principle by centralizing the
    sys.path manipulation needed to import placekitten from sibling package.

    Returns:
        PlaceKitten class from the placekitten package
    """
    import sys
    from pathlib import Path

    # Add src directory to path if not already present
    src_path = str(Path(__file__).parent.parent.parent)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    from placekitten import PlaceKitten  # noqa: E402

    return PlaceKitten
