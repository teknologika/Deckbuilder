"""
PlaceKittenIntegration - Bridge between PlaceKitten library and Deckbuilder engine.

This module provides the PlaceKittenIntegration class that generates professional
fallback images using PlaceKitten when user-provided images are missing or invalid.
"""

from typing import Dict, Optional, Tuple

from .image_handler import ImageHandler

try:
    # Import PlaceKitten using DRY utility
    from ..utils.path import get_placekitten

    PlaceKitten = get_placekitten()

    PLACEKITTEN_AVAILABLE = True
except ImportError:
    PLACEKITTEN_AVAILABLE = False
    print("Warning: PlaceKitten library not available. Image fallbacks will be disabled.")


class PlaceKittenIntegration:
    """
    Bridge between PlaceKitten library and Deckbuilder engine.

    Generates professional fallback images with business-appropriate styling
    when user-provided images are missing or invalid.
    """

    def __init__(self, image_handler: ImageHandler):
        """
        Initialize PlaceKittenIntegration with image handler.

        Args:
            image_handler: ImageHandler instance for caching and processing
        """
        self.image_handler = image_handler

        # Initialize PlaceKitten if available
        if PLACEKITTEN_AVAILABLE:
            self.pk = PlaceKitten()
        else:
            self.pk = None

        # Professional styling configuration
        self.professional_config = self._get_professional_styling()

    def is_available(self) -> bool:
        """
        Check if PlaceKitten integration is available.

        Returns:
            bool: True if PlaceKitten library is available and ready
        """
        return PLACEKITTEN_AVAILABLE and self.pk is not None

    def generate_fallback(self, dimensions: Tuple[int, int], context: Optional[Dict] = None) -> Optional[str]:
        """
        Generate professional fallback image with business-appropriate styling.

        Args:
            dimensions: Target (width, height) for the image
            context: Optional context information for consistent generation

        Returns:
            str: Path to generated fallback image, or None if generation failed
        """
        if not self.is_available():
            return None

        try:
            width, height = dimensions

            # Generate cache key for fallback image
            cache_key = self._generate_fallback_cache_key(dimensions, context)
            cached_path = self.image_handler._get_cached_image(cache_key)

            if cached_path:
                return cached_path

            # Generate new fallback image
            return self._create_fallback_image(width, height, cache_key, context)

        except Exception as e:
            print(f"Warning: PlaceKitten fallback generation failed: {e}")
            return None

    def _create_fallback_image(self, width: int, height: int, cache_key: str, context: Optional[Dict] = None) -> Optional[str]:
        """
        Create new fallback image with professional styling.

        Args:
            width: Target width
            height: Target height
            cache_key: Cache key for storing result
            context: Optional context for generation

        Returns:
            str: Path to generated image, or None if failed
        """
        try:
            # Select consistent image based on context
            image_id = self._select_image_id(context)

            # Generate base image
            processor = self.pk.generate(image_id=image_id)

            # Apply professional styling pipeline
            styled_processor = self._apply_professional_styling(processor, width, height)

            # Save to cache with high quality
            output_path = self.image_handler.cache_dir / f"{cache_key}.jpg"
            final_path = styled_processor.save(str(output_path))

            return final_path

        except Exception as e:
            print(f"Warning: Failed to create fallback image: {e}")
            return None

    def _apply_professional_styling(self, processor, width: int, height: int):
        """
        Apply professional styling pipeline to PlaceKitten image.

        Args:
            processor: PlaceKitten ImageProcessor instance
            width: Target width
            height: Target height

        Returns:
            Styled ImageProcessor ready for saving
        """
        config = self.professional_config

        # Smart crop to exact dimensions
        styled = processor.smart_crop(width=width, height=height, strategy=config["smart_crop_strategy"])

        # Apply business-appropriate grayscale filter
        styled = styled.apply_filter(config["base_filter"])

        # Enhance contrast for professional appearance
        if config["contrast_adjustment"] != 100:
            styled = styled.apply_filter("contrast", value=config["contrast_adjustment"])

        # Subtle brightness adjustment if needed
        if config["brightness_adjustment"] != 100:
            styled = styled.apply_filter("brightness", value=config["brightness_adjustment"])

        return styled

    def _select_image_id(self, context: Optional[Dict] = None) -> int:
        """
        Select consistent image ID based on context.

        Args:
            context: Optional context with slide information

        Returns:
            int: Image ID (1-based) for consistent selection
        """
        if not context:
            return 1  # Default to first image

        # Use slide index for consistency within presentations
        if "slide_index" in context:
            slide_index = context["slide_index"]
            # Cycle through available images based on slide index
            available_images = self.pk.get_image_count()
            return (slide_index % available_images) + 1

        # Use layout type for consistency
        if "layout" in context:
            layout = context["layout"]
            # Simple hash-based selection for consistent results
            layout_hash = hash(layout) % self.pk.get_image_count()
            return layout_hash + 1

        return 1  # Default fallback

    def _generate_fallback_cache_key(self, dimensions: Tuple[int, int], context: Optional[Dict] = None) -> str:
        """
        Generate cache key for fallback image.

        Args:
            dimensions: Target dimensions
            context: Optional context information

        Returns:
            str: Cache key for consistent fallback generation
        """
        width, height = dimensions

        # Base key with dimensions and styling
        key_parts = [
            "placekitten_fallback",
            f"{width}x{height}",
            self.professional_config["base_filter"],
            f'contrast{self.professional_config["contrast_adjustment"]}',
            f'brightness{self.professional_config["brightness_adjustment"]}',
        ]

        # Add context-based components for consistency
        if context:
            if "slide_index" in context:
                key_parts.append(f'slide{context["slide_index"]}')
            elif "layout" in context:
                key_parts.append(f'layout{hash(context["layout"])}')

        return "_".join(str(part) for part in key_parts)

    def _get_professional_styling(self) -> Dict:
        """
        Get professional styling configuration for business presentations.

        Returns:
            dict: Configuration for professional image styling
        """
        return {
            "base_filter": "grayscale",  # Business-appropriate monochrome
            "contrast_adjustment": 95,  # Subtle contrast reduction
            "brightness_adjustment": 105,  # Slight brightness boost
            "smart_crop_strategy": "haar-face",  # Face-priority cropping
        }

    def get_fallback_info(self, dimensions: Tuple[int, int], context: Optional[Dict] = None) -> Dict:
        """
        Get information about fallback image that would be generated.

        Args:
            dimensions: Target dimensions
            context: Optional context information

        Returns:
            dict: Information about the fallback image
        """
        if not self.is_available():
            return {"available": False, "reason": "PlaceKitten library not available"}

        width, height = dimensions
        image_id = self._select_image_id(context)
        cache_key = self._generate_fallback_cache_key(dimensions, context)
        cached_path = self.image_handler._get_cached_image(cache_key)

        return {
            "available": True,
            "dimensions": dimensions,
            "image_id": image_id,
            "styling": self.professional_config,
            "cached": cached_path is not None,
            "cache_key": cache_key,
        }

    def cleanup_fallback_cache(self):
        """Clean up cached fallback images to free space."""
        try:
            # Remove all PlaceKitten fallback images from cache
            fallback_files = list(self.image_handler.cache_dir.glob("placekitten_fallback_*.jpg"))

            removed_count = 0
            for file_path in fallback_files:
                try:
                    file_path.unlink()
                    removed_count += 1
                except Exception:
                    continue  # nosec - Continue processing other files if one fails

            return {"removed_files": removed_count, "total_fallback_files": len(fallback_files)}

        except Exception as e:
            print(f"Warning: Fallback cache cleanup failed: {e}")
            return {"removed_files": 0, "total_fallback_files": 0}
