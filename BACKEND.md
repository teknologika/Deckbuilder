# Backend Architecture

This document provides detailed information about the backend architecture, design patterns, and implementation details of the Deck Builder MCP server.

## Architecture Overview

The Deck Builder MCP server is built using a layered architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Protocol Layer                   │
│  (FastMCP Server - Handles MCP communication)          │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   Tool Layer                           │
│  (MCP Tools - create_presentation, add_slides, etc.)   │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                 Business Logic Layer                   │
│        (Deckbuilder Class - Presentation Management)   │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Presentation Engine Layer                 │
│           (python-pptx - PowerPoint Generation)        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                File System Layer                       │
│     (Template Management & Output File Handling)       │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns:** Each layer has a specific responsibility
2. **Singleton Pattern:** Single Deckbuilder instance manages presentation state
3. **Async/Await:** Full asynchronous support for non-blocking operations
4. **Environment Configuration:** Externalized configuration through environment variables
5. **Error Boundaries:** Comprehensive error handling at each layer

## Project Structure

```
deck-builder-mcp/
├── src/
│   ├── main.py              # MCP Server & Tool Definitions
│   ├── deckbuilder.py       # Core Business Logic
│   └── default.pptx         # Default Template
├── generated-docs/          # Documentation Output
├── table-styles.css         # Table Styling Reference
├── table-styles.html        # Table Styling Examples
├── CLAUDE.md               # AI Assistant Guidelines
├── README.md               # Project Documentation
└── .gitignore              # Git Ignore Configuration
```

### Core Components

**`src/main.py`** - MCP Server Implementation
- **Responsibilities:**
  - FastMCP server initialization and configuration
  - MCP tool registration and routing
  - Async context lifecycle management
  - Transport layer configuration (stdio/SSE)
  - Error handling and response formatting

**`src/deckbuilder.py`** - Presentation Engine
- **Responsibilities:**
  - PowerPoint presentation creation and management
  - Template loading and validation
  - Slide generation from JSON data
  - File versioning and output management
  - Singleton pattern implementation

## Data Flow

The data flow through the system follows a clear request-response pattern:

```
1. MCP Client Request
   ↓
2. FastMCP Server (Protocol Handling)
   ↓
3. Tool Function (Parameter Validation)
   ↓
4. Deckbuilder Instance (Business Logic)
   ↓
5. Python-PPTX (Presentation Generation)
   ↓
6. File System (Template/Output Management)
   ↓ 
7. Response (Success/Error Message)
   ↓
8. MCP Client (Result Display)
```

### Detailed Data Flow Examples

**Presentation Creation Flow:**
1. Client sends `create_presentation` request with template name
2. FastMCP server routes to `create_presentation` tool function
3. Tool function validates parameters and calls Deckbuilder
4. Deckbuilder checks template existence and initializes python-pptx
5. New presentation object is created and stored in singleton
6. Success response returned to client

**Slide Addition Flow:**
1. Client sends JSON slide data via `add_*_slide` tool
2. FastMCP server validates and routes request
3. Tool function passes JSON to Deckbuilder's `add_slide_from_json`
4. Deckbuilder parses JSON and determines slide type
5. Appropriate slide layout is selected from template
6. Python-pptx creates slide with specified content
7. Slide is added to current presentation object

**File Output Flow:**
1. Client requests `write_presentation` with filename
2. Deckbuilder checks output directory and existing files
3. Version management logic determines final filename
4. Python-pptx saves presentation to disk
5. File path confirmation returned to client

## Core Components

### FastMCP Server (`main.py`)

**Initialization:**
```python
mcp = FastMCP(
    "deckbuilder",
    description="MCP server for creation of powerpoint decks",
    lifespan=deckbuilder_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)
```

**Lifecycle Management:**
- **Context Creation:** `DeckbuilderContext` dataclass holds singleton instance
- **Async Context Manager:** Manages Deckbuilder lifecycle automatically
- **Resource Cleanup:** Ensures proper resource disposal on server shutdown

**Tool Registration:**
- **Async Tool Functions:** All tools use async/await pattern
- **Parameter Validation:** Type hints and validation for all parameters
- **Error Handling:** Try-catch blocks with descriptive error messages

### Deckbuilder Class (`deckbuilder.py`)

