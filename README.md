# Deckbuilder

[![Test Suite](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml/badge.svg)](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml)
[![PlaceKitten Integrated](https://img.shields.io/badge/PlaceKitten-Integrated-blue)](src/placekitten/README.md)
[![108 Tests Passing](https://img.shields.io/badge/Tests-108%20Passing-green)](#development)

Deckbuilder is a Python library and MCP (Model Context Protocol) server for intelligent PowerPoint presentation generation. Deckbuilder transforms LLMs from layout pickers into presentation consultants using a **content-first design philosophy**.

# Core Features

### ** One-shot Powerpoint Presentation creation from JSON or FrontMatter formatted Markdown **

Deckbuilder provides a comprehensive Python library for PowerPoint generation with sophisticated content intelligence. The library features a singleton-based presentation engine that processes JSON data, markdown with YAML frontmatter, and structured content through semantic placeholder detection. Key capabilities include a hybrid template system combining semantic detection with JSON mapping, CLI tools for template management and validation, multi-tier placeholder naming conventions, and content-first layout recommendations. The system supports 50+ business presentation layouts with rich formatting (bold, italic, underline), professional table styling, and automatic template enhancement with organized backup systems.

[Deckbuilder Python Library](docs/Features/Deckbuilder_Python_Library.md) | [PlaceKitten Documentation](src/placekitten/README.md)

### 🎨 **Rich Content Support**
- **Inline Formatting**: `**bold**`, `*italic*`, `___underline___`, `***bold italic***`
- **Mixed Content**: Headings, paragraphs, and bullet points in single slides
- **Advanced Tables**: Professional styling with custom colors and themes
- **50+ Layout Library**: Progressive implementation of business presentation layouts

### 🖼️ **PlaceKitten Image Processing** ✅ COMPLETE
- **Smart Image Fallbacks**: Automatic professional placeholder generation for missing/invalid images
- **Computer Vision**: Intelligent cropping with face detection and rule-of-thirds composition
- **Professional Filters**: 10+ effects including automatic grayscale for business presentations
- **Seamless Integration**: Zero-configuration fallback system with intelligent caching
- **Performance Optimized**: <2s processing, <5s smart crop, cached duplicate prevention

### 📝 **Multiple Input Formats**
- **JSON**: Precise programmatic control with comprehensive structure
- **Markdown + YAML**: Intuitive authoring with frontmatter definitions


### 🎯 **Content-First Intelligence**
Instead of asking "what layouts exist?", the Deckbuilder MCP tools ask "what does the user want to communicate?" This transforms the system from a layout picker into an intelligent presentation consultant.


### 🔧 **Template Management**
- **CLI Tools**: Analyze, validate, and enhance PowerPoint templates
- **Semantic Detection**: Automatic placeholder identification
- **Hybrid Mapping**: Semantic detection + JSON configuration for reliability



## Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Claude Desktop** or another MCP-compatible client
- **Virtual environment** (recommended)

### Installation

#### Option 1: Production Install (Recommended)

1. **Install from PyPI:**
```bash
pip install deckbuilder
```

2. **Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "deckbuilder-server",
      "env": {
        "DECK_TEMPLATE_FOLDER": "/Users/username/Documents/Deckbuilder/Templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/Users/username/Documents/Deckbuilder"
      }
    }
  }
}
```

3. **Create directories and copy templates:**
```bash
mkdir -p ~/Documents/Deckbuilder/Templates
mkdir -p ~/Documents/Deckbuilder

# Copy default template from package installation
python -c "
import deckbuilder
import shutil
from pathlib import Path
pkg_path = Path(deckbuilder.__file__).parent
template_src = pkg_path.parent / 'assets' / 'templates'
if template_src.exists():
    shutil.copytree(template_src, Path.home() / 'Documents/Deckbuilder/Templates', dirs_exist_ok=True)
    print('✅ Templates copied successfully')
else:
    print('⚠️ Template source not found, you may need to copy templates manually')
"
```

#### Option 2: Development Install

1. **Clone and setup:**
```bash
git clone https://github.com/teknologika/deckbuilder.git
cd deckbuilder
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .[dev]
```

2. **Configure Claude Desktop (Development):**
```json
{
  "mcpServers": {
    "deckbuilder-dev": {
      "command": "/path/to/deckbuilder/.venv/bin/python",
      "args": ["/path/to/deckbuilder/src/mcp_server/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "DECK_TEMPLATE_FOLDER": "/path/to/deckbuilder/assets/templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/Users/username/Documents/Deckbuilder"
      }
    }
  }
}
```

3. **Create output directory:**
```bash
mkdir -p ~/Documents/Deckbuilder
```

4. **Test the server:**
```bash
./run_server.sh
```

## CLI Usage (Standalone)

After installation, you can use Deckbuilder directly from the command line without Claude Desktop:

### Production CLI (After pip install)
```bash
# Create presentation from markdown
deckbuilder create examples/basic_presentation.md --output "My Presentation"

# Template management
deckbuilder analyze default --verbose
deckbuilder validate default
deckbuilder templates

# PlaceKitten image generation
deckbuilder image 800 600 --filter grayscale --output placeholder.jpg
deckbuilder crop photo.jpg 1920 1080 --save-steps

# Configuration
deckbuilder config
deckbuilder --help
```

### Development CLI (From source)
```bash
# Activate virtual environment first
source .venv/bin/activate

# Use Python module directly
python src/deckbuilder/cli.py create examples/basic_presentation.md
python src/deckbuilder/cli.py --help

# Or use the development script
./deckbuilder create examples/basic_presentation.md
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    MCP Server Layer                 │
│  ┌─────────────────┐        ┌────────────────────┐  │
│  │   FastMCP       │        │   Content-First    │  │
│  │   Endpoints     │◄──────►│   MCP Tools        │  │
│  └────────┬────────┘        └────────────────────┘  │
│           │                                         │
├───────────┴─────────────────────────────────────────┤
│                 Presentation Engine                 │
│  ┌─────────────────┐        ┌────────────────────┐  │
│  │  PowerPoint     │        │   Template         │  │
│  │  Generation     │◄──────►│   Management       │  │
│  └────────┬────────┘        └────────────────────┘  │
│           │                                         │
├───────────┴─────────────────────────────────────────┤
│                Content Intelligence                 │
│  ┌─────────────────┐        ┌────────────────────┐  │
│  │  Layout         │        │   Semantic         │  │
│  │  Intelligence   │◄──────►│   Analysis         │  │
│  └─────────────────┘        └────────────────────┘  │
└─────────────────────────────────────────────────────┘
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

### PlaceKitten Image Processing (Enhanced YAML)

```markdown
---
layout: Picture with Caption
title: Market Analysis
media:
  image_path: "charts/revenue_growth.png"  # Primary image source
  alt_text: "Revenue growth chart"          # Accessibility support
  caption: "**Q4 Revenue Growth**"          # Formatted caption
  description: |
    Revenue increased ***23%*** this quarter with strong performance in:
    • Enterprise sales: *35% growth*
    • Subscription revenue: **18% increase**
    • New market expansion: ***12% boost***
---
```

**Smart Fallback Behavior** ✅ IMPLEMENTED: When `image_path` is missing or invalid, PlaceKitten automatically generates professional placeholder images with:
- ✅ **File Validation**: Checks image existence, format, and accessibility
- ✅ **Professional Styling**: Automatic grayscale filtering for business-appropriate context  
- ✅ **Smart Cropping**: Computer vision-based cropping to exact placeholder dimensions
- ✅ **Performance Optimization**: Intelligent caching prevents duplicate processing
- ✅ **Seamless Integration**: Zero user intervention required for fallback generation

```python
# Direct PlaceKitten usage
from placekitten import PlaceKitten

pk = PlaceKitten()
placeholder = (pk.generate(1920, 1080, image_id=1)
                .smart_crop(1920, 1080)
                .apply_filter("grayscale")
                .save("professional_placeholder.jpg"))
```

## MCP Tools

### `create_presentation_from_markdown` ✅ ENHANCED
Creates presentations from markdown with YAML frontmatter. Handles complete workflow: parse → create → populate → save.

**Enhanced Features:**
- ✅ **Smart Image Fallbacks**: Automatic PlaceKitten generation for missing images
- ✅ **Professional Styling**: Business-appropriate grayscale filtering and smart cropping
- ✅ **Rich Content Support**: Bold, italic, underline formatting preservation
- ✅ **Performance Optimization**: Intelligent caching and processing

**Parameters:**
- `markdown_content` (required): Markdown with frontmatter slide definitions
- `fileName` (optional): Output filename (default: "Sample_Presentation")
- `templateName` (optional): Template to use (default: "default")

### `create_presentation` ✅ ENHANCED
Creates presentations from JSON data with automatic saving.

**Enhanced Features:**
- ✅ **Image Field Support**: Automatic fallback for `image_1`, `image_2`, etc. fields
- ✅ **Professional Styling**: Business-appropriate image processing
- ✅ **Format Flexibility**: Supports both YAML frontmatter and JSON structures

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

- **Python 3.11+** with modern type hints and comprehensive error handling
- **FastMCP** for Model Context Protocol server implementation
- **python-pptx** for PowerPoint generation and template manipulation
- **PyYAML** for structured frontmatter processing
- **OpenCV + Pillow** for computer vision and image processing (PlaceKitten)
- **pytest** with 108 comprehensive tests including image integration validation

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
