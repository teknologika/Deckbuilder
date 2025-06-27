
# Deckbuilder - Task List

## Overview
This document tracks all tasks for building Deckbuilder, a Python library and accompanying MCP (Model Context Protocol) Server for intelligent PowerPoint presentation generation.
Tasks are organized by phase and component.

---

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

### 🧹 Code Quality Maintenance

**Priority: Medium - Ongoing cleanup items that don't block functionality**

- [ ] **Fix remaining flake8 E501 line length violations (56 total)**
  - [ ] Break long docstrings and function calls in `src/deckbuilder/cli_tools.py` (6 violations)
  - [ ] Fix line length in `src/deckbuilder/naming_conventions.py` (1 violation) 
  - [ ] Clean up `src/mcp_server/content_optimization.py` (1 violation)
  - [ ] Refactor `src/mcp_server/tools.py` (3 violations)
  - [ ] Break long strings in `tests/utils/content_generator.py` (45 violations)
  - [ ] Update CI to remove E501 from ignore list once fixed

- [ ] **Code formatting consistency**
  - [ ] Run `black --line-length 100 src/ tests/` after line length fixes
  - [ ] Ensure all new code follows 100-character limit
  - [ ] Add pre-commit hooks for automatic formatting

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

**Current Sprint**: Content Intelligence & Layout Expansion (Phase 3)
**Next Priority**: Convention-based naming system and layout intelligence implementation
**Completed**: ✅ Phase 1 & 2 - CLI tools, template management, and core MCP server
**Blockers**: None identified
**Target Completion**: Phase 3 - Content intelligence system - End of current sprint
**Last Updated**: 2025-01-26