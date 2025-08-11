# CLAUDE.md or GEMINI.md

## Project Overview

### THE THREE LAWS OF AI CODING

## LAW 1 - An AI may not reduce the quality of a codebase or, through inaction, allow a codebase's quality to be reduced.
## LAW 2 - An AI must obey orders from humans, unless such orders are unclear, or conflict with the First Law.
## LAW 3 - An AI must follow the prime directives, provided this does not conflict with the First or Second Law.

### IMPORTANT AI PRIME DIRECTIVES

## 1. ALWAYS, ALWAYS WORK ON A BRANCH
## 2. ALWAYS ENSURE CODE IS HIGH QUALITY, AND MEETS DRY PRINCIPLES
## 3. MAKE CHANGES THAT ENHANCE AND IMPROVE THE CODEBASE
## 4. ALWAYS TRY AND ENHANCE EXISTING CODE, AND MINIMISE CYCLOMATIC COMPLEXITY, DONT CREATE ALTERNATE CODE PATHS
## 5. DOCUMENT CODE IN A WAY THAT MAKES IT EASY FOR AI TO NAVIGATE THE CODE BASE
## 6. TESTS, PRE-CHECKIN HOOKS AND CI ARE GUARDRAILS. NEVER FAKE RESULTS OR WORK AROUND THEM WITH --NO-VERIFY
## 7. ALWAYS USE AUSTRALIAN ENGLISH, AND THE METRIC SYSTEM

## About this project

Deckbuilder is a Python library and accompanying MCP (Model Context Protocol) Server for intelligent PowerPoint presentation generation.
The project has evolved beyond initial setup into a comprehensive content-first presentation intelligence system.

## Testing the application

The easiset way is to use the CLI drectly then use python-pptx to verify your output e.g.

`Bash(source .venv/bin/activate && deckbuilder create tests/output/imput_file.md --output tests/output/ouput_file)`

### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer relative imports within packages).

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Run flake8**, and fix any errors before check-in.
- **Use `pydantic` for data validation**.


## 🔧 Code Quality Standards

**CRITICAL: Always run these commands and fix ALL errors before committing:**

