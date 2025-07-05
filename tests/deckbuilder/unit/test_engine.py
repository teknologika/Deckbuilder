"""
Unit tests for the refactored, JSON-only Deckbuilder engine.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

import pytest

# Test imports with graceful handling
try:
    from deckbuilder.engine import Deckbuilder
    HAS_ENGINE = True
except ImportError:
    HAS_ENGINE = False


@pytest.mark.skipif(not HAS_ENGINE, reason="Deckbuilder engine not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestEngineRendering(unittest.TestCase):

    def setUp(self):
        """Set up a fresh engine instance and mock the Presentation object for each test."""
        # This patch will mock the Presentation class in the engine module
        self.patcher = patch('deckbuilder.engine.Presentation')
        self.mock_presentation_class = self.patcher.start()
        self.mock_presentation = self.mock_presentation_class.return_value

        # Mock the slide layouts
        self.mock_presentation.slide_layouts = MagicMock()
        self.mock_presentation.slides = MagicMock()

        # Instantiate the engine
        self.engine = Deckbuilder(path_manager_instance=MagicMock())
        self.engine.prs = self.mock_presentation

    def tearDown(self):
        """Stop the patcher after each test."""
        self.patcher.stop()

    def test_add_slide_with_title_and_paragraph(self):
        """
        Verify that a simple slide with a title and paragraph
        calls the correct pptx methods.
        """
        canonical_slide = {
            "layout": "Title and Content",
            "placeholders": {
                "title": "My Test Title"
            },
            "content": [
                {
                    "type": "paragraph",
                    "text": "This is a test paragraph."
                }
            ]
        }

        # Call the method under test
        self.engine.presentation_builder.add_slide(self.engine.prs, canonical_slide)

        # Assertions
        self.mock_presentation.slides.add_slide.assert_called_once()
        mock_slide = self.mock_presentation.slides.add_slide.return_value

        # This is a simplified assertion. A real implementation would need to
        # mock the placeholder objects and their text frames to verify the title
        # and content were set correctly.
        self.assertGreater(mock_slide.placeholders.__setitem__.call_count, 0)

    def test_add_slide_with_heading_and_bullets(self):
        """
        Verify that a slide with a heading and bullet points is processed correctly.
        """
        canonical_slide = {
            "layout": "Title and Content",
            "content": [
                {
                    "type": "heading",
                    "level": 1,
                    "text": "This is a Heading"
                },
                {
                    "type": "bullets",
                    "items": [
                        {"level": 1, "text": "Bullet 1"},
                        {"level": 2, "text": "Bullet 1.1"}
                    ]
                }
            ]
        }

        self.engine.presentation_builder.add_slide(self.engine.prs, canonical_slide)

        self.mock_presentation.slides.add_slide.assert_called_once()
        mock_slide = self.mock_presentation.slides.add_slide.return_value

        # Again, a simplified assertion. A more robust test would inspect the
        # calls to add_paragraph, and check the level property of the paragraphs.
        self.assertGreater(mock_slide.shapes.add_textbox.call_count, 0)

    def test_add_slide_with_table(self):
        """
        Verify that a slide with a table is processed correctly.
        """
        canonical_slide = {
            "layout": "Title and Content",
            "content": [
                {
                    "type": "table",
                    "header": ["Col A", "Col B"],
                    "rows": [
                        ["Cell 1", "Cell 2"],
                        ["Cell 3", "Cell 4"]
                    ]
                }
            ]
        }

        self.engine.presentation_builder.add_slide(self.engine.prs, canonical_slide)

        self.mock_presentation.slides.add_slide.assert_called_once()
        mock_slide = self.mock_presentation.slides.add_slide.return_value
        mock_slide.shapes.add_table.assert_called_once()