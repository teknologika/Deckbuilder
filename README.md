# Deckbuilder

[![Test Suite](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml/badge.svg)](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml)

A Python library and MCP (Model Context Protocol) server for intelligent PowerPoint presentation generation. Deckbuilder transforms LLMs from layout pickers into presentation consultants using a **content-first design philosophy**.

## Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Claude Desktop** or another MCP-compatible client
- **Virtual environment** (recommended)

### Installation

1. **Clone and setup:**
```bash
git clone <repository-url>
cd deckbuilder
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "/path/to/deckbuilder/venv/bin/python",
      "args": ["/path/to/deckbuilder/src/mcp_server/main.py"],
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

3. **Create directories:**
```bash
mkdir -p ~/Documents/Deckbuilder/Templates
mkdir -p ~/Documents/Deckbuilder
```

4. **Test the server:**
```bash
./run_server.sh
```

## Core Features

### 🎯 **Content-First Intelligence**
Instead of asking "what layouts exist?", Deckbuilder asks "what does the user want to communicate?" This transforms the system from a layout picker into an intelligent presentation consultant.

### 📝 **Multiple Input Formats**
- **JSON**: Precise programmatic control with comprehensive structure
- **Markdown + YAML**: Intuitive authoring with frontmatter definitions

### 🎨 **Rich Content Support**
- **Inline Formatting**: `**bold**`, `*italic*`, `___underline___`, `***bold italic***`
- **Mixed Content**: Headings, paragraphs, and bullet points in single slides
- **Advanced Tables**: Professional styling with custom colors and themes
- **50+ Layout Library**: Progressive implementation of business presentation layouts

### 🔧 **Template Management**
- **CLI Tools**: Analyze, validate, and enhance PowerPoint templates
- **Semantic Detection**: Automatic placeholder identification
- **Hybrid Mapping**: Semantic detection + JSON configuration for reliability

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server Layer                     │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │   FastMCP       │        │   Content-First    │     │
│  │   Endpoints     │◄──────►│   MCP Tools        │     │
│  └────────┬────────┘        └────────────────────┘     │
│           │                                              │
├───────────┴──────────────────────────────────────────────┤
│                 Presentation Engine                      │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │  PowerPoint     │        │   Template         │     │
│  │  Generation     │◄──────►│   Management       │     │
│  └────────┬────────┘        └────────────────────┘     │
│           │                                              │
├───────────┴──────────────────────────────────────────────┤
│                Content Intelligence                      │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │  Layout         │        │   Semantic         │     │
│  │  Intelligence   │◄──────►│   Analysis         │     │
│  └─────────────────┘        └────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Markdown with Frontmatter (Recommended)

```markdown
---
layout: Title Slide
---
# **Deckbuilder** Presentation
## Creating presentations with *content-first* intelligence

---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: "**Fast** processing with optimized algorithms"
  - title: Security
    content: "***Enterprise-grade*** encryption and compliance"
  - title: Usability
    content: "*Intuitive* interface with minimal learning curve"
  - title: Cost
    content: "___Transparent___ pricing with proven ROI"
---

---
layout: table
style: dark_blue_white_text
---
# Project Status

