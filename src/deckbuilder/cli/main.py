#!/usr/bin/env python3
"""
Deckbuilder CLI - Standalone Command Line Interface

Complete command-line interface for Deckbuilder presentation generation,
template management, and PlaceKitten image processing. Designed for
local development and standalone usage without MCP server dependency.
"""

import json
import os
import platform
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Optional

import click

from ..core.engine import Deckbuilder
from .commands import TemplateManager
from ..content.formatting_support import FormattingSupport, print_supported_languages
from ..utils.path import create_cli_path_manager, get_placekitten


def clear_hidden_flag(path):
    if platform.system() == "Darwin":
        subprocess.run(["chflags", "nohidden", str(path)], check=False)  # nosec B603 B607


# Initialize PlaceKitten using DRY utility (needed by CLI class)
PlaceKitten = get_placekitten()  # noqa: E402


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
            click.echo(f"❌ Template folder not found: {template_folder}", err=True)
            click.echo(
                "💡 Run 'deckbuilder init' to create template folder and copy default files",
                err=True,
            )
            return False
        return True

    def _get_available_templates(self):
        """Get list of available templates with error handling"""
        template_folder = self.path_manager.get_template_folder()
        if not template_folder.exists():
            return []

        return [template.stem for template in template_folder.glob("*.pptx")]

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
            click.echo(f"❌ Input file not found: {input_file}", err=True)
            raise click.Abort()

        # Validate templates folder exists
        if not self._validate_templates_folder():
            raise click.Abort()

        # Determine output filename
        if not output_name:
            output_name = input_path.stem

        # Use PathManager to get template name (respects CLI arg > env var > default)
        template_name = template or self.path_manager.get_template_name()

        # Show template selection feedback
        template_folder = self.path_manager.get_template_folder()
        template_file = self.path_manager.get_template_file_path(template_name)

        click.echo(f"Using template: {template_name}.pptx from {template_folder}")

        # Check if template file exists
        if template_file.exists():
            click.echo(f"Template file: {template_file.name} ✓ Found")
        else:
            click.echo(f"✗ Template file not found: {template_file}", err=True)
            click.echo("Run 'deckbuilder init' to create template folder with default files", err=True)
            return

        # Reset singleton and create fresh instance with CLI path manager
        Deckbuilder.reset()
        db = Deckbuilder(path_manager_instance=self.path_manager)

        try:
            presentation_data = {}
            markdown_content = None

            if input_path.suffix.lower() == ".md":
                from deckbuilder.content.frontmatter_to_json_converter import markdown_to_canonical_json
                from deckbuilder.core.validation import PresentationValidator

                # Process markdown file
                markdown_content = input_path.read_text(encoding="utf-8")
                click.echo(f"Processing markdown file: {input_path.name}")
                presentation_data = markdown_to_canonical_json(markdown_content)

                # STEP 0: Validate Markdown → JSON conversion
                template_folder = str(self.path_manager.get_template_folder())
                validator = PresentationValidator(presentation_data, template_name, template_folder)
                validator.validate_markdown_to_json(markdown_content, presentation_data)
            elif input_path.suffix.lower() == ".json":
                # Process JSON file directly
                with open(input_path, "r", encoding="utf-8") as f:
                    presentation_data = json.load(f)
                click.echo(f"Processing JSON file: {input_path.name}")
            else:
                raise ValueError(f"Unsupported file format: {input_path.suffix}. " "Supported formats: .md, .json")

            result = db.create_presentation(
                presentation_data,
                fileName=output_name,
                templateName=template_name,
                language_code=self.language,  # Pass language from CLI/env vars
                font_name=self.font,  # Pass font from CLI/env vars
            )

            # Check if result indicates an error
            if result and ("Error creating presentation from markdown:" in result or "Error creating presentation from JSON:" in result):
                click.echo(f"✗ {result}", err=True)
                raise RuntimeError(result)

            click.echo(f"✓ Presentation created successfully: {result}")
            return result

        except Exception as e:
            click.echo(f"❌ Error creating presentation: {e}", err=True)
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
            click.echo(f"✅ Placeholder image generated: {result}")
            return result

        except Exception as e:
            click.echo(f"❌ Error generating image: {e}", err=True)
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
            click.echo(f"✅ Smart crop completed: {result}")

            if save_steps:
                click.echo("📁 Processing steps saved with 'smart_crop_' prefix")

            return result

        except Exception as e:
            click.echo(f"❌ Error processing image: {e}", err=True)
            raise

    def list_templates(self):
        """List available templates"""
        if not self._validate_templates_folder():
            return

        templates = self._get_available_templates()
        if templates:
            click.echo("📋 Available templates:")
            for template in templates:
                click.echo(f"  • {template}")
        else:
            click.echo("❌ No templates found in template folder", err=True)
            click.echo("💡 Run 'deckbuilder init' to copy default template files", err=True)

    def init_templates(self, path: str = "./templates"):
        """Initialize template folder with default files and provide setup guidance"""
        target_path = Path(path).resolve()

        # Create template folder
        target_path.mkdir(parents=True, exist_ok=True)

        try:
            # Copy directly from package assets without creating cache folder
            from importlib.resources import files

            # Get package assets directly
            package_assets = files("deckbuilder") / "assets" / "templates"

            # Copy template files (JSON mapping files no longer used)
            files_copied = []

            try:
                source_pptx = package_assets / "default.pptx"
                if source_pptx.is_file():
                    # Copy directly from package to templates folder
                    target_file = target_path / "default.pptx"
                    with source_pptx.open("rb") as src, open(target_file, "wb") as dst:
                        dst.write(src.read())
                    clear_hidden_flag(target_file)
                    files_copied.append("default.pptx")
                    click.echo("✅ Copied: default.pptx")
                else:
                    click.echo("❌ Source template not found: default.pptx", err=True)
            except Exception as e:
                click.echo(f"❌ Failed to copy default.pptx: {e}", err=True)

            # Copy HTML color reference file
            try:
                package_assets_root = files("deckbuilder") / "assets"
                source_html = package_assets_root / "html_colors_reference.html"
                if source_html.is_file():
                    target_file = target_path / "HTML_Colors_Reference.html"
                    with source_html.open("rb") as src, open(target_file, "wb") as dst:
                        dst.write(src.read())
                    clear_hidden_flag(target_file)
                    files_copied.append("HTML_Colors_Reference.html")
                    click.echo("✅ Copied: HTML_Colors_Reference.html")
                else:
                    click.echo("⚠️ HTML color reference not found", err=True)
            except Exception as e:
                click.echo(f"⚠️ Failed to copy HTML color reference: {e}", err=True)

            if not files_copied:
                click.echo("❌ No template files found to copy", err=True)
                return

            # Generate documentation and examples
            click.echo("📝 Generating documentation and examples...")

            try:
                # Try relative import first (for package usage)
                try:
                    # Generate documentation and examples
                    from deckbuilder.cli.commands import DocumentationGenerator
                except ImportError:

                    # Fallback to absolute import (for direct script execution)
                    import sys

                    current_dir = Path(__file__).parent
                    sys.path.insert(0, str(current_dir))
                    from deckbuilder.cli.commands import DocumentationGenerator

                    # from cli_tools import DocumentationGenerator
                click.echo(f"💡 Taret location: {target_path}", err=True)
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

                click.echo(f"Template folder created at {target_path}")
                click.echo(f"Copied: {', '.join(files_copied)}")
                click.echo("Generated documentation:")
                for file in generated_files:
                    click.echo(f"   - {file}")
                click.echo()

                # Enhanced success messaging
                click.echo("🚀 Next steps:")
                click.echo("   1. Read: Getting_Started.md")
                click.echo("   2. Open: HTML_Colors_Reference.html (in browser)")
                click.echo("   3. Try: deckbuilder create example_presentation.md")
                click.echo("   4. Compare: Both example files show the same content in different formats")
                click.echo()

            except ImportError as e:
                click.echo(f"Could not generate documentation: {e}", err=True)
                click.echo("Template folder created at", target_path)
                click.echo("Copied:", ", ".join(files_copied))
                click.echo()

            # Environment variable guidance
            click.echo("💡 To make this permanent, add to your .bash_profile:")
            click.echo(f'export DECK_TEMPLATE_FOLDER="{target_path}"')
            click.echo(f'export DECK_OUTPUT_FOLDER="{target_path.parent}"')
            click.echo('export DECK_TEMPLATE_NAME="default"')
            click.echo()

            # Bash completion setup instructions
            click.echo("🔧 Optional: Enable tab completion for deckbuilder commands:")
            completion_url = "https://raw.githubusercontent.com/teknologika/deckbuilder/main/src/deckbuilder/deckbuilder-completion.bash"
            click.echo(f"   curl -o ~/.deckbuilder-completion.bash {completion_url}")
            click.echo('   echo "source ~/.deckbuilder-completion.bash" >> ~/.bash_profile')
            click.echo()
            click.echo("Then reload: source ~/.bash_profile")
            click.echo()
            click.echo("✨ After setup, you can use TAB to complete commands, templates, file paths, and directories!")

        except Exception as e:
            # Extract filename from JSON parsing errors
            error_msg = str(e)
            if "Expecting property name enclosed in double quotes" in error_msg:
                click.echo(f"⚠️ JSON parsing error in master_default_presentation.json: {e}", err=True)
            else:
                click.echo(f"⚠️ Error setting up templates: {e}", err=True)
            click.echo("💡 Make sure you have write permissions to the target directory", err=True)

    def _copy_golden_files_as_examples(self, target_path):
        """Copy master presentation files as examples with example_ prefix"""
        import json
        from importlib.resources import files

        # Copy directly from package assets without creating cache folder
        package_assets = files("deckbuilder") / "assets"
        master_md_source = package_assets / "master_default_presentation.md"
        master_json_source = package_assets / "master_default_presentation.json"

        # Update title in markdown content to showcase Deckbuilder
        try:
            if master_md_source.is_file():
                content = master_md_source.read_text(encoding="utf-8")
                # Replace test title with showcase title
                updated_content = content.replace(
                    "**Deckbuilder**: *Intelligent* PowerPoint Generation",
                    "**Deckbuilder: Intelligent PowerPoint Generation** © Bruce McLeod",
                )
                # Write to target as example_presentation.md
                with open(target_path / "example_presentation.md", "w", encoding="utf-8") as f:
                    f.write(updated_content)
        except Exception as e:
            click.echo(f"⚠️ Could not copy markdown example: {e}", err=True)

        # Update title in JSON content to showcase Deckbuilder
        try:
            if master_json_source.is_file():
                content = master_json_source.read_text(encoding="utf-8")
                json_data = json.loads(content)

                # Update first slide title if it exists
                if json_data.get("slides"):
                    first_slide = json_data["slides"][0]
                    if first_slide.get("layout") == "Title Slide":
                        placeholders = first_slide.get("placeholders", {})
                        if "title_top" in placeholders:
                            placeholders["title_top"] = "**Deckbuilder: Intelligent PowerPoint Generation** © Bruce McLeod"

                # Write to target as example_presentation.json
                with open(target_path / "example_presentation.json", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            click.echo(f"⚠️ Could not copy JSON example: {e}", err=True)

    def get_config(self):
        """Display current configuration with proper defaults and source indicators"""
        click.echo("🔧 Deckbuilder Configuration:")

        # Template folder with source indication
        template_folder = self.path_manager.get_template_folder()
        env_template_folder = os.getenv("DECK_TEMPLATE_FOLDER")

        if self.path_manager._template_folder:
            # CLI argument provided
            click.echo(f"  Template Folder: {template_folder} (CLI Argument)")
        elif env_template_folder:
            # Environment variable set
            click.echo(f"  Template Folder: {template_folder} (Environment Variable)")
        else:
            # Default fallback
            click.echo(f"  Template Folder: {template_folder} (Default)")

        # Output folder with source indication
        output_folder = self.path_manager.get_output_folder()
        env_output_folder = os.getenv("DECK_OUTPUT_FOLDER")
        if env_output_folder:
            # Check if it's the current directory to determine source
            current_dir = Path.cwd()
            if output_folder == current_dir:
                click.echo("  Output Folder: . (Default)")
            else:
                click.echo(f"  Output Folder: {output_folder} (Environment Variable)")
        else:
            click.echo("  Output Folder: . (Default)")

        # Default template with source indication
        template_name = self.path_manager.get_template_name()
        env_template_name = os.getenv("DECK_TEMPLATE_NAME")
        if env_template_name:
            if template_name == "default":
                click.echo("  Default Template: default (Default)")
            else:
                click.echo(f"  Default Template: {template_name} (Environment Variable)")
        else:
            click.echo("  Default Template: default (Default)")

        # Display language setting with description and source
        language_code = os.getenv("DECK_PROOFING_LANGUAGE")
        if language_code:
            languages = FormattingSupport.get_supported_languages()
            language_desc = languages.get(language_code, language_code)
            if language_code == "en-AU":
                click.echo(f"  Proofing Language: {language_code} ({language_desc}) (Default)")
            else:
                click.echo(f"  Proofing Language: {language_code} ({language_desc}) (Environment Variable)")
        else:
            click.echo("  Proofing Language: en-AU (English (Australia)) (Default)")

        # Display font setting with corrected message
        font_name = os.getenv("DECK_DEFAULT_FONT")
        if font_name:
            click.echo(f"  Default Font: {font_name} (Environment Variable)")
        else:
            click.echo("  Default Font: Not set (using template fonts)")

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
                click.echo(f"❌ {error_msg}", err=True)
                if suggestions:
                    click.echo(f"💡 Did you mean: {', '.join(suggestions)}?", err=True)
                click.echo("📋 Use 'deckbuilder languages' to see all supported languages", err=True)
                valid = False

        if font_name:
            is_valid, warning_msg, suggestions = formatter.validate_font_name(font_name)
            if warning_msg:
                click.echo(f"⚠️  {warning_msg}", err=True)
                if suggestions:
                    click.echo(f"💡 Similar common fonts: {', '.join(suggestions)}?", err=True)
                click.echo("ℹ️  Custom fonts will still be applied if available on the system", err=True)

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
            click.echo(f"❌ Input file not found: {input_file}", err=True)
            return False

        if not input_path.suffix.lower() == ".pptx":
            click.echo(f"❌ File must be a PowerPoint file (.pptx): {input_file}", err=True)
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
            click.echo("❌ No updates specified. Use --language or --font arguments.", err=True)
            return False

        click.echo(f"🔄 Updating {' and '.join(updates)} in: {input_file}")

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
                click.echo(f"✅ {result['message']}")
                if result["backup_path"]:
                    click.echo(f"📁 Backup created: {result['backup_path']}")

                stats = result["stats"]
                click.echo("📊 Processing Summary:")
                click.echo(f"   Master slides: {stats['master_slides_processed']}")
                click.echo(f"   Content slides: {stats['content_slides_processed']}")
                click.echo(f"   Text runs processed: {stats['total_runs_processed']}")
                if language_code:
                    click.echo(f"   Language applied: {stats['total_language_applied']} runs")
                    click.echo(f"   Text replaced: {stats['total_text_replaced']} runs")
                if font_name:
                    click.echo(f"   Font applied: {stats['total_font_applied']} runs")
                    if stats.get("theme_fonts_updated", 0) > 0:
                        click.echo(f"   Theme fonts updated: {stats['theme_fonts_updated']} (majorFont + minorFont)")
                return True
            else:
                click.echo(f"❌ {result['error']}", err=True)
                return False

        except Exception as e:
            click.echo(f"❌ Error processing presentation: {e}", err=True)
            raise

    # Pattern Management Methods

    def list_patterns(self, source: str = "all", verbose: bool = False):
        """List all available patterns with optional filtering"""
        try:
            from deckbuilder.templates.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.templates.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())
        patterns = loader.load_patterns()

        if not patterns:
            click.echo("📋 No patterns found")
            return

        click.echo(f"📋 Available Patterns ({len(patterns)} total)")
        click.echo()

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
            click.echo(f"{source_icon} {layout_name}")

            if verbose:
                description = pattern_data.get("description", "No description")
                validation = pattern_data.get("validation", {})
                required_fields = validation.get("required_fields", [])
                optional_fields = validation.get("optional_fields", [])

                click.echo(f"   Description: {description}")
                click.echo(f"   Required fields: {', '.join(required_fields) if required_fields else 'None'}")
                click.echo(f"   Optional fields: {', '.join(optional_fields) if optional_fields else 'None'}")
                click.echo()

    def validate_patterns(self, pattern_name: str = None, show_fixes: bool = False):
        """Validate pattern files and show any errors"""
        try:
            from deckbuilder.templates.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.templates.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())

        if pattern_name:
            # Validate specific pattern
            patterns = loader.load_patterns()
            if pattern_name not in patterns:
                click.echo(f"❌ Pattern '{pattern_name}' not found", err=True)
                return False

            pattern_data = patterns[pattern_name]
            errors = loader.validator.validate_pattern(pattern_data)

            if errors:
                click.echo(f"❌ Pattern '{pattern_name}' validation failed:", err=True)
                for error in errors:
                    click.echo(f"   • {error}", err=True)
                if show_fixes:
                    click.echo("\n💡 Suggestions:")
                    click.echo("   • Check that all required fields are present")
                    click.echo("   • Verify YAML syntax in examples")
                    click.echo("   • Ensure layout name matches yaml_pattern.layout")
            else:
                click.echo(f"✅ Pattern '{pattern_name}' is valid")

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
                        click.echo(f"❌ Built-in pattern {pattern_file.name} failed validation", err=True)

            # Check user patterns
            if loader.user_patterns_dir.exists():
                for pattern_file in loader.user_patterns_dir.glob("*.json"):
                    pattern_data = loader._load_pattern_file(pattern_file)
                    validation_count += 1
                    if pattern_data is None:
                        all_valid = False
                        click.echo(f"❌ User pattern {pattern_file.name} failed validation", err=True)

            if all_valid:
                click.echo(f"✅ All {validation_count} patterns are valid")
            else:
                click.echo("❌ Some patterns failed validation", err=True)
                if show_fixes:
                    click.echo("\n💡 Run with --fix flag for specific suggestions")

        return all_valid

    def show_pattern_info(self, pattern_name: str, show_example: bool = False):
        """Show detailed information about a specific pattern"""
        try:
            from deckbuilder.templates.pattern_loader import PatternLoader
        except ImportError:
            from src.deckbuilder.templates.pattern_loader import PatternLoader

        loader = PatternLoader(self.path_manager.get_template_folder())
        patterns = loader.load_patterns()

        if pattern_name not in patterns:
            click.echo(f"❌ Pattern '{pattern_name}' not found", err=True)
            available = ", ".join(sorted(patterns.keys()))
            click.echo(f"💡 Available patterns: {available}")
            return

        pattern_data = patterns[pattern_name]

        click.echo(f"📋 Pattern: {pattern_name}")
        click.echo()
        click.echo(f"Description: {pattern_data.get('description', 'No description')}")
        click.echo()

        # Show validation info
        validation = pattern_data.get("validation", {})
        required_fields = validation.get("required_fields", [])
        optional_fields = validation.get("optional_fields", [])

        click.echo("Required fields:")
        for field in required_fields:
            click.echo(f"  • {field}")

        click.echo("\nOptional fields:")
        for field in optional_fields:
            click.echo(f"  • {field}")

        if show_example:
            example = pattern_data.get("example", "")
            if example:
                click.echo("\nExample frontmatter:")
                click.echo("```yaml")
                click.echo(example)
                click.echo("```")
            else:
                click.echo("\nNo example available")

    def copy_patterns(
        self,
        copy_all: bool = False,
        pattern_name: str = None,
        overwrite: bool = False,
        backup: bool = False,
    ):
        """Copy built-in patterns to user override directory"""
        try:
            from deckbuilder.templates.pattern_loader import PatternLoader
            import shutil
            from datetime import datetime
        except ImportError:
            from src.deckbuilder.templates.pattern_loader import PatternLoader
            import shutil
            from datetime import datetime

        loader = PatternLoader(self.path_manager.get_template_folder())

        # Create user patterns directory if it doesn't exist
        loader.user_patterns_dir.mkdir(parents=True, exist_ok=True)

        if not loader.builtin_patterns_dir.exists():
            click.echo("❌ Built-in patterns directory not found", err=True)
            return False

        if not copy_all and not pattern_name:
            click.echo("❌ Must specify either --all or --pattern <name>", err=True)
            return False

        copied_count = 0

        if copy_all:
            click.echo("📋 Copying all built-in patterns to user override directory...")
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
                except Exception:  # nosec B112
                    continue

            if not pattern_files:
                click.echo(f"❌ Pattern '{pattern_name}' not found in built-in patterns", err=True)
                return False

        for pattern_file in pattern_files:
            try:
                # Load pattern to get layout name
                pattern_data = loader._load_pattern_file(pattern_file)
                if not pattern_data:
                    click.echo(f"⚠️ Skipping invalid pattern file: {pattern_file.name}", err=True)
                    continue

                layout_name = pattern_data.get("yaml_pattern", {}).get("layout")
                if not layout_name:
                    click.echo(
                        f"⚠️ Skipping pattern file without layout name: {pattern_file.name}",
                        err=True,
                    )
                    continue

                # Create target filename
                target_filename = layout_name.lower().replace(" ", "_") + ".json"
                target_path = loader.user_patterns_dir / target_filename

                # Check if file exists
                if target_path.exists() and not overwrite:
                    click.echo(
                        f"⚠️ User pattern '{layout_name}' already exists (use --overwrite to replace)",
                        err=True,
                    )
                    continue

                # Create backup if requested
                if backup and target_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_path = target_path.with_suffix(f".backup_{timestamp}.json")
                    shutil.copy2(target_path, backup_path)
                    click.echo(f"💾 Created backup: {backup_path.name}")

                # Copy the pattern file
                shutil.copy2(pattern_file, target_path)
                click.echo(f"✅ Copied: {layout_name} → {target_filename}")
                copied_count += 1

            except Exception as e:
                click.echo(f"❌ Error copying {pattern_file.name}: {e}", err=True)

        if copied_count > 0:
            click.echo(f"\n✅ Successfully copied {copied_count} pattern(s)")
            click.echo(f"📁 Location: {loader.user_patterns_dir}")
            click.echo("\n💡 You can now customize these patterns to override built-in behavior")
        else:
            click.echo("❌ No patterns were copied", err=True)

        return copied_count > 0

    def show_completion_help(self):
        """Show tab completion installation instructions"""
        click.echo("🔧 Tab Completion Setup")
        click.echo()
        click.echo("To enable tab completion for deckbuilder commands:")
        click.echo()
        click.echo("1. Download the completion script:")
        completion_url = "https://raw.githubusercontent.com/teknologika/deckbuilder/main/src/deckbuilder/deckbuilder-completion.bash"
        click.echo(f"   curl -o ~/.deckbuilder-completion.bash {completion_url}")
        click.echo()
        click.echo("2. Add to your .bash_profile:")
        click.echo('   echo "source ~/.deckbuilder-completion.bash" >> ~/.bash_profile')
        click.echo()
        click.echo("3. Reload your shell:")
        click.echo("   source ~/.bash_profile")
        click.echo()
        click.echo("✨ After setup, you can use TAB to complete:")
        click.echo("   • Commands: deckbuilder <TAB>")
        click.echo("   • Template names: deckbuilder analyze <TAB>")
        click.echo("   • File paths: deckbuilder create <TAB>")
        click.echo("   • Directory navigation: deckbuilder create docs/<TAB>")
        click.echo("   • Output paths: deckbuilder create file.md -o outputs/<TAB>")
        click.echo("   • Global flags: deckbuilder -<TAB>")
        click.echo()
        click.echo("For system-wide installation:")
        click.echo("   sudo curl -o /etc/bash_completion.d/deckbuilder \\")
        click.echo(f"        {completion_url}")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-t", "--template-folder", metavar="PATH", help="Template folder path.")
