# Template Management System

## Overview

The Template Management System provides automated tools for analyzing, enhancing, and documenting PowerPoint templates without requiring manual PowerPoint editing. This system eliminates the complex workflow of manually updating placeholder names and maintaining template documentation.

### Current Limitations

- **Manual PowerPoint editing required**: Users must manually rename placeholders in PowerPoint
- **Inconsistent naming**: No standardized placeholder naming conventions
- **Outdated documentation**: Manual documentation gets out of sync with templates
- **Complex workflow**: Multiple manual steps to add new templates
- **Limited structured frontmatter support**: Only 6 of 19 layouts supported

### Proposed Solution

Automated template management through MCP tools that can:
- Extract template structure automatically
- Update master slide placeholder names programmatically
- Generate synchronized documentation
- Validate template consistency
- Support convention-based structured frontmatter

## Architecture

```
PowerPoint Template (.pptx)
    ↓
[analyze_template] → Raw Structure (.g.json)
    ↓
User Edits JSON Mapping
    ↓
[enhance_template] → Enhanced Template (.pptx)
    ↓
[document_template] → Documentation (.md)
    ↓
[validate_template] → Validation Report
```

## MCP Tools Specification

### 1. Template Analysis Tool

```python
async def analyze_template(ctx: Context, template_name: str, output_format: str = "json") -> str
```

**Purpose**: Extract PowerPoint template structure and generate raw placeholder mapping

**Parameters**:
- `template_name`: Name of PowerPoint template (e.g., "default", "corporate")
- `output_format`: Output format - "json" or "markdown" (default: "json")

**Implementation Details**:
```python
def analyze_template_implementation(template_name: str):
    # 1. Load PowerPoint template
    template_path = os.path.join(TEMPLATE_FOLDER, f"{template_name}.pptx")
    prs = Presentation(template_path)
    
    # 2. Extract slide layouts
    layouts = {}
    for i, layout in enumerate(prs.slide_layouts):
        layout_info = {
            "index": i,
            "name": layout.name,
            "placeholders": {}
        }
        
        # 3. Extract placeholder information
        for placeholder in layout.placeholders:
            placeholder_info = {
                "idx": placeholder.placeholder_format.idx,
                "type": placeholder.placeholder_format.type,
                "current_name": placeholder.name,
                "suggested_name": generate_semantic_name(placeholder, layout.name)
            }
            layout_info["placeholders"][str(placeholder.placeholder_format.idx)] = placeholder_info
        
        layouts[layout.name] = layout_info
    
    # 4. Generate template mapping structure
    template_mapping = {
        "template_info": {
            "name": template_name,
            "version": "1.0",
            "layouts_count": len(layouts),
            "analyzed_date": datetime.now().isoformat()
        },
        "layouts": layouts,
        "suggested_aliases": generate_layout_aliases(layouts),
        "naming_analysis": analyze_naming_patterns(layouts)
    }
    
    # 5. Save raw mapping for user editing
    output_file = f"{template_name}.g.json"
    save_json(template_mapping, output_file)
    
    return f"Template analysis complete. Generated: {output_file}"
```

**Output**: 
- Generates `{template_name}.g.json` with raw structure
- Returns analysis summary with layout count and placeholder statistics

**Error Handling**:
- Template file not found
- Corrupted PowerPoint file
- Permission issues
- Invalid template structure

### 2. Template Enhancement Tool

```python
async def enhance_template(ctx: Context, template_name: str, mapping_file: str = None, create_backup: bool = True) -> str
```

**Purpose**: Automatically update master slide placeholder names using semantic mapping

**Parameters**:
- `template_name`: Template to enhance
- `mapping_file`: Custom JSON mapping file (default: `{template_name}.json`)
- `create_backup`: Create backup before modification (default: True)

