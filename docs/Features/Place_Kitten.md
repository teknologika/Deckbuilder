# PlaceKitten Library

## ⚠️ IMPLEMENTATION STATUS: NOT IMPLEMENTED

**Current Status**: 📋 **PLANNED / DESIGN PHASE ONLY**

This documentation describes the planned design for PlaceKitten library. **The actual implementation does not exist yet** - only placeholder files are present in `src/placekitten/`.

## Overview

PlaceKitten is a planned comprehensive Python image processing library that will provide intelligent image cropping, filtering, and placeholder generation capabilities. The library will combine advanced computer vision processing with a simple Python API for creating presentation-ready images.

## Architecture

### Core Components

1. **PlaceKitten Class**: Main interface for image processing and generation
2. **Intelligent Cropping Engine**: Computer vision-based automatic cropping for optimal composition
3. **Filter Pipeline**: Comprehensive image processing filters and effects
4. **Presentation Integration**: Seamless integration with deck-builder-mcp for slide images

### Design Philosophy

- **Content-Aware Processing**: Automatic detection of important regions using edge detection and contour analysis
- **Presentation-Optimized**: 16:9 aspect ratio cropping with rule-of-thirds composition
- **Simple Python API**: Easy-to-use classes and methods with extensive customization options
- **Quality Output**: High-resolution processing with detailed step visualization

## Python API Specification

### Basic Usage

```python
from placekitten import PlaceKitten, ImageProcessor

# Initialize the library
pk = PlaceKitten()

# Generate a placeholder image
image = pk.generate(width=800, height=450)

# Process an existing image with smart cropping
processor = ImageProcessor("input/photo.jpg")
cropped = processor.smart_crop(width=1920, height=1080)
processed = cropped.apply_filter("sepia").save("output/result.jpg")
```

### PlaceKitten Class

```python
class PlaceKitten:
    def __init__(self, source_folder: str = "demo"):
        """Initialize PlaceKitten with source image folder"""

    def generate(self, width: int, height: int = None,
                filter_type: str = None, image_id: int = None,
                random: bool = False) -> ImageProcessor:
        """Generate placeholder image with specified dimensions"""

    def batch_process(self, input_folder: str, output_folder: str,
                     width: int, height: int = None,
                     filters: list = None) -> list:
        """Process multiple images in batch"""
```

### ImageProcessor Class

```python
class ImageProcessor:
    def __init__(self, image_path: str = None, image_array: np.ndarray = None):
        """Initialize with image file or numpy array"""

    def smart_crop(self, width: int, height: int = None,
                   save_steps: bool = False) -> "ImageProcessor":
        """Intelligent cropping with computer vision"""

    def apply_filter(self, filter_name: str, **kwargs) -> "ImageProcessor":
        """Apply image filter"""

    def resize(self, width: int, height: int = None) -> "ImageProcessor":
        """Resize image maintaining aspect ratio"""

    def save(self, output_path: str, quality: str = "high") -> str:
        """Save processed image"""

    def get_array(self) -> np.ndarray:
        """Get image as numpy array"""
```

### Filter Options

#### Available Filters
```python
# Basic filters
processor.apply_filter("greyscale")
processor.apply_filter("blur", strength=10)
processor.apply_filter("invert")
processor.apply_filter("sepia")

# Advanced filters
processor.apply_filter("pixelate", strength=5)
processor.apply_filter("brightness", value=100)
processor.apply_filter("contrast", value=70)
processor.apply_filter("edge_detection")
```

#### Chaining Operations
```python
# Method chaining for complex processing
result = (ImageProcessor("input.jpg")
          .smart_crop(1920, 1080, save_steps=True)
          .apply_filter("sepia")
          .apply_filter("brightness", value=50)
          .save("output/final.jpg"))
```

### Dimension Handling

#### Auto-Height (16:9 aspect ratio)
```python
pk.generate(500)        # 500x281 (16:9)
pk.generate(800)        # 800x450 (16:9)
pk.generate(1920)       # 1920x1080 (16:9)
```

#### Custom Dimensions
```python
pk.generate(500, 280)   # 500x280 custom
pk.generate(800, 600)   # 800x600 custom
pk.generate(1024, 768)  # 1024x768 custom
```

## Intelligent Cropping Engine

### Processing Pipeline

1. **Original Analysis** - Load and validate source image
2. **Grayscale Conversion** - Prepare for edge detection
3. **Noise Reduction** - Gaussian blur for cleaner analysis
4. **Edge Detection** - Canny edge detection for contour identification
5. **Contour Analysis** - Find largest significant contours
6. **Composition Calculation** - Apply rule-of-thirds for optimal cropping
7. **Smart Cropping** - Intelligent crop with subject positioning
8. **Final Processing** - Apply filters and output generation

### Rule-of-Thirds Integration

- **Subject Detection**: Identifies primary subject using largest contour
- **Optimal Positioning**: Centers subject in lower third of 16:9 composition
- **Visual Balance**: Maintains professional presentation standards
- **Boundary Safety**: Ensures crops remain within image bounds

