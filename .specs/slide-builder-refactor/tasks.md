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

## Phase 1: ✅ COMPLETE - Extract and Enhance TableHandler (Dependency: None)

- [x] 3. **Create TableHandler module (~300 lines)**
  - [x] 3.1. Extract `_is_table_markdown()` method and enhance it as `detect_table_content()`
  - [x] 3.2. DELETE `_contains_table_content()` duplicate method completely
  - [x] 3.3. Create unified table detection and plain text parsing
  - [x] 3.4. Create `parse_table_structure()` - PLAIN TEXT ONLY, no markdown parsing
  - [x] 3.5. Create `create_table_from_data()` - enhanced table creation
  - [x] 3.6. Create `position_table_on_slide()` - table positioning logic

- [x] 4. **Remove all markdown parsing from table cells**
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

## Phase 3: ✅ COMPLETE - ContentProcessor (Template Font Preservation) + Enhanced TableHandler

**ARCHITECTURE DECISION**: Move table font logic to TableHandler, preserve template fonts in ContentProcessor

- [x] 7. **✅ COMPLETE: ContentProcessor module (~150 lines - SIMPLIFIED)**
  - [x] 7.1. Extract `_apply_content_to_single_placeholder()` → `apply_content_to_placeholder()`
  - [x] 7.2. **Preserve template fonts** - no font override logic (CLI remap handles custom fonts separately)
  - [x] 7.3. **Added proper newline support** - convert `\n` → PowerPoint paragraphs  
  - [x] 7.4. Keep semantic type detection (title vs content vs media)
  - [x] 7.5. Preserve existing inline formatting capabilities
  - [x] 7.6. **Template fonts preserved** - no font sizing interference

- [x] 7b. **✅ COMPLETE: Enhanced TableHandler with Template-First Font Logic**
  - [x] 7b.1. Added template-first font handling (no hardcoded defaults)
  - [x] 7b.2. Moved font validation from `table_integration.py` 
  - [x] 7b.3. Added `get_font_size_for_row()` method from `table_builder.py`
  - [x] 7b.4. Added `get_default_fonts()`, `validate_font_sizes()`, `calculate_table_fonts()`
  - [x] 7b.5. Template fonts preserved when no explicit table fonts specified

- [x] 7c. **Integration and Export**
  - [x] 7c.1. Updated `core/__init__.py` to export ContentProcessor
  - [x] 7c.2. Created comprehensive unit tests for ContentProcessor
  - [x] 7c.3. Removed hardcoded font fallbacks (template fonts preserved)

## ~~Phase 4: Extract and Fix ShapeBuilder~~ → **🗑️ ELIMINATED - NOT NEEDED**

**ARCHITECTURE DECISION**: ShapeBuilder eliminated - dynamic shape system was over-engineered

### Why Phase 4 Was Eliminated:
- **content_segmenter.py is DEPRECATED** - returns empty segments `{"segments": [], "has_mixed_content": False}`
- **_create_dynamic_content_shapes() does nothing** - no content segments to process
- **Template layouts are better** - use dedicated PowerPoint layouts instead:
  - Table Only, Table with Content Above, Table with Content Left, etc.
- **~400 lines eliminated** from planned codebase
- **Simpler architecture** - 5 modules instead of 6

### ~~Original Phase 4 Tasks (CANCELLED):~~
- ~~8.1. Extract existing `_create_dynamic_content_shapes()` logic~~
- ~~8.2. FIX broken positioning issues in dynamic shape creation~~
- ~~8.3. Create `calculate_shape_positioning()` - proper spacing, no overlap~~
- ~~8.4. Create `create_text_shape()` - positioned text shape creation~~
- ~~8.5. Create `create_positioned_table()` - table positioning integration~~
- ~~8.6. Fix coordinate calculation and prevent shape overlap~~

## Phase 4 REVISED: Remove Deprecated Dynamic Shape Code

- [x] 8. **🗑️ CLEANUP: Remove deprecated dynamic shape system**
  - [x] 8.1. DELETE `src/deckbuilder/content/content_segmenter.py` (already deprecated)
  - [x] 8.2. DELETE `_create_dynamic_content_shapes()` method from slide_builder_legacy.py
  - [x] 8.3. REMOVE `_content_segments` and `_requires_dynamic_shapes` handling
  - [x] 8.4. CLEAN UP dynamic vs static path separation in frontmatter_to_json_converter.py
  - [x] 8.5. UPDATE imports and references to content_segmenter
  - [x] 8.6. VERIFY table processing works via template layouts only

