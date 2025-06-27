# Image Support - PlaceKitten Integration Design

## Overview

This document specifies the integration of the PlaceKitten library with Deckbuilder's PowerPoint generation engine to provide seamless image support for presentations. The design implements automatic fallback image generation with professional styling when user-provided images are missing or invalid.

## Design Philosophy

### "See What We Did There? :-)" - Smart Professional Defaults

The integration leverages PlaceKitten's computer vision capabilities to provide:
- **Grayscale filtering** for business-appropriate presentation context
- **Smart cropping** with face detection and rule-of-thirds composition
- **Seamless fallback behavior** requiring no user intervention
- **Professional quality** that maintains presentation integrity

This approach transforms missing images from presentation blockers into elegant placeholder solutions.

## Current State Analysis

### ✅ What's Working (PlaceKitten Library)
- Complete computer vision pipeline with OpenCV edge detection
- Smart cropping engine with face detection and rule-of-thirds
- 9-step visualization system for debugging and education
- 10+ professional filters including grayscale, sepia, brightness
- Flexible dimension handling with aspect ratio preservation
- Method chaining for complex processing workflows

### ✅ What's Working (Deckbuilder Engine)
- "Picture with Caption" layout structure in structured frontmatter
- JSON placeholder mapping for `image_1` placeholders
- Caption and description text handling with inline formatting
- PowerPoint template integration with placeholder detection

### ❌ What's Missing (Integration Gap)
- **No actual image insertion** - `image_1` placeholders treated as text
- **No `image_path` field processing** - enhanced YAML structure not implemented
- **No automatic fallback logic** - missing images cause errors
- **No PowerPoint image integration** - `PP_PLACEHOLDER_TYPE.PICTURE` not utilized

## Enhanced YAML Structure

### Current Structure
```yaml
layout: Picture with Caption
title: System Architecture
media:
  caption: High-level system architecture diagram
  description: |
    Main components include:
    • Frontend: React-based interface
    • API: RESTful services
    • Database: PostgreSQL with Redis
```

### Enhanced Structure (Proposed)
```yaml
layout: Picture with Caption
title: System Architecture
media:
  image_path: "assets/architecture_diagram.png"  # NEW - Primary image source
  alt_text: "System architecture overview"       # NEW - Accessibility support
  caption: High-level system architecture diagram
  description: |
    Main components include:
    • Frontend: React-based interface
    • API: RESTful services  
    • Database: PostgreSQL with Redis
```

**Backward Compatibility**: Existing presentations without `image_path` will automatically receive PlaceKitten fallback images.

## Smart Fallback Architecture

### Processing Flow
```
YAML/JSON Input → Parse media.image_path → Validate File Exists
                                              ↓ (if missing/invalid)
PowerPoint Generation ← Insert Image ← PlaceKitten Fallback
                                              ↓
                                    Grayscale + Smart Crop → Cache
```

### Fallback Logic Implementation
```python
def get_image_for_placeholder(image_path, placeholder_dimensions, slide_context):
    """
    Get image for PowerPoint placeholder with smart fallback.
    
    Args:
        image_path: User-provided image path (may be None/invalid)
        placeholder_dimensions: (width, height) from PowerPoint template
        slide_context: Slide metadata for consistent selection
        
    Returns:
        str: Path to image file (original or generated fallback)
    """
    # Primary: Use provided image if valid
    if image_path and os.path.exists(image_path):
        return validate_and_process_image(image_path, placeholder_dimensions)
    
    # Fallback: Generate professional PlaceKitten placeholder
    return generate_placekitten_fallback(placeholder_dimensions, slide_context)

def generate_placekitten_fallback(dimensions, context):
    """Generate professional PlaceKitten fallback with caching."""
    width, height = dimensions
    cache_key = f"placekitten_{width}x{height}_grayscale"
    
    # Check cache first
    cached_path = get_cached_image(cache_key)
    if cached_path:
        return cached_path
    
    # Generate new fallback
    pk = PlaceKitten()
    processor = pk.generate(image_id=1)  # Consistent selection
    
    # Apply professional styling
    styled = (processor
              .smart_crop(width, height)      # Exact dimensions
              .apply_filter("grayscale")      # Business context
              .apply_filter("contrast", value=95))  # Subtle enhancement
    
    # Cache and return
    output_path = f"temp/fallback_{cache_key}.jpg"
    final_path = styled.save(output_path)
    cache_image(cache_key, final_path)
    
    return final_path
```

## PowerPoint Integration Workflow

