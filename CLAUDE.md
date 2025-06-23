# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) Server for building PowerPoint presentations. The project has evolved beyond initial setup into a comprehensive content-first presentation intelligence system.

## 🔧 Code Quality Standards

**CRITICAL: Always run these commands and fix ALL errors before committing:**

```bash
# Format code with black (REQUIRED)
black --line-length 100 src/

# Check all flake8 violations (REQUIRED)  
flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503

# Run tests to ensure no regressions (REQUIRED)
pytest tests/
```

**⚠️ ZERO TOLERANCE POLICY: No commits allowed with flake8 F-level errors (F401, F841, F811, F541, etc.)**

### Code Quality Rules

**Imports (Critical F-level violations):**
- Remove ALL unused imports (F401) - check each import statement
- Import order: stdlib → third-party → local, alphabetical within groups
- Use `# noqa: E402` only when imports must follow `sys.path.insert()`
- Never duplicate imports (F811)

**Variables (Critical F-level violations):**
- Remove ALL unused variables (F841) - either use them or delete them
- Use `_` for intentionally unused variables: `for _, item in enumerate(items)`
- Comment out variables for future use: `# content_length = len(content)  # Future: use for analysis`

**F-strings (Critical F-level violations):**
- Fix ALL f-strings without placeholders (F541): `f"Hello"` → `"Hello"`
- Only use f-strings when you have variables: `f"Hello {name}"`

**Line Length (E501 - Style violations):**
- Maximum 100 characters per line
- Break long function calls, docstrings, and string literals
- Use parentheses for continuation: `("long string part 1 "\n"part 2")`

### Enforcement Strategy
1. **Pre-commit**: Always run `flake8` before any commit
2. **Zero F-errors**: F-level errors MUST be fixed immediately  
3. **Style consistency**: Use `black` for automatic formatting
4. **Test coverage**: Ensure all code changes include relevant tests

### CI Integration
The project includes GitHub Actions workflows that enforce code quality:

- **`.github/workflows/test.yml`**: Runs pytest and flake8 on every push/PR
- **`.github/workflows/claude-code-review.yml`**: Claude-powered code review for PRs

**CI Requirements:**
- All tests must pass (50+ tests including engine, template processing, etc.)
- Zero flake8 F-level errors (F401, F841, F811, F541) 
- Python 3.11+ compatibility required



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

Always use Python 3.11+ and activate the virtual environment:
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

# How you work
1. Design a feature first, remind me to put you into plan-only mode
2. Save that design into ./docs/Features/feature_name.md
3. At the bottom of the design put a TODO which you implement as we go. 

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

### Phase 1: Content-First MCP Tools ✅ COMPLETED
1. ✅ `analyze_presentation_needs()` - Content and goal analysis (placeholder implemented)
2. ✅ `recommend_slide_approach()` - Layout recommendations (placeholder implemented)
3. ✅ `optimize_content_for_layout()` - Content optimization and YAML generation (placeholder implemented)

### Phase 2: Template Management System ✅ COMPLETED
1. ✅ **CLI Template Management Tools** - Comprehensive command-line utilities
   - `analyze` - Template structure analysis with detailed validation
   - `document` - Auto-generated comprehensive template documentation
   - `validate` - Template and mapping validation with specific fix suggestions
   - `enhance` - Master slide placeholder modification with organized backup system
2. ✅ **Master Slide Enhancement** - Direct PowerPoint template modification using python-pptx
3. ✅ **Organized File Management** - `.g.pptx` convention and dedicated backup folders
4. ✅ **Comprehensive Documentation** - Updated user guides and technical specifications

### Phase 3: Content Intelligence & Layout Expansion (Current Focus)
1. **Convention-Based Naming System** - Standardized placeholder naming patterns
2. **Layout Intelligence Implementation** - `src/layout_intelligence.json` with semantic metadata
3. **Content Matching Algorithms** - Smart layout recommendations based on content analysis
4. **Template Library Expansion** - Progressive implementation of 50+ layouts from `SupportedTemplates.md`
5. **Performance Optimization** - Enhanced content intelligence and comprehensive testing

## Important Instructions

1. **🔧 CODE QUALITY FIRST**: Always run `flake8` and fix ALL F-level errors before any commit
2. **Always design a feature first, and ask me to review the design before implementing it**
3. **Follow content-first principles**: Start with user needs, not system capabilities
4. **Maintain separation of concerns**: Technical structure vs semantic intelligence
5. **Document decisions**: Update feature docs when making design choices
6. **Test with real scenarios**: Use actual user presentation needs for validation
7. **Clean imports**: Remove unused imports (F401) and variables (F841) immediately
8. **Format consistently**: Use `black --line-length 100 src/` before committing

## Testing & Validation

When tests fail, ask the user how to fix them before actually fixing them.

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

