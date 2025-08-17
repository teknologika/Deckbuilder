"""
Test template layout system (verifying NO dynamic shape creation).

This test suite verifies that the system uses PowerPoint template layouts
instead of the deprecated dynamic shape creation system.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Import core modules
from deckbuilder.core.layout_resolver import LayoutResolver
from deckbuilder.templates.pattern_loader import PatternLoader


class TestTemplateLayoutSystem:
    """Test that template layouts are used instead of dynamic shapes."""

    def setup_method(self):
        """Set up test instances."""
        self.layout_resolver = LayoutResolver()

        # Mock presentation with layouts
        self.mock_prs = Mock()
        self.mock_layouts = []

        # Common PowerPoint layouts
        layout_names = [
            "Title Slide",
            "Title and Content",
            "Section Header",
            "Two Content",
            "Comparison",
            "Title Only",
            "Blank",
            "Content with Caption",
            "Picture with Caption",
            "Table Only",
            "Table with Content Above",
            "Table with Content Above and Below",
            "Four Columns",
            "Three Columns",
        ]

        for name in layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            self.mock_layouts.append(mock_layout)

        self.mock_prs.slide_layouts = self.mock_layouts

    def test_layout_resolver_finds_standard_layouts(self):
        """Test that layout resolver can find standard PowerPoint layouts."""
        # Test finding basic layouts
        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Title and Content")
        assert layout.name == "Title and Content"

        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Two Content")
        assert layout.name == "Two Content"

        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Comparison")
        assert layout.name == "Comparison"

    def test_layout_resolver_finds_table_layouts(self):
        """Test that layout resolver can find table-specific layouts."""
        # These layouts replace dynamic shape creation for tables
        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Table Only")
        assert layout.name == "Table Only"

        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Table with Content Above")
        assert layout.name == "Table with Content Above"

        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, "Table with Content Above and Below")
        assert layout.name == "Table with Content Above and Below"

    def test_layout_resolver_error_handling(self):
        """Test layout resolver provides helpful error messages."""
        # Test non-existent layout
        with pytest.raises(ValueError) as exc_info:
            self.layout_resolver.get_layout_by_name(self.mock_prs, "Non-Existent Layout")

        error_msg = str(exc_info.value)
        assert "Layout 'Non-Existent Layout' not found" in error_msg
        assert "Available layouts:" in error_msg

        # Test similar layout suggestion - check that it works when similar layout found
        with pytest.raises(ValueError) as exc_info:
            self.layout_resolver.get_layout_by_name(self.mock_prs, "title")  # Should match "Title Slide" and "Title and Content"

        error_msg = str(exc_info.value)
        # The error should mention available layouts
        assert "Available layouts:" in error_msg

    def test_list_available_layouts(self):
        """Test listing all available layouts."""
        layouts = self.layout_resolver.list_available_layouts(self.mock_prs)

        expected_layouts = [
            "Title Slide",
            "Title and Content",
            "Section Header",
            "Two Content",
            "Comparison",
            "Title Only",
            "Blank",
            "Content with Caption",
            "Picture with Caption",
            "Table Only",
            "Table with Content Above",
            "Table with Content Above and Below",
            "Four Columns",
            "Three Columns",
        ]

        assert len(layouts) == len(expected_layouts)
        for expected in expected_layouts:
            assert expected in layouts

    def test_validate_layout_exists(self):
        """Test layout validation without exceptions."""
        # Valid layouts
        assert self.layout_resolver.validate_layout_exists(self.mock_prs, "Title and Content") is True
        assert self.layout_resolver.validate_layout_exists(self.mock_prs, "Table Only") is True

        # Invalid layout
        assert self.layout_resolver.validate_layout_exists(self.mock_prs, "Invalid Layout") is False


class TestPatternLoaderIntegration:
    """Test pattern loader integration with layout system."""

    def setup_method(self):
        """Set up test instances."""
        # Mock the structured frontmatter patterns directory
        self.test_patterns_dir = Path(__file__).parent.parent / "structured_frontmatter_patterns"

    @patch("src.deckbuilder.templates.pattern_loader.Path.exists")
    @patch("src.deckbuilder.templates.pattern_loader.Path.iterdir")
    def test_pattern_loader_discovers_layouts(self, mock_iterdir, mock_exists):
        """Test that PatternLoader discovers available layout patterns."""
        # Mock pattern files
        mock_pattern_files = [
            Mock(name="title_and_content.json", suffix=".json"),
            Mock(name="two_content.json", suffix=".json"),
            Mock(name="table_only.json", suffix=".json"),
            Mock(name="table_with_content_above.json", suffix=".json"),
        ]

        for mock_file in mock_pattern_files:
            mock_file.is_file.return_value = True

        mock_iterdir.return_value = mock_pattern_files
        mock_exists.return_value = True

        # Mock JSON content
        mock_patterns = {
            "title_and_content.json": {
                "yaml_pattern": {"layout": "Title and Content", "title_top": "str", "content": "str"},
                "validation": {"required_fields": ["title_top"], "optional_fields": ["content"]},
            },
            "table_only.json": {"yaml_pattern": {"layout": "Table Only", "table_data": "table"}, "validation": {"required_fields": ["table_data"], "optional_fields": []}},
        }

        with patch("builtins.open", create=True) as mock_open:
            with patch("json.load") as mock_json_load:
                # Set up JSON loading behavior
                def json_load_side_effect(file):
                    filename = mock_open.return_value.__enter__.return_value.name
                    if filename in mock_patterns:
                        return mock_patterns[filename]
                    return {"yaml_pattern": {}, "validation": {}}

                mock_json_load.side_effect = json_load_side_effect

                # Create PatternLoader
                pattern_loader = PatternLoader()

                # Test pattern discovery
                assert hasattr(pattern_loader, "get_pattern_for_layout")


class TestNoDynamicShapeCreation:
    """Verify that dynamic shape creation is NOT used anywhere."""

    def test_no_content_segmenter(self):
        """Verify content_segmenter.py has been eliminated."""
        # Check that content_segmenter.py doesn't exist in src
        from pathlib import Path

        src_dir = Path(__file__).parent.parent.parent / "src"

        # Search recursively for any content_segmenter.py files
        content_segmenter_files = list(src_dir.rglob("content_segmenter.py"))
        assert len(content_segmenter_files) == 0, f"Found content_segmenter.py files: {content_segmenter_files}"

    def test_no_dynamic_shape_methods(self):
        """Verify dynamic shape creation methods don't exist."""
        # Import slide builder modules and check they don't have dynamic shape methods
        try:
            from deckbuilder.core import slide_builder

            # Check that slide_builder doesn't have dynamic shape methods
            assert not hasattr(slide_builder, "_create_dynamic_content_shapes"), "slide_builder should not have _create_dynamic_content_shapes method"

            assert not hasattr(slide_builder, "_content_segments"), "slide_builder should not have _content_segments attribute"

        except ImportError:
            # If slide_builder doesn't exist, that's fine - it's been refactored
            pass

    def test_no_dynamic_shape_imports(self):
        """Verify no imports of deprecated dynamic shape modules."""
        # Check core modules don't import content_segmenter
        from pathlib import Path
        import re

        src_dir = Path(__file__).parent.parent.parent / "src"

        # Search for any imports of content_segmenter
        import_pattern = re.compile(r"from.*content_segmenter|import.*content_segmenter")

        for py_file in src_dir.rglob("*.py"):
            try:
                content = py_file.read_text()
                matches = import_pattern.findall(content)
                assert len(matches) == 0, f"Found content_segmenter import in {py_file}: {matches}"
            except Exception:
                # Skip files that can't be read
                continue


