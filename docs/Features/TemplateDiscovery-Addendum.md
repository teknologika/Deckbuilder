# Template Discovery System - Addendum: Complete B+C Implementation

## Overview

This addendum extends the Template Discovery specification to include complete implementations of **Option B** (Template Introspection API) and **Option C** (Structured Frontmatter System). The main specification focused heavily on Option D (Auto-Discovery), but the full combo approach (B+C+D) requires these additional components.

## Option B: Complete Template Introspection API

### Core Philosophy
Provide comprehensive programmatic access to template capabilities, allowing LLMs and other systems to:
1. Discover what's available
2. Understand how to use it
3. Validate their attempts
4. Get specific help when needed

### Additional MCP Tools

#### B.1 System-Level Discovery
```python
@server.tool()
def list_available_templates() -> dict:
    """Get all templates available in the system"""
    template_folder = os.getenv('DECK_TEMPLATE_FOLDER', 'templates')
    
    templates = []
    for file in os.listdir(template_folder):
        if file.endswith('.pptx'):
            template_name = file[:-5]  # Remove .pptx
            json_file = os.path.join(template_folder, f"{template_name}.json")
            
            templates.append({
                "name": template_name,
                "has_mapping": os.path.exists(json_file),
                "file_path": os.path.join(template_folder, file),
                "last_modified": os.path.getmtime(os.path.join(template_folder, file))
            })
    
    return {
        "templates": templates,
        "template_folder": template_folder,
        "default_template": "default"
    }

@server.tool()
def get_system_capabilities() -> dict:
    """Get overall system capabilities and configuration"""
    return {
        "supported_formats": ["json", "markdown_frontmatter", "structured_frontmatter"],
        "semantic_fields": ["title", "subtitle", "content"],
        "template_folder": os.getenv('DECK_TEMPLATE_FOLDER'),
        "output_folder": os.getenv('DECK_OUTPUT_FOLDER'),
        "version": "2.0",
        "features": {
            "semantic_detection": True,
            "json_mapping": True,
            "structured_frontmatter": True,
            "auto_documentation": True,
            "inline_formatting": True,
            "rich_content": True,
            "table_support": True
        }
    }
```

#### B.2 Template Schema and Structure
```python
@server.tool()
def get_template_schema(template_name: str = "default") -> dict:
    """Get complete programmatic schema for template usage"""
    
    template_analysis = get_enhanced_template_analysis(template_name)
    
    schema = {
        "template": template_name,
        "version": "2.0",
        "layouts": {}
    }
    
    for layout_name, layout_info in template_analysis["layouts"].items():
        layout_schema = {
            "name": layout_name,
            "index": layout_info["index"],
            "purpose": layout_info["semantic_analysis"]["purpose"],
            "complexity": layout_info["semantic_analysis"]["complexity"],
            
            # Field definitions
            "fields": {
                "required": ["title"] if layout_info["semantic_analysis"]["purpose"] != "title_slide" else [],
                "optional": [],
                "semantic": ["title", "subtitle", "content"],  # Always use semantic detection
                "mapped": []  # Use JSON mapping
            },
            
            # Data types and validation
            "field_types": {
                "title": {"type": "string", "max_length": 100},
                "subtitle": {"type": "string", "max_length": 150},
                "content": {"type": ["string", "array"], "supports_formatting": True}
            },
            
            # Structured frontmatter support
            "structured_frontmatter": {
                "supported": layout_info.get("frontmatter_support", {}).get("supported", False),
                "structure": layout_info.get("frontmatter_support", {}).get("structure"),
                "example": layout_info.get("usage_examples", {}).get("frontmatter_structured", {}).get("yaml")
            }
        }
        
        # Extract mapped fields from placeholders
        for placeholder_idx, placeholder_name in layout_info["placeholders"].items():
            if placeholder_name not in ["title", "subtitle", "content"]:
                layout_schema["fields"]["mapped"].append(placeholder_name)
                layout_schema["field_types"][placeholder_name] = {
                    "type": "string",
                    "placeholder_index": int(placeholder_idx),
                    "supports_formatting": True
                }
        
        schema["layouts"][layout_name] = layout_schema
    
    return schema

@server.tool()
def get_layout_structure(layout_name: str, template_name: str = "default") -> dict:
    """Get detailed structure information for a specific layout"""
    
    schema = get_template_schema(template_name)
    layout_schema = schema["layouts"].get(layout_name)
    
    if not layout_schema:
        available = list(schema["layouts"].keys())
        return {"error": f"Layout '{layout_name}' not found. Available: {available}"}
    
    return {
        "layout": layout_name,
        "template": template_name,
        "structure": layout_schema,
        "usage_patterns": {
            "json_format": generate_json_template(layout_schema),
            "frontmatter_format": generate_frontmatter_template(layout_schema),
            "structured_format": layout_schema["structured_frontmatter"]["example"] if layout_schema["structured_frontmatter"]["supported"] else None
        },
        "validation_rules": extract_validation_rules(layout_schema)
    }
```

