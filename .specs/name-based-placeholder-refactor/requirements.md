# Requirements Document: Name-Based Placeholder Refactor

## Introduction

This feature implements a complete architectural refactor to eliminate all index-based mappings and dual code paths in the Deckbuilder presentation system. The system will be replaced with an ultra-DRY name-based approach where PowerPoint template names serve as the single source of truth for both layouts and placeholders.

## Problem Statement

### Current Issues
1. **Dual Code Paths**: Multiple competing systems process placeholders (field-driven vs semantic processing)
2. **Index-Based Complexity**: Separate JSON mapping files maintain placeholder indices that duplicate PowerPoint template information
3. **Table Processing Failures**: Current table_data fields fail due to code path conflicts
4. **Maintenance Burden**: Index mappings require constant synchronization with PowerPoint templates
5. **DRY Violations**: PowerPoint template names exist alongside duplicate JSON mappings

### Root Cause
The system currently uses:
- Layout selection by index: `prs.slide_layouts[index]`
- Placeholder mapping by index: `placeholder.placeholder_format.idx`
- Separate JSON files with index mappings: `"13": "table_data"`

This creates multiple sources of truth and competing processing systems.

## Requirements

### Requirement 1: Single Source of Truth
**User Story:** As a developer, I want PowerPoint template names to be the only source of layout and placeholder definitions, so that there is no duplication or synchronization issues.

#### Acceptance Criteria
1. WHEN the system needs layout information THEN it SHALL read directly from PowerPoint template names
2. WHEN the system needs placeholder information THEN it SHALL read directly from PowerPoint placeholder names  
3. WHEN template changes are made THEN no JSON mapping files SHALL require updates
4. IF a layout name doesn't exist THEN the system SHALL provide clear error with available layout names

### Requirement 2: Name-Based Layout Selection
**User Story:** As a user, I want to specify exact PowerPoint layout names in my JSON, so that layout selection is intuitive and direct.

#### Acceptance Criteria
1. WHEN user specifies `"layout": "Table Only"` THEN system SHALL find layout by exact name match
2. WHEN layout name is invalid THEN system SHALL suggest available layout names
3. WHEN multiple layouts have similar names THEN system SHALL match exact names only
4. IF layout name contains special characters THEN system SHALL handle them correctly

### Requirement 3: Name-Based Placeholder Mapping
**User Story:** As a user, I want my JSON field names to match PowerPoint placeholder names exactly, so that content mapping is direct and obvious.

#### Acceptance Criteria
1. WHEN user specifies `"table_data": {...}` THEN system SHALL find placeholder named "table_data"
2. WHEN field name doesn't match any placeholder THEN system SHALL list available placeholder names
3. WHEN placeholder names contain special characters THEN system SHALL handle exact matches
4. IF multiple placeholders exist THEN system SHALL match by name, not index

### Requirement 4: Single Processing Path
**User Story:** As a developer, I want only one code path for processing placeholders, so that there are no conflicts or dual processing issues.

#### Acceptance Criteria
1. WHEN processing slide content THEN only field-driven processing SHALL execute
2. WHEN table_data is processed THEN `_handle_table_placeholder` SHALL be called correctly
3. WHEN any placeholder type is processed THEN the same processing logic SHALL apply
4. IF semantic processing exists THEN it SHALL be removed completely

### Requirement 5: Runtime Discovery
**User Story:** As a user, I want to discover available layouts and placeholder names through CLI commands, so that I don't need to guess or maintain documentation.

#### Acceptance Criteria
1. WHEN user runs `deckbuilder layouts` THEN system SHALL list all available layout names
2. WHEN user runs `deckbuilder inspect "Layout Name"` THEN system SHALL show placeholder names for that layout
3. WHEN user requests example JSON THEN system SHALL generate copy-paste ready template
4. IF layout doesn't exist THEN system SHALL suggest similar layout names

### Requirement 6: Zero Index Dependencies
**User Story:** As a developer, I want no index-based lookups anywhere in the codebase, so that the system is resilient to PowerPoint template changes.

#### Acceptance Criteria
1. WHEN PowerPoint template layouts are reordered THEN system SHALL continue working without changes
2. WHEN PowerPoint placeholder indices change THEN system SHALL continue working without changes
3. WHEN searching for layouts or placeholders THEN system SHALL never use index numbers
4. IF index-based code exists THEN it SHALL be completely removed

## Success Criteria

### Functional Success
1. **Table Creation Works**: `table_data` field successfully creates tables in TABLE placeholders
2. **All Placeholder Types Work**: TITLE, TABLE, CONTENT, PICTURE placeholders all function via name matching
3. **Layout Selection Works**: All PowerPoint layouts accessible by exact name
4. **Discovery Tools Work**: CLI commands provide complete layout and placeholder information

### Technical Success  
1. **Single Code Path**: Only one processing system handles all placeholder types
2. **Zero JSON Mappings**: No index-based mapping files required
3. **PowerPoint Template Authority**: Template changes require no code changes
4. **Clean Architecture**: No dual processing paths or competing systems

### User Experience Success
1. **Intuitive Names**: Users work with exact PowerPoint names (no aliases, no indices)
2. **Clear Errors**: Helpful messages when names don't match
3. **Easy Discovery**: Simple CLI commands reveal all available options
4. **Copy-Paste Examples**: Generated JSON templates work immediately

## Out of Scope
1. **Alias Systems**: No shortcut names or alternative references
2. **Index Fallbacks**: No backwards compatibility with index-based systems  
3. **Complex Mapping**: No conditional or computed placeholder mappings
4. **Legacy Support**: Existing index-based JSON files will need conversion

## Dependencies
1. **PowerPoint Templates**: Must have meaningful placeholder names
2. **python-pptx Library**: Must support name-based layout and placeholder access
3. **Test Suite**: All existing tests must pass after refactor
4. **CLI Framework**: Must support new inspection commands

## Implementation Phases
1. **Phase 1**: Baseline and analysis (30 minutes)
2. **Phase 2**: Layout name-based system (45 minutes)  
3. **Phase 3**: Placeholder name-based system (60 minutes)
4. **Phase 4**: Runtime discovery tools (30 minutes)
5. **Phase 5**: Cleanup and validation (30 minutes)

**Total Estimated Time**: 3 hours 15 minutes