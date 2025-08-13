# Implementation Tasks: Name-Based Placeholder Refactor

## Overview
This document breaks down the name-based placeholder refactor into detailed, actionable implementation tasks. Each task includes specific files to modify, code changes to make, and validation steps.

## Phase 1: Baseline & Analysis (30 minutes)

### Task 1.1: Create Baseline Commit
**Objective:** Establish stable starting point before refactor
**Estimated Time:** 10 minutes

**Steps:**
1. Run full test suite to ensure current state is stable:
   ```bash
   source .venv/bin/activate
   pytest tests/ --tb=short > baseline_test_results.txt
   black --line-length 200 src/
   flake8 src/ tests/ --max-line-length=200 --ignore=E203,W503,E501
   ```

2. Create baseline commit:
   ```bash
   git add -A
   git commit -m "BASELINE: Pre-refactor state - all tests passing
   
   Establishing baseline before name-based placeholder refactor.
   All systems working with index-based mappings and dual processing paths.
   
   Current Issues:
   - Table processing fails due to dual code paths
   - Index-based mappings create maintenance burden
   - JSON mapping files duplicate PowerPoint template information
   
   🤖 Generated with [Claude Code](https://claude.ai/code)
   
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

**Validation:** Commit created successfully, test results saved

### Task 1.2: Map Index-Based Dependencies
**Objective:** Document all current index-based usage
**Estimated Time:** 15 minutes

**Steps:**
1. Find layout index usage:
   ```bash
   grep -r "slide_layouts\[" src/ > analysis_layout_indices.txt
   grep -r "layout_index\|layouts.*index" src/ >> analysis_layout_indices.txt
   ```

2. Find placeholder index usage:
   ```bash
   grep -r "placeholder_format\.idx" src/ > analysis_placeholder_indices.txt
   grep -r "field_to_index\|placeholder_mappings" src/ >> analysis_placeholder_indices.txt
   ```

3. Find JSON mapping dependencies:
   ```bash
   grep -r "layout_mapping\|self\.layout_mapping" src/ > analysis_json_dependencies.txt
   ```

**Expected Findings:**
- `slide_builder.py`: Multiple uses of `placeholder.placeholder_format.idx`
- `slide_builder.py`: `layout_index = self.layout_mapping["layouts"][layout_name]["index"]`
- `slide_builder.py`: `field_to_index` mapping creation
- `engine.py`: Layout mapping initialization

**Validation:** Analysis files created with complete dependency mapping

### Task 1.3: Document Current Processing Flow
**Objective:** Map execution paths and identify dual processing points
**Estimated Time:** 5 minutes

**Steps:**
1. Create flow documentation:
   ```python
   # docs/current_processing_flow.md
   ## Current Processing Flow Analysis
   
   ### Entry Point: add_slide_with_direct_mapping()
   1. Layout lookup via index: `layout = prs.slide_layouts[layout_index]`
   2. Field processing loop: Attempts to map fields to placeholders
   3. Semantic processing: Handles placeholders by type
   
   ### Dual Processing Paths:
   - Field-driven: Fails for table_data fields
   - Type-driven: Creates empty placeholder structures
   
   ### Table Processing Failure Point:
   - Field processing can't find table_data placeholder
   - Semantic processing creates empty TABLE placeholder
   - No coordination between the two systems
   ```

**Validation:** Processing flow documented, dual paths identified

## Phase 2: Layout Name-Based System (45 minutes)

### Task 2.1: Create LayoutResolver Module
**Objective:** Implement name-based layout lookup system
**Estimated Time:** 20 minutes

**Files to Create:**
- `src/deckbuilder/core/layout_resolver.py`

**Implementation:**
```python
"""Layout resolution utilities for name-based lookups."""

from typing import List
from pptx import Presentation


