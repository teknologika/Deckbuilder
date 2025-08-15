# Implementation Tasks for Slide Builder Refactor

## Setup and Infrastructure

- [ ] 1. **Create new module directory structure**
  - [ ] 1.1. Create `src/deckbuilder/core/refactored/` directory
  - [ ] 1.2. Add `__init__.py` files for proper module imports
  - [ ] 1.3. Set up module import structure for dependency injection

- [ ] 2. **Establish testing infrastructure**
  - [ ] 2.1. Create `tests/core/refactored/` test directory structure
  - [ ] 2.2. Set up test fixtures for slide creation and validation
  - [ ] 2.3. Create test data using existing structured frontmatter patterns

## Phase 1: Extract and Enhance TableHandler (Dependency: None)

- [ ] 3. **Create TableHandler module (~300 lines)**
  - [ ] 3.1. Extract `_is_table_markdown()` method and enhance it
  - [ ] 3.2. DELETE `_contains_table_content()` duplicate method completely
  - [ ] 3.3. Create `detect_table_content()` - unified table detection
  - [ ] 3.4. Create `parse_table_structure()` - PLAIN TEXT ONLY, no markdown parsing
  - [ ] 3.5. Create `create_table_from_data()` - enhanced table creation
  - [ ] 3.6. Create `position_table_on_slide()` - table positioning logic

- [ ] 4. **Remove all markdown parsing from table cells**
  - [ ] 4.1. Identify all table markdown parsing code in existing codebase
  - [ ] 4.2. Replace with plain text cell processing
  - [ ] 4.3. Update table creation to use plain text only
  - [ ] 4.4. Verify 50%+ performance improvement in table processing

## Phase 2: Extract and Enhance PlaceholderManager (Dependency: LayoutResolver)

- [ ] 5. **Create LayoutResolver module (~200 lines)**
  - [ ] 5.1. USE existing layout resolution from `core/layout_resolver.py`
  - [ ] 5.2. Integrate with existing PatternLoader system
  - [ ] 5.3. Create clean interface for layout-to-pattern mapping
  - [ ] 5.4. Add error handling for missing layouts

- [ ] 6. **Create PlaceholderManager module (~350 lines)**
  - [ ] 6.1. Import and USE existing PatternLoader from `templates/pattern_loader.py`
  - [ ] 6.2. Import and USE existing semantic detection from `content/placeholder_types.py`
  - [ ] 6.3. Create `map_fields_to_placeholders()` - pattern-driven field mapping
  - [ ] 6.4. Create `_find_placeholder_semantically()` - semantic detection integration
  - [ ] 6.5. DELETE 92-line `_resolve_field_name_variations()` hardcoded dictionary
  - [ ] 6.6. Implement clear error messages (no fallbacks)

## Phase 3: Extract and Enhance ContentProcessor (Dependency: PlaceholderManager)

- [ ] 7. **Create ContentProcessor module (~400 lines)**
  - [ ] 7.1. Extract and enhance `_apply_content_to_single_placeholder()` logic
  - [ ] 7.2. USE existing inline formatting from current system
  - [ ] 7.3. Create `apply_content_to_placeholder()` - cleaned up content application
  - [ ] 7.4. Enhance existing `_get_placeholder_font_size()` as `calculate_font_sizing()`
  - [ ] 7.5. Create `estimate_content_dimensions()` for layout calculations
  - [ ] 7.6. Remove complex formatting paths, keep essential formatting

## Phase 4: Extract and Fix ShapeBuilder (Dependency: ContentProcessor, TableHandler)

- [ ] 8. **Create ShapeBuilder module (~400 lines)**
  - [ ] 8.1. Extract existing `_create_dynamic_content_shapes()` logic
  - [ ] 8.2. FIX broken positioning issues in dynamic shape creation
  - [ ] 8.3. Create `calculate_shape_positioning()` - proper spacing, no overlap
  - [ ] 8.4. Create `create_text_shape()` - positioned text shape creation
  - [ ] 8.5. Create `create_positioned_table()` - table positioning integration
  - [ ] 8.6. Fix coordinate calculation and prevent shape overlap

## Phase 5: Extract and Simplify SlideCoordinator (Dependency: All modules)

- [ ] 9. **Create SlideCoordinator module (~300 lines)**
  - [ ] 9.1. REPLACE bloated 127-line `add_slide()` with clean `create_slide()`
  - [ ] 9.2. Wire all enhanced modules together via dependency injection
  - [ ] 9.3. ENHANCE existing `clear_slides()` logic
  - [ ] 9.4. ENHANCE existing `add_speaker_notes()` logic
  - [ ] 9.5. Create simple orchestration flow (no complex branching)
  - [ ] 9.6. Implement clear error handling throughout

## Phase 6: Integration and API Compatibility (Dependency: SlideCoordinator)

