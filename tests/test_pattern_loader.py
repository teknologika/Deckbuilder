#!/usr/bin/env python3
"""
TDD Tests for User-Supplied Pattern Support

These tests define the expected behavior for the pattern loading system before implementation.
Following TDD methodology: write failing tests first, then implement to make them pass.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/39
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestPatternLoader:
    """Test PatternLoader class for dynamic pattern discovery and loading."""
    
    def test_pattern_loader_class_exists(self):
        """Test that PatternLoader class exists and is importable."""
        # PatternLoader class should now be importable
        
        from src.deckbuilder.pattern_loader import PatternLoader
        
        # Should be able to create an instance
        loader = PatternLoader()
        assert loader is not None
        assert hasattr(loader, 'load_patterns')
        assert hasattr(loader, 'get_pattern_for_layout')
    
    def test_pattern_loader_initialization(self):
        """Test PatternLoader can be initialized with template folder."""
        from src.deckbuilder.pattern_loader import PatternLoader
        
        # Test initialization with template folder path
        test_folder = "/tmp/test_templates"
        loader = PatternLoader(test_folder)
        
        assert loader.template_folder == Path(test_folder)
        assert loader.user_patterns_dir == Path(test_folder) / "patterns"
        assert hasattr(loader, 'builtin_patterns_dir')
        
        # Test initialization without folder (should use defaults)
        loader_default = PatternLoader()
        assert loader_default.template_folder is not None
    
    def test_load_built_in_patterns_only(self):
        """Test loading built-in patterns when no user patterns exist."""
        from src.deckbuilder.pattern_loader import PatternLoader
        
        # Create loader with a temp folder (no user patterns)
        loader = PatternLoader("/tmp/nonexistent")
        
        # Load patterns - should get built-in patterns only
        patterns = loader.load_patterns()
        
        # Should have loaded some built-in patterns
        assert len(patterns) > 0
        
        # Check that specific expected patterns exist
        assert "Four Columns" in patterns
        assert "Comparison" in patterns
        
        # Verify pattern structure for Four Columns
        four_columns = patterns["Four Columns"]
        assert "description" in four_columns
        assert "yaml_pattern" in four_columns
        assert "validation" in four_columns
        assert "example" in four_columns
        
        # Verify pattern structure for Comparison
        comparison = patterns["Comparison"]
        assert "description" in comparison
        assert comparison["description"] == "Side-by-side comparison layout for contrasting two options"
    
    def test_load_user_patterns_from_subfolder(self, tmp_path):
        """Test loading user patterns from {template_folder}/patterns/ subfolder."""
        from src.deckbuilder.pattern_loader import PatternLoader
        
        # Setup: Create template folder with patterns subfolder
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()
        
        # Create user pattern file
        user_pattern = {
            "description": "User custom layout",
            "yaml_pattern": {"layout": "Custom Layout", "title": "str", "content": "str"},
            "validation": {"required_fields": ["title", "content"]},
            "example": "---\nlayout: Custom Layout\ntitle: Example\ncontent: Content\n---"
        }
        
        custom_pattern_file = patterns_folder / "custom_layout.json"
        with open(custom_pattern_file, 'w') as f:
            json.dump(user_pattern, f)
        
        # Create PatternLoader with this template folder
        loader = PatternLoader(template_folder)
        
        # Load patterns - should include both built-in and user patterns
        patterns = loader.load_patterns()
        
        # Should have both built-in and user patterns
        assert len(patterns) > 0
        
        # Should include the custom user pattern
        assert "Custom Layout" in patterns
        
        # Verify the user pattern was loaded correctly
        custom = patterns["Custom Layout"]
        assert custom["description"] == "User custom layout"
        assert custom["yaml_pattern"]["layout"] == "Custom Layout"
        assert "title" in custom["validation"]["required_fields"]
    
    def test_user_patterns_override_built_in_patterns(self, tmp_path):
        """Test that user patterns override built-in patterns with same layout name."""
        from src.deckbuilder.pattern_loader import PatternLoader
        
        # Setup: Create user pattern that overrides "Four Columns"
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()
        
        # User override for "Four Columns" layout
        user_override = {
            "description": "Custom four-column layout with user modifications",
            "yaml_pattern": {
                "layout": "Four Columns", 
                "title": "str",
                "col1": "str",  # Different field names
                "col2": "str",
                "col3": "str", 
                "col4": "str"
            },
            "validation": {"required_fields": ["title", "col1", "col2", "col3", "col4"]},
            "example": "---\nlayout: Four Columns\ntitle: Custom Example\ncol1: Custom content\n---"
        }
        
        override_file = patterns_folder / "four_columns.json"
        with open(override_file, 'w') as f:
            json.dump(user_override, f)
        
        # Create PatternLoader with this template folder
        loader = PatternLoader(template_folder)
        
        # Load patterns
        patterns = loader.load_patterns()
        
        # Should have "Four Columns" pattern
        assert "Four Columns" in patterns
        
        # Should be the user override, not the built-in pattern
        four_columns = patterns["Four Columns"]
        assert four_columns["description"] == "Custom four-column layout with user modifications"
        
        # Should use user's field names (col1, col2, etc.) not built-in (content_col1, content_col2, etc.)
        required_fields = four_columns["validation"]["required_fields"]
        assert "col1" in required_fields
        assert "col2" in required_fields
        assert "content_col1" not in required_fields  # Should not have built-in field names
    
    def test_layout_names_from_pattern_files(self):
        """Test that layout names are read from pattern files, not hard-coded."""
        from src.deckbuilder.pattern_loader import PatternLoader
        
        loader = PatternLoader("/tmp/nonexistent")  # Force built-in patterns only
        
        # Load patterns and verify they contain expected layout names from the files
        patterns = loader.load_patterns()
        
        # These are the layout names that should be defined in the pattern files themselves
        # (in the yaml_pattern.layout field of each JSON file)
        expected_layouts = {
            "Four Columns",
            "Three Columns", 
            "Four Columns With Titles",
            "Comparison",
            "SWOT Analysis",
            "Picture with Caption",
            "Two Content",
            "Title and Vertical Text",
            "Vertical Title and Text",
            "Agenda, 6 Textboxes",
            "Title and 6-item Lists"
        }
        
        # Verify that patterns were loaded based on their internal layout names
        actual_layouts = set(patterns.keys())
        
        # Should have at least some of the expected layouts (the files that exist)
        intersection = expected_layouts.intersection(actual_layouts)
        assert len(intersection) > 0, f"No expected layouts found. Got: {actual_layouts}"
        
        # Verify that each pattern's yaml_pattern.layout matches the key
        for layout_name, pattern_data in patterns.items():
            pattern_layout = pattern_data.get('yaml_pattern', {}).get('layout')
            assert pattern_layout == layout_name, f"Pattern key '{layout_name}' doesn't match yaml_pattern.layout '{pattern_layout}'"
            
        # Test find_pattern_file_for_layout method
        for layout_name in patterns.keys():
            pattern_file = loader.find_pattern_file_for_layout(layout_name)
            assert pattern_file is not None, f"Could not find pattern file for layout: {layout_name}"
    
    def test_pattern_validation_for_safety(self, tmp_path):
        """Test that user patterns are validated for required fields and safety."""
        # This test will FAIL until we implement pattern validation
        
        # Setup: Create invalid user pattern
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()
        
        # Invalid pattern missing required fields
        invalid_pattern = {
            "description": "Invalid pattern"
            # Missing yaml_pattern, validation, example
        }
        
        invalid_file = patterns_folder / "invalid_pattern.json"
        with open(invalid_file, 'w') as f:
            json.dump(invalid_pattern, f)
        
        # Expected behavior: PatternLoader validates patterns and reports errors
        
        assert False, "Pattern validation for safety not implemented"
    
    def test_graceful_fallback_for_missing_patterns(self):
        """Test graceful handling when pattern file doesn't exist for a layout."""
        # This test will FAIL until we implement fallback behavior
        
        # Expected behavior: When PowerPoint layout has no corresponding pattern file,
        # system should gracefully fall back to basic layout info without pattern data
        
        assert False, "Graceful fallback for missing patterns not implemented"


