#!/usr/bin/env python3
"""
Deckbuilder CLI - Standalone Command Line Interface

Complete command-line interface for Deckbuilder presentation generation,
template management, and PlaceKitten image processing. Designed for
local development and standalone usage without MCP server dependency.

Usage:
    deckbuilder create presentation.md
    deckbuilder analyze default
    deckbuilder generate-image 800 600 --filter grayscale
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Conditional imports for development vs installed package
try:
    # Try package imports first (for installed package)
    from deckbuilder.engine import Deckbuilder
    from deckbuilder.cli_tools import TemplateManager
    from deckbuilder.formatting_support import FormattingSupport, print_supported_languages
    from deckbuilder.path_manager import create_cli_path_manager
    from placekitten import PlaceKitten
except ImportError:
    # Fallback to development imports (when running from source)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    sys.path.insert(0, str(project_root))

    from src.deckbuilder.engine import Deckbuilder  # noqa: E402
    from src.deckbuilder.cli_tools import TemplateManager  # noqa: E402
    from src.deckbuilder.formatting_support import (
        FormattingSupport,
        print_supported_languages,
    )  # noqa: E402
    from src.deckbuilder.path_manager import create_cli_path_manager  # noqa: E402
    from src.placekitten import PlaceKitten  # noqa: E402


class DeckbuilderCLI:
    """Standalone Deckbuilder command-line interface"""

    def __init__(self, template_folder=None, language=None, font=None):
        """Initialize CLI with template folder for CLI context"""
        # Create CLI-specific path manager
        self.path_manager = create_cli_path_manager(template_folder=template_folder)
        self.language = language
        self.font = font

    def _validate_templates_folder(self):
        """Validate templates folder exists and provide helpful error message"""
        if not self.path_manager.validate_template_folder_exists():
            template_folder = self.path_manager.get_template_folder()
            print(f"❌ Template folder not found: {template_folder}")
            print("💡 Run 'deckbuilder init' to create template folder and copy default files")
            return False
        return True

    def _get_available_templates(self):
        """Get list of available templates with error handling"""
        template_folder = os.getenv("DECK_TEMPLATE_FOLDER")
        if not template_folder or not Path(template_folder).exists():
            return []

        template_path = Path(template_folder)
        return [template.stem for template in template_path.glob("*.pptx")]

    def create_presentation(self, input_file: str, output_name: Optional[str] = None, template: Optional[str] = None) -> str:
        """
        Create presentation from markdown or JSON file

        Args:
            input_file: Path to markdown (.md) or JSON (.json) input file
            output_name: Optional output filename (without extension)
            template: Optional template name to use

        Returns:
            str: Path to generated presentation file
        """
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            print("💡 Check file path or create the file first")
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Validate templates folder exists
        if not self._validate_templates_folder():
            return

        # Determine output filename
        if not output_name:
            output_name = input_path.stem

        # Use default template if none provided
        template_name = template or "default"

        # Show template selection feedback
        template_folder = self.path_manager.get_template_folder()
        template_file = self.path_manager.get_template_file_path(template_name)
        mapping_file = self.path_manager.get_template_json_path(template_name)

        print(f"Using template: {template_name}.pptx from {template_folder}")

        # Check if template files exist and report status
        if template_file.exists():
            print(f"Template file: {template_file.name} ✓ Found")
        else:
            print(f"✗ Template file not found: {template_file}")
            print("Run 'deckbuilder init' to create template folder with default files")
            return

        if mapping_file.exists():
            print(f"Mapping file: {mapping_file.name} ✓ Found")
        else:
            print(f"Mapping file not found: {mapping_file.name} (will use fallback detection)")

        # Reset singleton and create fresh instance with CLI path manager
        Deckbuilder.reset()
        db = Deckbuilder(path_manager_instance=self.path_manager)

        try:
            presentation_data = {}
            markdown_content = None

            if input_path.suffix.lower() == ".md":
                from deckbuilder import converter
                from deckbuilder.validation import PresentationValidator

                # Process markdown file
                markdown_content = input_path.read_text(encoding="utf-8")
                print(f"Processing markdown file: {input_path.name}")
                presentation_data = converter.markdown_to_canonical_json(markdown_content)

                # STEP 0: Validate Markdown → JSON conversion
                template_folder = str(self.path_manager.get_template_folder())
                validator = PresentationValidator(presentation_data, template_name, template_folder)
                validator.validate_markdown_to_json(markdown_content, presentation_data)
            elif input_path.suffix.lower() == ".json":
                # Process JSON file directly
                with open(input_path, "r", encoding="utf-8") as f:
                    presentation_data = json.load(f)
                print(f"Processing JSON file: {input_path.name}")
            else:
                raise ValueError(f"Unsupported file format: {input_path.suffix}. " "Supported formats: .md, .json")

            result = db.create_presentation(
                presentation_data,
                fileName=output_name,
                templateName=template_name,
            )

            # Check if result indicates an error
            if result and ("Error creating presentation from markdown:" in result or "Error creating presentation from JSON:" in result):
                print(f"✗ {result}")
                raise RuntimeError(result)
            print(f"✓ Presentation created successfully: {result}")
            return result

        except Exception as e:
            print(f"✗ Error creating presentation: {e}")
            raise

    def analyze_template(self, template_name: str = "default", verbose: bool = False):
        """Analyze PowerPoint template structure"""
        if not self._validate_templates_folder():
            return
        manager = TemplateManager()
        manager.analyze_template(template_name, verbose=verbose)

    def validate_template(self, template_name: str = "default"):
        """Validate template and mappings"""
        if not self._validate_templates_folder():
            return
        manager = TemplateManager()
        manager.validate_template(template_name)

    def document_template(self, template_name: str = "default", output_file: Optional[str] = None):
        """Generate comprehensive template documentation"""
        if not self._validate_templates_folder():
            return
        manager = TemplateManager()
        manager.document_template(template_name, output_file)

    def enhance_template(
        self,
        template_name: str = "default",
        mapping_file: Optional[str] = None,
        no_backup: bool = False,
        use_conventions: bool = True,
    ):
        """Enhance template with improved placeholder names"""
        if not self._validate_templates_folder():
            return
        manager = TemplateManager()
        create_backup = not no_backup
        manager.enhance_template(template_name, mapping_file, create_backup, use_conventions)

    def generate_placeholder_image(
        self,
        width: int,
        height: int,
        image_id: Optional[int] = None,
        filter_type: Optional[str] = None,
        output_file: Optional[str] = None,
    ):
        """Generate PlaceKitten placeholder image"""
        pk = PlaceKitten()

        try:
            # Set output filename
            if not output_file:
                filter_suffix = f"_{filter_type}" if filter_type else ""
                id_suffix = f"_id{image_id}" if image_id else ""
                output_file = f"placeholder_{width}x{height}{id_suffix}{filter_suffix}.jpg"

            # Generate image with optional parameters
            image = pk.generate(width=width, height=height, image_id=image_id, filter_type=filter_type)

            # Save image
            result = image.save(output_file)
            print(f"✅ Placeholder image generated: {result}")
            return result

        except Exception as e:
            print(f"❌ Error generating image: {e}")
            raise

    def smart_crop_image(
        self,
        input_file: str,
        width: int,
        height: int,
        save_steps: bool = False,
        output_file: Optional[str] = None,
    ):
        """Apply smart cropping to an existing image"""
        try:
            from placekitten.processor import ImageProcessor
        except ImportError:
            from src.placekitten.processor import ImageProcessor

        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input image not found: {input_file}")

        try:
            processor = ImageProcessor(str(input_path))

            # Apply smart cropping
            result_processor = processor.smart_crop(width=width, height=height, save_steps=save_steps, output_prefix="smart_crop")

            # Set output filename
            if not output_file:
                output_file = f"smart_cropped_{width}x{height}_{input_path.name}"

            # Save result
            result = result_processor.save(output_file)
            print(f"✅ Smart crop completed: {result}")

            if save_steps:
                print("📁 Processing steps saved with 'smart_crop_' prefix")

            return result

        except Exception as e:
            print(f"❌ Error processing image: {e}")
            raise

    def list_templates(self):
        """List available templates"""
        if not self._validate_templates_folder():
            return

        templates = self._get_available_templates()
        if templates:
            print("📋 Available templates:")
            for template in templates:
                print(f"  • {template}")
        else:
            print("❌ No templates found in template folder")
            print("💡 Run 'deckbuilder init' to copy default template files")

    def init_templates(self, path: str = "./templates"):
        """Initialize template folder with default files and provide setup guidance"""
        import shutil

        target_path = Path(path).resolve()

        # Create template folder
        target_path.mkdir(parents=True, exist_ok=True)

        try:
            # Use global path manager to locate package assets
            from deckbuilder.path_manager import path_manager as global_pm

            if not global_pm.validate_assets_exist():
                print("❌ Could not locate template assets")
                print("💡 Default templates not found in package")
                print(f"💡 Expected location: {global_pm.get_assets_templates_path()}")
                return

            assets_path = global_pm.get_assets_templates_path()
            source_pptx = assets_path / "default.pptx"
            source_json = assets_path / "default.json"

            # Copy template files
            files_copied = []
            if source_pptx.exists():
                shutil.copy2(source_pptx, target_path / "default.pptx")
                files_copied.append("default.pptx")

            if source_json.exists():
                shutil.copy2(source_json, target_path / "default.json")
                files_copied.append("default.json")

            if not files_copied:
                print("❌ No template files found to copy")
                return

            # Generate documentation and examples
            print("📝 Generating documentation and examples...")

            try:
                # Try relative import first (for package usage)
                try:
                    from deckbuilder.cli_tools import DocumentationGenerator
                except ImportError:
                    # Fallback to absolute import (for direct script execution)
                    import sys

                    current_dir = Path(__file__).parent
                    sys.path.insert(0, str(current_dir))
                    from cli_tools import DocumentationGenerator
                doc_gen = DocumentationGenerator(template_folder=str(target_path))

                # Generate Getting_Started.md
                doc_gen.generate_getting_started(output_path=target_path / "Getting_Started.md")

                # Copy golden test files as examples (no subfolder, use example_ prefix)
                self._copy_golden_files_as_examples(target_path)

                generated_files = [
                    "Getting_Started.md",
                    "example_presentation.md",
                    "example_presentation.json",
                ]

                print("Template folder created at", target_path)
                print("Copied:", ", ".join(files_copied))
                print("Generated documentation:")
                for file in generated_files:
                    print(f"   - {file}")
                print()

                # Enhanced success messaging
                print("🚀 Next steps:")
                print("   1. Read: Getting_Started.md")
                print("   2. Try: deckbuilder create example_presentation.md")
                print("   3. Compare: Both example files show the same content in different formats")
                print()

            except ImportError as e:
                print(f"Could not generate documentation: {e}")
                print("Template folder created at", target_path)
                print("Copied:", ", ".join(files_copied))
                print()

            # Environment variable guidance
            print("💡 To make this permanent, add to your .bash_profile:")
            print(f'export DECK_TEMPLATE_FOLDER="{target_path}"')
            print(f'export DECK_OUTPUT_FOLDER="{target_path.parent}"')
            print('export DECK_TEMPLATE_NAME="default"')
            print()

            # Bash completion setup instructions
            print("🔧 Optional: Enable tab completion for deckbuilder commands:")
            completion_url = "https://raw.githubusercontent.com/teknologika/deckbuilder/main/src/deckbuilder/deckbuilder-completion.bash"
            print(f"   curl -o ~/.deckbuilder-completion.bash {completion_url}")
            print('   echo "source ~/.deckbuilder-completion.bash" >> ~/.bash_profile')
            print()
            print("Then reload: source ~/.bash_profile")
            print()
            print("✨ After setup, you can use TAB to complete commands, templates, file paths, and directories!")

        except Exception as e:
            # Extract filename from JSON parsing errors
            error_msg = str(e)
            if "Expecting property name enclosed in double quotes" in error_msg:
                print(f"⚠️ JSON parsing error in master_default_presentation.json: {e}")
            else:
                print(f"⚠️ Error setting up templates: {e}")
            print("💡 Make sure you have write permissions to the target directory")

    def _copy_golden_files_as_examples(self, target_path):
        """Copy master presentation files as examples with example_ prefix"""
        import json
        from deckbuilder.path_manager import path_manager

        # Use centralized path management for master files (source of truth)
        master_md, master_json = path_manager.get_master_presentation_files()

        # Update title in markdown content to showcase Deckbuilder
        if master_md.exists():
            content = master_md.read_text()
            # Replace test title with showcase title
            updated_content = content.replace(
                "# **Comprehensive Layout Test** with *Inline* Formatting\n## Testing all ___19 layouts___ and **formatting** capabilities",
                "# **Deckbuilder: Intelligent PowerPoint Generation** © Bruce McLeod\n## Showcasing all ___19 layouts___ with **professional** *formatting* capabilities",
            )
            # Write to target as example_presentation.md
            with open(target_path / "example_presentation.md", "w", encoding="utf-8") as f:
                f.write(updated_content)

        # Update title in JSON content to showcase Deckbuilder
        if master_json.exists():
            with open(master_json, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Update first slide title if it exists
            if json_data.get("presentation", {}).get("slides"):
                first_slide = json_data["presentation"]["slides"][0]
                if first_slide.get("type") == "Title Slide":
                    first_slide["title"] = "**Deckbuilder: Intelligent PowerPoint Generation** © Bruce McLeod"
                    # Update subtitle/rich_content if it exists
                    if "rich_content" in first_slide and first_slide["rich_content"]:
                        first_slide["rich_content"][0]["heading"] = "Showcasing all ___19 layouts___ with **professional** *formatting* capabilities"

            # Write to target as example_presentation.json
            with open(target_path / "example_presentation.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

    def get_config(self):
        """Display current configuration with proper defaults and source indicators"""
        print("🔧 Deckbuilder Configuration:")

        # Template folder with source indication
        template_folder = self.path_manager.get_template_folder()
        env_template_folder = os.getenv("DECK_TEMPLATE_FOLDER")

        if self.path_manager._template_folder:
            # CLI argument provided
            print(f"  Template Folder: {template_folder} (CLI Argument)")
        elif env_template_folder:
            # Environment variable set
            print(f"  Template Folder: {template_folder} (Environment Variable)")
        else:
            # Default fallback
            print(f"  Template Folder: {template_folder} (Default)")

        # Output folder with source indication
        output_folder = self.path_manager.get_output_folder()
        env_output_folder = os.getenv("DECK_OUTPUT_FOLDER")
        if env_output_folder:
            # Check if it's the current directory to determine source
            current_dir = Path.cwd()
            if output_folder == current_dir:
                print("  Output Folder: . (Default)")
            else:
                print(f"  Output Folder: {output_folder} (Environment Variable)")
        else:
            print("  Output Folder: . (Default)")

        # Default template with source indication
        template_name = self.path_manager.get_template_name()
        env_template_name = os.getenv("DECK_TEMPLATE_NAME")
        if env_template_name:
            if template_name == "default":
                print("  Default Template: default (Default)")
            else:
                print(f"  Default Template: {template_name} (Environment Variable)")
        else:
            print("  Default Template: default (Default)")

        # Display language setting with description and source
        language_code = os.getenv("DECK_PROOFING_LANGUAGE")
        if language_code:
            languages = FormattingSupport.get_supported_languages()
            language_desc = languages.get(language_code, language_code)
            if language_code == "en-AU":
                print(f"  Proofing Language: {language_code} ({language_desc}) (Default)")
            else:
                print(f"  Proofing Language: {language_code} ({language_desc}) (Environment Variable)")
        else:
            print("  Proofing Language: en-AU (English (Australia)) (Default)")

        # Display font setting with corrected message
        font_name = os.getenv("DECK_DEFAULT_FONT")
        if font_name:
            print(f"  Default Font: {font_name} (Environment Variable)")
        else:
            print("  Default Font: Not set (using template fonts)")

    def list_supported_languages(self):
        """List all supported proofing languages"""
        print_supported_languages()

    def validate_language_and_font(self, language_code: Optional[str] = None, font_name: Optional[str] = None) -> bool:
        """
        Validate language and font settings, showing helpful messages.

        Returns:
            True if all provided settings are valid
        """
        formatter = FormattingSupport()
        valid = True

        if language_code:
            is_valid, error_msg, suggestions = formatter.validate_language_code(language_code)
            if not is_valid:
                print(f"❌ {error_msg}")
                if suggestions:
                    print(f"💡 Did you mean: {', '.join(suggestions)}?")
                print("📋 Use 'deckbuilder languages' to see all supported languages")
                valid = False

        if font_name:
            is_valid, warning_msg, suggestions = formatter.validate_font_name(font_name)
            if warning_msg:
                print(f"⚠️  {warning_msg}")
                if suggestions:
                    print(f"💡 Similar common fonts: {', '.join(suggestions)}")
                print("ℹ️  Custom fonts will still be applied if available on the system")

        return valid

    def remap_presentation(
        self,
        input_file: str,
        language_code: Optional[str] = None,
        font_name: Optional[str] = None,
        output_file: Optional[str] = None,
        create_backup: bool = True,
    ):
        """
        Remap language and/or font settings in an existing PowerPoint presentation.
        Updates both master slides and content slides.

        Args:
            input_file: Path to input PowerPoint file
            language_code: Optional language code to apply
            font_name: Optional font name to apply
            output_file: Optional output file path
            create_backup: Whether to create backup file
        """
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False

        if not input_path.suffix.lower() == ".pptx":
            print(f"❌ File must be a PowerPoint file (.pptx): {input_file}")
            return False

        # Validate settings
        if not self.validate_language_and_font(language_code, font_name):
            return False

        # Show what will be updated
        updates = []
        if language_code:
            languages = FormattingSupport.get_supported_languages()
            lang_desc = languages.get(language_code, language_code)
            updates.append(f"language to {language_code} ({lang_desc})")
        if font_name:
            updates.append(f"font to '{font_name}'")

        if not updates:
            print("❌ No updates specified. Use --language or --font arguments.")
            return False

        print(f"🔄 Updating {' and '.join(updates)} in: {input_file}")

        try:
            formatter = FormattingSupport()
            result = formatter.update_presentation(
                presentation_path=str(input_path),
                language_code=language_code,
                font_name=font_name,
                output_path=output_file,
                create_backup=create_backup,
            )

            if result["success"]:
                print(f"✅ {result['message']}")
                if result["backup_path"]:
                    print(f"📁 Backup created: {result['backup_path']}")

                stats = result["stats"]
                print("📊 Processing Summary:")
                print(f"   Master slides: {stats['master_slides_processed']}")
                print(f"   Content slides: {stats['content_slides_processed']}")
                print(f"   Text runs processed: {stats['total_runs_processed']}")
                if language_code:
                    print(f"   Language applied: {stats['total_language_applied']} runs")
                if font_name:
                    print(f"   Font applied: {stats['total_font_applied']} runs")
                return True
            else:
                print(f"❌ {result['error']}")
                return False

        except Exception as e:
            print(f"❌ Error processing presentation: {e}")
            return False

    # Pattern Management Methods

    def list_patterns(self, source: str = "all", verbose: bool = False):
        """List all available patterns with optional filtering"""
        try:
            from deckbuilder.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())
        patterns = loader.load_patterns()

        if not patterns:
            print("📋 No patterns found")
            return

        print(f"📋 Available Patterns ({len(patterns)} total)")
        print()

        for layout_name, pattern_data in sorted(patterns.items()):
            # Determine source
            pattern_source = (
                "user"
                if loader.user_patterns_dir.exists() and any(p.name.replace(".json", "") == layout_name.lower().replace(" ", "_") for p in loader.user_patterns_dir.glob("*.json"))
                else "builtin"
            )

            # Apply source filter
            if source != "all" and source != pattern_source:
                continue

            source_icon = "👤" if pattern_source == "user" else "📦"
            print(f"{source_icon} {layout_name}")

            if verbose:
                description = pattern_data.get("description", "No description")
                validation = pattern_data.get("validation", {})
                required_fields = validation.get("required_fields", [])
                optional_fields = validation.get("optional_fields", [])

                print(f"   Description: {description}")
                print(f"   Required fields: {', '.join(required_fields) if required_fields else 'None'}")
                print(f"   Optional fields: {', '.join(optional_fields) if optional_fields else 'None'}")
                print()

    def validate_patterns(self, pattern_name: str = None, show_fixes: bool = False):
        """Validate pattern files and show any errors"""
        try:
            from deckbuilder.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())

        if pattern_name:
            # Validate specific pattern
            patterns = loader.load_patterns()
            if pattern_name not in patterns:
                print(f"❌ Pattern '{pattern_name}' not found")
                return False

            pattern_data = patterns[pattern_name]
            errors = loader.validator.validate_pattern(pattern_data)

            if errors:
                print(f"❌ Pattern '{pattern_name}' validation failed:")
                for error in errors:
                    print(f"   • {error}")
                if show_fixes:
                    print("\n💡 Suggestions:")
                    print("   • Check that all required fields are present")
                    print("   • Verify YAML syntax in examples")
                    print("   • Ensure layout name matches yaml_pattern.layout")
            else:
                print(f"✅ Pattern '{pattern_name}' is valid")

        else:
            # Validate all patterns
            all_valid = True
            validation_count = 0

            # Check built-in patterns
            if loader.builtin_patterns_dir.exists():
                for pattern_file in loader.builtin_patterns_dir.glob("*.json"):
                    pattern_data = loader._load_pattern_file(pattern_file)
                    validation_count += 1
                    if pattern_data is None:
                        all_valid = False
                        print(f"❌ Built-in pattern {pattern_file.name} failed validation")

            # Check user patterns
            if loader.user_patterns_dir.exists():
                for pattern_file in loader.user_patterns_dir.glob("*.json"):
                    pattern_data = loader._load_pattern_file(pattern_file)
                    validation_count += 1
                    if pattern_data is None:
                        all_valid = False
                        print(f"❌ User pattern {pattern_file.name} failed validation")

            if all_valid:
                print(f"✅ All {validation_count} patterns are valid")
            else:
                print("❌ Some patterns failed validation")
                if show_fixes:
                    print("\n💡 Run with --fix flag for specific suggestions")

        return all_valid

    def show_pattern_info(self, pattern_name: str, show_example: bool = False):
        """Show detailed information about a specific pattern"""
        try:
            from deckbuilder.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())
        patterns = loader.load_patterns()

        if pattern_name not in patterns:
            print(f"❌ Pattern '{pattern_name}' not found")
            available = ", ".join(sorted(patterns.keys()))
            print(f"💡 Available patterns: {available}")
            return

        pattern_data = patterns[pattern_name]

        print(f"📋 Pattern: {pattern_name}")
        print()
        print(f"Description: {pattern_data.get('description', 'No description')}")
        print()

        # Show validation info
        validation = pattern_data.get("validation", {})
        required_fields = validation.get("required_fields", [])
        optional_fields = validation.get("optional_fields", [])

        print("Required fields:")
        for field in required_fields:
            print(f"  • {field}")

        print("\nOptional fields:")
        for field in optional_fields:
            print(f"  • {field}")

        if show_example:
            example = pattern_data.get("example", "")
            if example:
                print("\nExample frontmatter:")
                print("```yaml")
                print(example)
                print("```")
            else:
                print("\nNo example available")

    def copy_patterns(self, copy_all: bool = False, pattern_name: str = None, overwrite: bool = False, backup: bool = False):
        """Copy built-in patterns to user override directory"""
        try:
            from deckbuilder.pattern_loader import PatternLoader
            import shutil
            from datetime import datetime
        except ImportError:
            from src.deckbuilder.pattern_loader import PatternLoader
            import shutil
            from datetime import datetime

        loader = PatternLoader(self.path_manager.get_template_folder())

        # Create user patterns directory if it doesn't exist
        loader.user_patterns_dir.mkdir(parents=True, exist_ok=True)

        if not loader.builtin_patterns_dir.exists():
            print("❌ Built-in patterns directory not found")
            return False

        if not copy_all and not pattern_name:
            print("❌ Must specify either --all or --pattern <name>")
            return False

        copied_count = 0

        if copy_all:
            print("📋 Copying all built-in patterns to user override directory...")
            pattern_files = list(loader.builtin_patterns_dir.glob("*.json"))
        else:
            # Find specific pattern file
            pattern_files = []
            for pattern_file in loader.builtin_patterns_dir.glob("*.json"):
                try:
                    pattern_data = loader._load_pattern_file(pattern_file)
                    if pattern_data and pattern_data.get("yaml_pattern", {}).get("layout") == pattern_name:
                        pattern_files = [pattern_file]
                        break
                except Exception:
                    continue

            if not pattern_files:
                print(f"❌ Pattern '{pattern_name}' not found in built-in patterns")
                return False

        for pattern_file in pattern_files:
            try:
                # Load pattern to get layout name
                pattern_data = loader._load_pattern_file(pattern_file)
                if not pattern_data:
                    print(f"⚠️ Skipping invalid pattern file: {pattern_file.name}")
                    continue

                layout_name = pattern_data.get("yaml_pattern", {}).get("layout")
                if not layout_name:
                    print(f"⚠️ Skipping pattern file without layout name: {pattern_file.name}")
                    continue

                # Create target filename
                target_filename = layout_name.lower().replace(" ", "_") + ".json"
                target_path = loader.user_patterns_dir / target_filename

                # Check if file exists
                if target_path.exists() and not overwrite:
                    print(f"⚠️ User pattern '{layout_name}' already exists (use --overwrite to replace)")
                    continue

                # Create backup if requested
                if backup and target_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_path = target_path.with_suffix(f".backup_{timestamp}.json")
                    shutil.copy2(target_path, backup_path)
                    print(f"💾 Created backup: {backup_path.name}")

                # Copy the pattern file
                shutil.copy2(pattern_file, target_path)
                print(f"✅ Copied: {layout_name} → {target_filename}")
                copied_count += 1

            except Exception as e:
                print(f"❌ Error copying {pattern_file.name}: {e}")

        if copied_count > 0:
            print(f"\n✅ Successfully copied {copied_count} pattern(s)")
            print(f"📁 Location: {loader.user_patterns_dir}")
            print("\n💡 You can now customize these patterns to override built-in behavior")
        else:
            print("❌ No patterns were copied")

        return copied_count > 0

    def show_completion_help(self):
        """Show tab completion installation instructions"""
        print("🔧 Tab Completion Setup")
        print()
        print("To enable tab completion for deckbuilder commands:")
        print()
        print("1. Download the completion script:")
        completion_url = "https://raw.githubusercontent.com/teknologika/deckbuilder/main/" "src/deckbuilder/deckbuilder-completion.bash"
        print(f"   curl -o ~/.deckbuilder-completion.bash {completion_url}")
        print()
        print("2. Add to your .bash_profile:")
        print('   echo "source ~/.deckbuilder-completion.bash" >> ~/.bash_profile')
        print()
        print("3. Reload your shell:")
        print("   source ~/.bash_profile")
        print()
        print("✨ After setup, you can use TAB to complete:")
        print("   • Commands: deckbuilder <TAB>")
        print("   • Template names: deckbuilder analyze <TAB>")
        print("   • File paths: deckbuilder create <TAB>")
        print("   • Directory navigation: deckbuilder create docs/<TAB>")
        print("   • Output paths: deckbuilder create file.md -o outputs/<TAB>")
        print("   • Global flags: deckbuilder -<TAB>")
        print()
        print("For system-wide installation:")
        print("   sudo curl -o /etc/bash_completion.d/deckbuilder \\")
        print(f"        {completion_url}")


def create_parser():
    """Create hierarchical command-line argument parser"""
    parser = argparse.ArgumentParser(
        prog="deckbuilder",
        description="Deckbuilder CLI - Intelligent PowerPoint presentation generation © Bruce McLeod",
        usage="deckbuilder [options] <command> <subcommand> [parameters]",
        add_help=False,  # Custom help handling
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global arguments (apply to all commands)
    parser.add_argument(
        "-t",
        "--template-folder",
        metavar="PATH",
        help="Template folder path (default: env var or current dir)",
    )
    parser.add_argument(
        "-l",
        "--language",
        metavar="LANG",
        help="Proofing language (e.g., en-US, en-AU)",
    )
    parser.add_argument("-f", "--font", metavar="FONT", help='Default font family (e.g., "Calibri", "Arial")')
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("-V", "--version", action="store_true", help="Show version information")

    subparsers = parser.add_subparsers(dest="command", help="Available commands", metavar="<command>")

    # Create presentation command (stays as top-level)
    create_parser = subparsers.add_parser("create", help="Generate presentations from markdown or JSON", add_help=False)
    create_parser.add_argument("input_file", help="Input markdown (.md) or JSON (.json) file")
    create_parser.add_argument("--output", "-o", help="Output filename (without extension)")
    create_parser.add_argument("--template", "-t", help="Template name to use (default: 'default')")
    create_parser.add_argument("-h", "--help", action="store_true", help="Show help for create command")

    # Template management commands (grouped)
    template_parser = subparsers.add_parser("template", help="Manage PowerPoint templates and mappings", add_help=False)
    template_parser.add_argument("-h", "--help", action="store_true", help="Show help for template commands")
    template_subs = template_parser.add_subparsers(dest="template_command", help="Template subcommands", metavar="<subcommand>")

    # Template analyze
    analyze_parser = template_subs.add_parser("analyze", help="Analyze template structure and placeholders", add_help=False)
    analyze_parser.add_argument("template", nargs="?", default="default", help="Template name")
    analyze_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    analyze_parser.add_argument("-h", "--help", action="store_true", help="Show help for analyze command")

    # Template validate
    validate_parser = template_subs.add_parser("validate", help="Validate template and JSON mappings", add_help=False)
    validate_parser.add_argument("template", nargs="?", default="default", help="Template name")
    validate_parser.add_argument("-h", "--help", action="store_true", help="Show help for validate command")

    # Template document
    document_parser = template_subs.add_parser("document", help="Generate comprehensive template documentation", add_help=False)
    document_parser.add_argument("template", nargs="?", default="default", help="Template name")
    document_parser.add_argument("--output", "-o", help="Output documentation file")
    document_parser.add_argument("-h", "--help", action="store_true", help="Show help for document command")

    # Template enhance
    enhance_parser = template_subs.add_parser("enhance", help="Enhance template with corrected placeholders", add_help=False)
    enhance_parser.add_argument("template", nargs="?", default="default", help="Template name")
    enhance_parser.add_argument("--mapping", help="Custom mapping file")
    enhance_parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    enhance_parser.add_argument(
        "--no-conventions",
        action="store_false",
        dest="use_conventions",
        help="Don't use naming conventions",
    )
    enhance_parser.add_argument("-h", "--help", action="store_true", help="Show help for enhance command")

    # Template list
    list_parser = template_subs.add_parser("list", help="List all available templates", add_help=False)
    list_parser.add_argument("-h", "--help", action="store_true", help="Show help for list command")

    # Pattern management commands (grouped)
    pattern_parser = subparsers.add_parser("pattern", help="Manage structured frontmatter patterns", add_help=False)
    pattern_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern commands")
    pattern_subs = pattern_parser.add_subparsers(dest="pattern_command", help="Pattern subcommands", metavar="<subcommand>")

    # Pattern list
    pattern_list_parser = pattern_subs.add_parser("list", help="List all available patterns", add_help=False)
    pattern_list_parser.add_argument("--source", choices=["all", "builtin", "user"], default="all", help="Pattern source filter")
    pattern_list_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed pattern information")
    pattern_list_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern list command")

    # Pattern validate
    pattern_validate_parser = pattern_subs.add_parser("validate", help="Validate pattern files and schema", add_help=False)
    pattern_validate_parser.add_argument("pattern", nargs="?", help="Specific pattern name to validate (default: all)")
    pattern_validate_parser.add_argument("--fix", action="store_true", help="Show suggestions for fixing validation errors")
    pattern_validate_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern validate command")

    # Pattern info
    pattern_info_parser = pattern_subs.add_parser("info", help="Show detailed information about a pattern", add_help=False)
    pattern_info_parser.add_argument("pattern", help="Pattern name to show information for")
    pattern_info_parser.add_argument("--example", action="store_true", help="Show example frontmatter")
    pattern_info_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern info command")

    # Pattern create
    pattern_create_parser = pattern_subs.add_parser("create", help="Create a new user pattern", add_help=False)
    pattern_create_parser.add_argument("layout_name", help="Layout name for the new pattern")
    pattern_create_parser.add_argument("--template", help="Template to base the pattern on")
    pattern_create_parser.add_argument("--interactive", "-i", action="store_true", help="Interactive pattern creation")
    pattern_create_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern create command")

    # Pattern copy
    pattern_copy_parser = pattern_subs.add_parser("copy", help="Copy built-in patterns to user override directory", add_help=False)
    pattern_copy_parser.add_argument("--all", action="store_true", help="Copy all built-in patterns")
    pattern_copy_parser.add_argument("--pattern", help="Copy specific pattern by name")
    pattern_copy_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing user patterns")
    pattern_copy_parser.add_argument("--backup", action="store_true", help="Create backup of existing patterns")
    pattern_copy_parser.add_argument("-h", "--help", action="store_true", help="Show help for pattern copy command")

    # Image processing commands (grouped)
    image_parser = subparsers.add_parser("image", help="Process and generate images with PlaceKitten", add_help=False)
    image_parser.add_argument("-h", "--help", action="store_true", help="Show help for image commands")
    image_subs = image_parser.add_subparsers(dest="image_command", help="Image subcommands", metavar="<subcommand>")

    # Image generate
    generate_parser = image_subs.add_parser("generate", help="Generate PlaceKitten placeholder images", add_help=False)
    generate_parser.add_argument("width", type=int, help="Image width")
    generate_parser.add_argument("height", type=int, help="Image height")
    generate_parser.add_argument("--id", type=int, help="Specific kitten image ID (1-6)")
    generate_parser.add_argument("--filter", help="Filter to apply (grayscale, sepia, blur, etc.)")
    generate_parser.add_argument("--output", "-o", help="Output filename")
    generate_parser.add_argument("-h", "--help", action="store_true", help="Show help for generate command")

    # Image crop
    crop_parser = image_subs.add_parser("crop", help="Smart crop existing images", add_help=False)
    crop_parser.add_argument("input_file", help="Input image file")
    crop_parser.add_argument("width", type=int, help="Target width")
    crop_parser.add_argument("height", type=int, help="Target height")
    crop_parser.add_argument("--save-steps", action="store_true", help="Save processing steps")
    crop_parser.add_argument("--output", "-o", help="Output filename")
    crop_parser.add_argument("-h", "--help", action="store_true", help="Show help for crop command")

    # Configuration and setup commands (grouped)
    config_parser = subparsers.add_parser("config", help="Configuration, setup, and system information", add_help=False)
    config_parser.add_argument("-h", "--help", action="store_true", help="Show help for config commands")
    config_subs = config_parser.add_subparsers(dest="config_command", help="Configuration subcommands", metavar="<subcommand>")

    # Config show
    show_parser = config_subs.add_parser("show", help="Show current configuration", add_help=False)
    show_parser.add_argument("-h", "--help", action="store_true", help="Show help for show command")

    # Config languages
    languages_parser = config_subs.add_parser("languages", help="List supported languages", add_help=False)
    languages_parser.add_argument("-h", "--help", action="store_true", help="Show help for languages command")

    # Config completion
    completion_parser = config_subs.add_parser("completion", help="Setup bash completion", add_help=False)
    completion_parser.add_argument("-h", "--help", action="store_true", help="Show help for completion command")

    # Remap command (update existing PowerPoint presentations)
    remap_parser = subparsers.add_parser(
        "remap",
        help="Update language and font settings in existing PowerPoint files",
        add_help=False,
    )
    remap_parser.add_argument("input_file", help="Input PowerPoint (.pptx) file to update")
    remap_parser.add_argument(
        "--language",
        "-l",
        metavar="LANG",
        help="Language code to apply (e.g., en-US, en-AU, es-ES)",
    )
    remap_parser.add_argument("--font", "-f", metavar="FONT", help="Font family to apply (e.g., Calibri, Arial)")
    remap_parser.add_argument("--output", "-o", metavar="FILE", help="Output file path (default: overwrite input)")
    remap_parser.add_argument("--no-backup", action="store_true", help="Skip creating backup file")
    remap_parser.add_argument("-h", "--help", action="store_true", help="Show help for remap command")

    # Help command
    help_parser = subparsers.add_parser("help", help="Show detailed help information", add_help=False)
    help_parser.add_argument("help_command", nargs="?", help="Command to show help for")
    help_parser.add_argument("help_subcommand", nargs="?", help="Subcommand to show help for")

    # Init command (back to top-level for easy first-time setup)
    init_parser = subparsers.add_parser("init", help="Initialize template folder with default files", add_help=False)
    init_parser.add_argument("path", nargs="?", default="./templates", help="Template folder path (default: ./templates)")
    init_parser.add_argument("-h", "--help", action="store_true", help="Show help for init command")

    return parser


def show_main_help():
    """Show main help message"""
    print(
        """usage: deckbuilder [options] <command> <subcommand> [parameters]

