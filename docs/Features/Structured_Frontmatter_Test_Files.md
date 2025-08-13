# Structured Frontmatter Test Files System

## Overview

The Structured Frontmatter Test Files system provides comprehensive sample data for all layout patterns, enabling systematic validation, testing, and example generation. This system treats the 30+ structured frontmatter pattern files as the **single source of truth** for field specifications.

### Purpose
- **Validation Testing**: Ensure field processor handles all valid field combinations correctly
- **Example Generation**: Provide realistic test data for each layout type
- **Integration Testing**: Enable comprehensive presentations exercising all patterns
- **Documentation Support**: Generate examples for user guides and API documentation

### Relationship to Architecture
The test files system directly supports our clean, name-based processing architecture by:
- Validating against structured frontmatter pattern specifications
- Eliminating need for legacy field accommodation
- Providing authoritative test data for each layout's valid fields
- Supporting single-path processing validation

## Architecture

### Directory Structure
```
src/deckbuilder/structured_frontmatter_patterns/
├── test_files/
│   ├── basic/
│   │   ├── title_slide/
│   │   ├── title_and_content/
│   │   ├── title_only/
│   │   └── blank/
│   ├── multi_column/
│   │   ├── two_content/
│   │   ├── three_columns/
│   │   ├── four_columns/
│   │   └── comparison/
│   ├── specialized/
│   │   ├── swot_analysis/
│   │   ├── agenda_6_textboxes/
│   │   ├── title_and_6_item_lists/
│   │   └── big_number/
│   ├── tables/
│   │   ├── table_only/
│   │   ├── table_with_content_above/
│   │   ├── table_with_content_above_and_below/
│   │   └── table_with_content_left/
│   └── advanced/
│       ├── timeline/
│       ├── process_steps/
│       ├── team_members/
│       └── key_metrics/
├── [existing pattern files...]
└── README.md
```

### File Naming Conventions
For each layout pattern directory:
- `basic_example.json` - Minimal valid data matching required fields only
- `rich_content_example.json` - Full data with formatting and all optional fields
- `edge_case_example.json` - Boundary conditions, special characters, complex content
- `basic_example.md` - Minimal valid data matching required fields only that matches `basic_example.json`
- `rich_content_example.md` - Full data with formatting and all optional fields that matches `rich_content_example.json`

### When Building The app
`rich_content_example.json` and `rich_content_example.md` will be used to generate the files that are deployed when deckbuilder init is run as `example_presentaiton.json` and `example_presentation.md`

## When testing the app
A test harness will be created as follows.

1. Each test will will execute using `Bash(source .venv/bin/activate && deckbuilder create tests/output/imput_file --output tests/output/ouput_file)`, or the deckbuilder equivalent call, "black box" testing style.
2. The output pptx file will be loaded, and verified 1:1 against the input json using python-pptx. this will confirm existance of content on the slide matches what is expected using the python-pptx api to verify the file. This will be done using a write once, use many test harness that follows DRY principles.
3. Once proven. This testing approach will be extended to replace as many existing tests as possible.

## Test Data Categories

### Basic Examples
**Purpose**: Validate minimal field requirements
**Content**: 
- Only required fields populated
- Simple, clean content without formatting
- Baseline validation data

**Example** (`title_slide/basic_example.json`):
```json
{
  "slides": [{
    "layout": "Title Slide",
    "placeholders": {
      "title": "Basic Title Slide",
      "subtitle": "Simple subtitle text"
    }
  }]
}
```

### Rich Content Examples  
**Purpose**: Test full feature set including formatting
**Content**:
- All required and optional fields populated
- Rich markdown formatting: **bold**, *italic*, ***bold+italic***, ___underline___
- Realistic professional content
- Complex structures (bullets, numbering, multi-line)

**Example** (`swot_analysis/rich_content_example.json`):
```json
{
  "slides": [{
    "layout": "SWOT Analysis", 
    "placeholders": {
      "title": "**SWOT** Analysis - *Strategic* Overview",
      "content_top_left": "**Strengths**\n- *Market leadership* position\n• ***Innovative*** technology platform\n- ___Strong___ customer relationships",
      "content_top_right": "**Weaknesses**\n- *Limited* geographic presence\n• ***High*** operational costs\n- ___Dependency___ on key suppliers",
      "content_bottom_left": "**Opportunities**\n- *Emerging* markets expansion\n• ***Digital*** transformation trends\n- ___Strategic___ partnerships",
      "content_bottom_right": "**Threats**\n- *Increased* competition\n- ***Regulatory*** changes\n- ___Economic___ uncertainty"
    }
  }]
}
```

### Edge Case Examples
**Purpose**: Test boundary conditions and error handling
**Content**:
- Maximum field lengths
- Special characters and Unicode
- Empty optional fields
- Complex formatting combinations
- Unusual but valid content structures

## Implementation Plan

