#!/bin/bash
# Deckbuilder CLI Bash Completion Script
# Generated for hierarchical command structure
#
# Installation:
#   1. User installation: Copy to ~/.deckbuilder-completion.bash
#   2. Add to your .bash_profile: source ~/.deckbuilder-completion.bash
#   3. System installation: sudo cp deckbuilder-completion.bash /etc/bash_completion.d/deckbuilder
#   4. Auto-setup: deckbuilder config completion

_deckbuilder_completion() {
    local cur prev opts commands template_commands image_commands config_commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    if [[ ${COMP_CWORD} == 1 ]]; then
        commands="create template image config init help"
        COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
        return 0
    fi
    
    # Handle hierarchical subcommands
    case "${COMP_WORDS[1]}" in
        template)
            # Template subcommands
            if [[ ${COMP_CWORD} == 2 ]]; then
                template_commands="analyze validate document enhance list"
                COMPREPLY=($(compgen -W "${template_commands}" -- ${cur}))
                return 0
            fi
            
            # Template name completion for template subcommands
            if [[ ${COMP_CWORD} == 3 && "${COMP_WORDS[2]}" != "list" ]]; then
                # Try to get template names from deckbuilder
                local templates
                if command -v deckbuilder >/dev/null 2>&1; then
                    templates=$(deckbuilder template list 2>/dev/null | grep -E "^  •" | sed 's/^  • //')
                else
                    # Fallback to common template names
                    templates="default"
                fi
                COMPREPLY=($(compgen -W "${templates}" -- ${cur}))
                return 0
            fi
            ;;
            
        image)
            # Image subcommands
            if [[ ${COMP_CWORD} == 2 ]]; then
                image_commands="generate crop"
                COMPREPLY=($(compgen -W "${image_commands}" -- ${cur}))
                return 0
            fi
            
            # File completion for image crop
            if [[ ${COMP_CWORD} == 3 && "${COMP_WORDS[2]}" == "crop" ]]; then
                COMPREPLY=($(compgen -f -X "!*.@(jpg|jpeg|png|gif|bmp|tiff)" -- ${cur}))
                return 0
            fi
            ;;
            
        config)
            # Config subcommands
            if [[ ${COMP_CWORD} == 2 ]]; then
                config_commands="show languages completion"
                COMPREPLY=($(compgen -W "${config_commands}" -- ${cur}))
                return 0
            fi
            ;;
            
        create)
            # File completion for create command
            if [[ ${COMP_CWORD} == 2 ]]; then
                # Complete .md and .json files
                local files
                files=($(compgen -f -- ${cur}))
                COMPREPLY=()
                for file in "${files[@]}"; do
                    if [[ "$file" == *.md ]] || [[ "$file" == *.json ]]; then
                        COMPREPLY+=("$file")
                    fi
                done
                return 0
            fi
            ;;
            
        init)
            # Directory completion for init command
            if [[ ${COMP_CWORD} == 2 ]]; then
                COMPREPLY=($(compgen -d -- ${cur}))
                return 0
            fi
            ;;
            
        help)
            # Help command completion
            if [[ ${COMP_CWORD} == 2 ]]; then
                commands="create template image config init"
                COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
                return 0
            fi
            
            # Help subcommand completion
            if [[ ${COMP_CWORD} == 3 ]]; then
                case "${COMP_WORDS[2]}" in
                    template)
                        template_commands="analyze validate document enhance list"
                        COMPREPLY=($(compgen -W "${template_commands}" -- ${cur}))
                        return 0
                        ;;
                    image)
                        image_commands="generate crop"
                        COMPREPLY=($(compgen -W "${image_commands}" -- ${cur}))
                        return 0
                        ;;
                    config)
                        config_commands="show languages completion"
                        COMPREPLY=($(compgen -W "${config_commands}" -- ${cur}))
                        return 0
                        ;;
                esac
            fi
            ;;
    esac
    
    # Global flag completion
    case "${prev}" in
        --language|-l)
            # Language completion - try to get from deckbuilder
            local languages
            if command -v deckbuilder >/dev/null 2>&1; then
                languages=$(deckbuilder config languages 2>/dev/null | grep -E "^  [a-z]{2}-[A-Z]{2}" | awk '{print $1}')
            else
                # Fallback to common languages
                languages="en-AU en-US es-ES fr-FR de-DE pt-BR it-IT ja-JP ko-KR zh-CN"
            fi
            COMPREPLY=($(compgen -W "${languages}" -- ${cur}))
            return 0
            ;;
            
        --font|-f)
            # Font completion - common system fonts
            local fonts="Arial Calibri Helvetica Times\ New\ Roman Georgia Verdana Trebuchet\ MS"
            COMPREPLY=($(compgen -W "${fonts}" -- ${cur}))
            return 0
            ;;
            
        --templates|-t)
            # Directory completion for templates folder
            COMPREPLY=($(compgen -d -- ${cur}))
            return 0
            ;;
            
        --output|-o)
            # For most commands, this is a directory or filename
            case "${COMP_WORDS[1]}" in
                create)
                    # For create, it's just a filename without extension
                    COMPREPLY=($(compgen -f -- ${cur}))
                    return 0
                    ;;
                template)
                    if [[ "${COMP_WORDS[2]}" == "document" ]]; then
                        # For template document, it's a markdown file
                        COMPREPLY=($(compgen -f -X "!*.md" -- ${cur}))
                        return 0
                    fi
                    ;;
                image)
                    # For image commands, it's an image file
                    COMPREPLY=($(compgen -f -X "!*.@(jpg|jpeg|png|gif|bmp)" -- ${cur}))
                    return 0
                    ;;
                *)
                    # General directory completion
                    COMPREPLY=($(compgen -d -- ${cur}))
                    return 0
                    ;;
            esac
            ;;
            
        --filter)
            # Filter completion for image commands
            local filters="grayscale sepia blur invert brightness contrast pixelate saturation sharpness"
            COMPREPLY=($(compgen -W "${filters}" -- ${cur}))
            return 0
            ;;
            
        --id)
            # Kitten image ID completion (1-6)
            COMPREPLY=($(compgen -W "1 2 3 4 5 6" -- ${cur}))
            return 0
            ;;
    esac
    
    # General file completion for remaining cases
    if [[ ${cur} == *.* ]]; then
        COMPREPLY=($(compgen -f -- ${cur}))
        return 0
    fi
    
    # Flag completion
    local flags="--help -h --templates -t --output -o --language -l --font -f"
    COMPREPLY=($(compgen -W "${flags}" -- ${cur}))
    return 0
}

# Register the completion function
complete -F _deckbuilder_completion deckbuilder

# Also register for common alternative names
complete -F _deckbuilder_completion deck
complete -F _deckbuilder_completion db

# Enable bash completion features if available
if [[ -n ${BASH_COMPLETION_VERSINFO} ]]; then
    # Use enhanced completion features if bash-completion is available
    shopt -s progcomp
fi