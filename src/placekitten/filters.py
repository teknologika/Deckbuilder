"""
Filters - Image filter pipeline and effect implementations.

This module provides a comprehensive set of image filters and effects
for the PlaceKitten library with easy extensibility.
"""

from typing import Callable, Dict

import PIL.ImageOps
from PIL import Image, ImageEnhance, ImageFilter


class FilterRegistry:
    """Registry for image filters with extensible architecture."""

    def __init__(self):
        """Initialize filter registry with built-in filters."""
        self._filters: Dict[str, Callable] = {}
        self._register_builtin_filters()

    def _register_builtin_filters(self) -> None:
        """Register all built-in filters."""
        # Basic filters
        self.register("grayscale", self._grayscale)
        self.register("greyscale", self._grayscale)  # Alternative spelling
        self.register("blur", self._blur)
        self.register("sepia", self._sepia)
        self.register("invert", self._invert)

        # Enhancement filters
        self.register("brightness", self._brightness)
        self.register("contrast", self._contrast)
        self.register("saturation", self._saturation)
        self.register("sharpness", self._sharpness)

        # Effect filters
        self.register("pixelate", self._pixelate)
        self.register("edge_detection", self._edge_detection)
        self.register("emboss", self._emboss)
        self.register("smooth", self._smooth)

    def register(self, name: str, filter_func: Callable) -> None:
        """
        Register a new filter.

        Args:
            name: Filter name
            filter_func: Filter function that takes (image, **kwargs)
        """
        self._filters[name] = filter_func

    def apply(self, image: Image.Image, filter_name: str, **kwargs) -> Image.Image:
        """
        Apply filter to image.

        Args:
            image: PIL Image to process
            filter_name: Name of filter to apply
            **kwargs: Filter-specific parameters

        Returns:
            Processed PIL Image
        """
        if filter_name not in self._filters:
            available = ", ".join(self._filters.keys())
            raise ValueError(f"Unknown filter '{filter_name}'. Available: {available}")

        return self._filters[filter_name](image, **kwargs)

    def list_filters(self) -> list:
        """Get list of available filter names."""
        return list(self._filters.keys())

    # Built-in filter implementations

    def _grayscale(self, image: Image.Image, **kwargs) -> Image.Image:
        """Convert image to grayscale."""
        return image.convert("L").convert("RGB")

    def _blur(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply Gaussian blur."""
        strength = kwargs.get("strength", 5)
        return image.filter(ImageFilter.GaussianBlur(radius=strength))

    def _sepia(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply sepia tone effect."""
        # Sepia transformation matrix
        sepia_filter = (0.393, 0.769, 0.189, 0, 0.349, 0.686, 0.168, 0, 0.272, 0.534, 0.131, 0)
        return image.convert("RGB", sepia_filter)

    def _invert(self, image: Image.Image, **kwargs) -> Image.Image:
        """Invert image colors."""
        return PIL.ImageOps.invert(image)

    def _brightness(self, image: Image.Image, **kwargs) -> Image.Image:
        """Adjust image brightness."""
        value = kwargs.get("value", 100)  # 100 = no change
        factor = value / 100.0
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    def _contrast(self, image: Image.Image, **kwargs) -> Image.Image:
        """Adjust image contrast."""
        value = kwargs.get("value", 100)  # 100 = no change
        factor = value / 100.0
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    def _saturation(self, image: Image.Image, **kwargs) -> Image.Image:
        """Adjust image saturation."""
        value = kwargs.get("value", 100)  # 100 = no change
        factor = value / 100.0
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)

    def _sharpness(self, image: Image.Image, **kwargs) -> Image.Image:
        """Adjust image sharpness."""
        value = kwargs.get("value", 100)  # 100 = no change
        factor = value / 100.0
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    def _pixelate(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply pixelation effect."""
        strength = kwargs.get("strength", 5)
        width, height = image.size

        # Resize down and back up for pixelation
        small_size = (max(1, width // strength), max(1, height // strength))
        pixelated = image.resize(small_size, Image.Resampling.NEAREST)
        return pixelated.resize((width, height), Image.Resampling.NEAREST)

    def _edge_detection(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply edge detection filter."""
        return image.filter(ImageFilter.FIND_EDGES)

    def _emboss(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply emboss effect."""
        return image.filter(ImageFilter.EMBOSS)

    def _smooth(self, image: Image.Image, **kwargs) -> Image.Image:
        """Apply smoothing filter."""
        strength = kwargs.get("strength", 1)
        for _ in range(strength):
            image = image.filter(ImageFilter.SMOOTH)
        return image


# Global filter registry instance
filter_registry = FilterRegistry()


# Convenience functions for direct filter access
def apply_filter(image: Image.Image, filter_name: str, **kwargs) -> Image.Image:
    """
    Apply filter to image using global registry.

    Args:
        image: PIL Image to process
        filter_name: Name of filter to apply
        **kwargs: Filter-specific parameters

    Returns:
        Processed PIL Image
    """
    return filter_registry.apply(image, filter_name, **kwargs)


def list_available_filters() -> list:
    """Get list of all available filters."""
    return filter_registry.list_filters()


def register_custom_filter(name: str, filter_func: Callable) -> None:
    """
    Register a custom filter.

    Args:
        name: Filter name
        filter_func: Filter function that takes (image, **kwargs)
    """
    filter_registry.register(name, filter_func)
