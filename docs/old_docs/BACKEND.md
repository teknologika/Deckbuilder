# Deckbuilder Backend Architecture

## Overview

The Deckbuilder backend is an MCP (Model Context Protocol) server built with FastMCP that enables AI assistants to create and manipulate PowerPoint presentations programmatically. The system uses a dynamic template mapping approach for flexible content placement with content-first intelligence.

## Project Structure

```
src/
├── mcp_server/
│   ├── main.py             # FastMCP server and MCP tools
│   ├── tools.py            # Template analyzer for JSON mapping generation
│   └── content_*.py        # Content-first MCP tools (planned)
├── deckbuilder/
│   ├── engine.py           # Core presentation engine
│   ├── structured_frontmatter.py  # YAML frontmatter processing
│   ├── placeholder_types.py       # PowerPoint placeholder definitions
│   └── cli_tools.py        # Standalone template management CLI utilities
├── placekitten/
│   └── __init__.py         # Image processing library (planned)
└── assets/
    └── templates/
        ├── default.pptx    # Default PowerPoint template
        └── default.json    # Default template JSON mapping
tests/
├── test_tools.py           # Template analyzer testing
├── test_*.json             # Test presentation data
├── test_*.md               # Test markdown presentations
└── output/                 # Generated presentation files
```

## Data Flow

### Presentation Creation Flow

1. **Template Selection**: Client specifies template name (e.g., "default")
2. **Template Loading**:
   - `deckbuilder/engine.py` loads `templateName.pptx` from template folder
   - Automatically loads corresponding `templateName.json` mapping file
   - Falls back to `assets/templates/default.json` if template-specific mapping not found
3. **Slide Creation**: Client provides slide data via MCP tools
4. **Layout Resolution**:
   - Slide `type` mapped to layout name via JSON `aliases`
   - Layout name resolved to PowerPoint layout index via JSON `layouts`
5. **Content Placement**: Slide content mapped to specific placeholders using JSON placeholder mappings
6. **Output Generation**: Completed presentation saved as timestamped `.g.pptx` file

### Template Analysis Flow (CLI Tools)

1. **Template Analysis**: `deckbuilder/cli_tools.py` provides standalone template management
2. **Structure Extraction**: Discovers layout names, indices, and placeholder information
3. **Validation**: Detects naming inconsistencies and provides PowerPoint fix instructions
4. **JSON Generation**: Creates `templateName.g.json` with raw extracted structure
5. **Documentation**: Auto-generates comprehensive template documentation
6. **User Customization**: Users edit `.g.json` to map placeholders to semantic field names
7. **Template Activation**: Users rename `.g.json` to `.json` to activate the mapping

## Core Components

### FastMCP Server (`mcp_server/main.py`)
- **MCP Protocol Handler**: Implements Model Context Protocol for AI assistant integration
- **Streamlined API**: Exposes two comprehensive tools: `create_presentation` and `create_presentation_from_markdown`
- **Complete Workflows**: Each tool handles creation, population, and saving in a single call
- **Environment Management**: Handles template and output folder configuration
- **Async Operations**: Supports concurrent presentation generation

### Deckbuilder Engine (`deckbuilder/engine.py`)
- **Presentation Management**: Creates and manipulates PowerPoint presentations using python-pptx
- **Template System**: Loads PowerPoint templates and JSON mapping configurations
- **Layout Resolution**: Maps user slide types to PowerPoint layouts via JSON configuration
- **Content Rendering**: Supports rich text formatting, tables, and multimedia content
- **Singleton Pattern**: Ensures consistent state across MCP tool calls

### Template Management System

#### CLI Template Tools (`deckbuilder/cli_tools.py`)
- **Standalone Operation**: Template management independent of MCP server
- **Comprehensive Analysis**: Layout extraction with validation and fix suggestions
- **Documentation Generation**: Auto-creates template specifications and usage examples
- **Validation System**: Detects placeholder naming issues with PowerPoint editing instructions
- **Environment Independence**: Smart path detection with command-line argument support
- **JSON Generation**: Creates template mapping files with actual PowerPoint names
- **Environment Integration**: Uses standard template and output folder paths
- **Automation Support**: Enables template analysis via test scripts

### Configuration System
- **JSON Mappings**: Template-specific layout and placeholder configurations
- **Environment Variables**: `DECK_TEMPLATE_FOLDER`, `DECK_OUTPUT_FOLDER` for path management
- **Fallback Strategy**: Graceful degradation when mappings are unavailable
- **Auto-Discovery**: Automatic copying of template files on first use

### Styling Engine (`deckbuilder/table_styles.py`)
- **Table Formatting**: Comprehensive table styling with headers, borders, and colors
- **Theme Support**: Predefined color schemes and formatting options
- **Custom Colors**: Support for hex color overrides
- **Style Inheritance**: Consistent formatting across presentation elements

### Content Intelligence System
- **Layout Intelligence** (`deckbuilder/layout_intelligence.json`): Semantic metadata for smart layout recommendations
- **Content Analysis** (`mcp_server/content_analysis.py`): Content-first MCP tools for analyzing user needs
- **Structured Frontmatter** (`deckbuilder/structured_frontmatter.py`): YAML processing with automatic PowerPoint mapping

## MCP Tool Architecture

### Tool Design Philosophy
The server implements a **streamlined two-tool approach** that prioritizes simplicity and completeness:

- **`create_presentation`**: Accepts comprehensive JSON with all slides and automatically saves
- **`create_presentation_from_markdown`**: Processes markdown with frontmatter and automatically saves

### Benefits of Simplified Architecture
- **Reduced Complexity**: Users need only one tool call instead of multiple sequential calls
- **Atomic Operations**: Each tool provides complete functionality (create + populate + save)
- **Error Reduction**: Eliminates state management issues between multiple tool calls
- **Better UX**: Cleaner API surface with comprehensive examples and documentation

### Tool Workflow
1. **Input Processing**: Parse JSON or markdown content
2. **Template Loading**: Load specified PowerPoint template and JSON mapping
3. **Presentation Creation**: Initialize empty presentation with template
4. **Content Population**: Add all slides with formatting and layout mapping
5. **Automatic Saving**: Save to disk with timestamp and return confirmation
