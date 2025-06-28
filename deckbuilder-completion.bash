#!/bin/bash
# Bash completion script for deckbuilder CLI
# 
# Installation:
#   1. Download this file to ~/.deckbuilder-completion.bash
#   2. Add to your .bash_profile: source ~/.deckbuilder-completion.bash
#   3. Reload: source ~/.bash_profile
#
# Or install system-wide:
#   sudo cp deckbuilder-completion.bash /etc/bash_completion.d/deckbuilder

_deckbuilder_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    local commands="create analyze validate document enhance image crop config templates init"
    
    # Global options
    local global_opts="-t --templates -o --output -h --help --version"
    
    # Command-specific options
    local create_opts="--output --template"
    local analyze_opts="--verbose"
    local document_opts="--output"
    local enhance_opts="--mapping --no-backup --no-conventions"
    local image_opts="--id --filter --output"
    local crop_opts="--save-steps --output"
    
    # Filter types for image command
    local filters="grayscale sepia blur invert brightness contrast pixelate saturation sharpness"
    
    # Get available templates from templates folder
    _get_templates() {
        local template_folder
        
        # Check for -t/--templates argument in current command
        for ((i=1; i<COMP_CWORD; i++)); do
            if [[ "${COMP_WORDS[i]}" == "-t" || "${COMP_WORDS[i]}" == "--templates" ]]; then
                template_folder="${COMP_WORDS[i+1]}"
                break
            fi
        done
        
        # Fall back to environment variable or default
        if [[ -z "$template_folder" ]]; then
            template_folder="${DECK_TEMPLATE_FOLDER:-./templates}"
        fi
        
        # List .pptx files without extension
        if [[ -d "$template_folder" ]]; then
            find "$template_folder" -name "*.pptx" -exec basename {} .pptx \; 2>/dev/null
        fi
    }
    
    # Complete file paths for specific contexts
    _complete_files() {
        case "$1" in
            "md_json")
                # Markdown and JSON files
                COMPREPLY=($(compgen -f -X "!*.@(md|json)" -- "$cur"))
                ;;
            "images")
                # Image files
                COMPREPLY=($(compgen -f -X "!*.@(jpg|jpeg|png|gif|bmp|tiff)" -- "$cur"))
                ;;
            "directories")
                # Directories only
                COMPREPLY=($(compgen -d -- "$cur"))
                ;;
            *)
                # All files
                COMPREPLY=($(compgen -f -- "$cur"))
                ;;
        esac
    }
    
    # Main completion logic
    case $COMP_CWORD in
        1)
            # First argument: complete commands and global options
            COMPREPLY=($(compgen -W "$commands $global_opts" -- "$cur"))
            ;;
        *)
            # Find the main command (skip global options)
            local command=""
            local i=1
            while [[ $i -lt $COMP_CWORD ]]; do
                local word="${COMP_WORDS[i]}"
                if [[ "$commands" =~ $word ]]; then
                    command="$word"
                    break
                elif [[ "$word" == "-t" || "$word" == "--templates" || "$word" == "-o" || "$word" == "--output" ]]; then
                    # Skip global option and its value
                    ((i++))
                fi
                ((i++))
            done
            
            # Complete based on previous word and command context
            case "$prev" in
                # Global options
                "-t"|"--templates")
                    _complete_files "directories"
                    ;;
                "-o"|"--output")
                    if [[ "$command" == "create" || "$command" == "document" || "$command" == "image" || "$command" == "crop" ]]; then
                        # For output files, complete directories and files
                        _complete_files
                    else
                        _complete_files "directories"
                    fi
                    ;;
                    
                # Command-specific options
                "--template")
                    COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                    ;;
                "--filter")
                    COMPREPLY=($(compgen -W "$filters" -- "$cur"))
                    ;;
                "--mapping")
                    COMPREPLY=($(compgen -f -X "!*.json" -- "$cur"))
                    ;;
                    
                # Commands that expect specific file types
                "create")
                    _complete_files "md_json"
                    ;;
                "crop")
                    _complete_files "images"
                    ;;
                    
                # Template commands that expect template names
                "analyze"|"validate"|"document"|"enhance")
                    COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                    ;;
                    
                # Init command expects directory path
                "init")
                    _complete_files "directories"
                    ;;
                    
                *)
                    # Complete based on command context
                    case "$command" in
                        "create")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$create_opts" -- "$cur"))
                            else
                                _complete_files "md_json"
                            fi
                            ;;
                        "analyze")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$analyze_opts" -- "$cur"))
                            else
                                COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                            fi
                            ;;
                        "validate")
                            COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                            ;;
                        "document")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$document_opts" -- "$cur"))
                            else
                                COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                            fi
                            ;;
                        "enhance")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$enhance_opts" -- "$cur"))
                            else
                                COMPREPLY=($(compgen -W "$(_get_templates)" -- "$cur"))
                            fi
                            ;;
                        "image")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$image_opts" -- "$cur"))
                            else
                                # Complete numbers for width/height or nothing
                                COMPREPLY=()
                            fi
                            ;;
                        "crop")
                            if [[ "$cur" == -* ]]; then
                                COMPREPLY=($(compgen -W "$crop_opts" -- "$cur"))
                            else
                                # First argument should be image file
                                local arg_count=0
                                for ((i=1; i<COMP_CWORD; i++)); do
                                    if [[ "${COMP_WORDS[i]}" == "$command" ]]; then
                                        arg_count=$((COMP_CWORD - i - 1))
                                        break
                                    fi
                                done
                                
                                if [[ $arg_count -eq 1 ]]; then
                                    _complete_files "images"
                                else
                                    # Width/height arguments - no completion
                                    COMPREPLY=()
                                fi
                            fi
                            ;;
                        "init")
                            _complete_files "directories"
                            ;;
                        *)
                            # No command found, complete commands and global options
                            COMPREPLY=($(compgen -W "$commands $global_opts" -- "$cur"))
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
    
    # Handle directory completion properly
    if [[ ${#COMPREPLY[@]} -eq 1 && -d "${COMPREPLY[0]}" ]]; then
        # Add trailing slash for directories
        COMPREPLY[0]="${COMPREPLY[0]}/"
    fi
    
    return 0
}

# Register the completion function
complete -F _deckbuilder_completion deckbuilder

# Also register for python module execution
complete -F _deckbuilder_completion "python -m deckbuilder.cli"
complete -F _deckbuilder_completion "python3 -m deckbuilder.cli"