**Implementation Details**:
```python
def enhance_template_implementation(template_name: str, mapping_file: str, create_backup: bool):
    # 1. Create backup if requested
    if create_backup:
        backup_path = create_template_backup(template_name)
        print(f"Backup created: {backup_path}")
    
    # 2. Load template and mapping
    template_path = f"{template_name}.pptx"
    prs = Presentation(template_path)
    mapping = load_json_mapping(mapping_file or f"{template_name}.json")
    
    # 3. Access slide master for placeholder modification
    slide_master = prs.slide_master
    layout_masters = prs.slide_layouts
    
    # 4. Update master placeholder names
    for layout_name, layout_info in mapping["layouts"].items():
        layout_index = layout_info["index"]
        placeholder_mappings = layout_info.get("placeholders", {})
        
        # Access specific layout master
        layout_master = layout_masters[layout_index]
        
        # Update each placeholder name
        for placeholder in layout_master.placeholders:
            placeholder_idx = str(placeholder.placeholder_format.idx)
            if placeholder_idx in placeholder_mappings:
                new_name = placeholder_mappings[placeholder_idx]
                
                # Update placeholder name on master slide
                try:
                    placeholder.element.nvSpPr.cNvPr.name = new_name
                    print(f"Updated placeholder {placeholder_idx}: '{placeholder.name}' → '{new_name}'")
                except Exception as e:
                    print(f"Warning: Could not update placeholder {placeholder_idx}: {e}")
    
    # 5. Save enhanced template
    enhanced_path = f"{template_name}_enhanced.pptx"
    prs.save(enhanced_path)
    
    # 6. Validate enhancement success
    validation_result = validate_placeholder_names(enhanced_path, mapping)
    
    return f"Template enhanced successfully: {enhanced_path}\nValidation: {validation_result}"
```

**Process Flow**:
1. Create timestamped backup of original template
2. Load PowerPoint template via python-pptx
3. Load corresponding JSON mapping file
4. Access slide master and layout masters
5. Update `placeholder.name` for each mapped placeholder
6. Save enhanced template with descriptive names
7. Validate all placeholders were updated correctly

**Output**:
- Enhanced template file with semantic placeholder names
- Validation report confirming successful updates
- Backup file location (if created)

### 3. Template Documentation Generator

```python
async def document_template(ctx: Context, template_name: str, output_path: str = "./docs/Features/") -> str
```

**Purpose**: Generate comprehensive template documentation with layout analysis

**Parameters**:
- `template_name`: Template to document
- `output_path`: Output directory for documentation (default: "./docs/Features/")

**Implementation Details**:
```python
def document_template_implementation(template_name: str, output_path: str):
    # 1. Analyze template structure
    template_analysis = analyze_template_structure(template_name)
    mapping = load_template_mapping(template_name)
    structured_patterns = analyze_structured_frontmatter_support(template_name)
    
    # 2. Generate documentation sections
    doc_sections = {
        "overview": generate_template_overview(template_analysis),
        "layout_table": generate_layout_summary_table(template_analysis, structured_patterns),
        "detailed_layouts": generate_detailed_layout_docs(template_analysis, mapping),
        "structured_frontmatter": generate_structured_frontmatter_docs(structured_patterns),
        "usage_examples": generate_usage_examples(template_analysis),
        "validation_results": generate_validation_report(template_name)
    }
    
    # 3. Format as markdown
    markdown_content = f"""# {template_name.title()} Template Documentation

## Template Overview
{doc_sections["overview"]}

## Layout Summary
{doc_sections["layout_table"]}

## Detailed Layout Specifications
{doc_sections["detailed_layouts"]}

## Structured Frontmatter Support
{doc_sections["structured_frontmatter"]}

## Usage Examples
{doc_sections["usage_examples"]}

## Validation Report
{doc_sections["validation_results"]}

---
*Generated automatically by Template Management System on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    # 4. Save documentation
    output_file = os.path.join(output_path, f"{template_name}Template.md")
    save_file(output_file, markdown_content)
    
    return f"Documentation generated: {output_file}"
```

**Generated Documentation Sections**:

1. **Template Overview**
   - Template name, version, file size
   - Total layouts and placeholders
   - Generation timestamp

2. **Layout Summary Table**
   ```markdown
   | Layout Name | Index | Placeholders | Structured Support | JSON Mapping |
   |-------------|-------|--------------|-------------------|--------------|
   | Title Slide | 0 | 5 | ✅ | ✅ |
   | Four Columns With Titles | 13 | 12 | ❌ | ✅ |
   ```

