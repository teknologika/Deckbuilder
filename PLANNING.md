# Deckbuilder - Project Planning Document

## Project Overview

This is a comprehensive Python library and MCP (Model Context Protocol) Server for building PowerPoint presentations with a **content-first design philosophy**. The system transforms LLMs from layout pickers into intelligent presentation consultants by understanding user communication goals before suggesting technical solutions.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server Layer                     │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │   FastMCP       │        │   Content-First    │     │
│  │   Endpoints     │◄──────►│   MCP Tools        │     │
│  └────────┬────────┘        └────────────────────┘     │
│           │                                              │
├───────────┼──────────────────────────────────────────────┤
│           │           Presentation Engine                │
│  ┌────────▼────────┐        ┌────────────────────┐     │
│  │  PowerPoint     │        │   Template         │     │
│  │  Generation     │◄──────►│   Management       │     │
│  └────────┬────────┘        └────────────────────┘     │
│           │                                              │
├───────────┼──────────────────────────────────────────────┤
│           │          PlaceKitten Image Processing        │
│  ┌────────▼────────┐        ┌────────────────────┐     │
│  │   Intelligent   │        │   Filter Pipeline  │     │
│  │   Cropping      │◄──────►│   & Processing     │     │
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

## Core Design Principles

### 1. Content-First Methodology
- **Never start with "what layouts exist?"**
- **Always start with "what does the user want to communicate?"**
- Understand user content and communication goals first
- Recommend presentation structure based on message intent
- Suggest optimal layouts with audience consideration
- Optimize content for chosen layouts

### 2. Modular Architecture
- **Maximum file size: 500 lines of code**
- Clear separation of concerns between components
- Reusable modules grouped by feature or responsibility
- Clean dependency injection and interfaces

### 3. Type Safety & Code Quality
- **Zero tolerance for flake8 F-level errors** (F401, F841, F811, F541)
- Comprehensive type hints using Python 3.11+ features
- Pydantic for data validation and serialization
- Black formatting with 100-character line length

### 4. Testing-First Development
- **Every new feature requires pytest unit tests**
- Minimum test coverage: 1 expected use, 1 edge case, 1 failure case
- Tests mirror main app structure in `/tests` folder
- Integration tests for end-to-end workflows

## System Components

### 1. MCP Server Layer (`/src/mcp_server/`)
- **main.py**: FastMCP server with lifespan management and context
- **tools.py**: MCP tool implementations (create_presentation, analyze_needs, etc.)
- **Content-First Tools**:
  - `analyze_presentation_needs()` - Content and goal analysis
  - `recommend_slide_approach()` - Layout recommendations
  - `optimize_content_for_layout()` - Content optimization and YAML generation

### 2. Presentation Engine (`/src/deckbuilder/`)
- **engine.py**: Core PowerPoint generation using python-pptx
- **structured_frontmatter.py**: YAML → JSON → PowerPoint conversion
- **placeholder_types.py**: Template placeholder detection and mapping
- **table_styles.py**: Professional table formatting system
- **cli_tools.py**: Command-line template management utilities

### 3. Content Intelligence System
- **layout_intelligence.json**: Semantic metadata for layout recommendations
- **layout_intelligence.py**: Content matching algorithms
- **naming_conventions.py**: Standardized placeholder naming patterns
- **Hybrid Approach**: Semantic detection + JSON mapping for reliability

### 4. Template Management System
- **CLI Tools**: analyze, document, validate, enhance commands
- **Master Slide Enhancement**: Direct PowerPoint template modification
- **Organized File Management**: `.g.pptx` convention with backup system
- **Progressive Implementation**: 50+ business presentation layouts planned

## Technical Stack

### Core Technologies
- **Python 3.11+**: Primary language with modern type hints
- **FastMCP**: Model Context Protocol server framework
- **python-pptx**: PowerPoint generation and manipulation
- **PyYAML**: Structured frontmatter processing
- **Pydantic**: Data validation and serialization

### Development Tools
- **pytest + pytest-cov**: Testing framework with coverage
- **black**: Code formatting (100-character lines)
- **flake8**: Linting with zero tolerance for F-level errors
- **GitHub Actions**: CI/CD with automated testing and code review

## Development Workflow

### 1. Feature Development Process
```
Design → Plan Mode → Feature Documentation → Implementation → Testing → Documentation
```

1. **Always design a feature first** and request plan-only mode
2. **Save design to `./docs/Features/feature_name.md`**
3. **Add TODO section at bottom of design for implementation tracking**
4. **Implement with comprehensive testing**
5. **Update TASK.md with completion status**

### 2. Code Quality Standards

**CRITICAL: Always run before committing:**
```bash
# Format code with black (REQUIRED)
black --line-length 100 src/

# Check all flake8 violations (REQUIRED)
flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503,E501

# Run tests to ensure no regressions (REQUIRED)
pytest tests/
```

