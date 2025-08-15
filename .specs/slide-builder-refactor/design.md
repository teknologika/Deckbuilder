# Design Document: Slide Builder Refactor

## Architecture Overview

This design completely refactors the 1,352-line slide_builder.py monolith into 6 focused modules under 400 lines each, eliminating all redundant code, removing markdown table support, and fixing broken functionality while maintaining backward compatibility.

**CORE PRINCIPLE: ENHANCE EXISTING CODE, DON'T CREATE ALTERNATE PATHS**

Following AI Coding Laws:
- **Law #1**: Improve code quality by removing redundancy
- **Prime Directive #4**: MINIMIZE complexity, DON'T create alternate code paths
- **User Requirement**: SUCCESS or CLEAR ERRORS - NO FALLBACKS

## Current State Analysis

### What Gets DELETED (Zero Tolerance for Redundancy)

1. **DELETE**: 92-line `_resolve_field_name_variations()` hardcoded dictionary (lines 446-538)
2. **DELETE**: `_contains_table_content()` - pure duplicate of `_is_table_markdown()`
3. **DELETE**: All layered fallback logic and complex detection paths
4. **DELETE**: All markdown parsing from table cells
5. **DELETE**: Multiple duplicate placeholder finding methods
6. **DELETE**: Legacy mapping code in `_copy_placeholder_names_from_mapping()`

### What Gets ENHANCED (Use Existing Systems)

#### Existing Systems That Work:
1. **PatternLoader** (`templates/pattern_loader.py`) - loads structured frontmatter patterns
2. **Semantic Detection** (`content/placeholder_types.py`) - detects placeholder types  
3. **Name Resolution** (`core/placeholder_resolver.py`) - finds placeholders by name
4. **Layout Resolution** (`core/layout_resolver.py`) - resolves PowerPoint layouts

#### Existing Systems Integration:
- **PRIMARY**: PatternLoader defines exact fields for each layout
- **SECONDARY**: Semantic detection finds placeholders by type
- **NO FALLBACKS**: Success or clear error messages

## Simplified Module Architecture

### Module 1: SlideCoordinator (~300 lines)
**Single Responsibility:** High-level slide creation orchestration

```python
class SlideCoordinator:
    """Simple orchestration - ENHANCE existing workflow, remove bloat"""
    
    def __init__(self, placeholder_manager: PlaceholderManager, 
                       content_processor: ContentProcessor,
                       table_handler: TableHandler,
                       shape_builder: ShapeBuilder):
        # Wire existing systems together
        
    def create_slide(self, prs, slide_data: dict, content_formatter, image_placeholder_handler) -> Slide:
        """SIMPLIFIED orchestration - replace bloated 127-line add_slide()"""
        # 1. Get layout from existing layout resolver
        # 2. Map fields using existing PatternLoader + semantic detection
        # 3. Apply content using enhanced processors
        # 4. Handle speaker notes
        
    def clear_slides(self, prs) -> None:
        """ENHANCE existing clear_slides logic"""
        
    def add_speaker_notes(self, slide, notes_content: str, content_formatter) -> None:
        """ENHANCE existing speaker notes logic"""
```

### Module 2: PlaceholderManager (~350 lines)
**Single Responsibility:** Use existing systems to map fields to placeholders

