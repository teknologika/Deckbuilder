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

## Layered Content Architecture

Deckbuilder uses a sophisticated **layered content architecture** that enables multiple input approaches while maintaining template flexibility and layout intelligence. This architecture serves different user skill levels and use cases through distinct content field types.

### Content Flow Pipeline
```
User Input → Structured Processing → Content Formatting → Semantic Detection → Template Mapping → PowerPoint
```

### Content Field Layers

#### 1. **Input Layer** (User-Facing)
- **Basic Semantic Fields**: `content`, `title`, `subtitle`, `rich_content`
- **Purpose**: Simple, intuitive content authoring
- **Users**: Basic users, simple presentations
- **Example**: `{"title": "My Slide", "content": ["Bullet 1", "Bullet 2"]}`

#### 2. **Structured Layer** (Clean Authoring)
- **Structured Frontmatter**: `columns`, `sections`, `comparison`, `left/right`
- **Purpose**: Human-readable YAML with automatic conversion
- **Users**: Content creators, complex layouts
- **Example**: 
```yaml
columns:
  - title: Performance
    content: Fast processing
  - title: Security  
    content: Enterprise-grade
```

#### 3. **Template Layer** (Precise Control)
- **Direct Placeholder Fields**: `content_col1`, `title_left`, `image_1`
- **Purpose**: Exact PowerPoint placeholder mapping
- **Users**: Advanced users, custom templates
- **Example**: `{"title_col1": "Column 1 Title", "content_col1": "Column 1 Content"}`

#### 4. **Formatting Layer** (Processed Content)
- **Formatted Fields**: `content_formatted`, `rich_content_formatted`, `title_formatted`
- **Purpose**: Inline formatting applied (`**bold**`, `*italic*`, `___underline___`)
- **Users**: Internal processing pipeline
- **Example**: `{"text": "Bold text", "format": {"bold": True}}`

### Content Processing Components

#### **Structured Frontmatter Processor** (`structured_frontmatter.py`)
- Converts clean YAML to direct placeholder fields
- Supports 9 layout types with specific patterns
- Enables human-readable authoring with template precision
- **Input**: `columns: [{title, content}]` → **Output**: `title_col1`, `content_col1`

#### **Content Formatting Engine** (`content_formatting.py`)
- Universal formatting processor independent of structure
- Handles inline markdown: `**bold**`, `*italic*`, `___underline___`
- Processes all content types: strings, lists, rich content blocks
- **Input**: Raw content → **Output**: Structured formatting data

#### **Semantic Detection System** (`engine.py`)
- Intelligent placeholder detection and content routing
- Falls back from specific → generic field mapping
- Handles multiple content types in single processing pipeline
- **Priority**: Direct placeholders → Semantic fields → Generic mapping

#### **Template Mapping System** (`template JSON files`)
- Bridges semantic detection with actual PowerPoint placeholders
- Enables flexible template support through JSON configuration
- Maintains layout-specific intelligence and content optimization
- **Structure**: `{"1": "content_col1", "2": "content_col2"}`

### Architecture Benefits

#### **Multi-Level User Support**
- **Beginners**: Simple semantic fields (`content`, `title`)
- **Intermediate**: Structured frontmatter (clean YAML)
- **Advanced**: Direct placeholder control (`content_col1`)
- **Expert**: Custom template mapping and layout creation

#### **Template Flexibility**
- Works with any PowerPoint template through JSON mapping
- Maintains precise placeholder control when needed
- Enables intelligent content optimization per layout
- Supports progressive template enhancement

#### **Content Intelligence**
- Layout-specific content recommendations
- Automatic content optimization for chosen layouts
- Semantic content analysis for intelligent suggestions
- Progressive enhancement from simple to complex content

#### **Separation of Concerns**
- **Structure**: Layout and placeholder management
- **Content**: Text, formatting, and rich content blocks
- **Intelligence**: Content analysis and optimization
- **Rendering**: PowerPoint generation and formatting

### Design Decision Rationale

