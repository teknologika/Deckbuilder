#!/usr/bin/env python3
"""
Pytest test suite for Deckbuilder-PlaceKitten image integration.
Tests image insertion, fallback functionality, and PowerPoint generation.
"""

import os
import sys
import secrets
import shutil
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

import pytest  # noqa: E402
from deckbuilder.engine import Deckbuilder  # noqa: E402


@pytest.fixture
def test_output_dir():
    """Create and return test output directory with unique hex string."""
    # Generate random 6-digit hex string for unique folder name
    hex_id = secrets.token_hex(3)  # 3 bytes = 6 hex characters
    output_dir = Path(__file__).parent / "output" / f"test_{hex_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    yield output_dir

    # Clean up after test
    if output_dir.exists():
        shutil.rmtree(output_dir)


@pytest.fixture
def deckbuilder_with_env(test_output_dir):
    """Initialize Deckbuilder with proper environment variables."""
    # Set required environment variables
    original_env = {}
    env_vars = {
        "DECK_TEMPLATE_FOLDER": str(project_root / "src" / "deckbuilder" / "assets" / "templates"),
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": str(test_output_dir),
    }

    # Store original values and set new ones
    for key, value in env_vars.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    # Reset singleton to pick up new environment variables
    Deckbuilder.reset()

    deck = Deckbuilder()

    yield deck

    # Restore original environment
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


class TestDeckbuilderImageBasic:
    """Test basic Deckbuilder image functionality."""

    def test_deckbuilder_initialization_with_images(self, deckbuilder_with_env):
        """Test Deckbuilder initializes with image components."""
        deck = deckbuilder_with_env

        assert hasattr(deck, "image_handler")
        assert hasattr(deck, "placekitten")
        assert deck.image_handler is not None
        assert deck.placekitten is not None

    def test_placekitten_availability(self, deckbuilder_with_env):
        """Test PlaceKitten availability through Deckbuilder."""
        deck = deckbuilder_with_env

        assert deck.placekitten.is_available()

        fallback_info = deck.placekitten.get_fallback_info((800, 600))
        assert fallback_info["available"] is True
        assert "image_id" in fallback_info
        assert fallback_info["styling"]["base_filter"] == "grayscale"

    def test_image_handler_validation(self, deckbuilder_with_env):
        """Test image validation functionality."""
        deck = deckbuilder_with_env

        # Test valid image
        valid_image = "src/placekitten/images/ACuteKitten-1.png"
        assert deck.image_handler.validate_image(valid_image) is True

        # Test invalid image
        invalid_image = "assets/non_existent.png"
        assert deck.image_handler.validate_image(invalid_image) is False


class TestMarkdownImageIntegration:
    """Test image integration with markdown input."""

    def test_markdown_with_valid_image(self, deckbuilder_with_env, test_output_dir):
        """Test markdown with valid image path."""
        deck = deckbuilder_with_env

        markdown = """---
layout: Picture with Caption
title: Test Valid Image
media:
  image_path: "src/placekitten/images/ACuteKitten-1.png"
  caption: "Test kitten image"
---
"""

        result = deck.create_presentation_from_markdown(markdown, "test_valid_image")

        assert "Successfully created presentation" in result

        # Check output file exists and has reasonable size
        output_files = list(test_output_dir.glob("*.pptx"))
        assert (
            len(output_files) > 0
        ), f"No .pptx files found in {test_output_dir}. Files present: {list(test_output_dir.glob('*'))}"

        output_file = output_files[0]
        file_size_kb = output_file.stat().st_size / 1024
        assert file_size_kb > 50, f"File size {file_size_kb:.1f}KB too small for embedded image"

    def test_markdown_with_fallback_image(self, deckbuilder_with_env, test_output_dir):
        """Test markdown with missing image (triggers PlaceKitten fallback)."""
        deck = deckbuilder_with_env

        markdown = """---
layout: Picture with Caption
title: Test Fallback Image
media:
  image_path: "assets/non_existent_image.png"
  caption: "PlaceKitten fallback"
---
"""

        result = deck.create_presentation_from_markdown(markdown, "test_fallback_image")

        assert "Successfully created presentation" in result

        # Check output file exists and has reasonable size
        output_files = list(test_output_dir.glob("*.pptx"))
        assert (
            len(output_files) > 0
        ), f"No .pptx files found in {test_output_dir}. Files present: {list(test_output_dir.glob('*'))}"

        output_file = output_files[0]
        file_size_kb = output_file.stat().st_size / 1024
        assert file_size_kb > 50, f"File size {file_size_kb:.1f}KB too small for embedded image"

    def test_markdown_multiple_images(self, deckbuilder_with_env, test_output_dir):
        """Test markdown with multiple image slides."""
        deck = deckbuilder_with_env

        markdown = """---
layout: Picture with Caption
title: First Image
media:
  image_path: "src/placekitten/images/ACuteKitten-1.png"
  caption: "First kitten"
---

---
layout: Picture with Caption
title: Second Image
media:
  image_path: "src/placekitten/images/ACuteKitten-2.png"
  caption: "Second kitten"
---
"""

        result = deck.create_presentation_from_markdown(markdown, "test_multiple_images")

        assert "Successfully created presentation with 2 slides" in result

        # Check output file
        output_files = list(test_output_dir.glob("*.pptx"))
        assert (
            len(output_files) > 0
        ), f"No .pptx files found in {test_output_dir}. Files present: {list(test_output_dir.glob('*'))}"

        output_file = output_files[0]
        file_size_kb = output_file.stat().st_size / 1024
        assert (
            file_size_kb > 100
        ), f"File size {file_size_kb:.1f}KB too small for multiple embedded images"