```python
class PlaceholderManager:
    """ENHANCE existing PatternLoader + semantic detection - NO fallbacks"""
    
    def __init__(self, layout_resolver: LayoutResolver):
        # USE existing PatternLoader
        from ..templates.pattern_loader import PatternLoader
        self.pattern_loader = PatternLoader()
        
        # USE existing semantic detection
        from ..content.placeholder_types import (
            is_title_placeholder, is_content_placeholder, is_media_placeholder
        )
        self.semantic_detector = {
            'title': is_title_placeholder,
            'content': is_content_placeholder,
            'media': is_media_placeholder
        }
    
    def map_fields_to_placeholders(self, slide, slide_data: dict, layout_name: str) -> Dict[str, Placeholder]:
        """SIMPLE mapping: Pattern defines fields → Semantic detection finds placeholders"""
        
        # Get pattern from existing PatternLoader
        pattern = self.pattern_loader.get_pattern_for_layout(layout_name)
        if not pattern:
            raise ValueError(f"No pattern found for layout '{layout_name}' - check structured_frontmatter_patterns/")
        
        # Pattern yaml_pattern defines exact expected fields
        expected_fields = pattern.get("yaml_pattern", {})
        
        mapped_placeholders = {}
        for field_name, field_value in slide_data.items():
            if field_name in expected_fields:
                # Use semantic detection to find placeholder
                placeholder = self._find_placeholder_semantically(slide, field_name)
                if placeholder:
                    mapped_placeholders[field_name] = placeholder
                else:
                    raise ValueError(f"Cannot find {field_name} placeholder on slide for layout '{layout_name}'")
        
        return mapped_placeholders
        
    def _find_placeholder_semantically(self, slide, field_name: str) -> Optional[Placeholder]:
        """USE existing semantic detection based on field name"""
        if field_name == "title" or field_name.startswith("title_"):
            return self._find_by_semantic_type(slide, 'title')
        elif field_name == "content" or field_name.startswith("content_"):
            return self._find_by_semantic_type(slide, 'content')
        elif field_name == "image" or "image" in field_name:
            return self._find_by_semantic_type(slide, 'media')
        else:
            # Clear error - no fallback
            raise ValueError(f"Unknown field type '{field_name}' - update semantic mapping")
```

### Module 3: ContentProcessor (~400 lines)
**Single Responsibility:** ENHANCE existing content application

```python
class ContentProcessor:
    """ENHANCE existing content formatting - remove complexity"""
    
    def apply_content_to_placeholder(self, placeholder, content, formatting_options: dict) -> None:
        """ENHANCED version of existing content application"""
        
    def apply_inline_formatting(self, text: str, paragraph) -> None:
        """USE existing inline formatting logic"""
        
    def calculate_font_sizing(self, placeholder) -> FontInfo:
        """ENHANCE existing _get_placeholder_font_size"""
```

### Module 4: TableHandler (~300 lines)
**Single Responsibility:** SIMPLIFY existing table processing

```python
class TableHandler:
    """ENHANCE existing table detection - REMOVE markdown parsing"""
    
    def detect_table_content(self, content: str) -> bool:
        """ENHANCE existing _is_table_markdown - remove _contains_table_content duplicate"""
        
    def create_table_from_data(self, slide, table_data: dict, position: Position) -> Table:
        """ENHANCE existing table creation - PLAIN TEXT ONLY"""
        
    def parse_table_structure(self, table_text: str) -> TableData:
        """SIMPLIFIED: Plain text only, NO markdown parsing"""
        lines = [line.strip() for line in table_text.split('\n') if line.strip()]
        table_data = []
        for line in lines:
            if '|' in line and not self._is_separator_line(line):
                # Plain text cells only
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                table_data.append(cells)
        return TableData(data=table_data, type="table")
```

### Module 5: ShapeBuilder (~400 lines)
**Single Responsibility:** FIX existing dynamic shape creation

```python
class ShapeBuilder:
    """FIX existing dynamic shape positioning issues"""
    
    def create_dynamic_shapes(self, slide, content_segments: List[ContentSegment]) -> List[Shape]:
        """FIX existing _create_dynamic_content_shapes positioning bugs"""
        
    def calculate_shape_positioning(self, slide, existing_content) -> List[Position]:
        """FIX broken positioning logic - no overlap, proper spacing"""
```

### Module 6: LayoutResolver (~200 lines)
**Single Responsibility:** USE existing layout resolution

```python
class LayoutResolver:
    """USE existing layout resolution systems"""
    
    def __init__(self):
        # USE existing layout resolution from core/layout_resolver.py
        
    def resolve_layout_by_name(self, prs, layout_name: str) -> SlideLayout:
        """USE existing layout resolution logic"""
```

## Simple Flow (No Fallbacks)

