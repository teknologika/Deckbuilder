# Template Discovery & Self-Documentation System

## 📋 TODO / Implementation Status

### ✅ COMPLETED
- **Part A(Structured Frontmatter)**: ✅ IMPLEMENTED
  - ✅ `StructuredFrontmatterRegistry` class created
  - ✅ Support for Four Columns, Two Content, Comparison, Picture with Caption layouts
  - ✅ One-way conversion from structured YAML to placeholder mappings
  - ✅ Integration with markdown parser (`parse_markdown_with_frontmatter`)
  - ✅ Template mapping system loading (`_ensure_layout_mapping`)
  - ✅ Validation system for structured frontmatter
  - ✅ Working end-to-end with test presentations

### 🔄 IN PROGRESS
- **Template Loading Fixes**: ✅ COMPLETED
  - ✅ Fixed layout mapping not being loaded during markdown parsing
  - ✅ Fixed template fallback to src folder when environment variables not set
  - ✅ All structured frontmatter slides now populate correctly

### 🚧 PENDING IMPLEMENTATION
- **Part B(MCP Discovery Tools)**: ❌ NOT STARTED
  - ❌ `describe_template()` MCP tool
  - ❌ `get_layout_help()` MCP tool  
  - ❌ `suggest_layout()` MCP tool
  - ❌ `validate_slide_data()` MCP tool
  - ❌ `list_available_templates()` MCP tool
  - ❌ `get_template_schema()` MCP tool

- **Part C (Auto-Documentation)**: ❌ NOT STARTED
  - ❌ Enhanced template analyzer with semantic analysis
  - ❌ Smart example generation
  - ❌ Auto-generated template guides
  - ❌ Usage pattern inference

---

## Overview

This specification defines an enhanced template analysis and discovery system that makes PowerPoint templates self-documenting for both human users and LLMs. The system combines semantic analysis of template structure with intelligent example generation to provide automatic documentation, structured frontmatter support, and programmatic discovery capabilities.

## Goals

1. **Zero Learning Curve**: Templates automatically document themselves with complete working examples
2. **LLM-Friendly Discovery**: Programmatic tools for AI systems to understand and use templates
3. **Human-Friendly Authoring**: Clean, structured frontmatter syntax for complex layouts
4. **Future-Proof**: New templates automatically gain documentation and discovery capabilities
5. **Maintain Compatibility**: Preserve existing JSON API while adding new capabilities

## Architecture Overview

### Three-Pronged Approach

**Option B: Template Introspection API** (MCP Tools)
- Programmatic discovery of available templates and layouts
- Validation and help systems for LLM integration
- Schema generation and field documentation

**Option C: Structured Frontmatter System** ✅ IMPLEMENTED
- Clean YAML syntax for complex layouts
- Automatic conversion to PowerPoint placeholder mappings
- Human-readable authoring experience

**Option D: Auto-Documentation System**
- Semantic analysis of PowerPoint templates
- Intelligent example generation
- Self-documenting template guides

## Option C: Structured Frontmatter System ✅ IMPLEMENTED

### Current Implementation

The structured frontmatter system provides clean, human-readable YAML structures that abstract away PowerPoint placeholder names while maintaining full functionality.

#### Key Components

1. **`StructuredFrontmatterRegistry`** (`src/structured_frontmatter.py`)
   - Defines supported layouts and their YAML structures
   - Contains mapping rules between YAML fields and PowerPoint placeholders
   - Currently supports: Four Columns, Two Content, Comparison, Picture with Caption

2. **`StructuredFrontmatterConverter`** (`src/structured_frontmatter.py`)
   - Converts structured YAML to placeholder mappings
   - Template-aware using actual PPTX placeholder names
   - Handles dynamic mapping generation

3. **`StructuredFrontmatterValidator`** (`src/structured_frontmatter.py`)
   - Validates structured frontmatter syntax and content
   - Provides warnings and error messages
   - Ensures data integrity before conversion

#### Working Examples

**Four Columns Layout:**
```yaml
---
layout: Four Columns
title: Feature Comparison Matrix
columns:
  - title: Performance
    content: "Fast processing with optimized algorithms"
  - title: Security
    content: "Enterprise-grade encryption with SOC2 compliance"
  - title: Usability
    content: "Intuitive interface with minimal learning curve"
  - title: Cost
    content: "Transparent pricing with flexible plans"
---
```

**Comparison Layout:**
```yaml
---
layout: Comparison
title: Traditional vs Modern Approach
comparison:
  left:
    title: Traditional Method
    content: "Proven track record with established processes"
  right:
    title: Modern Solution
    content: "Cloud-native architecture with automated workflows"
---
```

**Two Content Layout:**
```yaml
---
layout: Two Content
title: Two Content Layout Test
sections:
  - title: Left Side Content
    content:
      - "**Feature A** details"
      - "*Feature B* information"
  - title: Right Side Content
    content:
      - "***Important*** updates"
      - "**Security** measures"
---
```

#### Integration Points