### 1. Placeholder Detection
```python
from pptx.enum.shapes import PP_PLACEHOLDER_TYPE
from .placeholder_types import is_media_placeholder

def detect_image_placeholders(slide):
    """Detect PICTURE type placeholders in slide."""
    image_placeholders = []
    
    for shape in slide.placeholders:
        if shape.placeholder_format.type == PP_PLACEHOLDER_TYPE.PICTURE:
            image_placeholders.append({
                'shape': shape,
                'dimensions': (shape.width, shape.height),
                'index': shape.placeholder_format.idx
            })
    
    return image_placeholders
```

### 2. Enhanced Engine Integration
```python
def populate_image_placeholder(placeholder_info, media_data, slide_context):
    """
    Populate image placeholder with smart fallback logic.
    
    Args:
        placeholder_info: Dict with shape, dimensions, index
        media_data: Dict with image_path, alt_text, etc.
        slide_context: Slide metadata for caching
    """
    # Get image with fallback logic
    image_path = get_image_for_placeholder(
        media_data.get('image_path'),
        placeholder_info['dimensions'],
        slide_context
    )
    
    # Insert image into PowerPoint placeholder
    try:
        placeholder_info['shape'].insert_picture(image_path)
        
        # Set alt text for accessibility
        if media_data.get('alt_text'):
            placeholder_info['shape'].element.nvPicPr.cNvPr.set('descr', media_data['alt_text'])
            
    except Exception as e:
        # Log error but don't fail presentation generation
        print(f"Warning: Could not insert image {image_path}: {e}")
        # Could implement text fallback here if needed
```

### 3. Template Mapping Updates
```python
# Enhanced structured frontmatter mapping
def enhance_picture_with_caption_mapping(placeholders, slide_data):
    """Enhanced mapping for Picture with Caption layouts."""
    mapping_rules = {}
    
    # Standard text mappings (existing)
    for idx, placeholder_name in placeholders.items():
        name_lower = placeholder_name.lower()
        if "text_caption" in name_lower:
            mapping_rules["media.caption"] = placeholder_name
        elif "content" in name_lower:
            mapping_rules["media.description"] = placeholder_name
    
    # NEW: Image placeholder mapping
    for idx, placeholder_name in placeholders.items():
        if "image_" in placeholder_name.lower():
            mapping_rules["media.image_path"] = {
                'placeholder_name': placeholder_name,
                'type': 'image',
                'fallback_enabled': True
            }
    
    return mapping_rules
```

## Implementation Components

### 1. ImageHandler Class
```python
class ImageHandler:
    """Core image file validation, processing, and management."""
    
    def __init__(self, cache_dir: str = "temp/image_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
    
    def validate_image(self, image_path: str) -> bool:
        """Validate image file existence and format."""
        if not image_path or not os.path.exists(image_path):
            return False
        
        path = Path(image_path)
        return path.suffix.lower() in self.supported_formats
    
    def process_image(self, image_path: str, target_dimensions: tuple) -> str:
        """Process and resize image to target dimensions."""
        # Implementation for image validation, resizing, format conversion
        pass
    
    def get_cached_image(self, cache_key: str) -> Optional[str]:
        """Retrieve cached image if available."""
        # Implementation for cache lookup
        pass
```

### 2. PlaceKittenIntegration Class
```python
class PlaceKittenIntegration:
    """Bridge between PlaceKitten library and Deckbuilder engine."""
    
    def __init__(self, image_handler: ImageHandler):
        self.image_handler = image_handler
        self.pk = PlaceKitten()
    
    def generate_fallback(self, dimensions: tuple, context: dict = None) -> str:
        """Generate professional fallback image with caching."""
        # Implementation for PlaceKitten fallback generation
        pass
    
    def get_professional_styling(self) -> dict:
        """Get consistent professional styling parameters."""
        return {
            'base_filter': 'grayscale',
            'contrast_adjustment': 95,
            'brightness_adjustment': 105,
            'smart_crop_strategy': 'haar-face'
        }
```

### 3. Enhanced Engine Methods
```python
# Add to existing engine.py
def populate_media_content(self, slide, content_data, layout_mapping):
    """Enhanced media content population with image support."""
    
    # Handle image placeholders
    if 'media' in content_data:
        media_data = content_data['media']
        
        # Find image placeholders
        image_placeholders = self.detect_image_placeholders(slide)
        
        for placeholder_info in image_placeholders:
            self.populate_image_placeholder(placeholder_info, media_data, {
                'slide_index': slide.slide_index,
                'layout': content_data.get('layout'),
                'title': content_data.get('title')
            })
    
    # Continue with existing text content population
    # ... existing implementation
```

## Performance Considerations

### Caching Strategy
- **Cache Key Format**: `placekitten_{width}x{height}_{filter}_{strategy}`
- **Cache Location**: `temp/image_cache/` (gitignored)
- **Cache Invalidation**: Size-based LRU eviction (max 100MB)
- **Cache Persistence**: Survives session restarts for performance

