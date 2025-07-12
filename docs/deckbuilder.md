# Deckbuilder Library v1.2.0

The Deckbuilder library is a powerful Python API for creating professional PowerPoint presentations from structured content. Enhanced in v1.2.0 with smart template recommendations and improved content processing.

## `Deckbuilder` Class

The `Deckbuilder` class is the main entry point for creating presentations. It is a singleton class that can be accessed using the `get_deckbuilder_client()` function.

### Methods

*   `create_presentation(presentation_data, fileName, templateName)`: Creates a presentation from a dictionary of presentation data.
*   `write_presentation(fileName)`: Writes the presentation to a file.

## `PresentationBuilder` Class

The `PresentationBuilder` class is responsible for orchestrating the creation of slides, placement of content, and formatting. It is used by the `Deckbuilder` class to build the presentation.

### Methods

*   `add_slide(prs, slide_data)`: Adds a slide to the presentation.
*   `clear_slides(prs)`: Clears all slides from the presentation.

## `SlideBuilder` Class

The `SlideBuilder` class is responsible for creating individual slides. It is used by the `PresentationBuilder` class to build the slides.

### Methods

*   `add_slide(prs, slide_data, content_formatter, image_placeholder_handler)`: Adds a slide to the presentation.

## `ContentFormatter` Class

The `ContentFormatter` class is responsible for formatting content for slides. It can handle simple text, lists, and rich content blocks with headings, paragraphs, and bullets.

### Methods

*   `add_simple_content_to_placeholder(placeholder, content)`: Adds content to a placeholder.
*   `apply_inline_formatting(text, paragraph)`: Applies inline formatting to a paragraph.

## `TableBuilder` Class

The `TableBuilder` class is responsible for creating and styling tables. It has predefined styles for headers, rows, and borders.

### Methods

*   `add_table_to_slide(slide, table_data)`: Adds a table to a slide.

## `ImageHandler` Class

The `ImageHandler` class is responsible for validating, processing, and managing image files. It can handle various image formats, resize images while preserving the aspect ratio, and cache processed images for better performance.

### Methods

*   `validate_image(image_path)`: Validates an image file.
*   `process_image(image_path, target_dimensions, quality)`: Processes and resizes an image.

## `ImagePlaceholderHandler` Class

The `ImagePlaceholderHandler` class is responsible for handling image insertion into PowerPoint picture placeholders. It uses an `ImageHandler` to process and validate images and a `PlaceKittenIntegration` to generate fallback images.

### Methods

*   `handle_image_placeholder(placeholder, field_name, field_value, slide_data)`: Handles image insertion into a placeholder.

## `TemplateManager` Class

The `TemplateManager` class is responsible for managing templates. It can check if a template exists, load layout mappings from JSON files, and prepare templates for use.

### Methods

*   `check_template_exists(template_name)`: Checks if a template exists.
*   `load_layout_mapping(template_name)`: Loads a layout mapping from a JSON file.
*   `prepare_template(template_name)`: Prepares a template for use.

## `PathManager` Class

The `PathManager` class is responsible for managing all file paths in a centralized location. It supports different contexts (CLI, MCP, library) and provides methods for getting the project root, assets path, template folder, output folder, and template name.

## `PlaceholderTypes` Module

The `placeholder_types` module defines semantic groupings of PowerPoint placeholder types for generic content placement. This allows the deckbuilder to work with any PowerPoint template by detecting placeholder types rather than relying on specific layout configurations.

## `StructuredFrontmatter` Module

The `structured_frontmatter` module provides a system for defining and converting structured frontmatter in markdown files to the canonical JSON format used by the `Deckbuilder` library.

## `Validation` Module

The `validation` module provides a system for validating the presentation generation process. It has methods for validating the markdown to JSON conversion, the JSON to template mapping, and the final PPTX output.