### Phase 1: Infrastructure Creation
1. **Create** `src/deckbuilder/structured_frontmatter_patterns/test_files/` directory
2. **Establish** category subdirectories (basic, multi_column, specialized, tables, advanced)
3. **Create** layout-specific subdirectories for each of the 30+ patterns
4. **Add** README.md explaining structure and usage

### Phase 2: Sample Test Data Generation
1. **Analyze** each structured frontmatter pattern's `yaml_pattern` specification
2. **Generate** test data matching field requirements exactly
3. **Include** realistic, professional content appropriate to each layout type
4. **Ensure** proper markdown formatting demonstration
5. **Validate** test data against pattern specifications

### Phase 3: Test Data Categories Implementation
1. **Create** basic examples for all 30+ layout patterns
2. **Develop** rich content examples with full formatting
3. **Design** edge case examples for boundary testing
4. **Verify** all test data loads and processes correctly

### Phase 4: Integration Framework
1. **Create** test utilities to load test files programmatically
2. **Implement** batch validation against structured frontmatter patterns
3. **Enable** automated testing of field mapping for all layouts
4. **Support** future example generation and documentation creation

## Layout Coverage

### Complete Pattern Mapping
The test files system covers all structured frontmatter patterns:

**Basic Layouts (4)**:
- `title_slide` - Professional presentation opening
- `title_and_content` - Standard content slide
- `title_only` - Section breaks and discussion prompts  
- `blank` - Custom content slides

**Multi-Column Layouts (8)**:
- `two_content` - Side-by-side comparison
- `comparison` - Before/after or competitive analysis
- `three_columns` - Triple content areas
- `three_columns_with_titles` - Titled triple columns
- `four_columns` - Quadruple content areas  
- `four_columns_with_titles` - Titled quadruple columns
- `before_and_after` - Transformation showcases
- `pros_and_cons` - Decision analysis

**Specialized Layouts (10)**:
- `swot_analysis` - Strategic quadrant analysis
- `agenda_6_textboxes` - Meeting agenda format
- `title_and_6_item_lists` - Complex multi-section content
- `big_number` - Key metric highlighting
- `timeline` - Process or historical progression
- `process_steps` - Workflow documentation
- `team_members` - Personnel showcases
- `key_metrics` - Performance dashboards
- `problem_solution` - Issue resolution format
- `section_header` - Topic introductions

**Table Layouts (5)**:
- `table_only` - Pure data presentation
- `table_with_content_above` - Context + data
- `table_with_content_above_and_below` - Full context + data + conclusion
- `table_with_content_left` - Side-by-side table and content
- `content_table_content_table_content` - Complex alternating layout

**Media Layouts (3)**:
- `picture_with_caption` - Image-focused slides
- `content_with_caption` - Content with explanatory captions
- `title_and_vertical_text` - Vertical content orientation

### Field Specifications
Each test file strictly adheres to its pattern's field requirements:
- **Required fields**: Must be present in all examples
- **Optional fields**: Demonstrated in rich content examples
- **Field types**: String, with proper markdown formatting support
- **Validation**: Matches `yaml_pattern` specification exactly

## Future Integration

### Automated Example Generation
The test files provide foundation for:
- **User documentation examples**: Convert test data to markdown examples
- **API documentation**: Generate code samples and expected outputs  
- **Tutorial content**: Progressive examples from basic to advanced
- **Template showcases**: Visual examples of each layout capability

### Comprehensive Testing Framework
Test files enable:
- **Field mapping validation**: Systematic testing of all field combinations
- **Presentation generation testing**: End-to-end validation using realistic data
- **Regression testing**: Ensure changes don't break existing functionality
- **Performance testing**: Benchmark processing with representative data

### Documentation Generation
- **Pattern documentation**: Auto-generate pattern usage examples
- **Field reference**: Create comprehensive field specification docs
- **Layout galleries**: Visual showcases of all layout capabilities
- **Best practices**: Examples demonstrating optimal content structure

## Benefits

### Code Quality
- ✅ **Single Source of Truth**: Structured frontmatter patterns define all valid fields
- ✅ **Eliminates Legacy Accommodation**: No need for arbitrary field name handling
- ✅ **Clean Validation**: Test against authoritative pattern specifications
- ✅ **Systematic Coverage**: Every layout pattern has comprehensive test data

### Development Efficiency  
- ✅ **Rapid Testing**: Pre-built test data for all scenarios
- ✅ **Realistic Examples**: Professional content for meaningful testing
- ✅ **Edge Case Coverage**: Boundary conditions pre-defined
- ✅ **Integration Ready**: Foundation for automated testing frameworks

### User Experience
- ✅ **Clear Examples**: Users see realistic, professional content examples
- ✅ **Pattern Understanding**: Each layout's capabilities clearly demonstrated
- ✅ **Best Practices**: Examples show optimal content structure and formatting
- ✅ **Progressive Learning**: Basic to advanced examples for skill building

This system creates a comprehensive test data foundation that maintains our architectural principles while providing robust validation and example generation capabilities.