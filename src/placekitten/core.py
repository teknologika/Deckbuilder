"""
PlaceKitten Core - Main PlaceKitten class for placeholder image generation.

This module provides the main PlaceKitten class that handles image generation
from existing kitten images with dimension management and basic functionality.
"""

import random
from pathlib import Path
from typing import List, Optional

from .processor import ImageProcessor


class PlaceKitten:
    """
    Main PlaceKitten class for generating placeholder images from kitten photos.

    Provides basic image generation with dimension handling, supporting both
    auto-height 16:9 aspect ratio and custom dimensions.
    """

    def __init__(self, source_folder: str = "demo"):
        """
        Initialize PlaceKitten with source image folder.

        Args:
            source_folder: Folder name containing source images (relative to assets/images/)
        """
        self.source_folder = source_folder
        self._image_cache = None
        self._setup_image_paths()

    def _setup_image_paths(self) -> None:
        """Setup paths to kitten images."""
        # Get placekitten module directory (this file's parent)
        placekitten_module = Path(__file__).parent

        if self.source_folder == "demo":
            # Use the images folder within placekitten module for demo mode
            self.images_path = placekitten_module / "images"
        else:
            # Use custom source folder within placekitten module
            self.images_path = placekitten_module / "images" / self.source_folder

        if not self.images_path.exists():
            raise RuntimeError(f"Image source folder not found: {self.images_path}")

    def _get_available_images(self) -> List[Path]:
        """Get list of available image files."""
        if self._image_cache is None:
            # Cache the image list for performance
            image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
            self._image_cache = sorted([img for img in self.images_path.iterdir() if img.is_file() and img.suffix.lower() in image_extensions])

        if not self._image_cache:
            raise RuntimeError(f"No images found in {self.images_path}")

        return self._image_cache

    def _calculate_height(self, width: int) -> int:
        """Calculate height for 16:9 aspect ratio."""
        return int(width * 9 / 16)

    def generate(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        filter_type: Optional[str] = None,
        image_id: Optional[int] = None,
        random_selection: bool = False,
    ) -> ImageProcessor:
        """
        Generate placeholder image with specified dimensions.

        Args:
            width: Image width in pixels (optional - scales from height if only height given)
            height: Image height in pixels (optional - scales from width if only width given)
            filter_type: Filter to apply (e.g., "sepia", "grayscale")
            image_id: Specific image ID to use (1-based index, uses random if invalid/None)
            random_selection: Force random image selection (overrides image_id)

        Returns:
            ImageProcessor instance for further manipulation

        Note:
            When both width and height are specified, uses smart cropping for exact dimensions.
            When only one dimension is specified, preserves aspect ratio using scaling.
        """

        # Get available images
        available_images = self._get_available_images()

        # Select image (using 1-based indexing, random for invalid/None)
        if random_selection:
            selected_image = random.choice(available_images)  # nosec
        elif image_id is not None and 1 <= image_id <= len(available_images):
            selected_image = available_images[image_id - 1]  # Convert to 0-based index
        else:
            # Use random for None or out-of-range image_id
            selected_image = random.choice(available_images)  # nosec

        # Create ImageProcessor with the selected image
        processor = ImageProcessor(str(selected_image))

        # Handle dimensions - crop for exact dimensions or preserve aspect ratio
        if width is None and height is None:
            # Return full size image - no resizing
            pass
        elif width is not None and height is not None:
            # Both specified - use smart crop to exact dimensions (crop-first approach)
            processor = processor.smart_crop(width, height)
        elif width is not None:
            # Only width specified - calculate height preserving aspect ratio
            original_width, original_height = processor.get_size()
            aspect_ratio = original_height / original_width
            calculated_height = int(width * aspect_ratio)
            processor = processor.resize(width, calculated_height)
        elif height is not None:
            # Only height specified - calculate width preserving aspect ratio
            original_width, original_height = processor.get_size()
            aspect_ratio = original_width / original_height
            calculated_width = int(height * aspect_ratio)
            processor = processor.resize(calculated_width, height)

        # Apply filter if specified
        if filter_type:
            processor = processor.apply_filter(filter_type)

        return processor

    def list_available_images(self) -> List[str]:
        """
        Get list of available image filenames.

        Returns:
            List of image filenames
        """
        images = self._get_available_images()
        return [img.name for img in images]

    def get_image_count(self) -> int:
        """
        Get count of available images.

        Returns:
            Number of available images
        """
        return len(self._get_available_images())

    def batch_process(self, configs: List[dict], output_folder: str = "output") -> List[str]:
        """
        Process multiple images in batch.

        Args:
            configs: List of configuration dictionaries with width, height, etc.
            output_folder: Output folder for generated images

        Returns:
            List of generated file paths
        """
        results = []

        # Ensure output folder exists
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        for i, config in enumerate(configs):
            # Generate image with config
            processor = self.generate(**config)

            # Generate filename
            width = config.get("width", 500)
            height = config.get("height", self._calculate_height(width))
            filename = f"placekitten_{width}x{height}_{i + 1}.jpg"

            # Save image
            output_file = output_path / filename
            result = processor.save(str(output_file))
            results.append(result)

        return results

    def is_available(self) -> bool:
        """
        Check if PlaceKitten service is available.

        Returns:
            True if available images exist
        """
        return len(self._get_available_images()) > 0

    def get_fallback_info(self, dimensions: tuple, context: dict = None) -> dict:
        """
        Get fallback image information for given dimensions.

        Args:
            dimensions: Tuple of (width, height)
            context: Optional context dictionary (layout, slide_index, etc.)

        Returns:
            Dictionary with fallback image information
        """
        width, height = dimensions
        available_images = self._get_available_images()

        return {
            "available": len(available_images) > 0,
            "image_id": 1 if available_images else None,
            "dimensions": {"width": width, "height": height},
            "styling": {
                "base_filter": "grayscale",
                "contrast": 95,
                "brightness": 105,
                "smart_crop_strategy": "rule_of_thirds",
                "face_detection": True,
                "professional_mode": True,
            },
        }
