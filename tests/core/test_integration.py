"""
Integration tests for enhanced modular architecture

Tests the complete workflow from SlideBuilder through SlideCoordinator
to all enhanced modules, ensuring seamless integration and backward compatibility.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.deckbuilder.core.slide_builder import SlideBuilder
from src.deckbuilder.core.presentation_builder import PresentationBuilder


class TestArchitectureIntegration(unittest.TestCase):
    """Test integration between all enhanced modules."""

    def setUp(self):
        """Set up test fixtures."""
        self.slide_builder = SlideBuilder()
        
        # Mock PowerPoint objects
        self.mock_prs = Mock()
        self.mock_slide_layout = Mock() 
        self.mock_slide = Mock()
        self.mock_content_formatter = Mock()
        self.mock_image_handler = Mock()
        
        # Test slide data
        self.test_slide_data = {
            "layout": "Title and Content",
            "title": "Integration Test",
            "content": "Testing enhanced architecture"
        }

    def test_slidebuilder_delegates_to_coordinator(self):
        """Test that SlideBuilder correctly delegates to SlideCoordinator."""
        # Mock the coordinator's create_slide method
        with patch.object(self.slide_builder._coordinator, 'create_slide', return_value=self.mock_slide) as mock_create:
            
            result = self.slide_builder.add_slide(
                self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
            )
            
            # Verify delegation
            mock_create.assert_called_once_with(
                self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
            )
            assert result == self.mock_slide

    def test_slidebuilder_clear_slides_delegation(self):
        """Test clear_slides delegation to coordinator."""
        with patch.object(self.slide_builder._coordinator, 'clear_slides') as mock_clear:
            
            self.slide_builder.clear_slides(self.mock_prs)
            
            mock_clear.assert_called_once_with(self.mock_prs)

    def test_slidebuilder_speaker_notes_delegation(self):
        """Test add_speaker_notes delegation to coordinator."""
        with patch.object(self.slide_builder._coordinator, 'add_speaker_notes') as mock_notes:
            
            self.slide_builder.add_speaker_notes(self.mock_slide, "Test notes", self.mock_content_formatter)
            
            mock_notes.assert_called_once_with(self.mock_slide, "Test notes", self.mock_content_formatter)

    def test_enhanced_modules_accessible_through_slidebuilder(self):
        """Test that all enhanced modules are accessible through SlideBuilder."""
        # Test property access
        layout_resolver = self.slide_builder.layout_resolver
        placeholder_manager = self.slide_builder.placeholder_manager
        content_processor = self.slide_builder.content_processor
        table_handler = self.slide_builder.table_handler
        coordinator = self.slide_builder.coordinator
        
        # Verify all modules are accessible
        assert layout_resolver is not None
        assert placeholder_manager is not None
        assert content_processor is not None
        assert table_handler is not None
        assert coordinator is not None
        
        # Verify they're the same instances (proper delegation)
        assert layout_resolver is coordinator.layout_resolver
        assert placeholder_manager is coordinator.placeholder_manager
        assert content_processor is coordinator.content_processor
        assert table_handler is coordinator.table_handler

    def test_presentation_builder_integration(self):
        """Test PresentationBuilder works with new SlideBuilder."""
        # This tests that PresentationBuilder can instantiate and use the new SlideBuilder
        try:
            # Create mock path manager for PresentationBuilder  
            from unittest.mock import Mock
            from pathlib import Path
            mock_path_manager = Mock()
            mock_path_manager.get_output_folder.return_value = Path("/tmp")
            
            presentation_builder = PresentationBuilder(mock_path_manager)
            
            # Verify it uses the new SlideBuilder
            assert hasattr(presentation_builder, 'slide_builder')
            assert hasattr(presentation_builder.slide_builder, 'coordinator')
            
            print("✅ PresentationBuilder integration successful")
            
        except Exception as e:
            self.fail(f"PresentationBuilder integration failed: {e}")

    def test_backward_compatibility_method_signatures(self):
        """Test that all method signatures remain exactly the same."""
        import inspect
        
        # Test add_slide signature
        add_slide_sig = inspect.signature(self.slide_builder.add_slide)
        expected_params = ['prs', 'slide_data', 'content_formatter', 'image_placeholder_handler']
        actual_params = list(add_slide_sig.parameters.keys())
        
        assert actual_params == expected_params, f"add_slide signature changed: {actual_params}"
        
        # Test clear_slides signature
        clear_slides_sig = inspect.signature(self.slide_builder.clear_slides)
        assert list(clear_slides_sig.parameters.keys()) == ['prs']
        
        # Test add_speaker_notes signature
        notes_sig = inspect.signature(self.slide_builder.add_speaker_notes)
        assert list(notes_sig.parameters.keys()) == ['slide', 'notes_content', 'content_formatter']

    def test_legacy_private_method_compatibility(self):
        """Test that legacy private methods are preserved for compatibility."""
        # Test _find_placeholder_by_name exists and works
        mock_slide = Mock()
        mock_slide.placeholders = []  # Make placeholders iterable
        result = self.slide_builder._find_placeholder_by_name(mock_slide, "test_field")
        
        # Should not crash and should return None for non-existent placeholder
        assert result is None

    def test_field_processor_preserved(self):
        """Test that field_processor is preserved for compatibility."""
        assert hasattr(self.slide_builder, 'field_processor')
        assert self.slide_builder.field_processor is not None

    @patch('src.deckbuilder.core.slide_coordinator.debug_print')
    def test_end_to_end_slide_creation_workflow(self, mock_debug):
        """Test complete end-to-end slide creation workflow."""
        # Mock all dependencies for a complete workflow test
        with patch.object(self.slide_builder.layout_resolver, 'resolve_layout_by_name', return_value=self.mock_slide_layout):
            with patch.object(self.slide_builder.placeholder_manager, 'map_fields_to_placeholders', return_value={"title": Mock()}):
                with patch.object(self.slide_builder.content_processor, 'apply_content_to_placeholder'):
                    
                    self.mock_prs.slides.add_slide.return_value = self.mock_slide
                    self.mock_content_formatter.format_slide_data.return_value = self.test_slide_data
                    
                    # Execute complete workflow
                    result = self.slide_builder.add_slide(
                        self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
                    )
                    
                    # Verify result
                    assert result == self.mock_slide
                    
                    # Verify workflow steps were executed
                    self.slide_builder.layout_resolver.resolve_layout_by_name.assert_called_once()
                    self.mock_prs.slides.add_slide.assert_called_once()
                    self.slide_builder.placeholder_manager.map_fields_to_placeholders.assert_called_once()
                    self.slide_builder.content_processor.apply_content_to_placeholder.assert_called_once()

    def test_error_handling_propagation(self):
        """Test that errors are properly propagated through the delegation chain."""
        # Test that errors from coordinator are properly propagated
        with patch.object(self.slide_builder._coordinator, 'create_slide', side_effect=RuntimeError("Test error")):
            
            with self.assertRaises(RuntimeError) as context:
                self.slide_builder.add_slide(
                    self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
                )
            
            assert "Test error" in str(context.exception)

    def test_module_count_and_architecture(self):
        """Test that we have the expected 5-module architecture."""
        # Verify we have exactly the expected modules
        modules = {
            'layout_resolver': self.slide_builder.layout_resolver,
            'placeholder_manager': self.slide_builder.placeholder_manager, 
            'content_processor': self.slide_builder.content_processor,
            'table_handler': self.slide_builder.table_handler,
            'slide_coordinator': self.slide_builder.coordinator
        }
        
        assert len(modules) == 5, f"Expected 5 modules, got {len(modules)}"
        
        # Verify all modules are distinct objects
        module_ids = [id(module) for module in modules.values()]
        assert len(set(module_ids)) == 5, "Modules should be distinct objects"

    def test_add_slide_with_direct_mapping_compatibility(self):
        """Test that add_slide_with_direct_mapping maintains compatibility."""
        with patch.object(self.slide_builder._coordinator, 'create_slide', return_value=self.mock_slide) as mock_create:
            
            result = self.slide_builder.add_slide_with_direct_mapping(
                self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
            )
            
            # Should delegate to the same create_slide method
            mock_create.assert_called_once_with(
                self.mock_prs, self.test_slide_data, self.mock_content_formatter, self.mock_image_handler
            )
            assert result == self.mock_slide


class TestMCPServerCompatibility(unittest.TestCase):
    """Test compatibility with MCP server integration."""
    
    def test_slidebuilder_import_compatibility(self):
        """Test that SlideBuilder can be imported as before."""
        # Test import from core module
        from src.deckbuilder.core import SlideBuilder
        builder = SlideBuilder()
        
        # Test that it has the enhanced architecture
        assert hasattr(builder, 'coordinator')
        assert hasattr(builder, 'layout_resolver')
        
    def test_legacy_slidebuilder_still_available(self):
        """Test that legacy SlideBuilder is still available if needed."""
        from src.deckbuilder.core import SlideBuilderLegacy
        legacy_builder = SlideBuilderLegacy()
        
        # Should be the old implementation
        assert not hasattr(legacy_builder, 'coordinator')
        assert hasattr(legacy_builder, 'field_processor')


if __name__ == '__main__':
    unittest.main()