Deckbuilder CLI - Intelligent PowerPoint presentation generation © Bruce McLeod

Commands:
  create                    Generate presentations from markdown or JSON
  template                  Manage PowerPoint templates and mappings
  pattern                   Manage structured frontmatter patterns
  image                     Process and generate images with PlaceKitten
  config                    Configuration and system information
  remap                     Update language and font settings in existing PowerPoint files
  init                      Initialize template folder with default files
  help                      Show detailed help for commands

Global Options:
  -t, --template-folder PATH Template folder path (default: env var or current dir)
  -l, --language LANG        Proofing language (en-AU, es-ES, etc.)
  -f, --font FONT            Default font family
  -h, --help                 Show this help message

Examples:
  deckbuilder init                      # First-time setup
  deckbuilder create presentation.md
  deckbuilder template analyze default --verbose
  deckbuilder image generate 800 600 --filter grayscale
  deckbuilder config languages

To see help for a specific command:
  deckbuilder help <command>
  deckbuilder <command> help
"""
    )


def show_template_help():
    """Show template command help"""
    print(
        """Template management commands:

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
"""
    )


def show_pattern_help():
    """Show pattern command help"""
    print(
        """Pattern management commands:

Usage: deckbuilder pattern <subcommand> [options]

Subcommands:
  list                    List all available patterns (builtin + user)
  validate [pattern]      Validate pattern files and schema
  info <pattern>          Show detailed pattern information
  copy --all|--pattern    Copy built-in patterns to user override directory
  create <layout>         Create new user pattern (planned)