```
1. PatternLoader.get_pattern_for_layout(layout_name)
   ↓ SUCCESS: Pattern found with yaml_pattern fields
   ↓ ERROR: "No pattern found for layout 'X' - check structured_frontmatter_patterns/"

2. For each field in pattern.yaml_pattern:
   ↓ Semantic detection finds placeholder by field type
   ↓ SUCCESS: Placeholder found and mapped
   ↓ ERROR: "Cannot find {field_name} placeholder on slide for layout 'X'"

3. Apply content to mapped placeholders
   ↓ SUCCESS: Content applied
   ↓ ERROR: Clear error about what failed

4. Create dynamic shapes if needed
   ↓ SUCCESS: Shapes positioned correctly
   ↓ ERROR: Clear error about positioning failure
```

## Integration with Existing Systems

### PatternLoader Integration
```python
# USE existing structured_frontmatter_patterns system
pattern = self.pattern_loader.get_pattern_for_layout("Title and Content")
# Returns: {
#   "yaml_pattern": {"layout": "Title and Content", "title": "str", "content": "str"},
#   "validation": {"required_fields": ["title"], "optional_fields": ["content"]}
# }
```

### Semantic Detection Integration
```python
# USE existing placeholder_types.py functions
from ..content.placeholder_types import is_title_placeholder, is_content_placeholder

# Map field types to semantic detection
if field_name.startswith("title"):
    for placeholder in slide.placeholders:
        if is_title_placeholder(placeholder.placeholder_format.type):
            return placeholder
```

## Table Processing Simplification

### BEFORE (Complex - Gets Deleted):
- Parse markdown within table cells
- Preserve bold, italic, links
- Complex formatting detection
- Multiple parsing code paths

### AFTER (Simple - Enhanced):
```python
def parse_table_structure(self, table_text: str) -> TableData:
    """Plain text only - enhance existing _is_table_markdown"""
    lines = [line.strip() for line in table_text.split('\n') if line.strip()]
    table_data = []
    for line in lines:
        if '|' in line and not self._is_separator_line(line):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_data.append(cells)
    return TableData(data=table_data, type="table")
```

## API Compatibility Layer

### Backward Compatibility Wrapper
```python
class SlideBuilder:
    """Legacy API wrapper - maintains exact same interface"""
    
    def __init__(self):
        # Initialize enhanced modules using existing systems
        self.coordinator = SlideCoordinator(...)
        
    def add_slide(self, prs, slide_data: dict, content_formatter, image_placeholder_handler):
        """Delegates to enhanced coordinator"""
        return self.coordinator.create_slide(prs, slide_data, content_formatter, image_placeholder_handler)
```

## Success Metrics

### Quantitative Results:
- **File count**: 6 focused modules (vs 1 monolith)
- **Lines per module**: ≤400 (vs 1,352)
- **Code elimination**: 60% reduction through redundancy removal
- **Method elimination**: Remove duplicate methods completely
- **Table performance**: 50%+ faster with plain text only

### Qualitative Results:
- **Clear errors**: "No pattern found for layout 'X'" instead of silent fallbacks
- **Enhanced existing**: PatternLoader + semantic detection work better together
- **Zero fallbacks**: Success or clear error messages
- **Simplified flow**: One path through the system
- **Better maintainability**: Each module has single responsibility

## Migration Strategy

### Phase 1: Extract and Enhance TableHandler
- ENHANCE existing `_is_table_markdown()`
- DELETE `_contains_table_content()` duplicate
- REMOVE all markdown parsing from cells

### Phase 2: Extract and Enhance PlaceholderManager  
- USE existing PatternLoader
- USE existing semantic detection
- DELETE 92-line hardcoded variations dictionary

### Phase 3: Extract and Enhance ContentProcessor
- ENHANCE existing content application
- REMOVE complex formatting paths

### Phase 4: Extract and Fix ShapeBuilder
- FIX existing positioning bugs
- ENHANCE existing shape creation

### Phase 5: Extract and Simplify SlideCoordinator
- REPLACE bloated 127-line add_slide()
- USE existing orchestration patterns

### Phase 6: Integrate with LayoutResolver
- USE existing layout resolution
- Wire all enhanced modules together

Each phase: ENHANCE existing code, DELETE redundant code, NO new alternate paths.