class LayoutResolver:
    """Provides name-based layout resolution functionality."""
    
    @staticmethod
    def get_layout_by_name(prs: Presentation, layout_name: str):
        """
        Find layout by exact name match.
        
        Args:
            prs: PowerPoint presentation object
            layout_name: Exact layout name to find
            
        Returns:
            Layout object if found
            
        Raises:
            ValueError: If layout not found with helpful suggestions
        """
        # Direct name matching
        for layout in prs.slide_layouts:
            if layout.name == layout_name:
                return layout
        
        # Generate helpful error with suggestions
        available = [l.name for l in prs.slide_layouts]
        similar = [name for name in available if layout_name.lower() in name.lower()]
        
        error_msg = f"Layout '{layout_name}' not found.\n"
        if similar:
            error_msg += f"Similar layouts: {similar}\n"
        error_msg += f"Available layouts: {available}"
        
        raise ValueError(error_msg)
    
    @staticmethod
    def list_available_layouts(prs: Presentation) -> List[str]:
        """
        List all available layout names.
        
        Args:
            prs: PowerPoint presentation object
            
        Returns:
            List of layout names
        """
        return [layout.name for layout in prs.slide_layouts]
    
    @staticmethod
    def validate_layout_exists(prs: Presentation, layout_name: str) -> bool:
        """
        Check if layout exists without raising exception.
        
        Args:
            prs: PowerPoint presentation object
            layout_name: Layout name to check
            
        Returns:
            True if layout exists, False otherwise
        """
        try:
            LayoutResolver.get_layout_by_name(prs, layout_name)
            return True
        except ValueError:
            return False
```

**Validation:**
1. Import test: `from deckbuilder.core.layout_resolver import LayoutResolver`
2. Function test: Successfully finds "Table Only" layout
3. Error test: Provides helpful suggestions for invalid layout names

### Task 2.2: Update SlideBuilder to Use LayoutResolver
**Objective:** Replace index-based layout lookup with name-based
**Estimated Time:** 15 minutes

**Files to Modify:**
- `src/deckbuilder/core/slide_builder.py`

**Changes:**

1. **Add import:**
```python
from .layout_resolver import LayoutResolver
```

2. **Replace layout lookup logic in `add_slide_with_direct_mapping()`:**

**OLD CODE:**
```python
layout_name = slide_data.get("layout")
layouts = self.layout_mapping.get("layouts", {})
layout_info = layouts.get(layout_name, {})
layout_index = layout_info.get("index")
if layout_index is None:
    raise ValueError(f"Unknown layout: {layout_name}")
layout = prs.slide_layouts[layout_index]
```

**NEW CODE:**
```python
layout_name = slide_data.get("layout")
if not layout_name:
    raise ValueError("Missing 'layout' field in slide data")

# Use name-based lookup
layout = LayoutResolver.get_layout_by_name(prs, layout_name)
```

3. **Remove layout_mapping dependency from `__init__()`:**

**OLD CODE:**
```python
def __init__(self, layout_mapping=None):
    self.layout_mapping = layout_mapping or {}
```

**NEW CODE:**
```python
def __init__(self):
    pass  # No layout mapping needed
```

**Validation:**
1. Test layout lookup works: Create slide with "Table Only" layout
2. Test error handling: Try invalid layout name, verify helpful error message
3. Verify no JSON dependencies: No references to `self.layout_mapping`

### Task 2.3: Update Engine to Remove Layout Mapping
**Objective:** Remove JSON layout mapping initialization
**Estimated Time:** 10 minutes

**Files to Modify:**
- `src/deckbuilder/core/engine.py`

**Changes:**

1. **Remove layout mapping loading:**
```python
# OLD: Remove this entire section
if self.layout_mapping_path and os.path.exists(self.layout_mapping_path):
    with open(self.layout_mapping_path, 'r') as f:
        self.layout_mapping = json.load(f)

# NEW: No layout mapping needed
# Layout names come directly from PowerPoint template
```

2. **Update SlideBuilder initialization:**
```python
# OLD
slide_builder = SlideBuilder(layout_mapping=self.layout_mapping)

# NEW  
slide_builder = SlideBuilder()
```

3. **Remove layout mapping attributes:**
```python
# Remove these from __init__:
self.layout_mapping_path = ...
self.layout_mapping = ...
```

**Validation:**
1. Engine initializes successfully without JSON file
2. Slide creation still works using layout names
3. No references to layout_mapping remain

## Phase 3: Placeholder Name-Based System (60 minutes)

### Task 3.1: Create PlaceholderResolver Module
**Objective:** Implement name-based placeholder lookup system
**Estimated Time:** 25 minutes

**Files to Create:**
- `src/deckbuilder/core/placeholder_resolver.py`

**Implementation:**
```python
"""Placeholder resolution utilities for name-based lookups."""

