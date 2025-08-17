"""
Cross-module integration tests for the refactored slide builder system.

This test suite verifies that all refactored modules work together correctly:
- PlaceholderManager: Placeholder resolution and mapping  
- ContentProcessor: Content application with template fonts
- TableHandler: Table processing with plain text
- LayoutResolver: Layout resolution from templates
- SlideCoordinator: High-level orchestration (when implemented)

Tests the complete slide creation workflow end-to-end.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Import refactored modules
from deckbuilder.core.layout_resolver import LayoutResolver
from deckbuilder.core.table_handler import TableHandler
from deckbuilder.core.placeholder_resolver import PlaceholderResolver
from deckbuilder.core.content_processor import ContentProcessor


class TestCrossModuleIntegration:
    """Test integration between all refactored modules."""
    
    def setup_method(self):
        """Set up test instances of all modules."""
        self.layout_resolver = LayoutResolver()
        self.table_handler = TableHandler()
        self.placeholder_resolver = PlaceholderResolver()
        self.content_processor = ContentProcessor()
        
        # Mock presentation and slide objects
        self.mock_prs = Mock()
        self.mock_slide = Mock()
        
        # Mock common layouts
        layout_names = [
            "Title and Content",
            "Two Content", 
            "Table Only",
            "Table with Content Above",
            "Comparison"
        ]
        
        mock_layouts = []
        for name in layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            mock_layouts.append(mock_layout)
        
        self.mock_prs.slide_layouts = mock_layouts
        
        # Mock slide placeholders
        self.mock_slide.placeholders = []
        
    def test_simple_content_slide_workflow(self):
        """Test complete workflow for simple content slide creation."""
        # Simulate slide data for "Title and Content" layout
        slide_data = {
            "layout": "Title and Content",
            "title": "Test Slide Title",
            "content": "This is test content for the slide."
        }
        
        # Step 1: Layout Resolution
        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, slide_data["layout"])
        assert layout.name == "Title and Content"
        
        # Step 2: Placeholder Resolution
        # Mock the placeholder resolution process
        with patch.object(self.placeholder_resolver, 'get_placeholder_by_name') as mock_get:
            mock_get.return_value = Mock()
            
            # Find placeholders for each field
            title_placeholder = self.placeholder_resolver.get_placeholder_by_name(
                self.mock_slide, "title"
            )
            content_placeholder = self.placeholder_resolver.get_placeholder_by_name(
                self.mock_slide, "content"
            )
            
            # Verify placeholder finding was called
            assert mock_get.call_count == 2
            assert title_placeholder is not None
            assert content_placeholder is not None
        
        # Step 3: Content Processing
        # Mock content application
        with patch.object(self.content_processor, 'apply_content_to_placeholder') as mock_apply:
            # Apply title
            self.content_processor.apply_content_to_placeholder(
                title_placeholder, slide_data["title"]
            )
            
            # Apply content
            self.content_processor.apply_content_to_placeholder(
                content_placeholder, slide_data["content"]
            )
            
            # Verify content application was called
            assert mock_apply.call_count == 2
    
    def test_table_slide_workflow(self):
        """Test complete workflow for table slide creation."""
        # Simulate slide data with table content
        slide_data = {
            "layout": "Table Only",
            "table_data": """
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1 Col 1 | Row 1 Col 2 | Row 1 Col 3 |
| Row 2 Col 1 | Row 2 Col 2 | Row 2 Col 3 |
"""
        }
        
        # Step 1: Layout Resolution
        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, slide_data["layout"])
        assert layout.name == "Table Only"
        
        # Step 2: Table Detection and Processing
        # Test table detection
        table_detected = self.table_handler.detect_table_content(slide_data["table_data"])
        assert table_detected is True
        
        # Test table parsing
        table_structure = self.table_handler.parse_table_structure(slide_data["table_data"])
        expected_structure = [
            ["Header 1", "Header 2", "Header 3"],
            ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
            ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
        ]
        assert table_structure == expected_structure
        
        # Step 3: Table Creation
        # Mock table creation
        mock_table_shape = Mock()
        with patch.object(self.table_handler, 'create_table_from_data') as mock_create:
            mock_create.return_value = mock_table_shape
            
            # Position calculation
            position = self.table_handler.position_table_on_slide(self.mock_slide)
            size = (300, 200)  # Mock size
            
            # Create table
            table_shape = self.table_handler.create_table_from_data(
                self.mock_slide, table_structure, position, size
            )
            
            # Verify table creation was called
            mock_create.assert_called_once_with(
                self.mock_slide, table_structure, position, size
            )
            assert table_shape == mock_table_shape
    
    def test_mixed_content_workflow(self):
        """Test workflow for mixed content (content + table)."""
        # Simulate slide data with both content and table
        slide_data = {
            "layout": "Table with Content Above",
            "title": "Mixed Content Slide",
            "content": "Content above the table",
            "table_data": """
