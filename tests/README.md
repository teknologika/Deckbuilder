# Testing Framework for Deck Builder MCP

This directory contains a comprehensive testing framework for the deck-builder MCP project, designed to work seamlessly with VS Code and provide robust validation of all components.

## Quick Start

### VS Code Setup

1. **Open the workspace**: Open `deck-builder-mcp.code-workspace` in VS Code
2. **Install recommended extensions**: VS Code will prompt you to install recommended extensions
3. **Activate environment**: The testing framework will automatically detect your Python virtual environment
4. **Run tests**: Use the Testing tab in VS Code or keyboard shortcuts

### Command Line Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python tests/utils/test_runner.py --all

# Run specific component tests
python tests/utils/test_runner.py --deckbuilder
python tests/utils/test_runner.py --mcp-server

# Run with coverage
python tests/utils/test_runner.py --coverage

# Validate environment
python tests/utils/test_runner.py --validate
```

## VS Code Integration Features

### 🧪 Test Discovery & Execution
- **Automatic test discovery**: Tests are automatically discovered and shown in the Testing panel
- **Run individual tests**: Click any test in the Test Explorer to run it
- **Debug tests**: Set breakpoints and debug tests directly in VS Code
- **Keyboard shortcuts**: 
  - `Ctrl+Shift+P` → "Python: Run All Tests"
  - `Ctrl+Shift+P` → "Python: Debug All Tests"

### 📊 Coverage Integration
- **Visual coverage**: Coverage gutters show which lines are covered
- **Coverage reports**: HTML reports generated in `htmlcov/` directory
- **Real-time feedback**: Coverage updates as you run tests

### 🛠️ Development Tools
- **Snippets**: Type `testclass`, `testmethod`, `fixture` for quick test templates
- **Formatting**: Automatic code formatting on save
- **Linting**: Real-time error detection and suggestions
- **IntelliSense**: Full autocompletion for test fixtures and utilities

### 🚀 Quick Actions
Use the Command Palette (`Ctrl+Shift+P`) for quick actions:
- "Tasks: Run Task" → Choose from predefined test tasks
- "Python: Run Selection/Line in Python Terminal"
- "Test: Run All Tests"
- "Test: Debug All Tests"

## Test Structure

```
tests/
├── conftest.py                    # Global pytest configuration
├── deckbuilder/                   # Deckbuilder engine tests
│   ├── conftest.py               # Deckbuilder-specific fixtures
│   ├── unit/                     # Unit tests
│   │   ├── test_engine.py
│   │   ├── test_naming_conventions.py
│   │   └── test_structured_frontmatter.py
│   ├── integration/              # Integration tests
│   │   └── test_template_processing.py
│   └── fixtures/                 # Test data and fixtures
│       ├── sample_content.py
│       └── sample_templates/
├── mcp_server/                   # MCP server tests
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── utils/                        # Test utilities
│   ├── content_generator.py     # Content generation system
│   ├── template_test_generator.py # Auto-generate test files
│   ├── pptx_validator.py        # PowerPoint validation
│   └── test_runner.py           # Command-line test runner
└── shared/                      # Shared utilities
```

## Running Tests in VS Code

### Method 1: Test Explorer
1. Open the **Testing** panel (Test tube icon in sidebar)
2. Tests are automatically discovered and displayed
3. Click the play button next to any test to run it
4. Use the debug button to debug with breakpoints

### Method 2: Command Palette
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Run" and select your preferred option:
   - "Python: Run All Tests"
   - "Python: Run Failed Tests"
   - "Python: Debug All Tests"

### Method 3: Tasks
1. Press `Ctrl+Shift+P` and type "Tasks: Run Task"
2. Choose from predefined tasks:
   - "pytest: Run All Tests"
   - "pytest: Run Deckbuilder Tests"
   - "pytest: Run with Coverage"
   - "pytest: Generate Test Report"

### Method 4: Terminal
Use the integrated terminal with the test runner:
```bash
# In VS Code terminal
python tests/utils/test_runner.py --deckbuilder --coverage
```

## Debugging Tests

### Setting Breakpoints
1. Open any test file
2. Click in the gutter next to line numbers to set breakpoints
3. Run tests in debug mode:
   - Use "Debug All Tests" from Command Palette
   - Or click the debug button in Test Explorer

### Debug Configurations
Pre-configured debug configurations are available:
- **Debug Current Test File**: Debug the currently open test file
- **Debug Specific Test Function**: Debug a specific test function
- **Debug All Deckbuilder Tests**: Debug all deckbuilder tests
- **Debug Template Test Generator**: Debug template generation

### Debug Console
Use the Debug Console to:
- Inspect variables during test execution
- Execute Python code in the test context
- Examine fixture values and test state

## Test Utilities

### Content Generator
Generates realistic test content for different scenarios:

```python
from tests.utils.content_generator import ContentGenerator, ContentType

# Create generator
generator = ContentGenerator(seed=42)

# Generate column content
columns = generator.build_column_content(4, ContentType.BUSINESS)

# Generate comparison content
comparison = generator.build_comparison_content('features')

# Generate table data
table = generator.build_table_content(5, 3, include_formatting=True)
```

### Template Test Generator
Auto-generates test files from template JSON:

```python
from tests.utils.template_test_generator import TemplateTestGenerator
from pathlib import Path

# Generate test files for a template
generator = TemplateTestGenerator()
report = generator.generate_test_files(
    template_path=Path("assets/templates/default.json"),
    output_dir=Path("tests/generated"),
    content_type=ContentType.BUSINESS
)

