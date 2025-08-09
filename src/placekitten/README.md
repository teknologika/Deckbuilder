# PlaceKitten - Intelligent Image Processing Library

[![PlaceKitten Complete](https://img.shields.io/badge/PlaceKitten-Complete-brightgreen)](../../TASK.md)
[![Deckbuilder Integration](https://img.shields.io/badge/Deckbuilder-Integrated-blue)](#deckbuilder-integration)
[![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-blue)](#smart-cropping-engine)
[![Filter Pipeline](https://img.shields.io/badge/Filters-10%2B%20Available-orange)](#filter-pipeline)
[![Tests Passing](https://img.shields.io/badge/Tests-108%20Passing-green)](#testing)

PlaceKitten is a comprehensive Python image processing library that provides intelligent image cropping, filtering, and placeholder generation capabilities. Built with advanced computer vision processing and a simple Python API, PlaceKitten creates presentation-ready images with professional quality.

## ✨ Key Features

### 🧠 **Intelligent Processing**
- **Smart Cropping**: Computer vision-based automatic cropping with face detection
- **Rule-of-Thirds**: Optimal composition using professional photography principles  
- **9-Step Visualization**: Complete processing pipeline with debug output
- **Aspect Ratio Preservation**: Flexible dimensions with intelligent scaling

### 🎨 **Professional Filters**
- **10+ Filter Options**: Grayscale, sepia, blur, brightness, contrast, and more
- **Method Chaining**: Fluent API for complex processing workflows
- **High-Quality Output**: LANCZOS resampling for professional results
- **Customizable Parameters**: Fine-tune effects for specific needs

### 🖼️ **Smart Placeholder Generation**
- **6 Curated Images**: High-quality kitten photos for development and testing
- **1-Based Indexing**: User-friendly image selection (1, 2, 3...)
- **Random Selection**: Smart fallback for invalid image IDs
- **Full-Size Support**: Original dimensions when no size specified

## 🚀 Quick Start

### Installation
PlaceKitten is included with the Deckbuilder library:

```bash
# Clone the repository
git clone https://github.com/teknologika/Deckbuilder.git
cd Deckbuilder

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from placekitten import PlaceKitten, ImageProcessor

# Initialize PlaceKitten
pk = PlaceKitten()

# Generate a placeholder image (16:9 aspect ratio)
image = pk.generate(width=800, height=450)
result = image.save("output.jpg")

# Apply filters with method chaining
filtered = pk.generate(width=1200, height=800, image_id=2)
result = filtered.apply_filter("sepia").apply_filter("brightness", value=110).save("filtered.jpg")

# Process existing images with smart cropping
processor = ImageProcessor("input.jpg")
cropped = processor.smart_crop(1920, 1080, save_steps=True)
result = cropped.save("smart_cropped.jpg")
```

## 📖 Core API

### PlaceKitten Class

```python
class PlaceKitten:
    def __init__(self, source_folder: str = "demo"):
        """Initialize with kitten image collection"""
    
    def generate(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        filter_type: Optional[str] = None,
        image_id: Optional[int] = None,
        random_selection: bool = False,
    ) -> ImageProcessor:
        """Generate placeholder image with flexible dimensions"""
    
    def list_available_images(self) -> List[str]:
        """Get list of available image filenames"""
    
    def get_image_count(self) -> int:
        """Get total number of available images"""
```

#### Flexible Dimension Handling

```python
# Aspect ratio preservation (original dimensions)
pk.generate()                    # Full size image
pk.generate(width=800)           # Height calculated to preserve aspect ratio
pk.generate(height=450)          # Width calculated to preserve aspect ratio
pk.generate(width=800, height=450)  # Exact dimensions

# 1-based indexing for user-friendly selection
pk.generate(width=500, image_id=1)   # First image
pk.generate(width=500, image_id=3)   # Third image
pk.generate(width=500, image_id=99)  # Random fallback (invalid ID)
```

### ImageProcessor Class

```python
class ImageProcessor:
    def __init__(self, image_path: str = None, image_array: np.ndarray = None):
        """Initialize with image file or numpy array"""
    
    def smart_crop(
        self,
        width: int,
        height: Optional[int] = None,
        save_steps: bool = False,
        output_prefix: str = "smart_crop",
        output_folder: Optional[str] = None,
        strategy: str = "haar-face",
    ) -> "ImageProcessor":
        """Intelligent cropping with computer vision"""
    
    def apply_filter(self, filter_name: str, **kwargs) -> "ImageProcessor":
        """Apply image filter with customizable parameters"""
    
    def resize(self, width: int, height: Optional[int] = None) -> "ImageProcessor":
        """Resize image maintaining aspect ratio"""
    
    def save(self, output_path: str, quality: str = "high") -> str:
        """Save processed image with quality control"""
```

## 🧠 Smart Cropping Engine

PlaceKitten's intelligent cropping engine uses advanced computer vision to create optimal compositions:

### Processing Pipeline

1. **Original Analysis** - Load and validate source image
2. **Grayscale Conversion** - Prepare for edge detection  
3. **Noise Reduction** - Gaussian blur for cleaner analysis
4. **Edge Detection** - Canny edge detection for contour identification
5. **Subject Detection** - Haar cascade face detection + contour analysis
6. **Bounding Box Calculation** - Identify primary subject region
7. **Rule-of-Thirds Grid** - Apply professional composition guidelines
8. **Crop Area Optimization** - Calculate optimal crop positioning
9. **Final Processing** - Generate cropped result with applied filters

### Smart Cropping Example

```python
from placekitten import ImageProcessor

# Load an image and apply intelligent cropping
processor = ImageProcessor("photo.jpg")

# Smart crop with step visualization
result = processor.smart_crop(
    width=1920, 
    height=1080,
    save_steps=True,           # Save debug steps
    output_folder="debug/",    # Output directory
    strategy="haar-face"       # Face-priority cropping
)

# Save final result
output_file = result.save("smart_cropped_result.jpg")
print(f"Smart crop completed: {output_file}")

# Access crop information
crop_info = result.get_crop_info()
print(f"Original size: {crop_info['original_size']}")
print(f"Subject detected: {crop_info['subject_bbox']}")
```

### Step Visualization

When `save_steps=True`, the engine outputs detailed processing steps:

- `smart_crop_1-original.jpg` - Source image
- `smart_crop_2-grayscale.jpg` - Grayscale conversion
- `smart_crop_3-blurred.jpg` - Noise reduction
- `smart_crop_4-edges.jpg` - Edge detection (red highlights)
- `smart_crop_5-largest-contour.jpg` - Primary contour (green outline)
- `smart_crop_6-bounding-box.jpg` - Subject bounding box (blue overlay)
- `smart_crop_7-rule-of-thirds.jpg` - Rule-of-thirds grid (yellow lines)
- `smart_crop_8-crop-area.jpg` - Final crop area (magenta border)
- `smart_crop_9-final.jpg` - Final processed result

## 🎨 Filter Pipeline

PlaceKitten includes a comprehensive filter system with 10+ professional effects:

### Available Filters

```python
# Basic filters
processor.apply_filter("grayscale")
processor.apply_filter("sepia") 
processor.apply_filter("invert")
processor.apply_filter("blur", strength=5)

# Advanced filters
processor.apply_filter("brightness", value=120)  # 120% brightness
processor.apply_filter("contrast", value=85)     # 85% contrast
processor.apply_filter("saturation", value=150)  # 150% saturation
processor.apply_filter("sharpness", value=200)   # 200% sharpness
processor.apply_filter("pixelate", strength=10)  # 10px blocks

# Specialized filters
processor.apply_filter("edge_enhance")
processor.apply_filter("edge_enhance_more")
```

### Method Chaining Workflows

```python
# Complex processing pipeline
result = (ImageProcessor("input.jpg")
    .smart_crop(1200, 800, save_steps=True)
    .apply_filter("sepia")
    .apply_filter("brightness", value=110)
    .apply_filter("contrast", value=90)
    .save("final_result.jpg"))

# Business presentation styling
professional = (pk.generate(1920, 1080, image_id=1)
    .smart_crop(1920, 1080)
    .apply_filter("grayscale")        # Professional look
    .apply_filter("contrast", value=95)
    .save("presentation_image.jpg"))
```

### Filter Registry

```python
from placekitten import list_available_filters, register_custom_filter

# List all available filters
filters = list_available_filters()
print(f"Available filters: {filters}")

# Register custom filter
def vintage_effect(image, **kwargs):
    # Custom filter implementation
    return processed_image

register_custom_filter("vintage", vintage_effect)
```

## 🔗 Deckbuilder Integration ✅ COMPLETE

PlaceKitten is fully integrated with the Deckbuilder presentation system providing intelligent image fallbacks:

### Automatic Image Fallbacks ✅ IMPLEMENTED

When `image_path` is missing or invalid in PowerPoint templates, PlaceKitten automatically generates professional placeholder images:

```yaml
# Current YAML structure (fully implemented)
layout: Picture with Caption
title: Market Analysis
media:
  image_path: "charts/revenue_growth.png"  # Primary image (validated)
  caption: "Q4 revenue increased 23%"      # Caption text

# Alternative formats also supported:
layout: Picture with Caption
title: System Architecture
image_1: "assets/non_existent_image.png"   # Triggers automatic fallback
text_caption_1: "Smart image fallback with professional styling"
```

**Automatic Fallback Features** (fully implemented):
- ✅ **File Validation**: Checks image existence, format, and accessibility
- ✅ **Professional Styling**: Automatic grayscale filtering for business presentations
- ✅ **Smart Cropping**: Computer vision-based cropping to exact placeholder dimensions
- ✅ **Performance Optimization**: Intelligent caching prevents duplicate processing
- ✅ **Seamless Integration**: Zero user intervention required for fallback generation

### Professional Presentation Styling ✅ INTEGRATED

```python
# PlaceKitten-Deckbuilder integration handles this automatically:
# 1. Image validation in Deckbuilder engine
# 2. Automatic PlaceKitten fallback generation
# 3. Professional styling applied via PlaceKittenIntegration

# Manual professional placeholder generation:
def create_presentation_placeholder(width, height):
    pk = PlaceKitten()
    return (pk.generate(image_id=1)           # Consistent selection
             .smart_crop(width, height)       # Exact dimensions
             .apply_filter("grayscale")       # Professional look
             .save(f"placeholder_{width}x{height}.jpg"))

# Direct integration usage (automatic in Deckbuilder):
from deckbuilder.image.placeholder import PlaceKittenIntegration
from deckbuilder.image.image_handler import ImageHandler

# This happens automatically when image_path is invalid:
image_handler = ImageHandler("cache/")
placekitten = PlaceKittenIntegration(image_handler)
fallback_path = placekitten.generate_fallback_image(1920, 1080)
```

## 🏗️ Implementation Details

### Dependencies

- **OpenCV (cv2)** - Computer vision processing and face detection
- **Pillow (PIL)** - Image manipulation, I/O, and format conversion
- **NumPy** - Array processing and mathematical operations
- **Pathlib** - Enhanced file system operations and path handling

### Performance Specifications ✅ ACHIEVED

- ✅ **Processing Time**: < 2 seconds for standard operations (measured)
- ✅ **Smart Crop**: < 5 seconds with full step visualization (optimized)
- ✅ **Memory Usage**: < 500MB per processing session (validated)
- ✅ **Supported Formats**: JPG, JPEG, PNG, WebP, BMP, GIF (input and output)
- ✅ **Maximum Resolution**: 4K (3840x2160) tested and validated
- ✅ **Cache Performance**: Instant retrieval for duplicate requests
- ✅ **Integration Speed**: Seamless fallback generation in Deckbuilder workflow

### Image Collection

PlaceKitten includes 6 high-quality kitten images for development and testing:

1. `ACuteKitten-1.png` - Single kitten portrait
2. `ACuteKitten-2.png` - Kitten with toys
3. `ACuteKitten-3.png` - Sleeping kitten
4. `TwoKittens Playing-1.png` - Playful duo
5. `TwoKittens Playing-2.png` - Interactive scene  
6. `TwoKittens Sleeping-1.png` - Peaceful rest

## 📝 Examples & Use Cases

### 0. Deckbuilder Integration (Primary Use Case) ✅ IMPLEMENTED

```python
# Automatic integration - no code required!
# Simply use Deckbuilder with image paths:

# Via MCP Server (Claude Desktop):
from mcp_server.tools import create_presentation_from_markdown

markdown_content = """
---
layout: Picture with Caption
title: Product Launch
media:
  image_path: "missing_product_image.png"  # PlaceKitten fallback triggers
  caption: "New product features overview"
---
"""

# PlaceKitten automatically provides professional fallback
result = create_presentation_from_markdown(markdown_content)
# Result: PowerPoint with grayscale kitten image, perfectly sized

# Via Direct Engine Usage:
from deckbuilder.engine import Deckbuilder

db = Deckbuilder()
presentation = db.create_presentation_from_markdown(markdown_content)
# Same result: automatic PlaceKitten fallback with professional styling
```

### 1. Presentation Development

```python
# Quick prototype with consistent placeholders
pk = PlaceKitten()

# Generate slide images with professional styling
for slide_num in range(1, 6):
    image = (pk.generate(1920, 1080, image_id=slide_num)
             .apply_filter("grayscale")
             .apply_filter("brightness", value=105)
             .save(f"slide_{slide_num}_placeholder.jpg"))
```

### 2. Template Testing

```python
# Test various aspect ratios for template validation
test_dimensions = [
    (1920, 1080),  # 16:9 widescreen
    (1024, 768),   # 4:3 standard
    (800, 600),    # SVGA
    (1280, 720),   # HD
]

pk = PlaceKitten()
for width, height in test_dimensions:
    test_image = pk.generate(width, height, image_id=1)
    test_image.save(f"test_{width}x{height}.jpg")
```

### 3. Batch Processing

```python
# Process multiple images with consistent styling
input_folder = Path("raw_images")
output_folder = Path("processed")
output_folder.mkdir(exist_ok=True)

for image_file in input_folder.glob("*.jpg"):
    processor = ImageProcessor(str(image_file))
    result = (processor
              .smart_crop(1200, 800)
              .apply_filter("sepia")
              .save(str(output_folder / f"processed_{image_file.name}")))
    print(f"Processed: {result}")
```

## 🔧 Advanced Configuration

### Deckbuilder Integration Configuration

```python
# The integration is configured via environment variables:
# DECK_TEMPLATE_FOLDER, DECK_OUTPUT_FOLDER, DECK_TEMPLATE_NAME

# Cache directory is automatically set in output folder:
# {DECK_OUTPUT_FOLDER}/tmp/image_cache/

# Manual configuration for standalone usage:
from deckbuilder.image_handler import ImageHandler
from deckbuilder.placekitten_integration import PlaceKittenIntegration

# Custom cache location
image_handler = ImageHandler("custom/cache/path")
placekitten = PlaceKittenIntegration(image_handler)

# Generate fallback with custom dimensions
fallback = placekitten.generate_fallback_image(1600, 900)
print(f"Generated fallback: {fallback}")
```

### Custom Source Images

```python
# Use custom image collection
pk = PlaceKitten("custom_folder")  # Images in src/placekitten/images/custom_folder/

# Or process specific images
processor = ImageProcessor("custom_image.jpg")
result = processor.smart_crop(800, 600).save("output.jpg")
```

### Batch Processing with Configuration

```python
# Batch process with custom configurations
configs = [
    {"width": 1920, "height": 1080, "filter_type": "grayscale", "image_id": 1},
    {"width": 800, "height": 600, "filter_type": "sepia", "image_id": 2},
    {"width": 1200, "height": 800, "filter_type": "blur", "image_id": 3},
]

pk = PlaceKitten()
results = pk.batch_process(configs, output_folder="batch_output")
print(f"Generated {len(results)} images")
```

## 🐛 Troubleshooting

### Common Issues

**Import Error**: `ModuleNotFoundError: No module named 'cv2'`
```bash
pip install opencv-python
```

**Memory Issues**: Large image processing
```python
# Use quality settings to manage memory
processor.save("output.jpg", quality="medium")  # Reduces memory usage
```

**Permission Errors**: File access issues
```python
# Ensure output directories exist
output_path = Path("output")
output_path.mkdir(parents=True, exist_ok=True)
```

### Performance Optimization

```python
# For better performance:
# 1. Use appropriate quality settings
processor.save("output.jpg", quality="high")  # vs "medium" or "low"

# 2. Avoid unnecessary step visualization in production
processor.smart_crop(800, 600, save_steps=False)  # Default

# 3. Cache frequently used images
cached_processor = pk.generate(1920, 1080, image_id=1)  # Reuse this
```

## 📚 API Reference

For complete API documentation, see:
- [PlaceKitten Core API](core.py) - Main image generation class
- [ImageProcessor API](processor.py) - Image manipulation and processing
- [Smart Crop Engine](smart_crop.py) - Computer vision cropping algorithms
- [Filter Pipeline](filters.py) - Available filters and custom filter registration

## 🧪 Testing

PlaceKitten includes comprehensive test coverage with 108 total tests:

```bash
# Run PlaceKitten-specific tests
pytest tests/placekitten/ -v

# Run integration tests with Deckbuilder
pytest tests/deckbuilder/test_image_integration.py -v

# Run all tests including image fallback validation
pytest tests/ -k "placekitten or image"
```

**Test Coverage**:
- ✅ **18 PlaceKitten Core Tests**: Basic functionality, smart cropping, filters
- ✅ **15 Deckbuilder Integration Tests**: Fallback generation, markdown/JSON input
- ✅ **File Size Validation**: Confirms images actually appear in PowerPoint files
- ✅ **Professional Styling**: Validates grayscale filtering and smart cropping
- ✅ **Performance Testing**: Caching, processing speed, memory usage

## 🤝 Contributing

PlaceKitten is part of the Deckbuilder project. For contribution guidelines, see the main [project repository](../../README.md).

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run code quality checks
black --line-length 100 src/placekitten/
flake8 src/placekitten/ --max-line-length=100

# Run tests
pytest tests/placekitten/ -v --cov=src/placekitten
```

## 📄 License

MIT License - see the main project for details.

---

**PlaceKitten** - Professional image processing made simple 🐱