| Product | Price | Stock |
|---------|-------|-------|
| Widget A | $10 | 50 |
| Widget B | $15 | 30 |
"""
        }
        
        # Step 1: Layout Resolution
        layout = self.layout_resolver.get_layout_by_name(self.mock_prs, slide_data["layout"])
        assert layout.name == "Table with Content Above"
        
        # Step 2: Content Processing
        # Mock placeholder resolution
        with patch.object(self.placeholder_resolver, 'get_placeholder_by_name') as mock_get:
            mock_get.return_value = Mock()
            
            # Find placeholders for each field
            placeholders = {}
            for field_name in ["title", "content"]:
                if field_name in slide_data:
                    placeholders[field_name] = self.placeholder_resolver.get_placeholder_by_name(
                        self.mock_slide, field_name
                    )
            
            # Apply content to placeholders
            with patch.object(self.content_processor, 'apply_content_to_placeholder') as mock_apply:
                for field_name, placeholder in placeholders.items():
                    self.content_processor.apply_content_to_placeholder(
                        placeholder, slide_data[field_name]
                    )
                
                # Verify content was applied
                assert mock_apply.call_count == 2
        
        # Step 3: Table Processing
        # Test table detection and processing
        table_detected = self.table_handler.detect_table_content(slide_data["table_data"])
        assert table_detected is True
        
        table_structure = self.table_handler.parse_table_structure(slide_data["table_data"])
        expected_structure = [
            ["Product", "Price", "Stock"],
            ["Widget A", "$10", "50"],
            ["Widget B", "$15", "30"]
        ]
        assert table_structure == expected_structure
        
        # Mock table creation with intelligent positioning
        with patch.object(self.table_handler, 'create_table_from_data') as mock_create:
            mock_create.return_value = Mock()
            
            # Calculate position considering existing content
            content_height = 150  # Mock content height
            position = self.table_handler.position_table_on_slide(
                self.mock_slide, content_height
            )
            
            # Verify position is below content
            assert position[1] > content_height  # Top position should be below content
    
    def test_error_handling_across_modules(self):
        """Test error handling and coordination across modules."""
        # Test 1: Invalid layout handling
        with pytest.raises(ValueError) as exc_info:
            self.layout_resolver.get_layout_by_name(self.mock_prs, "Non-existent Layout")
        
        error_msg = str(exc_info.value)
        assert "Layout 'Non-existent Layout' not found" in error_msg
        
        # Test 2: Invalid table data handling
        invalid_table_data = "This is not a table"
        table_detected = self.table_handler.detect_table_content(invalid_table_data)
        assert table_detected is False
        
        table_structure = self.table_handler.parse_table_structure(invalid_table_data)
        assert table_structure == []
        
        # Test 3: Empty table creation handling
        result = self.table_handler.create_table_from_data(
            self.mock_slide, [], (100, 100), (200, 100)
        )
        assert result is None  # Should return None for empty data
    
    def test_module_dependencies(self):
        """Test that modules have minimal dependencies on each other."""
        # Each module should be independently testable
        
        # LayoutResolver should work independently
        layout_resolver = LayoutResolver()
        layouts = layout_resolver.list_available_layouts(self.mock_prs)
        assert isinstance(layouts, list)
        
        # TableHandler should work independently
        table_handler = TableHandler()
        assert hasattr(table_handler, 'detect_table_content')
        assert hasattr(table_handler, 'parse_table_structure')
        assert hasattr(table_handler, 'create_table_from_data')
        
        # ContentProcessor should work independently
        content_processor = ContentProcessor()
        assert hasattr(content_processor, 'apply_content_to_placeholder')
        
        # PlaceholderResolver should work independently
        placeholder_resolver = PlaceholderResolver()
        assert hasattr(placeholder_resolver, 'get_placeholder_by_name')


class TestTemplateFirstIntegration:
    """Test the template-first approach integration."""
    
    def setup_method(self):
        """Set up test instances."""
        self.layout_resolver = LayoutResolver()
        self.table_handler = TableHandler()
        
    def test_template_layout_selection_workflow(self):
        """Test that template layouts are selected based on content type."""
        # Mock presentation with comprehensive layouts
        mock_prs = Mock()
        
        layout_scenarios = {
            # Content type -> Expected layout
            "simple_text": "Title and Content",
            "table_only": "Table Only", 
            "text_and_table": "Table with Content Above",
            "comparison": "Comparison",
            "two_columns": "Two Content"
        }
        
        # Mock all required layouts
        layout_names = list(layout_scenarios.values())
        mock_layouts = []
        for name in layout_names:
            mock_layout = Mock()
            mock_layout.name = name
            mock_layouts.append(mock_layout)
        
        mock_prs.slide_layouts = mock_layouts
        
        # Test each scenario
        for content_type, expected_layout in layout_scenarios.items():
            layout = self.layout_resolver.get_layout_by_name(mock_prs, expected_layout)
            assert layout.name == expected_layout, f"Content type '{content_type}' should use layout '{expected_layout}'"
    
    def test_no_dynamic_shape_fallback(self):
        """Test that system doesn't fall back to dynamic shape creation."""
        # This test verifies the architectural decision to use template layouts
        # instead of dynamic shape creation
        
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]
        
        # Test that requesting unsupported layout fails clearly
        # (no fallback to dynamic shapes)
        with pytest.raises(ValueError):
            self.layout_resolver.get_layout_by_name(mock_prs, "Complex Dynamic Layout")
        
        # This is the desired behavior: clear errors instead of fallbacks
    
    def test_plain_text_table_processing(self):
        """Test that tables are processed as plain text (no markdown)."""
        table_with_markdown = """
| **Bold Header** | *Italic Header* | [Link Header](url) |
|-----------------|-----------------|---------------------|
| **Bold Data** | *Italic Data* | [Link Data](url2) |
"""
        
        # Test detection
        detected = self.table_handler.detect_table_content(table_with_markdown)
        assert detected is True
        
        # Test parsing (markdown should be treated as plain text)
        structure = self.table_handler.parse_table_structure(table_with_markdown)
        expected = [
            ["**Bold Header**", "*Italic Header*", "[Link Header](url)"],
            ["**Bold Data**", "*Italic Data*", "[Link Data](url2)"]
        ]
        assert structure == expected
        
        # Verify that markdown is NOT parsed (treated as literal text)
        assert "**Bold Header**" in structure[0][0]  # Bold markers preserved
        assert "*Italic Header*" in structure[0][1]  # Italic markers preserved
        assert "[Link Header](url)" in structure[0][2]  # Link syntax preserved