@click.option("-l", "--language", metavar="LANG", envvar="DECK_PROOFING_LANGUAGE", help="Proofing language (e.g., en-US).")
@click.option("-f", "--font", metavar="FONT", envvar="DECK_DEFAULT_FONT", help='Default font family (e.g., "Calibri").')
@click.version_option(package_name="deckbuilder", prog_name="Deckbuilder")
@click.pass_context
def main(ctx, template_folder, language, font):
    """Deckbuilder CLI - Intelligent PowerPoint presentation generation."""
    ctx.obj = DeckbuilderCLI(template_folder=template_folder, language=language, font=font)


@main.command()
@click.argument("command_name", required=False)
@click.option("--env", is_flag=True, help="Show environment variables.")
@click.pass_context
def help(ctx, command_name, env):
    """Show help for commands."""
    if command_name:
        # Show help for specific command or group
        cmd = main.get_command(ctx, command_name)
        if cmd:
            click.echo(cmd.get_help(ctx))
        else:
            click.echo(f"No such command '{command_name}'.")
            click.echo("Available commands:")
            for cmd_name in main.list_commands(ctx):
                click.echo(f"  {cmd_name}")
    else:
        # Show general help
        click.echo(main.get_help(ctx))

        # Always show version info
        click.echo()
        _show_version_info()

        # Show environment variables if requested or always for main help
        click.echo()
        _show_environment_info()


