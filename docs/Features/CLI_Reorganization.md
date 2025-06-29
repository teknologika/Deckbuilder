# CLI Reorganization: Clean Hierarchical Command Structure

## Overview

Transform the Deckbuilder CLI from a messy flat command structure to a clean, professional hierarchical system with comprehensive bash completion.

## Current Problem

### Current CLI State
```bash
usage: deckbuilder [-h] [-t PATH] [-o PATH] [-l LANG] [-f FONT] 
{create,analyze,validate,document,enhance,image,crop,remap,languages,config,templates,completion,init} ...

positional arguments:
  {create,analyze,validate,document,enhance,image,crop,remap,languages,config,templates,completion,init}
                        Available commands
```

**Issues:**
- ❌ Overwhelming: 13 top-level commands cluttering help output
- ❌ Unorganized: Related functions scattered across flat namespace
- ❌ Unprofessional: Doesn't match enterprise CLI standards
- ❌ Incomplete Completion: References non-existent bash completion file
- ❌ Poor Discoverability: Hard to find related functionality

## Proposed Solution

### New Clean Interface
```bash
usage: deckbuilder [options] <command> <subcommand> [<subcommand> ...] [parameters]

To see help text, you can run:
  deckbuilder help
  deckbuilder <command> help
  deckbuilder <command> <subcommand> help
```

## Command Structure Design

### Hierarchical Organization

#### Primary Commands
```
create      Generate presentations from markdown or JSON
template    Manage PowerPoint templates and mappings
image       Process and generate images with PlaceKitten
config      Configuration, setup, and system information
help        Show detailed help information
```

#### Complete Command Tree
```
deckbuilder create <file> [options]
  └── Generate presentations from markdown or JSON files

deckbuilder template <subcommand>
  ├── analyze <name> [--verbose]     # Analyze template structure
  ├── validate <name>                # Validate template and mappings
  ├── document <name> [--output]     # Generate template documentation
  ├── enhance <name> [options]       # Enhance template placeholders
  └── list                           # List available templates

deckbuilder image <subcommand>
  ├── generate <w> <h> [options]     # Generate PlaceKitten images
  └── crop <file> <w> <h> [options]  # Smart crop existing images

deckbuilder config <subcommand>
  ├── show                           # Show current configuration
  ├── languages                      # List supported languages
  ├── init [path]                    # Initialize template folder
  └── completion                     # Setup bash completion

deckbuilder help [command] [subcommand]
  └── Show contextual help information
```

## Command Mapping (Old → New)

| Current Command | New Command | Notes |
|----------------|-------------|-------|
| `create` | `create` | ✅ Keep as top-level (most used) |
| `analyze` | `template analyze` | 🔄 Grouped with template functions |
| `validate` | `template validate` | 🔄 Grouped with template functions |
| `document` | `template document` | 🔄 Grouped with template functions |
| `enhance` | `template enhance` | 🔄 Grouped with template functions |
| `templates` | `template list` | 🔄 Logical naming in template group |
| `image` | `image generate` | 🔄 Clarified as generation function |
| `crop` | `image crop` | 🔄 Grouped with image functions |
| `remap` | ❌ **REMOVED** | 🗑️ Redundant with global --language/--font |
| `languages` | `config languages` | 🔄 Part of configuration |
| `config` | `config show` | 🔄 Clarified as display function |
| `completion` | `config completion` | 🔄 Part of setup process |
| `init` | `config init` | 🔄 Part of setup process |

## Bash Completion Design

### Completion Script: `deckbuilder-completion.bash`

#### Multi-Level Completion Support
```bash
deckbuilder <TAB>                    # → create template image config help
deckbuilder template <TAB>           # → analyze validate document enhance list
deckbuilder config <TAB>             # → show languages init completion
deckbuilder create <TAB>             # → [file path completion]
deckbuilder template analyze <TAB>   # → [template name completion]
deckbuilder --language <TAB>         # → en-AU en-US es-ES fr-FR de-DE...
deckbuilder --font <TAB>             # → Arial Calibri "Times New Roman"...
```

#### Smart Context-Aware Completion
- **File Paths**: Complete `.md`, `.json`, `.pptx` files appropriately
- **Template Names**: Read from `DECK_TEMPLATE_FOLDER` or default locations
- **Language Codes**: Complete both locale codes (`en-AU`) and full names (`English (Australia)`)
- **Font Names**: Complete common system fonts and quoted font names with spaces

#### Installation Methods
1. **User Installation**: `~/.deckbuilder-completion.bash`
2. **System Installation**: `/etc/bash_completion.d/deckbuilder`
3. **Auto-Setup**: `deckbuilder config completion` generates and installs

## Help System Enhancement

### Contextual Help Design