3. **Detailed Layout Specifications**
   For each layout:
   ```markdown
   ### Title Slide (Index: 0)
   **PowerPoint Placeholders**:
   - `idx=0`: "Title 1" → Maps to `title` field
   - `idx=1`: "Subtitle 2" → Maps to `subtitle` field
   
   **JSON Mapping**: ✅ Configured in `default.json`
   **Structured Frontmatter**: ✅ Supported with YAML pattern
   **Usage Example**:
   ```yaml
   ---
   layout: Title Slide
   ---
   # My Presentation Title
   ## Subtitle text
   ```

4. **Structured Frontmatter Support Analysis**
   - Layouts with structured patterns
   - Missing pattern implementations
   - Suggested YAML structures

5. **Usage Examples**
   - JSON format examples for each layout
   - Markdown frontmatter examples
   - Common use cases and best practices

6. **Validation Report**
   - Placeholder naming consistency
   - Missing mappings or patterns
   - Recommendations for improvements

### 4. Template Validation Tool

```python
async def validate_template(ctx: Context, template_name: str, check_structured: bool = True) -> str
```

**Purpose**: Validate template consistency and identify mapping issues

**Parameters**:
- `template_name`: Template to validate
- `check_structured`: Include structured frontmatter validation (default: True)

**Implementation Details**:
```python
def validate_template_implementation(template_name: str, check_structured: bool):
    validation_results = {
        "template_structure": validate_template_structure(template_name),
        "json_mapping": validate_json_mapping(template_name),
        "placeholder_naming": validate_placeholder_naming(template_name),
        "structured_frontmatter": validate_structured_patterns(template_name) if check_structured else None
    }
    
    # Generate validation report
    report = generate_validation_report(validation_results)
    
    return report

def validate_template_structure(template_name: str):
    """Validate basic template structure and accessibility"""
    try:
        prs = Presentation(f"{template_name}.pptx")
        layouts = prs.slide_layouts
        
        return {
            "status": "valid",
            "layout_count": len(layouts),
            "issues": []
        }
    except Exception as e:
        return {
            "status": "invalid", 
            "error": str(e)
        }

def validate_json_mapping(template_name: str):
    """Validate JSON mapping matches template structure"""
    issues = []
    
    # Load template and mapping
    prs = Presentation(f"{template_name}.pptx")
    try:
        mapping = load_json_mapping(f"{template_name}.json")
    except FileNotFoundError:
        return {"status": "missing", "message": "JSON mapping file not found"}
    
    # Check each layout mapping
    for layout_name, layout_info in mapping["layouts"].items():
        layout_index = layout_info["index"]
        
        # Verify layout exists
        if layout_index >= len(prs.slide_layouts):
            issues.append(f"Layout '{layout_name}' index {layout_index} exceeds available layouts")
            continue
            
        actual_layout = prs.slide_layouts[layout_index]
        mapped_placeholders = layout_info.get("placeholders", {})
        
        # Check placeholder mappings
        actual_placeholder_indices = {str(p.placeholder_format.idx) for p in actual_layout.placeholders}
        mapped_indices = set(mapped_placeholders.keys())
        
        missing_in_mapping = actual_placeholder_indices - mapped_indices
        extra_in_mapping = mapped_indices - actual_placeholder_indices
        
        if missing_in_mapping:
            issues.append(f"Layout '{layout_name}': Unmapped placeholders {missing_in_mapping}")
        if extra_in_mapping:
            issues.append(f"Layout '{layout_name}': Extra mappings {extra_in_mapping}")
    
    return {
        "status": "valid" if not issues else "issues_found",
        "issues": issues
    }

def validate_placeholder_naming(template_name: str):
    """Validate placeholder naming follows conventions"""
    naming_issues = []
    
    mapping = load_json_mapping(f"{template_name}.json")
    
    for layout_name, layout_info in mapping["layouts"].items():
        placeholders = layout_info.get("placeholders", {})
        
        for idx, name in placeholders.items():
            # Check naming conventions
            if not follows_naming_convention(name, layout_name):
                naming_issues.append(f"Layout '{layout_name}' placeholder {idx}: '{name}' doesn't follow conventions")
    
    return {
        "status": "valid" if not naming_issues else "issues_found",
        "issues": naming_issues,
        "conventions": get_naming_conventions()
    }
```

**Validation Checks**:
- Template file accessibility and structure
- JSON mapping completeness and accuracy
- Placeholder naming convention compliance
- Structured frontmatter pattern coverage
- Cross-reference consistency

**Output**: Comprehensive validation report with issues and recommendations

## Naming Conventions

### Layout-Specific Patterns

**Column Layouts** (Three Columns, Four Columns, etc.):
- `Col {N} Title Placeholder {idx}` → `columns[N-1].title`
- `Col {N} Text Placeholder {idx}` → `columns[N-1].content`

**SWOT Analysis**:
- `Text Placeholder Top Left` → `swot.strengths`
- `Text Placeholder Top Right` → `swot.weaknesses`
- `Text Placeholder Bottom Left` → `swot.opportunities`
- `Text Placeholder Bottom Right` → `swot.threats`

**Agenda Layouts**:
- `Text Placeholder Number {NN}` → `agenda[N].number`
- `Text Placeholder Content {N}` → `agenda[N].item`

**Comparison Layouts**:
- `Text Placeholder 2` → `comparison.left.title`
- `Content Placeholder 3` → `comparison.left.content`
- `Text Placeholder 4` → `comparison.right.title`
- `Content Placeholder 5` → `comparison.right.content`

### Convention Detection Algorithm

```python
def detect_layout_pattern(layout_name: str, placeholders: Dict[str, str]) -> str:
    """Detect layout pattern from placeholder names"""
    
    if "columns" in layout_name.lower():
        return detect_column_pattern(placeholders)
    elif "swot" in layout_name.lower():
        return "swot_analysis"
    elif "agenda" in layout_name.lower():
        return "agenda_list"
    elif "comparison" in layout_name.lower():
        return "comparison"
    else:
        return "custom"

