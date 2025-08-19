# Status Tables with Per-Cell Colors

Learn how to create dynamic status tables where cell content automatically determines colors for visual status indicators.

## Overview

Status tables use **per-cell color detection** to automatically apply colors based on cell content. When a cell contains a valid HTML color name (like "GREEN", "RED", "BLUE"), Deckbuilder automatically:

1. **Sets the background color** to match the color name
2. **Sets the text color** to match the background (creating invisible text effect)
3. **Creates visual status indicators** perfect for dashboards and reports
4. **🧠 Smart height calculation** ensures optimal table sizing without manual adjustment

## Quick Start

```yaml
---
layout: Table Only
title: "Project Status Dashboard"
cell_color_mode: auto              # Enable per-cell color detection
table_data: |
  | Project | Backend | Frontend | Testing | Deployment |
  | Alpha   | GREEN   | GREEN    | YELLOW  | RED        |
  | Beta    | BLUE    | BLUE     | BLUE    | BLUE       |
  | Gamma   | LIME    | LIME     | GREEN   | DARKGREEN  |
---
```

This creates a visual status grid where each status shows as a colored block.

## Configuration Options

### Cell Color Mode

Control per-cell color detection with `cell_color_mode`:

```yaml
cell_color_mode: auto      # Default - detect colors automatically
cell_color_mode: enabled   # Force enable (same as auto)
cell_color_mode: disabled  # Turn off color detection completely
```

### Available Status Colors

All 140 HTML color names work. Popular choices for status tables:

**Status Indicators:**
- `GREEN` / `LIME` / `DARKGREEN` - Success, completed, positive
- `RED` / `DARKRED` / `CRIMSON` - Error, failed, critical
- `YELLOW` / `GOLD` / `ORANGE` - Warning, in progress, moderate
- `BLUE` / `NAVY` / `LIGHTBLUE` - Information, planned, neutral

**Extended Palette:**
- `PURPLE` / `VIOLET` / `MAGENTA` - Special status, review needed
- `GRAY` / `SILVER` / `LIGHTGRAY` - Inactive, disabled, N/A
- `TRANSPARENT` - Empty cells, spacers, hidden content

## Example Patterns

### Project Status Dashboard

```yaml
---
layout: Table Only
title: "Q4 Project Status"
style: dark_blue_white_text
row_style: solid_white
border_style: thin_gray
cell_color_mode: auto
table_data: |
  | Project | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Overall |
  | Website Redesign | GREEN | GREEN | YELLOW | RED | YELLOW |
  | Mobile App | GREEN | GREEN | GREEN | GREEN | GREEN |
  | API Integration | BLUE | BLUE | BLUE | GRAY | BLUE |
  | Analytics Platform | GREEN | YELLOW | RED | GRAY | RED |
  | Security Audit | GREEN | GREEN | GREEN | YELLOW | GREEN |
---
```

### Performance Metrics Grid

```yaml
---
layout: Table with Content Above
title: "System Performance Dashboard"
content: "Real-time system health indicators updated every 5 minutes"
cell_color_mode: auto
custom_colors:
  header_bg: darkblue
  header_text: white
  primary_row: transparent
table_data: |
  | Service | CPU | Memory | Disk | Network | Status |
  | Web Server | GREEN | GREEN | YELLOW | GREEN | GREEN |
  | Database | YELLOW | RED | GREEN | GREEN | YELLOW |
  | Cache | GREEN | GREEN | GREEN | GREEN | GREEN |
  | API Gateway | GREEN | YELLOW | GREEN | BLUE | YELLOW |
  | Load Balancer | GREEN | GREEN | GREEN | GREEN | GREEN |
---
```

### Team Workload Status

```yaml
---
layout: Table Only
title: "Team Capacity & Workload"
cell_color_mode: auto
table_data: |
  | Team Member | Mon | Tue | Wed | Thu | Fri | Weekend |
  | Alice Johnson | GREEN | GREEN | YELLOW | YELLOW | RED | TRANSPARENT |
  | Bob Chen | BLUE | BLUE | BLUE | GREEN | GREEN | TRANSPARENT |
  | Carol Davis | GREEN | YELLOW | RED | RED | YELLOW | TRANSPARENT |
  | David Wilson | LIME | LIME | LIME | GREEN | GREEN | GRAY |
  | Eva Martinez | YELLOW | YELLOW | GREEN | GREEN | BLUE | TRANSPARENT |
---
```

### Financial Health Matrix

```yaml
---
layout: Table Only
title: "Q3 Financial Performance"
style: white_dark_text
cell_color_mode: auto
custom_colors:
  header_bg: navy
  header_text: white
table_data: |
  | Department | Revenue | Costs | Profit | Trend | Forecast |
  | Sales | GREEN | GREEN | GREEN | LIME | GREEN |
  | Marketing | YELLOW | RED | YELLOW | ORANGE | YELLOW |
  | Engineering | BLUE | YELLOW | BLUE | LIGHTBLUE | BLUE |
  | Operations | GREEN | GREEN | GREEN | DARKGREEN | GREEN |
  | Support | GRAY | GREEN | GRAY | SILVER | GRAY |
---
```

## Advanced Techniques

### Mixed Content with Status Indicators

Combine regular text with color-coded status cells:

