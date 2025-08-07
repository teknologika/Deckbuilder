> [!IMPORTANT]  
> Deckbuilder is currently under active development and should NOT be considered production ready.

# 🎯 Deckbuilder
[![PyPI version](https://badge.fury.io/py/deckbuilder.svg)](https://badge.fury.io/py/deckbuilder)
[![Test Suite](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml/badge.svg)](https://github.com/teknologika/deckbuilder/actions/workflows/test.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Create professional PowerPoint presentations from Markdown or JSON**

Deckbuilder is a Python library, Command Line tool, and MCP server that generates PowerPoint presentations from structured content. Focus on your content - Deckbuilder handles the formatting and layout.

## ✨ Key Features

### 🚀 **One-Shot Presentation Generation**
Create complete PowerPoint presentations from JSON or Markdown with YAML frontmatter in a single command.

### 🎨 **Rich Content Support**
- **Advanced Formatting**: `**bold**`, `*italic*`, `___underline___`, `***bold italic***`
- **Language & Font updating**: The ability to update the fonts and language of all slide objects using the command line tools using the CLI.
- **Professional Tables**: Custom styling with themes, colors, and precise dimension controls (column widths, row heights, table sizing).
- **Supported Layouts**: Progressive library of templates being added.

### 🧠 **Smart Template System**
- **Intelligent Layout Selection**: Automatic layout recommendations based on content type
- **Pattern-Based Architecture**: Customize any layout with your own templates
- **Rich Content Support**: Tables, images, multi-column layouts with professional styling

### 🖼️ **Smart Image Processing**
- **Automatic Image Fallbacks**: Missing images? Deckbuilder generates professional placeholders automatically
- **Smart Cropping**: Face detection and intelligent composition for perfect image sizing
- **Professional Filters**: Business-appropriate styling with grayscale and other effects

### ⚡ **Enhanced CLI Experience**
- **Professional Hierarchical Interface**: Clean command structure (`deckbuilder <command> <subcommand>`)
- **One-Command Setup**: `deckbuilder init` creates templates and configuration
- **Context-Aware Paths**: CLI args > env vars > current directory precedence
- **Always Local Output**: CLI outputs to current directory for predictable local development
- **Global Arguments**: `-t/--template-folder`, `-l/--language`, `-f/--font` for complete customisation
- **Comprehensive Command Structure**:
  - `deckbuilder template` → analyze, validate, document, enhance, list
  - `deckbuilder config` → show, languages, completion
  - `deckbuilder image` → generate, crop
  - `deckbuilder remap` → update existing PowerPoint files with language/font changes
- **Template Management**: Analyze, validate, and enhance PowerPoint templates with detailed validation

## 🚀 Quick Start

### Installation

```bash
pip install deckbuilder
```

### CLI Usage (Standalone)

```bash
# Initialize templates (one-time setup) This will create the default template and mapping JSON.
deckbuilder init

# Create presentation from markdown (outputs to current directory)
deckbuilder create presentation.md

# Use custom template folder (CLI arg overrides env vars)
deckbuilder --template-folder /custom/templates create presentation.md

# Create with custom language and font (supports both formats)
deckbuilder create presentation.md --language "es-ES" --font "Arial"
deckbuilder create presentation.md --language "Spanish (Spain)" --font "Times New Roman"

# View supported languages
deckbuilder config languages

# Template management & intelligence
deckbuilder template analyze default --verbose
deckbuilder template validate default
deckbuilder template list

# Smart template recommendations available through MCP tools

# Image generation with crop-first approach
deckbuilder image generate 800 600 --filter grayscale
deckbuilder image crop image.jpg 800 600

# Language and font remapping for existing PowerPoint files
deckbuilder remap existing.pptx --language en-US --font Arial

# View current configuration (shows path sources)
deckbuilder config show

# Get help
deckbuilder --help
```

### MCP Server (Claude Desktop)

Add to your Claude Desktop configuration:

**Option 1: Direct installation (recommended)**
```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "deckbuilder-server",
      "env": {
        "DECK_TEMPLATE_FOLDER": "/Users/username/Documents/Deckbuilder/Templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/Users/username/Documents/Deckbuilder",
        "DECK_PROOFING_LANGUAGE": "en-AU",
        "DECK_DEFAULT_FONT": "Calibri"
      }
    }
  }
}
```
**New Environment Variables:**
- `DECK_PROOFING_LANGUAGE`: Set proofing language for spell-check and grammar (accepts both "en-AU" and "English (Australia)" formats)
- `DECK_DEFAULT_FONT`: Set default font family for all presentations
- **Default Language**: Australian English (`en-AU`) if not specified

## 📝 Usage Examples

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
layout: Picture with Caption
title: Market Analysis
media:
  image_path: "charts/revenue_growth.png"  # Auto-fallback to PlaceKitten if missing
  alt_text: "Revenue growth chart"
  caption: "**Q4 Revenue Growth** - 23% increase"
---

---
layout: Title and Content
title: "**Table Dimensions:** Custom Column Widths"
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
column_widths: [8, 6, 4, 5]
row_height: 0.9
content: |
  Sales Performance Report with individual column width control:

  | **Product Category** | **Q1 Sales** | **Q2** | **Growth %** |
  | Enterprise Software | $125,000 | $142,000 | +13.6% |
  | SaaS Solutions | $89,500 | $98,200 | +9.7% |
  | Cloud Services | $156,000 | $178,000 | +14.1% |
  | Mobile Apps | $67,300 | $73,800 | +9.7% |
---

---
layout: Title and Content
title: "**Table Dimensions:** Equal Column Distribution"
style: light_blue_dark_text
row_style: alternating_light_gray
border_style: thin_gray
table_width: 22
row_height: 0.9
content: |
  Team Performance Dashboard with equal column distribution:

  | **Team Member** | **Projects** | **Completed** | **Success Rate** |
  | Alice Johnson | 25 | 24 | 96% |
  | Bob Smith | 18 | 17 | 94% |
  | Carol Davis | 32 | 31 | 97% |
  | David Wilson | 21 | 20 | 95% |
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
      },
      {
        "type": "Title and Content",
        "title": "Team Performance Dashboard",
        "table": {
          "column_widths": [6, 4, 5, 3],
          "row_height": 1.8,
          "data": [
            ["**Team Member**", "**Projects**", "**Completed**", "**Rate**"],
            ["Alice Johnson", "25", "24", "96%"],
            ["Bob Smith", "18", "17", "94%"],
            ["Carol Davis", "32", "31", "97%"]
          ],
          "header_style": "dark_blue_white_text",
          "row_style": "alternating_light_gray",
          "border_style": "thin_gray"
        }
      }
    ]
  }
}
```

### Python API

```python
from deckbuilder import Deckbuilder