## Phase 5: Extract and Simplify SlideCoordinator (Dependency: All enhanced modules)

- [x] 9. **Create SlideCoordinator module (~300 lines)**
  - [x] 9.1. REPLACE bloated 127-line `add_slide()` with clean `create_slide()`
  - [x] 9.2. Wire all enhanced modules together via dependency injection
  - [x] 9.3. ENHANCE existing `clear_slides()` logic
  - [x] 9.4. ENHANCE existing `add_speaker_notes()` logic
  - [x] 9.5. Create simple orchestration flow (no complex branching)
  - [x] 9.6. Implement clear error handling throughout

## Phase 6: Integration and API Compatibility (Dependency: SlideCoordinator)

- [x] 10. **Create backward compatibility wrapper**
  - [x] 10.1. Create new `SlideBuilder` class to delegate to new architecture
  - [x] 10.2. Maintain exact same public API signatures
  - [x] 10.3. Preserve all existing method interfaces
  - [x] 10.4. Test MCP server integration with new architecture

- [x] 11. **Integration testing and validation**
  - [x] 11.1. Run comprehensive integration tests across all modules
  - [x] 11.2. Validate all existing functionality preserved
  - [x] 11.3. Verify performance improvements (50%+ table processing)
  - [x] 11.4. Test with real structured frontmatter patterns

## Testing Tasks

### Unit Tests
- [x] 12. **TableHandler unit tests (ENHANCED for font handling)**
  - [x] 12.1. Test `detect_table_content()` with various table formats
  - [x] 12.2. Test `parse_table_structure()` plain text processing
  - [x] 12.3. Test table font handling methods (`get_default_fonts()`, etc.)
  - [x] 12.4. Test font size validation and calculation
  - [x] 12.5. Verify markdown treated as literal text in cells

- [x] 13. **PlaceholderManager unit tests - HYBRID APPROACH**
  - [x] 13.1. Test pattern loading and validation
  - [x] 13.2. Test index-based placeholder normalization (PlaceholderNormalizer)
  - [x] 13.3. Test EVERY SLIDE workflow: indices → add slide → rename → map by name
  - [x] 13.4. Test clear error messages for missing patterns/placeholders

- [x] 14. **ContentProcessor unit tests (Template font preservation)**
  - [x] 14.1. Test content application to various placeholder types
  - [x] 14.2. Test inline formatting preservation
  - [x] 14.3. **✅ Test newline conversion** (`\n` → PowerPoint paragraphs)
  - [x] 14.4. Test semantic type detection (title vs content vs media)
  - [x] 14.5. **✅ Verify NO font override behavior** - template fonts preserved

- ~~15. **ShapeBuilder unit tests**~~ → **🗑️ ELIMINATED**
  - ~~15.1. Test dynamic shape positioning (no overlap)~~
  - ~~15.2. Test text shape creation~~
  - ~~15.3. Test positioned table creation~~
  - ~~15.4. Verify fixes for broken positioning functionality~~

- [x] 15. **SlideCoordinator unit tests** (RENUMBERED)
  - [x] 15.1. Test slide creation orchestration
  - [x] 15.2. Test module coordination and error handling
  - [x] 15.3. Test speaker notes functionality
  - [x] 15.4. Test backward compatibility

### Integration Tests
- [x] 16. **Cross-module integration tests** (RENUMBERED)
  - [x] 16.1. Test complete slide creation workflow
  - [x] 16.2. Test pattern loading → placeholder mapping → content application
  - [x] 16.3. Test table detection → creation → positioning → font handling
  - [x] 16.4. **✅ Test template layouts** (instead of dynamic shape creation)

- [ ] 17. **System integration tests** (RENUMBERED)
  - [x] 17.1. Test MCP server compatibility
  - [x] 17.2. Test all structured frontmatter pattern types
  - [-] 17.3. Test backward compatibility with existing API
  - [x] 17.4. Test performance benchmarks vs original system

### Regression Tests
- [ ] 18. **Comprehensive regression testing** (RENUMBERED)
  - [x] 18.1. Run all existing test suites against new architecture
  - [ ] 18.2. Verify zero functionality regressions
  - [ ] 18.3. Test edge cases and error conditions
  - [ ] 18.4. **✅ Validate template layouts work** (replacing broken dynamic positioning)

