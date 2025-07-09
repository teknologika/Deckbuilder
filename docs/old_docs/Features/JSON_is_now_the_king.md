# Refactoring Plan: JSON is King

This document outlines the architectural refactor to standardize the Deckbuilder rendering pipeline on a single, canonical JSON model. The goal is to eliminate inconsistencies, improve robustness, and simplify the core engine for future development.

## Task List ✅ COMPLETED

- [x] **1. Implement Canonical JSON Model:** Define and document the final JSON schema. ✅ COMPLETED
- [x] **2. Create Converter Module:** Create `src/deckbuilder/converter.py`. ✅ COMPLETED
- [x] **3. Implement `markdown_to_json`:** Build the function in the new module to convert `.md` files to the canonical JSON format. ✅ COMPLETED
- [x] **4. Refactor `cli.py`:** Update the `create` command to use the new converter and pass only JSON to the engine. ✅ COMPLETED
- [x] **5. Refactor `engine.py`:** Strip all Markdown and multi-format parsing logic, leaving only the logic that processes the canonical JSON model. ✅ COMPLETED
- [x] **6. Refactor `structured_frontmatter.py`:** Integrate its conversion logic into the new `converter.py` module. ✅ COMPLETED
- [x] **7. Test Suite Update:** Update all relevant unit and integration tests to reflect the pipeline changes. ✅ COMPLETED
- [x] **8. Documentation Update:** Update all user and developer documentation to reflect the new architecture. ✅ COMPLETED

## ✅ IMPLEMENTATION STATUS: COMPLETE

The "JSON is King" refactoring has been successfully implemented with a reliability-first approach:

### 🎯 Key Achievements

1. **Single Format Pipeline**: Engine only accepts canonical JSON format - no backward compatibility bloat
2. **Strict Validation**: Comprehensive input validation with clear error messages for invalid formats
3. **Clean Architecture**: Eliminated all legacy code paths and deprecated methods
4. **Reliable Conversion**: Markdown to canonical JSON conversion working correctly
5. **Test Coverage**: All tests updated to use canonical format exclusively
6. **Format Standardization**: All master files and fixtures converted to canonical format

---

## 1. The Canonical JSON Presentation Model

This is the single, authoritative structure that the rendering engine will operate on. All inputs must be converted to this format.

```json
{
  "slides": [
    {
      "layout": "Title Slide",
      "style": "default_style",
      "placeholders": {
        "title": "This is the Title",
        "subtitle": "This is the subtitle"
      },
      "content": [
        {
          "type": "heading",
          "level": 1,
          "text": "A Formatted **Heading**"
        },
        {
          "type": "paragraph",
          "text": "This is a paragraph with *italic* and ___underline___."
        },
        {
          "type": "bullets",
          "items": [
            { "level": 1, "text": "First bullet" },
            { "level": 2, "text": "Second-level bullet" }
          ]
        },
        {
          "type": "table",
          "style": "dark_blue_white_text",
          "border_style": "thin_gray",
          "header": ["Header 1", "Header 2"],
          "rows": [
            ["Cell 1.1", "Cell 1.2"],
            ["Cell 2.1", "Cell 2.2"]
          ]
        },
        {
          "type": "image",
          "path": "path/to/image.png",
          "caption": "An image caption",
          "alt_text": "Accessibility text"
        }
      ]
    }
  ]
}
```

**Key Design Points:**

-   **`slides` array:** The root object contains a single `slides` array.
-   **`layout`:** A mandatory string specifying the slide layout from the template.
-   **`placeholders`:** A key-value map for direct placeholder replacement (e.g., `title`, `subtitle`, `body`). This is for simple content.
-   **`content` array:** A structured list of content blocks for the main content area of a slide. This allows for rich, mixed content.
-   **Explicit `type` in content blocks:** Each object in the `content` array has a `type` (`heading`, `paragraph`, `bullets`, `table`, `image`) to remove ambiguity.
-   **Inline Formatting:** All `text` fields throughout the model are strings that will be processed by the existing `content_formatting.py` module to handle `**bold**`, `*italic*`, etc.

---

## 2. File-by-File Implementation Plan

### A. New File: `src/deckbuilder/converter.py`

This new module will contain all logic for converting legacy formats into the canonical JSON model.

**Responsibilities:**

1.  Parse Markdown files with YAML frontmatter.
2.  Transform the parsed data into the canonical JSON structure.
3.  Incorporate the logic from `structured_frontmatter.py`.