# Initialize engine
db = Deckbuilder()

# Create from markdown
result = db.create_presentation_from_markdown(
    markdown_content=open("presentation.md").read(),
    fileName="My_Presentation"
)

# Create from JSON
result = db.create_presentation(
    json_data={"presentation": {"slides": [...]}},
    fileName="JSON_Presentation"
)

print(f"✅ Created: {result}")
```

## 🌍 Language & Font Support

### Supported Languages (20)
Deckbuilder supports 20 proofing languages for spell-check and grammar. You can use either locale codes (`en-AU`) or full names (`English (Australia)`):

```bash
# View all supported languages (shows both formats)
deckbuilder config languages
```

**Available Languages:**
- English (United States, United Kingdom, Canada, Australia)
- Spanish (Spain, Mexico, Latin America)
- French (France, Canada)
- German (Germany, Austria, Switzerland)
- Italian, Portuguese (Brazil, Portugal)
- Chinese (Simplified, Traditional), Japanese, Korean
- Dutch, Russian, Arabic

### Font Customization

```bash
# Set language and font globally (supports both formats)
export DECK_PROOFING_LANGUAGE="en-AU"           # Locale code format
export DECK_PROOFING_LANGUAGE="English (Australia)"  # Full name format
export DECK_DEFAULT_FONT="Arial"

# Or use CLI arguments (both formats work)
deckbuilder create presentation.md --language "fr-CA" --font "Times New Roman"
deckbuilder create presentation.md --language "French (Canada)" --font "Arial"

# Check current settings (shows locale codes and descriptions)
deckbuilder config show
```

## 🖼️ PlaceKitten Image Processing

**Smart Image Fallback System** - When images are missing or invalid, PlaceKitten automatically generates professional placeholders:

```python
from placekitten import PlaceKitten

pk = PlaceKitten()
placeholder = (pk.generate(1920, 1080, image_id=1)
                .smart_crop(1920, 1080)
                .apply_filter("grayscale")
                .save("professional_placeholder.jpg"))
