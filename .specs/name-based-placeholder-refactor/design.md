# Design Document: Name-Based Placeholder Refactor

## Architecture Overview

This refactor transforms the Deckbuilder system from index-based dual processing paths to a single, name-based processing pipeline. The PowerPoint template becomes the authoritative schema definition.

## System Architecture

### Current Architecture (Problems)
```
User JSON → Layout Index Lookup → Slide Creation → Dual Processing:
                                                   ├─ Field Processing (fails for tables)
                                                   └─ Semantic Processing (creates empty placeholders)
```

### New Architecture (Solution)
```
User JSON → Layout Name Lookup → Slide Creation → Single Field Processing → Content Application
```

## Core Components

### 1. Layout Resolution System

**Current Implementation:**
```python
# Problem: Index-based lookup
layout_index = self.layout_mapping["layouts"][layout_name]["index"]
layout = prs.slide_layouts[layout_index]
```

**New Implementation:**
```python
# Solution: Direct name-based lookup
def get_layout_by_name(prs, layout_name):
    for layout in prs.slide_layouts:
        if layout.name == layout_name:
            return layout
    available = [l.name for l in prs.slide_layouts]
    raise ValueError(f"Layout '{layout_name}' not found. Available: {available}")
```

### 2. Placeholder Resolution System

**Current Implementation:**
```python
# Problem: Index-based mapping with dual paths
field_to_index = {field_name: int(placeholder_idx) for placeholder_idx, field_name in placeholder_mappings.items()}
for placeholder in slide.placeholders:
    if placeholder.placeholder_format.idx == target_index:
        # Process placeholder
```

**New Implementation:**
```python
# Solution: Direct name-based lookup
def find_placeholder_by_name(slide, field_name):
    for placeholder in slide.placeholders:
        try:
            placeholder_name = placeholder.element.nvSpPr.cNvPr.name
            if placeholder_name == field_name:
                return placeholder
        except AttributeError:
            continue
    return None
```

### 3. Single Processing Pipeline

**Current Flow (Dual Paths):**
1. Field processing attempts to map fields to placeholders
2. Semantic processing handles placeholders by type
3. Both systems run independently, causing conflicts

**New Flow (Single Path):**
1. Field-driven processing only
2. For each field in slide_data:
   - Find placeholder by name
   - Apply content based on placeholder type
   - Handle all types (TITLE, TABLE, CONTENT, PICTURE) uniformly

## Detailed Design

### Phase 1: Baseline and Analysis

**Objective:** Document current state and dependencies

**Tasks:**
1. **Dependency Mapping:**
   ```python
   # Find all index-based layout usage
   grep -r "slide_layouts\[" src/
   
   # Find all placeholder index usage  
   grep -r "placeholder_format\.idx" src/
   
   # Find all JSON mapping usage
   grep -r "field_to_index\|placeholder_mappings" src/
   ```

2. **Code Flow Documentation:**
   - Map execution path in `add_slide_with_direct_mapping()`
   - Identify dual processing entry points
   - Document current table processing failure points

3. **Test Baseline:**
   ```bash
   pytest tests/ --tb=short > baseline_test_results.txt
   ```

### Phase 2: Layout Name-Based System

**Objective:** Replace layout index lookups with name-based lookups

**Core Changes:**

1. **New Layout Resolution Module:**
   ```python
   # src/deckbuilder/core/layout_resolver.py
   class LayoutResolver:
       @staticmethod
       def get_layout_by_name(prs, layout_name):
           """Find layout by exact name match."""
           for layout in prs.slide_layouts:
               if layout.name == layout_name:
                   return layout
           
           # Provide helpful error with suggestions
           available = [l.name for l in prs.slide_layouts]
           similar = [name for name in available if layout_name.lower() in name.lower()]
           
           error_msg = f"Layout '{layout_name}' not found.\n"
           if similar:
               error_msg += f"Similar layouts: {similar}\n"
           error_msg += f"Available layouts: {available}"
           
           raise ValueError(error_msg)
       
       @staticmethod
       def list_available_layouts(prs):
           """List all available layout names."""
           return [layout.name for layout in prs.slide_layouts]
   ```

2. **Update SlideBuilder:**
   ```python
   # src/deckbuilder/core/slide_builder.py
   def add_slide_with_direct_mapping(self, prs, slide_data, content_formatter, image_placeholder_handler):
       layout_name = slide_data.get("layout")
       if not layout_name:
           raise ValueError("Missing 'layout' field in slide data")
       
       # NEW: Use name-based lookup
       layout = LayoutResolver.get_layout_by_name(prs, layout_name)
       slide = prs.slides.add_slide(layout)
       
       # Continue with single processing path...
   ```