The multiple content field approaches are **intentional architectural layers**, not inconsistency:

1. **Flexibility**: Supports multiple user skill levels and use cases
2. **Intelligence**: Enables layout-specific content optimization
3. **Template Support**: Works with any PowerPoint template
4. **Progressive Enhancement**: Users can grow from simple to advanced usage
5. **Content-First**: Maintains focus on content over layout selection

This layered approach enables the content-first methodology while preserving the technical flexibility needed for professional presentation generation.

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
- **cli.py**: Standalone CLI interface with environment logic and user-friendly commands

### 3. Content Intelligence System
- **layout_intelligence.json**: Semantic metadata for layout recommendations
- **layout_intelligence.py**: Content matching algorithms
- **naming_conventions.py**: Standardized placeholder naming patterns
- **Hybrid Approach**: Semantic detection + JSON mapping for reliability

### 4. CLI Interface System
- **Environment Resolution Logic**: CLI args > environment variables > sensible defaults
- **Template Setup**: `deckbuilder init [PATH]` command for streamlined initialization
- **User-Friendly Commands**: Simplified arguments (`-t`, `-o`) with tab completion
- **Error Handling**: Actionable error messages with setup guidance
- **Environment Integration**: Bash profile examples and permanent configuration support

### 5. Template Management System
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
Design → Plan Mode → Feature Documentation → Create github issue → Implementation → Testing → Documentation → Commit → Push → Close issue as complete → Ask user to publish to PyPi or not.
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

### Content-First Testing Philosophy 🚨 CRITICAL LESSONS LEARNED

**The False Confidence Problem**: During v1.0.2 development, we discovered that 157/157 passing tests gave us false confidence while critical content mapping failures went undetected. This revealed a fundamental flaw in our testing approach.

#### Traditional Testing vs Content-First Testing

**❌ Traditional Approach (What We Had)**:
- Tests focused on "no crashes" instead of "correct output"
- Validated technical execution without verifying actual content placement
- Passing tests while slide content was completely broken
- Unit tests isolated from real PowerPoint generation

**✅ Content-First Testing (What We Need)**:
- **Test actual PowerPoint content**, not just successful API calls
- **Validate field mapping** for complex layouts (content_left_1, content_right_1, etc.)
- **Verify frontmatter processing** from YAML to slide content
- **End-to-end validation** of complete input → output workflows

#### Critical Testing Insights

**Root Cause Analysis**: We optimized for "no crashes" instead of "correct output", leading to:
- JSON complex field mapping broken (content_left_1, content_right_1 not placed)
- Markdown frontmatter title mapping broken (titles not appearing)
- Image insertion regression (previously working functionality)
- Silent failure detection problems

**The Template Mapping vs Content Generation Distinction**:
- ✅ **Template mapping works perfectly** - JSON structure correctly identifies layouts
- ✅ **Core PowerPoint engine works correctly** - When data reaches it, slides generate properly
- ❌ **Input processing pipelines broken** - JSON and Markdown preprocessing fails
- ❌ **Content placement mapping broken** - Complex field names not recognized

#### New Testing Standards

**Content Validation Requirements**:
1. **Read generated PowerPoint files** using python-pptx to extract actual text
2. **Verify specific content placement** in correct slide locations
3. **Test complex field mappings** (multi-column layouts, structured data)
4. **Validate complete workflows** from input format to final slide content

**Diagnostic Testing Framework**:
- **Pipeline isolation tests** - Separate template analysis from content generation
- **Content extraction validation** - Read actual PowerPoint slide text
- **Field mapping verification** - Test complex layout placeholder assignments
- **End-to-end workflow tests** - Complete input → output validation

### Test Organization
- **Unit Tests**: `/tests/deckbuilder/unit/` and `/tests/mcp_server/unit/`
- **Integration Tests**: `/tests/deckbuilder/integration/` and `/tests/mcp_server/integration/`
- **E2E Diagnostic Tests**: `/tests/deckbuilder/e2e/test_pipeline_diagnostics.py`
- **Test Data**: Comprehensive markdown files in `/tests/`
- **Fixtures**: Reusable test data and mock objects