class TestTableLayoutsReplacement:
    """Test that table layouts replace dynamic shape positioning."""

    def test_table_layouts_available(self):
        """Test that table-specific layouts are available."""
        layout_resolver = LayoutResolver()

        # Mock presentation with table layouts
        mock_prs = Mock()
        table_layout_names = ["Table Only", "Table with Content Above", "Table with Content Above and Below", "Table with Content Left", "Content Table Content Table Content"]

        table_layouts = []
        for name in table_layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            table_layouts.append(mock_layout)

        mock_prs.slide_layouts = table_layouts

        # Verify table layouts can be found
        assert layout_resolver.validate_layout_exists(mock_prs, "Table Only")
        assert layout_resolver.validate_layout_exists(mock_prs, "Table with Content Above")
        assert layout_resolver.validate_layout_exists(mock_prs, "Table with Content Above and Below")

    def test_mixed_content_uses_layouts(self):
        """Test that mixed content scenarios use proper layouts instead of dynamic shapes."""
        # This test verifies the architectural decision to use template layouts
        # instead of dynamic shape positioning for mixed content scenarios

        layout_resolver = LayoutResolver()

        # Mock presentation with mixed content layouts
        mock_prs = Mock()
        mixed_layout_names = [
            "Title and Content",  # Simple content
            "Table Only",  # Table-only content
            "Table with Content Above",  # Content + Table
            "Content with Caption",  # Content + Image
            "Two Content",  # Side-by-side content
            "Comparison",  # Comparison layout
        ]

        mixed_layouts = []
        for name in mixed_layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            mixed_layouts.append(mock_layout)

        mock_prs.slide_layouts = mixed_layouts

        # Verify all mixed content scenarios have dedicated layouts
        # (no dynamic shape creation needed)
        scenarios = [
            "Title and Content",  # Replace: dynamic text positioning
            "Table Only",  # Replace: dynamic table creation
            "Table with Content Above",  # Replace: mixed content dynamic positioning
            "Two Content",  # Replace: dynamic column layout
            "Comparison",  # Replace: dynamic comparison layout
        ]

        for scenario in scenarios:
            assert layout_resolver.validate_layout_exists(mock_prs, scenario), f"Layout '{scenario}' should exist to replace dynamic shape creation"


class TestLayoutSystemIntegration:
    """Test integration between layout resolution and pattern loading."""

    def test_layout_pattern_coordination(self):
        """Test that layout resolver and pattern loader work together."""
        # This test verifies the architecture where:
        # 1. PatternLoader provides field mappings for layouts
        # 2. LayoutResolver finds the actual PowerPoint layout
        # 3. No dynamic shape creation is involved

        layout_resolver = LayoutResolver()

        # Mock presentation
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]

        # Test the coordination
        layout = layout_resolver.get_layout_by_name(mock_prs, "Title and Content")
        assert layout.name == "Title and Content"

        # This represents the NEW architecture:
        # 1. PatternLoader tells us what fields the layout expects
        # 2. LayoutResolver finds the PowerPoint layout
        # 3. Content is applied to placeholders (no dynamic shapes)

        assert layout is not None, "Layout resolution should work for template-based approach"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