from typing import List, Dict, Optional, Any
from pptx.shapes.placeholder import SlidePlaceholder


class PlaceholderResolver:
    """Provides name-based placeholder resolution functionality."""
    
    @staticmethod
    def find_placeholder_by_name(slide, field_name: str) -> Optional[SlidePlaceholder]:
        """
        Find placeholder by exact name match.
        
        Args:
            slide: PowerPoint slide object
            field_name: Field name to match against placeholder names
            
        Returns:
            Placeholder object if found, None otherwise
        """
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
    def list_placeholder_names(slide) -> List[Dict[str, Any]]:
        """
        List all placeholder names in a slide.
        
        Args:
            slide: PowerPoint slide object
            
        Returns:
            List of dicts with name, type, and index information
        """
        names = []
        for placeholder in slide.placeholders:
            try:
                name = placeholder.element.nvSpPr.cNvPr.name
                placeholder_type = placeholder.placeholder_format.type
                type_name = placeholder_type.name if hasattr(placeholder_type, 'name') else str(placeholder_type)
                
                names.append({
                    'name': name,
                    'type': type_name,
                    'type_value': placeholder_type,
                    'index': placeholder.placeholder_format.idx  # For debugging only
                })
            except AttributeError:
                # Skip placeholders without accessible names
                continue
        return names
    
    @staticmethod
    def find_placeholders_by_type(slide, placeholder_type) -> List[SlidePlaceholder]:
        """
        Find all placeholders of a specific type.
        
        Args:
            slide: PowerPoint slide object
            placeholder_type: PP_PLACEHOLDER_TYPE to search for
            
        Returns:
            List of matching placeholders
        """
        matches = []
        for placeholder in slide.placeholders:
            if placeholder.placeholder_format.type == placeholder_type:
                matches.append(placeholder)
        return matches
    
    @staticmethod
    def get_available_names_summary(slide) -> str:
        """
        Get a formatted summary of available placeholder names.
        
        Args:
            slide: PowerPoint slide object
            
        Returns:
            Formatted string listing available placeholders
        """
        placeholders = PlaceholderResolver.list_placeholder_names(slide)
        if not placeholders:
            return "No placeholders found"
        
        summary = "Available placeholders:\n"
        for ph in placeholders:
            summary += f"  • {ph['name']} ({ph['type']})\n"
        
        return summary.rstrip()
```

**Validation:**
1. Import test: `from deckbuilder.core.placeholder_resolver import PlaceholderResolver`
2. Name lookup test: Find "table_data" placeholder by name
3. List test: Get all placeholder names in "Table Only" layout
4. Type lookup test: Find all TABLE type placeholders

### Task 3.2: Replace Dual Processing with Single Field Processing
**Objective:** Eliminate competing code paths, use single name-based system
**Estimated Time:** 25 minutes

**Files to Modify:**
- `src/deckbuilder/core/slide_builder.py`

**Changes:**

1. **Add import:**
```python
from .placeholder_resolver import PlaceholderResolver
```

2. **Replace dual processing logic in `add_slide_with_direct_mapping()`:**

**OLD CODE (Remove entirely):**
```python
# Remove field_to_index mapping creation
field_to_index = {}
for placeholder_idx, field_name in placeholder_mappings.items():
    field_to_index[field_name] = int(placeholder_idx)

# Remove complex field processing with index lookups
for field_name, field_value in slide_data.get("placeholders", {}).items():
    # Complex index-based matching logic
    if target_field in field_to_index:
        placeholder_idx = field_to_index[target_field]
        for placeholder in slide.placeholders:
            if placeholder.placeholder_format.idx == placeholder_idx:
                # Process placeholder