Options:
  --source all|builtin|user  Filter patterns by source (for list)
  --verbose, -v             Show detailed information
  --example                 Show example frontmatter (for info)
  --overwrite              Overwrite existing patterns (for copy)
  --backup                 Create backup before overwrite (for copy)
  --fix                    Show fix suggestions (for validate)

Examples:
  deckbuilder pattern list --verbose
  deckbuilder pattern copy --all --backup
  deckbuilder pattern info "Four Columns" --example
  deckbuilder pattern validate "Two Content" --fix

For detailed help on a subcommand:
  deckbuilder help pattern <subcommand>
"""
    )


def show_image_help():
    """Show image command help"""
    print(
        """Image processing commands:

Usage: deckbuilder image <subcommand> [options]

Subcommands:
  generate <w> <h>         Generate PlaceKitten placeholder images
  crop <file> <w> <h>      Smart crop existing images

Examples:
  deckbuilder image generate 800 600 --filter grayscale
  deckbuilder image crop input.jpg 1920 1080 --save-steps

For detailed help on a subcommand:
  deckbuilder help image <subcommand>
"""
    )


def show_config_help():
    """Show config command help"""
    print(
        """Configuration and setup commands:

Usage: deckbuilder config <subcommand> [options]

Subcommands:
  show                     Show current configuration
  languages                List supported languages
  completion               Setup bash completion

