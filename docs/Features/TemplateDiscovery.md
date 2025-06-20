# Template Discovery & Self-Documentation System

## Overview

This specification defines an enhanced template analysis and discovery system that makes PowerPoint templates self-documenting for both human users and LLMs. The system combines semantic analysis of template structure with intelligent example generation to provide automatic documentation, structured frontmatter support, and programmatic discovery capabilities.

## Goals

1. **Zero Learning Curve**: Templates automatically document themselves with complete working examples
2. **LLM-Friendly Discovery**: Programmatic tools for AI systems to understand and use templates
3. **Human-Friendly Authoring**: Clean, structured frontmatter syntax for complex layouts
4. **Future-Proof**: New templates automatically gain documentation and discovery capabilities
5. **Maintain Compatibility**: Preserve existing JSON API while adding new capabilities

## Architecture

### Core Components

1. **Enhanced Template Analyzer** (`tools.py`): Extended semantic analysis of PowerPoint templates
2. **Template Discovery API** (new MCP tools): Programmatic template introspection
3. **Structured Frontmatter Parser** (`deckbuilder.py`): Support for nested YAML structures
4. **Smart Example Generator**: Context-aware example content generation
5. **Documentation Generator**: Auto-generated template guides and usage examples

## Enhanced Template Analysis

### Current State
The existing `TemplateAnalyzer` extracts basic placeholder mappings:
```json
{
  "layouts": {
    "Four Columns": {
      "index": 11,
      "placeholders": {
        "0": "Title 1",
        "13": "Col 1 Title Placeholder 2",
        "14": "Col 1 Text Placeholder 3"
      }
    }
  }
}
```

### Enhanced Analysis Output
The enhanced analyzer will produce comprehensive template documentation:

```json
{
  "template_info": {
    "name": "Default",
    "version": "1.0",
    "analysis_version": "2.0"
  },
  "layouts": {
    "Four Columns": {
      "index": 11,
      "placeholders": {
        "0": "Title 1",
        "13": "Col 1 Title Placeholder 2",
        "14": "Col 1 Text Placeholder 3",
        "15": "Col 2 Title Placeholder 4",
        "16": "Col 2 Text Placeholder 5",
        "17": "Col 3 Title Placeholder 6",
        "18": "Col 3 Text Placeholder 7",
        "19": "Col 4 Title Placeholder 8",
        "20": "Col 4 Text Placeholder 9"
      },
      "semantic_analysis": {
        "purpose": "comparison",
        "description": "Four-column comparison layout with individual titles and content areas",
        "best_for": ["feature comparisons", "specifications", "pros/cons", "quadrant analysis"],
        "complexity": "intermediate",
        "column_count": 4,
        "has_individual_titles": true,
        "spatial_layout": "grid_4x1"
      },
      "usage_examples": {
        "realistic_scenario": "Software Feature Comparison",
        "json_example": {
          "type": "Four Columns",
          "title": "Feature Comparison",
          "Col 1 Title Placeholder 2": "Performance",
          "Col 1 Text Placeholder 3": "Fast processing with optimized algorithms",
          "Col 2 Title Placeholder 4": "Security", 
          "Col 2 Text Placeholder 5": "Enterprise-grade encryption and compliance",
          "Col 3 Title Placeholder 6": "Usability",
          "Col 3 Text Placeholder 7": "Intuitive interface with minimal learning curve",
          "Col 4 Title Placeholder 8": "Cost",
          "Col 4 Text Placeholder 9": "Competitive pricing with flexible plans"
        },
        "frontmatter_structured": {
          "yaml": "---\nlayout: Four Columns\ntitle: Feature Comparison\ncolumns:\n  - title: Performance\n    content: Fast processing with optimized algorithms\n  - title: Security\n    content: Enterprise-grade encryption and compliance\n  - title: Usability\n    content: Intuitive interface with minimal learning curve\n  - title: Cost\n    content: Competitive pricing with flexible plans\n---",
          "mapping_logic": {
            "columns[0].title": "Col 1 Title Placeholder 2",
            "columns[0].content": "Col 1 Text Placeholder 3",
            "columns[1].title": "Col 2 Title Placeholder 4",
            "columns[1].content": "Col 2 Text Placeholder 5",
            "columns[2].title": "Col 3 Title Placeholder 6",
            "columns[2].content": "Col 3 Text Placeholder 7",
            "columns[3].title": "Col 4 Title Placeholder 8",
            "columns[3].content": "Col 4 Text Placeholder 9"
          }
        }
      }
    }
  }
}
```

