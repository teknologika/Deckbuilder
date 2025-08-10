#!/usr/bin/env python3
"""
Pattern Loader for User-Supplied Pattern Support

Loads and manages structured frontmatter patterns from multiple sources:
- Built-in patterns from structured_frontmatter_patterns/ directory
- User patterns from {DECK_TEMPLATE_FOLDER}/patterns/ subfolder

Implements pattern discovery, validation, and override behavior.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/39
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from .pattern_schema import PatternSchemaValidator


class PatternLoader:
    """
    Dynamic pattern loader with user customization support.

    Discovers and loads structured frontmatter patterns from built-in
    and user-supplied directories with intelligent override behavior.
    """

    def __init__(self, template_folder: Optional[Union[str, Path]] = None):
        """
        Initialize PatternLoader with template folder path.

        Args:
            template_folder: Path to template folder. If None, uses DECK_TEMPLATE_FOLDER
                           environment variable or default location.
        """
        self.logger = logging.getLogger(__name__)

        # Initialize pattern validator
        self.validator = PatternSchemaValidator()

        # Determine template folder path
        if template_folder:
            self.template_folder = Path(template_folder)
        else:
            # Use environment variable or default location
            env_template_folder = os.getenv("DECK_TEMPLATE_FOLDER")
            if env_template_folder:
                self.template_folder = Path(env_template_folder)
            else:
                # Default to built-in templates
                self.template_folder = Path(__file__).parent / "assets" / "templates"

        # Built-in patterns directory (one level up from templates/)
        self.builtin_patterns_dir = Path(__file__).parent.parent / "structured_frontmatter_patterns"

        # User patterns directory (within template folder)
        self.user_patterns_dir = self.template_folder / "patterns"

        # Pattern cache for performance
        self._pattern_cache: Dict[str, Dict[str, Any]] = {}

        self.logger.debug(f"PatternLoader initialized with template folder: {self.template_folder}")

    def load_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all patterns from built-in and user directories.

        Returns:
            Dictionary mapping layout names to pattern data
        """
        if self._pattern_cache:
            return self._pattern_cache

        patterns = {}

        # Load built-in patterns first
        builtin_patterns = self._load_builtin_patterns()
        patterns.update(builtin_patterns)

        # Load user patterns (override built-in if same layout name)
        user_patterns = self._load_user_patterns()
        patterns.update(user_patterns)

        # Cache for performance
        self._pattern_cache = patterns

        self.logger.info(f"Loaded {len(patterns)} patterns ({len(builtin_patterns)} built-in, {len(user_patterns)} user)")

        return patterns

    def _load_builtin_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load patterns from built-in structured_frontmatter_patterns directory."""
        patterns = {}

        if not self.builtin_patterns_dir.exists():
            self.logger.warning(f"Built-in patterns directory not found: {self.builtin_patterns_dir}")
            return patterns

        for pattern_file in self.builtin_patterns_dir.glob("*.json"):
            try:
                pattern_data = self._load_pattern_file(pattern_file)

                if pattern_data:
                    # Get layout name from the pattern data itself, not filename
                    layout_name = pattern_data.get("yaml_pattern", {}).get("layout")

                    if layout_name:
                        patterns[layout_name] = pattern_data
                        self.logger.debug(f"Loaded built-in pattern: {layout_name} from {pattern_file.name}")
                    else:
                        self.logger.warning(f"Pattern {pattern_file} missing layout name in yaml_pattern.layout")

            except Exception as e:
                self.logger.error(f"Error loading built-in pattern {pattern_file}: {e}")

        return patterns

    def _load_user_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load patterns from user patterns directory."""
        patterns = {}

        if not self.user_patterns_dir.exists():
            self.logger.debug(f"User patterns directory not found: {self.user_patterns_dir}")
            return patterns

        for pattern_file in self.user_patterns_dir.glob("*.json"):
            try:
                pattern_data = self._load_pattern_file(pattern_file)

                if pattern_data:
                    # Get layout name from the pattern data itself, not filename
                    layout_name = pattern_data.get("yaml_pattern", {}).get("layout")

                    if layout_name:
                        patterns[layout_name] = pattern_data
                        self.logger.info(f"Loaded user pattern: {layout_name} from {pattern_file.name} (overrides built-in)")
                    else:
                        self.logger.warning(f"User pattern {pattern_file} missing layout name in yaml_pattern.layout")

            except Exception as e:
                self.logger.error(f"Error loading user pattern {pattern_file}: {e}")

        return patterns

    def find_pattern_file_for_layout(self, layout_name: str) -> Optional[Path]:
        """
        Find the pattern file that defines a specific layout.

        This scans all pattern files to find one with matching yaml_pattern.layout value.
        Used for reverse lookup when users want to override a specific layout.
        """
        # Check built-in patterns first
        if self.builtin_patterns_dir.exists():
            for pattern_file in self.builtin_patterns_dir.glob("*.json"):
                try:
                    pattern_data = self._load_pattern_file(pattern_file)
                    if pattern_data and pattern_data.get("yaml_pattern", {}).get("layout") == layout_name:
                        return pattern_file
                except Exception:  # nosec B112
                    continue

        # Check user patterns
        if self.user_patterns_dir.exists():
            for pattern_file in self.user_patterns_dir.glob("*.json"):
                try:
                    pattern_data = self._load_pattern_file(pattern_file)
                    if pattern_data and pattern_data.get("yaml_pattern", {}).get("layout") == layout_name:
                        return pattern_file
                except Exception:  # nosec B112
                    continue

        return None

    def _load_pattern_file(self, pattern_file: Path) -> Optional[Dict[str, Any]]:
        """Load and validate a single pattern file with comprehensive schema validation."""
        try:
            with open(pattern_file, "r", encoding="utf-8") as f:
                pattern_data = json.load(f)

            # Comprehensive schema validation
            validation_errors = self.validator.validate_pattern(pattern_data)

            if validation_errors:
                self.logger.error(f"Pattern validation failed for {pattern_file}:")
                for error in validation_errors:
                    self.logger.error(f"  - {error}")
                return None

            return pattern_data

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in pattern file {pattern_file}: {e}")
            return None
        except PermissionError:
            self.logger.error(f"Permission denied accessing pattern file {pattern_file}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading pattern file {pattern_file}: {e}")
            return None

    def get_pattern_for_layout(self, layout_name: str) -> Optional[Dict[str, Any]]:
        """Get pattern data for a specific layout name."""
        patterns = self.load_patterns()
        return patterns.get(layout_name)

    def get_layout_names(self) -> List[str]:
        """Get list of all available layout names."""
        patterns = self.load_patterns()
        return list(patterns.keys())

    def get_patterns_by_file_source(self) -> Dict[str, Dict[str, Any]]:
        """
        Get patterns organized by their source (built-in vs user).

        Returns:
            Dictionary with 'builtin' and 'user' keys containing pattern data
        """
        return {"builtin": self._load_builtin_patterns(), "user": self._load_user_patterns()}

    def clear_cache(self) -> None:
        """Clear pattern cache to force reloading."""
        self._pattern_cache.clear()
        self.logger.debug("Pattern cache cleared")

    def validate_all_patterns(self) -> Dict[str, List[str]]:
        """
        Validate all pattern files in both built-in and user directories.

        Returns:
            Dictionary mapping file paths to validation errors (empty if valid)
        """
        validation_results = {}

        # Validate built-in patterns
        if self.builtin_patterns_dir.exists():
            builtin_results = self.validator.validate_all_patterns(self.builtin_patterns_dir)
            for filename, errors in builtin_results.items():
                validation_results[f"builtin:{filename}"] = errors

        # Validate user patterns
        if self.user_patterns_dir.exists():
            user_results = self.validator.validate_all_patterns(self.user_patterns_dir)
            for filename, errors in user_results.items():
                validation_results[f"user:{filename}"] = errors

        return validation_results

    def validate_pattern_file(self, pattern_file: Path) -> List[str]:
        """
        Validate a specific pattern file.

        Args:
            pattern_file: Path to pattern file to validate

        Returns:
            List of validation errors (empty if valid)
        """
        return self.validator.validate_pattern_file(pattern_file)
