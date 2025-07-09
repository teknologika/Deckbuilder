# Deckbuilder CLI Design Specification

## Overview

The Deckbuilder CLI provides a standalone command-line interface for presentation generation, template management, and image processing. Unlike the MCP server which relies on environment variables for configuration, the CLI should be user-friendly with sensible defaults and clear setup guidance.

## Design Philosophy

### CLI vs MCP Server Differences

**MCP Server Approach:**
- Environment variables are required (`DECK_TEMPLATE_FOLDER`, `DECK_OUTPUT_FOLDER`)
- Server assumes proper configuration by Claude Desktop
- Works in controlled environment with known paths

**CLI Approach:**
- Environment variables are optional convenience
- Sensible defaults for local development
- Clear error messages with actionable solutions
- Self-contained setup commands

## Environment Resolution Logic

### Template Folder Resolution Priority

1. **CLI Argument** (`--template-folder PATH`) - Highest priority
   ```bash
   deckbuilder --template-folder ~/my-templates create slides.md
   ```

2. **Environment Variable** (`DECK_TEMPLATE_FOLDER`) - If set
   ```bash
   export DECK_TEMPLATE_FOLDER="/home/user/templates"
   ```

3. **Default Location** (`./templates/`) - Current directory fallback
   ```bash
   # Looks for templates in current directory
   deckbuilder create slides.md
   ```

4. **Error with Guidance** - If templates folder not found
   ```bash
   ❌ Template folder not found: ./templates/
   💡 Run 'deckbuilder init' to create template folder and copy default files
   ```

### Output Folder Resolution Priority

**CLI Context: Always outputs to current directory for predictable local development**

1. **Current Directory** (`.`) - CLI always uses current directory
   ```bash
   # Always saves in current directory for local development workflow
   deckbuilder create slides.md
   ```

2. **Context-Aware Behavior** - Different contexts have different precedence rules:
   - **CLI Context**: Always current directory (overrides env vars)
   - **MCP Context**: Environment variables required, no fallbacks
   - **Library Context**: Constructor args > env vars > current directory

## Command Structure

### Global Arguments (Apply to All Commands)

```bash
deckbuilder [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]

Global Options:
  --template-folder PATH    Template folder path (overrides env vars)
  -l, --language LANG      Proofing language (e.g., "en-AU" or "English (Australia)")
  -f, --font FONT          Default font family (e.g., "Arial", "Times New Roman")
  -h, --help              Show help message
  --version               Show version
```

### Context-Aware Architecture

**CLI Context Behavior:**
- Template folder: CLI args > env vars > current directory
- Output folder: Always current directory (predictable local development)
- Language/Font: CLI args > env vars > defaults

```bash
# Use custom template folder (CLI arg overrides env vars)
deckbuilder --template-folder ~/templates create slides.md

# Set language and font globally
deckbuilder --language "es-ES" --font "Arial" create slides.md

# Always outputs to current directory for local development
deckbuilder create slides.md  # outputs to ./presentation_name.pptx
```

## Init Command Specification

### Basic Usage

```bash
# Create templates in ./templates/ (default)
deckbuilder init

# Create templates in custom location
deckbuilder init ~/my-templates/

# Create templates in specific path
deckbuilder init /absolute/path/to/templates/
```

### Init Command Behavior

1. **Create folder structure** if it doesn't exist
2. **Copy default assets** from package:
   - `default.pptx` - PowerPoint template
   - `default.json` - Layout mappings
3. **Provide environment variable guidance**
4. **Confirm successful setup**

### Init Command Output Example

```bash
$ deckbuilder init
✅ Template folder created at ./templates/
📁 Copied: default.pptx, default.json

💡 To make this permanent, add to your .bash_profile:
export DECK_TEMPLATE_FOLDER="/Users/username/current-project/templates"
export DECK_OUTPUT_FOLDER="/Users/username/current-project"
export DECK_TEMPLATE_NAME="default"

Then reload: source ~/.bash_profile

🚀 Ready to use! Try: deckbuilder create example.md
```

### Init with Custom Path

```bash
$ deckbuilder init ~/my-project/templates/
✅ Template folder created at /Users/username/my-project/templates/
📁 Copied: default.pptx, default.json

💡 To make this permanent, add to your .bash_profile:
export DECK_TEMPLATE_FOLDER="/Users/username/my-project/templates"
export DECK_OUTPUT_FOLDER="/Users/username/my-project"
export DECK_TEMPLATE_NAME="default"

Then reload: source ~/.bash_profile
```

## Tab Completion Support

### Implementation Approach

Create `deckbuilder-completion.bash` script that provides:

1. **Command completion** - All available commands
2. **Template name completion** - Dynamic from templates folder
3. **File path completion** - Native bash file completion
4. **Flag completion** - Available options for each command

### Completion Script Features

```bash
# Complete commands
deckbuilder <TAB>
create  init  analyze  validate  document  enhance  image  crop  config  templates

# Complete template names
deckbuilder analyze <TAB>
default  custom  presentation-template

# Complete file paths
deckbuilder create <TAB>
slides.md  presentation.json  examples/

# Complete global flags
deckbuilder -<TAB>
-t  --templates  -o  --output  -h  --help  --version
```

### Installation Instructions