#### B.3 Validation and Help System
```python
@server.tool()
def validate_slide_data(slide_data: dict, layout_name: str = None, template_name: str = "default") -> dict:
    """Validate slide data against layout requirements"""
    
    # Auto-detect layout if not provided
    if not layout_name:
        layout_name = slide_data.get("type", "Title and Content")
    
    schema = get_template_schema(template_name)
    layout_schema = schema["layouts"].get(layout_name)
    
    if not layout_schema:
        return {
            "valid": False,
            "errors": [f"Unknown layout: {layout_name}"],
            "suggestions": list(schema["layouts"].keys())
        }
    
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    # Check required fields
    for required_field in layout_schema["fields"]["required"]:
        if required_field not in slide_data:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Missing required field: '{required_field}'")
    
    # Check field types and constraints
    for field_name, field_value in slide_data.items():
        if field_name in ["type"]:
            continue
            
        field_def = layout_schema["field_types"].get(field_name)
        if not field_def:
            validation_result["warnings"].append(f"Unknown field '{field_name}' for layout '{layout_name}'")
            continue
            
        # Type validation
        expected_type = field_def["type"]
        if isinstance(expected_type, list):
            if not any(isinstance(field_value, t) for t in [str if t == "string" else t for t in expected_type]):
                validation_result["errors"].append(f"Field '{field_name}' should be one of: {expected_type}")
        elif expected_type == "string" and not isinstance(field_value, str):
            validation_result["errors"].append(f"Field '{field_name}' should be a string")
        elif expected_type == "array" and not isinstance(field_value, list):
            validation_result["errors"].append(f"Field '{field_name}' should be an array")
    
    # Provide suggestions for improvement
    if slide_data.get("type") != layout_name:
        validation_result["suggestions"].append(f"Consider setting 'type': '{layout_name}' for clarity")
    
    validation_result["valid"] = len(validation_result["errors"]) == 0
    return validation_result

@server.tool()
def get_field_help(field_name: str, layout_name: str = None, template_name: str = "default") -> dict:
    """Get specific help for a field in a layout"""
    
    schema = get_template_schema(template_name)
    
    # If no layout specified, search across all layouts
    if not layout_name:
        matches = []
        for layout, layout_schema in schema["layouts"].items():
            if field_name in layout_schema["field_types"]:
                matches.append({
                    "layout": layout,
                    "field_info": layout_schema["field_types"][field_name],
                    "usage": get_field_usage_example(field_name, layout, template_name)
                })
        
        return {
            "field": field_name,
            "found_in_layouts": matches,
            "semantic_field": field_name in ["title", "subtitle", "content"]
        }
    
    # Specific layout help
    layout_schema = schema["layouts"].get(layout_name)
    if not layout_schema:
        return {"error": f"Layout '{layout_name}' not found"}
    
    field_info = layout_schema["field_types"].get(field_name)
    if not field_info:
        available_fields = list(layout_schema["field_types"].keys())
        return {
            "error": f"Field '{field_name}' not available in layout '{layout_name}'",
            "available_fields": available_fields
        }
    
    return {
        "field": field_name,
        "layout": layout_name,
        "definition": field_info,
        "usage": get_field_usage_example(field_name, layout_name, template_name),
        "tips": generate_field_tips(field_name, field_info)
    }

@server.tool()
def suggest_improvements(slide_data: dict, template_name: str = "default") -> dict:
    """Analyze slide data and suggest improvements"""
    
    layout_name = slide_data.get("type", "Title and Content")
    validation = validate_slide_data(slide_data, layout_name, template_name)
    
    suggestions = {
        "validation_issues": validation["errors"] + validation["warnings"],
        "content_improvements": [],
        "layout_suggestions": [],
        "formatting_tips": []
    }
    
    # Content analysis
    if "title" in slide_data:
        title_length = len(slide_data["title"])
        if title_length > 60:
            suggestions["content_improvements"].append("Consider shortening the title for better readability")
        elif title_length < 5:
            suggestions["content_improvements"].append("Consider a more descriptive title")
    
    # Layout suggestions
    content_fields = [k for k in slide_data.keys() if k not in ["type", "title", "subtitle"]]
    if len(content_fields) > 3:
        suggestions["layout_suggestions"].append("Consider using a multi-column layout for better organization")
    
    # Formatting tips
    for field_name, field_value in slide_data.items():
        if isinstance(field_value, str) and any(marker in field_value for marker in ["**", "*", "___"]):
            suggestions["formatting_tips"].append(f"Field '{field_name}' uses inline formatting - ensure it renders correctly")
    
    return suggestions
```

