# Deck Builder MCP

## Overview

The Deck Builder MCP is a Model Context Protocol (MCP) server that enables AI assistants to programmatically create and manipulate PowerPoint presentations. Built with Python and FastMCP, this server provides a comprehensive set of tools for generating professional presentations with multiple slide types, custom styling, and template support.

The server solves the common challenge of automating presentation creation by offering both JSON and markdown interfaces for defining slide content and structure. Users can choose between precise JSON control or intuitive markdown authoring with YAML frontmatter. It's particularly useful for generating reports, dashboards, and structured presentations from data or user specifications.

**Technology Stack:**
- **Backend Framework:** FastMCP (Model Context Protocol)
- **Presentation Engine:** python-pptx
- **Content Parsing:** PyYAML for frontmatter, custom markdown parser
- **Transport:** stdio/SSE
- **Language:** Python 3.x
- **Configuration:** Environment variables with .env support

## Features

- **Multiple Input Formats:** Support for both JSON and Markdown with YAML frontmatter
- **Rich Content Support:** Mixed content with headings, paragraphs, and bullet points
- **Inline Formatting:** Full support for bold, italic, underline, and combined formatting within text
- **Multiple Slide Types:** Support for title slides, content slides, and data tables
- **Template-Based Generation:** Use custom PowerPoint templates or default layouts
- **JSON Configuration:** Define presentations using structured JSON data
- **Markdown Authoring:** Create presentations using familiar markdown syntax with frontmatter
- **Custom Table Styling:** Advanced table formatting with predefined styles and color overrides
- **Intelligent File Naming:** ISO timestamp format with `.g.pptx` extension for generated files
- **Environment Configuration:** Flexible setup through environment variables
- **Singleton Pattern:** Efficient memory management for presentation objects
- **Async Support:** Full asynchronous operation for better performance
- **Multiple Transport Options:** Support for both stdio and SSE transports

## Prerequisites

### Development Environment

- **Python 3.8+** with pip package manager
- **Virtual environment** (recommended for dependency isolation)
- **Claude Desktop** or another MCP-compatible client
- **PowerPoint templates** (optional, default template included)

### Required Python Dependencies

```bash
pip install python-pptx fastmcp python-dotenv pyyaml
```

### Directory Structure Setup

The server uses environment variables to configure file paths:

```bash
# Create required directories
mkdir -p ~/Documents/Deckbuilder/Templates
mkdir -p ~/Documents/Deckbuilder
```

## Installation & Configuration

1. **Clone the repository:**
```bash
git clone <repository-url>
cd deck-builder-mcp
```

2. **Set up virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the server (for testing):**
```bash
./run_server.sh
```

5. **Configure Claude Desktop:**

Add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "/path/to/deck-builder-mcp/venv/bin/python",
      "args": ["/path/to/deck-builder-mcp/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "DECK_TEMPLATE_FOLDER": "/Users/username/Documents/Deckbuilder/Templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/Users/username/Documents/Deckbuilder"
      }
    }
  }
}
```

## Design Approach

This project follows a **content-first design philosophy** that prioritizes user communication goals over template constraints. The architecture consists of three key design patterns:

### Feature Documentation
- **[Placeholder Matching](docs/Features/PlaceholderMatching.md)**: Hybrid semantic detection and JSON mapping system for reliable content placement
- **[Template Discovery](docs/Features/TemplateDiscovery.md)**: Content-first MCP tools for intelligent presentation consulting  
- **[Supported Templates](docs/Features/SupportedTemplates.md)**: Progressive implementation roadmap for 50+ business presentation layouts

### Design Philosophy

**Content-First Intelligence**: Instead of asking "what layouts exist?", the system asks "what does the user want to communicate?" This approach transforms the LLM from a layout picker into an intelligent presentation consultant.

**Separation of Concerns**: Technical template structure (`default.json`) remains separate from semantic content intelligence (`layout_intelligence.json`), enabling independent evolution of both systems.

**Progressive Enhancement**: Start with user content analysis, recommend optimal presentation structure, then provide layout-specific optimization - ensuring every step adds value to the communication goal.

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────────────────────────┐    ┌─────────────────┐
│   MCP Client    │    │           Deck Builder               │    │   PowerPoint    │
│  (Claude, etc.) │◄──►│          MCP Server                  │◄──►│     Files       │
└─────────────────┘    └──────────────────────────────────────┘    └─────────────────┘
                                           │
                       ┌───────────────────┼───────────────────┐
                       ▼                   ▼                   ▼
              ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
              │  Content-First  │ │   Template      │ │   Structured    │
              │   MCP Tools     │ │   Management    │ │   Frontmatter   │
              │                 │ │                 │ │                 │
              │ • analyze_      │ │ • Semantic      │ │ • YAML Parser   │
              │   presentation_ │ │   Detection     │ │ • Layout        │
              │   needs()       │ │ • JSON Mapping  │ │   Mapping       │
              │ • recommend_    │ │ • Template      │ │ • Content       │
              │   slide_        │ │   Loading       │ │   Optimization  │
              │   approach()    │ │                 │ │                 │
              │ • optimize_     │ │                 │ │                 │
              │   content_for_  │ │                 │ │                 │
              │   layout()      │ │                 │ │                 │
              └─────────────────┘ └─────────────────┘ └─────────────────┘
                       │                   │                   │
                       └───────────────────┼───────────────────┘
                                           ▼
                              ┌─────────────────────┐
                              │ Layout Intelligence │
                              │                     │
                              │ • Content Triggers  │
                              │ • Semantic Tags     │
                              │ • Audience Analysis │
                              │ • Use Case Examples │
                              └─────────────────────┘
```

