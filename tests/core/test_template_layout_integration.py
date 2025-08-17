"""
Integration test demonstrating template layout usage.

This test creates a simple presentation scenario and verifies that
the system uses PowerPoint template layouts instead of dynamic shapes.
"""

import pytest
from unittest.mock import Mock

# Import core functionality
from deckbuilder.core.layout_resolver import LayoutResolver


class TestTemplateLayoutIntegration:
    """Integration test for template layout system."""

    def test_slide_creation_uses_template_layouts(self):
        """Test that slide creation uses PowerPoint template layouts."""
        # This is an integration test showing the template-first approach

        layout_resolver = LayoutResolver()

        # Mock a typical presentation with common layouts
        mock_prs = Mock()

        # Simulate common PowerPoint template layouts
        standard_layouts = ["Title Slide", "Title and Content", "Two Content", "Table Only", "Table with Content Above", "Content with Caption", "Section Header", "Blank"]

        mock_layouts = []
        for layout_name in standard_layouts:
            mock_layout = Mock()
            mock_layout.name = layout_name
            mock_layouts.append(mock_layout)

        mock_prs.slide_layouts = mock_layouts

        # Test scenario 1: Simple content slide
        content_layout = layout_resolver.get_layout_by_name(mock_prs, "Title and Content")
        assert content_layout.name == "Title and Content"

        # Test scenario 2: Table-only slide (replaces dynamic table creation)
        table_layout = layout_resolver.get_layout_by_name(mock_prs, "Table Only")
        assert table_layout.name == "Table Only"

        # Test scenario 3: Mixed content slide (replaces dynamic positioning)
        mixed_layout = layout_resolver.get_layout_by_name(mock_prs, "Table with Content Above")
        assert mixed_layout.name == "Table with Content Above"

        # Test scenario 4: Two column content (replaces dynamic column creation)
        two_col_layout = layout_resolver.get_layout_by_name(mock_prs, "Two Content")
        assert two_col_layout.name == "Two Content"

    def test_error_handling_for_missing_layouts(self):
        """Test that clear errors are provided for missing layouts."""
        layout_resolver = LayoutResolver()

        # Mock presentation with limited layouts
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]

        # Test that requesting a non-existent layout gives clear error
        with pytest.raises(ValueError) as exc_info:
            layout_resolver.get_layout_by_name(mock_prs, "Advanced Table Layout")

        error_msg = str(exc_info.value)
        assert "Layout 'Advanced Table Layout' not found" in error_msg
        assert "Available layouts:" in error_msg
        assert "Title and Content" in error_msg

    def test_layout_discovery(self):
        """Test that the system can discover all available layouts."""
        layout_resolver = LayoutResolver()

        # Mock presentation with comprehensive layout set
        mock_prs = Mock()

        # Comprehensive set of PowerPoint layouts that replace dynamic shapes
        comprehensive_layouts = [
            # Basic layouts
            "Title Slide",
            "Title and Content",
            "Section Header",
            "Title Only",
            "Blank",
            # Multi-content layouts (replace dynamic positioning)
            "Two Content",
            "Comparison",
            "Four Columns",
            "Three Columns",
            # Table layouts (replace dynamic table creation)
            "Table Only",
            "Table with Content Above",
            "Table with Content Above and Below",
            "Table with Content Left",
            # Media layouts (replace dynamic media positioning)
            "Content with Caption",
            "Picture with Caption",
            "Picture Only",
            # Special layouts
            "Quote",
            "Section Divider",
            "Timeline",
        ]

        mock_layouts = []
        for layout_name in comprehensive_layouts:
            mock_layout = Mock()
            mock_layout.name = layout_name
            mock_layouts.append(mock_layout)

        mock_prs.slide_layouts = mock_layouts

        # Test layout discovery
        available_layouts = layout_resolver.list_available_layouts(mock_prs)

        # Verify all layouts are discovered
        assert len(available_layouts) == len(comprehensive_layouts)

        for expected_layout in comprehensive_layouts:
            assert expected_layout in available_layouts, f"Layout '{expected_layout}' should be available"

        # Verify specific layout categories are covered

        # Table layouts (replace dynamic table system)
        table_layouts = [layout for layout in available_layouts if "Table" in layout]
        assert len(table_layouts) >= 4, "Should have multiple table layouts to replace dynamic table creation"

        # Multi-content layouts (replace dynamic positioning)
        multi_content_layouts = [layout for layout in available_layouts if any(word in layout for word in ["Two", "Three", "Four", "Comparison"])]
        assert len(multi_content_layouts) >= 4, "Should have multi-content layouts to replace dynamic positioning"

        # Media layouts (replace dynamic media handling)
        media_layouts = [layout for layout in available_layouts if any(word in layout for word in ["Picture", "Content with Caption"])]
        assert len(media_layouts) >= 2, "Should have media layouts to replace dynamic media positioning"


class TestTemplateFirstArchitecture:
    """Test the template-first architectural approach."""

    def test_template_first_approach(self):
        """Test that the system follows template-first principles."""
        # This test demonstrates the architectural shift:
        # OLD: Dynamic shape creation based on content analysis
        # NEW: Template layout selection based on user intent

        layout_resolver = LayoutResolver()

        # Simulate template selection workflow
        mock_prs = Mock()

        # User scenarios mapped to template layouts
        scenario_to_layout = {
            "I want a title slide": "Title Slide",
            "I want text content": "Title and Content",
            "I want a table": "Table Only",
            "I want text above a table": "Table with Content Above",
            "I want two columns": "Two Content",
            "I want to compare things": "Comparison",
            "I want text with an image": "Content with Caption",
        }

        # Mock all required layouts
        layout_names = list(scenario_to_layout.values())
        mock_layouts = []
        for name in layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            mock_layouts.append(mock_layout)

        mock_prs.slide_layouts = mock_layouts

        # Test that each user scenario maps to a template layout
        for scenario, expected_layout in scenario_to_layout.items():
            layout = layout_resolver.get_layout_by_name(mock_prs, expected_layout)
            assert layout.name == expected_layout, f"Scenario '{scenario}' should use layout '{expected_layout}'"

    def test_no_fallback_to_dynamic_shapes(self):
        """Test that system doesn't fall back to dynamic shape creation."""
        # This test verifies that the system follows the "SUCCESS or CLEAR ERRORS" principle
        # instead of falling back to dynamic shape creation

        layout_resolver = LayoutResolver()

        # Mock presentation with limited layouts
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]

        # Test that requesting unsupported layout fails cleanly
        # (no fallback to dynamic shape creation)
        with pytest.raises(ValueError):
            layout_resolver.get_layout_by_name(mock_prs, "Complex Dynamic Layout")

        # This is the desired behavior: clear errors instead of fallbacks
        # The system should never attempt dynamic shape creation as a fallback

    def test_layout_validation_prevents_errors(self):
        """Test that layout validation prevents runtime errors."""
        layout_resolver = LayoutResolver()

        # Mock presentation
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]

        # Test validation before attempting to use layout
        assert layout_resolver.validate_layout_exists(mock_prs, "Title and Content") is True
        assert layout_resolver.validate_layout_exists(mock_prs, "Non-existent Layout") is False

        # This validation pattern prevents the need for dynamic shape fallbacks
        # by checking layout availability before attempting to use them


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