### Step Visualization

When `save_steps=True` is specified, the engine outputs:

1. `_1-1-original.jpg` - Source image
2. `_1-2-grayscale.jpg` - Grayscale conversion
3. `_1-3-blurred.jpg` - Noise reduction
4. `_1-4-edges.jpg` - Edge detection (red highlights)
5. `_1-5-largest-edge.jpg` - Primary contour (green outline)
6. `_1-6-bounding-box.jpg` - Subject bounding box (blue fill)
7. `_1-7-thirds-and-two-thirds.jpg` - Rule-of-thirds grid (yellow)
8. `_1-8-crop-area.jpg` - Final crop area (magenta border)
9. `_1-9-cropped.jpg` - Final processed image

## Integration with Deck Builder

### MCP Tool Integration

```python
def generate_placeholder_image(
    width: int,
    height: Optional[int] = None,
    filter_type: Optional[str] = None,
    image_id: Optional[int] = None,
    random: bool = False,
    smart_crop: bool = True
) -> str:
    """Generate placeholder image for presentation slides"""
    from placekitten import PlaceKitten

    pk = PlaceKitten()
    processor = pk.generate(width, height, filter_type, image_id, random)

    if smart_crop:
        processor = processor.smart_crop(width, height)

    return processor.save(f"output/slide_image_{width}x{height}.jpg")
```

### Slide Template Integration

PlaceKitten can generate images directly for presentation templates:

```python
from placekitten import PlaceKitten

# Generate presentation-ready images
pk = PlaceKitten()
business_image = pk.generate(1920, 1080, image_id=5).apply_filter("sepia").save("images/market_analysis.jpg")

# Use in YAML templates
slides_data = {
    "slides": [
        {
            "layout": "Picture with Caption",
            "content": {
                "title": "Market Analysis",
                "image_path": business_image,
                "caption": "Revenue trends showing consistent growth"
            }
        }
    ]
}
```

### Automatic Image Processing

- **Batch Processing**: Process multiple images from input folder
- **Template Optimization**: Automatic sizing for slide layouts
- **Quality Assurance**: Validation and error handling
- **Format Conversion**: Support for JPG, PNG, WebP formats

## Implementation Phases

### Phase 1: Core Library (Current Focus)
- [ ] Basic placeholder image generation
- [ ] Dimension handling (auto-height and custom)
- [ ] Basic filter pipeline implementation
- [ ] File system integration for image processing

### Phase 2: Intelligent Processing
- [ ] Computer vision pipeline implementation
- [ ] Edge detection and contour analysis
- [ ] Rule-of-thirds composition engine
- [ ] Step visualization system

### Phase 3: Advanced Features
- [ ] Category-based image selection
- [ ] Quality optimization algorithms
- [ ] Batch processing capabilities
- [ ] Performance optimization and caching

### Phase 4: MCP Integration
- [ ] Deck builder tool integration
- [ ] Automatic template sizing
- [ ] Presentation workflow optimization
- [ ] Comprehensive testing and validation

## Technical Requirements

### Dependencies
- OpenCV (cv2) - Computer vision processing
- PIL (Pillow) - Image manipulation
- NumPy - Array processing
- Pathlib - Enhanced file system operations
- Pathlib - File system operations

### Image Processing Requirements
- Input formats: JPG, JPEG, PNG, WebP
- Output formats: JPG, PNG, WebP
- Maximum resolution: 4K (3840x2160)
- Processing quality: Lossless intermediate steps

### Performance Targets
- Processing time: < 2 seconds for standard operations
- Smart crop processing: < 5 seconds with visualization
- Batch processing: 10+ images per minute
- Memory usage: < 500MB per processing session

## Use Cases

### Presentation Development
1. **Quick Prototyping**: Rapid slide creation with placeholder images
2. **Template Testing**: Validate layouts with various image dimensions
3. **Content Planning**: Visualize presentation flow with representative images

### Image Processing Workflows
1. **Batch Optimization**: Process multiple images for consistent presentation quality
2. **Automatic Cropping**: Convert landscape images to presentation-ready 16:9 format
3. **Quality Enhancement**: Apply professional filters and adjustments

### Development and Testing
1. **Library Testing**: Consistent placeholder images for development
2. **Layout Validation**: Test presentation layouts with various dimensions
3. **Filter Development**: Experiment with image processing effects

## Success Criteria

### Functional Requirements
- ✅ Python-based image generation with dimensions
- ✅ Filter pipeline with multiple effect options
- ✅ Intelligent cropping with computer vision
- ✅ Integration with deck-builder-mcp workflows

### Quality Requirements
- Professional-grade image processing output
- Consistent 16:9 aspect ratio optimization
- Reliable edge detection and subject identification
- High-performance batch processing capabilities

### User Experience Requirements
- Simple, intuitive Python API
- Comprehensive filter and customization options
- Detailed processing visualization for learning
- Seamless integration with presentation workflows

# Possible implementation
https://tomaszs2.medium.com/effortless-image-cropping-with-python-automate-your-workflow-in-minute-987fbec9c3e8