## Option C: Complete Structured Frontmatter System

### Core Philosophy
Provide clean, human-readable YAML structures that abstract away the ugly PowerPoint placeholder names while maintaining full functionality.

### C.1 Comprehensive Structure Definitions

#### Structure Mapping Registry
```python
class StructuredFrontmatterRegistry:
    """Registry of structured frontmatter patterns for different layout types"""
    
    STRUCTURE_DEFINITIONS = {
        "Four Columns": {
            "structure_type": "columns",
            "yaml_pattern": {
                "layout": "Four Columns",
                "title": str,
                "columns": [
                    {"title": str, "content": str}
                ]
            },
            "mapping_rules": {
                "title": "semantic:title",
                "columns[{i}].title": "Col {i+1} Title Placeholder {2+i*2}",
                "columns[{i}].content": "Col {i+1} Text Placeholder {3+i*2}"
            },
            "validation": {
                "min_columns": 1,
                "max_columns": 4,
                "required_fields": ["title"]
            }
        },
        
        "Comparison": {
            "structure_type": "comparison",
            "yaml_pattern": {
                "layout": "Comparison",
                "title": str,
                "comparison": {
                    "left": {"title": str, "content": str},
                    "right": {"title": str, "content": str}
                }
            },
            "mapping_rules": {
                "title": "semantic:title",
                "comparison.left.title": "Text Placeholder 2",
                "comparison.left.content": "Content Placeholder 3",
                "comparison.right.title": "Text Placeholder 4", 
                "comparison.right.content": "Content Placeholder 5"
            }
        },
        
        "Two Content": {
            "structure_type": "sections",
            "yaml_pattern": {
                "layout": "Two Content",
                "title": str,
                "sections": [
                    {"title": str, "content": [str]}
                ]
            },
            "mapping_rules": {
                "title": "semantic:title",
                "sections[0].content": "Content Placeholder 2",
                "sections[1].content": "Content Placeholder 3"
            }
        },
        
        "Picture with Caption": {
            "structure_type": "media",
            "yaml_pattern": {
                "layout": "Picture with Caption",
                "title": str,
                "media": {
                    "type": "picture",
                    "caption": str,
                    "description": str
                }
            },
            "mapping_rules": {
                "title": "semantic:title",
                "media.caption": "Text Placeholder 3",
                "media.description": "semantic:content"
            }
        }
    }
    
    @classmethod
    def get_structure_definition(cls, layout_name: str) -> dict:
        """Get structure definition for a layout"""
        return cls.STRUCTURE_DEFINITIONS.get(layout_name, {})
    
    @classmethod
    def supports_structured_frontmatter(cls, layout_name: str) -> bool:
        """Check if layout supports structured frontmatter"""
        return layout_name in cls.STRUCTURE_DEFINITIONS
```

