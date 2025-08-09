"""
Unit tests for the refactored, canonical JSON-only Deckbuilder engine.
"""

from unittest.mock import Mock, patch
import pytest

# Test imports with graceful handling
try:
    from deckbuilder.core.engine import Deckbuilder

    HAS_ENGINE = True
except ImportError:
    HAS_ENGINE = False


@pytest.fixture
def engine_setup():
    """Set up a fresh engine instance with proper mocking"""
    # Reset singleton before each test
    if HAS_ENGINE:
        Deckbuilder.reset()

    # Mock path manager
    mock_path_manager = Mock()
    mock_path_manager.get_output_folder.return_value = "/tmp/test"
    mock_path_manager.get_template_name.return_value = "default"
    mock_path_manager.get_template_folder.return_value = "/tmp/templates"

    # Mock presentation builder
    mock_presentation_builder = Mock()

    # Create engine with mocked components
    with (
        patch("deckbuilder.core.engine.PresentationBuilder") as mock_pb_class,
        patch("deckbuilder.templates.manager.TemplateManager") as mock_tm_class,
        patch("deckbuilder.content.processor.ContentProcessor") as mock_cp_class,
        patch("pptx.Presentation") as mock_prs_class,
    ):

        mock_pb_class.return_value = mock_presentation_builder
        mock_template_manager = mock_tm_class.return_value
        mock_content_processor = mock_cp_class.return_value
        mock_prs = mock_prs_class.return_value

        # Mock the prepare_template method to return expected tuple
        # Using None for template_path to avoid trying to load real PowerPoint file
        mock_template_manager.prepare_template.return_value = (
            None,  # No template path - will create empty presentation
            {"layouts": {"Title Slide": {"index": 0}, "Title and Content": {"index": 1}}},
        )

        # Mock check_template_exists method
        mock_template_manager.check_template_exists.return_value = None

        engine = Deckbuilder(path_manager_instance=mock_path_manager)

        # Return all mock objects that tests might need
        return {
            "engine": engine,
            "mock_path_manager": mock_path_manager,
            "mock_presentation_builder": mock_presentation_builder,
            "mock_template_manager": mock_template_manager,
            "mock_content_processor": mock_content_processor,
            "mock_prs": mock_prs,
        }


@pytest.mark.skipif(not HAS_ENGINE, reason="Deckbuilder engine not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestEngineCanonicalJSON:
    """Test engine with canonical JSON format only"""

    def test_canonical_json_validation_success(self, engine_setup):
        """Test that valid canonical JSON format is accepted"""
        setup = engine_setup
        engine = setup["engine"]
        mock_presentation_builder = setup["mock_presentation_builder"]

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
            patch.object(engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = engine.create_presentation(valid_canonical_data, "test")

        # Verify presentation builder was called with canonical data
        mock_presentation_builder.add_slide.assert_called_once()
        assert "Successfully created presentation with 1 slides" in result

    def test_canonical_json_validation_missing_slides(self, engine_setup):
        """Test that missing 'slides' array raises ValueError"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_data = {"other": "data"}  # No 'slides' key

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "'slides' array at root level" in str(exc_info.value)

    def test_canonical_json_validation_empty_slides(self, engine_setup):
        """Test that empty slides array raises ValueError"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_data = {"slides": []}

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "At least one slide is required" in str(exc_info.value)

    def test_canonical_json_validation_invalid_slide_structure(self, engine_setup):
        """Test that slides without required fields raise ValueError"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_data = {"slides": [{"style": "default_style", "placeholders": {}, "content": []}]}  # Missing 'layout'

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "must have a 'layout' field" in str(exc_info.value)

    def test_canonical_json_validation_invalid_placeholders_type(self, engine_setup):
        """Test that non-dict placeholders raise ValueError"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_data = {
            "slides": [
                {
                    "layout": "Title Slide",
                    "placeholders": "invalid",  # Should be dict
                    "content": [],
                }
            ]
        }

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "'placeholders' must be a dictionary" in str(exc_info.value)

    def test_canonical_json_validation_invalid_content_type(self, engine_setup):
        """Test that non-array content raises ValueError"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_data = {
            "slides": [
                {
                    "layout": "Title and Content",
                    "placeholders": {},
                    "content": "invalid",  # Should be array
                }
            ]
        }

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "'content' must be an array" in str(exc_info.value)

    def test_create_presentation_with_content_blocks(self, engine_setup):
        """Test presentation creation with various content block types"""
        setup = engine_setup
        engine = setup["engine"]
        mock_presentation_builder = setup["mock_presentation_builder"]

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
            patch.object(engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = engine.create_presentation(canonical_data, "complex_test")

        # Verify result is successful
        assert "Successfully created presentation" in result

        # Verify all content types were processed
        mock_presentation_builder.add_slide.assert_called_once()
        call_args = mock_presentation_builder.add_slide.call_args
        slide_data = call_args[0][1]  # Second argument is slide_data

        assert slide_data["layout"] == "Title and Content"
        assert len(slide_data["content"]) == 4
        assert slide_data["content"][0]["type"] == "heading"
        assert slide_data["content"][1]["type"] == "paragraph"
        assert slide_data["content"][2]["type"] == "bullets"
        assert slide_data["content"][3]["type"] == "table"

    def test_multiple_slides_processing(self, engine_setup):
        """Test that multiple slides are processed correctly"""
        setup = engine_setup
        engine = setup["engine"]
        mock_presentation_builder = setup["mock_presentation_builder"]

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
            patch.object(engine, "write_presentation", return_value="test.pptx"),
            patch("deckbuilder.validation.PresentationValidator") as mock_validator,
        ):
            mock_val_instance = mock_validator.return_value
            mock_val_instance.validate_pre_generation.return_value = None
            mock_val_instance.validate_post_generation.return_value = None
            result = engine.create_presentation(canonical_data, "multi_slide_test")

        # Verify all slides were processed
        assert mock_presentation_builder.add_slide.call_count == 3
        assert "Successfully created presentation with 3 slides" in result

    def test_rejects_invalid_structure(self, engine_setup):
        """Test that invalid data structure is rejected"""
        setup = engine_setup
        engine = setup["engine"]

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

        with pytest.raises(ValueError) as exc_info:
            engine.create_presentation(invalid_data)

        assert "'slides' array at root level" in str(exc_info.value)

    def test_rejects_non_dict_input(self, engine_setup):
        """Test that non-dictionary input is rejected"""
        setup = engine_setup
        engine = setup["engine"]

        invalid_inputs = ["string", 123, [], None]

        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError) as exc_info:
                engine.create_presentation(invalid_input)

            assert "must be a dictionary" in str(exc_info.value)