Examples:
  deckbuilder config show
  deckbuilder config languages
  deckbuilder config completion

For detailed help on a subcommand:
  deckbuilder help config <subcommand>
"""
    )


def handle_help_command(args):
    """Handle help command with contextual information"""
    if not hasattr(args, "help_command") or not args.help_command:
        show_main_help()
        return

    if args.help_command == "template":
        if hasattr(args, "help_subcommand") and args.help_subcommand:
            # Show specific template subcommand help
            if args.help_subcommand == "analyze":
                print("Analyze template structure and placeholders")
                print("Usage: deckbuilder template analyze <name> [--verbose]")
            elif args.help_subcommand == "validate":
                print("Validate template and JSON mappings")
                print("Usage: deckbuilder template validate <name>")
            elif args.help_subcommand == "document":
                print("Generate comprehensive template documentation")
                print("Usage: deckbuilder template document <name> [--output file]")
            elif args.help_subcommand == "enhance":
                print("Enhance template with corrected placeholders")
                print("Usage: deckbuilder template enhance <name> [options]")
            elif args.help_subcommand == "list":
                print("List all available templates")
                print("Usage: deckbuilder template list")
            else:
                print(f"Unknown template subcommand: {args.help_subcommand}")
        else:
            show_template_help()
    elif args.help_command == "pattern":
        if hasattr(args, "help_subcommand") and args.help_subcommand:
            # Show specific pattern subcommand help
            if args.help_subcommand == "list":
                print("List all available patterns")
                print("Usage: deckbuilder pattern list [--source all|builtin|user] [--verbose]")
            elif args.help_subcommand == "validate":
                print("Validate pattern files and schema")
                print("Usage: deckbuilder pattern validate [pattern_name] [--fix]")
            elif args.help_subcommand == "info":
                print("Show detailed information about a pattern")
                print("Usage: deckbuilder pattern info <pattern_name> [--example]")
            elif args.help_subcommand == "copy":
                print("Copy built-in patterns to user override directory")
                print("Usage: deckbuilder pattern copy --all|--pattern <name> [--overwrite] [--backup]")
            elif args.help_subcommand == "create":
                print("Create a new user pattern")
                print("Usage: deckbuilder pattern create <layout_name> [--template template] [--interactive]")
            else:
                print(f"Unknown pattern subcommand: {args.help_subcommand}")
        else:
            show_pattern_help()
    elif args.help_command == "image":
        if hasattr(args, "help_subcommand") and args.help_subcommand:
            if args.help_subcommand == "generate":
                print("Generate PlaceKitten placeholder images")
                print("Usage: deckbuilder image generate <width> <height> [options]")
            elif args.help_subcommand == "crop":
                print("Smart crop existing images")
                print("Usage: deckbuilder image crop <file> <width> <height> [options]")
            else:
                print(f"Unknown image subcommand: {args.help_subcommand}")
        else:
            show_image_help()
    elif args.help_command == "config":
        if hasattr(args, "help_subcommand") and args.help_subcommand:
            if args.help_subcommand == "show":
                print("Show current configuration")
                print("Usage: deckbuilder config show")
            elif args.help_subcommand == "languages":
                print("List supported languages")
                print("Usage: deckbuilder config languages")
            elif args.help_subcommand == "completion":
                print("Setup bash completion")
                print("Usage: deckbuilder config completion")
            else:
                print(f"Unknown config subcommand: {args.help_subcommand}")
        else:
            show_config_help()
    elif args.help_command == "create":
        print("Generate presentations from markdown or JSON")
        print("Usage: deckbuilder create <file> [options]")
        print("Options:")
        print("  --output, -o       Output filename (without extension)")
        print("  --template, -t     Template name to use")
    elif args.help_command == "init":
        print("Initialize template folder with default files")
        print("Usage: deckbuilder init [path]")
        print("Arguments:")
        print("  path               Template folder path (default: ./templates)")
    elif args.help_command == "remap":
        print("Update language and font settings in existing PowerPoint files")
        print("Usage: deckbuilder remap <file.pptx> [options]")
        print("Arguments:")
        print("  input_file         PowerPoint file (.pptx) to update")
        print("Options:")
        print("  --language, -l     Language code (e.g., en-US, en-AU, es-ES)")
        print("  --font, -f         Font family (e.g., Calibri, Arial)")
        print("  --output, -o       Output file path (default: overwrite input)")
        print("  --no-backup        Skip creating backup file")
        print("Examples:")
        print("  deckbuilder remap presentation.pptx --language en-US")
        print("  deckbuilder remap slides.pptx --font Arial --output new_slides.pptx")
    else:
        print(f"Unknown command: {args.help_command}")
        print("Available commands: create, template, image, config, remap, init, help")


def handle_template_command(cli, args):
    """Handle template subcommands"""
    if hasattr(args, "help") and args.help:
        show_template_help()
        return

    if not hasattr(args, "template_command") or not args.template_command:
        show_template_help()
        return

    if args.template_command == "analyze":
        if hasattr(args, "help") and args.help:
            print("Analyze template structure and placeholders")
            print("Usage: deckbuilder template analyze <name> [--verbose]")
            return
        cli.analyze_template(args.template, verbose=args.verbose)
    elif args.template_command == "validate":
        if hasattr(args, "help") and args.help:
            print("Validate template and JSON mappings")
            print("Usage: deckbuilder template validate <name>")
            return
        cli.validate_template(args.template)
    elif args.template_command == "document":
        if hasattr(args, "help") and args.help:
            print("Generate comprehensive template documentation")
            print("Usage: deckbuilder template document <name> [--output file]")
            return
        cli.document_template(args.template, args.output)
    elif args.template_command == "enhance":
        if hasattr(args, "help") and args.help:
            print("Enhance template with corrected placeholders")
            print("Usage: deckbuilder template enhance <name> [options]")
            return
        cli.enhance_template(
            template_name=args.template,
            mapping_file=args.mapping,
            no_backup=args.no_backup,
            use_conventions=args.use_conventions,
        )
    elif args.template_command == "list":
        if hasattr(args, "help") and args.help:
            print("List all available templates")
            print("Usage: deckbuilder template list")
            return
        cli.list_templates()
    else:
        print(f"Unknown template subcommand: {args.template_command}")
        show_template_help()


def handle_pattern_command(cli, args):
    """Handle pattern subcommands"""
    if hasattr(args, "help") and args.help:
        show_pattern_help()
        return

    if not hasattr(args, "pattern_command") or not args.pattern_command:
        show_pattern_help()
        return

    if args.pattern_command == "list":
        if hasattr(args, "help") and args.help:
            print("List all available patterns")
            print("Usage: deckbuilder pattern list [--source all|builtin|user] [--verbose]")
            return
        cli.list_patterns(args.source, args.verbose)

    elif args.pattern_command == "validate":
        if hasattr(args, "help") and args.help:
            print("Validate pattern files and schema")
            print("Usage: deckbuilder pattern validate [pattern_name] [--fix]")
            return
        cli.validate_patterns(args.pattern, args.fix)

    elif args.pattern_command == "info":
        if hasattr(args, "help") and args.help:
            print("Show detailed information about a pattern")
            print("Usage: deckbuilder pattern info <pattern_name> [--example]")
            return
        cli.show_pattern_info(args.pattern, args.example)

    elif args.pattern_command == "copy":
        if hasattr(args, "help") and args.help:
            print("Copy built-in patterns to user override directory")
            print("Usage: deckbuilder pattern copy --all|--pattern <name> [--overwrite] [--backup]")
            return
        cli.copy_patterns(args.all, args.pattern, args.overwrite, args.backup)

    elif args.pattern_command == "create":
        if hasattr(args, "help") and args.help:
            print("Create a new user pattern")
            print("Usage: deckbuilder pattern create <layout_name> [--template template_name] [--interactive]")
            return
        print("❌ Pattern creation not yet implemented")
        print("💡 Use 'deckbuilder pattern copy' to copy built-in patterns for customization")

    else:
        print(f"Unknown pattern subcommand: {args.pattern_command}")
        show_pattern_help()


def handle_image_command(cli, args):
    """Handle image subcommands"""
    if hasattr(args, "help") and args.help:
        show_image_help()
        return

    if not hasattr(args, "image_command") or not args.image_command:
        show_image_help()
        return

    if args.image_command == "generate":
        if hasattr(args, "help") and args.help:
            print("Generate PlaceKitten placeholder images")
            print("Usage: deckbuilder image generate <width> <height> [options]")
            return
        cli.generate_placeholder_image(
            width=args.width,
            height=args.height,
            image_id=args.id,
            filter_type=args.filter,
            output_file=args.output,
        )
    elif args.image_command == "crop":
        if hasattr(args, "help") and args.help:
            print("Smart crop existing images")
            print("Usage: deckbuilder image crop <file> <width> <height> [options]")
            return
        cli.smart_crop_image(
            input_file=args.input_file,
            width=args.width,
            height=args.height,
            save_steps=args.save_steps,
            output_file=args.output,
        )
    else:
        print(f"Unknown image subcommand: {args.image_command}")
        show_image_help()


def handle_config_command(cli, args):
    """Handle config subcommands"""
    if hasattr(args, "help") and args.help:
        show_config_help()
        return

    if not hasattr(args, "config_command") or not args.config_command:
        show_config_help()
        return

    if args.config_command == "show":
        if hasattr(args, "help") and args.help:
            print("Show current configuration")
            print("Usage: deckbuilder config show")
            return
        cli.get_config()
    elif args.config_command == "languages":
        if hasattr(args, "help") and args.help:
            print("List supported languages")
            print("Usage: deckbuilder config languages")
            return
        cli.list_supported_languages()
    elif args.config_command == "completion":
        if hasattr(args, "help") and args.help:
            print("Setup bash completion")
            print("Usage: deckbuilder config completion")
            return
        cli.show_completion_help()
    else:
        print(f"Unknown config subcommand: {args.config_command}")
        show_config_help()


def main():
    """Main CLI entry point with hierarchical command structure"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle version flag
    if hasattr(args, "version") and args.version:
        # Create a temporary path manager for version info
        from deckbuilder.path_manager import path_manager

        version = path_manager.get_version()
        print(f"Deckbuilder CLI v{version}")
        print("Intelligent PowerPoint presentation generation © Bruce McLeod")
        return

    # Handle help flag or missing command
    if (hasattr(args, "help") and args.help) or not args.command:
        show_main_help()
        return

    # Handle help command specially
    if args.command == "help":
        handle_help_command(args)
        return

    # Initialize CLI with global arguments
    cli = DeckbuilderCLI(
        template_folder=getattr(args, "template_folder", None),
        language=getattr(args, "language", None),
        font=getattr(args, "font", None),
    )

    try:
        # Route hierarchical commands
        if args.command == "create":
            if hasattr(args, "help") and args.help:
                print("Generate presentations from markdown or JSON")
                print("Usage: deckbuilder create <file> [options]")
                return
            cli.create_presentation(input_file=args.input_file, output_name=args.output, template=args.template)
        elif args.command == "template":
            handle_template_command(cli, args)
        elif args.command == "pattern":
            handle_pattern_command(cli, args)
        elif args.command == "image":
            handle_image_command(cli, args)
        elif args.command == "config":
            handle_config_command(cli, args)
        elif args.command == "init":
            if hasattr(args, "help") and args.help:
                print("Initialize template folder with default files")
                print("Usage: deckbuilder init [path]")
                return
            cli.init_templates(args.path)
        elif args.command == "remap":
            if hasattr(args, "help") and args.help:
                print("Update language and font settings in existing PowerPoint files")
                print("Usage: deckbuilder remap <file.pptx> [options]")
                print("Options:")
                print("  --language, -l LANG  Language code (e.g., en-US, en-AU, es-ES)")
                print("  --font, -f FONT      Font family (e.g., Calibri, Arial)")
                print("  --output, -o FILE    Output file path (default: overwrite input)")
                print("  --no-backup          Skip creating backup file")
                return
            success = cli.remap_presentation(
                input_file=args.input_file,
                language_code=getattr(args, "language", None),
                font_name=getattr(args, "font", None),
                output_file=getattr(args, "output", None),
                create_backup=not getattr(args, "no_backup", False),
            )
            if not success:
                sys.exit(1)
        else:
            print(f"Unknown command: {args.command}")
            show_main_help()

    except Exception as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
