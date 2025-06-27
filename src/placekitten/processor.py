"""
ImageProcessor - Core image manipulation and processing functionality.

This module provides the ImageProcessor class for image loading, resizing,
filtering, and saving with method chaining support.
"""

import os
import numpy as np
from pathlib import Path
from typing import Optional, Union
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime
from .filters import apply_filter


class ImageProcessor:
    """
    Image processing class with method chaining support.
    
    Handles image loading, manipulation, filtering, and saving operations
    with a fluent interface for complex processing pipelines.
    """
    
    def __init__(
        self, 
        image_path: Optional[str] = None, 
        image_array: Optional[np.ndarray] = None
    ):
        """
        Initialize ImageProcessor with image file or numpy array.
        
        Args:
            image_path: Path to image file
            image_array: NumPy array containing image data
        """
        if image_path is not None:
            self.image = Image.open(image_path)
            self.source_path = image_path
        elif image_array is not None:
            self.image = Image.fromarray(image_array)
            self.source_path = None
        else:
            raise ValueError("Must provide either image_path or image_array")
        
        # Ensure RGB mode for consistent processing
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
    
    def resize(self, width: int, height: Optional[int] = None) -> "ImageProcessor":
        """
        Resize image maintaining aspect ratio or to specific dimensions.
        
        Args:
            width: Target width in pixels
            height: Target height in pixels (maintains aspect ratio if None)
            
        Returns:
            New ImageProcessor instance with resized image
        """
        if height is None:
            # Maintain aspect ratio
            aspect_ratio = self.image.height / self.image.width
            height = int(width * aspect_ratio)
        
        # Use high-quality resampling
        resized_image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Create new processor instance
        new_processor = ImageProcessor.__new__(ImageProcessor)
        new_processor.image = resized_image
        new_processor.source_path = self.source_path
        
        return new_processor
    
    def apply_filter(self, filter_name: str, **kwargs) -> "ImageProcessor":
        """
        Apply image filter using the filter registry.
        
        Args:
            filter_name: Name of filter to apply
            **kwargs: Filter-specific parameters
            
        Returns:
            New ImageProcessor instance with filter applied
        """
        # Use the centralized filter registry
        filtered_image = apply_filter(self.image.copy(), filter_name, **kwargs)
        
        # Create new processor instance
        new_processor = ImageProcessor.__new__(ImageProcessor)
        new_processor.image = filtered_image
        new_processor.source_path = self.source_path
        
        return new_processor
    
    def smart_crop(
        self, 
        width: int, 
        height: Optional[int] = None, 
        save_steps: bool = False
    ) -> "ImageProcessor":
        """
        Intelligent cropping with computer vision (placeholder for Phase 2).
        
        Args:
            width: Target width
            height: Target height (16:9 if None)
            save_steps: Save intermediate processing steps
            
        Returns:
            New ImageProcessor instance with cropped image
        """
        if height is None:
            height = int(width * 9 / 16)
        
        # Phase 1: Simple center crop (will be enhanced in Phase 2)
        # Calculate crop box for center crop
        img_width, img_height = self.image.size
        
        # Calculate scaling to fit target aspect ratio
        target_ratio = width / height
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            # Image is wider than target, crop width
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            crop_box = (left, 0, left + new_width, img_height)
        else:
            # Image is taller than target, crop height
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            crop_box = (0, top, img_width, top + new_height)
        
        # Crop and resize
        cropped_image = self.image.crop(crop_box)
        final_image = cropped_image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Create new processor instance
        new_processor = ImageProcessor.__new__(ImageProcessor)
        new_processor.image = final_image
        new_processor.source_path = self.source_path
        
        return new_processor
    
    def save(self, output_path: str, quality: str = "high") -> str:
        """
        Save processed image.
        
        Args:
            output_path: Output file path
            quality: Quality level ("high", "medium", "low")
            
        Returns:
            Path to saved file
        """
        # Determine quality settings
        if quality == "high":
            jpeg_quality = 95
        elif quality == "medium":
            jpeg_quality = 85
        else:  # low
            jpeg_quality = 70
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine format from extension
        file_extension = output_path.suffix.lower()
        
        if file_extension in ['.jpg', '.jpeg']:
            self.image.save(output_path, 'JPEG', quality=jpeg_quality, optimize=True)
        elif file_extension == '.png':
            self.image.save(output_path, 'PNG', optimize=True)
        elif file_extension == '.webp':
            self.image.save(output_path, 'WEBP', quality=jpeg_quality, optimize=True)
        else:
            # Default to JPEG
            output_path = output_path.with_suffix('.jpg')
            self.image.save(output_path, 'JPEG', quality=jpeg_quality, optimize=True)
        
        return str(output_path)
    
    def get_array(self) -> np.ndarray:
        """
        Get image as numpy array.
        
        Returns:
            Image as numpy array
        """
        return np.array(self.image)
    
    def get_size(self) -> tuple:
        """
        Get image dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return self.image.size
    
    def get_info(self) -> dict:
        """
        Get image information.
        
        Returns:
            Dictionary with image information
        """
        width, height = self.image.size
        return {
            'width': width,
            'height': height,
            'mode': self.image.mode,
            'format': self.image.format,
            'source_path': self.source_path
        }