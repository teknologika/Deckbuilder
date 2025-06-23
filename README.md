# Deck Builder MCP

## Overview

The Deck Builder MCP is a Model Context Protocol (MCP) server that enables AI assistants to programmatically create and manipulate PowerPoint presentations. Built with Python and FastMCP, this server provides a comprehensive set of tools for generating professional presentations with multiple slide types, custom styling, and template support.

The server solves the common challenge of automating presentation creation by offering both JSON and markdown interfaces for defining slide content and structure. Users can choose between precise JSON control or intuitive markdown authoring with YAML frontmatter. It's particularly useful for generating reports, dashboards, and structured presentations from data or user specifications.

**Technology Stack:**
- **Backend Framework:** FastMCP (Model Context Protocol)
- **Presentation Engine:** python-pptx
- **Content Parsing:** PyYAML for frontmatter, custom markdown parser
- **Transport:** stdio/SSE
- **Language:** Python 3.11+
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

- **Python 3.11+** with pip package manager
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
      "args": ["/path/to/deck-builder-mcp/src/mcp_server/main.py"],
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

### Core Components

**`src/mcp_server/`** - MCP Server Implementation
- **`main.py`** - FastMCP server setup with lifecycle management
- **`tools.py`** - Tool definitions for presentation operations and template analysis
- **`content_*.py`** - Content-first MCP tools (planned)

**`src/deckbuilder/`** - Presentation Engine
- **`engine.py`** - Core Deckbuilder class for presentation management
- **`structured_frontmatter.py`** - YAML frontmatter processing and layout mapping
- **`placeholder_types.py`** - PowerPoint placeholder type definitions
- **`cli_tools.py`** - Command-line template management utilities

**`src/placekitten/`** - Image Processing Library (Planned)
- **`__init__.py`** - PlaceKitten library placeholder
- Smart image cropping and computer vision features (not implemented)

**`assets/templates/`** - Template System
- **`default.json`** - PowerPoint layout to placeholder mappings
- **`default.pptx`** - Default PowerPoint template file

**`run_server.sh`** - Server startup script
- Virtual environment activation and server launch
- Convenient development and testing script

### Available MCP Tools

The server provides two comprehensive tools for complete "one-shot" presentation creation:

#### 1. `create_presentation` - JSON-Based Presentation Creation
**Purpose**: Create complete PowerPoint presentations from structured JSON data
**Usage**: One-shot creation with automatic saving

**Parameters**:
- `json_data` (required): JSON string containing presentation structure
- `fileName` (optional): Output filename (default: "Sample_Presentation")  
- `templateName` (optional): Template to use (default: "default")

**Supported Features**:
- **All PowerPoint layouts**: Title Slide, Title and Content, Two Content, Four Columns, Comparison, Section Header, Title Only, Picture with Caption, Content with Caption, Blank, Table
- **Structured frontmatter layouts**: Clean YAML syntax automatically converted to PowerPoint placeholders
- **Rich content support**: Headings, paragraphs, bullet points with automatic formatting
- **Inline formatting**: `**bold**`, `*italic*`, `___underline___`, `***bold italic***`
- **Table styling**: Multiple header, row, and border styles with custom color support
- **Template compatibility**: Works with any PowerPoint template via semantic detection + JSON mapping

#### 2. `create_presentation_from_markdown` - Markdown-Based Presentation Creation  
**Purpose**: Create presentations using familiar markdown syntax with YAML frontmatter
**Usage**: One-shot creation from markdown content with automatic saving

**Parameters**:
- `markdown_content` (required): Markdown string with frontmatter slide definitions
- `fileName` (optional): Output filename (default: "Sample_Presentation")
- `templateName` (optional): Template to use (default: "default")

**Supported Features**:
- **YAML frontmatter**: Clean slide definitions with `layout:` specification
- **Structured frontmatter**: Advanced layouts like Four Columns, Two Content, Comparison with semantic field mapping
- **Markdown content**: Standard markdown syntax for content areas
- **Mixed content**: Headings (`## Title`), paragraphs, and bullets (`- item`) in single slides
- **Inline formatting**: Full support for bold, italic, underline combinations
- **Table slides**: Markdown tables with styling options via frontmatter