## Implementation Plan

### Phase 1: Enhanced Template Analyzer

#### 1.1 Semantic Layout Analysis
```python
class EnhancedTemplateAnalyzer:
    def analyze_layout_semantics(self, layout):
        """Analyze layout structure to infer purpose and usage patterns"""
        return {
            "purpose": self._infer_layout_purpose(layout),
            "description": self._generate_description(layout),
            "best_for": self._suggest_use_cases(layout),
            "complexity": self._assess_complexity(layout),
            "spatial_layout": self._analyze_spatial_arrangement(layout),
            "column_count": self._count_content_columns(layout),
            "has_individual_titles": self._has_multiple_title_areas(layout)
        }
    
    def _infer_layout_purpose(self, layout):
        """Infer layout purpose from name and structure"""
        name_lower = layout.name.lower()
        content_count = self._count_content_placeholders(layout)
        
        purpose_map = {
            ("four", "column"): "comparison",
            ("two", "content"): "side_by_side", 
            ("comparison",): "comparison",
            ("title", "only"): "section_break",
            ("picture",): "media",
            ("table",): "data"
        }
        
        for keywords, purpose in purpose_map.items():
            if all(keyword in name_lower for keyword in keywords):
                return purpose
                
        return "general_content" if content_count > 0 else "title_slide"
```

#### 1.2 Smart Example Generation
```python
def generate_smart_examples(self, layout_analysis):
    """Generate contextually appropriate examples based on layout purpose"""
    
    purpose = layout_analysis["purpose"]
    
    example_generators = {
        "comparison": self._generate_comparison_examples,
        "side_by_side": self._generate_side_by_side_examples,
        "content": self._generate_content_examples,
        "title_slide": self._generate_title_examples,
        "media": self._generate_media_examples,
        "data": self._generate_table_examples
    }
    
    generator = example_generators.get(purpose, self._generate_generic_examples)
    return generator(layout_analysis)

def _generate_comparison_examples(self, layout_analysis):
    """Generate realistic comparison content"""
    columns = layout_analysis.get("column_count", 2)
    
    scenarios = {
        4: {
            "scenario": "Software Feature Comparison",
            "columns": [
                {"title": "Performance", "content": "Fast processing with optimized algorithms"},
                {"title": "Security", "content": "Enterprise-grade encryption and compliance"},
                {"title": "Usability", "content": "Intuitive interface with minimal learning curve"},
                {"title": "Cost", "content": "Competitive pricing with flexible plans"}
            ]
        },
        2: {
            "scenario": "Solution Comparison", 
            "columns": [
                {"title": "Option A", "content": "Traditional approach with proven reliability"},
                {"title": "Option B", "content": "Modern solution with advanced features"}
            ]
        }
    }
    
    return scenarios.get(columns, scenarios[2])
```

### Phase 2: MCP Discovery Tools