# Remove semantic processing methods
self._apply_content_by_semantic_type(...)
```

**NEW CODE (Single processing path):**
```python
def _process_slide_fields(self, slide, slide_data, content_formatter, image_placeholder_handler):
    """Single field processing path - replaces all dual processing."""
    
    successful_mappings = []
    failed_mappings = []
    
    # Process each field in slide_data using name-based lookup
    for field_name, field_value in slide_data.get("placeholders", {}).items():
        
        # Primary method: Find placeholder by name
        placeholder = PlaceholderResolver.find_placeholder_by_name(slide, field_name)
        
        if placeholder:
            # Apply content based on placeholder type
            self._apply_content_to_placeholder(
                slide, placeholder, field_name, field_value,
                slide_data, content_formatter, image_placeholder_handler
            )
            successful_mappings.append(field_name)
        else:
            # Helpful error with available options
            available_summary = PlaceholderResolver.get_available_names_summary(slide)
            failed_mappings.append({
                'field': field_name,
                'available_summary': available_summary
            })
    
    # Report any failures
    if failed_mappings:
        self._report_mapping_failures(failed_mappings, slide_data.get("layout", "Unknown"))
    
    return successful_mappings

def _report_mapping_failures(self, failed_mappings, layout_name):
    """Report placeholder mapping failures with helpful information."""
    print(f"\n❌ PLACEHOLDER MAPPING FAILURES in layout '{layout_name}':")
    
    for failure in failed_mappings:
        print(f"\n  Field '{failure['field']}' could not be mapped to any placeholder")
        print(f"  {failure['available_summary']}")
    
    print()
```

3. **Update main processing call:**
```python
# In add_slide_with_direct_mapping(), replace dual processing with:
successful_mappings = self._process_slide_fields(
    slide, slide_data, content_formatter, image_placeholder_handler
)
```

**Validation:**
1. Single code path: Only `_process_slide_fields()` handles all placeholders
2. Name-based lookup: All placeholders found by name, not index
3. Clear errors: Failed mappings show available placeholder names

### Task 3.3: Implement Unified Placeholder Type Handling
**Objective:** Handle all placeholder types through single method
**Estimated Time:** 10 minutes

**Files to Modify:**
- `src/deckbuilder/core/slide_builder.py`

**Changes:**

1. **Create unified content application method:**
```python
def _apply_content_to_placeholder(self, slide, placeholder, field_name, field_value, slide_data, content_formatter, image_placeholder_handler):
    """
    Apply content to placeholder based on its type.
    
    This method replaces all type-specific processing logic with a single,
    unified approach that handles all placeholder types consistently.
    """
    from pptx.enum.shapes import PP_PLACEHOLDER_TYPE
    
    placeholder_type = placeholder.placeholder_format.type
    debug_print(f"  Processing {field_name} -> {placeholder_type} placeholder")
    
    # Handle each placeholder type appropriately
    if placeholder_type == PP_PLACEHOLDER_TYPE.TITLE:
        self._handle_title_placeholder(placeholder, field_value)
        
    elif placeholder_type == PP_PLACEHOLDER_TYPE.TABLE:
        self._handle_table_placeholder(placeholder, field_name, field_value, slide_data, slide)
        
    elif placeholder_type == PP_PLACEHOLDER_TYPE.PICTURE:
        image_placeholder_handler.handle_image_placeholder(placeholder, field_name, field_value, slide_data)
        
    elif placeholder_type in [PP_PLACEHOLDER_TYPE.BODY, PP_PLACEHOLDER_TYPE.OBJECT]:
        content_formatter.add_content_to_placeholder(placeholder, field_value)
        
    else:
        # Generic text fallback for unknown types
        if hasattr(placeholder, "text_frame") and placeholder.text_frame:
            placeholder.text_frame.text = str(field_value)
        elif hasattr(placeholder, "text"):
            placeholder.text = str(field_value)
        else:
            debug_print(f"    Warning: Don't know how to handle {placeholder_type} placeholder")

def _handle_title_placeholder(self, placeholder, field_value):
    """Handle TITLE type placeholders."""
    if hasattr(placeholder, "text_frame") and placeholder.text_frame:
        placeholder.text_frame.text = str(field_value)
    elif hasattr(placeholder, "text"):
        placeholder.text = str(field_value)
