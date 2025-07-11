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
        
        # Determine template folder path
        if template_folder:
            self.template_folder = Path(template_folder)
        else:
            # Use environment variable or default location
            env_template_folder = os.getenv('DECK_TEMPLATE_FOLDER')
            if env_template_folder:
                self.template_folder = Path(env_template_folder)
            else:
                # Default to built-in templates
                self.template_folder = Path(__file__).parent / "assets" / "templates"
        
        # Built-in patterns directory
        self.builtin_patterns_dir = Path(__file__).parent / "structured_frontmatter_patterns"
        
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
                layout_name = self._pattern_file_to_layout_name(pattern_file.stem)
                pattern_data = self._load_pattern_file(pattern_file)
                
                if pattern_data:
                    patterns[layout_name] = pattern_data
                    self.logger.debug(f"Loaded built-in pattern: {layout_name}")
                    
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
                layout_name = self._pattern_file_to_layout_name(pattern_file.stem)
                pattern_data = self._load_pattern_file(pattern_file)
                
                if pattern_data:
                    patterns[layout_name] = pattern_data
                    self.logger.info(f"Loaded user pattern: {layout_name} (overrides built-in)")
                    
            except Exception as e:
                self.logger.error(f"Error loading user pattern {pattern_file}: {e}")
        
        return patterns
    
    def _pattern_file_to_layout_name(self, file_stem: str) -> str:
        """
        Convert pattern filename to PowerPoint layout name.
        
        Examples:
            "four_columns" -> "Four Columns"
            "comparison" -> "Comparison" 
            "swot_analysis" -> "SWOT Analysis"
        """
        # Split by underscores and title case each word
        words = file_stem.split('_')
        
        # Handle special cases
        if file_stem == "swot_analysis":
            return "SWOT Analysis"
        elif file_stem == "title_and_6_item_lists":
            return "Title and 6-item Lists"
        elif "columns" in file_stem and "with" in file_stem and "titles" in file_stem:
            # four_columns_with_titles -> Four Columns With Titles
            return " ".join(word.title() for word in words)
        elif "columns" in file_stem:
            # four_columns -> Four Columns
            return " ".join(word.title() for word in words)
        elif "and" in words:
            # title_and_vertical_text -> Title and Vertical Text
            # vertical_title_and_text -> Vertical Title and Text  
            return " ".join(word if word == "and" else word.title() for word in words)
        elif file_stem.startswith("agenda"):
            # agenda_6_textboxes -> Agenda, 6 Textboxes
            if "6" in words:
                return "Agenda, 6 Textboxes"
        elif file_stem == "picture_with_caption":
            return "Picture with Caption"
        else:
            # Default: title case each word
            return " ".join(word.title() for word in words)
    
    def _load_pattern_file(self, pattern_file: Path) -> Optional[Dict[str, Any]]:
        """Load and validate a single pattern file."""
        try:
            with open(pattern_file, 'r', encoding='utf-8') as f:
                pattern_data = json.load(f)
            
            # Basic validation - check for required fields
            required_fields = ['description', 'yaml_pattern', 'validation', 'example']
            missing_fields = [field for field in required_fields if field not in pattern_data]
            
            if missing_fields:
                self.logger.warning(f"Pattern {pattern_file} missing required fields: {missing_fields}")
                return None
            
            return pattern_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in pattern file {pattern_file}: {e}")
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
    
    def layout_name_to_pattern_file(self, layout_name: str) -> str:
        """
        Convert PowerPoint layout name to pattern filename.
        
        Examples:
            "Four Columns" -> "four_columns.json"
            "Comparison" -> "comparison.json"
            "SWOT Analysis" -> "swot_analysis.json"
        """
        # Handle special cases first
        if layout_name == "Agenda, 6 Textboxes":
            return "agenda_6_textboxes.json"
        elif layout_name == "Title and 6-item Lists":
            return "title_and_6_item_lists.json"
        elif layout_name.startswith("Title and"):
            # Keep "and" lowercase: "Title and Vertical Text" -> "title_and_vertical_text"
            file_name = layout_name.replace(" and ", "_and_").lower().replace(' ', '_')
        elif layout_name == "Picture with Caption":
            return "picture_with_caption.json"
        else:
            # Convert to lowercase and replace spaces with underscores
            file_name = layout_name.lower().replace(' ', '_')
        
        return f"{file_name}.json"
    
    def clear_cache(self) -> None:
        """Clear pattern cache to force reloading."""
        self._pattern_cache.clear()
        self.logger.debug("Pattern cache cleared")