# Supported Templates Specification

This document tracks the implementation status of PowerPoint templates and layouts in the deck-builder-mcp system.

## Currently Implemented (Default Template)

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ✅ | Title Slide | Opening slide with title and subtitle | Title 1, Subtitle 2 |
| ✅ | Title and Content | Standard slide with title and bulleted content | Title 1, Content Placeholder 2 |
| ✅ | Section Header | Divider slide between presentation sections | Title 1, Text Placeholder 2 |
| ✅ | Two Content | Side-by-side content areas | Title 1, Content Placeholder 2, Content Placeholder 3 |
| ✅ | Comparison | Left vs right comparison layout | Title 1, Text Placeholder 2, Content Placeholder 3, Text Placeholder 4, Content Placeholder 5 |
| ✅ | Title Only | Minimal slide with just title | Title 1 |
| ✅ | Blank | Empty slide for custom content | (none - just footer elements) |
| ✅ | Content with Caption | Content area with descriptive text | Title 1, Content Placeholder 2, Text Placeholder 3 |
| ✅ | Picture with Caption | Image-focused slide with caption | Title 1, Picture Placeholder 2, Text Placeholder 3 |
| ✅ | Title and Vertical Text | Title with vertically oriented text | Title 1, Vertical Text Placeholder 2 |
| ✅ | Vertical Title and Text | Both title and text vertically oriented | Vertical Title 1, Vertical Text Placeholder 2 |
| ✅ | Four Columns | Quad content areas with titles | Title 1, Col 1-4 Title/Text Placeholders |

## Content Structure Layouts

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ✅ | Title Slide | Title, subtitle, presenter info | Title 1, Subtitle 2 |
| ✅ | Section Header | Divider slides between topics | Title 1, Text Placeholder 2 |
| ✅ | Title and Content | Traditional bulleted lists | Title 1, Content Placeholder 2 |
| ✅ | Two Content | Side-by-side content areas | Title 1, Content Placeholder 2, Content Placeholder 3 |
| ✅  | Three Column | Triple content areas | Col 1-3 Title/Text Placeholders |
| ✅  | Three Column With Titles | Triple content areas | Title 1, Content Placeholder 2-4 |
| ✅ | Four Columns With Titles | Quad content areas | Title 1, Col 1-4 Title/Text Placeholders |
| ✅ | Four Columns| Quad content areas | Title 1, Col 1-4 Text Placeholders |
| ✅ | Blank | Minimal structure for custom content | (none) |

## Comparison & Analysis

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ✅ | Comparison | Side-by-side contrasts (vs, before/after) | Title 1, Text Placeholder 2, Content Placeholder 3, Text Placeholder 4, Content Placeholder 5 |
| ❌ | Pros & Cons | Advantages/disadvantages layout | Title 1, Pros Header, Pros Content, Cons Header, Cons Content |
| ✅ | SWOT Analysis | Strengths/Weaknesses/Opportunities/Threats | Title 1, 4 SWOT Quadrant Placeholders |
| ❌ | Gap Analysis | Current state vs desired state | Title 1, Current State, Desired State, Gap Content |
| ❌ | Feature Matrix | Comparison table format | Title 1, Table Placeholder |

## Data & Metrics

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ✅  | Big Number | Prominent metric display | Title 1, Big Number Placeholder, Context Text |
| ❌ | KPI Dashboard | Multiple metrics grid | Title 1, KPI Grid Placeholders |
| ❌ | Chart Slide | Graph with supporting text | Title 1, Chart Placeholder, Supporting Text |
| ❌ | Data Table | Structured data presentation | Title 1, Table Placeholder |
| ❌ | Progress Tracker | Status indicators | Title 1, Progress Bar Placeholders |
| ❌ | Scorecard | Performance metrics | Title 1, Metric Placeholders |

## Process & Flow

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ❌ | Timeline | Chronological events | Title 1, Timeline Content Placeholders |
| ❌ | Process Flow | Sequential steps | Title 1, Step Placeholders |
| ✅  | Title and 6-item Lists | 6 step process | Title 1, 1-6 Action Item Title and Conent Placeholders |
| ❌ | Workflow | Decision trees/flowcharts | Title 1, Workflow Diagram Placeholder |
| ❌ | Roadmap | Future planning timeline | Title 1, Roadmap Content Placeholders |
| ❌ | Journey Map | User/customer experience flow | Title 1, Journey Stage Placeholders |
| ❌ | Funnel | Conversion/sales process | Title 1, Funnel Stage Placeholders |

## Visual & Media

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ✅ | Picture with Caption | Image-focused with description | Title 1, Picture Placeholder 2, Text Placeholder 3 |
| ❌ | Image Gallery | Multiple images | Title 1, Image Placeholders |
| ❌ | Video Slide | Embedded media | Title 1, Video Placeholder |
| ❌ | Infographic | Data visualization | Title 1, Infographic Placeholder |
| ❌ | Icon Grid | Visual concept representation | Title 1, Icon Grid Placeholders |

## Business Specific

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ❌ | Problem-Solution | Issue identification + resolution | Title 1, Problem Content, Solution Content |
| ❌ | Executive Summary | High-level overview | Title 1, Summary Content Placeholders |
| ❌ | Financial Summary | Revenue/costs/projections | Title 1, Financial Data Placeholders |
| ❌ | Team Introduction | People profiles | Title 1, Team Member Placeholders |
| ❌ | Product Showcase | Feature highlights | Title 1, Product Feature Placeholders |
| ❌ | Case Study | Success story format | Title 1, Case Study Content Placeholders |
| ❌ | Testimonial | Customer feedback | Title 1, Quote Placeholder, Attribution |
| ❌ | Call to Action | Next steps/decision points | Title 1, CTA Content, Action Items |

## Strategic & Planning

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ❌ | Vision Statement | Company direction | Title 1, Vision Content |
| ❌ | Strategic Objectives | Goals breakdown | Title 1, Objective Placeholders |
| ❌ | Initiative Overview | Project summary | Title 1, Initiative Content Placeholders |
| ❌ | Resource Allocation | Budget/staffing | Title 1, Resource Content Placeholders |
| ❌ | Risk Assessment | Threat analysis | Title 1, Risk Content Placeholders |
| ❌ | Success Metrics | KPI definitions | Title 1, Metrics Content Placeholders |

## Meeting & Workshop

| Supported | Name | Description | Required Placeholders |
|-----------|------|-------------|----------------------|
| ❌ | Agenda | Meeting structure | Title 1, Agenda Items |
| ✅ | Agenda, 6 Textboxes | Meeting structure | Title 1, 6 Agenda Item placeholders |
| ❌ | Discussion Points | Topics for conversation | Title 1, Discussion Content |
| ❌ | Action Items | Task assignments | Title 1, Action Item Placeholders |


| ❌ | Decision Matrix | Options evaluation | Title 1, Decision Content |
| ❌ | Parking Lot | Deferred items | Title 1, Parking Lot Content |
| ❌ | Next Steps | Follow-up actions | Title 1, Next Steps Content |

## Implementation Status Summary

- **Implemented**: 12 layouts from default template
- **Planned**: 50+ additional layouts across business categories
- **Priority**: Content-first MCP tools can recommend appropriate layouts
- **Extensibility**: New layouts can be added by extending template JSON files

## Notes

- All layouts include standard footer elements: Date Placeholder, Footer Placeholder, Slide Number Placeholder
- Placeholder names correspond to PowerPoint template structure
- Structured frontmatter system provides human-readable YAML interface
- Content-first MCP tools will recommend optimal layouts based on user content and goals