### Key Test Files
- **`test_presentation.md`**: Primary structured frontmatter examples
- **`test_comprehensive_layouts.json`**: All layout validation data (20 slides)
- **`FormattingTest.md`**: Inline formatting (bold, italic, underline)
- **`TestPrompt.md`**: Real-world user scenarios
- **`test_pipeline_diagnostics.py`**: Critical content mapping validation

### Template Testing
```bash
# Analyze template structure with validation
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate comprehensive documentation
python src/deckbuilder/cli_tools.py document default

# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default
```

### Content-First Testing Commands
```bash
# Run diagnostic tests to isolate pipeline failures
pytest tests/deckbuilder/e2e/test_pipeline_diagnostics.py -v -s

# Test actual content generation and validation
python -m pytest tests/deckbuilder/e2e/ -v --tb=short

# Generate test presentations and validate content
deckbuilder create tests/deckbuilder/test_comprehensive_layouts.json --output test_validation
```

## Current Implementation Status

### ✅ Completed Features
- Core presentation engine with structured frontmatter support
- Template system with semantic detection and JSON mapping
- Content-first MCP tools (placeholder implementations)
- CLI template management tools (analyze, document, validate, enhance)
- Master slide enhancement with backup system
- Comprehensive testing framework (50+ tests)

### ✅ Completed: PlaceKitten Image Processing & Deckbuilder Integration ✅ 
1. ✅ **Asset Cleanup** - Flatten image directory structure for cleaner paths
2. ✅ **Core Library Implementation** - Basic placeholder generation with existing kitten images
3. ✅ **Intelligent Cropping Engine** - Computer vision-based automatic cropping for optimal composition
4. ✅ **Filter Pipeline System** - Professional image processing with method chaining
5. ✅ **Advanced Computer Vision** - Smart cropping with face detection, 9-step visualization
6. ✅ **PlaceKitten-Deckbuilder Integration** - Complete smart fallback system with professional styling
7. ✅ **Comprehensive Testing** - 108 tests including 18 PlaceKitten + 15 integration tests
8. ✅ **MCP Tool Enhancement** - Full image support documentation and USER CONTENT POLICY

### 🚀 Current Priority: CLI Tools & PyPI Package Development
**Development Focus**: Transition from MCP-only to standalone CLI tools and PyPI distribution

#### Smart Image Fallback Architecture ✅ IMPLEMENTED
```
YAML/JSON Input → Parse image_path → Validate File Exists
         ↓ (if missing/invalid)  
PlaceKitten Fallback → Grayscale Filter → Smart Crop → PowerPoint Insert
         ↓ (performance optimization)
Image Cache → Professional Styling → Dimension Matching → File Generation
```

**Achieved Goals**:
- ✅ **Professional Presentation Context**: Grayscale filtering for business-appropriate placeholders
- ✅ **Intelligent Sizing**: Smart crop to exact PowerPoint placeholder dimensions  
- ✅ **Seamless Integration**: No user intervention required for fallback generation
- ✅ **Performance Optimization**: Cached generation to avoid duplicate processing
- ✅ **Comprehensive Testing**: File size validation confirms images actually appear in PowerPoint

#### Enhanced YAML Structure
```yaml
layout: Picture with Caption
title: System Architecture
media:
  image_path: "assets/architecture_diagram.png"  # Primary image source
  alt_text: "System architecture overview"       # Accessibility support  
  caption: "High-level system architecture"      # Existing caption field
  description: "Main components include..."      # Existing description
```

**Backward Compatibility**: Existing presentations without image_path continue to work with PlaceKitten fallbacks

#### PowerPoint Integration Workflow
1. **Placeholder Detection**: Identify `PP_PLACEHOLDER_TYPE.PICTURE` placeholders in templates
2. **Image Validation**: Check file existence, format, and accessibility
3. **Smart Fallback**: Generate PlaceKitten with professional styling (grayscale + smart crop)
4. **Dimension Matching**: Resize to exact placeholder bounds with aspect ratio preservation
5. **Image Insertion**: Use `python-pptx` `placeholder.insert_picture()` for seamless placement