```

2. **Ensure `_handle_table_placeholder` method exists and is called:**
```python
# Verify this method exists and gets called for TABLE placeholders
def _handle_table_placeholder(self, placeholder, field_name, field_value, slide_data, slide):
    """Handle TABLE placeholder by creating table directly in placeholder space."""
    debug_print(f"  Handling TABLE placeholder for field: {field_name}")
    # ... existing implementation should work correctly now
```

**Validation:**
1. All placeholder types handled: TITLE, TABLE, CONTENT, PICTURE all work
2. Table processing called: `_handle_table_placeholder` receives TABLE placeholders
3. Unified processing: Single method handles all types consistently

## Phase 4: Runtime Discovery Tools (30 minutes)

### Task 4.1: Create Discovery CLI Module
**Objective:** Implement CLI commands for layout and placeholder discovery
**Estimated Time:** 20 minutes

**Files to Create:**
- `src/deckbuilder/cli/discovery.py`

**Implementation:**
```python
"""CLI commands for discovering layouts and placeholders."""

import json
from pptx import Presentation
from ..core.layout_resolver import LayoutResolver
from ..core.placeholder_resolver import PlaceholderResolver


class DiscoveryCommands:
    """Provides CLI commands for template discovery."""
    
    def __init__(self, template_path: str):
        """
        Initialize discovery commands.
        
        Args:
            template_path: Path to PowerPoint template file
        """
        self.template_path = template_path
        self.prs = Presentation(template_path)
    
    def list_layouts(self) -> None:
        """List all available slide layouts."""
        layouts = LayoutResolver.list_available_layouts(self.prs)
        
        print(f"Available Layouts ({len(layouts)}):")
        print(f"Template: {self.template_path}")
        print()
        
        for i, layout_name in enumerate(layouts, 1):
            print(f"  {i:2d}. {layout_name}")
        
        print()
        print("Usage: deckbuilder inspect \"<layout_name>\" to see placeholders")
    
    def inspect_layout(self, layout_name: str, show_example: bool = False) -> None:
        """
        Inspect placeholders in a specific layout.
        
        Args:
            layout_name: Name of layout to inspect
            show_example: Whether to generate example JSON
        """
        try:
            # Create temporary slide to inspect placeholders
            layout = LayoutResolver.get_layout_by_name(self.prs, layout_name)
            temp_slide = self.prs.slides.add_slide(layout)
            
            # Get placeholder information
            placeholders = PlaceholderResolver.list_placeholder_names(temp_slide)
            
            print(f"Layout: {layout_name}")
            print(f"Placeholders ({len(placeholders)}):")
            print()
            
            if placeholders:
                for placeholder in placeholders:
                    print(f"  • {placeholder['name']} ({placeholder['type']})")
            else:
                print("  No placeholders found")
            
            if show_example and placeholders:
                print()
                self._generate_example_json(layout_name, placeholders)
            
            # Clean up temporary slide
            self._cleanup_temp_slide(temp_slide)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def _generate_example_json(self, layout_name: str, placeholders: list) -> None:
        """Generate copy-paste ready JSON example."""
        example = {
            "layout": layout_name,
            "placeholders": {}
        }
        
        # Generate appropriate example content for each placeholder type
        for placeholder in placeholders:
            name = placeholder['name']
            ptype = placeholder['type']
            
            if 'TABLE' in ptype.upper():
                example["placeholders"][name] = {
                    "type": "table",
                    "data": [
                        ["Header 1", "Header 2", "Header 3"],
                        ["Data 1", "Data 2", "Data 3"],
                        ["Data 4", "Data 5", "Data 6"]
                    ],
                    "header_style": "dark_blue_white_text",
                    "row_style": "alternating_light_gray"
                }
            elif 'TITLE' in ptype.upper():
                example["placeholders"][name] = "Your Slide Title Here"
            elif 'PICTURE' in ptype.upper():
                example["placeholders"][name] = "path/to/your/image.jpg"
            elif 'DATE' in ptype.upper():
                example["placeholders"][name] = "2024-08-13"
            elif 'FOOTER' in ptype.upper():
                example["placeholders"][name] = "Footer text"
            elif 'SLIDE_NUMBER' in ptype.upper():
                example["placeholders"][name] = "1"
            else:
                example["placeholders"][name] = "Your content here"
        
        print("Example JSON:")
        print("```json")
        print(json.dumps({"slides": [example]}, indent=2))
        print("```")
        
        print()
        print("Copy the JSON above and modify the content as needed.")
    
    def _cleanup_temp_slide(self, temp_slide) -> None:
        """Clean up temporary slide used for inspection."""
        try:
            # Remove the temporary slide
            slide_id = temp_slide.slide_id
            slides = self.prs.slides
            slide_index = None
            
            for i, slide in enumerate(slides):
                if slide.slide_id == slide_id:
                    slide_index = i
                    break
            
            if slide_index is not None:
                xml_slides = self.prs.part.rels
                for rel in xml_slides.values():
                    if hasattr(rel, 'target_part') and hasattr(rel.target_part, 'slide_id'):
                        if rel.target_part.slide_id == slide_id:
                            self.prs.part.drop_rel(rel.rId)
                            break
        except Exception:
            # If cleanup fails, it's not critical for functionality
            pass