def _show_version_info():
    """Show version information."""
    try:
        from importlib.metadata import version

        deckbuilder_version = version("deckbuilder")
    except Exception:
        deckbuilder_version = "unknown"

    click.echo("📋 Version Information:")
    click.echo(f"   Deckbuilder: {deckbuilder_version}")


def _show_environment_info():
    """Show environment variable information."""
    import os

    click.echo("🌍 Environment Variables:")

    # Core path variables
    env_vars = [
        ("DECK_TEMPLATE_FOLDER", "Template folder location"),
        ("DECK_OUTPUT_FOLDER", "Output folder location"),
        ("DECK_TEMPLATE_NAME", "Default template name"),
        ("DECK_ASSET_CACHE_DIR", "Asset cache directory"),
    ]

    # Formatting variables
    formatting_vars = [
        ("DECK_PROOFING_LANGUAGE", "Default proofing language"),
        ("DECK_DEFAULT_FONT", "Default font family"),
    ]

    # Debug variables
    debug_vars = [
        ("DECKBUILDER_DEBUG", "Debug mode"),
        ("DECKBUILDER_QUIET", "Quiet mode"),
        ("DECKBUILDER_VALIDATION_DEBUG", "Validation debug"),
        ("DECKBUILDER_SLIDE_DEBUG", "Slide debug"),
        ("DECKBUILDER_CONTENT_DEBUG", "Content debug"),
    ]

    def show_var_group(title, var_list):
        click.echo(f"   {title}:")
        for var_name, _ in var_list:
            value = os.getenv(var_name)
            if value:
                click.echo(f"     {var_name}={value}")
            else:
                click.echo(f"     {var_name}=<not set>")

    show_var_group("Core", env_vars)
    show_var_group("Formatting", formatting_vars)
    show_var_group("Debug", debug_vars)