#### 2.1 Template Discovery API
```python
@server.tool()
def describe_template(template_name: str = "default") -> dict:
    """Get complete template documentation with examples and usage guidance"""
    
    template_path = get_template_path(template_name)
    enhanced_analysis = EnhancedTemplateAnalyzer().analyze_template_with_documentation(template_path)
    
    return {
        "template": template_name,
        "summary": {
            "total_layouts": len(enhanced_analysis["layouts"]),
            "layout_types": [layout["semantic_analysis"]["purpose"] for layout in enhanced_analysis["layouts"].values()],
            "recommended_layouts": get_recommended_layouts(enhanced_analysis)
        },
        "layouts": enhanced_analysis["layouts"],
        "usage_guide": generate_usage_guide(enhanced_analysis)
    }

@server.tool()
def get_layout_help(layout_name: str, template_name: str = "default") -> dict:
    """Get specific help and examples for a layout"""
    
    template_analysis = get_template_analysis(template_name)
    layout_info = template_analysis["layouts"].get(layout_name)
    
    if not layout_info:
        available = list(template_analysis["layouts"].keys())
        return {"error": f"Layout '{layout_name}' not found. Available: {available}"}
    
    return {
        "layout": layout_name,
        "description": layout_info["semantic_analysis"]["description"],
        "best_for": layout_info["semantic_analysis"]["best_for"],
        "complexity": layout_info["semantic_analysis"]["complexity"],
        "examples": {
            "json": layout_info["usage_examples"]["json_example"],
            "frontmatter": layout_info["usage_examples"]["frontmatter_structured"]["yaml"]
        },
        "required_fields": ["title"],
        "optional_fields": extract_optional_fields(layout_info["placeholders"]),
        "tips": generate_usage_tips(layout_info)
    }

@server.tool()
def suggest_layout(content_description: str, template_name: str = "default") -> list:
    """Suggest best layouts based on content description"""
    
    template_analysis = get_template_analysis(template_name)
    suggestions = []
    
    description_lower = content_description.lower()
    
    for layout_name, layout_info in template_analysis["layouts"].items():
        semantic = layout_info["semantic_analysis"]
        score = calculate_relevance_score(description_lower, semantic)
        
        if score > 0.3:  # Relevance threshold
            suggestions.append({
                "layout": layout_name,
                "relevance_score": score,
                "reason": generate_suggestion_reason(description_lower, semantic),
                "example": layout_info["usage_examples"]["frontmatter_structured"]["yaml"]
            })
    
    return sorted(suggestions, key=lambda x: x["relevance_score"], reverse=True)[:3]
```

### Phase 3: Structured Frontmatter Support

#### 3.1 Enhanced Frontmatter Parser
```python
def parse_structured_frontmatter(self, frontmatter_content: str, layout_info: dict) -> dict:
    """Parse structured frontmatter and convert to placeholder mappings"""
    
    try:
        parsed = yaml.safe_load(frontmatter_content)
    except yaml.YAMLError:
        return self._parse_frontmatter_safe(frontmatter_content)
    
    layout_name = parsed.get("layout")
    if not layout_name or layout_name not in self.layout_mapping["layouts"]:
        return parsed
    
    # Check if this layout has structured frontmatter support
    layout_data = self.layout_mapping["layouts"][layout_name]
    if "frontmatter_support" not in layout_data.get("usage_examples", {}):
        return parsed
    
    # Convert structured format to placeholder mappings
    mapping_logic = layout_data["usage_examples"]["frontmatter_structured"]["mapping_logic"]
    return self._convert_structured_to_placeholders(parsed, mapping_logic)

def _convert_structured_to_placeholders(self, structured_data: dict, mapping_logic: dict) -> dict:
    """Convert structured frontmatter to placeholder field names"""
    
    result = {"type": structured_data.get("layout", "content")}
    
    # Handle direct mappings (title, subtitle, etc.)
    for key, value in structured_data.items():
        if key not in ["layout", "columns", "sections", "comparison"]:
            result[key] = value
    
    # Handle structured mappings
    if "columns" in structured_data:
        for i, column in enumerate(structured_data["columns"]):
            for field, content in column.items():
                mapping_key = f"columns[{i}].{field}"
                if mapping_key in mapping_logic:
                    placeholder_name = mapping_logic[mapping_key]
                    result[placeholder_name] = content
    
    # Handle comparison structures
    if "comparison" in structured_data:
        comp = structured_data["comparison"]
        for side in ["left", "right"]:
            if side in comp:
                for field, content in comp[side].items():
                    mapping_key = f"comparison.{side}.{field}"
                    if mapping_key in mapping_logic:
                        placeholder_name = mapping_logic[mapping_key]
                        result[placeholder_name] = content
    
    return result
```

#### 3.2 Structured Frontmatter Examples