#### Template Management CLI Tools
- **`src/deckbuilder/cli_tools.py`**: Comprehensive template management utilities
  - Extracts PowerPoint template structure with detailed validation
  - Generates JSON mappings and comprehensive documentation
  - Enhances templates with master slide placeholder modification
  - Provides organized backup system and error reporting

### Running Tests

#### Template Analysis and Enhancement
Generate JSON mappings and enhance PowerPoint templates:
```bash
# Analyze template structure with validation
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate comprehensive documentation
python src/deckbuilder/cli_tools.py document default

# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default

# Enhance template with corrected placeholder names
python src/deckbuilder/cli_tools.py enhance default
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

## Implementation Roadmap

### ✅ Completed Features
- [x] Core presentation engine with structured frontmatter support
- [x] Template system with semantic detection and JSON mapping
- [x] Layout selection fix (prefer `layout` field over `type` field)
- [x] Enhanced placeholder naming (copy descriptive names from template mapping)
- [x] File-based MCP tool (`create_presentation_from_file`)
- [x] JSON object input fix (changed from string to dict parameter)

### 🚧 Template Management System (Current Focus)

#### Phase 1: Command-Line Tools ✅ COMPLETED
- [x] **Create standalone template analysis utility**
  - [x] Build `src/deckbuilder/cli_tools.py` with command-line interface
  - [x] Add environment-independent path handling
  - [x] Test with default template analysis

- [x] **Implement template validation**
  - [x] Add `validate` command to CLI tool
  - [x] Cross-reference JSON mapping with actual template structure
  - [x] Validate template file accessibility
  - [x] Check JSON mapping completeness

- [x] **Create documentation generator**
  - [x] Add `document` command to CLI tool
  - [x] Generate markdown docs with layout tables
  - [x] Include placeholder details and usage examples
  - [x] Auto-sync with template analysis results
  
- [ ] **Update the user documentation

**CLI Usage Examples:**
```bash
# Analyze template structure
python src/deckbuilder/cli_tools.py analyze default --verbose

# Generate comprehensive documentation  
python src/deckbuilder/cli_tools.py document default

# Validate template and mappings
python src/deckbuilder/cli_tools.py validate default

# Custom paths
python src/deckbuilder/cli_tools.py analyze custom --template-folder ./my-templates
```

#### Phase 2: Template Enhancement
- [ ] **Master slide placeholder modification**
  - [ ] Research python-pptx master slide editing capabilities
  - [ ] Implement `enhance_template` MCP tool
  - [ ] Add backup and versioning system
  - [ ] Test placeholder name updates on master slides
  - [ ] Update the user documentation

- [ ] **Convention-based naming system**
  - [ ] Define naming patterns for all layout types
  - [ ] Implement pattern detection algorithms
  - [ ] Auto-generate structured frontmatter patterns
  - [ ] Add naming convention validation

#### Phase 3: Complete Structured Frontmatter Support
- [ ] **Add missing layout patterns**
  - [ ] Four Columns With Titles structured pattern
  - [ ] SWOT Analysis structured pattern  
  - [ ] Agenda structured pattern
  - [ ] Big Number structured pattern
  - [ ] Title Only, Blank, Section Header patterns

- [ ] **Dynamic pattern generation**
  - [ ] Replace hard-coded patterns with convention-based detection
  - [ ] Auto-generate YAML structures from JSON mappings
  - [ ] Unified registry for all 19 layouts
  - [ ] Backward compatibility with existing patterns

  - [ ] Update the user documentation

### 📋 Future Enhancements
- [ ] **Content-First MCP Tools**
  - [ ] `analyze_presentation_needs()` - Content and goal analysis
  - [ ] `recommend_slide_approach()` - Layout recommendations
  - [ ] `optimize_content_for_layout()` - Content optimization

- [ ] **Advanced Template Features**
  - [ ] Template comparison and migration tools
  - [ ] Custom template creation wizard
  - [ ] Template validation CI/CD integration
  - [ ] Multi-template support and switching

### 🔧 Technical Debt
- [ ] **Code Organization**
  - [ ] Consolidate template analysis code
  - [ ] Improve error handling across MCP tools
  - [ ] Add comprehensive logging
  - [ ] Create unit tests for template management

- [ ] **Documentation Updates**
  - [ ] Update README with new MCP tools
  - [ ] Add template creation user guide
  - [ ] Document naming conventions clearly
  - [ ] Create troubleshooting guide

## Progress Tracking

**Current Sprint**: Template Management System Phase 2
**Next Priority**: Master slide placeholder modification with python-pptx
**Completed**: ✅ Phase 1 - Command-line tools for template analysis, validation, and documentation
**Blockers**: None identified
**Target Completion**: Phase 2 - Week 2, Phase 3 - Week 3