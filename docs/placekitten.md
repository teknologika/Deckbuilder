# PlaceKitten Library v1.2.0

The PlaceKitten library is an advanced image processing tool for generating professional placeholder images from kitten photos. Enhanced in v1.2.0 with **crop-first approach** for exact dimensions and business-appropriate styling.

## 🎉 What's New in v1.2.0

*   **🖼️ Crop-First Approach**: Smart cropping instead of scaling for exact dimensions
*   **🎯 Better Visual Results**: Proper composition instead of distorted stretching
*   **👁️ Enhanced Smart Cropping**: Improved face detection and rule-of-thirds composition
*   **🎨 Professional Styling**: Optimized filters for business presentations
*   **⚡ Performance Optimized**: Intelligent caching and fallback systems

## `PlaceKitten` Class

The `PlaceKitten` class is the main entry point for generating placeholder images. It provides methods for generating images with different dimensions, filters, and other effects.

### Methods

*   `generate(width, height, filter_type, image_id, random_selection)`: **ENHANCED** - Now uses smart cropping for exact dimensions when both width and height specified
*   `list_available_images()`: Lists the available kitten images.
*   `get_image_count()`: Gets the number of available kitten images.
*   `batch_process(configs, output_folder)`: Processes multiple images in batch with crop-first approach

## `ImageProcessor` Class

The `ImageProcessor` class is responsible for image loading, resizing, filtering, and saving. It uses the `Pillow` and `NumPy` libraries for image manipulation and provides a fluent interface for complex processing pipelines.

### Methods

*   `resize(width, height)`: Resizes an image.
*   `apply_filter(filter_name, **kwargs)`: Applies a filter to an image.
*   `smart_crop(width, height, save_steps, output_prefix, output_folder, strategy)`: Intelligently crops an image.
*   `save(output_path, quality)`: Saves an image.

## `SmartCropEngine` Class

The `SmartCropEngine` class is responsible for intelligent cropping of images using computer vision techniques. It uses OpenCV for edge detection, contour analysis, and rule-of-thirds composition.

### Methods

*   `smart_crop(image, target_width, target_height, save_steps, output_prefix, output_folder, strategy)`: Performs intelligent cropping on an image.

## `FilterRegistry` Class

The `FilterRegistry` class is responsible for managing and applying image filters. It has a set of built-in filters like grayscale, blur, sepia, and also allows for registering custom filters.

### Methods

*   `register(name, filter_func)`: Registers a new filter.
*   `apply(image, filter_name, **kwargs)`: Applies a filter to an image.
*   `list_filters()`: Lists the available filters.
