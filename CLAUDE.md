# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) Server for building PowerPoint presentations. The project has evolved beyond initial setup into a comprehensive content-first presentation intelligence system.

**Current Status**: 
- ✅ Core presentation engine implemented with structured frontmatter support
- ✅ Template system with semantic detection and JSON mapping  
- 🚧 Content-first MCP tools in design phase
- 📋 50+ layout templates planned for progressive implementation

## Architecture

This project implements a **content-first design philosophy** with three key components:
1. **Presentation Engine**: PowerPoint generation with template support
2. **Content Intelligence**: Semantic analysis for layout recommendations  
3. **Progressive Templates**: Expanding library of business presentation layouts

The system transforms LLMs from layout pickers into intelligent presentation consultants.

## Development Environment

Always use Python 3 and activate the virtual environment:
```bash
source venv/bin/activate
```

## ⚠️ IMPORTANT: MCP Server Environment Configuration

**When testing the engine directly (not through MCP)**, the presentation engine will fail to load template mappings because environment variables are not set. Environment variables are configured in the MCP server parameters, not in local `.env` files.

**MCP Server Configuration** (Claude Desktop config):
```json
{
  "env": {
    "DECK_TEMPLATE_FOLDER": "/path/to/deck-builder-mcp/assets/templates",
    "DECK_OUTPUT_FOLDER": "/path/to/deck-builder-mcp/output", 
    "DECK_TEMPLATE_NAME": "default"
  }
}
```

**Impact on Development**:
- ✅ **MCP tools work correctly** - environment variables are available
- ❌ **Direct engine testing may fail** - missing template paths cause fallback to minimal layout mapping
- ❌ **Layout selection issues** - incorrect layouts selected when template mapping not loaded

**Testing Workaround**: When testing engine directly, manually set environment variables or expect fallback behavior with limited layouts.

## Design Approach

This project follows a **content-first methodology**:
1. **Understand user content and communication goals first**
2. **Recommend presentation structure based on message intent**  
3. **Suggest optimal layouts with audience consideration**
4. **Optimize content for chosen layouts**

Never start with "what layouts exist?" - always start with "what does the user want to communicate?"

## Key Design Decisions

### Content Intelligence Storage
- **Decision**: Separate `layout_intelligence.json` file (Option 2)
- **Rationale**: Clean separation of technical template structure from semantic content intelligence
- **Location**: `src/layout_intelligence.json` 
- **Integration**: Used by content-first MCP tools for layout recommendations

### Template Architecture  
- **Technical Structure**: `default.json` (placeholder mappings)
- **Semantic Intelligence**: `layout_intelligence.json` (content matching)
- **Documentation**: `SupportedTemplates.md` (implementation roadmap)
- **Hybrid Approach**: Semantic detection + JSON mapping for reliable content placement

## Feature Documentation

Refer to these comprehensive specifications before implementing:

### Core Feature Specifications
- **[PlaceholderMatching.md](docs/Features/PlaceholderMatching.md)**: 
  - Hybrid semantic detection and JSON mapping system
  - Template analyzer workflow and JSON schema
  - Content placement strategies and troubleshooting
  - **Content Intelligence Storage Design** with Option 2 decision rationale
  
- **[TemplateDiscovery.md](docs/Features/TemplateDiscovery.md)**:
  - Content-first MCP tools design (analyze_presentation_needs, recommend_slide_approach, optimize_content_for_layout)
  - Complete end-to-end user workflow scenarios
  - Design evolution from layout-centric to content-first approach
  - Implementation roadmap and success criteria
  
- **[SupportedTemplates.md](docs/Features/SupportedTemplates.md)**:
  - Progressive implementation roadmap for 50+ business presentation layouts
  - Status tracking with ✅/❌ indicators across 7 layout categories
  - Required placeholders and descriptions for each layout
  - Current: 12 implemented, 50+ planned

## Implementation Priorities

### Phase 1: Content-First MCP Tools (Current Focus)
1. `analyze_presentation_needs()` - Content and goal analysis
2. `recommend_slide_approach()` - Layout recommendations  
3. `optimize_content_for_layout()` - Content optimization and YAML generation

### Phase 2: Layout Intelligence
1. Create `src/layout_intelligence.json` with semantic metadata
2. Implement content matching algorithms
3. Test end-to-end content-first workflow

### Phase 3: Template Expansion
1. Progressive implementation of 50+ layouts from `SupportedTemplates.md`
2. Enhanced content intelligence for new layouts
3. Performance optimization and comprehensive testing

## Important Instructions

1. **Always design a feature first, and ask me to review the design before implementing it**
2. **Follow content-first principles**: Start with user needs, not system capabilities
3. **Maintain separation of concerns**: Technical structure vs semantic intelligence
4. **Document decisions**: Update feature docs when making design choices
5. **Test with real scenarios**: Use actual user presentation needs for validation

## Testing & Validation

### Test Files and Usage

The project includes comprehensive test files for validation:

#### Core Test Files
- **`tests/test_presentation.md`**: Primary markdown test with structured frontmatter examples
  - Tests Four Columns, Two Content, Comparison, and Picture with Caption layouts
  - Demonstrates clean YAML syntax and content optimization
  - Used for end-to-end presentation generation testing

- **`tests/test_structured_frontmatter.md`**: Extended structured frontmatter examples
  - Additional layout variations and edge cases
  - Content formatting and validation scenarios

- **`tests/FormattingTest.md`**: Inline formatting validation
  - Bold, italic, underline combinations
  - Complex formatting patterns and edge cases

- **`tests/TestPrompt.md`**: User scenario testing
  - Real-world presentation requests
  - Content-first workflow validation

#### Template Analysis Tools
- **`tests/test_tools.py`**: Template analyzer and environment setup
  - Extracts PowerPoint template structure
  - Generates JSON mappings for new templates
  - Sets up test environment with proper folder structure

### Running Tests

#### Template Analysis
Generate JSON mappings for PowerPoint templates:
```bash
cd tests
python test_tools.py
# Creates templateName.g.json files for customization
```

#### Presentation Generation Testing
Test structured frontmatter system:
```bash
# Through MCP client (Claude Desktop)
# Use create_presentation_from_markdown tool with test_presentation.md content
```

#### Manual Validation
1. **Content Placement**: Verify titles, content, and placeholders appear correctly
2. **Formatting**: Check bold, italic, underline rendering
3. **Layout Accuracy**: Ensure structured frontmatter maps to correct layouts
4. **Template Loading**: Verify JSON mappings work with PowerPoint templates

### Test Data Validation

The test files validate:
- **Structured frontmatter conversion**: YAML → JSON → PowerPoint
- **Content optimization**: 64% complexity reduction achieved
- **Layout intelligence**: Semantic content matching
- **Formatting preservation**: All inline formatting maintained
- **Template compatibility**: Works across different PowerPoint templates

### Output Validation

Generated presentations should demonstrate:
- Clean content placement without formatting explosion
- Proper layout selection based on content structure
- Accurate placeholder mapping using semantic detection + JSON fallback
- Professional appearance matching structured frontmatter specifications