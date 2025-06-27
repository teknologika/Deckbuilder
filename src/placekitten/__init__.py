"""
PlaceKitten - Intelligent Image Processing Library

A comprehensive Python library for intelligent image cropping, filtering,
and placeholder generation with computer vision capabilities.

Quick Start:
    from placekitten import PlaceKitten, ImageProcessor

    # Generate placeholder image
    pk = PlaceKitten()
    image = pk.generate(width=800, height=450)
    result = image.apply_filter("sepia").save("output.jpg")

    # Process existing image
    processor = ImageProcessor("input.jpg")
    result = processor.smart_crop(1920, 1080).save("cropped.jpg")
"""

__version__ = "0.1.0"
__author__ = "Deckbuilder Team"
__license__ = "MIT"

# Import main classes for public API
from .core import PlaceKitten
from .filters import apply_filter, list_available_filters, register_custom_filter
from .processor import ImageProcessor
from .smart_crop import SmartCropEngine

# Public API exports
__all__ = [
    # Main classes
    "PlaceKitten",
    "ImageProcessor",
    "SmartCropEngine",
    # Filter utilities
    "apply_filter",
    "list_available_filters",
    "register_custom_filter",
    # Version info
    "__version__",
    "__author__",
    "__license__",
]