#### C.2 Bidirectional Conversion System
```python
class StructuredFrontmatterConverter:
    """Convert between structured frontmatter and placeholder mappings"""
    
    def __init__(self, layout_mapping: dict):
        self.layout_mapping = layout_mapping
        self.registry = StructuredFrontmatterRegistry()
    
    def convert_structured_to_placeholders(self, structured_data: dict) -> dict:
        """Convert structured frontmatter to placeholder field names"""
        
        layout_name = structured_data.get("layout")
        if not layout_name:
            return structured_data
            
        structure_def = self.registry.get_structure_definition(layout_name)
        if not structure_def:
            # Fallback to regular frontmatter parsing
            return structured_data
        
        result = {"type": layout_name}
        mapping_rules = structure_def["mapping_rules"]
        
        # Process each mapping rule
        for structured_path, placeholder_target in mapping_rules.items():
            value = self._extract_value_by_path(structured_data, structured_path)
            if value is not None:
                if placeholder_target.startswith("semantic:"):
                    # Use semantic field name directly
                    semantic_field = placeholder_target.split(":", 1)[1]
                    result[semantic_field] = value
                else:
                    # Use exact placeholder name
                    result[placeholder_target] = value
        
        return result
    
    def convert_placeholders_to_structured(self, slide_data: dict) -> dict:
        """Convert placeholder mappings back to structured frontmatter"""
        
        layout_name = slide_data.get("type")
        if not layout_name:
            return slide_data
            
        structure_def = self.registry.get_structure_definition(layout_name)
        if not structure_def:
            return slide_data
        
        # Start with the base structure
        result = {"layout": layout_name}
        
        # Reverse the mapping rules
        for structured_path, placeholder_target in structure_def["mapping_rules"].items():
            if placeholder_target.startswith("semantic:"):
                semantic_field = placeholder_target.split(":", 1)[1]
                if semantic_field in slide_data:
                    self._set_value_by_path(result, structured_path, slide_data[semantic_field])
            else:
                if placeholder_target in slide_data:
                    self._set_value_by_path(result, structured_path, slide_data[placeholder_target])
        
        return result
    
    def _extract_value_by_path(self, data: dict, path: str):
        """Extract value from nested dict using dot notation path"""
        
        # Handle array indexing like "columns[0].title"
        if "[" in path and "]" in path:
            return self._extract_array_value(data, path)
        
        # Handle simple dot notation like "comparison.left.title"
        keys = path.split(".")
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _extract_array_value(self, data: dict, path: str):
        """Extract value from array using path like 'columns[0].title'"""
        
        # Parse "columns[0].title" into ["columns", 0, "title"]
        parts = []
        current_part = ""
        i = 0
        
        while i < len(path):
            if path[i] == "[":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                # Find the closing bracket
                j = i + 1
                while j < len(path) and path[j] != "]":
                    j += 1
                index = int(path[i+1:j])
                parts.append(index)
                i = j + 1
                if i < len(path) and path[i] == ".":
                    i += 1
            elif path[i] == ".":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                i += 1
            else:
                current_part += path[i]
                i += 1
        
        if current_part:
            parts.append(current_part)
        
        # Navigate through the data structure
        current = data
        for part in parts:
            if isinstance(part, int):
                if isinstance(current, list) and len(current) > part:
                    current = current[part]
                else:
                    return None
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current
    
    def _set_value_by_path(self, data: dict, path: str, value):
        """Set value in nested dict using dot notation path"""
        
        if "[" in path and "]" in path:
            self._set_array_value(data, path, value)
            return
        
        keys = path.split(".")
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _set_array_value(self, data: dict, path: str, value):
        """Set value in array structure"""
        # Implementation similar to _extract_array_value but for setting
        # This would handle creating the array structure as needed
        pass
```

