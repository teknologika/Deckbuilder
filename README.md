# Deck Builder MCP

## Overview

The Deck Builder MCP is a Model Context Protocol (MCP) server that enables AI assistants to programmatically create and manipulate PowerPoint presentations. Built with Python and FastMCP, this server provides a comprehensive set of tools for generating professional presentations with multiple slide types, custom styling, and template support.

The server solves the common challenge of automating presentation creation by offering a JSON-based interface for defining slide content and structure. It's particularly useful for generating reports, dashboards, and structured presentations from data or user specifications.

**Technology Stack:**
- **Backend Framework:** FastMCP (Model Context Protocol)
- **Presentation Engine:** python-pptx
- **Transport:** stdio/SSE
- **Language:** Python 3.x
- **Configuration:** Environment variables with .env support

## Features

- **Multiple Slide Types:** Support for title slides, content slides, and data tables
- **Template-Based Generation:** Use custom PowerPoint templates or default layouts
- **JSON Configuration:** Define presentations using structured JSON data
- **Custom Table Styling:** Advanced table formatting with predefined styles and color overrides
- **Automatic File Versioning:** Intelligent file naming to prevent overwrites
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
pip install python-pptx fastmcp python-dotenv
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
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install python-pptx fastmcp python-dotenv
```

4. **Configure Claude Desktop:**

Add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "/path/to/deck-builder-mcp/.venv/bin/python",
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

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │    │  Deck Builder    │    │   PowerPoint    │
│  (Claude, etc.) │◄──►│   MCP Server     │◄──►│     Files       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Template       │
                       │   Management     │
                       └──────────────────┘
```

**Key Components:**
- **FastMCP Server:** Handles MCP protocol communication
- **Deckbuilder Class:** Core presentation management (singleton pattern)
- **Template System:** PowerPoint template loading and management
- **JSON Parser:** Converts structured data to presentation elements

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
- JSON data parsing and slide generation
- File versioning and output management

**`src/default.pptx`** - Default Template
- Fallback PowerPoint template with standard layouts
- Automatically copied to template directory if needed

### Available MCP Tools

1. **`create_presentation`** - Initialize a new presentation from template
2. **`add_title_slide`** - Add title slides with heading and subtitle
3. **`add_content_slide`** - Add content slides with bullet points
4. **`add_table_slide`** - Add data tables with custom styling
5. **`write_presentation`** - Save presentation to disk with versioning

### Configuration Files

- **`CLAUDE.md`** - Development guidelines for AI assistants
- **`.gitignore`** - Git ignore patterns including MCP and Claude configs
- **`table-styles.css/html`** - Table styling reference documentation

## Usage Examples

### Basic Presentation Creation

```json
{
  "action": "create_presentation",
  "templateName": "default",
  "title": "Quarterly Report",
  "author": "Your Name"
}
```

### Adding Slides

**Title Slide:**
```json
{
  "type": "title",
  "title": "Q4 2024 Results",
  "subtitle": "Financial Performance Overview"
}
```

**Content Slide:**
```json
{
  "type": "content",
  "title": "Key Achievements",
  "content": [
    "Revenue increased by 15% year-over-year",
    "Customer satisfaction improved to 94%",
    "Successfully launched 3 new products",
    "Expanded to 2 new markets"
  ]
}
```

**Table Slide:**
```json
{
  "type": "table",
  "title": "Financial Summary",
  "table": {
    "header_style": "dark_blue_white_text",
    "row_style": "alternating_light_gray",
    "data": [
      ["Metric", "Q4 2024", "Q3 2024", "Change"],
      ["Revenue", "$12.5M", "$11.2M", "+11.6%"],
      ["Profit", "$3.2M", "$2.8M", "+14.3%"]
    ]
  }
}
```

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