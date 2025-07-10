"""
Unit tests for the refactored, canonical JSON-only Deckbuilder engine.
"""

import unittest
from unittest.mock import Mock, patch
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
class TestEngineCanonicalJSON(unittest.TestCase):
    """Test engine with canonical JSON format only"""

    def setUp(self):
        """Set up a fresh engine instance with proper mocking"""
        # Reset singleton before each test
        if HAS_ENGINE:
            Deckbuilder.reset()

        # Mock path manager
        self.mock_path_manager = Mock()
        self.mock_path_manager.get_output_folder.return_value = "/tmp/test"
        self.mock_path_manager.get_template_name.return_value = "default"
        self.mock_path_manager.get_template_folder.return_value = "/tmp/templates"

        # Mock presentation builder
        self.mock_presentation_builder = Mock()

        # Create engine with mocked components
        with (
            patch("deckbuilder.engine.PresentationBuilder") as mock_pb_class,
            patch("deckbuilder.engine.TemplateManager") as mock_tm_class,
            patch("deckbuilder.engine.ContentProcessor") as mock_cp_class,
            patch("deckbuilder.engine.Presentation") as mock_prs_class,
        ):

            mock_pb_class.return_value = self.mock_presentation_builder
            self.mock_template_manager = mock_tm_class.return_value
            self.mock_content_processor = mock_cp_class.return_value
            self.mock_prs = mock_prs_class.return_value

            # Mock the prepare_template method to return expected tuple
            # Using None for template_path to avoid trying to load real PowerPoint file
            self.mock_template_manager.prepare_template.return_value = (
                None,  # No template path - will create empty presentation
                {"layouts": {"Title Slide": {"index": 0}, "Title and Content": {"index": 1}}},
            )

            # Mock check_template_exists method
            self.mock_template_manager.check_template_exists.return_value = None

            self.engine = Deckbuilder(path_manager_instance=self.mock_path_manager)

    def test_canonical_json_validation_success(self):
        """Test that valid canonical JSON format is accepted"""
        valid_canonical_data = {
            "slides": [
                {
                    "layout": "Title Slide",
                    "style": "default_style",
                    "placeholders": {"title": "Test Title"},
                    "content": [],
                }
            ]
        }

        # Mock the write_presentation method and validation to avoid file I/O
        with (
            patch.object(self.engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = self.engine.create_presentation(valid_canonical_data, "test")

        # Verify presentation builder was called with canonical data
        self.mock_presentation_builder.add_slide.assert_called_once()
        self.assertIn("Successfully created presentation with 1 slides", result)

    def test_canonical_json_validation_missing_slides(self):
        """Test that missing 'slides' array raises ValueError"""
        invalid_data = {"other": "data"}  # No 'slides' key

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("'slides' array at root level", str(context.exception))

    def test_canonical_json_validation_empty_slides(self):
        """Test that empty slides array raises ValueError"""
        invalid_data = {"slides": []}

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("At least one slide is required", str(context.exception))

    def test_canonical_json_validation_invalid_slide_structure(self):
        """Test that slides without required fields raise ValueError"""
        invalid_data = {"slides": [{"style": "default_style", "placeholders": {}, "content": []}]}  # Missing 'layout'

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("must have a 'layout' field", str(context.exception))

    def test_canonical_json_validation_invalid_placeholders_type(self):
        """Test that non-dict placeholders raise ValueError"""
        invalid_data = {
            "slides": [
                {
                    "layout": "Title Slide",
                    "placeholders": "invalid",  # Should be dict
                    "content": [],
                }
            ]
        }

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("'placeholders' must be a dictionary", str(context.exception))

    def test_canonical_json_validation_invalid_content_type(self):
        """Test that non-array content raises ValueError"""
        invalid_data = {
            "slides": [
                {
                    "layout": "Title and Content",
                    "placeholders": {},
                    "content": "invalid",  # Should be array
                }
            ]
        }

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("'content' must be an array", str(context.exception))

    def test_create_presentation_with_content_blocks(self):
        """Test presentation creation with various content block types"""
        canonical_data = {
            "slides": [
                {
                    "layout": "Title and Content",
                    "style": "default_style",
                    "placeholders": {"title": "Test Slide with **Bold** Text"},
                    "content": [
                        {"type": "heading", "level": 1, "text": "Main Heading"},
                        {
                            "type": "paragraph",
                            "text": "This is a test paragraph with *formatting*.",
                        },
                        {
                            "type": "bullets",
                            "items": [
                                {"level": 1, "text": "First bullet"},
                                {"level": 2, "text": "Sub bullet"},
                                {"level": 1, "text": "Second bullet"},
                            ],
                        },
                        {
                            "type": "table",
                            "style": "dark_blue_white_text",
                            "header": ["Column A", "Column B"],
                            "rows": [["Data 1", "Data 2"], ["Data 3", "Data 4"]],
                        },
                    ],
                }
            ]
        }

        with (
            patch.object(self.engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = self.engine.create_presentation(canonical_data, "complex_test")

        # Verify result is successful
        self.assertIn("Successfully created presentation", result)

        # Verify all content types were processed
        self.mock_presentation_builder.add_slide.assert_called_once()
        call_args = self.mock_presentation_builder.add_slide.call_args
        slide_data = call_args[0][1]  # Second argument is slide_data

        self.assertEqual(slide_data["layout"], "Title and Content")
        self.assertEqual(len(slide_data["content"]), 4)
        self.assertEqual(slide_data["content"][0]["type"], "heading")
        self.assertEqual(slide_data["content"][1]["type"], "paragraph")
        self.assertEqual(slide_data["content"][2]["type"], "bullets")
        self.assertEqual(slide_data["content"][3]["type"], "table")

    def test_multiple_slides_processing(self):
        """Test that multiple slides are processed correctly"""
        canonical_data = {
            "slides": [
                {"layout": "Title Slide", "placeholders": {"title": "First Slide"}, "content": []},
                {
                    "layout": "Title and Content",
                    "placeholders": {"title": "Second Slide"},
                    "content": [{"type": "paragraph", "text": "Second slide content"}],
                },
                {
                    "layout": "Blank",
                    "placeholders": {},
                    "content": [{"type": "heading", "level": 1, "text": "Blank slide heading"}],
                },
            ]
        }

        with (
            patch.object(self.engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = self.engine.create_presentation(canonical_data, "multi_slide_test")

        # Verify all slides were processed
        self.assertEqual(self.mock_presentation_builder.add_slide.call_count, 3)
        self.assertIn("Successfully created presentation with 3 slides", result)

    def test_rejects_invalid_structure(self):
        """Test that invalid data structure is rejected"""
        invalid_data = {
            "presentation": {
                "slides": [
                    {
                        "layout": "Title Slide",
                        "placeholders": {"title": "Test"},
                        "content": [],
                    }
                ]
            }
        }

        with self.assertRaises(ValueError) as context:
            self.engine.create_presentation(invalid_data)

        self.assertIn("'slides' array at root level", str(context.exception))

    def test_rejects_non_dict_input(self):
        """Test that non-dictionary input is rejected"""
        invalid_inputs = ["string", 123, [], None]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValueError) as context:
                    self.engine.create_presentation(invalid_input)

                self.assertIn("must be a dictionary", str(context.exception))
