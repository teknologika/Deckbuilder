#!/usr/bin/env python3
"""
Test script for tools.py template analyzer.
"""

import os
import sys
import shutil
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server.tools import analyze_pptx_template
from deckbuilder.engine import get_deckbuilder_client


def setup_test_environment():
    """Set up test environment with folders and template."""
    test_dir = os.path.dirname(__file__)

    # Create test folders
    templates_folder = os.path.join(test_dir, "..", "assets", "templates")
    output_folder = os.path.join(test_dir, "output")

    # Clean output directory if it exists
    if os.path.exists(output_folder):
        print(f"Cleaning output directory: {output_folder}")
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"  Removed: {filename}")
            except Exception as e:
                print(f"  Failed to remove {filename}: {e}")

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    # Set environment variables
    os.environ["DECK_TEMPLATE_FOLDER"] = templates_folder
    os.environ["DECK_OUTPUT_FOLDER"] = output_folder

    print(f"Template folder: {templates_folder}")
    print(f"Output folder: {output_folder}")

    return templates_folder, output_folder


def test_analyze_template():
    """Test the template analyzer."""
    try:
        _, output_folder = setup_test_environment()

        # Test analyzing the default template
        print("\nAnalyzing default.pptx template...")
        result = analyze_pptx_template("default")

        print("\nRaw Template Structure:")
        print(json.dumps(result, indent=2))

        # Check if output file was created
        output_file = os.path.join(output_folder, "default.g.json")
        if os.path.exists(output_file):
            print(f"\n✓ Generated mapping file: {output_file}")
            print("  Rename to 'default.json' when ready to use with deckbuilder")
        else:
            print("✗ Output file was not created")

        return result

    except Exception as e:
        print(f"Error during test: {str(e)}")
        return None


def test_presentation_creation(testInputFile: str):
    """Test creating a presentation from JSON with inline formatting and all placeholders."""
    try:
        _, output_folder = setup_test_environment()

        # Load test JSON file
        test_dir = os.path.dirname(__file__)
        test_json_path = os.path.join(test_dir, testInputFile)

        if not os.path.exists(test_json_path):
            print(f"✗ Test JSON file not found: {test_json_path}")
            return None

        with open(test_json_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)

        print(f"\nLoaded test data with {len(test_data['presentation']['slides'])} slides")

        # Get deckbuilder client
        deck = get_deckbuilder_client()

        # Create presentation using default template
        print("\nCreating test presentation...")
        result = deck.create_presentation("default", "test_json")
        print(result)

        # Add all slides from test JSON
        print("\nAdding slides...")
        slide_count = 0
        for slide_data in test_data["presentation"]["slides"]:
            try:
                result = deck.add_slide_from_json(slide_data)
                slide_count += 1
                print(
                    f"  ✓ Added slide {slide_count}: {slide_data.get('type', 'unknown')} - {slide_data.get('title', 'no title')[:50]}..."
                )
            except Exception as e:
                print(f"  ✗ Failed to add slide {slide_count + 1}: {str(e)}")

        # Save presentation
        print(f"\nSaving presentation with {slide_count} slides...")
        result = deck.write_presentation("test_json")
        print(result)

        # Check if file was created
        output_files = [
            f
            for f in os.listdir(output_folder)
            if f.startswith("test_json") and f.endswith(".g.pptx")
        ]
        if output_files:
            latest_file = sorted(output_files)[-1]
            print(f"✓ Test presentation created: {latest_file}")
            print(f"  Location: {os.path.join(output_folder, latest_file)}")
            print(f"  Contains {slide_count} slides with inline formatting and placeholder content")
        else:
            print("✗ Test presentation file was not created")

        return True

    except Exception as e:
        print(f"Error during presentation test: {str(e)}")
        return None