#### Main Help (`deckbuilder help`)
```
usage: deckbuilder [options] <command> <subcommand> [parameters]

Deckbuilder CLI - Intelligent PowerPoint presentation generation

Commands:
  create                    Generate presentations from markdown or JSON
  template                  Manage PowerPoint templates and mappings
  image                     Process and generate images with PlaceKitten
  config                    Configuration, setup, and system information
  help                      Show detailed help for commands

Global Options:
  -t, --templates PATH      Template folder path
  -o, --output PATH         Output folder path  
  -l, --language LANG       Proofing language (en-AU, es-ES, etc.)
  -f, --font FONT           Default font family

Examples:
  deckbuilder create presentation.md
  deckbuilder template analyze default --verbose
  deckbuilder config languages
  deckbuilder help template

To see help for a specific command:
  deckbuilder help <command>
  deckbuilder <command> help
```

#### Command Help (`deckbuilder help template`)
```
Template management commands:

Usage: deckbuilder template <subcommand> [options]

Subcommands:
  analyze <name>           Analyze template structure and placeholders
  validate <name>          Validate template and JSON mappings
  document <name>          Generate comprehensive template documentation
  enhance <name>           Enhance template with corrected placeholders
  list                     List all available templates

Examples:
  deckbuilder template analyze default --verbose
  deckbuilder template validate default
  deckbuilder template document default --output docs.md
  deckbuilder template enhance default --no-backup
  deckbuilder template list

For detailed help on a subcommand:
  deckbuilder help template <subcommand>
```

## Implementation Strategy

### Phase 1: Argument Parser Restructuring

#### 1.1 Main Parser Modification
```python
def create_parser():
    parser = argparse.ArgumentParser(
        prog="deckbuilder",
        description="Deckbuilder CLI - Intelligent PowerPoint presentation generation",
        usage="deckbuilder [options] <command> <subcommand> [parameters]",
        add_help=False  # Custom help handling
    )
    # Add global arguments only
    # No subparser display in main help
```

#### 1.2 Hierarchical Subparsers
```python
# Create main command parsers
subparsers = parser.add_subparsers(dest="command")

# Create command with nested subparsers  
template_parser = subparsers.add_parser("template")
template_subs = template_parser.add_subparsers(dest="template_command")

# Add nested commands
template_subs.add_parser("analyze")
template_subs.add_parser("validate")
# etc.
```

#### 1.3 Custom Help System
```python
def handle_help_command(args):
    if args.help_command == "template":
        show_template_help()
    elif args.help_command == "image":
        show_image_help()
    # etc.
```

### Phase 2: Command Routing Update

#### 2.1 New Routing Logic
```python
def main():
    args = parser.parse_args()
    
    # Handle help command specially
    if args.command == "help":
        handle_help_command(args)
        return
    
    # Route hierarchical commands
    if args.command == "template":
        handle_template_command(args)
    elif args.command == "image":
        handle_image_command(args)
    # etc.
```

#### 2.2 Backward Compatibility Layer
```python
# Map old commands to new structure during transition
LEGACY_COMMAND_MAP = {
    "analyze": ("template", "analyze"),
    "validate": ("template", "validate"),
    "languages": ("config", "languages"),
    # etc.
}
```

### Phase 3: Bash Completion Implementation

#### 3.1 Completion Script Generation
```python
def generate_completion_script():
    """Generate comprehensive bash completion script"""
    return """
#!/bin/bash
_deckbuilder_completion() {
    local cur prev opts commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    if [[ ${COMP_CWORD} == 1 ]]; then
        commands="create template image config help"
        COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
        return 0
    fi
    
    # Template subcommands
    if [[ ${COMP_WORDS[1]} == "template" && ${COMP_CWORD} == 2 ]]; then
        commands="analyze validate document enhance list"
        COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
        return 0
    fi
    
    # Template name completion
    if [[ ${COMP_WORDS[1]} == "template" && ${COMP_CWORD} == 3 ]]; then
        local templates=$(deckbuilder template list 2>/dev/null | grep -v "^📋" | awk '{print $1}')
        COMPREPLY=($(compgen -W "${templates}" -- ${cur}))
        return 0
    fi
    
    # Language completion for --language flag
    if [[ ${prev} == "--language" || ${prev} == "-l" ]]; then
        local languages=$(deckbuilder config languages 2>/dev/null | grep -E "^  [a-z]{2}-[A-Z]{2}" | awk '{print $1}')
        COMPREPLY=($(compgen -W "${languages}" -- ${cur}))
        return 0
    fi
    
    # File completion for create command and file arguments
    if [[ ${COMP_WORDS[1]} == "create" || ${cur} == *.* ]]; then
        COMPREPLY=($(compgen -f -- ${cur}))
        return 0
    fi
}

complete -F _deckbuilder_completion deckbuilder
"""
```