```

**Validation:**
1. Import test: `from deckbuilder.cli.discovery import DiscoveryCommands`
2. List layouts: Shows all available PowerPoint layouts
3. Inspect layout: Shows placeholders for specific layout
4. Example generation: Creates valid JSON with appropriate sample content

### Task 4.2: Integrate Discovery Commands into CLI
**Objective:** Add new commands to main CLI interface
**Estimated Time:** 10 minutes

**Files to Modify:**
- `src/deckbuilder/cli/main.py`

**Changes:**

1. **Add imports:**
```python
from .discovery import DiscoveryCommands
```

2. **Add new CLI commands:**
```python
@cli.command()
@click.option('--template', default='default', help='Template name to inspect')
def layouts(template):
    """List all available slide layouts."""
    try:
        template_path = get_template_path(f"{template}.pptx")
        discovery = DiscoveryCommands(template_path)
        discovery.list_layouts()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1

@cli.command()
@click.argument('layout_name')
@click.option('--example', is_flag=True, help='Generate example JSON')
@click.option('--template', default='default', help='Template name to use')
def inspect(layout_name, example, template):
    """Inspect placeholders in a specific layout."""
    try:
        template_path = get_template_path(f"{template}.pptx")
        discovery = DiscoveryCommands(template_path)
        discovery.inspect_layout(layout_name, show_example=example)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
```

3. **Update CLI help:**
```python
# Add to main CLI group description
@click.group()
def cli():
    """
    Deckbuilder - PowerPoint presentation generator
    
    Common workflows:
      deckbuilder layouts                    # List available layouts
      deckbuilder inspect "Table Only"      # Show placeholders
      deckbuilder inspect "Table Only" --example  # Generate JSON template
      deckbuilder create input.json --output presentation  # Create presentation
    """
    pass
```

**Validation:**
1. CLI commands work: `deckbuilder layouts` and `deckbuilder inspect` commands available
2. Help integration: Commands appear in help output
3. Template support: Works with different template files

## Phase 5: Cleanup & Validation (30 minutes)

### Task 5.1: Remove Legacy Index-Based Code
**Objective:** Eliminate all index-based lookup code
**Estimated Time:** 15 minutes

**Files to Modify:**
- `src/deckbuilder/core/slide_builder.py`
- `src/deckbuilder/core/engine.py`

**Changes:**

1. **Remove from slide_builder.py:**
```python
# Remove these methods entirely:
- Any remaining field_to_index usage
- placeholder_format.idx matching loops  
- layout_mapping references
- _apply_content_by_semantic_type (if exists)
- Dual processing code paths

# Search and remove:
grep -n "placeholder_format\.idx\|field_to_index\|layout_mapping" src/deckbuilder/core/slide_builder.py
```

2. **Remove from engine.py:**
```python
# Remove layout mapping initialization
- layout_mapping_path parameter
- JSON mapping file loading
- layout_mapping attribute
```

3. **Update all method signatures:**
```python
# Remove layout_mapping parameters from all methods
# Update calls to SlideBuilder to not pass layout_mapping
```

**Validation:**
1. No index references: `grep -r "placeholder_format\.idx" src/` returns nothing
2. No JSON mapping: `grep -r "layout_mapping" src/` returns nothing  
3. Tests still pass: Basic functionality works without index system

### Task 5.2: Update Tests for Name-Based System
**Objective:** Ensure test suite works with new name-based approach
**Estimated Time:** 10 minutes

**Files to Modify:**
- `tests/` (various test files)

**Changes:**

1. **Update test data to use layout names:**
```python
# OLD test data
{"layout": "title_slide", ...}  # If using aliases

