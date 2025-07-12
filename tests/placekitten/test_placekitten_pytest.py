"""
Pytest test suite for PlaceKitten library.
Tests computer vision pipeline, smart cropping, and filter functionality.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

import pytest  # noqa: E402
from placekitten import PlaceKitten  # noqa: E402


@pytest.fixture
def test_output_dir():
    """Create and return test output directory."""
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def placekitten():
    """Initialize PlaceKitten instance."""
    return PlaceKitten("demo")


class TestPlaceKittenBasic:
    """Test basic PlaceKitten functionality."""

    def test_import_successful(self):
        """Test that PlaceKitten can be imported successfully."""
        from placekitten import PlaceKitten

        assert PlaceKitten is not None

    def test_initialization(self, placekitten):
        """Test PlaceKitten initialization."""
        assert placekitten is not None
        assert hasattr(placekitten, "generate")
        assert hasattr(placekitten, "list_available_images")

    def test_list_available_images(self, placekitten):
        """Test listing available images."""
        images = placekitten.list_available_images()
        assert isinstance(images, list)
        assert len(images) > 0

        # Check that we have expected kitten images
        image_names = [str(img) for img in images]
        assert any("ACuteKitten" in name for name in image_names)

    def test_generate_basic(self, placekitten, test_output_dir):
        """Test basic image generation."""
        processor = placekitten.generate(width=400, height=300, image_id=1)
        assert processor is not None

        # Save and verify output
        output_file = processor.save(str(test_output_dir / "test_basic_generate.jpg"))
        assert output_file.endswith("test_basic_generate.jpg")
        assert Path(output_file).exists()


class TestPlaceKittenSmartCrop:
    """Test smart cropping functionality."""

    def test_smart_crop_basic(self, placekitten, test_output_dir):
        """Test basic smart cropping without step visualization."""
        processor = placekitten.generate(width=800, height=600, image_id=1)

        smart_processor = processor.smart_crop(width=400, height=300)
        assert smart_processor is not None

        output_file = smart_processor.save(str(test_output_dir / "test_smart_crop_basic.jpg"))
        assert Path(output_file).exists()

    def test_smart_crop_with_steps(self, placekitten, test_output_dir):
        """Test smart cropping with step visualization."""
        processor = placekitten.generate(width=800, height=450, image_id=1)

        smart_processor = processor.smart_crop(
            width=800,
            height=450,
            save_steps=True,
            output_prefix="pytest_demo",
            output_folder=str(test_output_dir),
        )

        # Save final result
        output_file = smart_processor.save(str(test_output_dir / "pytest_smart_crop_final.jpg"))
        assert Path(output_file).exists()

        # Verify step files were created
        step_files = [f for f in test_output_dir.iterdir() if f.name.startswith("pytest_demo_")]
        assert len(step_files) == 9, f"Expected 9 step files, got {len(step_files)}"

    def test_smart_crop_different_aspects(self, placekitten, test_output_dir):
        """Test smart cropping with different aspect ratios."""
        processor = placekitten.generate(width=800, height=600, image_id=2)

        # Test square crop
        square_processor = processor.smart_crop(width=300, height=300)
        square_file = square_processor.save(str(test_output_dir / "test_smart_crop_square.jpg"))
        assert Path(square_file).exists()

        # Test wide crop
        wide_processor = processor.smart_crop(width=600, height=200)
        wide_file = wide_processor.save(str(test_output_dir / "test_smart_crop_wide.jpg"))
        assert Path(wide_file).exists()


class TestPlaceKittenFilters:
    """Test filter pipeline functionality."""

    @pytest.mark.parametrize("filter_name", ["grayscale", "sepia", "blur"])
    def test_individual_filters(self, placekitten, test_output_dir, filter_name):
        """Test individual filter types."""
        processor = placekitten.generate(width=400, height=300, filter_type=filter_name, image_id=1)

        output_file = processor.save(str(test_output_dir / f"pytest_filter_{filter_name}.jpg"))
        assert Path(output_file).exists()

    def test_chained_filters(self, placekitten, test_output_dir):
        """Test chaining multiple filters."""
        processor = placekitten.generate(width=400, height=300, image_id=1)

        # Chain filters
        filtered_processor = processor.apply_filter("grayscale").apply_filter("blur")

        output_file = filtered_processor.save(str(test_output_dir / "pytest_chained_filters.jpg"))
        assert Path(output_file).exists()

    def test_filter_with_smart_crop(self, placekitten, test_output_dir):
        """Test combining filters with smart cropping."""
        processor = placekitten.generate(width=800, height=600, image_id=1)

        # Apply smart crop then filter
        result = processor.smart_crop(width=400, height=400).apply_filter("grayscale")

        output_file = result.save(str(test_output_dir / "pytest_filter_smart_crop.jpg"))
        assert Path(output_file).exists()


class TestPlaceKittenIntegration:
    """Test PlaceKitten integration scenarios."""

    def test_professional_styling_config(self, placekitten, test_output_dir):
        """Test professional styling configuration for business presentations."""
        processor = placekitten.generate(width=800, height=600, image_id=1)

        # Apply professional styling (grayscale + smart crop)
        professional = processor.smart_crop(width=600, height=400).apply_filter("grayscale")

        output_file = professional.save(str(test_output_dir / "pytest_professional_styling.jpg"))
        assert Path(output_file).exists()

    def test_multiple_image_ids(self, placekitten, test_output_dir):
        """Test using different image IDs."""
        available_images = placekitten.list_available_images()

        # Test first few images
        for i in range(1, min(4, len(available_images) + 1)):
            processor = placekitten.generate(width=400, height=300, image_id=i)
            output_file = processor.save(str(test_output_dir / f"pytest_image_id_{i}.jpg"))
            assert Path(output_file).exists()

    def test_error_handling_invalid_image_id(self, placekitten, test_output_dir):
        """Test error handling for invalid image ID."""
        available_images = placekitten.list_available_images()
        invalid_id = len(available_images) + 10

        # PlaceKitten may handle invalid IDs gracefully by wrapping around
        # So let's just test it doesn't crash
        try:
            processor = placekitten.generate(width=400, height=300, image_id=invalid_id)
            # If it succeeds, verify we get a valid processor
            assert processor is not None
            output_file = processor.save(str(test_output_dir / "test_invalid_id_handled.jpg"))
            assert Path(output_file).exists()
        except (IndexError, ValueError):
            # If it raises an exception, that's also acceptable behavior
            pass

    def test_method_chaining(self, placekitten, test_output_dir):
        """Test method chaining functionality."""
        result = placekitten.generate(width=800, height=600, image_id=1).smart_crop(width=400, height=400).apply_filter("grayscale").save(str(test_output_dir / "pytest_method_chaining.jpg"))

        assert Path(result).exists()


@pytest.mark.cleanup
class TestCleanup:
    """Test cleanup functionality."""

    def test_no_root_directory_pollution(self):
        """Ensure no test files are created in root directory."""
        project_root = Path(__file__).parent.parent.parent
        root_test_files = [f for f in project_root.iterdir() if f.is_file() and f.name.startswith("test_") and f.suffix == ".jpg"]

        assert len(root_test_files) == 0, f"Found test files in root directory: {root_test_files}"

    def test_output_directory_structure(self):
        """Verify test output is properly organized."""
        test_output_dir = Path(__file__).parent / "test_output"

        if test_output_dir.exists():
            # Should only contain image files (ignore system files like .gitignore)
            for file in test_output_dir.iterdir():
                if file.is_file() and not file.name.startswith("."):
                    assert file.suffix in [".jpg", ".jpeg", ".png"], f"Unexpected file type: {file}"
