# Advanced Features Example

This example showcases advanced Deckbuilder features including image processing, complex layouts, and rich formatting.

## Usage

```bash
deckbuilder create examples/advanced_features.md --output "Advanced Demo"
```

## Advanced Presentation

---
layout: Title Slide
title: **Advanced Deckbuilder Features**
subtitle: ***PlaceKitten Integration*** & Smart Content Processing
---

---
layout: Title and Content
title: PlaceKitten Image Processing Pipeline
content: |
  **9-Step Smart Cropping Process:**
  
  1. ***Original Analysis*** - Load and validate source
  2. **Grayscale Conversion** - Prepare for edge detection
  3. *Noise Reduction* - Gaussian blur for analysis
  4. **Edge Detection** - Canny algorithm for contours
  5. ***Subject Detection*** - Face detection + contour analysis
  6. **Bounding Box** - Primary subject identification
  7. *Rule-of-Thirds Grid* - Professional composition
  8. **Crop Optimization** - Calculate optimal positioning
  9. ***Final Processing*** - Generate with applied filters
---

---
layout: Comparison
title: Image Fallback Comparison
left:
  title: Without PlaceKitten
  content: |
    ❌ **Broken images**
    ❌ *Manual placeholder hunting*
    ❌ Inconsistent sizing
    ❌ ___Development delays___
right:
  title: With PlaceKitten
  content: |
    ✅ **Automatic fallbacks**
    ✅ *Professional styling*
    ✅ Perfect dimensions
    ✅ ___Instant generation___
---

---
layout: Picture with Caption  
title: Computer Vision Processing
media:
  image_path: "examples/missing_chart.png"  # Triggers PlaceKitten with smart crop
  caption: "***Intelligent cropping*** with face detection and **rule-of-thirds** composition"
---

---
layout: Picture with Caption
title: Professional Business Styling  
media:
  image_path: "examples/invalid_diagram.jpg"  # Another fallback example
  caption: "Automatic **grayscale filtering** for *business-appropriate* presentations"
---

---
layout: Four Columns
title: PlaceKitten Feature Matrix
columns:
  - title: Computer Vision
    content: |
      • **Face detection**
      • *Contour analysis* 
      • ***Edge detection***
      • ___Composition rules___
  - title: Smart Filters
    content: |
      • **Grayscale** business mode
      • *Sepia* vintage effects
      • ***Blur*** backgrounds
      • ___Brightness___ control
  - title: Performance
    content: |
      • **< 2 second** processing
      • *Intelligent caching*
      • ***Memory optimized***
      • ___Batch processing___
  - title: Integration
    content: |
      • **Zero configuration**
      • *Seamless fallbacks*
      • ***CLI commands***
      • ___Python API___
---

---
layout: Table
title: Technical Specifications
style: alternating_light_gray
---

| **Component** | *Technology* | ___Performance___ | **Status** |
|---------------|--------------|-------------------|------------|
| Smart Cropping | ***OpenCV*** | < 5s with visualization | ✅ Complete |
| Image Processing | **Pillow** | < 2s standard ops | ✅ Complete |
| Face Detection | *Haar Cascades* | Real-time | ✅ Complete |
| Caching System | ___Intelligent___ | Instant retrieval | ✅ Complete |
| CLI Integration | **Standalone** | Zero config | ✅ Complete |
| MCP Server | *FastMCP* | Claude Desktop | ✅ Complete |

---
layout: Section Header
title: Ready for Production
subtitle: **PyPI Distribution** & ***Enterprise Ready***
---