def test_markdown_presentation(testInputFile: str):
    """Test creating a presentation from markdown with frontmatter and inline formatting."""
    try:
        _, output_folder = setup_test_environment()

        # Load test markdown file
        test_dir = os.path.dirname(__file__)
        test_md_path = os.path.join(test_dir, testInputFile)

        if not os.path.exists(test_md_path):
            print(f"✗ Test markdown file not found: {test_md_path}")
            return None

        with open(test_md_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Count slides in markdown (count frontmatter blocks)
        slide_count = markdown_content.count("---\nlayout:")
        print(f"\nLoaded markdown with {slide_count} slides")

        # Get deckbuilder client
        deck = get_deckbuilder_client()

        # Create presentation from markdown
        print("\nCreating presentation from markdown...")
        result = deck.create_presentation_from_markdown(
            markdown_content=markdown_content, fileName="test_markdown", templateName="default"
        )
        print(result)

        # Check if file was created
        output_files = [
            f
            for f in os.listdir(output_folder)
            if f.startswith("test_markdown") and f.endswith(".g.pptx")
        ]
        if output_files:
            latest_file = sorted(output_files)[-1]
            print(f"✓ Markdown presentation created: {latest_file}")
            print(f"  Location: {os.path.join(output_folder, latest_file)}")
            print(
                f"  Contains {slide_count} slides with markdown formatting and frontmatter layouts"
            )

            # Show what layouts were used
            layouts_used = []
            lines = markdown_content.split("\n")
            for line in lines:
                if line.startswith("layout:"):
                    layout = line.replace("layout:", "").strip()
                    layouts_used.append(layout)

            if layouts_used:
                print(f"  Layouts used: {', '.join(set(layouts_used))}")
        else:
            print("✗ Markdown presentation file was not created")

        return True

    except Exception as e:
        print(f"Error during markdown test: {str(e)}")
        return None


def test_analyze_template_no_cleanup():
    """Test the template analyzer without cleaning output directory."""
    try:
        # Use existing environment setup without cleanup
        templates_folder = os.environ.get("DECK_TEMPLATE_FOLDER")
        output_folder = os.environ.get("DECK_OUTPUT_FOLDER")

        if not templates_folder or not output_folder:
            print("Environment not set up. Call setup_test_environment() first.")
            return None

        # Test analyzing the default template
        print("\nAnalyzing default.pptx template...")
        result = analyze_pptx_template("default")

        # Check if output file was created
        output_file = os.path.join(output_folder, "default.g.json")
        if os.path.exists(output_file):
            print(f"\n✓ Generated mapping file: {output_file}")
            print("  Rename to 'default.json' when ready to use with deckbuilder")
        else:
            print("✗ Output file was not created")

        return result

    except Exception as e:
        print(f"Error during test: {str(e)}")
        return None


def test_presentation_creation_no_cleanup(testInputFile: str):
    """Test creating a presentation from JSON without cleaning output directory."""
    try:
        # Use existing environment setup
        output_folder = os.environ.get("DECK_OUTPUT_FOLDER")

        if not output_folder:
            print("Environment not set up. Call setup_test_environment() first.")
            return None

        # Load test JSON file
        test_dir = os.path.dirname(__file__)
        test_json_path = os.path.join(test_dir, testInputFile)

        if not os.path.exists(test_json_path):
            print(f"✗ Test JSON file not found: {test_json_path}")
            return None

        with open(test_json_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)

        print(f"\nLoaded test data with {len(test_data['presentation']['slides'])} slides")

        # Get deckbuilder client
        deck = get_deckbuilder_client()

        # Create presentation using default template
        print("\nCreating test presentation...")
        result = deck.create_presentation("default", "test_json")
        print(result)

        # Add all slides from test JSON
        print("\nAdding slides...")
        slide_count = 0
        for slide_data in test_data["presentation"]["slides"]:
            try:
                result = deck.add_slide_from_json(slide_data)
                slide_count += 1
                print(
                    f"  ✓ Added slide {slide_count}: {slide_data.get('type', 'unknown')} - {slide_data.get('title', 'no title')[:50]}..."
                )
            except Exception as e:
                print(f"  ✗ Failed to add slide {slide_count + 1}: {str(e)}")

        # Save presentation
        print(f"\nSaving presentation with {slide_count} slides...")
        result = deck.write_presentation("test_json")
        print(result)

        # Check if file was created
        output_files = [
            f
            for f in os.listdir(output_folder)
            if f.startswith("test_json") and f.endswith(".g.pptx")
        ]
        if output_files:
            latest_file = sorted(output_files)[-1]
            print(f"✓ Test presentation created: {latest_file}")
            print(f"  Location: {os.path.join(output_folder, latest_file)}")
            print(f"  Contains {slide_count} slides with inline formatting and placeholder content")
        else:
            print("✗ Test presentation file was not created")

        return True

    except Exception as e:
        print(f"Error during presentation test: {str(e)}")
        return None


def test_markdown_presentation_no_cleanup(testInputFile: str):
    """Test creating a presentation from markdown without cleaning output directory."""
    try:
        # Use existing environment setup
        output_folder = os.environ.get("DECK_OUTPUT_FOLDER")

        if not output_folder:
            print("Environment not set up. Call setup_test_environment() first.")
            return None

        # Load test markdown file
        test_dir = os.path.dirname(__file__)
        test_md_path = os.path.join(test_dir, testInputFile)

        if not os.path.exists(test_md_path):
            print(f"✗ Test markdown file not found: {test_md_path}")
            return None

        with open(test_md_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Count slides in markdown (count frontmatter blocks)
        slide_count = markdown_content.count("---\nlayout:")
        print(f"\nLoaded markdown with {slide_count} slides")

        # Get deckbuilder client
        deck = get_deckbuilder_client()

        # Create presentation from markdown
        print("\nCreating presentation from markdown...")
        result = deck.create_presentation_from_markdown(
            markdown_content=markdown_content, fileName="test_markdown", templateName="default"
        )
        print(result)

        # Check if file was created
        output_files = [
            f
            for f in os.listdir(output_folder)
            if f.startswith("test_markdown") and f.endswith(".g.pptx")
        ]
        if output_files:
            latest_file = sorted(output_files)[-1]
            print(f"✓ Markdown presentation created: {latest_file}")
            print(f"  Location: {os.path.join(output_folder, latest_file)}")
            print(
                f"  Contains {slide_count} slides with markdown formatting and frontmatter layouts"
            )

            # Show what layouts were used
            layouts_used = []
            lines = markdown_content.split("\n")
            for line in lines:
                if line.startswith("layout:"):
                    layout = line.replace("layout:", "").strip()
                    layouts_used.append(layout)

            if layouts_used:
                print(f"  Layouts used: {', '.join(set(layouts_used))}")
        else:
            print("✗ Markdown presentation file was not created")

        return True

    except Exception as e:
        print(f"Error during markdown test: {str(e)}")
        return None


def run_all_tests():
    """Run all available tests."""
    print("=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)

    # Clean output directory once at the start
    print("\n" + "─" * 30)
    print("SETUP: Cleaning Output Directory")
    print("─" * 30)
    setup_test_environment()

    # Test 1: JSON Presentation Creation
    print("\n" + "─" * 30)
    print("TEST 1: JSON Presentation Creation")
    print("─" * 30)
    test_presentation_creation_no_cleanup("test_comprehensive_layouts.json")

    # Test 2: Markdown Presentation Creation (All 19 Layouts)
    print("\n" + "─" * 30)
    print("TEST 2: Markdown Presentation Creation (All 19 Layouts)")
    print("─" * 30)
    test_markdown_presentation_no_cleanup("test_comprehensive_layouts.md")

    print("\n" + "─" * 30)
    print("OUTPUT FILES PRESERVED FOR MANUAL REVIEW")
    print("─" * 30)

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        run_all_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "json":
        test_presentation_creation("test_comprehensive_layouts.json")
    elif len(sys.argv) > 1 and sys.argv[1] == "markdown":
        test_markdown_presentation("test_comprehensive_layouts.md")
    elif len(sys.argv) > 1 and sys.argv[1] == "presentation":
        # For backward compatibility, run both presentation tests
        print("Running both JSON and Markdown presentation tests...\n")
        test_presentation_creation("test_comprehensive_layouts.json")
        print("\n" + "─" * 50 + "\n")
        test_markdown_presentation("test_comprehensive_layouts.md")
    else:
        test_analyze_template()