@main.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", help="Output filename (without extension).")
@click.option("--template", help="Template name to use (default: 'default').")
@click.pass_obj
def create(cli, input_file, output, template):
    """Generate presentations from markdown or JSON."""
    cli.create_presentation(input_file, output, template)


@main.group()
def template():
    """Manage PowerPoint templates and mappings."""
    pass


@template.command()
@click.argument("template_name", default="default")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
@click.pass_obj
def analyze(cli, template_name, verbose):
    """Analyze template structure and placeholders."""
    cli.analyze_template(template_name, verbose=verbose)


@template.command()
@click.argument("template_name", default="default")
@click.pass_obj
def validate(cli, template_name):
    """Validate template and JSON mappings."""
    cli.validate_template(template_name)


@template.command()
@click.argument("template_name", default="default")
@click.option("--output", "-o", help="Output documentation file.")
@click.pass_obj
def document(cli, template_name, output):
    """Generate comprehensive template documentation."""
    cli.document_template(template_name, output)


@template.command()
@click.argument("template_name", default="default")
@click.option("--mapping", help="Custom mapping file.")
@click.option("--no-backup", is_flag=True, help="Skip backup creation.")
@click.option("--use-conventions/--no-conventions", default=True, help="Use naming conventions.")
@click.pass_obj
def enhance(cli, template_name, mapping, no_backup, use_conventions):
    """Enhance template with corrected placeholders."""
    cli.enhance_template(template_name, mapping, not no_backup, use_conventions)


