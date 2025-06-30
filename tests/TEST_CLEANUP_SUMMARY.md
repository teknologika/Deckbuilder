# Test Directory Pollution Fix Summary

## Problem Description

Several pytest tests were creating `.pptx` and other output files in the project root directory instead of using proper test output directories. This violated the project's clean directory structure guidelines.

## Files Fixed

### 1. `/tests/deckbuilder/e2e/test_golden_file_validation.py`
**Issues Fixed:**
- CLI tests were searching for output files in both temp directories AND project root (`Path.cwd()`)
- `subprocess.run()` calls used `cwd=self.project_root` which could create files in root
- Search directories included project root paths

**Solutions Applied:**
- Removed `Path.cwd()` from search directories
- Changed `cwd=temp_dir` for all CLI subprocess calls that generate files
- Kept `cwd=self.project_root` only for informational commands (version, config, template list)
- Ensured all output goes to temporary directories

### 2. `/tests/deckbuilder/integration/test_cli_path_management.py` 
**Issues Fixed:**
- CLI tests created temporary files without specifying output directories
- Tests didn't force CLI to use temporary directories for output

**Solutions Applied:**
- Added `output_path=temp_dir` to CLI constructor calls
- Added `dir=temp_dir` parameter to `tempfile.NamedTemporaryFile()` calls
- Wrapped test file creation in `tempfile.TemporaryDirectory()` contexts

### 3. `/tests/conftest.py`
**Enhancements Added:**
- Added `cli_temp_env()` fixture for CLI tests that forces output to temp directories
- Added `prevent_root_pollution()` autouse fixture that automatically detects and cleans up any files created in project root
- Automatic cleanup of common test output directories

## Root Cause Analysis

The main causes of directory pollution were:

1. **Implicit Working Directory**: Tests relied on current working directory without explicitly controlling output paths
2. **Incomplete Mocking**: Environment variables weren't consistently overridden to force temp directory usage  
3. **Mixed Search Patterns**: Tests looked for output in both temp directories AND project root as fallback
4. **CLI Design**: CLI creates output relative to working directory when output folder not explicitly set

## Prevention Strategy

### For Future Test Development:

1. **Always use temporary directories**:
   ```python
   with tempfile.TemporaryDirectory() as temp_dir:
       # Your test code here
   ```

2. **Force CLI output paths**:
   ```python
   cli = DeckbuilderCLI(output_path=temp_dir)
   # OR set environment variables
   env["DECK_OUTPUT_FOLDER"] = temp_dir
   ```

3. **Use `dir=temp_dir` for temporary files**:
   ```python
   with tempfile.NamedTemporaryFile(mode='w', suffix='.md', dir=temp_dir) as f:
   ```

4. **Set working directory for subprocess calls**:
   ```python
   subprocess.run([...], cwd=temp_dir, env=env)  # Not cwd=project_root
   ```

5. **Use the existing fixtures**:
   - `cli_temp_env()` for CLI tests
   - `mock_deckbuilder_env()` for engine tests
   - The autouse `prevent_root_pollution()` fixture provides safety net

## Validation

The `prevent_root_pollution()` fixture automatically:
- Detects any new `.pptx`, `.json`, `.md`, `.txt` files in project root
- Cleans up test output directories like `test_output_md`, `from_markdown`, etc.
- Prints warnings when cleanup occurs (indicates test needs fixing)

## Test Results

After applying fixes:
- ✅ `test_cli_generates_presentation_from_markdown` - PASSED
- ✅ `test_create_presentation_markdown` - PASSED  
- ✅ `test_create_presentation_json` - PASSED
- ✅ `test_unsupported_file_format_error` - PASSED
- ✅ No files created in project root during test execution

## Key Principles for Test Isolation

1. **Never pollute the project root** - Use `/tests/output/` or temporary directories
2. **Use dedicated test environments** - Mock all paths and environment variables
3. **Clean up automatically** - Leverage pytest fixtures for cleanup
4. **Test in isolation** - Each test should be independent of file system state
5. **Use the safety net** - The autouse fixture catches violations

This ensures clean test execution and prevents CI/CD issues related to file system pollution.