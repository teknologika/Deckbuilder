# Supported Templates Specification

This document tracks the implementation status of PowerPoint templates and layouts in the deck-builder-mcp system.


## Content Structure Layouts

| Supported | Name                     | Description                          | Required Placeholders                                 | Pattern File                                                                                                        |
| --------- | ------------------------ | ------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| ✅         | Title Slide              | Title, subtitle, presenter info      | Title 1, Subtitle 2                                   | [title_slide.json](../src/deckbuilder/structured_frontmatter_patterns/title_slide.json)                             |
| ✅         | Section Header           | Divider slides between topics        | Title 1, Text Placeholder 2                           | [section_header.json](../src/deckbuilder/structured_frontmatter_patterns/section_header.json)                       |
| ✅         | Title and Content        | Traditional bulleted lists           | Title 1, Content Placeholder 2                        | [title_and_content.json](../src/deckbuilder/structured_frontmatter_patterns/title_and_content.json)                 |
| ✅         | Two Content              | Side-by-side content areas           | Title 1, Content Placeholder 2, Content Placeholder 3 | [two_content.json](../src/deckbuilder/structured_frontmatter_patterns/two_content.json)                             |
| ✅         | Three Column             | Triple content areas                 | Title 1, Content Placeholder 2-4                      | [three_columns.json](../src/deckbuilder/structured_frontmatter_patterns/three_columns.json)                         |
| ✅         | Three Column With Titles | Triple content areas                 | Title 1, Col 1-3 Title/Text Placeholders              | [three_columns_with_titles.json](../src/deckbuilder/structured_frontmatter_patterns/three_columns_with_titles.json) |
| ✅         | Four Columns With Titles | Quad content areas                   | Title 1, Col 1-4 Title/Text Placeholders              | [four_columns_with_titles.json](../src/deckbuilder/structured_frontmatter_patterns/four_columns_with_titles.json)   |
| ✅         | Four Columns             | Quad content areas                   | Title 1, Col 1-4 Text Placeholders                    | [four_columns.json](../src/deckbuilder/structured_frontmatter_patterns/four_columns.json)                           |
| ✅         | Blank                    | Minimal structure for custom content | (none)                                                |

## Comparison & Analysis

| Supported | Name             | Description                                | Required Placeholders                                                                         | Pattern File                                                                                      |
| --------- | ---------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ✅         | Comparison       | Side-by-side contrasts (vs, before/after)  | Title 1, Text Placeholder 2, Content Placeholder 3, Text Placeholder 4, Content Placeholder 5 | [comparison.json](../src/deckbuilder/structured_frontmatter_patterns/comparison.json)             |
| ✅         | Pros & Cons      | Advantages/disadvantages layout            | Title 1, Left Title, Left Content, Right Title, Right Content                                 | [pros_and_cons.json](../src/deckbuilder/structured_frontmatter_patterns/pros_and_cons.json)       |
| ✅         | Before & After   | Transformation comparison layout           | Title 1, Left Title, Left Content, Right Title, Right Content                                 | [before_and_after.json](../src/deckbuilder/structured_frontmatter_patterns/before_and_after.json) |
| ✅         | Problem Solution | Issue identification + resolution          | Title 1, Left Content, Right Content                                                          | [problem_solution.json](../src/deckbuilder/structured_frontmatter_patterns/problem_solution.json) |
| ✅         | SWOT Analysis    | Strengths/Weaknesses/Opportunities/Threats | Title 1, 4 SWOT Quadrant Placeholders                                                         | [swot_analysis.json](../src/deckbuilder/structured_frontmatter_patterns/swot_analysis.json)       |
| ❌         | Gap Analysis     | Current state vs desired state             | Title 1, Current State, Desired State, Gap Content                                            | *Use before_and_after.json*                                                                       |
| ❌         | Feature Matrix   | Comparison table format                    | Title 1, Table Placeholder                                                                    | *Use title_and_content.json with table*                                                           |

## Data & Metrics

| Supported | Name             | Description                  | Required Placeholders                         | Pattern File                                                                            |
| --------- | ---------------- | ---------------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------- |
| ✅         | Big Number       | Prominent metric display     | Title 1, Big Number Placeholder, Context Text | [big_number.json](../src/deckbuilder/structured_frontmatter_patterns/big_number.json)   |
| ✅         | Key Metrics      | Multiple KPIs display        | Title 1, 4 Metric Content Areas               | [key_metrics.json](../src/deckbuilder/structured_frontmatter_patterns/key_metrics.json) |
| ❌         | KPI Dashboard    | Multiple metrics grid        | Title 1, KPI Grid Placeholders                | *Use key_metrics.json*                                                                  |
| ❌         | Chart Slide      | Graph with supporting text   | Title 1, Chart Placeholder, Supporting Text   | *Use picture_with_caption.json*                                                         |
| ❌         | Data Table       | Structured data presentation | Title 1, Table Placeholder                    | *Use table layout options below*                                                        |
| ❌         | Progress Tracker | Status indicators            | Title 1, Progress Bar Placeholders            | *Use four_columns.json*                                                                 |
| ❌         | Scorecard        | Performance metrics          | Title 1, Metric Placeholders                  | *Use key_metrics.json*                                                                  |