**Key Components:**

**Core Engine:**
- **FastMCP Server:** Handles MCP protocol communication and tool orchestration
- **Deckbuilder Class:** Core presentation management with singleton pattern

**Content Intelligence Layer:**
- **Content-First MCP Tools:** Analyze user needs and recommend optimal layouts (🚧 In Design)
- **Layout Intelligence:** Semantic content matching with `layout_intelligence.json` (🚧 Planned)
- **Structured Frontmatter:** Clean YAML syntax with automatic PowerPoint mapping (✅ Implemented)

**Template System:**
- **Semantic Detection:** Automatic placeholder identification using PowerPoint types
- **JSON Mapping:** Custom layout configuration for advanced templates
- **Template Loading:** Dynamic template and configuration management

**Content Processing:**
- **Hybrid Placement:** Semantic detection + JSON mapping for reliable content placement
- **YAML Parser:** Converts structured frontmatter to presentation elements
- **Content Optimization:** 64% complexity reduction through render-time formatting

## Project Components

### Core Files

**`src/main.py`** - MCP Server Implementation
- FastMCP server setup with lifecycle management
- Tool definitions for presentation operations
- Async context management for the Deckbuilder client
- Transport configuration (stdio/SSE support)

**`src/deckbuilder.py`** - Presentation Engine
- Singleton Deckbuilder class for presentation management
- PowerPoint template handling and slide creation
- JSON and markdown parsing with frontmatter support
- Rich content rendering (headings, paragraphs, bullets)
- File versioning and output management
- Clean formatting without extra blank lines

**`src/table_styles.py`** - Table styling definitions
- Predefined header, row, and border styles for tables
- Color schemes and formatting options

**`src/slide_layouts.py`** - Slide layout mappings
- Default PowerPoint layout configurations
- Layout type to template index mappings

**`run_server.sh`** - Server startup script
- Virtual environment activation and server launch
- Convenient development and testing script

### Available MCP Tools

1. **`create_presentation`** - Create complete PowerPoint presentations from JSON data with automatic saving
2. **`create_presentation_from_markdown`** - Create complete presentations from markdown with frontmatter and automatic saving

The server provides a streamlined interface with just two comprehensive tools that handle complete presentation workflows, eliminating the need for multiple tool calls.

### Configuration Files

- **`CLAUDE.md`** - Development guidelines for AI assistants
- **`.gitignore`** - Git ignore patterns including MCP and Claude configs
- **`table-styles.css/html`** - Table styling reference documentation

## Usage Examples

### Markdown with Frontmatter (Recommended)

Create presentations using familiar markdown syntax with YAML frontmatter for layout control:

```markdown
---
layout: title
---
# AI-Powered Business Solutions
## Transforming Your Workflow in 2024

---
layout: content
---
# Key Benefits

## Performance Improvements
Our platform delivers ***significant improvements*** across all key metrics with **proven results**.

- ***Efficiency Gains:*** **40% reduction** in routine task completion time
- ***Quality Improvement:*** **68% fewer errors** through AI-assisted workflows  
- ***Cost Savings:*** Average **25% reduction** in ___operational expenses___
- ***Scalability:*** Solutions that ***automatically scale*** based on demand

The system provides *real-time monitoring* and **24/7 support** to ensure ___optimal performance___ at all times.

## Implementation Timeline
We can have your system up and running in just 2 weeks.

- Week 1: Setup and configuration
- Week 2: Training and go-live support

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
---
# Performance Metrics
| Metric | Before | After | Improvement |
| Response Time | 2.5s | 0.8s | 68% faster |
| Error Rate | 5.2% | 1.1% | 79% reduction |
| Uptime | 95.5% | 99.9% | 4.4% increase |
```

**Supported Layouts:**
- `title` - Title slide with title and subtitle
- `content` - Rich content slide with mixed headings, paragraphs, and bullets
- `table` - Data table with full styling support

**Content Features:**
- **Headings:** Use `## Heading` for bold section headers
- **Paragraphs:** Regular text for explanatory content
- **Bullets:** Use `- item` for bullet points
- **Tables:** Standard markdown table syntax with styling options
- **Inline Formatting:** 
  - *Italic text* using `*text*`
  - **Bold text** using `**text**`
  - ___Underlined text___ using `___text___`
  - ***Bold italic text*** using `***text***`
  - ***___Bold italic underlined text___*** using `***___text___***`

### JSON Configuration (Advanced)

For precise control or programmatic generation, use the comprehensive JSON format:

```json
{
  "presentation": {
    "slides": [
      {
        "type": "title",
        "title": "**Q4 2024 Results** with *Emphasis*",
        "subtitle": "Financial Performance ___Overview___"
      },
      {
        "type": "content",
        "title": "Key Achievements",
        "content": [
          "**Revenue increased** by 15% year-over-year",
          "*Customer satisfaction* improved to 94%",
          "Successfully launched ***3 new products***",
          "Expanded to ___2 new markets___"
        ]
      },
      {
        "type": "table",
        "title": "Financial Summary",
        "table": {
          "header_style": "dark_blue_white_text",
          "row_style": "alternating_light_gray",
          "data": [
            ["**Metric**", "*Q4 2024*", "___Q3 2024___", "Change"],
            ["Revenue", "$12.5M", "$11.2M", "+11.6%"],
            ["Profit", "$3.2M", "$2.8M", "+14.3%"]
          ]
        }
      }
    ]
  }
}
```

**Key Features:**
- **Complete Workflow:** Single tool call creates and saves entire presentation
- **Inline Formatting:** Full support for `**bold**`, `*italic*`, and `___underline___`
- **Multiple Slide Types:** Title, content, and table slides in one JSON structure
- **Automatic Saving:** No separate save step required

## Next Steps

### Potential Enhancements

- **Chart Integration:** Add support for generating charts and graphs
- **Image Support:** Enable embedding of images and diagrams
- **Advanced Layouts:** Support for more complex slide layouts
- **Batch Operations:** Process multiple presentations simultaneously
- **Theme Customization:** Dynamic theme and color scheme management
- **Export Formats:** Support for PDF and other output formats

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the existing code style
4. Add tests for new functionality
5. Submit a pull request with a clear description

## Troubleshooting

### Common Issues

**"Template not found" error:**
- Ensure `DECK_TEMPLATE_FOLDER` environment variable is set correctly
- Verify the template file exists in the specified directory
- Check file permissions on the template directory

**"Permission denied" when saving presentations:**
- Verify `DECK_OUTPUT_FOLDER` has write permissions
- Ensure the output directory exists
- Check if files are currently open in PowerPoint

**MCP connection failures:**
- Verify Python virtual environment is activated
- Check that all dependencies are installed correctly
- Ensure the path in Claude Desktop config matches your installation

**JSON parsing errors:**
- Validate JSON structure using an online JSON validator
- Ensure all required fields are present for each slide type
- Check for proper escaping of special characters

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=1
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2025 Bruce McLeod - Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0