# Proposed Folder Structure Design

This document outlines a new, more organized folder structure for the `src` directory. The goal of this redesign is to improve maintainability, scalability, and clarity of the codebase.

## Current Structure Issues

The current `src/deckbuilder` directory has a mix of modules at the top level and within a `content` subdirectory. This can be confusing for developers and makes it harder to locate specific functionality.

## Current Files in Root Directory

These files currently exist in `src/deckbuilder/` root and need to be organized:

- `__init__.py` - Package init (stays)
- `formatting_support.py` - Content formatting utilities
- `layout_analyzer.py` - Template layout analysis
- `layout_intelligence.py` - Layout recommendation intelligence  
- `naming_conventions.py` - CLI naming conventions
- `pattern_loader.py` - Template pattern loading
- `pattern_schema.py` - Pattern validation schemas
- `placeholder_types.py` - PowerPoint placeholder type constants
- `placekitten_integration.py` - Image placeholder integration
- `recommendation_engine.py` - Template recommendation engine
- `table_builder.py` - Table generation
- `table_styles.py` - Table styling
- `validation.py` - Presentation validation

## Proposed `src` Folder Structure

```
src/
├── deckbuilder/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands.py
│   │   └── naming_conventions.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── presentation_builder.py
│   │   ├── slide_builder.py
│   │   ├── table_builder.py
│   │   └── validation.py
│   ├── content/
│   │   ├── __init__.py
│   │   ├── formatter.py
│   │   ├── frontmatter.py
│   │   ├── processor.py
│   │   ├── formatting_support.py
│   │   └── placeholder_types.py
│   ├── image/
│   │   ├── __init__.py
│   │   ├── image_handler.py
│   │   ├── placeholder.py
│   │   └── placekitten_integration.py
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── metadata.py
│   │   ├── pattern_loader.py
│   │   ├── pattern_schema.py
│   │   ├── layout_analyzer.py
│   │   ├── layout_intelligence.py
│   │   ├── recommendation_engine.py
│   │   └── table_styles.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── path.py
├── mcp_server/
│   └── ...
└── placekitten/
    └── ...
```

### Rationale for the New Structure

*   **Clear Separation of Concerns:** The proposed structure groups modules by their primary function, making the codebase easier to navigate and understand.
    *   `cli/`: All command-line interface logic.
    *   `core/`: The main presentation generation engine.
    *   `content/`: All content processing, including formatting and frontmatter.
    *   `image/`: Image handling and placeholder logic.
    *   `templates/`: Template management and metadata.
    *   `utils/`: Shared utilities like logging and path management.
*   **Improved Discoverability:** It will be easier for new developers to find the code they are looking for.
*   **Reduced Complexity:** By breaking down the `deckbuilder` module into smaller, more focused sub-packages, the overall complexity of the system is reduced.
*   **Scalability:** This structure is more scalable, allowing for the addition of new features and modules without cluttering the main `deckbuilder` directory.

### Implementation Plan

1.  **Create New Directories:** Create the new subdirectories (`cli`, `core`, `image`, `templates`, `utils`) within `src/deckbuilder`.
2.  **Move Existing Files:**
    *   Move `cli.py` and `cli_tools.py` to `src/deckbuilder/cli/`.
    *   Move `engine.py`, `presentation_builder.py`, and `slide_builder.py` to `src/deckbuilder/core/`.
    *   Move `content_formatting.py`, `content_matcher.py`, `converter.py`, `structured_frontmatter.py`, and the existing `content` directory to `src/deckbuilder/content/`.
    *   Move `image_handler.py` and `image_placeholder_handler.py` to `src/deckbuilder/image/`.
    *   Move `template_manager.py` and `template_metadata.py` to `src/deckbuilder/templates/`.
    *   Move `logging_config.py` and `path_manager.py` to `src/deckbuilder/utils/`.
3.  **Update Imports:** Search the entire codebase and update all imports to reflect the new file locations.
4.  **Refactor `__init__.py` files:** Update the `__init__.py` files in each new subdirectory to expose the necessary classes and functions.