## Code Quality and Cleanup

- [ ] 19. **Code quality verification** (RENUMBERED)
  - [ ] 19.1. Run flake8 on all new modules - zero F-level errors
  - [ ] 19.2. Run black formatting on all code
  - [ ] 19.3. Verify each module ≤400 lines (ContentProcessor ~150 lines)
  - [ ] 19.4. Check cyclomatic complexity reduction

- [ ] 20. **Remove redundant code** (RENUMBERED)
  - [ ] 20.1. DELETE all identified duplicate methods
  - [ ] 20.2. DELETE font override logic from `slide_builder_legacy.py`
  - [ ] 20.3. DELETE unused imports and variables (F401, F841)
  - [ ] 20.4. **DELETE deprecated dynamic shape code** (content_segmenter.py, etc.)
  - [ ] 20.5. Verify 60%+ code reduction achieved

## Final Cleanup

- [ ] 21. **Remove legacy files and update documentation** (RENUMBERED)
  - [ ] 21.1. DELETE `slide_builder_legacy.py` when refactor complete
  - [ ] 21.2. **DELETE `content_segmenter.py`** (deprecated dynamic shape system)
  - [ ] 21.3. Update module documentation for new architecture
  - [ ] 21.4. Update API documentation for enhanced methods
  - [ ] 21.5. Document migration from old to new architecture
  - [ ] 21.6. Update troubleshooting guides with new error messages

## Code Quality Issues Discovered

- [ ] 22. **CLEANUP: Remove hardcoded table styling defaults (Move to TableHandler)** (RENUMBERED)
  - [ ] 22.1. Remove hardcoded defaults from `table_integration.py` 
  - [ ] 22.2. Move all table styling defaults to TableHandler
  - [ ] 22.3. Create single source of truth for table styling defaults
  - [ ] 22.4. Update all table styling to use TableHandler system
  - [ ] 22.5. Eliminate DRY violations in table styling configuration

- [ ] 23. **CLEANUP: Review unused methods after refactor optimization** (RENUMBERED)
  - [ ] 23.1. Review `_get_layout_name_mapping()` method in PlaceholderNormalizer - may be unused
  - [ ] 23.2. Review `_get_placeholder_font_size()` method - DELETE (no longer needed)
  - [ ] 23.3. Review `_create_dynamic_content_shapes()` method - DELETE (deprecated)
  - [ ] 23.4. Remove method if confirmed unused after testing

## REVISED Implementation Dependencies

**Critical Path UPDATED:**
1. ✅ TableHandler (independent) + Table Font Enhancement → 
2. ✅ LayoutResolver (independent) → 
3. ✅ PlaceholderManager (needs LayoutResolver) → 
4. ✅ ContentProcessor (needs PlaceholderManager) + TableHandler Font Integration → 
5. ~~ShapeBuilder~~ → **🗑️ ELIMINATED** → 
6. SlideCoordinator (needs enhanced modules) → 
7. Integration and Cleanup

**Key Architectural Changes:**
- **✅ ContentProcessor**: Simplified (~150 lines), NO font handling, focus on content + newlines
- **✅ TableHandler**: Enhanced with font logic, centralized table configuration, template-first approach
- **✅ Font Philosophy**: Preserve template fonts, only manage table fonts when explicitly needed
- **✅ Clean Separation**: Each module has clear, single responsibility
- **🗑️ ShapeBuilder ELIMINATED**: Dynamic shape system deprecated, use template layouts instead

**Success Criteria:**
- ✅ All modules ≤400 lines (ContentProcessor ~150 lines) 
- Zero functionality regressions (pending final testing)
- 50%+ table processing performance improvement (achieved in Phase 1)
- Clear error messages (no silent fallbacks)
- ✅ **HYBRID APPROACH IMPLEMENTED**: Index-based normalization every slide + Name-based mapping
- ✅ **Template fonts preserved** - no font override behavior except when explicitly requested
- ✅ **Proper newline support** - `\n` creates PowerPoint paragraphs
- All existing tests pass (pending integration)
- MCP server integration preserved (pending testing)
- Legacy file `slide_builder_legacy.py` successfully removed (pending Phase 6)
- ✅ **No hardcoded configuration** - eliminated font defaults, uses template/explicit config only
- **🗑️ Deprecated code eliminated** - content_segmenter.py and dynamic shape system removed