| **Feature** | *Status* | ___Priority___ |
| Authentication | **Complete** | *High* |
| User Management | ***In Progress*** | ___Medium___ |
| Reporting | *Planned* | **Low** |
```

### JSON Format (Programmatic)

```json
{
  "presentation": {
    "slides": [
      {
        "type": "Title Slide",
        "title": "**Deckbuilder** Presentation",
        "subtitle": "Content-first presentation generation"
      },
      {
        "type": "Title and Content",
        "title": "Key Benefits",
        "content": [
          "**Intelligent** content analysis",
          "*Semantic* layout recommendations",
          "***Professional*** template system"
        ]
      }
    ]
  }
}
```

## MCP Tools

### `create_presentation_from_markdown`
Creates presentations from markdown with YAML frontmatter. Handles complete workflow: parse → create → populate → save.

**Parameters:**
- `markdown_content` (required): Markdown with frontmatter slide definitions
- `fileName` (optional): Output filename (default: "Sample_Presentation")
- `templateName` (optional): Template to use (default: "default")

### `create_presentation`
Creates presentations from JSON data with automatic saving.

**Parameters:**
- `json_data` (required): JSON object containing presentation structure
- `fileName` (optional): Output filename
- `templateName` (optional): Template to use

### Content-First Tools (🚧 In Development)
- `analyze_presentation_needs()` - Content and goal analysis
- `recommend_slide_approach()` - Layout recommendations  
- `optimize_content_for_layout()` - Content optimization

## Template Management CLI

Deckbuilder includes standalone command-line tools for template management:

```bash
# Analyze template structure with validation
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate comprehensive documentation
python src/deckbuilder/cli_tools.py document default

# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default
```

**Features:**
- Extract PowerPoint template structure
- Generate JSON mappings for customization
- Detect naming inconsistencies with fix instructions
- Create comprehensive template documentation

## Supported Layouts

### ✅ Currently Implemented
- **Title Slide** - Opening slide with title and subtitle
- **Title and Content** - Rich text with headings, paragraphs, bullets
- **Four Columns** - Quad content areas with structured frontmatter
- **Two Content** - Side-by-side content areas
- **Comparison** - Left vs right comparison layout
- **Table** - Data tables with professional styling
- **Section Header** - Divider slides between topics
- **Picture with Caption** - Image-focused slides

### 🚧 Progressive Implementation (50+ Planned)
- Big Number displays, SWOT Analysis, Feature Matrix
- Timeline, Process Flow, Organizational Chart
- Dashboard, Metrics, Financial layouts
- And 40+ more business presentation layouts

See [Supported Templates](docs/Features/SupportedTemplates.md) for complete roadmap.

## Project Structure

```
src/
├── mcp_server/           # MCP Server Implementation
│   ├── main.py          # FastMCP server with lifecycle management
│   └── content_*.py     # Content-first tools (in development)
├── deckbuilder/         # Presentation Engine
│   ├── engine.py        # Core PowerPoint generation
│   ├── cli_tools.py     # Template management CLI
│   └── structured_frontmatter.py  # YAML processing
└── assets/templates/    # Template System
    ├── default.pptx     # PowerPoint template
    └── default.json     # Layout mappings
```

## Technology Stack

- **Python 3.11+** with modern type hints
- **FastMCP** for Model Context Protocol
- **python-pptx** for PowerPoint generation
- **PyYAML** for structured frontmatter
- **pytest** with comprehensive test coverage

## Documentation

- **[PLANNING.md](PLANNING.md)** - Project architecture and design principles
- **[API.md](docs/API.md)** - Complete API reference
- **[BACKEND.md](docs/BACKEND.md)** - Backend architecture details
- **[Feature Docs](docs/Features/)** - Detailed feature specifications

## Development

### Code Quality Standards
```bash
# Required before commits
black --line-length 100 src/
flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503,E501
pytest tests/
```

### Design Workflow
1. **Design features first** with plan-only mode
2. **Save designs** to `./docs/Features/feature_name.md`
3. **Follow content-first principles** - understand user needs before technical implementation
4. **Test comprehensively** with real presentation scenarios

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Follow code quality standards
4. Add comprehensive tests
5. Submit pull request with clear description

## Troubleshooting

**Template not found:**
- Verify `DECK_TEMPLATE_FOLDER` environment variable
- Check template file exists and has correct permissions

**Permission denied when saving:**
- Verify `DECK_OUTPUT_FOLDER` has write permissions
- Ensure files aren't currently open in PowerPoint

**MCP connection failures:**
- Verify virtual environment is activated
- Check Python path in Claude Desktop config
- Ensure all dependencies are installed

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

Copyright 2025 Bruce McLeod