**F-Level Error Policy:**
- **F401**: Remove ALL unused imports immediately
- **F841**: Remove ALL unused variables (or use `_` for intentional)
- **F811**: Never duplicate imports
- **F541**: Fix f-strings without placeholders

### 3. Task Management
- **Check TASK.md before starting new tasks**
- **Add new tasks with brief description and today's date**
- **Mark completed tasks immediately after finishing**
- **Add discovered sub-tasks to "Discovered During Work" section**

## Environment Configuration

### MCP Server Setup
Environment variables configured in MCP server parameters (not local `.env`):

```json
{
  "env": {
    "DECK_TEMPLATE_FOLDER": "/path/to/deckbuilder/assets/templates",
    "DECK_OUTPUT_FOLDER": "/path/to/deckbuilder/output",
    "DECK_TEMPLATE_NAME": "default"
  }
}
```

### Development Environment
```bash
# Always activate virtual environment
source venv/bin/activate

# Python 3.11+ required
python --version  # Should show 3.11+
```

## Testing Strategy

### Test Organization
- **Unit Tests**: `/tests/deckbuilder/unit/` and `/tests/mcp_server/unit/`
- **Integration Tests**: `/tests/deckbuilder/integration/` and `/tests/mcp_server/integration/`
- **Test Data**: Comprehensive markdown files in `/tests/`
- **Fixtures**: Reusable test data and mock objects

### Key Test Files
- **`test_presentation.md`**: Primary structured frontmatter examples
- **`test_comprehensive_layouts.json`**: All layout validation data
- **`FormattingTest.md`**: Inline formatting (bold, italic, underline)
- **`TestPrompt.md`**: Real-world user scenarios

### Template Testing
```bash
# Analyze template structure with validation
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate comprehensive documentation
python src/deckbuilder/cli_tools.py document default

# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default
```

## Current Implementation Status

### ✅ Completed Features
- Core presentation engine with structured frontmatter support
- Template system with semantic detection and JSON mapping
- Content-first MCP tools (placeholder implementations)
- CLI template management tools (analyze, document, validate, enhance)
- Master slide enhancement with backup system
- Comprehensive testing framework (50+ tests)

### 🖼️ Current Focus: PlaceKitten Image Processing Library
1. **Asset Cleanup** - Flatten image directory structure for cleaner paths
2. **Core Library Implementation** - Basic placeholder generation with existing kitten images
3. **Intelligent Cropping Engine** - Computer vision-based automatic cropping for optimal composition
4. **Filter Pipeline System** - Professional image processing with method chaining
5. **MCP Integration** - Seamless integration with presentation generation workflows
6. **Advanced Features** - Batch processing, performance optimization, and comprehensive testing

### 📋 Future Enhancements
- **Content Intelligence & Layout Expansion**
  - Convention-based naming system and standardized placeholder patterns
  - Layout intelligence implementation with full semantic metadata system
  - Content matching algorithms for smart recommendations based on analysis
  - Template library expansion with progressive 50+ layout implementation
- **Advanced Template Features**
  - Template comparison and migration tools
  - Custom template creation wizard
  - Multi-template support and switching
  - Real-time content analysis and optimization

## Success Metrics

### Code Quality Metrics
- **Zero flake8 F-level errors** in CI/CD pipeline
- **50+ passing tests** across unit and integration suites
- **100% of new features** include comprehensive unit tests
- **All files under 500 lines** with clear modular organization

### Feature Completion Metrics
- **PlaceKitten Library**: Complete image processing with smart cropping and filters
- **MCP Integration**: Seamless placeholder image generation in presentation workflows
- **Performance Targets**: <2s image processing, <5s smart crop with visualization
- **Content-First Tools**: Analyze → Recommend → Optimize workflow (Future)
- **Template Coverage**: 50+ business presentation layouts implemented (Future)
- **User Experience**: Single command presentation generation from markdown

## Constraints & Limitations

### Technical Constraints
- **Python 3.11+ only** - Uses modern type hints and features
- **MCP Environment Variables** - Direct engine testing requires manual setup
- **PowerPoint Template Dependency** - Requires valid .pptx template files
- **File Size Limits** - Maximum 500 lines per source file

### Development Constraints
- **Zero F-Level Errors Policy** - Blocks all commits with critical linting errors
- **Testing Requirements** - Every feature needs comprehensive test coverage
- **Documentation Standards** - Feature designs saved to `/docs/Features/`
- **Content-First Approach** - Never start with technical layouts

## Future Vision

Deckbuilder aims to become the definitive content-first presentation generation system, transforming how users interact with PowerPoint creation by:

1. **Intelligent Content Analysis** - Understanding communication goals before technical implementation
2. **Semantic Layout Matching** - AI-powered recommendations based on content structure and intent
3. **Progressive Template Library** - Comprehensive business presentation layout coverage
4. **Seamless Integration** - Single MCP tool for complete presentation workflows
5. **Enterprise Scalability** - Template management system for organizational consistency

This planning document serves as the architectural foundation referenced by CLAUDE.md for all development decisions and feature implementations.
