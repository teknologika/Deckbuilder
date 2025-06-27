"""
PlaceKitten Core - Main PlaceKitten class for placeholder image generation.

This module provides the main PlaceKitten class that handles image generation
from existing kitten images with dimension management and basic functionality.
"""

import os
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
        # Get project root (3 levels up from this file)
        project_root = Path(__file__).parent.parent.parent

        if self.source_folder == "demo":
            # Use the assets/images folder directly for demo mode
            self.images_path = project_root / "assets" / "images"
        else:
            # Use custom source folder
            self.images_path = project_root / "assets" / "images" / self.source_folder

        if not self.images_path.exists():
            raise RuntimeError(f"Image source folder not found: {self.images_path}")

    def _get_available_images(self) -> List[Path]:
        """Get list of available image files."""
        if self._image_cache is None:
            # Cache the image list for performance
            image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
            self._image_cache = [
                img
                for img in self.images_path.iterdir()
                if img.is_file() and img.suffix.lower() in image_extensions
            ]

        if not self._image_cache:
            raise RuntimeError(f"No images found in {self.images_path}")

        return self._image_cache

    def _calculate_height(self, width: int) -> int:
        """Calculate height for 16:9 aspect ratio."""
        return int(width * 9 / 16)

    def generate(
        self,
        width: int,
        height: Optional[int] = None,
        filter_type: Optional[str] = None,
        image_id: Optional[int] = None,
        random_selection: bool = False,
    ) -> ImageProcessor:
        """
        Generate placeholder image with specified dimensions.

        Args:
            width: Image width in pixels
            height: Image height in pixels (auto-calculated for 16:9 if None)
            filter_type: Filter to apply (e.g., "sepia", "grayscale")
            image_id: Specific image ID to use (0-based index)
            random_selection: Use random image selection

        Returns:
            ImageProcessor instance for further manipulation
        """
        # Calculate height if not provided (16:9 aspect ratio)
        if height is None:
            height = self._calculate_height(width)

        # Get available images
        available_images = self._get_available_images()

        # Select image
        if image_id is not None:
            if 0 <= image_id < len(available_images):
                selected_image = available_images[image_id]
            else:
                raise ValueError(f"Image ID {image_id} out of range (0-{len(available_images)-1})")
        elif random_selection:
            selected_image = random.choice(available_images)
        else:
            # Default to first image
            selected_image = available_images[0]

        # Create ImageProcessor with the selected image
        processor = ImageProcessor(str(selected_image))

        # Resize to target dimensions
        processor = processor.resize(width, height)

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
            filename = f"placekitten_{width}x{height}_{i+1}.jpg"

            # Save image
            output_file = output_path / filename
            result = processor.save(str(output_file))
            results.append(result)

        return results