print(f"Generated {len(report.generated_files)} test files")
print(f"Coverage: {report.coverage_percentage:.1f}%")
```

### PowerPoint Validator
Validates generated PowerPoint files:

```python
from tests.utils.pptx_validator import PowerPointValidator
from pathlib import Path

# Validate a presentation
validator = PowerPointValidator()
report = validator.validate_presentation(
    pptx_path=Path("output/test.pptx"),
    expected_content=expected_data
)

print(f"Validation result: {report.overall_result}")
print(f"Success rate: {report.success_rate:.1f}%")
```

## Coverage Reports

### Viewing Coverage in VS Code
1. Install the "Coverage Gutters" extension (recommended)
2. Run tests with coverage: `python tests/utils/test_runner.py --coverage`
3. Coverage indicators appear in the editor gutter:
   - ✅ Green: Line is covered
   - ❌ Red: Line is not covered
   - 🔶 Orange: Line is partially covered

### HTML Coverage Reports
Generate detailed HTML coverage reports:
```bash
python tests/utils/test_runner.py --coverage
open htmlcov/index.html  # Open in browser
```

## Test Markers

Use pytest markers to categorize and run specific test types:

```python
@pytest.mark.unit
@pytest.mark.deckbuilder
def test_naming_conventions():
    """Unit test for naming conventions."""
    pass

@pytest.mark.integration
@pytest.mark.requires_template
def test_template_processing():
    """Integration test requiring template files."""
    pass
```

Run tests by marker:
```bash
# Run only unit tests
pytest -m "unit"

# Run deckbuilder integration tests
pytest -m "integration and deckbuilder"

# Exclude slow tests
pytest -m "not slow"
```

## Fixtures and Test Data

### Global Fixtures (conftest.py)
- `project_root`: Path to project root
- `temp_dir`: Temporary directory for test files
- `mock_env_vars`: Mock environment variables
- `sample_template_json`: Basic template structure
- `sample_presentation_data`: Sample presentation data

### Deckbuilder Fixtures
- `naming_convention`: NamingConvention instance
- `structured_frontmatter_registry`: Registry for frontmatter patterns
- `layout_intelligence`: Layout intelligence engine
- `content_generator`: Content generation with fixed seed

### Content Fixtures
- `business_content_short/medium/long`: Business content samples
- `four_column_content`: Content for 4-column layouts
- `comparison_content`: Content for comparison layouts
- `table_content`: Table data with formatting

## Custom Test Snippets

VS Code includes custom snippets for common test patterns:

- `testclass` → Create pytest test class
- `testmethod` → Create test method
- `parametrize` → Create parametrized test
- `fixture` → Create pytest fixture
- `contenttest` → Create content generator test
- `pptxtest` → Create PowerPoint validation test
- `templatetest` → Create template generator test
- `mockenv` → Create test with mocked environment

## Troubleshooting

### Tests Not Discovered
1. Check that pytest is installed: `pip install pytest`
2. Verify Python interpreter path in VS Code settings
3. Ensure `tests/` directory is in workspace root
4. Check that test files follow naming convention (`test_*.py`)

### Import Errors
1. Verify `PYTHONPATH` includes `src/` and `tests/` directories
2. Check virtual environment is activated
3. Install required dependencies: `pip install -r requirements.txt`

### VS Code Not Finding Tests
1. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Clear test cache: `Ctrl+Shift+P` → "Python: Clear Cache and Reload Window"
3. Check test discovery settings in `.vscode/settings.json`

### Coverage Not Showing
1. Install Coverage Gutters extension
2. Run tests with coverage flag
3. Check that `.coverage` file is generated
4. Manually trigger coverage display: `Ctrl+Shift+P` → "Coverage Gutters: Display Coverage"

## Performance Tips

### Faster Test Execution
- Use `pytest -x` to stop on first failure
- Run specific test files instead of entire suite
- Use `pytest -k "test_name"` to run specific tests
- Enable parallel execution: `pytest -n auto`

### Efficient Development Workflow
1. Use "Run Tests on Save" for immediate feedback
2. Set up file watchers for automatic test execution
3. Use focused testing during development (`pytest path/to/specific/test.py`)
4. Leverage VS Code's integrated terminal for quick commands

## CI/CD Integration

The testing framework integrates with GitHub Actions for continuous testing:

- **Parallel test execution** across components
- **Multiple Python version testing** (3.8, 3.9, 3.10, 3.11)
- **Coverage reporting** with Codecov integration
- **Artifact collection** for test reports and coverage data
- **Code quality checks** with black, flake8, and mypy

See `.github/workflows/test.yml` for the complete CI configuration.

## Best Practices

### Writing Tests
1. **Follow AAA pattern**: Arrange, Act, Assert
2. **Use descriptive names**: Test names should explain what they test
3. **One assertion per test**: Keep tests focused and specific
4. **Use fixtures**: Leverage pytest fixtures for test data
5. **Mock external dependencies**: Use `pytest-mock` for isolation

### Test Organization
1. **Separate unit and integration tests**: Use different directories
2. **Group related tests**: Use test classes for related functionality
3. **Use meaningful markers**: Tag tests appropriately
4. **Keep tests independent**: Each test should run in isolation

### VS Code Workflow
1. **Use Test Explorer**: Leverage VS Code's test discovery
2. **Set up debugging**: Configure breakpoints for complex tests
3. **Monitor coverage**: Use coverage gutters for immediate feedback
4. **Organize workspace**: Use the provided workspace configuration
5. **Leverage snippets**: Use custom snippets for common patterns

---

For more information, see the [Testing Framework Specification](../docs/Features/Testing_Framework.md).