#### C.3 Enhanced Frontmatter Processing
```python
def parse_structured_frontmatter_enhanced(self, frontmatter_content: str, layout_info: dict) -> dict:
    """Enhanced frontmatter parsing with full structured support"""
    
    try:
        parsed = yaml.safe_load(frontmatter_content)
    except yaml.YAMLError as e:
        # Fallback to safe parsing for special characters
        return self._parse_frontmatter_safe(frontmatter_content)
    
    layout_name = parsed.get("layout")
    if not layout_name:
        return parsed
    
    # Check if this is structured frontmatter
    converter = StructuredFrontmatterConverter(self.layout_mapping)
    if converter.registry.supports_structured_frontmatter(layout_name):
        
        # Validate structured frontmatter
        validation_result = self._validate_structured_frontmatter(parsed, layout_name)
        if not validation_result["valid"]:
            # Log warnings but continue processing
            for warning in validation_result["warnings"]:
                print(f"Warning: {warning}")
        
        # Convert to placeholder mappings
        return converter.convert_structured_to_placeholders(parsed)
    
    # Regular frontmatter processing
    return parsed

def _validate_structured_frontmatter(self, data: dict, layout_name: str) -> dict:
    """Validate structured frontmatter against layout requirements"""
    
    structure_def = StructuredFrontmatterRegistry.get_structure_definition(layout_name)
    validation = structure_def.get("validation", {})
    
    result = {"valid": True, "warnings": [], "errors": []}
    
    # Check required fields
    required_fields = validation.get("required_fields", [])
    for field in required_fields:
        if field not in data:
            result["valid"] = False
            result["errors"].append(f"Missing required field: {field}")
    
    # Layout-specific validation
    if layout_name == "Four Columns" and "columns" in data:
        columns = data["columns"]
        min_cols = validation.get("min_columns", 1)
        max_cols = validation.get("max_columns", 4)
        
        if len(columns) < min_cols:
            result["warnings"].append(f"Expected at least {min_cols} columns, got {len(columns)}")
        elif len(columns) > max_cols:
            result["warnings"].append(f"Expected at most {max_cols} columns, got {len(columns)}")
    
    return result
```

### C.4 Complete Structure Examples

#### Four Columns with Validation
```yaml
---
layout: Four Columns
title: Comprehensive Feature Analysis
columns:
  - title: Performance
    content: |
      • Fast processing speeds
      • Optimized algorithms
      • Minimal resource usage
  - title: Security
    content: |
      • End-to-end encryption
      • Compliance certifications
      • Regular security audits
  - title: Usability
    content: |
      • Intuitive interface
      • Minimal learning curve
      • Comprehensive documentation
  - title: Cost
    content: |
      • Competitive pricing
      • Flexible payment plans
      • Transparent billing
---
```

#### Comparison Layout with Rich Content
```yaml
---
layout: Comparison
title: Solution Analysis
comparison:
  left:
    title: Traditional Approach
    content: |
      **Advantages:**
      • Proven reliability
      • Well-established workflows
      • Lower implementation risk
      
      **Disadvantages:**
      • Limited scalability
      • Higher maintenance costs
  right:
    title: Modern Solution
    content: |
      **Advantages:**
      • Advanced automation
      • Cloud-native architecture
      • Future-proof technology
      
      **Disadvantages:**
      • Learning curve required
      • Initial setup complexity
---
```

#### Media Layout with Structured Metadata
```yaml
---
layout: Picture with Caption
title: System Architecture Overview
media:
  type: picture
  caption: High-level system architecture diagram
  description: |
    This diagram shows the main components:
    • **Frontend**: React-based user interface
    • **API Layer**: RESTful services with authentication
    • **Database**: PostgreSQL with Redis caching
    • **Infrastructure**: Kubernetes deployment on AWS
---
```

## Integration Points

### How B+C+D Work Together

1. **Discovery (B)** → LLM calls `describe_template()` to understand available layouts
2. **Structure Help (B+C)** → LLM calls `get_layout_structure()` to get structured frontmatter examples
3. **Content Creation (C)** → LLM writes clean structured frontmatter
4. **Validation (B)** → System validates using `validate_slide_data()` before processing
5. **Auto-Documentation (D)** → System provides examples and suggestions throughout

### Error Handling and Fallbacks

1. **Structured Parsing Fails** → Fall back to regular frontmatter
2. **Layout Not Found** → Suggest similar layouts via semantic matching
3. **Field Validation Fails** → Provide specific error messages and correction suggestions
4. **Template Not Available** → Auto-generate basic structure from PowerPoint analysis

## Implementation Priority

### Phase 1: Core B Implementation
- Add comprehensive MCP tools for discovery and validation
- Implement schema generation from template analysis

### Phase 2: Structured Frontmatter (C)
- Build registry of structure definitions
- Implement bidirectional conversion system
- Add validation for structured formats

### Phase 3: Integration & Polish
- Connect B+C+D systems
- Add comprehensive error handling
- Create end-to-end testing

This addendum ensures we have the complete B+C+D combo system with full programmatic discovery (B), clean structured frontmatter (C), and intelligent auto-documentation (D) all working together.