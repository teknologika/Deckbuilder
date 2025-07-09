# Testing Framework Specification

## Overview

This document outlines a comprehensive testing framework for the deck-builder MCP project using pytest. The framework provides separate test suites for different components while maintaining shared utilities and clear testing boundaries.

### Purpose and Scope

The testing framework addresses three key requirements:
1. **Content Generation**: Hardcoded sample content for consistent testing
2. **Template Test Generation**: Auto-generate test files from template JSON structures
3. **PowerPoint Validation**: Verify generated PPTX files match expected outputs

### Component Separation

The project has two distinct components requiring different testing approaches:

- **`src/deckbuilder/`**: Core PowerPoint generation engine
- **`src/mcp_server/`**: MCP protocol server interface

This separation allows independent testing, focused dependencies, and parallel development.

## Framework Architecture

### Technology Choice: pytest

**Advantages:**
- **Fixtures**: Reusable test data and setup functions
- **Parametrized tests**: Test multiple scenarios automatically
- **Marks**: Categorize tests (unit, integration, slow, etc.)
- **Coverage reporting**: Comprehensive code coverage analysis
- **Mocking**: Mock external dependencies effectively
- **Parallel execution**: Run tests faster with pytest-xdist
- **Rich assertions**: Better error messages and debugging

### Dependencies

Add to `requirements.txt`:
```txt
# Testing dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-xdist>=3.0.0
pytest-html>=3.0.0
```

## Project Structure

```
tests/
├── conftest.py                    # Global pytest configuration
├── deckbuilder/                   # Tests for deckbuilder engine
│   ├── conftest.py               # deckbuilder-specific fixtures
│   ├── unit/
│   │   ├── test_engine.py
│   │   ├── test_naming_conventions.py
│   │   ├── test_structured_frontmatter.py
│   │   ├── test_layout_intelligence.py
│   │   ├── test_placeholder_types.py
│   │   └── test_table_styles.py
│   ├── integration/
│   │   ├── test_template_processing.py
│   │   ├── test_pptx_generation.py
│   │   ├── test_convention_based_naming.py
│   │   └── test_end_to_end_generation.py
│   └── fixtures/
│       ├── sample_templates/
│       │   ├── default_template.json
│       │   └── custom_template.json
│       ├── sample_content.py
│       ├── expected_outputs/
│       │   ├── four_columns_expected.json
│       │   └── comparison_expected.json
│       └── test_presentations/
│           ├── simple_test.pptx
│           └── complex_test.pptx
│
├── mcp_server/                    # Tests for MCP server
│   ├── conftest.py               # MCP-specific fixtures
│   ├── unit/
│   │   ├── test_tools.py
│   │   ├── test_main.py
│   │   └── test_mcp_handlers.py
│   ├── integration/
│   │   ├── test_mcp_communication.py
│   │   ├── test_tool_execution.py
│   │   └── test_server_lifecycle.py
│   └── fixtures/
│       ├── mcp_requests.py
│       ├── mock_responses.py
│       └── server_configs.py
│
├── shared/                        # Shared test utilities
│   ├── test_helpers.py
│   ├── common_fixtures.py
│   └── validation_utils.py
│
└── utils/                         # Test framework utilities
    ├── content_generator.py       # Content generation system
    ├── template_test_generator.py # Auto-generate test files
    ├── pptx_validator.py          # PowerPoint validation
    └── test_runner.py             # Test orchestration
```

## Deckbuilder Testing Suite

### Unit Tests

**Core Engine Components:**
```python
# test_engine.py
class TestDeckbuilderEngine:
    def test_singleton_behavior(self):
        """Verify deckbuilder singleton pattern"""

    def test_template_loading(self, sample_template):
        """Test template JSON loading and parsing"""

    def test_environment_configuration(self):
        """Test environment variable handling"""

# test_naming_conventions.py
class TestNamingConventions:
    @pytest.mark.parametrize("layout_name,expected_pattern", [
        ("Four Columns", "content_col{}_1"),
        ("Comparison", "content_left_1")
    ])
    def test_convention_generation(self, layout_name, expected_pattern):
        """Test convention-based placeholder naming"""

    def test_multi_tier_detection(self):
        """Test 5-tier detection system confidence scoring"""

# test_structured_frontmatter.py
class TestStructuredFrontmatter:
    def test_yaml_to_placeholder_conversion(self, structured_yaml):
        """Test conversion from structured YAML to placeholders"""

    def test_validation_rules(self, invalid_frontmatter):
        """Test frontmatter validation and error handling"""
```

### Integration Tests

**Template Processing and PowerPoint Generation:**
```python
# test_template_processing.py
class TestTemplateProcessing:
    def test_full_template_processing(self, complex_template):
        """Test complete template processing pipeline"""

    def test_placeholder_population(self, content_variations):
        """Test all placeholders get populated correctly"""

# test_pptx_generation.py
class TestPowerPointGeneration:
    def test_slide_creation(self, sample_presentation_data):
        """Test slide creation from JSON data"""

    def test_formatting_preservation(self, formatted_content):
        """Test bold/italic/underline formatting preservation"""

    def test_table_generation(self, table_data):
        """Test table creation and styling"""
```