**Example Frontmatter Layouts**:
```yaml
---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: "Fast processing with **optimized** algorithms"
  - title: Security  
    content: "***Enterprise-grade*** encryption"
---
```

**One-Shot Workflow**: Both tools handle the complete presentation lifecycle:
1. **Parse** input (JSON or Markdown)
2. **Create** presentation with specified template
3. **Add** all slides with proper layout selection and content placement
4. **Save** presentation to disk automatically
5. **Return** success confirmation with file details

This eliminates the need for multiple tool calls and provides immediate, ready-to-use PowerPoint files.

## Template Management CLI Tools

In addition to the MCP server, the project includes standalone command-line tools for template management. These tools operate independently and don't require the MCP server to be running.

### Available CLI Commands

#### 1. `analyze` - Template Structure Analysis
**Purpose**: Analyze PowerPoint templates to extract layout and placeholder information

```bash
# Basic analysis
python src/deckbuilder/cli_tools.py analyze default

# Detailed analysis with verbose output
python src/deckbuilder/cli_tools.py analyze default --verbose

# Custom template and output folders
python src/deckbuilder/cli_tools.py analyze default --template-folder ./templates --output-folder ./output
```

**Features**:
- Extracts all slide layouts with placeholder mappings
- Detects naming inconsistencies and validation issues
- Generates JSON mapping files (`.g.json`) for customization
- Provides specific PowerPoint editing instructions for fixes

#### 2. `document` - Template Documentation Generation
**Purpose**: Generate comprehensive documentation for templates

```bash
# Generate documentation for default template
python src/deckbuilder/cli_tools.py document default

# Custom documentation output path
python src/deckbuilder/cli_tools.py document default --doc-output ./docs/MyTemplate.md
```

**Output**:
- Complete layout specifications with placeholder details
- Usage examples in both JSON and YAML formats
- Template management instructions
- Status tracking (JSON mapping, structured frontmatter support)

#### 3. `validate` - Template and Mapping Validation
**Purpose**: Validate template structure and JSON mappings

```bash
# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default
```

**Validation Checks**:
- Template file accessibility
- JSON mapping structure and completeness
- Placeholder naming conventions
- Column layout consistency
- Comparison layout structure

### CLI Tool Setup

The CLI tools automatically detect template and output folders using this priority:

1. **Command-line arguments**: `--template-folder` and `--output-folder`
2. **Current directory**: Looks for `assets/templates` relative to current directory
3. **Project root**: Falls back to project's default template location

**Quick Setup**:
```bash
# From project root
cd /path/to/deck-builder-mcp

# Analyze default template (auto-detects paths)
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate documentation
python src/deckbuilder/cli_tools.py document default

# Validate everything
python src/deckbuilder/cli_tools.py validate default
```

### Template Enhancement Workflow

1. **Analyze**: Extract current template structure
   ```bash
   python src/deckbuilder/cli_tools.py analyze default --verbose
   ```

2. **Review Issues**: Check validation output for naming problems
   - Column layouts with inconsistent numbering
   - Duplicate placeholder names
   - Missing required placeholders

3. **Fix in PowerPoint**: 
   - Open PowerPoint template file
   - Go to View > Slide Master
   - Use Selection Pane to rename placeholders
   - Follow specific fix instructions from validation output

4. **Re-analyze**: Verify fixes
   ```bash
   python src/deckbuilder/cli_tools.py analyze default --verbose
   ```

5. **Generate Documentation**: Create updated documentation
   ```bash
   python src/deckbuilder/cli_tools.py document default
   ```

The CLI tools provide detailed fix instructions for common issues like:
- **Column Layout Fixes**: "In PowerPoint: Rename 'Col 1 Text Placeholder 3' → 'Col 1 Text Placeholder 2'"
- **Naming Consistency**: Standardizing placeholder naming patterns
- **Sequential Numbering**: Ensuring columns are numbered 1, 2, 3, 4 consistently

### Configuration Files

- **`CLAUDE.md`** - Development guidelines for AI assistants
- **`.gitignore`** - Git ignore patterns including MCP and Claude configs
- **`table-styles.css/html`** - Table styling reference documentation

## Usage Examples

### Markdown with Frontmatter (Recommended)

Create presentations using familiar markdown syntax with YAML frontmatter for layout control:

```markdown
---
layout: Title Slide
---
# **Test Presentation** with *Inline* Formatting
## Testing all ___placeholders___ and **formatting** capabilities

---
layout: Four Columns
title: Four Column Layout **Comprehensive** Test
columns:
  - title: Performance
    content: "**Fast processing** with optimized algorithms and *sub-millisecond* response times"
  - title: Security
    content: "***Enterprise-grade*** encryption with ___SOC2___ and GDPR compliance"
  - title: Usability
    content: "*Intuitive* interface with **minimal** learning curve and comprehensive docs"
  - title: Cost
    content: "___Transparent___ pricing with **flexible** plans and *proven* ROI"
---

---
layout: Comparison
title: Comparison Layout **Full** Test
comparison:
  left:
    title: Option A Benefits
    content: "**Cost effective** solution with *rapid* deployment and ***proven*** technology"
  right:
    title: Option B Benefits
    content: "___Advanced___ features with **future-proof** architecture and *scalable* design"
---

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
---
# Table Slide with **Formatted** Content

| **Feature** | *Status* | ___Priority___ |
| Authentication | **Complete** | *High* |
| User Management | ***In Progress*** | ___Medium___ |
| Reporting | *Planned* | **Low** |
| API Integration | ___Blocked___ | ***Critical*** |
```

**Supported Layouts:**
- `Title Slide` - Title slide with title and subtitle
- `Title and Content` - Rich content slide with mixed headings, paragraphs, and bullets
- `Four Columns` - Structured frontmatter with 4 content areas
- `Two Content` - Side-by-side content areas  
- `Comparison` - Left vs right comparison layout
- `Section Header` - Divider slides between topics
- `Picture with Caption` - Image-focused slide with caption
- `table` - Data table with full styling support
- `Blank` - Minimal structure for custom content

**Structured Frontmatter Features:**
- **Four Columns:** Clean YAML with `columns:` array
- **Two Content:** `sections:` with title and content pairs
- **Comparison:** `comparison:` with left/right structure
- **Picture with Caption:** `media:` with caption and description

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

For precise control or programmatic generation, use the comprehensive JSON format. **Important**: When calling the MCP tool, the JSON must be passed as a properly escaped string.

#### Simple JSON Example (Recommended for MCP calls):
```json
{
  "presentation": {
    "slides": [
      {
        "type": "Title Slide",
        "title": "**My Presentation** with *Formatting*",
        "subtitle": "Testing ___all___ capabilities"
      },
      {
        "type": "Title and Content",
        "title": "Key Points",
        "content": [
          "**First** important point",
          "*Second* key insight",
          "***Critical*** information"
        ]
      },
      {
        "type": "table",
        "title": "Summary Table",
        "table": {
          "header_style": "dark_blue_white_text",
          "row_style": "alternating_light_gray",
          "data": [
            ["**Item**", "*Status*", "___Priority___"],
            ["Task 1", "**Complete**", "*High*"],
            ["Task 2", "***In Progress***", "___Medium___"]
          ]
        }
      }
    ]
  }
}
```

#### For MCP Tool Usage:
When calling `create_presentation`, pass the JSON as a string parameter:

**✅ Correct Usage:**
```
Tool: create_presentation
Parameters:
- json_data: "{\"presentation\":{\"slides\":[{\"type\":\"Title Slide\",\"title\":\"**My Presentation**\",\"subtitle\":\"Test\"}]}}"
- fileName: "MyPresentation"
```

**❌ Incorrect Usage:**
```
Tool: create_presentation  
Parameters:
- json_data: {raw JSON object} // This will cause errors
```

#### Structured Frontmatter Alternative (Easier):
For complex layouts, consider using the markdown tool with structured frontmatter instead:

```yaml
---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: "**Fast** processing"
  - title: Security
    content: "***Enterprise*** grade"
---
```

**Key Features:**
- **Complete Workflow:** Single tool call creates and saves entire presentation
- **Inline Formatting:** Full support for `**bold**`, `*italic*`, and `___underline___`
- **Multiple Slide Types:** All PowerPoint layouts supported
- **Automatic Saving:** No separate save step required
- **String Parameter:** JSON must be properly escaped when calling MCP tools

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