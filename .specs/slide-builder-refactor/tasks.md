# Implementation Tasks for Slide Builder Refactor

## Setup and Infrastructure

- [x] 1. **Create new module structure directly in core**
  - [x] 1.1. Rename existing `slide_builder.py` to `slide_builder_legacy.py` (COMPLETED ✅)
  - [x] 1.2. Create new modules directly in `src/deckbuilder/core/` 
  - [x] 1.3. Set up clean import structure for new modules

- [x] 2. **Establish testing infrastructure**
  - [x] 2.1. Create `tests/core/` test directory structure for new modules
  - [x] 2.2. Set up test fixtures for slide creation and validation
  - [x] 2.3. Create test data using existing structured frontmatter patterns

## Phase 1: Extract and Enhance TableHandler (Dependency: None)

- [x] 3. **Create TableHandler module (~300 lines)**
  - [x] 3.1. Extract `_is_table_markdown()` method and enhance it as `detect_table_content()`
  - [x] 3.2. DELETE `_contains_table_content()` duplicate method completely
  - [x] 3.3. Create unified table detection and plain text parsing
  - [x] 3.4. Create `parse_table_structure()` - PLAIN TEXT ONLY, no markdown parsing
  - [x] 3.5. Create `create_table_from_data()` - enhanced table creation
  - [x] 3.6. Create `position_table_on_slide()` - table positioning logic

- [X] 4. **Remove all markdown parsing from table cells**
  - [x] 4.1. Identify all table markdown parsing code in existing codebase
  - [x] 4.2. Replace with plain text cell processing
  - [x] 4.3. Update table creation to use plain text only


## Phase 2: ✅ COMPLETE - PlaceholderManager with HYBRID APPROACH (Dependency: LayoutResolver)

- [x] 5. **Create LayoutResolver module (~200 lines)**
  - [x] 5.1. USE existing layout resolution from `core/layout_resolver.py`
  - [x] 5.2. Integrate with existing PatternLoader system
  - [x] 5.3. Create clean interface for layout-to-pattern mapping
  - [x] 5.4. ✅ Enhanced error handling with smart suggestions and fallback resolution

- [x] 6. **✅ COMPLETE: PlaceholderManager module with HYBRID APPROACH (~350 lines)**
  - [x] 6.1. Import and USE existing PatternLoader from `templates/pattern_loader.py`
  - [x] 6.2. ✅ HYBRID APPROACH: Index-based normalization + Name-based mapping 
  - [x] 6.3. Create `map_fields_to_placeholders()` with EVERY SLIDE normalization
  - [x] 6.4. **NEW WORKFLOW**: Get template indices → Add slide → Rename placeholders → Map by name
  - [x] 6.5. ✅ ELIMINATED: 92-line `_resolve_field_name_variations()` hardcoded dictionary
  - [x] 6.6. ✅ IMPLEMENTED: PlaceholderNormalizer for reliable index-based renaming

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
  - [ ] 10.1. Create new `SlideBuilder` class to delegate to new architecture
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

- [ ] 13. **PlaceholderManager unit tests - HYBRID APPROACH**
  - [ ] 13.1. Test pattern loading and validation
  - [ ] 13.2. Test index-based placeholder normalization (PlaceholderNormalizer)
  - [ ] 13.3. Test EVERY SLIDE workflow: indices → add slide → rename → map by name
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

## Final Cleanup

- [ ] 22. **Remove legacy files and update documentation**
  - [ ] 22.1. DELETE `slide_builder_legacy.py` when refactor complete
  - [ ] 22.2. Update module documentation for new architecture
  - [ ] 22.3. Update API documentation for enhanced methods
  - [ ] 22.4. Document migration from old to new architecture
  - [ ] 22.5. Update troubleshooting guides with new error messages

## Code Quality Issues Discovered

- [ ] 23. **CLEANUP: Remove hardcoded table styling defaults**
  - [ ] 23.1. Remove hardcoded defaults from `table_integration.py` ("dark_blue_white_text", "alternating_light_gray", "thin_gray", 0.6, etc.)
  - [ ] 23.2. Make table styling configuration-driven using structured frontmatter patterns
  - [ ] 23.3. Create single source of truth for table styling defaults
  - [ ] 23.4. Update all table styling to use PatternLoader system
  - [ ] 23.5. Eliminate DRY violations in table styling configuration

- [ ] 24. **CLEANUP: Review unused methods after refactor optimization**
  - [ ] 24.1. Review `_get_layout_name_mapping()` method in PlaceholderNormalizer - may be unused
  - [ ] 24.2. Direct access approach more robust than pre-computed mapping
  - [ ] 24.3. Remove method if confirmed unused after testing

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
- ✅ **HYBRID APPROACH IMPLEMENTED**: Index-based normalization every slide + Name-based mapping
- All existing tests pass
- MCP server integration preserved
- Legacy file `slide_builder_legacy.py` successfully removed
- All hardcoded configuration eliminated