```yaml
table_data: |
  | Task Description | Assigned To | Due Date | Priority | Status |
  | Setup CI/CD Pipeline | DevOps Team | 2024-03-15 | HIGH | GREEN |
  | Database Migration | Backend Team | 2024-03-20 | CRITICAL | YELLOW |
  | UI/UX Review | Design Team | 2024-03-10 | MEDIUM | RED |
  | Security Testing | QA Team | 2024-03-25 | HIGH | BLUE |
```

Only the "Status" column gets colored - other columns remain normal text.

### Invisible Text Effect for Clean Design

The invisible text effect (text color = background color) creates clean visual blocks:

```yaml
table_data: |
  | Metric | Q1 | Q2 | Q3 | Q4 |
  | Revenue Growth | GREEN | GREEN | YELLOW | RED |
  | Customer Satisfaction | LIME | LIME | LIME | GREEN |
  | Market Share | BLUE | LIGHTBLUE | CYAN | DARKBLUE |
```

Viewers see colored blocks but can still copy/select the text for data export.

### Transparent Spacers and Sections

Use `TRANSPARENT` for visual spacing and grouping:

```yaml
table_data: |
  | Category | Item 1 | Item 2 | Item 3 |
  | Frontend | GREEN | YELLOW | RED |
  | TRANSPARENT | TRANSPARENT | TRANSPARENT | TRANSPARENT |
  | Backend | BLUE | BLUE | GREEN |
  | TRANSPARENT | TRANSPARENT | TRANSPARENT | TRANSPARENT |
  | DevOps | LIME | GREEN | YELLOW |
```

## Color Psychology for Status Tables

### Universal Status Colors

- **🟢 GREEN family**: Success, completed, positive, go
- **🔴 RED family**: Error, failed, critical, stop
- **🟡 YELLOW/ORANGE family**: Warning, in progress, caution
- **🔵 BLUE family**: Information, planned, neutral, future

### Extended Status System

- **🟣 PURPLE**: Review needed, special attention, VIP
- **⚫ GRAY**: Inactive, disabled, not applicable, archived
- **⚪ TRANSPARENT**: Hidden, spacer, group separator

### Professional Color Schemes

**Corporate Status (Conservative):**
- `DARKGREEN`, `RED`, `ORANGE`, `NAVY`, `GRAY`

**Tech Dashboard (Modern):**
- `LIME`, `CRIMSON`, `GOLD`, `CYAN`, `SILVER`

**Health/Safety (High Contrast):**
- `GREEN`, `DARKRED`, `YELLOW`, `BLUE`, `BLACK`

## Best Practices

### 1. Consistent Color Meaning
Always use the same colors for the same meanings across all tables:
- GREEN = Good/Complete
- RED = Bad/Failed  
- YELLOW = Warning/In Progress
- BLUE = Information/Planned

### 2. Accessibility Considerations
- Use high contrast color combinations
- Include text labels when possible
- Test with colorblind-friendly palettes
- Provide legend or key when needed

### 3. Layout Optimization
```yaml
# Good: Dedicated status columns
| Task | Owner | Status | Priority |

# Better: Multiple status dimensions  
| Task | Owner | Backend | Frontend | Testing |
```

### 4. Performance Tips
- Use `cell_color_mode: disabled` for large tables that don't need colors
- Combine with transparent backgrounds for overlay effects
- Consider column width optimization for status indicators

## Troubleshooting

### Colors Not Appearing
```yaml
# Ensure cell_color_mode is enabled
cell_color_mode: auto

# Check color name spelling (case insensitive)
| Status |
| GREEN |  # ✅ Works
| Green |  # ✅ Works  
| green |  # ✅ Works
| GREAN |  # ❌ Typo - won't work
```

### Mixed Text and Colors
```yaml
# Only exact color name matches get colored
| Status |
| GREEN COMPLETED |     # ❌ Won't color (extra text)
| GREEN |              # ✅ Will color
| Status: GREEN |      # ❌ Won't color (extra text)
```

### Invisible Text Issues
If text becomes completely invisible:
- Check that `cell_color_mode` isn't conflicting with other settings
- Use `TRANSPARENT` for truly transparent cells instead
- Consider using contrasting text colors for accessibility

## Integration Examples

### With Content Above
```yaml
---
layout: Table with Content Above
title: "Sprint Review Dashboard"
content: |
  **Sprint 23 Results** - All user stories completed successfully
  
  Key achievements:
  • 95% test coverage maintained
  • Zero critical bugs in production
  • Customer satisfaction score: 4.8/5

cell_color_mode: auto
table_data: |
  | Epic | Stories | Testing | Deployment | Status |
  | User Authentication | GREEN | GREEN | GREEN | GREEN |
  | Payment Integration | GREEN | YELLOW | RED | YELLOW |
  | Analytics Dashboard | BLUE | BLUE | GRAY | BLUE |
---
```

### With Charts and Metrics
Combine status tables with other content types for comprehensive dashboards.

## Next Steps

- See [Table Styling Guide](./table-styling.md) for general table customization
- Check [HTML Colors Reference](../reference/html-colors.html) for complete color list
- View [Template Patterns](../reference/frontmatter-patterns.md) for layout options

Status tables transform static data into dynamic visual dashboards perfect for presentations, reports, and real-time monitoring displays.