@template.command(name="list")
@click.pass_obj
def list_templates(cli):
    """List all available templates."""
    cli.list_templates()


@main.group()
def pattern():
    """Manage structured frontmatter patterns."""
    pass


@pattern.command(name="list")
@click.option(
    "--source",
    type=click.Choice(["all", "builtin", "user"]),
    default="all",
    help="Pattern source filter.",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed pattern information.")
@click.pass_obj
def list_patterns(cli, source, verbose):
    """List all available patterns."""
    cli.list_patterns(source, verbose)


@pattern.command()
@click.argument("pattern_name", required=False)
@click.option("--fix", is_flag=True, help="Show suggestions for fixing validation errors.")
@click.pass_obj
def validate_pattern(cli, pattern_name, fix):
    """Validate pattern files and schema."""
    cli.validate_patterns(pattern_name, fix)


@pattern.command()
@click.argument("pattern_name")
@click.option("--example", is_flag=True, help="Show example frontmatter.")
@click.pass_obj
def info(cli, pattern_name, example):
    """Show detailed information about a pattern."""
    cli.show_pattern_info(pattern_name, example)


@pattern.command()
@click.option("--all", "copy_all", is_flag=True, help="Copy all built-in patterns.")
@click.option("--pattern", "pattern_name", help="Copy specific pattern by name.")
@click.option("--overwrite", is_flag=True, help="Overwrite existing user patterns.")
@click.option("--backup", is_flag=True, help="Create backup of existing patterns.")
@click.pass_obj
def copy(cli, copy_all, pattern_name, overwrite, backup):
    """Copy built-in patterns to user override directory."""
    cli.copy_patterns(copy_all, pattern_name, overwrite, backup)


@main.group()
def image():
    """Process and generate images with PlaceKitten."""
    pass


@image.command()
@click.argument("width", type=int)
@click.argument("height", type=int)
@click.option("--id", "image_id", type=int, help="Specific kitten image ID (1-6).")
@click.option("--filter", "filter_type", help="Filter to apply (grayscale, sepia, blur, etc.).")
@click.option("--output", "-o", help="Output filename.")
@click.pass_obj
def generate(cli, width, height, image_id, filter_type, output):
    """Generate PlaceKitten placeholder images."""
    cli.generate_placeholder_image(width, height, image_id, filter_type, output)


@image.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("width", type=int)
@click.argument("height", type=int)
@click.option("--save-steps", is_flag=True, help="Save processing steps.")
@click.option("--output", "-o", help="Output filename.")
@click.pass_obj
def crop(cli, input_file, width, height, save_steps, output):
    """Smart crop existing images."""
    cli.smart_crop_image(input_file, width, height, save_steps, output)


@main.group(name="config")
def config_group():
    """Configuration, setup, and system information."""
    pass


@config_group.command()
@click.pass_obj
def show(cli):
    """Show current configuration."""
    cli.get_config()


@config_group.command()
def languages():
    """List supported languages."""
    print_supported_languages()


@config_group.command()
@click.pass_obj
def completion(cli):
    """Setup bash completion."""
    cli.show_completion_help()


@main.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--language", "-l", metavar="LANG", envvar="DECK_PROOFING_LANGUAGE", help="Language code to apply.")
@click.option("--font", "-f", metavar="FONT", envvar="DECK_DEFAULT_FONT", help="Font family to apply.")
@click.option("--output", "-o", metavar="FILE", help="Output file path.")
@click.option("--no-backup", is_flag=True, help="Skip creating backup file.")
@click.pass_obj
def remap(cli, input_file, language, font, output, no_backup):
    """Update language and font settings in existing PowerPoint files."""
    success = cli.remap_presentation(input_file, language, font, output, not no_backup)
    if not success:
        sys.exit(1)


@main.command()
@click.argument("path", type=click.Path(), default="./templates")
@click.pass_obj
def init(cli, path):
    """Initialize template folder with default files."""
    cli.init_templates(path)


if __name__ == "__main__":
    main()