def generate_structured_pattern(layout_pattern: str, placeholders: Dict[str, str]) -> Dict:
    """Generate structured frontmatter pattern from detected layout"""
    
    if layout_pattern == "columns":
        return generate_column_pattern(placeholders)
    elif layout_pattern == "swot_analysis":
        return generate_swot_pattern(placeholders)
    # ... additional patterns
```

## Implementation Status

### Current State
- ✅ Basic template analysis exists in `tests/test_tools.py`
- ✅ Template analyzer class in `src/mcp_server/tools.py`
- ✅ JSON mapping generation capability
- ✅ Placeholder name modification on individual slides

### Phase 1: Core MCP Tools
- 🚧 Move analysis tools to MCP server
- 🚧 Implement `analyze_template` MCP tool
- 🚧 Add template validation capabilities
- 🚧 Create documentation generator

### Phase 2: Template Enhancement
- ⏳ Implement master slide placeholder modification
- ⏳ Add `enhance_template` MCP tool
- ⏳ Create backup and versioning system
- ⏳ Validate enhancement process

### Phase 3: Advanced Features
- ⏳ Convention-based structured frontmatter generation
- ⏳ Automated pattern detection and suggestion
- ⏳ Template comparison and migration tools
- ⏳ Integration with template documentation system

## User Benefits

1. **Simplified Template Addition**
   - No manual PowerPoint editing required
   - Automated placeholder naming
   - Generated documentation

2. **Consistent Professional Quality**
   - Standardized naming conventions
   - Validated template structure
   - Synchronized mapping and documentation

3. **Improved Developer Experience**
   - Clear template capabilities documentation
   - Automated validation and error detection
   - Easy template customization workflow

4. **Maintainable System**
   - Version-controlled template enhancements
   - Automated documentation updates
   - Consistent structured frontmatter support

## Technical Architecture

### Class Structure

```python
class TemplateManager:
    """Main template management orchestrator"""
    
    def __init__(self, template_folder: str, output_folder: str):
        self.analyzer = TemplateAnalyzer(template_folder)
        self.enhancer = TemplateEnhancer(template_folder)
        self.documenter = TemplateDocumenter(output_folder)
        self.validator = TemplateValidator()

class TemplateAnalyzer:
    """Extracts structure from PowerPoint templates"""
    
    def analyze_structure(self, template_name: str) -> TemplateStructure
    def generate_mapping(self, structure: TemplateStructure) -> JSONMapping
    def detect_patterns(self, structure: TemplateStructure) -> List[LayoutPattern]

class TemplateEnhancer:
    """Modifies master slide placeholder names"""
    
    def enhance_master_slides(self, template_name: str, mapping: JSONMapping) -> EnhancementResult
    def create_backup(self, template_name: str) -> str
    def validate_enhancement(self, enhanced_template: str) -> ValidationResult

class TemplateDocumenter:
    """Generates comprehensive template documentation"""
    
    def generate_documentation(self, template_name: str) -> str
    def create_layout_table(self, layouts: List[Layout]) -> str
    def generate_usage_examples(self, layouts: List[Layout]) -> str

class TemplateValidator:
    """Validates template consistency and conventions"""
    
    def validate_structure(self, template_name: str) -> ValidationResult
    def validate_mapping(self, template_name: str) -> ValidationResult
    def validate_naming(self, template_name: str) -> ValidationResult
```

### Integration Points

- **MCP Server**: Tools exposed through `main.py`
- **Engine Integration**: Enhanced templates work with existing presentation engine
- **Structured Frontmatter**: Auto-generated patterns for YAML support
- **Documentation System**: Generated docs integrate with existing feature docs

This comprehensive template management system will transform template creation from a manual, error-prone process into an automated, validated workflow that produces professional, well-documented templates.