**Proposed Content:**

```python
import yaml
from typing import Dict, Any, List

# Logic from structured_frontmatter.py will be moved here
# to convert things like `columns` into placeholder mappings.
from .structured_frontmatter import FrontmatterConverter 

def markdown_to_canonical_json(markdown_content: str) -> Dict[str, Any]:
    """
    Converts a Markdown string with frontmatter into the canonical JSON presentation model.
    This will be the single entry point for all .md files.
    """
    # 1. Split content into slides using "---"
    slides_raw = markdown_content.split('\n---\n')
    
    canonical_slides = []
    
    for slide_raw in slides_raw:
        if not slide_raw.strip():
            continue

        # 2. Parse Frontmatter (YAML) and Markdown Body
        parts = slide_raw.split('\n', 1)
        frontmatter_raw = parts[0]
        body_raw = parts[1] if len(parts) > 1 else ''
        
        frontmatter = yaml.safe_load(frontmatter_raw)
        
        # 3. Initialize Canonical Slide Object
        slide_obj = {
            "layout": frontmatter.get("layout", "Title and Content"),
            "style": frontmatter.get("style", "default_style"),
            "placeholders": {},
            "content": []
        }

        # 4. Use FrontmatterConverter to handle structured frontmatter
        # This integrates the logic from the old module.
        converter = FrontmatterConverter()
        placeholder_mappings = converter.convert_structured_to_placeholders(frontmatter)
        slide_obj["placeholders"] = placeholder_mappings

        # 5. Parse the Markdown body into structured content blocks
        # This logic will need to be robust, identifying headings, lists, tables, etc.
        # and converting them into the structured `content` array.
        # e.g., lines starting with '#' become 'heading' objects.
        # e.g., lines starting with '-' become 'bullets' objects.
        
        # ... parsing logic for body_raw ...

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}

```

### B. Refactor: `src/deckbuilder/cli.py`

The CLI will be simplified. It will perform the conversion step first, then pass the resulting JSON to the engine.

**Changes:**

-   In the `create` command function:
    -   Check the input file extension.
    -   If `.md`, call `converter.markdown_to_canonical_json()`.
    -   If `.json`, load the file and validate it against the canonical model.
    -   The call to `engine.create_presentation()` will **always** pass the canonical JSON data, never a file path.

**Example Snippet (`cli.py`):**

```python
# ... imports ...
from . import converter
from .engine import DeckbuilderEngine

# ... in main handler for the 'create' command ...

input_path = Path(args.input_file)
output_file = args.output or input_path.stem

if input_path.suffix.lower() == ".md":
    markdown_content = input_path.read_text(encoding="utf-8")
    presentation_data = converter.markdown_to_canonical_json(markdown_content)
elif input_path.suffix.lower() == ".json":
    with open(input_path, "r", encoding="utf-8") as f:
        presentation_data = json.load(f)
    # Optionally, add a validation step here against the canonical schema
else:
    # error out

# The engine is now only called with the canonical data model
engine = DeckbuilderEngine(template_name=args.template)
presentation = engine.create_presentation(presentation_data)
# ... save presentation ...
```

### C. Refactor: `src/deckbuilder/engine.py`

This is the most critical refactoring. The engine will be dramatically simplified.

**Changes:**

-   **Remove `parse_markdown_with_frontmatter()`:** This entire function and its helpers (`_parse_slide_content`, `_parse_rich_content`, etc.) are deleted. Their logic is now in `converter.py`.
-   **Remove `_parse_structured_frontmatter()`:** This is also moved to the converter.
-   **Remove `_auto_parse_json_formatting()`:** This becomes redundant as the new model is explicit. Inline formatting is handled at a lower level on all `text` fields.
-   **Modify `create_presentation()`:**
    -   It will now accept a single argument: `presentation_data: Dict[str, Any]`.
    -   The main loop will iterate through `presentation_data['slides']`.
    -   For each slide, it will call `_add_slide` with the slide object.
-   **Modify `_add_slide()`:**
    -   This function will be simplified. It receives a single canonical slide object.
    -   It will find the layout, then iterate through the `placeholders` and `content` arrays to populate the slide, calling the appropriate `python-pptx` methods.

**Example Snippet (`engine.py`):**