#### 3.2 Installation Integration
```python
def install_completion():
    """Install bash completion to user's profile"""
    completion_script = generate_completion_script()
    completion_path = Path.home() / ".deckbuilder-completion.bash"
    completion_path.write_text(completion_script)
    
    # Add to bash profile if not already present
    bash_profile = Path.home() / ".bash_profile"
    source_line = f"source {completion_path}"
    # Add source line if not present
```

### Phase 4: Documentation Updates

#### 4.1 README.md Updates
- Update all CLI examples to use new command structure
- Add bash completion installation instructions
- Show before/after CLI examples

#### 4.2 Package Integration
```toml
# pyproject.toml updates
[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
deckbuilder = ["deckbuilder-completion.bash"]
```

## Testing Strategy

### Manual Testing Checklist
- [ ] All new commands work correctly
- [ ] Help system shows proper information at each level
- [ ] Bash completion works for all command levels
- [ ] File path completion works correctly
- [ ] Template name completion works
- [ ] Language code completion works
- [ ] Backward compatibility maintained during transition
- [ ] Global arguments work with all commands
- [ ] Error handling for invalid command combinations

### Automated Testing
```python
def test_command_structure():
    """Test new command structure"""
    # Test main commands
    assert "create" in get_available_commands()
    assert "template" in get_available_commands()
    
    # Test subcommands
    assert "analyze" in get_template_subcommands()
    assert "generate" in get_image_subcommands()
    
    # Test command routing
    result = run_command(["template", "list"])
    assert result.success
```

## Success Criteria

### User Experience
✅ **Clean Interface**: Help output shows only essential commands  
✅ **Intuitive Navigation**: Related commands grouped logically  
✅ **Professional Appearance**: Matches enterprise CLI standards  
✅ **Powerful Completion**: Full tab completion for all levels  
✅ **Discoverable**: Users can explore functionality naturally  

### Technical Requirements
✅ **Backward Compatibility**: Old commands still work during transition  
✅ **Comprehensive Completion**: All commands, options, and contexts  
✅ **Maintainable Code**: Clean parser structure for future additions  
✅ **Proper Documentation**: Updated README and help system  
✅ **Package Integration**: Completion script included in distribution  

### Performance
✅ **Fast Completion**: Sub-100ms completion response time  
✅ **Efficient Parsing**: No performance regression in command execution  
✅ **Minimal Dependencies**: No additional package requirements  

## Rollout Plan

### Phase 1: New Structure (Parallel)
- Implement new command structure alongside old commands
- Both `deckbuilder analyze` and `deckbuilder template analyze` work
- Users can gradually adopt new syntax

### Phase 2: Documentation Update
- Update all documentation to show new syntax
- Add deprecation notices for old commands
- Provide migration guide

### Phase 3: Deprecation (Future Release)
- Add deprecation warnings for old command syntax
- Encourage migration to new structure
- Maintain backward compatibility

### Phase 4: Cleanup (Major Version)
- Remove old command syntax in next major version
- Clean command structure only

## Implementation TODOs

### 🏗️ Core Implementation
- [ ] Refactor `create_parser()` for hierarchical structure
- [ ] Implement custom help system with contextual information
- [ ] Add command routing for new structure (`handle_template_command`, etc.)
- [ ] Create backward compatibility mapping for transition period
- [ ] Update all command handlers to work with new argument structure

### 📝 Bash Completion
- [ ] Create comprehensive `deckbuilder-completion.bash` script
- [ ] Implement multi-level command completion
- [ ] Add smart context-aware completion (files, templates, languages)
- [ ] Create installation function in CLI (`config completion`)
- [ ] Test completion in multiple bash environments

### 📚 Documentation
- [ ] Update `README.md` with new command examples
- [ ] Add bash completion installation instructions
- [ ] Update CLI help examples throughout codebase
- [ ] Create migration guide for existing users

### 🧪 Testing & Validation
- [ ] Test all new command combinations
- [ ] Verify bash completion works correctly
- [ ] Ensure backward compatibility during transition
- [ ] Performance testing for completion response times
- [ ] Cross-platform testing (macOS, Linux)

### 📦 Package & Distribution
- [ ] Include completion script in package distribution
- [ ] Update `pyproject.toml` for script inclusion
- [ ] Test installation and completion setup
- [ ] Verify global installation works with `uv tool install`

---

**Status**: 🟡 Design Complete - Ready for Implementation  
**Priority**: High - Significant UX improvement  
**Estimated Effort**: 2-3 development sessions  
**Dependencies**: None  
**Risks**: Low - Backward compatibility maintained  