# Structured Frontmatter Test Files

This directory contains comprehensive test examples for all structured frontmatter layout patterns in Deckbuilder. Each layout pattern has two corresponding files:

- `example_[layout_name].json` - JSON format example
- `example_[layout_name].md` - Markdown format example  

## File Structure

All files follow the flattened naming convention:
```
test_files/
├── example_title_slide.json
├── example_title_slide.md
├── example_title_and_content.json
├── example_title_and_content.md
├── example_comparison.json
├── example_comparison.md
├── example_swot_analysis.json
├── example_swot_analysis.md
├── example_table_only.json
├── example_table_only.md
└── ... (22 total layout examples)
```

## Content Standards

Each example demonstrates:
- **Rich formatting** using markdown syntax (`**bold**`, `*italic*`, `___underline___`, `***bold-italic***`)
- **Professional business content** relevant to Deckbuilder's capabilities
- **Complete field coverage** for the layout pattern
- **Real-world scenarios** that users would actually create

## Development Workflow

### Adding New Layout Examples

1. **Create the example files** in this directory:
   ```bash
   # Create both JSON and Markdown versions
   touch test_files/example_new_layout.json
   touch test_files/example_new_layout.md
   ```

2. **Run tests** to verify the new examples work:
   ```bash
   python tests/test_structured_frontmatter_examples.py
   ```

3. **Generate master files** for packaging:
   ```bash
   python scripts/generate_master_examples.py
   ```

4. **Complete build process** (recommended):
   ```bash
   ./scripts/build_examples.sh
   ```

### Automated Build Process

The build script (`scripts/build_examples.sh`) provides a complete workflow:
1. ✅ **Test Validation** - Runs comprehensive test suite with cleanup
2. 🔍 **Layout Detection** - Auto-discovers all example files
3. 📋 **Template Ordering** - Orders examples by PowerPoint template sequence
4. 📦 **Master Generation** - Creates `master_examples.json` and `master_examples.md`

### Master Files for Packaging

Generated automatically in project root:
- **`master_examples.json`** - All examples combined in template order (for programmatic use)
- **`master_examples.md`** - All examples combined in template order (for documentation)

These files are regenerated automatically whenever you run the build process and contain:
- Complete metadata about source files
- All 22+ layout examples in PowerPoint template order
- Ready-to-use format for distribution and packaging

## Testing

### Manual Testing
```bash
# Run all tests with cleanup
python tests/test_structured_frontmatter_examples.py
```

### Automated Testing
```bash
# Complete build process (tests + master file generation)
./scripts/build_examples.sh
```

The test suite validates all examples using:
- **Black-box testing** with subprocess CLI execution
- **1:1 validation** using python-pptx analysis
- **Automatic cleanup** of generated test files
- **100% success rate** across all layout patterns

## Current Coverage

### ✅ Implemented Layouts (22 total)
- **Basic Foundation**: title_slide, title_and_content, title_only, blank
- **Multi-Column**: two_content, comparison, three_columns, four_columns
- **Business Intelligence**: key_metrics, big_number, process_steps, team_members
- **Comparisons**: before_and_after, problem_solution, pros_and_cons
- **Data & Analysis**: table_only, table_with_content_above, swot_analysis
- **Content & Media**: picture_with_caption, section_header
- **Specialized**: timeline, agenda_6_textboxes

### 🔄 Auto-Generated Files
When you run the build process, these master files are created:
- `master_examples.json` (all examples in template order)
- `master_examples.md` (all examples in template order)

This system provides a robust, scalable foundation for maintaining comprehensive layout examples that automatically stay synchronized with the PowerPoint template structure.