# NEW test data  
{"layout": "Title Slide", ...}  # Use exact PowerPoint layout names
```

2. **Update placeholder field names:**
```python
# Ensure test JSON uses exact placeholder names from PowerPoint template
{
  "placeholders": {
    "title_top": "Test Title",
    "table_data": {"type": "table", "data": [...]},
    "date_footer": "2024-08-13"
  }
}
```

3. **Add name-based validation tests:**
```python
def test_layout_name_based_lookup():
    """Test layout lookup by name."""
    from deckbuilder.core.layout_resolver import LayoutResolver
    # Test implementation

def test_placeholder_name_based_lookup():
    """Test placeholder lookup by name.""" 
    from deckbuilder.core.placeholder_resolver import PlaceholderResolver
    # Test implementation

def test_table_processing_works():
    """Test that table_data field creates actual tables."""
    # Create presentation with table_data
    # Verify table exists in output
    pass
```

**Validation:**
1. All tests pass: `pytest tests/` succeeds
2. Name-based tests: New validation tests pass
3. Table creation: table_data field successfully creates tables

### Task 5.3: Final System Validation
**Objective:** Verify complete system works end-to-end
**Estimated Time:** 5 minutes

**Validation Steps:**

1. **Test Discovery Commands:**
```bash
deckbuilder layouts
deckbuilder inspect "Table Only"
deckbuilder inspect "Table Only" --example
```

2. **Test Table Creation:**
```bash
# Create test file with table_data
echo '{
  "slides": [{
    "layout": "Table Only", 
    "placeholders": {
      "title_top": "Test Table",
      "table_data": {
        "type": "table",
        "data": [["A", "B"], ["1", "2"]]
      }
    }
  }]
}' > test_name_based.json

deckbuilder create test_name_based.json --output final_validation
```

3. **Analyze Generated Presentation:**
```python
# Verify table was created successfully
from pptx import Presentation
prs = Presentation("final_validation.YYYY-MM-DD_HHMM.g.pptx")
slide = prs.slides[0]

# Check for table shape
table_found = False
for shape in slide.shapes:
    if hasattr(shape, 'table'):
        table_found = True
        print(f"✅ Table created with {len(shape.table.rows)} rows")
        break

if not table_found:
    print("❌ Table not created")
```

**Success Criteria:**
1. ✅ Discovery commands work and show correct information
2. ✅ Table creation works via table_data field  
3. ✅ Layout selection works via exact layout names
4. ✅ All placeholder types (TITLE, TABLE, CONTENT, PICTURE) function correctly
5. ✅ Error messages are helpful and show available options
6. ✅ No index-based code remains in codebase
7. ✅ System is faster (no JSON parsing) and more maintainable

## Summary

Upon completion of all tasks:

### Eliminated Systems:
- ❌ Index-based layout lookups
- ❌ Index-based placeholder mappings  
- ❌ JSON mapping files
- ❌ Dual processing code paths
- ❌ Template synchronization burden

### New Systems:
- ✅ Name-based layout resolution
- ✅ Name-based placeholder resolution
- ✅ Single field processing pipeline
- ✅ Runtime discovery CLI tools
- ✅ Helpful error messages with suggestions

### Benefits Achieved:
- 🎯 **Table Processing Fixed**: table_data field works correctly
- 🧹 **Ultra-DRY System**: PowerPoint template is single source of truth
- 🚀 **Better Performance**: Faster startup, less memory usage
- 🛠️ **Easier Maintenance**: No JSON mapping files to maintain
- 👥 **Better UX**: Clear errors, easy discovery, intuitive names

The system is now truly name-based with PowerPoint templates as the authoritative schema definition.