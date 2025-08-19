# Table Styling Guide

Learn how to create professionally styled tables in your presentations with complete control over colors, fonts, borders, and dimensions.

## Quick Start

```yaml
---
layout: Table Only
title: "Sales Performance"
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
header_font_size: 14
data_font_size: 11
table_data: |
  | Region | Q1 | Q2 | Q3 |
  | North  | $125K | $132K | $145K |
  | South  | $98K  | $105K | $118K |
---
```

## Style Categories

### Header Styles (`style`)
Controls the appearance of your table header row:

| Style | Background | Text Color | Best For |
|-------|------------|------------|----------|
| `dark_blue_white_text` | Dark Blue (#4472C4) | White | Professional presentations |
| `light_blue_dark_text` | Light Blue (#D9EDFF) | Dark Gray | Clean, modern look |
| `dark_gray_white_text` | Dark Gray (#666666) | White | Corporate documents |
| `light_gray_dark_text` | Light Gray (#F2F2F2) | Dark Gray | Subtle emphasis |
| `white_dark_text` | White | Dark Gray | Minimal styling |
| `accent_color_white_text` | Accent Blue (#4472C4) | White | Brand consistency |

### Row Styles (`row_style`)
Controls the appearance of data rows:

| Style | Primary Row | Alternate Row | Effect |
|-------|-------------|---------------|---------|
| `alternating_light_gray` | White | Light Gray (#F8F8F8) | Easy to read |
| `alternating_light_blue` | White | Light Blue (#F0F8FF) | Modern appearance |
| `solid_white` | White | White | Clean, minimal |
| `solid_light_gray` | Light Gray | Light Gray | Subtle background |
| `no_fill` | Transparent | Transparent | Overlay-friendly |

### Border Styles (`border_style`)
Controls table borders:

| Style | Width | Placement | Best For |
|-------|-------|-----------|----------|
| `thin_gray` | 0.025cm | All borders | Standard tables |
| `thick_gray` | 0.05cm | All borders | Emphasis |
| `header_only` | 0.025cm | Header borders only | Clean look |
| `outer_only` | 0.025cm | Perimeter only | Contained appearance |
| `no_borders` | None | No borders | Minimal design |

## Font Controls

### Font Sizing
```yaml
header_font_size: 14    # Header row font size (points)
data_font_size: 11      # Data row font size (points)
```

**Recommended combinations:**
- **Readable**: header: 14, data: 11
- **Compact**: header: 12, data: 10  
- **Large**: header: 16, data: 13

## Dimension Controls

### Table Sizing
```yaml
table_width: 20.0       # Total width in cm
table_height: 12.0      # Total height in cm
row_height: 0.8         # Uniform row height in cm
```

### Column Width Control
```yaml
# Individual column widths (cm)
column_widths: [6.0, 4.0, 5.0, 5.0]

# Auto-distribution (equal widths)
table_width: 18.0  # Columns auto-sized equally
```

## Custom Colors

Override any style with custom hex colors:

```yaml
custom_colors:
  header_bg: "#003366"      # Header background
  header_text: "#FFFFFF"    # Header text color
  primary_row: "#F5F5F5"    # Primary row background
  alt_row: "#E8E8E8"        # Alternate row background
  border_color: "#888888"   # Border color
```

### Color Examples

**Corporate Blue:**
```yaml
style: white_dark_text
custom_colors:
  header_bg: "#1F4E79"
  header_text: "#FFFFFF"
```

**Minimal Grayscale:**
```yaml
style: light_gray_dark_text
row_style: solid_white
border_style: header_only
custom_colors:
  header_bg: "#E5E5E5"
  border_color: "#CCCCCC"
```

**Transparent Overlay:**
```yaml
style: white_dark_text
row_style: no_fill
border_style: no_borders
custom_colors:
  header_bg: "rgba(0,0,0,0)"  # Transparent header
  header_text: "#FFFFFF"      # White text
```

## Complete Examples

### Professional Sales Report
```yaml
---
layout: Table Only
title: "Q3 Sales Performance by Region"
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
header_font_size: 13
data_font_size: 11
table_width: 20.0
column_widths: [5.0, 4.0, 4.0, 4.0, 3.0]
row_height: 0.7
table_data: |
  | Region | Q1 Sales | Q2 Sales | Q3 Sales | Growth |
  | North America | $245,000 | $268,000 | $285,000 | +16.3% |
  | Europe | $189,000 | $201,000 | $215,000 | +13.8% |
  | Asia Pacific | $156,000 | $178,000 | $195,000 | +25.0% |
  | Latin America | $98,000 | $105,000 | $112,000 | +14.3% |
---
```

### Minimal Design Table
```yaml
---
layout: Table with Content Above
title: "Team Status Update"
content: "Current project assignments and completion rates:"
style: light_gray_dark_text
row_style: solid_white
border_style: header_only
header_font_size: 12
data_font_size: 10
custom_colors:
  header_bg: "#F0F0F0"
  border_color: "#D0D0D0"
table_data: |
  | Team Member | Project | Status | Complete |
  | Alice Johnson | Website Redesign | In Progress | 75% |
  | Bob Chen | Mobile App | Testing | 90% |
  | Carol Davis | API Integration | Planning | 25% |
---
```

### Custom Brand Colors
```yaml
---
layout: Table Only
title: "Brand Color Palette"
style: white_dark_text
row_style: solid_white
border_style: outer_only
header_font_size: 14
data_font_size: 11
custom_colors:
  header_bg: "#8B0000"      # Dark red brand color
  header_text: "#FFFFFF"
  border_color: "#8B0000"
table_data: |
  | Color Name | Hex Code | RGB Values | Usage |
  | Brand Red | #8B0000 | 139, 0, 0 | Primary brand |
  | Accent Gray | #4A4A4A | 74, 74, 74 | Text color |
  | Light Gray | #F5F5F5 | 245, 245, 245 | Background |
---
```

## Advanced Techniques

### Mixed Content Tables
Combine tables with other content on the same slide:

```yaml
---
layout: Table with Content Above
title: "Monthly Performance Review"
content: |
  Key highlights from this month's performance data:
  
  • **Revenue growth** exceeded targets by 12%
  • *Customer satisfaction* scores improved to 4.8/5
  • Team productivity increased across all regions

style: dark_blue_white_text
row_style: alternating_light_blue
border_style: thin_gray
table_data: |
  | Metric | Target | Actual | Variance |
  | Revenue | $500K | $560K | +12% |
  | Customers | 1,200 | 1,245 | +3.8% |
  | Satisfaction | 4.5 | 4.8 | +6.7% |
---
```

### Responsive Column Sizing
Let Deckbuilder auto-size columns based on content:

```yaml
# Option 1: Specify total width, auto-distribute columns
table_width: 18.0

# Option 2: Specify some columns, auto-size others
column_widths: [6.0, "auto", "auto", 4.0]  # First and last fixed, middle auto

# Option 3: Proportional sizing
column_widths: ["25%", "35%", "20%", "20%"]  # Percentage-based
```

## Best Practices

### 1. Choose Appropriate Styles
- **Financial data**: `dark_blue_white_text` + `alternating_light_gray`
- **Status reports**: `light_gray_dark_text` + `solid_white`
- **Comparison tables**: `accent_color_white_text` + `alternating_light_blue`

### 2. Font Size Guidelines
- **Dense data**: Smaller fonts (10-11pt data, 12pt header)
- **Key metrics**: Larger fonts (12-13pt data, 14-16pt header)
- **Presentation distance**: Consider viewing distance when sizing

### 3. Color Accessibility
- Ensure sufficient contrast between text and background
- Test with colorblind-friendly palettes
- Use custom colors for brand consistency

### 4. Column Width Tips
- **Numeric data**: Narrower columns (3-4cm)
- **Text descriptions**: Wider columns (6-8cm)
- **Mixed content**: Use custom column_widths array

### 5. Border Strategy
- **Data-heavy**: Use `thin_gray` for structure
- **Clean design**: Use `header_only` for minimal look
- **Overlay tables**: Use `no_borders` for transparency

## Troubleshooting

### Common Issues

**Table too wide for slide:**
```yaml
table_width: 18.0  # Reduce from default
# or
column_widths: [4.0, 4.0, 4.0, 4.0]  # Specify exact widths
```

**Text too small to read:**
```yaml
header_font_size: 14
data_font_size: 12
row_height: 0.8  # Increase for better spacing
```

**Colors not applying:**
```yaml
# Ensure proper hex format
custom_colors:
  header_bg: "#FF0000"  # Include # symbol
  # not "FF0000" or "red"
```

**Borders not showing:**
```yaml
border_style: thin_gray  # Ensure valid style name
custom_colors:
  border_color: "#333333"  # Dark enough to see
```

## Next Steps

- See [Table Style Reference](../reference/table-styles.md) for complete style listings
- Check [Structured Frontmatter Patterns](../reference/frontmatter-patterns.md) for layout options
- View [Brand Customization Guide](./brand-customization.md) for corporate styling