## Table Layouts

| Supported | Name                                | Description                                      | Required Placeholders                                                                    | Pattern File                                                                                                                      |
| --------- | ----------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| ✅         | Table Only                          | Pure data presentation                           | Title 1, Table Data                                                                     | [table_only.json](../src/deckbuilder/structured_frontmatter_patterns/table_only.json)                                           |
| ✅         | Table with Content Above            | Context explanation + data table                | Title 1, Content, Table Data                                                            | [table_with_content_above.json](../src/deckbuilder/structured_frontmatter_patterns/table_with_content_above.json)               |
| ✅         | Table with Content Above and Below  | Context + data + conclusions                     | Title 1, Content Above, Table Data, Content Below                                       | [table_with_content_above_and_below.json](../src/deckbuilder/structured_frontmatter_patterns/table_with_content_above_and_below.json) |
| ✅         | Table with Content Left             | Side-by-side analysis and data                   | Title 1, Content Left, Table Data                                                       | [table_with_content_left.json](../src/deckbuilder/structured_frontmatter_patterns/table_with_content_left.json)                 |
| ✅         | Content Table Content Table Content | Complex multi-dataset presentations              | Title 1, Content 1, Table Data 1, Content 2, Table Data 2, Content 3                  | [content_table_content_table_content.json](../src/deckbuilder/structured_frontmatter_patterns/content_table_content_table_content.json) |

**Table Styling Options** (available for all table layouts):
- `style`: Header style (dark_blue_white_text, light_blue_dark_text, etc.)
- `row_style`: Row style (alternating_light_gray, solid_white, etc.)  
- `border_style`: Border style (thin_gray, thick_gray, no_borders, etc.)
- `row_height`: Row height in cm (default: 0.6)
- `table_width`: Table width in cm (auto-calculated from columns if not set)
- `column_widths`: Array of column widths in cm
- `header_font_size`: Header font size in points (default: 12)
- `data_font_size`: Data font size in points (default: 10)
- `custom_colors`: Custom color overrides

## Process & Flow

| Supported | Name                   | Description                   | Required Placeholders                 | Pattern File                                                                                                  |
| --------- | ---------------------- | ----------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| ✅         | Timeline               | Chronological events          | Title 1, Content                      | [timeline.json](../src/deckbuilder/structured_frontmatter_patterns/timeline.json)                             |
| ✅         | Process Steps          | Sequential 4-step process     | Title 1, 4 Step Content Areas         | [process_steps.json](../src/deckbuilder/structured_frontmatter_patterns/process_steps.json)                   |
| ✅         | Title and 6-item Lists | 6 step process                | Title 1, 6 Action Item Placeholders   | [title_and_6_item_lists.json](../src/deckbuilder/structured_frontmatter_patterns/title_and_6_item_lists.json) |
| ❌         | Workflow               | Decision trees/flowcharts     | Title 1, Workflow Diagram Placeholder | *Use picture_with_caption.json*                                                                               |
| ❌         | Roadmap                | Future planning timeline      | Title 1, Roadmap Content Placeholders | *Use timeline.json*                                                                                           |
| ❌         | Journey Map            | User/customer experience flow | Title 1, Journey Stage Placeholders   | *Use process_steps.json*                                                                                      |
| ❌         | Funnel                 | Conversion/sales process      | Title 1, Funnel Stage Placeholders    | *Use picture_with_caption.json*                                                                               |

## Visual & Media

| Supported | Name                 | Description                    | Required Placeholders                              | Pattern File                                                                                              |
| --------- | -------------------- | ------------------------------ | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ✅         | Picture with Caption | Image-focused with description | Title 1, Picture Placeholder 2, Text Placeholder 3 | [picture_with_caption.json](../src/deckbuilder/structured_frontmatter_patterns/picture_with_caption.json) |
| ❌         | Image Gallery        | Multiple images                | Title 1, Image Placeholders                        | *Use picture_with_caption.json*                                                                           |
| ❌         | Video Slide          | Embedded media                 | Title 1, Video Placeholder                         | *Use picture_with_caption.json*                                                                           |
| ❌         | Infographic          | Data visualization             | Title 1, Infographic Placeholder                   | *Use picture_with_caption.json*                                                                           |
| ❌         | Icon Grid            | Visual concept representation  | Title 1, Icon Grid Placeholders                    | *Use four_columns.json*                                                                                   |