### Content Generation System

**Hardcoded Sample Content Library:**
```python
# fixtures/sample_content.py
BUSINESS_CONTENT = {
    'short': {
        'titles': ['Q4 Results', 'Market Update', 'Strategic Vision'],
        'content': ['Revenue up 15%', 'Strong market position', 'Growth initiatives']
    },
    'medium': {
        'titles': ['Quarterly Performance Review', 'Market Analysis & Trends'],
        'content': ['Revenue increased 15% year-over-year...', 'Market conditions show...']
    },
    'long': {
        'titles': ['Comprehensive Quarterly Performance Analysis'],
        'content': ['Our comprehensive analysis of Q4 performance shows...']
    }
}

TECHNICAL_CONTENT = {
    'architecture': ['Microservices', 'API Gateway', 'Database Layer'],
    'features': ['Authentication', 'Authorization', 'Monitoring'],
    'metrics': ['99.9% uptime', '50ms response time', '1M+ requests/day']
}

MARKETING_CONTENT = {
    'campaigns': ['Brand Awareness', 'Lead Generation', 'Customer Retention'],
    'channels': ['Digital Marketing', 'Social Media', 'Content Marketing'],
    'results': ['30% increase in leads', '25% higher engagement', '40% ROI improvement']
}
```

### PowerPoint Validation System

**PPTX Content Verification:**
```python
# utils/pptx_validator.py
class PowerPointValidator:
    def validate_content_preservation(self, pptx_path, expected_content):
        """Verify all expected content appears in generated PPTX"""

    def validate_layout_correctness(self, pptx_path, layout_mapping):
        """Verify correct slide layouts are used"""

    def validate_formatting_preservation(self, pptx_path, formatting_rules):
        """Verify bold/italic/underline formatting is preserved"""

    def validate_placeholder_population(self, pptx_path):
        """Ensure no placeholders remain empty"""

    def generate_validation_report(self, results):
        """Generate detailed validation report"""
```

## MCP Server Testing Suite

### Unit Tests

**Protocol and Tool Testing:**
```python
# test_tools.py
class TestMCPTools:
    def test_create_presentation_tool(self, mock_request):
        """Test create_presentation_from_markdown tool"""

    def test_analyze_template_tool(self, sample_template):
        """Test analyze_pptx_template tool"""

    def test_error_handling(self, invalid_requests):
        """Test tool error handling and responses"""

# test_mcp_handlers.py
class TestMCPHandlers:
    def test_request_parsing(self, mcp_requests):
        """Test MCP request parsing and validation"""

    def test_response_formatting(self, tool_results):
        """Test MCP response formatting"""
```

### Integration Tests

**Server Communication and Tool Execution:**
```python
# test_mcp_communication.py
class TestMCPCommunication:
    def test_server_startup(self):
        """Test MCP server initialization"""

    def test_tool_discovery(self, mcp_client):
        """Test tool discovery and registration"""

    def test_end_to_end_presentation_creation(self, full_request):
        """Test complete presentation creation workflow"""
```

## Test Utilities

### Template Test Generator

**Auto-generate test files from template JSON:**
```python
# utils/template_test_generator.py
class TemplateTestGenerator:
    def generate_test_files(self, template_json_path):
        """Generate {template_name}_test.json and {template_name}_test.md"""

    def validate_layout_coverage(self, template_json):
        """Ensure all layouts in template have test coverage"""

    def generate_structured_frontmatter_tests(self, layouts):
        """Generate structured frontmatter examples for each layout"""
```

### Content Builders

**Dynamic content generation for testing:**
```python
# utils/content_generator.py
class ContentGenerator:
    def build_column_content(self, num_columns, content_type='business'):
        """Generate content for multi-column layouts"""

    def build_comparison_content(self, comparison_type='features'):
        """Generate left/right comparison content"""

    def build_table_content(self, rows, cols, include_formatting=True):
        """Generate table data with optional formatting"""

    def apply_formatting_variations(self, content):
        """Add bold/italic/underline variations to content"""
```

## Test Execution

### Command Reference

```bash
# Run all tests
pytest

# Run with coverage reporting
pytest --cov=src/deckbuilder --cov=src/mcp_server --cov-report=html

# Run specific component tests
pytest tests/deckbuilder/
pytest tests/mcp_server/

# Run specific test types
pytest tests/deckbuilder/unit/
pytest tests/deckbuilder/integration/

# Run tests matching pattern
pytest -k "test_four_columns"
pytest -k "naming_conventions"

# Run tests with specific marks
pytest -m "unit"
pytest -m "integration"
pytest -m "slow" --maxfail=1

# Run tests in parallel
pytest -n auto

# Generate HTML report
pytest --html=reports/test_report.html
```

### Test Marks