class TestPatternLoaderIntegration:
    """Test PatternLoader integration with existing systems."""
    
    def test_integration_with_template_metadata_loader(self):
        """Test PatternLoader integrates with TemplateMetadataLoader."""
        # This test will FAIL until we implement integration
        
        # Expected behavior: TemplateMetadataLoader uses PatternLoader for 
        # layout descriptions instead of hard-coded generation
        
        assert False, "PatternLoader integration with TemplateMetadataLoader not implemented"
    
    @pytest.mark.asyncio 
    async def test_integration_with_get_template_layouts_mcp_tool(self):
        """Test PatternLoader provides data to get_template_layouts() MCP tool."""
        import os
        import json
        from pathlib import Path
        
        # Set up environment variables for MCP server
        original_env = os.environ.copy()
        try:
            os.environ['DECK_OUTPUT_FOLDER'] = '/tmp/test_output'
            os.environ['DECK_TEMPLATE_FOLDER'] = str(Path(__file__).parent.parent / 'src' / 'deckbuilder' / 'assets' / 'templates')
            os.environ['DECK_TEMPLATE_NAME'] = 'default'
            
            # Import and test the actual MCP tool
            from src.mcp_server.main import get_template_layouts
            
            # Create a real context object (not a mock)
            class TestContext:
                pass
            
            ctx = TestContext()
            result = await get_template_layouts(ctx, 'default')
            
            # Should return valid JSON
            assert isinstance(result, str)
            data = json.loads(result)
            
            # Should have expected structure
            assert "template_name" in data
            assert "layouts" in data
            assert data["template_name"] == "default"
            
            # Should have layouts with pattern data
            layouts = data["layouts"]
            assert len(layouts) > 0
            
            # Check if layouts with pattern files are using pattern descriptions
            pattern_layouts_found = False
            for layout_name, layout_info in layouts.items():
                if layout_name in ["Four Columns", "Comparison"]:
                    pattern_layouts_found = True
                    
                    # Should have description from pattern file, not hard-coded
                    description = layout_info.get("description", "")
                    assert len(description) > 0
                    
                    # Verify it's using pattern description by checking for specific pattern text
                    if layout_name == "Four Columns":
                        assert "four-column" in description.lower() or "content only" in description.lower()
                    elif layout_name == "Comparison":
                        assert "side-by-side" in description.lower() or "comparison" in description.lower()
                    
                    # Should have required_placeholders from pattern validation
                    required = layout_info.get("required_placeholders", [])
                    assert len(required) > 0
                    
                    # Should have example (either from pattern or fallback)
                    example = layout_info.get("example", {})
                    assert len(example) > 0
            
            assert pattern_layouts_found, "No layouts with pattern files found for testing"
            
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)
    
    def test_pattern_data_replaces_hard_coded_examples(self):
        """Test that pattern examples replace hard-coded layout generation."""
        # This test will FAIL until we remove hard-coded functions
        
        # Expected behavior: No more hard-coded example generation in:
        # - _generate_layout_example()
        # - _get_title_example_for_layout() 
        # - _get_content_example_for_layout()
        
        assert False, "Hard-coded example generation removal not implemented"
    
    def test_backward_compatibility_without_user_patterns(self):
        """Test system works normally when no user patterns folder exists."""
        # This test will FAIL until we implement backward compatibility
        
        # Expected behavior: System loads only built-in patterns and works normally
        # when {template_folder}/patterns/ doesn't exist
        
        assert False, "Backward compatibility without user patterns not implemented"


