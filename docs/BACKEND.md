# Backend Architecture

## Overview

The deck-builder-mcp backend is an MCP (Model Context Protocol) server built with FastMCP that enables AI assistants to create and manipulate PowerPoint presentations programmatically. The system uses a dynamic template mapping approach for flexible content placement.

## Project Structure

```
src/
├── main.py                 # FastMCP server and MCP tools
├── deckbuilder.py          # Core presentation engine 
├── tools.py                # Template analyzer for JSON mapping generation
├── table_styles.py         # Table styling configurations
├── default.pptx           # Default PowerPoint template
├── default.json           # Default template JSON mapping
└── tests/
    ├── test_tools.py       # Template analyzer testing
    ├── templates/          # Test template files  
    └── output/             # Generated mapping files
```

## Data Flow

### Presentation Creation Flow

1. **Template Selection**: Client specifies template name (e.g., "default")
2. **Template Loading**: 
   - `deckbuilder.py` loads `templateName.pptx` from template folder
   - Automatically loads corresponding `templateName.json` mapping file
   - Falls back to `src/default.json` if template-specific mapping not found
3. **Slide Creation**: Client provides slide data via MCP tools
4. **Layout Resolution**: 
   - Slide `type` mapped to layout name via JSON `aliases`
   - Layout name resolved to PowerPoint layout index via JSON `layouts`
5. **Content Placement**: Slide content mapped to specific placeholders using JSON placeholder mappings
6. **Output Generation**: Completed presentation saved as timestamped `.g.pptx` file

### Template Analysis Flow

1. **Template Analysis**: `tools.py` analyzes existing PowerPoint templates
2. **Structure Extraction**: Discovers layout names, indices, and placeholder information
3. **JSON Generation**: Creates `templateName.g.json` with raw extracted structure  
4. **User Customization**: Users edit `.g.json` to map placeholders to semantic field names
5. **Template Activation**: Users rename `.g.json` to `.json` to activate the mapping

## Core Components

### FastMCP Server (`main.py`)
- **MCP Protocol Handler**: Implements Model Context Protocol for AI assistant integration
- **Tool Registration**: Exposes presentation creation tools to MCP clients
- **Environment Management**: Handles template and output folder configuration
- **Async Operations**: Supports concurrent presentation generation

### Deckbuilder Engine (`deckbuilder.py`)
- **Presentation Management**: Creates and manipulates PowerPoint presentations using python-pptx
- **Template System**: Loads PowerPoint templates and JSON mapping configurations
- **Layout Resolution**: Maps user slide types to PowerPoint layouts via JSON configuration
- **Content Rendering**: Supports rich text formatting, tables, and multimedia content
- **Singleton Pattern**: Ensures consistent state across MCP tool calls

### Template Analyzer (`tools.py`)
- **PowerPoint Inspection**: Extracts layout and placeholder information from .pptx files
- **JSON Generation**: Creates template mapping files with actual PowerPoint names
- **Environment Integration**: Uses standard template and output folder paths
- **Automation Support**: Enables template analysis via test scripts

### Configuration System
- **JSON Mappings**: Template-specific layout and placeholder configurations
- **Environment Variables**: `DECK_TEMPLATE_FOLDER`, `DECK_OUTPUT_FOLDER` for path management
- **Fallback Strategy**: Graceful degradation when mappings are unavailable
- **Auto-Discovery**: Automatic copying of template files on first use

### Styling Engine (`table_styles.py`)
- **Table Formatting**: Comprehensive table styling with headers, borders, and colors
- **Theme Support**: Predefined color schemes and formatting options
- **Custom Colors**: Support for hex color overrides
- **Style Inheritance**: Consistent formatting across presentation elements
