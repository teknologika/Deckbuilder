# PlaceKitten Library

The PlaceKitten library is a tool for generating placeholder images from kitten photos. It provides a simple and intuitive API for creating images with different dimensions, filters, and other effects.

## `PlaceKitten` Class

The `PlaceKitten` class is the main entry point for generating placeholder images. It provides methods for generating images with different dimensions, filters, and other effects.

### Methods

*   `generate(width, height, filter_type, image_id, random_selection)`: Generates a placeholder image.
*   `list_available_images()`: Lists the available kitten images.
*   `get_image_count()`: Gets the number of available kitten images.
*   `batch_process(configs, output_folder)`: Processes multiple images in batch.

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