3. **Remove JSON Dependencies:**
   - Remove `self.layout_mapping` usage
   - Remove layout index lookups
   - Simplify initialization

### Phase 3: Placeholder Name-Based System

**Objective:** Replace placeholder index mappings with name-based lookups

**Core Changes:**

1. **Enhanced Placeholder Resolver:**
   ```python
   # src/deckbuilder/core/placeholder_resolver.py
   class PlaceholderResolver:
       @staticmethod
       def find_placeholder_by_name(slide, field_name):
           """Find placeholder by exact name match."""
           for placeholder in slide.placeholders:
               try:
                   placeholder_name = placeholder.element.nvSpPr.cNvPr.name
                   if placeholder_name == field_name:
                       return placeholder
               except AttributeError:
                   # Some placeholders don't have accessible names
                   continue
           return None
       
       @staticmethod
       def list_placeholder_names(slide):
           """List all placeholder names in a slide."""
           names = []
           for placeholder in slide.placeholders:
               try:
                   name = placeholder.element.nvSpPr.cNvPr.name
                   placeholder_type = placeholder.placeholder_format.type
                   names.append({
                       'name': name,
                       'type': placeholder_type.name if hasattr(placeholder_type, 'name') else str(placeholder_type)
                   })
               except AttributeError:
                   continue
           return names
   ```

2. **Unified Processing Logic:**
   ```python
   # src/deckbuilder/core/slide_builder.py
   def _process_slide_fields(self, slide, slide_data, content_formatter, image_placeholder_handler):
       """Single field processing path - replaces dual processing."""
       
       successful_mappings = []
       failed_mappings = []
       
       # Process each field in slide_data
       for field_name, field_value in slide_data.get("placeholders", {}).items():
           
           # Find placeholder by name (primary method)
           placeholder = PlaceholderResolver.find_placeholder_by_name(slide, field_name)
           
           if placeholder:
               self._apply_content_to_placeholder(
                   slide, placeholder, field_name, field_value, 
                   slide_data, content_formatter, image_placeholder_handler
               )
               successful_mappings.append(field_name)
           else:
               # Provide helpful error with available names
               available_names = PlaceholderResolver.list_placeholder_names(slide)
               failed_mappings.append({
                   'field': field_name,
                   'available': [p['name'] for p in available_names]
               })
       
       # Report results
       if failed_mappings:
           self._report_mapping_failures(failed_mappings)
       
       return successful_mappings
   ```

3. **Placeholder Type Handling:**
   ```python
   def _apply_content_to_placeholder(self, slide, placeholder, field_name, field_value, slide_data, content_formatter, image_placeholder_handler):
       """Apply content based on placeholder type."""
       placeholder_type = placeholder.placeholder_format.type
       
       if placeholder_type == PP_PLACEHOLDER_TYPE.TITLE:
           self._handle_title_placeholder(placeholder, field_value)
       elif placeholder_type == PP_PLACEHOLDER_TYPE.TABLE:
           self._handle_table_placeholder(placeholder, field_name, field_value, slide_data, slide)
       elif placeholder_type == PP_PLACEHOLDER_TYPE.PICTURE:
           image_placeholder_handler.handle_image_placeholder(placeholder, field_name, field_value, slide_data)
       elif placeholder_type in [PP_PLACEHOLDER_TYPE.BODY, PP_PLACEHOLDER_TYPE.OBJECT]:
           content_formatter.add_content_to_placeholder(placeholder, field_value)
       else:
           # Generic text fallback
           if hasattr(placeholder, "text_frame"):
               placeholder.text_frame.text = str(field_value)
   ```

### Phase 4: Runtime Discovery Tools

**Objective:** Provide CLI tools for layout and placeholder discovery

**Core Changes:**

