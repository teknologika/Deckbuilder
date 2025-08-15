# Requirements for Slide Builder Refactor

## Overview
Complete refactoring of the 1,352-line slide_builder.py module into smaller, focused modules with clear separation of concerns. Remove all redundant code, eliminate legacy mapping systems, fix currently broken features, and remove markdown support within tables to simplify processing while maintaining zero breaking changes to external APIs.

## Current State Analysis

### Critical Issues
- **File size violation**: 1,352 lines (270% over 500-line limit)
- **Multiple responsibilities**: Single class handles 8+ distinct concerns
- **Massive code duplication**: Multiple table detection methods, placeholder finders, content processors
- **Legacy cruft**: 60+ lines of hardcoded field variations that should be configuration-driven
- **Broken features**: Some functionality currently not working due to complexity
- **Table complexity**: Markdown support within tables adds unnecessary processing overhead

### Current Responsibilities (All Mixed Together)
1. Slide lifecycle management (clear_slides, add_slide)
2. Placeholder discovery and semantic detection
3. Content formatting and application
4. Table processing and detection (with complex markdown parsing)
5. Dynamic shape creation
6. Field name resolution with hardcoded variations
7. Font and sizing calculations
8. Image and media handling coordination

## User Stories

### Story 1: Developer Maintainability
**As a developer working on deckbuilder**, I want the slide building code split into focused modules under 400 lines each, so that I can understand, modify, and extend functionality without getting lost in a massive file.

#### Acceptance Criteria
1. WHEN examining any slide building module THEN it SHALL be under 400 lines
2. WHEN looking at a module THEN it SHALL have exactly one clear responsibility
3. WHEN tracing code flow THEN dependencies SHALL be explicit and minimal

### Story 2: Code Quality and Maintenance
**As a maintainer**, I want all redundant code eliminated and legacy mapping removed, so that there's exactly one way to do each operation with no duplication.

#### Acceptance Criteria
1. WHEN searching for table detection logic THEN there SHALL be exactly one method
2. WHEN looking for placeholder finding THEN there SHALL be one unified approach
3. WHEN examining field mapping THEN there SHALL be no hardcoded variations dictionary
4. WHEN checking content processing THEN there SHALL be one canonical path per content type

### Story 3: System Reliability  
**As a user of the deckbuilder system**, I want all currently broken features fixed during the refactor, so that the system works reliably for all supported operations.

#### Acceptance Criteria
1. WHEN creating presentations THEN all layout types SHALL work correctly
2. WHEN processing tables THEN no duplication or positioning errors SHALL occur
3. WHEN handling mixed content THEN dynamic shapes SHALL be created properly
4. WHEN running existing tests THEN 100% SHALL pass without modification

### Story 4: Simplified Table Processing
**As a system processing table data**, I want tables to use plain text only (no markdown), so that table processing is fast, reliable, and maintainable without complex parsing overhead.

#### Acceptance Criteria
1. WHEN processing table cells THEN they SHALL contain plain text only
2. WHEN creating tables THEN no markdown parsing SHALL be performed
3. WHEN table content contains markdown THEN it SHALL be treated as plain text
4. WHEN tables are created THEN performance SHALL be significantly improved

## Functional Requirements

### FR1: Module Architecture
- **Slide Coordinator** (~300 lines): High-level slide creation orchestration
- **Placeholder Manager** (~350 lines): Placeholder discovery, semantic detection, mapping
- **Content Processor** (~400 lines): Content application to placeholders with formatting
- **Table Handler** (~300 lines): **SIMPLIFIED** table processing (plain text only, no markdown)
- **Shape Builder** (~400 lines): Dynamic shape creation and positioning
- **Layout Resolver** (~200 lines): Layout discovery and template mapping

### FR2: Elimination Requirements
- **Remove**: All redundant table detection methods
- **Remove**: Hardcoded field variations dictionary (60+ lines)
- **Remove**: Duplicate placeholder finding logic
- **Remove**: Multiple content processing paths
- **Remove**: Legacy mapping code that's no longer used
- **Remove**: Method name variations that serve same purpose
- **Remove**: **ALL markdown parsing within table cells**
- **Remove**: **Table markdown formatting preservation logic**
- **Remove**: **Complex table content detection for markdown**

### FR3: API Compatibility
- **Maintain**: All public method signatures unchanged
- **Maintain**: All return value formats identical
- **Maintain**: All dependency injection patterns
- **Maintain**: All error handling behavior
- **Changed**: Table cells will now contain plain text (markdown treated as literal text)

