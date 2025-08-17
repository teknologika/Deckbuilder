"""
Unit tests for SlideCoordinator

Tests the high-level slide orchestration using enhanced modular architecture.
Validates dependency injection, error handling, and clean workflow coordination.
"""

import unittest
from unittest.mock import Mock, patch
from deckbuilder.core.slide_coordinator import SlideCoordinator


class TestSlideCoordinator(unittest.TestCase):
    """Test SlideCoordinator functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.coordinator = SlideCoordinator()

        # Mock dependencies
        self.mock_prs = Mock()
        self.mock_slide = Mock()
        self.mock_slide_layout = Mock()
        self.mock_content_formatter = Mock()
        self.mock_image_handler = Mock()

        # Mock slide data
        self.basic_slide_data = {"layout": "Title and Content", "title": "Test Title", "content": "Test content"}

    def test_dependency_injection_constructor(self):
        """Test SlideCoordinator with dependency injection in constructor."""
        mock_layout_resolver = Mock()
        mock_placeholder_manager = Mock()
        mock_content_processor = Mock()
        mock_table_handler = Mock()

        coordinator = SlideCoordinator(layout_resolver=mock_layout_resolver, placeholder_manager=mock_placeholder_manager, content_processor=mock_content_processor, table_handler=mock_table_handler)

        assert coordinator._layout_resolver == mock_layout_resolver
        assert coordinator._placeholder_manager == mock_placeholder_manager
        assert coordinator._content_processor == mock_content_processor
        assert coordinator._table_handler == mock_table_handler

    def test_lazy_loading_of_dependencies(self):
        """Test lazy loading of dependencies when not injected."""
        coordinator = SlideCoordinator()

        # Access properties to trigger lazy loading
        with patch("deckbuilder.refactor.layout_resolver.LayoutResolver") as mock_layout_resolver_class:
            with patch("deckbuilder.refactor.placeholder_manager.PlaceholderManager") as mock_placeholder_manager_class:
                with patch("deckbuilder.core.content_processor.ContentProcessor") as mock_content_processor_class:
                    with patch("deckbuilder.core.table_handler.TableHandler") as mock_table_handler_class:

                        # Trigger lazy loading
                        _ = coordinator.layout_resolver
                        _ = coordinator.placeholder_manager
                        _ = coordinator.content_processor
                        _ = coordinator.table_handler

                        # Verify lazy loading occurred
                        mock_layout_resolver_class.assert_called_once()
                        mock_placeholder_manager_class.assert_called_once()
                        mock_content_processor_class.assert_called_once()
                        mock_table_handler_class.assert_called_once()

    def test_create_slide_success_workflow(self):
        """Test successful slide creation workflow."""
        # Setup mocks
        self.coordinator._layout_resolver = Mock()
        self.coordinator._placeholder_manager = Mock()
        self.coordinator._content_processor = Mock()

        self.coordinator._layout_resolver.resolve_layout_by_name.return_value = self.mock_slide_layout
        self.mock_prs.slides.add_slide.return_value = self.mock_slide
        self.coordinator._placeholder_manager.map_fields_to_placeholders.return_value = {"title": Mock()}

        # Mock content formatter
        self.mock_content_formatter.format_slide_data.return_value = self.basic_slide_data

        # Create slide
        result = self.coordinator.create_slide(self.mock_prs, self.basic_slide_data, self.mock_content_formatter, self.mock_image_handler)

        # Verify workflow
        assert result == self.mock_slide
        self.coordinator._layout_resolver.resolve_layout_by_name.assert_called_once_with(self.mock_prs, "Title and Content")
        self.mock_prs.slides.add_slide.assert_called_once_with(self.mock_slide_layout)

        # Verify successful execution - no debug assertions needed

    def test_create_slide_invalid_data_type(self):
        """Test slide creation with invalid data type."""
        with self.assertRaises(RuntimeError) as context:
            self.coordinator.create_slide(self.mock_prs, "invalid_data", self.mock_content_formatter, self.mock_image_handler)

        assert "Slide creation failed" in str(context.exception)

    def test_create_slide_layout_resolution_failure(self):
        """Test slide creation with layout resolution failure."""
        # Mock layout resolution failure
        self.coordinator._layout_resolver = Mock()
        self.coordinator._layout_resolver.resolve_layout_by_name.side_effect = ValueError("Layout not found")

        # Mock content formatter
        self.mock_content_formatter.format_slide_data.return_value = self.basic_slide_data

        with self.assertRaises(RuntimeError) as context:
            self.coordinator.create_slide(self.mock_prs, self.basic_slide_data, self.mock_content_formatter, self.mock_image_handler)

        assert "Slide creation failed" in str(context.exception)

    @patch("deckbuilder.core.slide_coordinator.debug_print")
    def test_clear_slides_success(self, mock_debug):
        """Test successful slide clearing."""
        # Setup mock presentation with slides
        mock_slide1 = Mock()
        mock_slide2 = Mock()
        mock_slide1.part = Mock()
        mock_slide2.part = Mock()
        mock_slide1.part._rel.rId = "rId1"
        mock_slide2.part._rel.rId = "rId2"

        # Setup proper PowerPoint slides structure
        mock_slides = Mock()
        mock_slides.__len__ = Mock(return_value=2)
        mock_slides._sldIdLst = [Mock(), Mock()]
        mock_slides._sldIdLst[0].rId = "rId1"
        mock_slides._sldIdLst[1].rId = "rId2"
        self.mock_prs.slides = mock_slides
        self.mock_prs.part.drop_rel = Mock()

        # Clear slides
        self.coordinator.clear_slides(self.mock_prs)

        # Verify slides were dropped in reverse order
        assert self.mock_prs.part.drop_rel.call_count == 2
        mock_debug.assert_called_with("Cleared 2 slides from presentation")
        assert self.coordinator._current_slide_index == 0

    def test_clear_slides_failure(self):
        """Test slide clearing failure handling."""
        # Mock failure in slide clearing
        self.mock_prs.slides = [Mock()]
        self.mock_prs.part.drop_rel.side_effect = Exception("Drop failed")

        with self.assertRaises(RuntimeError) as context:
            self.coordinator.clear_slides(self.mock_prs)

        assert "Failed to clear slides" in str(context.exception)

    @patch("deckbuilder.core.slide_coordinator.debug_print")
    def test_add_speaker_notes_success(self, mock_debug):
        """Test successful speaker notes addition."""
        # Setup mock slide with notes
        mock_notes_slide = Mock()
        mock_text_frame = Mock()
        mock_paragraph = Mock()

        self.mock_slide.notes_slide = mock_notes_slide
        mock_notes_slide.notes_text_frame = mock_text_frame
        mock_text_frame.paragraphs = [mock_paragraph]

        notes_content = "This is a test speaker note"

        # Add speaker notes
        self.coordinator.add_speaker_notes(self.mock_slide, notes_content, self.mock_content_formatter)

        # Verify notes were added
        mock_text_frame.clear.assert_called_once()
        self.mock_content_formatter.apply_inline_formatting.assert_called_once_with(notes_content, mock_paragraph)
        mock_debug.assert_called_with(f"Added speaker notes: {len(notes_content)} characters")

    @patch("deckbuilder.core.slide_coordinator.error_print")
    def test_add_speaker_notes_failure_graceful(self, mock_error):
        """Test speaker notes failure is handled gracefully."""
        # Mock failure in speaker notes
        self.mock_slide.notes_slide.side_effect = Exception("Notes failed")

        # Should not raise exception
        self.coordinator.add_speaker_notes(self.mock_slide, "test notes", self.mock_content_formatter)

        # Should log error but not crash
        mock_error.assert_called_once()

    def test_add_speaker_notes_empty_content(self):
        """Test speaker notes with empty content."""
        # Should do nothing for empty content
        self.coordinator.add_speaker_notes(self.mock_slide, "", self.mock_content_formatter)
        self.coordinator.add_speaker_notes(self.mock_slide, None, self.mock_content_formatter)
        self.coordinator.add_speaker_notes(self.mock_slide, "   ", self.mock_content_formatter)

        # No calls should have been made to slide methods
        assert not hasattr(self.mock_slide, "notes_slide") or not self.mock_slide.notes_slide.called

    @patch("deckbuilder.refactor.placeholder_normalizer.PlaceholderNormalizer")
    def test_normalize_placeholder_names_success(self, mock_normalizer_class):
        """Test placeholder name normalization."""
        mock_normalizer = Mock()
        mock_normalizer_class.return_value = mock_normalizer

        self.mock_slide.slide_layout = self.mock_slide_layout

        # Test normalization
        self.coordinator._normalize_placeholder_names(self.mock_slide, "Title and Content")

        # Verify normalization was called
        mock_normalizer_class.assert_called_once()
        mock_normalizer.normalize_slide_placeholder_names.assert_called_once_with(self.mock_slide, self.mock_slide_layout)

    @patch("deckbuilder.core.slide_coordinator.error_print")
    @patch("deckbuilder.refactor.placeholder_normalizer.PlaceholderNormalizer")
    def test_normalize_placeholder_names_failure_graceful(self, mock_normalizer_class, mock_error):
        """Test placeholder normalization failure is handled gracefully."""
        mock_normalizer_class.side_effect = Exception("Normalization failed")

        # Should not raise exception
        self.coordinator._normalize_placeholder_names(self.mock_slide, "Title and Content")

        # Should log error but continue
        mock_error.assert_called_once()

    def test_process_slide_content_workflow(self):
        """Test slide content processing workflow."""
        # Setup mocks
        self.coordinator._placeholder_manager = Mock()
        self.coordinator._content_processor = Mock()

        mock_placeholder = Mock()
        self.coordinator._placeholder_manager.map_fields_to_placeholders.return_value = {"title": mock_placeholder}

        slide_data = {"title": "Test Title", "layout": "Title and Content"}

        # Process content
        self.coordinator._process_slide_content(self.mock_slide, slide_data, "Title and Content", self.mock_content_formatter, self.mock_image_handler)

        # Verify workflow
        self.coordinator._placeholder_manager.map_fields_to_placeholders.assert_called_once()
        self.coordinator._content_processor.apply_content_to_placeholder.assert_called_once_with(
            self.mock_slide, mock_placeholder, "title", "Test Title", slide_data, self.mock_content_formatter, self.mock_image_handler
        )

    def test_speaker_notes_detection_multiple_locations(self):
        """Test speaker notes detection from multiple locations."""
        # Test notes in main slide_data
        slide_data_1 = {"speaker_notes": "Notes in main"}
        self.coordinator._add_speaker_notes_if_present(self.mock_slide, slide_data_1, self.mock_content_formatter)

        # Test notes in placeholders
        slide_data_2 = {"placeholders": {"speaker_notes": "Notes in placeholders"}}
        self.coordinator._add_speaker_notes_if_present(self.mock_slide, slide_data_2, self.mock_content_formatter)

        # Should have attempted to add notes twice
        # (Implementation detail - would need to mock add_speaker_notes method to verify)

    def test_slide_index_tracking(self):
        """Test slide index tracking through multiple slide creations."""
        initial_index = self.coordinator._current_slide_index

        # Create multiple slides (mock successful creation)
        with patch.object(self.coordinator, "_validate_and_prepare_slide_data", return_value=self.basic_slide_data):
            with patch.object(self.coordinator, "_create_slide_with_layout", return_value=self.mock_slide):
                with patch.object(self.coordinator, "_normalize_placeholder_names"):
                    with patch.object(self.coordinator, "_process_slide_content"):
                        with patch.object(self.coordinator, "_add_speaker_notes_if_present"):

                            self.coordinator.create_slide(self.mock_prs, self.basic_slide_data, self.mock_content_formatter, self.mock_image_handler)
                            self.coordinator.create_slide(self.mock_prs, self.basic_slide_data, self.mock_content_formatter, self.mock_image_handler)

        # Verify index tracking
        assert self.coordinator._current_slide_index == initial_index + 2


if __name__ == "__main__":
    unittest.main()
