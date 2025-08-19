# Enhanced Table Color System

Design specification for adding HTML color name support, per-cell color overrides, and transparent backgrounds to the Deckbuilder table system.

## Feature Overview

This enhancement adds three major capabilities:
1. **HTML Color Name Support** - All 140 standard HTML color names
2. **Per-Cell Color Overrides** - Cell-specific colors for status tables
3. **Transparent Background Support** - True transparency with RGBA

## 1. HTML Color Name Support

### Implementation

**New Color Parser** (`src/deckbuilder/core/color_parser.py`):
```python
from pptx.dml.color import RGBColor

# HTML Color Name to RGB mapping
HTML_COLORS = {
    'transparent': None,
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aqua': (0, 255, 255),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'black': (0, 0, 0),
    'blanchedalmond': (255, 235, 205),
    'blue': (0, 0, 255),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'fuchsia': (255, 0, 255),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'gray': (128, 128, 128),
    'green': (0, 128, 0),
    'greenyellow': (173, 255, 47),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'maroon': (128, 0, 0),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'navy': (0, 0, 128),
    'oldlace': (253, 245, 230),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'orange': (255, 165, 0),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'purple': (128, 0, 128),
    'red': (255, 0, 0),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'silver': (192, 192, 192),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'teal': (0, 128, 128),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'white': (255, 255, 255),
    'whitesmoke': (245, 245, 245),
    'yellow': (255, 255, 0),
    'yellowgreen': (154, 205, 50),
}

def parse_color(color_value):
    """
    Parse color value - supports hex, HTML names, and transparent.
    
    Args:
        color_value: Color as hex (#FF0000), HTML name (red), or 'transparent'
        
    Returns:
        RGBColor object or None for transparent
    """
    if not color_value or not isinstance(color_value, str):
        return None
        
    color_value = color_value.strip().lower()
    
    # Handle transparent
    if color_value == 'transparent':
        return None
        
    # Try HTML color name first
    if color_value in HTML_COLORS:
        rgb_values = HTML_COLORS[color_value]
        if rgb_values is None:  # transparent
            return None
        return RGBColor(*rgb_values)
    
    # Fall back to hex parsing
    try:
        color_value = color_value.lstrip("#")
        if len(color_value) == 6:
            r = int(color_value[0:2], 16)
            g = int(color_value[2:4], 16)
            b = int(color_value[4:6], 16)
            return RGBColor(r, g, b)
    except (ValueError, TypeError):
        pass
        
    return None
```

### Usage Examples

```yaml
# HTML color names for styling
custom_colors:
  header_bg: "navy"           # HTML color name
  header_text: "white"        # HTML color name
  primary_row: "lightgray"    # HTML color name
  alt_row: "transparent"      # Transparent rows
  border_color: "darkgray"    # HTML color name
```

## 2. Per-Cell Color Overrides

### Implementation

**Enhanced Cell Processing**:
```python
def _apply_per_cell_colors(self, table, data):
    """
    Apply per-cell color overrides based on cell content.
    
    Args:
        table: PowerPoint table object
        data: Table data array
    """
    for row_idx, row_data in enumerate(data):
        for col_idx, cell_data in enumerate(row_data):
            if row_idx >= len(table.rows) or col_idx >= len(table.columns):
                continue
                
            cell = table.cell(row_idx, col_idx)
            cell_text = str(cell_data).strip().upper()
            
            # Check if cell text is a color name
            color = parse_color(cell_text)
            if color is not None:
                # Apply background color
                cell.fill.solid()
                cell.fill.fore_color.rgb = color
                
                # Apply text color (same as background for invisible effect)
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = color
                        
            elif cell_text == 'TRANSPARENT':
                # Make cell transparent
                cell.fill.background()
```

### Usage Examples

**Status Table with Color Coding**:
```yaml
table_data: |
  | Task | Status | Priority |
  | Setup Database | GREEN | HIGH |
  | Write Tests | YELLOW | MEDIUM |
  | Deploy Code | RED | HIGH |
  | AQUA | AQUA | AQUA |  # Invisible text for spacing
```

**Color-Coded Performance Dashboard**:
```yaml
table_data: |
  | Metric | Q1 | Q2 | Q3 | Q4 |
  | Revenue | GREEN | GREEN | YELLOW | RED |
  | Customers | BLUE | LIGHTBLUE | CYAN | DARKBLUE |
  | Satisfaction | LIME | LIME | LIME | GREEN |
```

## 3. Enhanced Table Configuration

### Row Height and Font Size Clarification

**Current System**:
- `row_height`: Uniform height for ALL rows (cm)
- `header_font_size`: Font size for header row only (points)
- `data_font_size`: Font size for ALL data rows (points)

