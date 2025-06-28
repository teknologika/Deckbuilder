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
    from placekitten import PlaceKitten
except ImportError:
    # Fallback to development imports (when running from source)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    sys.path.insert(0, str(project_root))

    from src.deckbuilder.engine import Deckbuilder  # noqa: E402
    from src.deckbuilder.cli_tools import TemplateManager  # noqa: E402
    from src.placekitten import PlaceKitten  # noqa: E402


class DeckbuilderCLI:
    """Standalone Deckbuilder command-line interface"""

    def __init__(self, templates_path=None, output_path=None):
        self.setup_environment(templates_path, output_path)

    def setup_environment(self, templates_path=None, output_path=None):
        """Setup environment variables with priority: CLI args > env vars > defaults"""

        # Template folder resolution priority
        if templates_path:
            # 1. CLI argument has highest priority
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(templates_path).resolve())
        elif not os.getenv("DECK_TEMPLATE_FOLDER"):
            # 2. Environment variable already set (skip)
            # 3. Default location: ./templates/
            default_templates = Path.cwd() / "templates"
            if default_templates.exists():
                os.environ["DECK_TEMPLATE_FOLDER"] = str(default_templates)
            else:
                # Will trigger error message in commands that need templates
                pass

        # Output folder resolution priority
        if output_path:
            # 1. CLI argument has highest priority
            output_folder = Path(output_path)
            output_folder.mkdir(parents=True, exist_ok=True)
            os.environ["DECK_OUTPUT_FOLDER"] = str(output_folder.resolve())
        elif not os.getenv("DECK_OUTPUT_FOLDER"):
            # 2. Environment variable already set (skip)
            # 3. Default location: current directory
            os.environ["DECK_OUTPUT_FOLDER"] = str(Path.cwd())

        # Default template name
        if not os.getenv("DECK_TEMPLATE_NAME"):
            os.environ["DECK_TEMPLATE_NAME"] = "default"

    def _validate_templates_folder(self):
        """Validate templates folder exists and provide helpful error message"""
        template_folder = os.getenv("DECK_TEMPLATE_FOLDER")
        if not template_folder or not Path(template_folder).exists():
            print("❌ Template folder not found: ./templates/")
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

    def create_presentation(
        self, input_file: str, output_name: Optional[str] = None, template: Optional[str] = None
    ) -> str:
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

        # Set template if provided
        if template:
            os.environ["DECK_TEMPLATE_NAME"] = template

        # Initialize Deckbuilder
        db = Deckbuilder()

        try:
            if input_path.suffix.lower() == ".md":
                # Process markdown file
                content = input_path.read_text(encoding="utf-8")
                result = db.create_presentation_from_markdown(
                    markdown_content=content, fileName=output_name
                )
            elif input_path.suffix.lower() == ".json":
                # Process JSON file
                with open(input_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                result = db.create_presentation(json_data=json_data, fileName=output_name)
            else:
                raise ValueError(
                    f"Unsupported file format: {input_path.suffix}. "
                    "Supported formats: .md, .json"
                )

            print(f"✅ Presentation created successfully: {result}")
            return result

        except Exception as e:
            print(f"❌ Error creating presentation: {e}")
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
            # Generate image with optional parameters
            image = pk.generate(
                width=width, height=height, image_id=image_id, filter_type=filter_type
            )

            # Set output filename
            if not output_file:
                filter_suffix = f"_{filter_type}" if filter_type else ""
                id_suffix = f"_id{image_id}" if image_id else ""
                output_file = f"placeholder_{width}x{height}{id_suffix}{filter_suffix}.jpg"

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
            result_processor = processor.smart_crop(
                width=width, height=height, save_steps=save_steps, output_prefix="smart_crop"
            )

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
            # Find the package assets (development structure)
            assets_path = Path(__file__).parent.parent.parent / "assets" / "templates"
            if assets_path.exists():
                source_pptx = assets_path / "default.pptx"
                source_json = assets_path / "default.json"
            else:
                print("❌ Could not locate template assets")
                print("💡 Default templates not found in package")
                return

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

            # Success message
            print(f"✅ Template folder created at {target_path}")
            print(f"📁 Copied: {', '.join(files_copied)}")
            print()

            # Environment variable guidance
            print("💡 To make this permanent, add to your .bash_profile:")
            print(f'export DECK_TEMPLATE_FOLDER="{target_path}"')
            print(f'export DECK_OUTPUT_FOLDER="{target_path.parent}"')
            print('export DECK_TEMPLATE_NAME="default"')
            print()
            print("Then reload: source ~/.bash_profile")
            print()
            print("🚀 Ready to use! Try: deckbuilder create example.md")

        except Exception as e:
            print(f"❌ Error setting up templates: {e}")
            print("💡 Make sure you have write permissions to the target directory")

    def get_config(self):
        """Display current configuration"""
        print("🔧 Deckbuilder Configuration:")
        print(f"  Template Folder: {os.getenv('DECK_TEMPLATE_FOLDER', 'Not set')}")
        print(f"  Output Folder: {os.getenv('DECK_OUTPUT_FOLDER', 'Not set')}")
        print(f"  Default Template: {os.getenv('DECK_TEMPLATE_NAME', 'Not set')}")

    def show_completion_help(self):
        """Show tab completion installation instructions"""
        print("🔧 Tab Completion Setup")
        print()
        print("To enable tab completion for deckbuilder commands:")
        print()
        print("1. Download the completion script:")
        completion_url = (
            "https://raw.githubusercontent.com/teknologika/deckbuilder/main/"
            "deckbuilder-completion.bash"
        )
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
        print("   • Global flags: deckbuilder -<TAB>")
        print()
        print("For system-wide installation:")
        print("   sudo curl -o /etc/bash_completion.d/deckbuilder")
        print(f"        {completion_url}")


def create_parser():
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        prog="deckbuilder",
        description="Deckbuilder CLI - Intelligent PowerPoint presentation generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create presentation from markdown
  deckbuilder create presentation.md
  deckbuilder -t ~/templates -o ~/output create slides.md

  # Template management
  deckbuilder analyze default --verbose
  deckbuilder validate default
  deckbuilder document default --output template_docs.md

  # Image generation
  deckbuilder image 800 600 --filter grayscale --output placeholder.jpg
  deckbuilder crop input.jpg 1920 1080 --save-steps

  # Configuration and setup
  deckbuilder config
  deckbuilder templates
  deckbuilder completion
  deckbuilder init
        """,
    )

    # Global arguments (apply to all commands)
    parser.add_argument(
        "-t", "--templates", metavar="PATH", help="Template folder path (default: ./templates/)"
    )
    parser.add_argument(
        "-o", "--output", metavar="PATH", help="Output folder path (default: current directory)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create presentation command
    create_parser = subparsers.add_parser(
        "create", help="Create presentation from markdown or JSON file"
    )
    create_parser.add_argument("input_file", help="Input markdown (.md) or JSON (.json) file")
    create_parser.add_argument("--output", "-o", help="Output filename (without extension)")
    create_parser.add_argument("--template", "-t", help="Template name to use (default: 'default')")

    # Template analysis commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze template structure")
    analyze_parser.add_argument("template", nargs="?", default="default", help="Template name")
    analyze_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    validate_parser = subparsers.add_parser("validate", help="Validate template and mappings")
    validate_parser.add_argument("template", nargs="?", default="default", help="Template name")

    document_parser = subparsers.add_parser("document", help="Generate template documentation")
    document_parser.add_argument("template", nargs="?", default="default", help="Template name")
    document_parser.add_argument("--output", "-o", help="Output documentation file")

    enhance_parser = subparsers.add_parser("enhance", help="Enhance template placeholders")
    enhance_parser.add_argument("template", nargs="?", default="default", help="Template name")
    enhance_parser.add_argument("--mapping", help="Custom mapping file")
    enhance_parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    enhance_parser.add_argument(
        "--no-conventions",
        action="store_false",
        dest="use_conventions",
        help="Don't use naming conventions",
    )

    # PlaceKitten image generation
    image_parser = subparsers.add_parser("image", help="Generate placeholder image")
    image_parser.add_argument("width", type=int, help="Image width")
    image_parser.add_argument("height", type=int, help="Image height")
    image_parser.add_argument("--id", type=int, help="Specific kitten image ID (1-6)")
    image_parser.add_argument("--filter", help="Filter to apply (grayscale, sepia, blur, etc.)")
    image_parser.add_argument("--output", "-o", help="Output filename")

    # Smart crop command
    crop_parser = subparsers.add_parser("crop", help="Apply smart cropping to image")
    crop_parser.add_argument("input_file", help="Input image file")
    crop_parser.add_argument("width", type=int, help="Target width")
    crop_parser.add_argument("height", type=int, help="Target height")
    crop_parser.add_argument("--save-steps", action="store_true", help="Save processing steps")
    crop_parser.add_argument("--output", "-o", help="Output filename")

    # Configuration commands
    subparsers.add_parser("config", help="Show current configuration")
    subparsers.add_parser("templates", help="List available templates")
    subparsers.add_parser("completion", help="Show tab completion setup instructions")

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize template folder with default files"
    )
    init_parser.add_argument(
        "path", nargs="?", default="./templates", help="Template folder path (default: ./templates)"
    )

    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize CLI with global arguments
    cli = DeckbuilderCLI(templates_path=args.templates, output_path=args.output)

    try:
        # Route commands
        if args.command == "create":
            cli.create_presentation(
                input_file=args.input_file, output_name=args.output, template=args.template
            )

        elif args.command == "analyze":
            cli.analyze_template(args.template, verbose=args.verbose)

        elif args.command == "validate":
            cli.validate_template(args.template)

        elif args.command == "document":
            cli.document_template(args.template, args.output)

        elif args.command == "enhance":
            cli.enhance_template(
                template_name=args.template,
                mapping_file=args.mapping,
                no_backup=args.no_backup,
                use_conventions=args.use_conventions,
            )

        elif args.command == "image":
            cli.generate_placeholder_image(
                width=args.width,
                height=args.height,
                image_id=args.id,
                filter_type=args.filter,
                output_file=args.output,
            )

        elif args.command == "crop":
            cli.smart_crop_image(
                input_file=args.input_file,
                width=args.width,
                height=args.height,
                save_steps=args.save_steps,
                output_file=args.output,
            )

        elif args.command == "config":
            cli.get_config()

        elif args.command == "templates":
            cli.list_templates()

        elif args.command == "completion":
            cli.show_completion_help()

        elif args.command == "init":
            cli.init_templates(args.path)

    except Exception as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