```bash
# Download completion script
curl -o ~/.deckbuilder-completion.bash https://raw.githubusercontent.com/teknologika/deckbuilder/main/deckbuilder-completion.bash

# Add to .bash_profile
echo "source ~/.deckbuilder-completion.bash" >> ~/.bash_profile

# Reload shell
source ~/.bash_profile
```

## Error Handling Improvements

### Template-Related Errors

**Missing Templates Folder:**
```bash
❌ Template folder not found: ./templates/
💡 Run 'deckbuilder init' to create template folder and copy default files
```

**Missing Specific Template:**
```bash
❌ Template not found: custom.pptx
📋 Available templates:
  • default
  • presentation-template
  • business-slides
💡 Use 'deckbuilder templates' to list all available templates
```

**Empty Templates Folder:**
```bash
❌ No templates found in ./templates/
💡 Run 'deckbuilder init .' to copy default template files
```

### Input File Errors

**Missing Input File:**
```bash
❌ Input file not found: slides.md
💡 Check file path or create the file first
```

**Unsupported Format:**
```bash
❌ Unsupported file format: .txt
💡 Supported formats: .md (markdown), .json (JSON)
```

### Permission Errors

**Cannot Create Output:**
```bash
❌ Permission denied: Cannot write to /restricted/path/
💡 Use -o flag to specify a writable output directory
```

## Command Examples

### Basic Usage

```bash
# Initialize templates in current directory
deckbuilder init

# Create presentation from markdown (outputs to current directory)
deckbuilder create slides.md

# Create with custom output name (still in current directory)
deckbuilder create slides.md --output "My_Presentation"

# Use different template folder
deckbuilder --template-folder ~/my-templates create slides.md

# Set language and font
deckbuilder --language "fr-CA" --font "Times New Roman" create slides.md
```

### Advanced Usage

```bash
# Use custom template folder with language/font settings
deckbuilder --template-folder ~/templates --language "es-ES" --font "Arial" create slides.md

# Template management
deckbuilder template analyze default --verbose
deckbuilder template validate business-slides
deckbuilder template document default

# Image generation
deckbuilder image generate 1920 1080 --filter grayscale
```

### Configuration and Info

```bash
# Show current configuration (shows path sources and current settings)
deckbuilder config show

# List all supported languages
deckbuilder config languages

# List available templates
deckbuilder template list

# Show help for specific command
deckbuilder create --help
```

## Context-Aware Path Management (✅ COMPLETED)

### Three Context Types
The Deckbuilder architecture now supports three distinct contexts with different path resolution behaviors:

1. **CLI Context** - Local development focused
   - Template folder: CLI args > env vars > current directory
   - Output folder: Always current directory (predictable local workflow)
   - Language/Font: CLI args > env vars > defaults

2. **MCP Context** - Server environment focused  
   - Template folder: Environment variables required (no fallbacks)
   - Output folder: Environment variables required (no fallbacks)
   - Language/Font: Environment variables > defaults

3. **Library Context** - Programmatic usage focused
   - Template folder: Constructor args > env vars > current directory
   - Output folder: Constructor args > env vars > current directory
   - Language/Font: Constructor args > env vars > defaults

### Anti-Pattern Fixed
- ❌ **Before**: CLI set environment variables globally
- ✅ **After**: Each context uses appropriate path resolution without side effects

## Implementation Roadmap

### Phase 1: Core Logic Improvements ✅ COMPLETED
- [x] Update environment resolution priority logic
- [x] Implement context-aware path management
- [x] Add language and font support
- [x] Improve error messages with actionable suggestions

### Phase 2: Init Command
- [ ] Implement `deckbuilder init [PATH]` command
- [ ] Add template asset copying from package
- [ ] Generate environment variable suggestions
- [ ] Provide setup confirmation and next steps

### Phase 3: Tab Completion
- [ ] Create bash completion script
- [ ] Dynamic template name completion
- [ ] Command and flag completion
- [ ] Installation documentation

### Phase 4: Enhanced UX
- [ ] Add command aliases for common operations
- [ ] Improve output formatting and colors
- [ ] Add progress indicators for long operations
- [ ] Create getting started tutorial

## Success Criteria

### User Experience
- [ ] New users can get started with single `deckbuilder init` command
- [ ] Clear error messages guide users to solutions
- [ ] Tab completion works for commands, templates, and files
- [ ] No required environment variables for basic usage

### Technical Requirements
- [ ] Backward compatibility with existing CLI usage
- [ ] Environment variables still work (MCP server compatibility)
- [ ] Package assets accessible for copying to user directories
- [ ] Cross-platform support (macOS, Linux, Windows)

### Documentation
- [ ] Updated help text reflects new argument structure
- [ ] README includes quick start guide
- [ ] Environment variable setup clearly documented
- [ ] Tab completion installation instructions provided

## Architecture Integration

This CLI improvement integrates with the existing Deckbuilder architecture:

- **Presentation Engine**: CLI provides user-friendly interface to core engine
- **Template Management**: Simplified template discovery and validation
- **PlaceKitten Integration**: Enhanced image commands with clear options
- **MCP Server**: CLI and MCP server share core logic but different UX approaches

The CLI serves as the primary user-facing interface for local development, while the MCP server provides Claude Desktop integration with controlled environment assumptions.