- [ ] 10. **Create backward compatibility wrapper**
  - [ ] 10.1. Update existing `SlideBuilder` class to delegate to new architecture
  - [ ] 10.2. Maintain exact same public API signatures
  - [ ] 10.3. Preserve all existing method interfaces
  - [ ] 10.4. Test MCP server integration with new architecture

- [ ] 11. **Integration testing and validation**
  - [ ] 11.1. Run comprehensive integration tests across all modules
  - [ ] 11.2. Validate all existing functionality preserved
  - [ ] 11.3. Verify performance improvements (50%+ table processing)
  - [ ] 11.4. Test with real structured frontmatter patterns

## Testing Tasks

### Unit Tests
- [ ] 12. **TableHandler unit tests**
  - [ ] 12.1. Test `detect_table_content()` with various table formats
  - [ ] 12.2. Test `parse_table_structure()` plain text processing
  - [ ] 12.3. Test table creation without markdown parsing
  - [ ] 12.4. Verify markdown treated as literal text in cells

- [ ] 13. **PlaceholderManager unit tests**
  - [ ] 13.1. Test pattern loading and validation
  - [ ] 13.2. Test semantic detection integration
  - [ ] 13.3. Test field mapping without hardcoded variations
  - [ ] 13.4. Test clear error messages for missing patterns/placeholders

- [ ] 14. **ContentProcessor unit tests**
  - [ ] 14.1. Test content application to various placeholder types
  - [ ] 14.2. Test inline formatting preservation
  - [ ] 14.3. Test font sizing calculations
  - [ ] 14.4. Test content dimension estimation

- [ ] 15. **ShapeBuilder unit tests**
  - [ ] 15.1. Test dynamic shape positioning (no overlap)
  - [ ] 15.2. Test text shape creation
  - [ ] 15.3. Test positioned table creation
  - [ ] 15.4. Verify fixes for broken positioning functionality

- [ ] 16. **SlideCoordinator unit tests**
  - [ ] 16.1. Test slide creation orchestration
  - [ ] 16.2. Test module coordination and error handling
  - [ ] 16.3. Test speaker notes functionality
  - [ ] 16.4. Test backward compatibility

### Integration Tests
- [ ] 17. **Cross-module integration tests**
  - [ ] 17.1. Test complete slide creation workflow
  - [ ] 17.2. Test pattern loading → placeholder mapping → content application
  - [ ] 17.3. Test table detection → creation → positioning
  - [ ] 17.4. Test dynamic shape creation with mixed content

- [ ] 18. **System integration tests**
  - [ ] 18.1. Test MCP server compatibility
  - [ ] 18.2. Test all structured frontmatter pattern types
  - [ ] 18.3. Test backward compatibility with existing API
  - [ ] 18.4. Test performance benchmarks vs original system

### Regression Tests
- [ ] 19. **Comprehensive regression testing**
  - [ ] 19.1. Run all existing test suites against new architecture
  - [ ] 19.2. Verify zero functionality regressions
  - [ ] 19.3. Test edge cases and error conditions
  - [ ] 19.4. Validate broken functionality now works (table duplication, positioning)

## Code Quality and Cleanup

- [ ] 20. **Code quality verification**
  - [ ] 20.1. Run flake8 on all new modules - zero F-level errors
  - [ ] 20.2. Run black formatting on all code
  - [ ] 20.3. Verify each module ≤400 lines
  - [ ] 20.4. Check cyclomatic complexity reduction

- [ ] 21. **Remove redundant code**
  - [ ] 21.1. DELETE all identified duplicate methods
  - [ ] 21.2. DELETE 92-line hardcoded variations dictionary
  - [ ] 21.3. DELETE unused imports and variables (F401, F841)
  - [ ] 21.4. Verify 60% code reduction achieved

## Documentation

- [ ] 22. **Update documentation**
  - [ ] 22.1. Document new module architecture
  - [ ] 22.2. Update API documentation for enhanced methods
  - [ ] 22.3. Document migration from old to new architecture
  - [ ] 22.4. Update troubleshooting guides with new error messages

## Implementation Dependencies

**Critical Path:**
1. TableHandler (independent) → 
2. LayoutResolver (independent) → 
3. PlaceholderManager (needs LayoutResolver) → 
4. ContentProcessor (needs PlaceholderManager) → 
5. ShapeBuilder (needs ContentProcessor, TableHandler) → 
6. SlideCoordinator (needs all modules)

**Testing Dependencies:**
- Unit tests can be written in parallel with module development
- Integration tests require all modules to be complete
- Regression tests are final validation step

**Success Criteria:**
- All modules ≤400 lines
- Zero functionality regressions
- 50%+ table processing performance improvement
- Clear error messages (no silent fallbacks)
- All existing tests pass
- MCP server integration preserved