- ✅ Integrated with `parse_markdown_with_frontmatter()` in `deckbuilder.py`
- ✅ Template mapping automatically loaded via `_ensure_layout_mapping()`
- ✅ Works with existing semantic detection system
- ✅ Supports inline formatting (bold, italic, underline)
- ✅ Backwards compatible with regular frontmatter

## Option B: Template Introspection API ❌ PENDING

### Planned MCP Tools

#### Core Discovery Tools
```python
@server.tool()
def describe_template(template_name: str = "default") -> dict:
    """Get complete template documentation with examples and usage guidance"""
    
@server.tool()
def get_layout_help(layout_name: str, template_name: str = "default") -> dict:
    """Get specific help and examples for a layout"""
    
@server.tool()
def suggest_layout(content_description: str, template_name: str = "default") -> list:
    """Suggest best layouts based on content description"""
```

#### Validation & Schema Tools
```python
@server.tool()
def validate_slide_data(slide_data: dict, layout_name: str = None, template_name: str = "default") -> dict:
    """Validate slide data against layout requirements"""
    
@server.tool()
def get_template_schema(template_name: str = "default") -> dict:
    """Get complete programmatic schema for template usage"""
    
@server.tool()
def list_available_templates() -> dict:
    """Get all templates available in the system"""
```

### Planned Integration with Structured Frontmatter

The MCP tools will provide:
1. **Discovery** → LLM learns about structured frontmatter layouts
2. **Examples** → Clean YAML examples for each layout
3. **Validation** → Verify structured frontmatter before processing
4. **Help** → Field-specific guidance and tips

## Option D: Auto-Documentation System ❌ PENDING

### Planned Features

#### Enhanced Template Analysis
- Semantic analysis of PowerPoint layouts
- Purpose inference (comparison, content, media, etc.)
- Complexity assessment and usage recommendations
- Spatial layout analysis

#### Smart Example Generation
- Context-aware content generation
- Realistic scenario creation
- Multiple format examples (JSON, frontmatter, structured)
- Best practice demonstrations

#### Auto-Generated Documentation
- Template-specific usage guides
- Layout comparison matrices
- Integration examples
- Troubleshooting guides

## Current File Structure

```
src/
├── deckbuilder.py (✅ enhanced with structured frontmatter)
├── structured_frontmatter.py (✅ complete implementation)
├── placeholder_types.py (✅ existing semantic detection)
├── tools.py (✅ existing template analyzer)
└── main.py (✅ MCP server entry point)

docs/Features/
├── PlaceholderMatching.md (✅ existing)
├── TemplateDiscovery.md (✅ this file)
└── generated/ (❌ planned for auto-docs)

tests/
├── test_presentation.md (✅ uses structured frontmatter)
├── test_structured_frontmatter.md (✅ additional examples)
└── test_presentation.json (✅ expected output)
```

## Implementation Roadmap

### Phase 1: Option B - MCP Discovery Tools (1-2 weeks)
1. Implement core MCP tools for template discovery
2. Add validation and schema generation
3. Create help and suggestion systems
4. Test with LLM clients

### Phase 2: Option D - Auto-Documentation (1-2 weeks)
1. Enhance template analyzer with semantic analysis
2. Implement smart example generation
3. Create auto-documentation generators
4. Generate template-specific guides

### Phase 3: Integration & Polish (1 week)
1. Connect all three systems (B+C+D)
2. Comprehensive error handling and fallbacks
3. End-to-end testing with real presentations
4. Performance optimization and documentation

## Success Criteria

1. ✅ **Structured Frontmatter Working**: Clean YAML syntax converts correctly to PowerPoint content
2. ❌ **LLM Self-Discovery**: An LLM can discover templates and layouts without prior knowledge
3. ❌ **Auto-Documentation**: Templates generate their own complete usage guides
4. ✅ **Backward Compatibility**: Existing JSON API continues to work unchanged
5. ❌ **Zero Configuration**: New templates automatically gain discovery capabilities

## Technical Notes

### Current Implementation Strengths
- ✅ Robust template mapping system with fallbacks
- ✅ Clean separation of concerns (registry, converter, validator)
- ✅ Template-aware mapping using actual PowerPoint placeholder names
- ✅ Comprehensive error handling and validation
- ✅ Seamless integration with existing semantic detection

### Known Limitations
- ❌ Only supports four layout types currently (can be extended)
- ❌ No bidirectional conversion (structured → YAML) - not needed for current use case
- ❌ Limited to predefined structure patterns (by design for safety)
- ❌ No programmatic discovery tools yet

### Extension Points
- **New Layout Support**: Add entries to `StructuredFrontmatterRegistry.STRUCTURE_DEFINITIONS`
- **Custom Structures**: Extend registry with new `structure_type` patterns
- **Advanced Validation**: Enhance `StructuredFrontmatterValidator` with layout-specific rules
- **Template Integration**: Connect with auto-documentation system when implemented

This specification serves as both documentation and implementation guide for the complete template discovery system, with clear status tracking and next steps.