#### Implementation Components
- **ImageHandler**: Core image file validation, processing, and error handling
- **PlaceKittenIntegration**: Bridge between PlaceKitten library and Deckbuilder engine
- **Enhanced Engine**: Extended placeholder detection and image insertion capabilities
- **Cached Generation**: Performance optimization for identical fallback requests

### 🛠️ Next Development Phases

#### Phase A: Documentation & Planning Cleanup
- **Complete Documentation Overhaul**
  - PlaceKitten API documentation with comprehensive examples and integration patterns
  - Updated README showcasing new image capabilities and complete feature set
  - Feature documentation in `/docs/Features/` for all major components
  - Integration guides for both MCP server and standalone CLI usage

#### Phase B: Standalone CLI Tools Development  
- **Independent CLI Architecture**
  - Standalone entry point separate from MCP server for local development
  - Enhanced template analysis with detailed reporting and validation
  - Direct presentation generation: `deckbuilder create presentation.md`
  - Debug tools for template validation, image testing, and troubleshooting

- **CLI Environment Logic Improvements** 🚧 IN PROGRESS
  - Environment variable resolution priority: CLI args > env vars > defaults
  - `deckbuilder init [PATH]` command for streamlined template setup
  - Simplified global arguments: `-t/--templates`, `-o/--output`
  - Enhanced error messages with actionable guidance
  - Environment variable setup guidance and bash_profile examples
  - Tab completion support for commands, templates, and file paths
  - **Reference**: [CLI Design Specification](docs/Features/Deckbuilder_CLI.md)

- **User Experience Enhancement**
  - Simplified workflows with intuitive command structure
  - Progress indicators and clear feedback for all operations
  - Comprehensive error handling with helpful suggestions
  - Configuration management for CLI preferences and settings

- **Local Development Ecosystem**
  - Testing utilities for presentations without MCP server dependency
  - Template management operations via command line
  - PlaceKitten generation and testing tools for image development
  - Performance profiling for optimization and monitoring

#### Phase C: PyPI Package Distribution
- **Professional Package Structure**
  - Optimized setup.py with proper dependencies and entry points
  - Comprehensive manifest files including templates and documentation
  - Command registration: `pip install deckbuilder` → global `deckbuilder` command
  - PyPI-ready documentation with installation and usage guides

- **Distribution & Publishing**
  - Semantic versioning strategy with automated changelog generation
  - Security scanning and dependency vulnerability management
  - Test PyPI validation followed by production release
  - Integration testing with real-world installation scenarios

### 📋 Current Development Issues

