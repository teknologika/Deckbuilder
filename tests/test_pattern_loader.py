"""
TDD Tests for User-Supplied Pattern Support

These tests define the expected behavior for the pattern loading system before implementation.
Following TDD methodology: write failing tests first, then implement to make them pass.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/39
"""

import pytest
import json
from pathlib import Path


class TestPatternLoader:
    """Test PatternLoader class for dynamic pattern discovery and loading."""

    def test_pattern_loader_class_exists(self):
        """Test that PatternLoader class exists and is importable."""
        # PatternLoader class should now be importable

        from deckbuilder.templates.pattern_loader import PatternLoader

        # Should be able to create an instance
        loader = PatternLoader()
        assert loader is not None
        assert hasattr(loader, "load_patterns")
        assert hasattr(loader, "get_pattern_for_layout")

    def test_pattern_loader_initialization(self):
        """Test PatternLoader can be initialized with template folder."""
        from deckbuilder.templates.pattern_loader import PatternLoader

        # Test initialization with template folder path
        test_folder = "/tmp/test_templates"
        loader = PatternLoader(test_folder)

        assert loader.template_folder == Path(test_folder)
        assert loader.user_patterns_dir == Path(test_folder) / "patterns"
        assert hasattr(loader, "builtin_patterns_dir")

        # Test initialization without folder (should use defaults)
        loader_default = PatternLoader()
        assert loader_default.template_folder is not None

    def test_load_built_in_patterns_only(self):
        """Test loading built-in patterns when no user patterns exist."""
        from deckbuilder.templates.pattern_loader import PatternLoader

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
        from deckbuilder.templates.pattern_loader import PatternLoader

        # Setup: Create template folder with patterns subfolder
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()

        # Create user pattern file
        user_pattern = {
            "description": "User custom layout",
            "yaml_pattern": {"layout": "Custom Layout", "title_top": "str", "content": "str"},
            "validation": {"required_fields": ["title_top", "content"]},
            "example": "---\nlayout: Custom Layout\ntitle_top: Example\ncontent: Content\n---",
        }

        custom_pattern_file = patterns_folder / "custom_layout.json"
        with open(custom_pattern_file, "w") as f:
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
        assert "title_top" in custom["validation"]["required_fields"]

    def test_user_patterns_override_built_in_patterns(self, tmp_path):
        """Test that user patterns override built-in patterns with same layout name."""
        from deckbuilder.templates.pattern_loader import PatternLoader

        # Setup: Create user pattern that overrides "Four Columns"
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()

        # User override for "Four Columns" layout
        user_override = {
            "description": "Custom four-column layout with user modifications",
            "yaml_pattern": {"layout": "Four Columns", "title": "str", "col1": "str", "col2": "str", "col3": "str", "col4": "str"},  # Different field names
            "validation": {"required_fields": ["title", "col1", "col2", "col3", "col4"]},
            "example": "---\nlayout: Four Columns\ntitle: Custom Example\ncol1: Custom content\n---",
        }

        override_file = patterns_folder / "four_columns.json"
        with open(override_file, "w") as f:
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
        from deckbuilder.templates.pattern_loader import PatternLoader

        loader = PatternLoader("/tmp/nonexistent")  # Force built-in patterns only

        # Load patterns and verify they contain expected layout names from the files
        patterns = loader.load_patterns()

        # These are the layout names that should be defined in the pattern files themselves
        # (in the yaml_pattern.layout field of each JSON file)
        # Now includes semantic aliases for improved discoverability
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
            "Title and 6-item Lists",
            # Semantic aliases for improved layout discoverability
            "pros_and_cons",
            "before_and_after",
            "problem_solution",
            "timeline",
            "process_steps",
            "team_members",
            "key_metrics",
        }

        # Verify that patterns were loaded based on their internal layout names
        actual_layouts = set(patterns.keys())

        # Should have at least some of the expected layouts (the files that exist)
        intersection = expected_layouts.intersection(actual_layouts)
        assert len(intersection) > 0, f"No expected layouts found. Got: {actual_layouts}"

        # Verify that each pattern's yaml_pattern.layout matches the key
        for layout_name, pattern_data in patterns.items():
            pattern_layout = pattern_data.get("yaml_pattern", {}).get("layout")
            assert pattern_layout == layout_name, f"Pattern key '{layout_name}' doesn't match yaml_pattern.layout '{pattern_layout}'"

        # Test find_pattern_file_for_layout method
        for layout_name in patterns.keys():
            pattern_file = loader.find_pattern_file_for_layout(layout_name)
            assert pattern_file is not None, f"Could not find pattern file for layout: {layout_name}"

    def test_pattern_validation_for_safety(self, tmp_path):
        """Test that user patterns are validated for required fields and safety."""
        # Test that PatternLoader properly validates user patterns

        from deckbuilder.templates.pattern_loader import PatternLoader

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
        with open(invalid_file, "w") as f:
            json.dump(invalid_pattern, f)

        # Create PatternLoader with this template folder
        loader = PatternLoader(template_folder)

        # Load patterns - invalid pattern should be rejected
        patterns = loader.load_patterns()

        # Invalid pattern should not be included in loaded patterns
        assert "Invalid Layout" not in patterns

        # Verify validation works correctly
        validation_results = loader.validate_all_patterns()

        # Should have validation errors for the invalid pattern
        assert len(validation_results) > 0
        has_invalid_pattern_error = any("invalid_pattern.json" in key for key in validation_results.keys())
        assert has_invalid_pattern_error

        # Verify specific validation errors for the invalid file
        invalid_errors = None
        for key, errors in validation_results.items():
            if "invalid_pattern.json" in key:
                invalid_errors = errors
                break

        assert invalid_errors is not None
        assert len(invalid_errors) > 0

        # Should contain errors about missing required fields
        error_text = " ".join(invalid_errors)
        assert "yaml_pattern" in error_text or "validation" in error_text or "example" in error_text

    def test_graceful_fallback_for_missing_patterns(self):
        """Test graceful handling when pattern file doesn't exist for a layout."""
        # Test that PatternLoader gracefully handles missing pattern files

        from deckbuilder.templates.pattern_loader import PatternLoader

        # Create loader with no user patterns
        loader = PatternLoader("/tmp/nonexistent")

        # Try to get pattern for a non-existent layout
        nonexistent_pattern = loader.get_pattern_for_layout("Nonexistent Layout")

        # Should return None gracefully, not crash
        assert nonexistent_pattern is None

        # System should still work for existing patterns
        patterns = loader.load_patterns()
        assert len(patterns) > 0

        # Should be able to find pattern files for existing layouts
        existing_layout = list(patterns.keys())[0]
        pattern_file = loader.find_pattern_file_for_layout(existing_layout)
        assert pattern_file is not None

        # But should return None for non-existent layouts
        missing_file = loader.find_pattern_file_for_layout("Nonexistent Layout")
        assert missing_file is None