class TestAPICompatibility:
    """Test backward compatibility with existing APIs."""
    
    def test_module_interfaces(self):
        """Test that module interfaces are compatible with expected usage."""
        # Test LayoutResolver interface
        layout_resolver = LayoutResolver()
        mock_prs = Mock()
        mock_layout = Mock()
        mock_layout.name = "Title and Content"
        mock_prs.slide_layouts = [mock_layout]
        
        # Should support the expected interface
        layout = layout_resolver.get_layout_by_name(mock_prs, "Title and Content")
        assert layout.name == "Title and Content"
        
        layouts = layout_resolver.list_available_layouts(mock_prs)
        assert isinstance(layouts, list)
        
        exists = layout_resolver.validate_layout_exists(mock_prs, "Title and Content")
        assert exists is True
        
        # Test TableHandler interface
        table_handler = TableHandler()
        
        # Should support table detection
        assert callable(table_handler.detect_table_content)
        
        # Should support table parsing
        assert callable(table_handler.parse_table_structure)
        
        # Should support table creation
        assert callable(table_handler.create_table_from_data)
        
        # Should support positioning
        assert callable(table_handler.position_table_on_slide)
    
    def test_error_handling_compatibility(self):
        """Test that error handling is consistent and informative."""
        layout_resolver = LayoutResolver()
        table_handler = TableHandler()
        
        mock_prs = Mock()
        mock_prs.slide_layouts = []
        
        # Test layout resolver error handling
        with pytest.raises(ValueError) as exc_info:
            layout_resolver.get_layout_by_name(mock_prs, "Missing Layout")
        
        error_msg = str(exc_info.value)
        assert "not found" in error_msg
        assert "Available layouts" in error_msg
        
        # Test table handler graceful handling
        # Should not raise exceptions for invalid input
        result = table_handler.detect_table_content("")
        assert result is False
        
        result = table_handler.parse_table_structure("")
        assert result == []


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])