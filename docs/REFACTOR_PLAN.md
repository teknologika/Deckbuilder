# Complete Name-Based Refactor Plan (Ultra-DRY)

## Overview
Eliminate all index-based mappings and dual code paths. Use PowerPoint template names as the single source of truth for both layouts and placeholders.

## Phase 1: Baseline & Analysis (30 minutes)
1. **Create baseline commit** - Ensure all tests pass before changes
2. **Map current code dependencies** on index-based systems:
   - Layout selection by index (`prs.slide_layouts[index]`)
   - Placeholder mapping by index (`placeholder.placeholder_format.idx`)
   - Alias resolution system
3. **Document current execution flow** in slide_builder.py
4. **Identify all dual code paths** causing current table issues

## Phase 2: Layout Name-Based System (45 minutes)
1. **Add layout-by-name helper method**:
   ```python
   def get_layout_by_name(prs, layout_name):
       for layout in prs.slide_layouts:
           if layout.name == layout_name:
               return layout
       raise ValueError(f"Layout '{layout_name}' not found")
   ```

2. **Replace all layout index usage**:
   - Update `add_slide_with_direct_mapping()` to use exact PowerPoint layout names
   - Remove layout index lookups from JSON
   - Remove alias resolution system entirely

3. **Eliminate JSON mapping file completely** - No JSON needed for name-based lookups

## Phase 3: Placeholder Name-Based System (60 minutes)
1. **Enhance placeholder-by-name helper**:
   ```python
   def find_placeholder_by_name(slide, field_name):
       # Direct name matching - single source of truth
   ```

2. **Remove ALL index-based placeholder logic**:
   - Remove `field_to_index` mapping creation
   - Remove index-based placeholder loops
   - No more JSON placeholder mappings to maintain

3. **Consolidate to single field processing path**:
   - Remove dual code paths (field vs semantic processing)
   - Make field-driven processing handle ALL placeholder types
   - Ensure `_handle_table_placeholder` gets called properly

## Phase 4: Runtime Discovery Tools (30 minutes)
1. **Add inspection CLI commands**:
   ```bash
   deckbuilder layouts                    # List available layouts
   deckbuilder inspect "Table Only"      # Show placeholders
   deckbuilder inspect "Table Only" --example  # Generate JSON
   ```

2. **Output user-friendly information** (no indexes, no aliases)

3. **Generate copy-paste ready JSON examples**

## Phase 5: Cleanup & Validation (30 minutes)
1. **Remove default.json entirely** (or make it optional documentation only)
2. **Remove alias processing code**
3. **Remove deprecated methods** and dead code paths
4. **Test all placeholder types**: TITLE, TABLE, CONTENT, PICTURE
5. **Verify table processing works end-to-end**
6. **Run full test suite** - ensure no regressions

## Ultra-DRY Result:
- ✅ **Zero JSON mapping files** - PowerPoint template IS the schema
- ✅ **Zero aliases** - Users use exact PowerPoint layout names
- ✅ **Zero indexes** - Direct name matching only
- ✅ **Single source of truth** - PowerPoint template defines everything
- ✅ **Runtime discovery** - CLI tools read template directly

## Success Criteria:
1. Users specify exact layout names: `"layout": "Table Only"`
2. Users specify exact field names: `"table_data": {...}`
3. System matches everything by name directly
4. No JSON mapping files required
5. Table creation works perfectly via name matching

## Expected Benefits:
- **Eliminates dual code paths** causing current table processing issues
- **Removes all mapping maintenance** - no JSON files to keep in sync
- **Simplifies user experience** - direct PowerPoint names, no aliases
- **Maximum DRY compliance** - PowerPoint template as single source of truth
- **Better debugging** - clear, single execution path