```

**Features:**
- ✅ **File Validation**: Checks image existence, format, and accessibility
- ✅ **Professional Styling**: Automatic grayscale filtering for business context  
- ✅ **Smart Cropping**: Computer vision-based cropping with face detection
- ✅ **Performance Optimized**: Intelligent caching prevents duplicate processing
- ✅ **Seamless Integration**: Zero user intervention required

## 🚀 What's New in v1.2.0

### Smart Template Recommendations
- **Content Analysis**: Automatically analyzes your content to suggest the best layouts
- **MCP Integration**: Available through Claude Desktop with intelligent recommendations

### Enhanced Image Processing  
- **Better Image Sizing**: Smart cropping ensures images fit perfectly without distortion
- **Automatic Fallbacks**: Professional placeholder images when your images are missing

### Improved Pattern System
- **User Customization**: Create custom layout patterns in `{template_folder}/patterns/`
- **Dynamic Loading**: All layouts now use flexible pattern files instead of hard-coded templates

## 🏗️ Architecture

```
    Your Content (Markdown/JSON)
              ↓
    ┌─────────────────────┐
    │   Content Analysis  │  ← Analyzes your content type and audience
    └─────────┬───────────┘
              ↓
    ┌─────────────────────┐
    │ Template Selection  │  ← Recommends best layouts for your content
    └─────────┬───────────┘
              ↓
    ┌─────────────────────┐
    │  PowerPoint Engine  │  ← Generates professional presentations
    └─────────┬───────────┘
              ↓
    Your Professional Presentation
```

## 🎨 Supported Markdown Layouts

### ✅ Currently Implemented
- **Title Slide** - Opening slide with title and subtitle
- **Title and Content** - Rich text with headings, paragraphs, bullets
- **Four Columns** - Quad content areas with structured frontmatter
- **Two Content** - Side-by-side content areas
- **Comparison** - Left vs right comparison layout
- **Table** - Data tables with professional styling
- **Section Header** - Divider slides between topics
- **Picture with Caption** - Image-focused slides with smart fallbacks

### 🚧 Progressive Implementation (50+ Planned)
- Big Number displays, SWOT Analysis, Feature Matrix
- Timeline, Process Flow, Organizational Chart
- Dashboard, Metrics, Financial layouts
- And 40+ more business presentation layouts

See [Feature Documentation](docs/old_docs/Features/) for detailed specifications.

## 🛠️ Development

### Prerequisites
- Python 3.11+
- Virtual environments are recommended.

### Development Install

```bash
git clone https://github.com/teknologika/deckbuilder.git
cd deckbuilder
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

### Code Quality Standards

```bash
# Format code (required before commits)
black --line-length 100 src/

# Check linting (required)
flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503,E501

# Run tests (required)
pytest tests/
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Follow code quality standards
4. Add comprehensive tests
5. Submit pull request with clear description

## 📚 Documentation

- **[Complete Documentation](docs/)** - Full documentation index
- **[Supported Templates](docs/supported_templates.md)** - Complete layout library (26+ patterns)
- **[Deckbuilder Library](docs/deckbuilder.md)** - Python API reference and classes
- **[Command-Line Interface](docs/cli.md)** - CLI commands and usage examples
- **[MCP Server](docs/mcp_server.md)** - Smart template recommendations and MCP tools
- **[PlaceKitten Library](docs/placekitten.md)** - Image processing with crop-first approach
- **[PlaceKitten Source](src/placekitten/README.md)** - Technical implementation details

## 🔧 Technology Stack

- **Python 3.11+** with modern type hints and comprehensive error handling
- **FastMCP** for Model Context Protocol server implementation
- **python-pptx** for PowerPoint generation and template manipulation
- **PyYAML** for structured frontmatter processing
- **OpenCV + Pillow** for computer vision and image processing
- **pytest** for unit testing
- **Anthropic Claude** - for most of the development gruntwork :-)

## 📋 Troubleshooting

**Template not found:**
```bash
# Create templates folder
deckbuilder init

# Check configuration
deckbuilder config
```

**Permission denied when saving:**
- Verify output folder has write permissions
- Ensure files aren't open in PowerPoint

**MCP connection failures:**
- Verify virtual environment is activated
- Check Python path in Claude Desktop config
- Ensure all dependencies are installed

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for intelligent presentation generation - Copyright Bruce McLeod**

[🚀 Get Started](#quick-start) • [📖 Documentation](docs/) • [🐛 Report Issues](https://github.com/teknologika/deckbuilder/issues)

</div>