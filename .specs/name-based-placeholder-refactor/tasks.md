# Implementation Tasks for Name-Based Placeholder Refactor

## Setup and Infrastructure

- [ ] 1. Create baseline commit and establish stable starting point
  - [ ] 1.1. Run full test suite to ensure current state is stable
  - [ ] 1.2. Create baseline commit with detailed description of current issues
  - [ ] 1.3. Generate baseline test results file

- [ ] 2. Map and document current index-based dependencies
  - [ ] 2.1. Find all layout index usage in codebase
  - [ ] 2.2. Find all placeholder index usage in codebase
  - [ ] 2.3. Find all JSON mapping dependencies
  - [ ] 2.4. Document current processing flow and dual code paths

## Core Functionality - Layout Name-Based System

- [ ] 3. Implement layout name-based resolution system
  - [ ] 3.1. Create LayoutResolver module with name-based lookup methods
  - [ ] 3.2. Add helpful error messages with suggestions for invalid layout names
  - [ ] 3.3. Add layout validation and listing functionality

- [ ] 4. Replace index-based layout lookups throughout system
  - [ ] 4.1. Update SlideBuilder to use LayoutResolver instead of index lookups
  - [ ] 4.2. Remove layout_mapping dependency from SlideBuilder initialization
  - [ ] 4.3. Update Engine to remove JSON layout mapping initialization
  - [ ] 4.4. Remove layout_mapping attributes and parameters

## Core Functionality - Placeholder Name-Based System

- [ ] 5. Implement placeholder name-based resolution system
  - [ ] 5.1. Create PlaceholderResolver module with name-based lookup methods
  - [ ] 5.2. Add placeholder listing and summary functionality
  - [ ] 5.3. Add placeholder type-based lookup for debugging

- [ ] 6. Replace dual processing paths with single field processing
  - [ ] 6.1. Remove field_to_index mapping creation entirely
  - [ ] 6.2. Remove complex index-based placeholder matching logic
  - [ ] 6.3. Implement single _process_slide_fields method using name-based lookup
  - [ ] 6.4. Add helpful error reporting for failed placeholder mappings

- [ ] 7. Implement unified placeholder type handling
  - [ ] 7.1. Create unified _apply_content_to_placeholder method
  - [ ] 7.2. Ensure all placeholder types (TITLE, TABLE, CONTENT, PICTURE) handled consistently
  - [ ] 7.3. Verify _handle_table_placeholder gets called correctly for TABLE placeholders
  - [ ] 7.4. Add fallback handling for unknown placeholder types

## Runtime Discovery Tools

- [ ] 8. Create CLI discovery system
  - [ ] 8.1. Create DiscoveryCommands class with template inspection functionality
  - [ ] 8.2. Implement list_layouts method to show all available layouts
  - [ ] 8.3. Implement inspect_layout method to show placeholders for specific layout
  - [ ] 8.4. Add example JSON generation with appropriate content for each placeholder type

- [ ] 9. Integrate discovery commands into main CLI
  - [ ] 9.1. Add 'layouts' command to list available slide layouts
  - [ ] 9.2. Add 'inspect' command to examine specific layout placeholders
  - [ ] 9.3. Add --example flag to generate copy-paste ready JSON templates
  - [ ] 9.4. Update CLI help text with discovery command usage

## Testing

- [ ] 10. Create unit tests for new name-based components
  - [ ] 10.1. Unit tests for LayoutResolver (valid/invalid names, error messages)
  - [ ] 10.2. Unit tests for PlaceholderResolver (name lookup, listing, type filtering)
  - [ ] 10.3. Unit tests for discovery CLI commands
  - [ ] 10.4. Unit tests for unified placeholder type handling

- [ ] 11. Create integration tests for end-to-end functionality
  - [ ] 11.1. Integration test for complete presentation creation using layout names
  - [ ] 11.2. Integration test for table_data field creating actual tables
  - [ ] 11.3. Integration test for all placeholder types working via name matching
  - [ ] 11.4. Integration test for discovery commands with real templates

- [ ] 12. Update existing tests for name-based system
  - [ ] 12.1. Update test data to use exact PowerPoint layout names
  - [ ] 12.2. Update test data to use exact placeholder field names
  - [ ] 12.3. Remove any tests dependent on index-based lookups
  - [ ] 12.4. Verify all existing tests pass with new name-based system

## Cleanup and Validation

- [ ] 13. Remove all legacy index-based code
  - [ ] 13.1. Remove field_to_index usage from slide_builder.py
  - [ ] 13.2. Remove placeholder_format.idx matching loops
  - [ ] 13.3. Remove layout_mapping references from engine.py
  - [ ] 13.4. Remove deprecated semantic processing methods

- [ ] 14. Validate complete system functionality
  - [ ] 14.1. Test discovery commands work correctly
  - [ ] 14.2. Test table creation via table_data field
  - [ ] 14.3. Test layout selection via exact layout names
  - [ ] 14.4. Test error handling provides helpful suggestions
  - [ ] 14.5. Verify no index-based code remains in codebase

- [ ] 15. Performance and maintenance validation
  - [ ] 15.1. Verify system startup is faster (no JSON parsing)
  - [ ] 15.2. Verify memory usage is reduced (no mapping structures)
  - [ ] 15.3. Test system resilience to PowerPoint template changes
  - [ ] 15.4. Validate all success criteria from requirements are met

## Documentation

- [ ] 16. Update system documentation
  - [ ] 16.1. Update user documentation with new layout/placeholder names
  - [ ] 16.2. Update developer documentation for name-based architecture
  - [ ] 16.3. Create migration guide for users moving from index-based system
  - [ ] 16.4. Document new discovery CLI commands and usage patterns

## Final Validation

- [ ] 17. End-to-end system verification
  - [ ] 17.1. Run complete test suite and verify all tests pass
  - [ ] 17.2. Test table processing end-to-end (current failure point)
  - [ ] 17.3. Verify all requirements from requirements document are satisfied
  - [ ] 17.4. Confirm all success criteria from design document are achieved

## Dependencies and Implementation Notes

### Task Dependencies:
- Tasks 1-2 (Setup) must be completed before any core functionality tasks
- Task 3 (Layout system) must be completed before Task 4 (Layout replacement)
- Task 5 (Placeholder system) must be completed before Tasks 6-7 (Placeholder replacement)
- Tasks 3-7 (Core functionality) must be completed before Task 8-9 (Discovery tools)
- Core functionality (Tasks 3-9) must be completed before cleanup (Tasks 13-14)
- Testing (Tasks 10-12) can be done in parallel with core functionality implementation

### Critical Success Factors:
1. **Table Processing Fix**: The primary goal is fixing table_data field processing
2. **Single Code Path**: Eliminating dual processing paths is essential
3. **Name-Based Authority**: PowerPoint template must be the single source of truth
4. **Backwards Incompatibility**: This is a breaking change with no index-based fallbacks

### Risk Mitigation:
- Baseline commit (Task 1) provides rollback point
- Incremental testing (Tasks 10-12) catches issues early
- Discovery tools (Tasks 8-9) help users adapt to new system
- Comprehensive validation (Tasks 14-15) ensures system reliability