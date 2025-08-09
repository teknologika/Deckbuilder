# Code Review Implementation Design

This document outlines the detailed design and implementation plan for the changes recommended in the code review. Each section corresponds to a recommendation from the original review.

## 1. Consolidate Formatting Logic

**Problem:** The formatting logic is split between `src/deckbuilder/content_formatting.py` and `src/deckbuilder/content/formatter.py`, leading to redundancy and potential inconsistencies.

**Proposed Solution:** All formatting-related code will be consolidated into `src/deckbuilder/content/formatter.py`. The `src/deckbuilder/content_formatting.py` file will be deleted.

**Implementation Steps:**

1.  **Merge `ContentFormatter` classes:**
    *   Copy any unique methods from the `ContentFormatter` class in `content_formatting.py` to the class in `content/formatter.py`.
    *   Ensure the `ContentFormatter` class in `content/formatter.py` contains the superset of all functionality.
2.  **Update Imports:**
    *   Search the entire codebase for imports from `deckbuilder.content_formatting`.
    *   Replace these imports with `from deckbuilder.content.formatter import ContentFormatter`.
3.  **Delete `content_formatting.py`:**
    *   Remove the file `src/deckbuilder/content_formatting.py` from the project.

**Impact:** This change will centralize the formatting logic, making it easier to maintain and update. All modules that previously imported from `content_formatting` will need to be updated.

## 2. Consolidate Frontmatter Processing

**Problem:** Frontmatter processing logic is duplicated across `src/deckbuilder/structured_frontmatter.py` and `src/deckbuilder/content/frontmatter.py`.

**Proposed Solution:** The functionality of `structured_frontmatter.py` will be merged into `content/frontmatter.py`. The `structured_frontmatter.py` file will then be removed.

**Implementation Steps:**

1.  **Merge Classes:**
    *   Move the `StructuredFrontmatterRegistry`, `StructuredFrontmatterConverter`, and `StructuredFrontmatterValidator` classes from `structured_frontmatter.py` to `content/frontmatter.py`.
2.  **Update Imports:**
    *   Search for any imports from `deckbuilder.structured_frontmatter` and update them to `deckbuilder.content.frontmatter`.
3.  **Delete `structured_frontmatter.py`:**
    *   Remove the file `src/deckbuilder/structured_frontmatter.py`.

**Impact:** This will create a single, authoritative source for all frontmatter-related logic, improving code clarity and maintainability.

## 3. Centralize `parse_inline_formatting`

**Problem:** The `parse_inline_formatting` method is duplicated in multiple files.

**Proposed Solution:** This method will be located exclusively in the consolidated `src/deckbuilder/content/formatter.py` module.

**Implementation Steps:**

1.  **Remove Duplicates:**
    *   Delete the `parse_inline_formatting` method from `src/deckbuilder/content/processor.py` and any other files where it is duplicated.
2.  **Update Calls:**
    *   In the files where the method was removed, import it from the new location: `from deckbuilder.content.formatter import ContentFormatter`.
    *   Create an instance of the `ContentFormatter` and call the method from that instance.

**Impact:** This change enforces the DRY principle, reducing code duplication and making the formatting logic easier to manage.

## 4. Refactor CLI Command Handling

**Problem:** The `cli.py` module uses a complex and hard-to-maintain system for command handling.

**Proposed Solution:** Refactor the CLI using the `click` library to simplify command creation and argument parsing.

**Implementation Steps:**

1.  **Add `click` Dependency:**
    *   Add `click` to the project's `requirements.txt` or `pyproject.toml`.
2.  **Refactor `cli.py`:**
    *   Rewrite the command structure using `click` decorators (`@click.group()`, `@click.command()`, `@click.option()`, `@click.argument()`).
    *   Replace the manual argument parsing and help handling with `click`'s automatic functionality.

**Impact:** The CLI will be more robust, easier to extend, and the code will be significantly cleaner and more readable.

## 5. Refactor `slide_builder.py`

**Problem:** The `_add_content_to_placeholders_fallback` and `_apply_content_by_semantic_type` methods in `slide_builder.py` have overlapping responsibilities.

**Proposed Solution:** Unify these two methods into a single, more flexible method that can handle both standard and fallback content application.

**Implementation Steps:**

1.  **Create a Unified Method:**
    *   Create a new private method, for example, `_apply_content_to_placeholder`.
    *   This method will take the placeholder and content as arguments and will contain the logic to handle different content types and placeholder types.
2.  **Refactor Existing Methods:**
    *   Update `_apply_content_to_mapped_placeholders` to call the new unified method.
    *   Remove the old `_add_content_to_placeholders_fallback` and `_apply_content_by_semantic_type` methods.

**Impact:** This refactoring will reduce code duplication within the `SlideBuilder` class, making the content application logic more streamlined and easier to debug.