### Memory Management
- **Lazy Loading**: PlaceKitten initialization only when needed
- **Streaming Processing**: Large image handling with memory limits
- **Cleanup**: Automatic temp file cleanup after presentation generation

### Processing Optimization
- **Dimension Matching**: Generate exact dimensions to avoid runtime resizing
- **Format Optimization**: JPEG output for smaller file sizes
- **Quality Balance**: High quality (95%) for professional appearance

## Error Handling Strategy

### Graceful Degradation
1. **Primary Image Fails**: Fall back to PlaceKitten generation
2. **PlaceKitten Fails**: Fall back to simple text placeholder
3. **All Image Processing Fails**: Continue presentation generation without images

### User Feedback
```python
def handle_image_error(error_type, details, slide_context):
    """Provide helpful feedback for image processing issues."""
    feedback_messages = {
        'file_not_found': f"Image not found: {details['path']} - using placeholder",
        'invalid_format': f"Unsupported format: {details['format']} - using placeholder", 
        'processing_error': f"Processing failed: {details['error']} - using placeholder"
    }
    
    # Log for developer awareness
    logger.warning(feedback_messages.get(error_type, f"Image issue: {details}"))
    
    # Could extend to user notifications in future
```

## Testing Strategy

### Unit Tests
- **ImageHandler**: File validation, caching, format support
- **PlaceKittenIntegration**: Fallback generation, styling consistency
- **Engine Integration**: Placeholder detection, image insertion

### Integration Tests
- **Complete Workflow**: YAML with image_path → PowerPoint with image
- **Fallback Scenarios**: Missing images → PlaceKitten placeholders
- **Performance Tests**: Cache effectiveness, memory usage

### Visual Validation
- **Presentation Output**: Manual review of generated PowerPoint files
- **Image Quality**: Verify professional appearance of fallback images
- **Layout Integrity**: Ensure images fit properly in templates

## Success Criteria

### Functional Requirements
✅ **Enhanced YAML Support**: `image_path` and `alt_text` fields functional  
✅ **Automatic Fallbacks**: Missing images generate PlaceKitten placeholders  
✅ **Professional Quality**: Grayscale + smart crop for business context  
✅ **Backward Compatibility**: Existing presentations continue working  

### Quality Requirements
✅ **Performance**: <3 seconds for image processing including fallback  
✅ **Reliability**: Zero presentation generation failures due to image issues  
✅ **Professional Appearance**: Fallback images indistinguishable from intentional placeholders  
✅ **Accessibility**: Alt text support for screen readers  

### User Experience Requirements
✅ **Seamless Integration**: No user intervention required for fallbacks  
✅ **Consistent Results**: Same input produces same output (caching)  
✅ **Clear Feedback**: Helpful warnings for image issues without blocking generation  
✅ **Documentation**: Clear examples of enhanced YAML structure  

## Implementation Roadmap

### Phase 1: Core Integration (1-2 days)
1. Create `ImageHandler` and `PlaceKittenIntegration` classes
2. Implement basic fallback logic with PlaceKitten generation
3. Add placeholder detection for `PP_PLACEHOLDER_TYPE.PICTURE`
4. Create unit tests for core functionality

### Phase 2: Enhanced YAML Support (1 day)
1. Extend structured frontmatter parser for `image_path` field
2. Update template mapping logic for image placeholders
3. Implement backward compatibility testing
4. Add integration tests for complete workflow

### Phase 3: Polish & Performance (1 day)
1. Implement caching system for generated images
2. Add error handling and user feedback
3. Performance optimization and memory management
4. Complete documentation and examples

### Phase 4: Documentation & Testing (Half day)
1. Update user documentation with enhanced YAML examples
2. Create troubleshooting guide for image issues
3. Add visual validation tests
4. Comprehensive testing across different templates

## Future Enhancements

### Advanced Features (Phase 5+)
- **Custom Image Collections**: User-provided placeholder image sets
- **Smart Image Selection**: Context-aware image selection based on slide content
- **Advanced Styling Options**: Configurable filter chains for different presentation themes
- **Batch Image Processing**: Optimize presentations with multiple images
- **Image Analytics**: Usage statistics and optimization recommendations

### MCP Tool Integration
- **`generate_placeholder_image`**: Direct PlaceKitten generation tool
- **`process_presentation_images`**: Batch image optimization
- **`analyze_image_usage`**: Presentation image analysis and recommendations

This design provides a comprehensive foundation for seamless image support in Deckbuilder presentations while maintaining the professional quality and ease of use that defines the platform.