```python
class DeckbuilderEngine:
    # ... __init__ ...

    def create_presentation(self, presentation_data: Dict[str, Any]) -> Presentation:
        """
        Creates a presentation from the canonical JSON data model.
        """
        # No more file reading or format sniffing.
        
        for slide_data in presentation_data.get("slides", []):
            self._add_slide(slide_data)
            
        return self.prs

    def _add_slide(self, slide_data: Dict[str, Any]):
        """
        Adds a single slide based on the canonical slide object.
        """
        layout_name = slide_data.get("layout")
        slide_layout = self._get_layout(layout_name)
        slide = self.prs.slides.add_slide(slide_layout)

        # 1. Process direct placeholders
        for placeholder_name, text in slide_data.get("placeholders", {}).items():
            # ... logic to find and fill placeholder ...
            # ... apply inline formatting to 'text' ...

        # 2. Process structured content blocks
        for content_block in slide_data.get("content", []):
            if content_block["type"] == "heading":
                # ... add heading to slide body ...
            elif content_block["type"] == "paragraph":
                # ... add paragraph to slide body ...
            # ... etc. for all content types ...

```

### D. Refactor: `src/deckbuilder/structured_frontmatter.py`

-   The core conversion logic (`convert_structured_to_placeholders`) will be moved into `converter.py` to be used during the Markdown parsing process.
-   This file can then be deprecated and removed, or kept as a utility module imported by the converter. The latter is recommended initially to minimize code churn.

This refactoring creates a clear, linear, and robust pipeline. It isolates the complexity of format conversion to a single, dedicated module, allowing the core rendering engine to be simple, predictable, and focused on its one true task: building a presentation from a well-defined JSON structure.

---

## 3. Testing Strategy

### A. E2E Golden File Tests (`tests/deckbuilder/e2e/test_golden_file_validation.py`)

This test suite is the most critical for ensuring the refactor does not introduce regressions.

**Required Changes:**

1.  **No Deletions:** The existing tests that run `deckbuilder create` on both `.md` and `.json` files are still valid and necessary, as the CLI will continue to support both input formats.

2.  **Strengthen Assertions:** The `test_markdown_and_json_produce_similar_content` test will be enhanced. Because the new pipeline guarantees that a Markdown file is converted to a canonical JSON object before rendering, the resulting PowerPoint files should be identical, not just "similar."
    -   **New Helper Function:** A `compare_presentations(prs1, prs2)` helper will be created to perform a deep comparison.
    -   **Assertions:**
        -   Slide count must be identical.
        -   For each slide, shape count must be identical.
        -   For each shape, compare text, dimensions, and font properties (bold, italic, etc.).

3.  **Create Canonical Golden File:** A new golden file, `tests/deckbuilder/fixtures/canonical_presentation.json`, will be created. This file will be the "source of truth" for the expected output.

4.  **New Test Case:** The `test_markdown_and_json_produce_similar_content` test will be renamed to `test_markdown_conversion_matches_canonical_json`. It will now perform the following steps:
    -   Generate a presentation from `test_presentation.md`.
    -   Generate a second presentation from the new `canonical_presentation.json`.
    -   Use the `compare_presentations` helper to assert that the two output files are identical.


### B. Unit Tests for Engine (`tests/deckbuilder/unit/test_engine.py`)

This test file will be rewritten to focus exclusively on the new engine's rendering logic.

**Required Changes:**

1.  **Complete Overhaul:** The existing tests, which focus on initialization and environment variables, will be deleted.

2.  **New Focus:** The new tests will unit-test the `_add_slide()` method in isolation.

3.  **Mocking:** The `python-pptx` library will be mocked to allow for inspecting the calls made to the presentation object without creating actual files.

4.  **New Test Structure:**
    -   Each test case will define a canonical slide JSON object.
    -   It will call `engine._add_slide()` with that object.
    -   It will then assert that the correct `python-pptx` methods were called with the expected arguments.

### C. Unit Tests for Converter (`tests/deckbuilder/unit/test_converter.py`)

The tests for the frontmatter conversion will be moved to a new test file for the converter.

**Required Changes:**

1.  **New Test File:** A new file, `tests/deckbuilder/unit/test_converter.py`, will be created.

2.  **Move and Adapt:** The tests from `tests/deckbuilder/unit/test_structured_frontmatter.py` will be moved here.

3.  **Expand Scope:** The tests will be expanded to test the entire `markdown_to_canonical_json()` function. They will take a full Markdown string as input and assert that the output is a correctly formed canonical JSON object.

4.  **Deprecate Old File:** The `tests/deckbuilder/unit/test_structured_frontmatter.py` file will be deleted after its tests have been moved.