**Four Columns Layout**:
```yaml
---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: Fast processing with optimized algorithms
  - title: Security
    content: Enterprise-grade encryption and compliance
  - title: Usability
    content: Intuitive interface with minimal learning curve
  - title: Cost
    content: Competitive pricing with flexible plans
---
```

**Comparison Layout**:
```yaml
---
layout: Comparison
title: Solution Analysis
comparison:
  left:
    title: Traditional Approach
    content: Proven reliability with established workflows
  right:
    title: Modern Solution
    content: Advanced features with improved efficiency
---
```

**Two Content Layout**:
```yaml
---
layout: Two Content
title: Before and After
sections:
  - title: Current State
    content:
      - Manual processes
      - Time-consuming workflows
      - Limited scalability
  - title: Future State
    content:
      - Automated systems
      - Streamlined operations
      - Unlimited growth potential
---
```

### Phase 4: Documentation Generation

#### 4.1 Auto-Generated Template Guide
```python
def generate_template_guide(template_analysis: dict) -> str:
    """Generate complete markdown guide for template usage"""
    
    guide = f"""# {template_analysis['template_info']['name']} Template Guide

## Overview
This template provides {len(template_analysis['layouts'])} different layout options for various presentation needs.

## Quick Start
For basic slides, use semantic field names that work with any layout:
- `title`: Main slide title
- `subtitle`: Subtitle (for title slides)
- `content`: Main content area

## Available Layouts

"""
    
    for layout_name, layout_info in template_analysis["layouts"].items():
        semantic = layout_info["semantic_analysis"]
        example = layout_info["usage_examples"]
        
        guide += f"""### {layout_name}
**Purpose**: {semantic["description"]}
**Best for**: {", ".join(semantic["best_for"])}
**Complexity**: {semantic["complexity"]}

**JSON Example**:
```json
{json.dumps(example["json_example"], indent=2)}
```

**Frontmatter Example**:
```yaml
{example["frontmatter_structured"]["yaml"]}
```

---

"""
    
    return guide
```

## File Structure Changes

```
docs/
├── Features/
│   ├── PlaceholderMatching.md (existing)
│   ├── TemplateDiscovery.md (this specification)
│   └── generated/
│       ├── DefaultTemplateGuide.md (auto-generated)
│       └── CorporateTemplateGuide.md (auto-generated)
src/
├── template_discovery.py (new)
├── enhanced_analyzer.py (new)
└── tools.py (enhanced)
```

## Migration Strategy

### Phase 1: Enhanced Analysis (Week 1)
- Extend `TemplateAnalyzer` with semantic analysis
- Generate enhanced template mappings
- Maintain backward compatibility

### Phase 2: MCP Discovery Tools (Week 2)
- Add template discovery MCP tools
- Implement layout suggestion system
- Create usage guide generation

### Phase 3: Structured Frontmatter (Week 3)
- Add structured frontmatter parsing
- Implement conversion logic
- Update markdown processing pipeline

### Phase 4: Documentation & Polish (Week 4)
- Auto-generate template guides
- Add comprehensive examples
- Create troubleshooting documentation

## Success Criteria

1. **LLM Integration**: An LLM can discover templates, understand layouts, and generate appropriate content without prior knowledge
2. **Human Usability**: Users can author complex layouts using clean, readable frontmatter
3. **Self-Documentation**: Templates automatically provide complete usage examples and documentation
4. **Backward Compatibility**: Existing JSON API continues to work unchanged
5. **Extensibility**: New templates automatically gain discovery and documentation capabilities

## Open Questions

1. Should we support custom structured frontmatter patterns beyond the built-in ones?
2. How do we handle edge cases where semantic analysis can't determine layout purpose?
3. Should example generation be customizable per template or use universal patterns?
4. How do we handle templates with unusual or complex placeholder arrangements?

## Next Steps

1. Create detailed implementation tickets for each phase
2. Design comprehensive test cases for semantic analysis
3. Create sample enhanced template mappings
4. Define MCP tool schemas and error handling
5. Plan integration testing with LLM clients