### FR4: Performance Requirements
- **Equal or better**: Processing speed for slide creation
- **Reduced**: Memory usage through elimination of duplicate code paths
- **Improved**: Code loading time through smaller modules
- **Significantly improved**: Table processing speed (no markdown parsing overhead)

### FR5: Table Processing Simplification
- **Plain text only**: Table cells contain raw text without any formatting
- **No markdown parsing**: Bold, italic, links treated as literal characters
- **Simplified detection**: Basic table structure detection only
- **Faster processing**: Elimination of complex formatting preservation logic
- **Cleaner code**: Table handler reduced from ~350 to ~300 lines

## Non-Functional Requirements

### NFR1: Code Quality Standards
- **Maximum file size**: 400 lines per module
- **Cyclomatic complexity**: Reduced by 50% minimum (more with table simplification)
- **Code duplication**: Zero tolerance - eliminated completely
- **Test coverage**: Maintain existing level (no regression)

### NFR2: Architecture Principles
- **Single Responsibility**: Each module handles exactly one concern
- **Dependency Inversion**: Modules depend on abstractions, not concretions
- **Open/Closed**: New functionality through extension, not modification
- **DRY Principle**: No duplicate code anywhere in the system
- **KISS Principle**: Tables use simplest possible plain text processing

### NFR3: Maintainability
- **Clear interfaces**: Each module has explicit, documented public API
- **Minimal coupling**: Modules interact through well-defined contracts
- **High cohesion**: Related functionality grouped together logically
- **Testable design**: Each module independently testable
- **Simplified table logic**: Easy to understand and modify table processing

## Success Criteria

### Quantitative Measures
1. **File count**: 6 focused modules replacing 1 massive file
2. **Line reduction**: Each module ≤ 400 lines (70% size reduction)
3. **Method reduction**: 60% fewer methods through elimination of duplicates and table simplification
4. **Test results**: 100% existing tests pass without modification
5. **Table performance**: 50%+ faster table processing with plain text

### Qualitative Measures
1. **Code clarity**: New developers can understand any module in < 15 minutes
2. **Change safety**: Modifications isolated to single modules
3. **Feature completion**: All currently broken functionality restored
4. **Zero regression**: No existing behavior changes (except table markdown → plain text)
5. **Table simplicity**: Table processing logic understandable in < 5 minutes

## Constraints

### Technical Constraints
- **Backward compatibility**: Zero breaking changes to external APIs (except table markdown removal)
- **MCP integration**: Must continue working with existing MCP server
- **Template system**: Template mapping functionality preserved
- **Performance**: No degradation in slide creation speed
- **Table change**: Users must accept plain text tables (no more markdown in cells)

### Business Constraints
- **No downtime**: Refactor cannot break production usage
- **Documentation**: All changes must be documented for future maintenance
- **Testing**: Comprehensive test coverage maintained throughout
- **User communication**: Table markdown removal must be clearly documented

## Out of Scope

### Explicitly Not Included
- **New features**: This is purely a refactor, no new functionality
- **API changes**: No modifications to public interfaces (except table simplification)
- **Template changes**: PowerPoint template files remain unchanged
- **Performance optimization**: Focus is on maintainability, not speed improvements beyond simplification
- **Configuration changes**: MCP server configuration format unchanged
- **Advanced table formatting**: Rich text, styling, complex layouts in tables

## Risk Mitigation

### High-Risk Areas
1. **Dynamic shape creation**: Currently has broken functionality
2. **Table processing**: Multiple code paths create complexity (simplified by removing markdown)
3. **Placeholder mapping**: Template compatibility must be preserved
4. **Content formatting**: Complex formatting logic must remain intact (except in tables)

### Mitigation Strategies
1. **Incremental refactor**: Move one responsibility at a time
2. **Comprehensive testing**: Test after each module extraction
3. **Backup branches**: Maintain rollback capability at each step
4. **Feature documentation**: Document what's currently broken vs. working
5. **Table simplification first**: Remove markdown table processing early to reduce complexity

### Table Simplification Benefits
1. **Reduced complexity**: Eliminates markdown parsing within table cells
2. **Better performance**: Faster table creation and processing
3. **Fewer bugs**: Less complex logic means fewer edge cases
4. **Easier maintenance**: Plain text table logic is straightforward
5. **Cleaner code**: Removes 100+ lines of complex table markdown processing