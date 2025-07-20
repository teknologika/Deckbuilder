"""
ImageHandler - Core image file validation, processing, and management.

This module provides the ImageHandler class for validating image files,
processing them for PowerPoint placeholders, and managing cached fallback images.
"""

import hashlib
import os
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


class ImageHandler:
    """
    Core image file validation, processing, and management.

    Handles image file validation, format conversion, resizing,
    and caching for optimal performance in presentation generation.
    """

    def __init__(self, cache_dir: str = "temp/image_cache"):
        """
        Initialize ImageHandler with cache directory.

        Args:
            cache_dir: Directory for caching processed images
        """
        self.cache_dir = Path(cache_dir)
        self._cache_initialized = False

        # Supported image formats for PowerPoint
        self.supported_formats = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}

        # Quality settings for output
        self.quality_settings = {"high": 95, "medium": 85, "low": 70}

    def _ensure_cache_dir(self):
        """
        Ensure cache directory exists. Called lazily when cache is first needed.
        """
        if not self._cache_initialized:
            try:
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                # Fallback to a temporary directory if cache_dir is not writable
                import tempfile

                self.cache_dir = Path(tempfile.gettempdir()) / "deckbuilder_image_cache"
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._cache_initialized = True

    def validate_image(self, image_path: str) -> bool:
        """
        Validate image file existence, format, and accessibility.

        Args:
            image_path: Path to image file to validate

        Returns:
            bool: True if image is valid and accessible, False otherwise
        """
        if not image_path:
            return False

        try:
            path = Path(image_path)

            # Check file existence
            if not path.exists():
                return False

            # Check if it's a file (not directory)
            if not path.is_file():
                return False

            # Check file extension
            if path.suffix.lower() not in self.supported_formats:
                return False

            # Try to open and validate the image
            with Image.open(path) as img:
                # Verify image can be loaded and read
                img.verify()

            return True

        except Exception:
            # Any exception during validation means invalid image
            return False

    def get_image_dimensions(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        Get image dimensions without loading the full image.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (width, height) or None if image invalid
        """
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception:
            return None

    def process_image(self, image_path: str, target_dimensions: Tuple[int, int], quality: str = "high") -> Optional[str]:
        """
        Process and resize image to target dimensions for PowerPoint placeholder.

        Args:
            image_path: Path to source image file
            target_dimensions: Target (width, height) for placeholder
            quality: Quality level ('high', 'medium', 'low')

        Returns:
            str: Path to processed image file, or None if processing failed
        """
        if not self.validate_image(image_path):
            return None

        try:
            target_width, target_height = target_dimensions

            # Generate cache key based on input and parameters
            cache_key = self._generate_cache_key(image_path, target_dimensions, quality)
            cached_path = self._get_cached_image(cache_key)

            if cached_path:
                return cached_path

            # Process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for JPEG output)
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Calculate dimensions preserving aspect ratio
                processed_img = self._resize_with_aspect_ratio(img, target_width, target_height)

                # Save processed image
                output_path = self._save_processed_image(processed_img, cache_key, quality)

                return str(output_path)

        except Exception as e:
            print(f"Warning: Image processing failed for {image_path}: {e}")
            return None

    def _resize_with_aspect_ratio(self, img: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """
        Resize image to fit target dimensions while preserving aspect ratio.

        Args:
            img: PIL Image object
            target_width: Target width
            target_height: Target height

        Returns:
            PIL Image resized to fit within target dimensions
        """
        # Get original dimensions
        orig_width, orig_height = img.size

        # Calculate scaling ratios
        width_ratio = target_width / orig_width
        height_ratio = target_height / orig_height

        # Use the smaller ratio to ensure image fits within bounds
        scale_ratio = min(width_ratio, height_ratio)

        # Calculate new dimensions
        new_width = int(orig_width * scale_ratio)
        new_height = int(orig_height * scale_ratio)

        # Resize using high-quality resampling
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _generate_cache_key(self, image_path: str, dimensions: Tuple[int, int], quality: str) -> str:
        """
        Generate unique cache key for processed image.

        Args:
            image_path: Source image path
            dimensions: Target dimensions
            quality: Quality setting

        Returns:
            str: Unique cache key
        """
        # Include file modification time to detect changes
        try:
            mtime = os.path.getmtime(image_path)
        except OSError:
            mtime = 0

        # Create hash from path, dimensions, quality, and modification time
        key_data = f"{image_path}_{dimensions[0]}x{dimensions[1]}_{quality}_{mtime}"
        return hashlib.md5(key_data.encode(), usedforsecurity=False).hexdigest()  # nosec

    def _get_cached_image(self, cache_key: str) -> Optional[str]:
        """
        Retrieve cached processed image if available.

        Args:
            cache_key: Cache key for the image

        Returns:
            str: Path to cached image, or None if not cached
        """
        self._ensure_cache_dir()
        cached_path = self.cache_dir / f"{cache_key}.jpg"

        if cached_path.exists():
            return str(cached_path)

        return None

    def _save_processed_image(self, img: Image.Image, cache_key: str, quality: str) -> Path:
        """
        Save processed image to cache with specified quality.

        Args:
            img: PIL Image to save
            cache_key: Cache key for filename
            quality: Quality level for JPEG compression

        Returns:
            Path: Path to saved image file
        """
        self._ensure_cache_dir()
        output_path = self.cache_dir / f"{cache_key}.jpg"

        # Get quality setting
        jpeg_quality = self.quality_settings.get(quality, 95)

        # Save as JPEG with specified quality
        img.save(output_path, "JPEG", quality=jpeg_quality, optimize=True)

        return output_path

    def cleanup_cache(self, max_size_mb: int = 100):
        """
        Clean up cache directory if it exceeds maximum size.

        Args:
            max_size_mb: Maximum cache size in megabytes
        """
        if not self._cache_initialized:
            return  # No cache to clean up
        try:
            # Calculate total cache size
            total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.jpg") if f.is_file())

            max_size_bytes = max_size_mb * 1024 * 1024

            if total_size > max_size_bytes:
                # Get files sorted by access time (LRU)
                cache_files = [(f, f.stat().st_atime) for f in self.cache_dir.glob("*.jpg") if f.is_file()]
                cache_files.sort(key=lambda x: x[1])  # Sort by access time

                # Remove oldest files until under limit
                current_size = total_size
                for file_path, _ in cache_files:
                    if current_size <= max_size_bytes:
                        break

                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    current_size -= file_size

        except Exception as e:
            print(f"Warning: Cache cleanup failed: {e}")

    def get_cache_stats(self) -> dict:
        """
        Get statistics about the image cache.

        Returns:
            dict: Cache statistics including file count and total size
        """
        if not self._cache_initialized:
            return {"file_count": 0, "total_size_mb": 0.0, "cache_dir": str(self.cache_dir)}
        try:
            cache_files = list(self.cache_dir.glob("*.jpg"))
            total_size = sum(f.stat().st_size for f in cache_files if f.is_file())

            return {
                "file_count": len(cache_files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_dir": str(self.cache_dir),
            }
        except Exception:
            return {"file_count": 0, "total_size_mb": 0.0, "cache_dir": str(self.cache_dir)}