**Enhanced System**:
```yaml
# Global settings (current)
row_height: 0.8              # All rows same height
header_font_size: 14         # Header row font
data_font_size: 11           # All data rows font

# New: Per-row height control
row_heights: [1.0, 0.8, 0.8, 0.8]  # Individual row heights

# New: Per-row font sizes
font_sizes:
  header: 14                 # Header row
  data: [11, 11, 11]        # Individual data row fonts
  
# New: Per-cell font sizes (for special cells)
cell_fonts:
  - row: 1, col: 2, size: 16  # Specific cell font size
```

## 4. Configuration Schema

### Basic Configuration (Backward Compatible)
```yaml
style: "navy"                    # HTML color name
row_style: "alternating_lightgray"
border_style: "thin_darkgray"
custom_colors:
  header_bg: "darkblue"          # HTML names
  header_text: "white"
  primary_row: "transparent"      # True transparency
  alt_row: "lightgray"
  border_color: "silver"
```

### Advanced Configuration (New Features)
```yaml
# Per-cell color override mode
cell_color_mode: "auto"          # auto | manual | disabled
auto_color_cells: true           # Apply colors to matching cell text

# Enhanced transparency
transparency:
  header: 0.9                    # 90% opaque header
  rows: 0.5                      # 50% opaque rows
  borders: 1.0                   # Fully opaque borders
  
# Advanced row configuration
advanced_rows:
  heights: [1.2, 0.8, 0.8, 0.8] # Per-row heights
  fonts: [14, 11, 11, 11]       # Per-row font sizes
  colors:                        # Per-row color overrides
    - row: 0, bg: "navy", text: "white"
    - row: 1, bg: "transparent", text: "black"
```

## 5. Migration Strategy

### Phase 1: Color Parser Enhancement
1. **Add HTML color parser** to existing `_parse_custom_color` method
2. **Maintain backward compatibility** with hex colors
3. **Add transparency support** with `None` return value

### Phase 2: Per-Cell Color System
1. **Add cell color detection** in table data processing
2. **Apply cell-specific styling** after general table styling
3. **Add configuration options** to enable/disable feature

### Phase 3: Advanced Configuration
1. **Add per-row height/font arrays**
2. **Enhance transparency system**
3. **Add cell-specific overrides**

## 6. Usage Examples

### Status Dashboard
```yaml
---
layout: Table Only
title: "Project Status Dashboard"
style: "white"
row_style: "solid_white"
border_style: "thin_gray"
cell_color_mode: "auto"         # Enable per-cell colors
table_data: |
  | Project | Backend | Frontend | Testing | Deployment |
  | Alpha | GREEN | GREEN | YELLOW | RED |
  | Beta | BLUE | LIGHTBLUE | BLUE | BLUE |
  | Gamma | TRANSPARENT | TRANSPARENT | TRANSPARENT | TRANSPARENT |
  | Delta | LIME | LIME | GREEN | DARKGREEN |
---
```

### Financial Report with Transparent Overlays
```yaml
---
layout: Table with Content Above
title: "Q4 Financial Performance"
content: "Performance metrics with color-coded status indicators"
style: "darkblue"
custom_colors:
  header_bg: "navy"
  header_text: "white"
  primary_row: "transparent"
  border_color: "lightgray"
advanced_rows:
  heights: [1.0, 0.7, 0.7, 0.7, 0.7]
  fonts: [14, 11, 11, 11, 11]
table_data: |
  | Metric | Target | Actual | Status | Trend |
  | Revenue | $500K | $520K | GREEN | ↗ |
  | Costs | $300K | $285K | GREEN | ↓ |
  | Profit | $200K | $235K | LIME | ↗ |
  | ROI | 15% | 18.5% | DARKGREEN | ↗ |
---
```

## 7. Implementation Timeline

### Week 1: Color Parser
- [ ] Create `color_parser.py` with HTML color support
- [ ] Enhance `_parse_custom_color` method
- [ ] Add transparency support
- [ ] Unit tests for color parsing

### Week 2: Per-Cell Colors
- [ ] Add cell color detection logic
- [ ] Implement cell-specific styling
- [ ] Add configuration options
- [ ] Integration tests

### Week 3: Advanced Features
- [ ] Per-row height/font arrays
- [ ] Enhanced transparency system
- [ ] Cell-specific overrides
- [ ] Performance optimization

### Week 4: Documentation & Testing
- [ ] Update documentation with new features
- [ ] Comprehensive test suite
- [ ] User acceptance testing
- [ ] Performance benchmarking

## 8. Benefits

1. **140 HTML Colors**: Easy-to-remember color names (red, blue, etc.)
2. **Status Tables**: Visual status indicators with invisible text
3. **True Transparency**: Proper overlay support for backgrounds
4. **Per-Cell Control**: Granular styling for complex tables
5. **Backward Compatibility**: Existing configurations continue working
6. **Enhanced Flexibility**: Professional table designs with minimal configuration

This enhancement transforms the table system from basic styling to professional-grade color management suitable for dashboard creation, status reporting, and complex data visualization.