class TestPatternLoaderIntegration:
    """Test PatternLoader integration with existing systems."""

    def test_integration_with_template_metadata_loader(self):
        """Test PatternLoader integrates with TemplateMetadataLoader."""
        from deckbuilder.templates.metadata import TemplateMetadataLoader

        # Test that TemplateMetadataLoader uses PatternLoader for layout descriptions
        loader = TemplateMetadataLoader()

        # Test that we can get enhanced layout metadata from patterns
        layout_meta = loader.get_enhanced_layout_metadata("Four Columns")
        assert layout_meta is not None
        assert layout_meta.display_name == "Four Columns"
        assert "four-column" in layout_meta.description.lower()
        assert "content_col1" in layout_meta.placeholders
        assert "content_col2" in layout_meta.placeholders
        assert "content_col3" in layout_meta.placeholders
        assert "content_col4" in layout_meta.placeholders

        # Test that we can create template metadata from patterns
        metadata = loader.create_template_metadata_from_patterns("default")
        assert metadata.total_layouts > 0
        assert "Four Columns" in metadata.layouts
        assert "Title Slide" in metadata.layouts

        # Test that the full load_template_metadata uses patterns
        full_metadata = loader.load_template_metadata("default")
        assert full_metadata.total_layouts == 31  # All pattern layouts including semantic aliases
        assert "Four Columns" in full_metadata.layouts

        # Test pattern example parsing
        example = loader.get_pattern_example("Title Slide")
        assert isinstance(example, dict)
        assert "title_top" in example

        # Test validation info
        validation = loader.get_layout_validation_info("Four Columns")
        assert "required_fields" in validation
        assert "optional_fields" in validation
        assert "available_fields" in validation

    @pytest.mark.asyncio
    async def test_integration_with_get_template_layouts_mcp_tool(self):
        """Test PatternLoader provides data to get_template_layouts() MCP tool."""
        import os
        import json
        from pathlib import Path

        # Set up environment variables for MCP server
        original_env = os.environ.copy()
        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            # Import and test the actual MCP tool
            from src.mcp_server.main import get_template_layouts

            # Create a real context object (not a mock)
            class TestContext:
                pass

            ctx = TestContext()
            result = await get_template_layouts(ctx, "default")

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
        # Test that hard-coded functions have been removed from MCP server

        import inspect
        from src.mcp_server import main as mcp_main

        # Get all functions in the MCP main module
        mcp_functions = [name for name, obj in inspect.getmembers(mcp_main) if inspect.isfunction(obj)]

        # Verify hard-coded functions have been removed
        hard_coded_functions = ["_generate_layout_example", "_get_title_example_for_layout", "_get_content_example_for_layout"]

        for func_name in hard_coded_functions:
            assert func_name not in mcp_functions, f"Hard-coded function {func_name} still exists in MCP server"

        # Verify the source code doesn't contain these function definitions
        import src.mcp_server.main

        source_file = inspect.getsourcefile(src.mcp_server.main)
        with open(source_file, "r") as f:
            source_content = f.read()

        for func_name in hard_coded_functions:
            assert f"def {func_name}" not in source_content, f"Hard-coded function definition {func_name} found in source"

    def test_backward_compatibility_without_user_patterns(self):
        """Test system works normally when no user patterns folder exists."""
        # Test that system works with only built-in patterns when no user patterns exist

        from deckbuilder.templates.pattern_loader import PatternLoader

        # Create loader with template folder that has no patterns subfolder
        loader = PatternLoader("/tmp/nonexistent_patterns_folder")

        # Should still load built-in patterns successfully
        patterns = loader.load_patterns()
        assert len(patterns) > 0

        # Should have common built-in patterns
        assert "Four Columns" in patterns
        assert "Comparison" in patterns

        # Should be able to get pattern data for built-in layouts
        four_columns = loader.get_pattern_for_layout("Four Columns")
        assert four_columns is not None
        assert "description" in four_columns
        assert "yaml_pattern" in four_columns

        # Should get empty results when checking for user patterns
        patterns_by_source = loader.get_patterns_by_file_source()
        assert len(patterns_by_source["user"]) == 0
        assert len(patterns_by_source["builtin"]) > 0

        # Validation should work normally (no user patterns to validate)
        validation_results = loader.validate_all_patterns()
        # Should have no user pattern errors since no user patterns exist
        user_errors = [key for key in validation_results.keys() if key.startswith("user:")]
        assert len(user_errors) == 0