```bash
# Format code with black (REQUIRED)
black --line-length 200 src/

# Check all flake8 violations (REQUIRED)
flake8 src/ tests/ --max-line-length=200 --ignore=E203,W503,E501

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
- Maximum 200 characters per line (ignored in CI for now)
- Break long function calls, docstrings, and string literals when practical
- Use parentheses for continuation: `("long string part 1 "\n"part 2")`
- **Note**: E501 ignored in CI to focus on critical F-level errors first

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

Deckbuilder implements a **content-first design philosophy** with three key components:
1. **Presentation Engine**: PowerPoint generation with template support
2. **Content Intelligence**: Semantic analysis for layout recommendations
3. **Progressive Templates**: Expanding library of business presentation layouts

The system transforms LLMs from layout pickers into intelligent presentation consultants.

## Development Environment

Always use Python 3.11+ and activate the virtual environment:
```bash
source .venv/bin/activate
```

## ⚠️ IMPORTANT: MCP Server Environment Configuration

**When testing the engine directly (not through MCP)**, the presentation engine will fail to load template mappings because environment variables are not set. Environment variables are configured in the MCP server parameters, not in local `.env` files.

**MCP Server Configuration** (Claude Desktop config):
```json
{
  "env": {
    "DECK_TEMPLATE_FOLDER": "/path/to/deckbuilder/assets/templates",
    "DECK_OUTPUT_FOLDER": "/path/to/deckbuilder/output",
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
- **[Placeholder_Matching.md](docs/Features/Placeholder_Matching.md)**:
  - Hybrid semantic detection and JSON mapping system
  - Template analyzer workflow and JSON schema
  - Content placement strategies and troubleshooting
  - **Content Intelligence Storage Design** with Option 2 decision rationale

- **[Template_Discovery.md](docs/Features/Template_Discovery.md)**:
  - Content-first MCP tools design (analyze_presentation_needs, recommend_slide_approach, optimize_content_for_layout)
  - Complete end-to-end user workflow scenarios
  - Design evolution from layout-centric to content-first approach
  - Implementation roadmap and success criteria

- **[Supported_Templates.md](docs/Features/Supported_Templates.md)**:
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
8. **Format consistently**: Use `black --line-length 200 src/` before committing
9. **🚫 NO ROOT DIRECTORY POLLUTION**: Never create test files, output files, or temporary files in the root directory. Use appropriate subdirectories:
   - Test files: `/tests/` directory with proper structure
   - Output files: `/tests/output/` directory ONLY
   - Temporary files: Use Python's `tempfile` module or existing `/temp/` subdirectories
   - Integration tests: `/tests/integration/` directory
   - Debug scripts: `/tests/debug/` directory (temporary, must be cleaned up)
   - **NEVER create new directories in root** - use existing structure only

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

### Dynamic Multi-Shape Creation Verification

**CRITICAL**: Use this 4-step methodology to verify dynamic multi-shape system functionality:

```bash
# Step 1: Activate virtual environment
source .venv/bin/activate

# Step 2: Install package in editable mode
uv pip install -e .

# Step 3: Create presentation using CLI command
deckbuilder create tests/output/dynamic_shapes_test_markdown.md --output tests/output/cli_test_verification

# Step 4: Verify using python-pptx analysis
python verify_presentation.py "tests/output/cli_test_verification.YYYY-MM-DD_HHMM.g.pptx"
```

**Current Status - SYSTEM REQUIRES FIXES:**
- ❌ **Table Multiplication Bug**: Creating multiple tables (3) instead of 1 from single table markdown
- ❌ **Incorrect Sizing**: Tables not respecting row_height and dimension configurations
- ❌ **Poor Positioning**: Tables not positioned correctly relative to text content
- ⚠️ **Partial Success**: TEXT_BOX creation working, but overall system needs debugging

**Current Actual Results (BROKEN):**
```
📊 PRESENTATION SUMMARY:
   Total tables: 3  # ← PROBLEM: Should be 1
   Total dynamic text boxes: 1
   ⚠️ Tables found but positioning/sizing incorrect
```

**Required Fixes Before System is Production Ready:**
1. **Fix content splitting algorithm** - Prevent table duplication in `_split_mixed_content_intelligently()`
2. **Implement proper table sizing** - Respect frontmatter dimensions (row_height, table_width, column_widths)
3. **Fix positioning logic** - Ensure intelligent vertical spacing between text and table shapes
4. **Validate shape creation** - One table markdown = one table shape

**Test File Requirements:**
Use markdown frontmatter format with mixed content:
```markdown
---
layout: Title and Content
title: "Dynamic Multi-Shape Test"
style: dark_blue_white_text
content: |
  Content before table
  
  | **Column** | *Data* |
  | Test | Value |
  
  Content after table
---
```

**Verification Script Location:**
- `/verify_presentation.py` - Python script for analysing generated presentations
- Provides detailed shape analysis and dynamic system validation
- Reports on placeholders, tables, text boxes, and positioning

## 🔄 Content Processing Consolidation Plan

**STATUS**: Planned for implementation to eliminate multiple overlapping content paths

### Current State Problems
The system currently has **multiple overlapping content processing paths** that create complexity and maintenance burden:

#### Key Files with Content Processing:
1. **`content_processor.py`** - Markdown→slide data with legacy rich content format
2. **`converter.py`** - `markdown_to_canonical_json()` and structured frontmatter  
3. **`content_formatter.py`** - Content→PowerPoint rendering with dual format support
4. **`content_formatting.py`** - Universal formatting module (underutilized)
5. **`structured_frontmatter.py`** - Alternative structured frontmatter registry

#### Format Conflicts:
- **Legacy Format**: `{"heading": "Text", "level": 1}`
- **Canonical Format**: `{"type": "heading", "text": "Text", "level": 1}`
- **Dual Support**: ContentFormatter handles both, creating complexity

### Consolidation Strategy

#### Phase 0: Baseline (REQUIRED FIRST STEP)
**CRITICAL**: Must be completed before any consolidation work begins
```bash
# Run full test suite to establish baseline
pytest tests/

# Check code quality 
flake8 src/ tests/ --max-line-length=200 --ignore=E203,W503,E501

# Format code
black --line-length 200 src/

# Commit baseline state
git add -A
git commit -m "Baseline: Pre-content consolidation state

All tests passing, code formatted, ready for content processing consolidation.
Establishes known good state before structural changes.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### Phase 1: Format Unification
**Goal**: Standardize on canonical JSON format throughout system

**Actions:**
1. **Remove Legacy Format Support** from `content_formatter.py`
   - Remove `{"heading": "text"}` format handling
   - Keep only `{"type": "heading", "text": "text"}` format
   - Simplify detection logic in `add_simple_content_to_placeholder`

2. **Update content_processor.py** to output canonical format
   - Modify `_parse_rich_content()` to use `{"type": "heading"}` format
   - Ensure consistency with converter.py output

3. **Run tests after each change** - Phase 1 checkpoint

#### Phase 2: Method Cleanup  
**Goal**: Clear, single-responsibility methods with intuitive names

**Actions:**
1. **Rename Methods** for clarity:
   ```python
   # OLD                              # NEW
   add_simple_content_to_placeholder  → add_content_to_placeholder
   _add_rich_content_list_to_placeholder → _add_content_blocks_to_placeholder  
   _add_single_rich_content_block_to_placeholder → _add_content_block_to_placeholder
   ```

2. **Remove Deprecated Methods**:
   - `add_rich_content_to_slide` (marked DEPRECATED)
   - `add_simple_content_to_slide` (marked DEPRECATED)

3. **Run tests after each change** - Phase 2 checkpoint

#### Phase 3: File Consolidation
**Goal**: Clear separation of concerns with minimal overlap

**Proposed Structure:**
```
src/deckbuilder/
├── content/
│   ├── __init__.py
│   ├── processor.py        # Markdown → Canonical JSON 
│   ├── formatter.py        # Canonical JSON → PowerPoint
│   └── frontmatter.py      # Structured frontmatter handling
└── [other modules]
```

**Actions:**
1. Create new `content/` package
2. Migrate and consolidate functionality
3. Update all imports throughout codebase
4. Remove old files after migration
5. **Full test suite** - Phase 3 checkpoint

#### Phase 4: Final Validation
**Goal**: Ensure no regressions, clean up

**Actions:**
1. **Full regression testing**
2. **Verify heading hierarchy** still works 
3. **Check MCP tools** functionality
4. **Update documentation**
5. **Final commit**

### Expected Benefits
- ✅ **Single Content Format** - No more dual format handling
- ✅ **Clear Method Names** - Intuitive, self-documenting code
- ✅ **Reduced Complexity** - Fewer code paths, fewer bugs
- ✅ **Easier Maintenance** - Single source of truth
- ✅ **Better Performance** - No format detection overhead

### Implementation Requirements
1. **MUST start with Phase 0** - Establish baseline
2. **Test after each phase** - No regressions allowed
3. **Commit after each phase** - Rollback safety
4. **Keep heading hierarchy working** - Recent implementation must be preserved