1. **CLI Commands Module:**
   ```python
   # src/deckbuilder/cli/discovery.py
   class DiscoveryCommands:
       def __init__(self, template_path):
           self.template_path = template_path
           self.prs = Presentation(template_path)
       
       def list_layouts(self):
           """List all available layouts."""
           layouts = LayoutResolver.list_available_layouts(self.prs)
           
           print("Available Layouts:")
           for i, layout_name in enumerate(layouts, 1):
               print(f"  {i:2d}. {layout_name}")
           
           return layouts
       
       def inspect_layout(self, layout_name, show_example=False):
           """Inspect placeholders in a specific layout."""
           try:
               layout = LayoutResolver.get_layout_by_name(self.prs, layout_name)
               temp_slide = self.prs.slides.add_slide(layout)
               
               placeholders = PlaceholderResolver.list_placeholder_names(temp_slide)
               
               print(f"Layout: {layout_name}")
               print(f"Placeholders ({len(placeholders)}):")
               
               for placeholder in placeholders:
                   print(f"  • {placeholder['name']} ({placeholder['type']})")
               
               if show_example:
                   self._generate_example_json(layout_name, placeholders)
               
               # Clean up temp slide
               slide_id = temp_slide.slide_id
               self.prs.part.drop_rel(slide_id)
               
           except ValueError as e:
               print(f"Error: {e}")
       
       def _generate_example_json(self, layout_name, placeholders):
           """Generate copy-paste ready JSON example."""
           example = {
               "layout": layout_name,
               "placeholders": {}
           }
           
           for placeholder in placeholders:
               name = placeholder['name']
               ptype = placeholder['type']
               
               if 'TABLE' in ptype:
                   example["placeholders"][name] = {
                       "type": "table",
                       "data": [
                           ["Header 1", "Header 2"],
                           ["Data 1", "Data 2"]
                       ]
                   }
               elif 'TITLE' in ptype:
                   example["placeholders"][name] = "Your Title Here"
               elif 'PICTURE' in ptype:
                   example["placeholders"][name] = "path/to/image.jpg"
               else:
                   example["placeholders"][name] = "Your content here"
           
           print("\nExample JSON:")
           print("```json")
           print(json.dumps({"slides": [example]}, indent=2))
           print("```")
   ```

2. **CLI Integration:**
   ```python
   # src/deckbuilder/cli/main.py
   @click.command()
   def layouts():
       """List all available slide layouts."""
       template_path = get_template_path("default.pptx")
       discovery = DiscoveryCommands(template_path)
       discovery.list_layouts()
   
   @click.command()
   @click.argument('layout_name')
   @click.option('--example', is_flag=True, help='Generate example JSON')
   def inspect(layout_name, example):
       """Inspect placeholders in a specific layout."""
       template_path = get_template_path("default.pptx")
       discovery = DiscoveryCommands(template_path)
       discovery.inspect_layout(layout_name, show_example=example)
   ```

### Phase 5: Cleanup and Validation

**Objective:** Remove legacy code and validate complete system

**Tasks:**

1. **Remove Legacy Systems:**
   ```python
   # Remove these methods/classes:
   - layout_mapping initialization
   - field_to_index mapping creation
   - index-based placeholder loops
   - semantic processing methods
   - dual processing code paths
   ```

2. **JSON File Cleanup:**
   ```bash
   # Optional: Keep for documentation only
   mv src/deckbuilder/assets/templates/default.json src/deckbuilder/assets/templates/default.json.legacy
   ```

3. **Test Updates:**
   - Update tests to use layout names instead of indices
   - Verify table processing works end-to-end
   - Test all placeholder types (TITLE, TABLE, CONTENT, PICTURE)
   - Test discovery CLI commands

4. **Validation Suite:**
   ```python
   # New validation tests
   def test_name_based_layout_selection():
       # Test exact layout name matching
       pass
   
   def test_name_based_placeholder_mapping():
       # Test field to placeholder name matching
       pass
   
   def test_table_processing_works():
       # Verify table_data creates actual tables
       pass
   
   def test_discovery_commands():
       # Test CLI discovery tools
       pass
   ```

## Error Handling

### Layout Not Found
```python
# Helpful error messages with suggestions
ValueError: Layout 'Table' not found.
Similar layouts: ['Table Only', 'Table with Content Above']
Available layouts: ['Title Slide', 'Title and Content', 'Table Only', ...]
```

### Placeholder Not Found
```python
# List available placeholders
ValueError: Field 'table_content' not found.
Available placeholders in 'Table Only': ['title_top', 'table_data', 'date_footer']
```

## Performance Considerations

1. **Layout Lookup:** O(n) where n = number of layouts (~24), negligible impact
2. **Placeholder Lookup:** O(m) where m = placeholders per slide (~5), negligible impact  
3. **Memory:** Reduced - no JSON mapping structures loaded
4. **Startup:** Faster - no mapping file parsing required

## Migration Strategy

1. **Backwards Compatibility:** None - clean break from index-based system
2. **User Migration:** Update documentation with new layout/placeholder names
3. **Test Migration:** Update test files to use exact PowerPoint names
4. **Template Updates:** Ensure meaningful placeholder names in templates

## Risk Mitigation

1. **Template Dependency:** Validate template has meaningful placeholder names
2. **Name Changes:** System resilient to template updates via name-based lookup
3. **Testing:** Comprehensive test suite covers all placeholder types
4. **Discovery:** CLI tools help users find correct names

## Success Metrics

1. **Functional:** Table creation works via `table_data` field
2. **Code Quality:** Zero index-based lookups remaining
3. **User Experience:** Clear error messages, easy discovery
4. **Maintainability:** No JSON mapping files to maintain
5. **Performance:** No degradation in processing speed