#### 🚨 Critical Content Mapping Failures (v1.0.2 Discovery)
- **JSON Complex Field Mapping Broken** - [GitHub Issue #26](https://github.com/teknologika/Deckbuilder/issues/26)
  - content_left_1, content_right_1, etc. not being placed in slides
  - Template mapping works, but content processing pipeline fails
  - Priority: Critical - Core functionality broken
  
- **Markdown Frontmatter Title Mapping Broken** - [GitHub Issue #27](https://github.com/teknologika/Deckbuilder/issues/27)
  - YAML frontmatter titles not appearing in generated slides
  - Schema validation or processing pipeline issue
  - Priority: Critical - Primary input format broken

- **Image Placeholders Not Being Inserted** - [GitHub Issue #29](https://github.com/teknologika/Deckbuilder/issues/29)
  - REGRESSION: Previously working functionality now broken
  - PlaceKitten integration not placing images in placeholders
  - Priority: Critical - Loss of existing functionality

- **Images Being Scaled Instead of Intelligently Cropped** - [GitHub Issue #30](https://github.com/teknologika/Deckbuilder/issues/30)
  - Should use smart cropping algorithms, not basic scaling
  - Professional presentation quality compromised
  - Priority: High - Quality improvement needed

- **CLI UX Enhancement** - [GitHub Issue #10](https://github.com/teknologika/Deckbuilder/issues/10)
  - Transform messy flat CLI to professional hierarchical command structure
  - Implement comprehensive bash completion with multi-level tab completion
  - Design: [CLI_Reorganization.md](docs/Features/CLI_Reorganization.md)
  - Priority: High - Significant user experience improvement

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

### Code Quality Metrics ✅ ACHIEVED
- ✅ **Zero flake8 F-level errors** in CI/CD pipeline (all critical violations resolved)
- ✅ **108 passing tests** across unit, integration, and PlaceKitten test suites  
- ✅ **100% of new features** include comprehensive unit tests with proper coverage
- ✅ **All files under 500 lines** with clear modular organization and separation of concerns

### Feature Completion Metrics ✅ ACHIEVED  
- ✅ **PlaceKitten Library**: Complete image processing with smart cropping and filters
- ✅ **MCP Integration**: Seamless placeholder image generation in presentation workflows
- ✅ **Performance Targets**: <2s image processing, <5s smart crop with visualization
- ✅ **Image Integration**: Smart fallback system with professional styling and caching
- ✅ **User Experience**: Comprehensive MCP tools with USER CONTENT POLICY
- 🚧 **CLI Tools**: Template analysis exists, needs standalone presentation generation
- 🚧 **PyPI Package**: Ready for distribution preparation and publication

### Next Phase Targets
- **Standalone CLI**: Independent command-line tools for local development
- **PyPI Distribution**: Professional package with `pip install deckbuilder` support
- **Documentation**: Complete API docs and integration guides
- **User Experience**: Simplified workflows for both CLI and MCP usage

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

## Architectural Lessons Learned 🚨 CRITICAL

### The False Confidence Anti-Pattern

**How Content Mapping Failures Went Undetected**:
1. **Unit Tests Passed** - Individual components worked in isolation
2. **Integration Tests Passed** - API calls succeeded without errors
3. **CI/CD Pipeline Passed** - All 157 tests reported success
4. **Actual Output Broken** - PowerPoint slides contained no user content

**Root Cause**: We optimized for "no crashes" instead of "correct output"

### Development Philosophy Changes

**Before (❌ Wrong Approach)**:
- Trust unit tests in isolation
- Assume API success means correct output
- Focus on technical implementation details
- Validate system behavior, not user outcomes

**After (✅ Correct Approach)**:
- **Content-First Testing**: Validate actual PowerPoint slide content
- **End-to-End Validation**: Test complete user workflows
- **Output Verification**: Read generated files, don't trust API responses
- **Regression Prevention**: Test existing functionality with each change

### Regression Prevention Strategy

**How Regressions Happened**:
- Image insertion was working, then mysteriously broke
- No tests validated actual image placement in PowerPoint files
- Changes to content processing pipeline went unnoticed
- Complex field mappings silently failed

**Prevention Measures**:
1. **Golden File Testing** - Compare actual output against known good files
2. **Content Extraction Tests** - Read PowerPoint files to verify content
3. **Workflow Integration Tests** - Test complete user scenarios
4. **Regression Test Suite** - Automated validation of previously working features

### Future Development Guidelines

**Never Again**: Allow tests to pass while core functionality is broken
**Always**: Validate actual user outcomes, not just technical execution
**Require**: End-to-end testing for all content processing features
**Mandate**: Regression tests for any previously working functionality

## Future Vision

Deckbuilder aims to become the definitive content-first presentation generation system, transforming how users interact with PowerPoint creation by:

1. **Intelligent Content Analysis** - Understanding communication goals before technical implementation
2. **Semantic Layout Matching** - AI-powered recommendations based on content structure and intent
3. **Progressive Template Library** - Comprehensive business presentation layout coverage
4. **Seamless Integration** - Single MCP tool for complete presentation workflows
5. **Enterprise Scalability** - Template management system for organizational consistency

This planning document serves as the architectural foundation referenced by CLAUDE.md for all development decisions and feature implementations.