class TestPatternLoaderErrorHandling:
    """Test PatternLoader error handling and edge cases."""

    def test_invalid_json_in_user_pattern_file(self, tmp_path):
        """Test handling of invalid JSON in user pattern files."""
        # Test that PatternLoader handles invalid JSON gracefully

        from deckbuilder.templates.pattern_loader import PatternLoader

        # Setup: Create pattern file with invalid JSON
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()

        invalid_file = patterns_folder / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write('{"invalid": json}')  # Invalid JSON syntax

        # Create a valid pattern file too
        valid_pattern = {
            "description": "Valid pattern for testing error handling",
            "yaml_pattern": {"layout": "Valid Layout", "title": "str", "content": "str"},
            "validation": {"required_fields": ["title", "content"]},
            "example": "---\nlayout: Valid Layout\ntitle: Test\ncontent: Test content\n---",
        }

        valid_file = patterns_folder / "valid.json"
        with open(valid_file, "w") as f:
            json.dump(valid_pattern, f)

        # Create PatternLoader
        loader = PatternLoader(template_folder)

        # Should load patterns without crashing
        patterns = loader.load_patterns()

        # Should include valid pattern but not invalid one
        assert "Valid Layout" in patterns
        assert len([k for k in patterns.keys() if "invalid" in k.lower()]) == 0

        # Validation should report the JSON error
        validation_results = loader.validate_all_patterns()

        # Should have error for invalid.json
        has_json_error = any("invalid.json" in key and len(errors) > 0 for key, errors in validation_results.items())
        assert has_json_error

    def test_permission_errors_on_pattern_files(self):
        """Test handling of file permission errors."""
        # Test that PatternLoader handles permission errors gracefully

        from deckbuilder.templates.pattern_loader import PatternLoader
        import os
        import tempfile
        import stat

        # Skip this test on Windows as chmod behavior differs
        if os.name == "nt":
            import pytest

            pytest.skip("Permission tests not reliable on Windows")

        with tempfile.TemporaryDirectory() as temp_dir:
            template_folder = Path(temp_dir) / "templates"
            template_folder.mkdir()
            patterns_folder = template_folder / "patterns"
            patterns_folder.mkdir()

            # Create a pattern file
            pattern_file = patterns_folder / "test_pattern.json"
            valid_pattern = {
                "description": "Test pattern for permission testing",
                "yaml_pattern": {"layout": "Test Layout", "title": "str"},
                "validation": {"required_fields": ["title"]},
                "example": "---\nlayout: Test Layout\ntitle: Test\n---",
            }

            with open(pattern_file, "w") as f:
                json.dump(valid_pattern, f)

            # Remove read permissions
            pattern_file.chmod(stat.S_IWRITE)  # Write only, no read

            try:
                # Create PatternLoader
                loader = PatternLoader(template_folder)

                # Should not crash when loading patterns
                patterns = loader.load_patterns()

                # Should not include the unreadable pattern
                assert "Test Layout" not in patterns

                # Validation should report permission error
                validation_results = loader.validate_all_patterns()

                # Should have permission error for the file
                has_permission_error = any("test_pattern.json" in key and len(errors) > 0 for key, errors in validation_results.items())
                assert has_permission_error

            finally:
                # Restore permissions for cleanup
                try:
                    pattern_file.chmod(stat.S_IREAD | stat.S_IWRITE)
                except OSError:
                    pass

    def test_pattern_file_schema_validation(self, tmp_path):
        """Test validation of pattern file schema and required fields."""
        # Test that PatternLoader validates schema and reports specific errors

        from deckbuilder.templates.pattern_loader import PatternLoader

        # Setup: Create pattern with wrong schema
        template_folder = tmp_path / "templates"
        template_folder.mkdir()
        patterns_folder = template_folder / "patterns"
        patterns_folder.mkdir()

        wrong_schema = {"wrong_field": "value", "missing_required_fields": True}

        wrong_file = patterns_folder / "wrong_schema.json"
        with open(wrong_file, "w") as f:
            json.dump(wrong_schema, f)

        # Create PatternLoader
        loader = PatternLoader(template_folder)

        # Should not crash when loading patterns
        patterns = loader.load_patterns()

        # Should not include the invalid pattern
        pattern_with_wrong_schema = [k for k in patterns.keys() if "wrong" in k.lower()]
        assert len(pattern_with_wrong_schema) == 0

        # Validate specific file and check for schema errors
        validation_errors = loader.validate_pattern_file(wrong_file)
        assert len(validation_errors) > 0

        # Should contain schema validation errors
        error_text = " ".join(validation_errors)
        assert "schema" in error_text.lower() or "validation" in error_text.lower()

        # Test validation of all patterns
        validation_results = loader.validate_all_patterns()

        # Should have errors for wrong_schema.json
        has_schema_error = any("wrong_schema.json" in key and len(errors) > 0 for key, errors in validation_results.items())
        assert has_schema_error