class TestJSONImageIntegration:
    """Test image integration with JSON input."""

    def test_json_with_image_field(self, deckbuilder_with_env, test_output_dir):
        """Test JSON input with image_1 field."""
        deck = deckbuilder_with_env

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Picture with Caption",
                        "title": "JSON Image Test",
                        "image_1": "src/placekitten/images/ACuteKitten-1.png",
                        "text_caption_1": "JSON image caption",
                    }
                ]
            }
        }

        # Create presentation and add slides
        deck.create_presentation("default", "test_json_image")
        result = deck.add_slide_from_json(json_data)

        assert "Successfully added slide(s)" in result

        # Save presentation
        save_result = deck.write_presentation("test_json_image")
        assert "Successfully created presentation" in save_result

        # Check output file
        output_files = list(test_output_dir.glob("*.pptx"))
        assert (
            len(output_files) > 0
        ), f"No .pptx files found in {test_output_dir}. Files present: {list(test_output_dir.glob('*'))}"

    def test_json_with_fallback(self, deckbuilder_with_env, test_output_dir):
        """Test JSON input with missing image (fallback)."""
        deck = deckbuilder_with_env

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Picture with Caption",
                        "title": "JSON Fallback Test",
                        "image_1": "assets/missing_image.png",
                        "text_caption_1": "Fallback caption",
                    }
                ]
            }
        }

        deck.create_presentation("default", "test_json_fallback")
        result = deck.add_slide_from_json(json_data)

        assert "Successfully added slide(s)" in result

        save_result = deck.write_presentation("test_json_fallback")
        assert "Successfully created presentation" in save_result


class TestImageProcessingFeatures:
    """Test specific image processing features."""

    def test_image_caching(self, deckbuilder_with_env):
        """Test image caching functionality."""
        deck = deckbuilder_with_env

        # Get initial cache stats
        initial_stats = deck.image_handler.get_cache_stats()
        initial_count = initial_stats["file_count"]

        # Process an image
        test_image = "src/placekitten/images/ACuteKitten-1.png"
        if deck.image_handler.validate_image(test_image):
            processed = deck.image_handler.process_image(test_image, (400, 300))
            assert processed is not None

            # Check cache stats increased
            final_stats = deck.image_handler.get_cache_stats()
            assert final_stats["file_count"] >= initial_count

    def test_image_dimensions(self, deckbuilder_with_env):
        """Test image dimension retrieval."""
        deck = deckbuilder_with_env

        test_image = "src/placekitten/images/ACuteKitten-1.png"
        if Path(test_image).exists():
            dimensions = deck.image_handler.get_image_dimensions(test_image)
            assert isinstance(dimensions, tuple)
            assert len(dimensions) == 2
            assert all(isinstance(d, int) and d > 0 for d in dimensions)

    def test_professional_styling_config(self, deckbuilder_with_env):
        """Test professional styling configuration."""
        deck = deckbuilder_with_env

        fallback_info = deck.placekitten.get_fallback_info(
            (800, 600), context={"layout": "Picture with Caption", "slide_index": 1}
        )

        assert fallback_info["styling"]["base_filter"] == "grayscale"
        assert "smart_crop_strategy" in fallback_info["styling"]


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_environment_variable_configuration(self, deckbuilder_with_env):
        """Test that environment variables are properly configured in testing."""
        deck = deckbuilder_with_env

        # Verify environment variables are set correctly
        assert deck.template_path is not None
        assert deck.template_name == "default"
        assert deck.output_folder is not None
        # Check that template_path is a valid directory path (context-aware behavior)
        assert Path(deck.template_path).exists()

    def test_invalid_layout(self, deckbuilder_with_env):
        """Test handling of invalid layout names."""
        deck = deckbuilder_with_env

        markdown = """---
layout: Non Existent Layout
title: Test Invalid Layout
media:
  image_path: "src/placekitten/images/ACuteKitten-1.png"
---
"""

        # Should not crash, should handle gracefully
        result = deck.create_presentation_from_markdown(markdown, "test_invalid_layout")
        assert "Successfully created presentation" in result

    def test_missing_image_with_no_fallback(self, deckbuilder_with_env, monkeypatch):
        """Test behavior when image is missing and fallback fails."""
        deck = deckbuilder_with_env

        # Mock PlaceKitten to be unavailable
        def mock_is_available():
            return False

        monkeypatch.setattr(deck.placekitten, "is_available", mock_is_available)

        markdown = """---
layout: Picture with Caption
title: Test No Fallback
media:
  image_path: "assets/definitely_missing.png"
---
"""

        # Should not crash, should handle gracefully
        result = deck.create_presentation_from_markdown(markdown, "test_no_fallback")
        assert "Successfully created presentation" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
