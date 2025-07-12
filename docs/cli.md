# Command-Line Interface (CLI) v1.2.0

The Deckbuilder CLI provides a professional command-line interface for generating presentations, managing templates, and processing images. Enhanced in v1.2.0 with improved template management and better image processing.

## Usage

```bash
deckbuilder [options] <command> <subcommand> [parameters]
```

## Global Options

*   `-t`, `--template-folder PATH`: Template folder path (default: environment variable or current directory)
*   `-l`, `--language LANG`: Proofing language (e.g., `en-US`, `en-AU`)
*   `-f`, `--font FONT`: Default font family (e.g., `"Calibri"`, `"Arial"`)
*   `-h`, `--help`: Show help message
*   `-V`, `--version`: Show version information

## Commands

### `create`

Generate presentations from markdown or JSON files.

```bash
deckbuilder create <input_file> [--output <output_name>] [--template <template_name>]
```

*   `<input_file>`: Input markdown (`.md`) or JSON (`.json`) file.
*   `--output`, `-o <output_name>`: Output filename (without extension).
*   `--template`, `-t <template_name>`: Template name to use (default: `default`).

### `template`

Manage PowerPoint templates and mappings.

#### Subcommands

*   `analyze [<template>] [--verbose, -v]`: Analyze template structure and placeholders.
*   `validate [<template>]`: Validate template and JSON mappings.
*   `document [<template>] [--output <file>]`: Generate comprehensive template documentation.
*   `enhance [<template>] [--mapping <file>] [--no-backup] [--no-conventions]`: Enhance template with corrected placeholders.
*   `list`: List all available templates.

### `image`

Process and generate images with PlaceKitten.

#### Subcommands

*   `generate <width> <height> [--id <id>] [--filter <type>] [--output <file>]`: Generate PlaceKitten placeholder images.
*   `crop <input_file> <width> <height> [--save-steps] [--output <file>]`: Smart crop existing images.

### `config`

Configuration, setup, and system information.

#### Subcommands

*   `show`: Show current configuration.
*   `languages`: List supported languages.
*   `completion`: Setup bash completion.

### `remap`

Update language and font settings in existing PowerPoint presentations.

```bash
deckbuilder remap <input_file> [--language <lang>] [--font <font>] [--output <file>] [--no-backup]
```

*   `<input_file>`: Input PowerPoint (`.pptx`) file to update.
*   `--language`, `-l <lang>`: Language code to apply (e.g., `en-US`, `en-AU`, `es-ES`).
*   `--font`, `-f <font>`: Font family to apply (e.g., `Calibri`, `Arial`).
*   `--output`, `-o <file>`: Output file path (default: overwrite input).
*   `--no-backup`: Skip creating backup file.

### `init`

Initialize template folder with default files and provide setup guidance.

```bash
deckbuilder init [<path>]
```

*   `<path>`: Template folder path (default: `./templates`).

### `help`

Show detailed help information for commands.

```bash
deckbuilder help <command> [<subcommand>]
```