**Singleton Implementation:**
```python
@singleton
class Deckbuilder:
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
```

**Core Attributes:**
- `template_path`: Directory containing PowerPoint templates
- `template_name`: Default template filename
- `output_folder`: Directory for saving presentations
- `prs`: Current python-pptx Presentation object

**Key Methods:**

**`create_presentation(fileName, templateName)`**
- Loads specified template or creates blank presentation
- Clears any existing slides
- Initializes new presentation object

**`add_slide_from_json(json_data)`**
- Parses JSON string or dictionary
- Handles multiple JSON formats (single slide, multiple slides, presentation wrapper)
- Routes to appropriate slide creation method

**`_add_slide(slide_data)`**
- Determines slide type and layout
- Creates slide using python-pptx
- Populates content based on slide type

**`write_presentation(fileName)`**
- Implements version management
- Creates output directory if needed
- Saves presentation with .latest.pptx extension

### Template Management

**Template Discovery:**
1. Check environment variable `DECK_TEMPLATE_FOLDER`
2. Look for template in specified directory
3. Copy default template if not found
4. Handle file permissions gracefully

**Layout Mapping:**
```python
DEFAULT_LAYOUTS = {
    "title": "title",                # Title slide with subtitle
    "table": "titleandcontent",      # Slide with title and table
    "content": "titleandcontent",    # Slide with title and bullet points
    "section": "sectionHeader",      # Section divider slide
    "blank": "blank"                 # Blank slide
}

DEFAULT_PPT_LAYOUTS = {
    "title": 0,                    # Title Slide
    "titleandcontent": 1,          # Title and Content
    "sectionHeader": 2,            # Section Header
    # ... additional layouts
}
```

### JSON Processing

**Supported JSON Formats:**

**Single Slide:**
```json
{
  "type": "content",
  "title": "Slide Title",
  "content": ["Bullet 1", "Bullet 2"]
}
```

**Multiple Slides:**
```json
{
  "slides": [
    {"type": "title", "title": "Main Title"},
    {"type": "content", "title": "Content", "content": ["Point 1"]}
  ]
}
```

**Presentation Wrapper:**
```json
{
  "presentation": {
    "slides": [/* slide objects */]
  }
}
```

### Error Handling Strategy

**Layered Error Handling:**
1. **Parameter Validation:** Type checking and required field validation
2. **JSON Parsing:** Graceful handling of malformed JSON
3. **File System Operations:** Permission and existence checks
4. **Template Processing:** Missing template handling
5. **PowerPoint Generation:** python-pptx error handling

**Error Response Format:**
All errors are returned as descriptive strings prefixed with "Error":
```python
return f"Error {operation}: {str(exception)}"
```

### Performance Considerations

**Singleton Pattern Benefits:**
- Single presentation object in memory
- Avoids repeated template loading
- Maintains state across multiple tool calls

**Async Operations:**
- Non-blocking file I/O operations
- Concurrent request handling capability
- Improved responsiveness for multiple clients

**Memory Management:**
- Template caching reduces file system access
- Slide objects cleaned up automatically by python-pptx
- Garbage collection handles unused presentation objects

### Configuration Management

**Environment Variables:**
- `DECK_TEMPLATE_FOLDER`: Template directory path
- `DECK_TEMPLATE_NAME`: Default template filename
- `DECK_OUTPUT_FOLDER`: Output directory path
- `TRANSPORT`: MCP transport type (stdio/sse)
- `HOST`: Server host (for SSE transport)
- `PORT`: Server port (for SSE transport)
- `DEBUG`: Enable debug logging

**Configuration Loading:**
```python
load_dotenv()  # Load from .env file
template_path = os.getenv('DECK_TEMPLATE_FOLDER')
template_name = os.getenv('DECK_TEMPLATE_NAME')
output_folder = os.getenv('DECK_OUTPUT_FOLDER')
```

### Security Considerations

**File System Security:**
- Path validation to prevent directory traversal
- File permission checks before operations
- Graceful handling of access denied errors

**JSON Security:**
- Safe JSON parsing with error handling
- No arbitrary code execution from JSON content
- Input sanitization for file names

**Template Security:**
- Template files are read-only operations
- No dynamic template generation from user input
- Default template fallback prevents injection