```python
# Categorize tests with marks
@pytest.mark.unit
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.deckbuilder
@pytest.mark.mcp_server
@pytest.mark.requires_template
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test-deckbuilder:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run deckbuilder tests
        run: pytest tests/deckbuilder/ --cov=src/deckbuilder

  test-mcp-server:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run MCP server tests
        run: pytest tests/mcp_server/ --cov=src/mcp_server
```

## Benefits

### Component Separation Benefits

1. **Independent Testing**: Test deckbuilder engine without MCP server dependencies
2. **Focused Dependencies**: Each test suite only requires component-specific dependencies
3. **Parallel Development**: Teams can work on different components independently
4. **Optimized CI/CD**: Run different test suites at different pipeline stages
5. **Clear Boundaries**: Enforces separation of concerns between components

### Testing Framework Benefits

1. **Comprehensive Coverage**: Unit, integration, and end-to-end testing
2. **Automated Generation**: Auto-generate test files from template structures
3. **Content Validation**: Verify PowerPoint content, formatting, and layout
4. **Regression Prevention**: Compare against known-good outputs
5. **Performance Monitoring**: Track test execution time and resource usage

---

## TODO List

### Phase 1: Foundation Setup
- [ ] Add pytest dependencies to requirements.txt
- [ ] Create basic test directory structure
- [ ] Set up global conftest.py with basic fixtures
- [ ] Create pytest.ini configuration file
- [ ] Set up coverage reporting configuration

### Phase 2: Content Generation System
- [ ] Create `utils/content_generator.py` with hardcoded sample libraries
- [ ] Implement business, technical, and marketing content sets
- [ ] Add content variation generators (short, medium, long)
- [ ] Create formatting variation system (bold, italic, underline combinations)
- [ ] Add dynamic content builders for specific layouts

### Phase 3: Deckbuilder Test Suite
- [ ] Create `tests/deckbuilder/conftest.py` with deckbuilder-specific fixtures
- [ ] Implement unit tests for core engine components:
  - [ ] `test_engine.py` - Singleton, template loading, environment config
  - [ ] `test_naming_conventions.py` - Convention-based naming, multi-tier detection
  - [ ] `test_structured_frontmatter.py` - YAML conversion, validation
  - [ ] `test_layout_intelligence.py` - Content analysis, layout recommendations
  - [ ] `test_placeholder_types.py` - Placeholder type detection
- [ ] Implement integration tests:
  - [ ] `test_template_processing.py` - End-to-end template processing
  - [ ] `test_pptx_generation.py` - PowerPoint file generation
  - [ ] `test_convention_based_naming.py` - Full naming convention workflow

### Phase 4: PowerPoint Validation System
- [ ] Create `utils/pptx_validator.py` with validation utilities
- [ ] Implement content preservation validation
- [ ] Add layout correctness verification
- [ ] Create formatting preservation checks
- [ ] Add placeholder population validation
- [ ] Implement validation report generation

### Phase 5: Template Test Generator
- [ ] Create `utils/template_test_generator.py`
- [ ] Implement automatic test file generation from template JSON
- [ ] Add layout coverage verification
- [ ] Create structured frontmatter test generation
- [ ] Add template validation utilities

### Phase 6: MCP Server Test Suite
- [ ] Create `tests/mcp_server/conftest.py` with MCP-specific fixtures
- [ ] Implement unit tests:
  - [ ] `test_tools.py` - MCP tool functionality
  - [ ] `test_main.py` - Server initialization and configuration
  - [ ] `test_mcp_handlers.py` - Request/response handling
- [ ] Implement integration tests:
  - [ ] `test_mcp_communication.py` - Server communication protocols
  - [ ] `test_tool_execution.py` - End-to-end tool execution
  - [ ] `test_server_lifecycle.py` - Server startup/shutdown

### Phase 7: Test Data and Fixtures
- [ ] Create sample template JSON files in `fixtures/sample_templates/`
- [ ] Add expected output files in `fixtures/expected_outputs/`
- [ ] Create test presentation files in `fixtures/test_presentations/`
- [ ] Implement shared fixtures in `shared/common_fixtures.py`
- [ ] Add MCP request/response fixtures

### Phase 8: Execution and Reporting
- [ ] Set up coverage reporting with HTML output
- [ ] Configure parallel test execution
- [ ] Add performance benchmarking for slow tests
- [ ] Create test result reporting utilities
- [ ] Set up CI/CD integration

### Phase 9: Advanced Features
- [ ] Add property-based testing with hypothesis
- [ ] Implement visual regression testing for PowerPoint outputs
- [ ] Add load testing for MCP server performance
- [ ] Create test data factories for complex scenarios
- [ ] Add mutation testing for test quality verification

### Phase 10: Documentation and Training
- [ ] Create test writing guidelines
- [ ] Document test execution procedures
- [ ] Add troubleshooting guide for common test failures
- [ ] Create examples of good test patterns
- [ ] Set up automated test documentation generation