## Business Specific

| Supported | Name              | Description                       | Required Placeholders                    | Pattern File                                                                                      |
| --------- | ----------------- | --------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ✅         | Problem-Solution  | Issue identification + resolution | Title 1, Left Content, Right Content     | [problem_solution.json](../src/deckbuilder/structured_frontmatter_patterns/problem_solution.json) |
| ✅         | Team Introduction | People profiles                   | Title 1, 4 Team Member Areas             | [team_members.json](../src/deckbuilder/structured_frontmatter_patterns/team_members.json)         |
| ❌         | Executive Summary | High-level overview               | Title 1, Summary Content Placeholders    | *Use title_and_content.json*                                                                      |
| ❌         | Financial Summary | Revenue/costs/projections         | Title 1, Financial Data Placeholders     | *Use key_metrics.json*                                                                            |
| ❌         | Product Showcase  | Feature highlights                | Title 1, Product Feature Placeholders    | *Use four_columns.json*                                                                           |
| ❌         | Case Study        | Success story format              | Title 1, Case Study Content Placeholders | *Use title_and_content.json*                                                                      |
| ❌         | Testimonial       | Customer feedback                 | Title 1, Quote Placeholder, Attribution  | *Use title_and_content.json*                                                                      |
| ❌         | Call to Action    | Next steps/decision points        | Title 1, CTA Content, Action Items       | *Use title_and_content.json*                                                                      |

## Strategic & Planning

| Supported | Name                 | Description       | Required Placeholders                    | Pattern File                     |
| --------- | -------------------- | ----------------- | ---------------------------------------- | -------------------------------- |
| ❌         | Vision Statement     | Company direction | Title 1, Vision Content                  | *Use title_and_content.json*     |
| ❌         | Strategic Objectives | Goals breakdown   | Title 1, Objective Placeholders          | *Use four_columns.json*          |
| ❌         | Initiative Overview  | Project summary   | Title 1, Initiative Content Placeholders | *Use title_and_content.json*     |
| ❌         | Resource Allocation  | Budget/staffing   | Title 1, Resource Content Placeholders   | *Use key_metrics.json*           |
| ❌         | Risk Assessment      | Threat analysis   | Title 1, Risk Content Placeholders       | *Use swot_analysis.json*         |
| ❌         | Success Metrics      | KPI definitions   | Title 1, Metrics Content Placeholders    | *Use key_metrics.json*           |

## Meeting & Workshop

| Supported | Name                | Description             | Required Placeholders               | Pattern File                                                                                                      |
| --------- | ------------------- | ----------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| ❌         | Agenda              | Meeting structure       | Title 1, Agenda Items               | *Use title_and_content.json*                                                                                      |
| ✅         | Agenda, 6 Textboxes | Meeting structure       | Title 1, 6 Agenda Item placeholders | [agenda_6_textboxes.json](../src/deckbuilder/structured_frontmatter_patterns/agenda_6_textboxes.json)             |
| ❌         | Discussion Points   | Topics for conversation | Title 1, Discussion Content         | *Use title_and_content.json*                                                                                      |
| ❌         | Action Items        | Task assignments        | Title 1, Action Item Placeholders   | *Use title_and_content.json*                                                                                      |
| ❌         | Decision Matrix     | Options evaluation      | Title 1, Decision Content           | *Use comparison.json*                                                                                             |
| ❌         | Parking Lot         | Deferred items          | Title 1, Parking Lot Content       | *Use title_and_content.json*                                                                                      |
| ❌         | Next Steps          | Follow-up actions       | Title 1, Next Steps Content        | *Use title_and_content.json*                                                                                      |

## Implementation Status Summary

- **Native PowerPoint Layouts**: 24 layouts with dedicated JSON patterns
- **Table Layouts**: 5 dedicated table presentation layouts (NEW)
- **Content Layouts**: 19 standard presentation layouts
- **Semantic Aliases**: 7 additional user-friendly discovery patterns
- **Total Discoverable**: 31 layout options for users
- **Achievable Variations**: 45+ layouts using existing patterns with guidance
- **Template Coverage**: 100% of PowerPoint template layouts implemented
- **Table Handling**: Template-based approach eliminates complex content splitting
- **Priority**: Content-first MCP tools can recommend appropriate layouts
- **Extensibility**: New layouts added via JSON patterns + PowerPoint templates

## Notes

- All layouts include standard footer elements: Date Placeholder, Footer Placeholder, Slide Number Placeholder
- Placeholder names correspond to PowerPoint template structure
- Structured frontmatter system provides human-readable YAML interface
- Content-first MCP tools will recommend optimal layouts based on user content and goals