class TestPatternLoaderPerformance:
    """Test PatternLoader performance and caching."""

    def test_pattern_loading_performance(self):
        """Test that pattern loading is performant for multiple calls."""
        # Test that pattern loading uses caching to avoid repeated file system access

        from deckbuilder.templates.pattern_loader import PatternLoader
        import time

        # Create loader
        loader = PatternLoader("/tmp/nonexistent")

        # Time first load
        start_time = time.time()
        patterns1 = loader.load_patterns()
        first_load_time = time.time() - start_time

        # Time second load (should be cached)
        start_time = time.time()
        patterns2 = loader.load_patterns()
        second_load_time = time.time() - start_time

        # Should return same patterns
        assert patterns1 == patterns2

        # Second load should be significantly faster (cached)
        # Allow for some variance but second load should be much faster
        assert second_load_time < first_load_time * 0.5 or second_load_time < 0.01

        # Verify cache is working by checking cache content
        assert len(loader._pattern_cache) > 0

        # Store the initial pattern keys for comparison
        initial_pattern_keys = set(patterns1.keys())

        # Clear cache and verify it works
        loader.clear_cache()
        assert len(loader._pattern_cache) == 0

        # After clearing, load should populate cache again
        patterns3 = loader.load_patterns()
        assert len(loader._pattern_cache) > 0
        # The patterns should be equivalent in content (comparing keys for basic check)
        assert set(patterns3.keys()) == initial_pattern_keys

    def test_pattern_cache_invalidation(self):
        """Test that pattern cache can be manually invalidated."""
        # Test cache invalidation behavior (currently manual via clear_cache)

        from deckbuilder.templates.pattern_loader import PatternLoader
        import tempfile
        import json

        with tempfile.TemporaryDirectory() as temp_dir:
            template_folder = Path(temp_dir) / "templates"
            template_folder.mkdir()
            patterns_folder = template_folder / "patterns"
            patterns_folder.mkdir()

            # Create initial pattern
            initial_pattern = {
                "description": "Initial pattern for cache testing",
                "yaml_pattern": {"layout": "Cache Test", "title": "str"},
                "validation": {"required_fields": ["title"]},
                "example": "---\nlayout: Cache Test\ntitle: Initial\n---",
            }

            pattern_file = patterns_folder / "cache_test.json"
            with open(pattern_file, "w") as f:
                json.dump(initial_pattern, f)

            # Create loader and load patterns
            loader = PatternLoader(template_folder)
            patterns1 = loader.load_patterns()

            # Verify initial pattern is loaded
            assert "Cache Test" in patterns1
            assert "Initial pattern" in patterns1["Cache Test"]["description"]

            # Modify the pattern file
            modified_pattern = initial_pattern.copy()
            modified_pattern["description"] = "Modified pattern for cache testing"

            with open(pattern_file, "w") as f:
                json.dump(modified_pattern, f)

            # Without clearing cache, should get cached version
            patterns2 = loader.load_patterns()
            assert patterns2["Cache Test"]["description"] == "Initial pattern for cache testing"

            # Clear cache manually
            loader.clear_cache()

            # After clearing cache, should get updated pattern
            patterns3 = loader.load_patterns()
            assert patterns3["Cache Test"]["description"] == "Modified pattern for cache testing"

            # Verify cache was repopulated
            assert len(loader._pattern_cache) > 0