class TestPatternLoaderErrorHandling:
    """Test PatternLoader error handling and edge cases."""
    
    def test_invalid_json_in_user_pattern_file(self, tmp_path):
        """Test handling of invalid JSON in user pattern files."""
        # This test will FAIL until we implement error handling
        
        # Setup: Create pattern file with invalid JSON
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()
        
        invalid_file = patterns_folder / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write('{"invalid": json}')  # Invalid JSON syntax
        
        # Expected behavior: PatternLoader handles JSON errors gracefully
        
        assert False, "Invalid JSON error handling not implemented"
    
    def test_permission_errors_on_pattern_files(self, tmp_path):
        """Test handling of file permission errors."""
        # This test will FAIL until we implement permission error handling
        
        # Expected behavior: PatternLoader handles permission errors gracefully
        # and continues loading other patterns
        
        assert False, "Permission error handling not implemented"
    
    def test_pattern_file_schema_validation(self, tmp_path):
        """Test validation of pattern file schema and required fields."""
        # This test will FAIL until we implement schema validation
        
        # Setup: Create pattern with wrong schema
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()
        
        wrong_schema = {
            "wrong_field": "value",
            "missing_required_fields": True
        }
        
        wrong_file = patterns_folder / "wrong_schema.json"
        with open(wrong_file, 'w') as f:
            json.dump(wrong_schema, f)
        
        # Expected behavior: PatternLoader validates schema and reports specific errors
        
        assert False, "Pattern file schema validation not implemented"


class TestPatternLoaderPerformance:
    """Test PatternLoader performance and caching."""
    
    def test_pattern_loading_performance(self):
        """Test that pattern loading is performant for multiple calls."""
        # This test will FAIL until we implement performance optimization
        
        # Expected behavior: Pattern loading should be cached to avoid 
        # repeated file system access for same template folder
        
        assert False, "Pattern loading performance optimization not implemented"
    
    def test_pattern_cache_invalidation(self):
        """Test that pattern cache is invalidated when files change."""
        # This test will FAIL until we implement cache invalidation
        
        # Expected behavior: If pattern files are modified, cache should 
        # be invalidated and patterns reloaded
        
        assert False, "Pattern cache invalidation not implemented"


if __name__ == "__main__":
    # Run the failing tests to verify TDD setup
    pytest.main([__file__, "-v", "--tb=short"])