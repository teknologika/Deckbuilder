#!/usr/bin/env python3
"""
Master Examples Generator Script

This script automatically generates master JSON and Markdown files containing all
structured frontmatter examples in the correct template order. Run this script
whenever new layout examples are added to maintain synchronized master files.

Usage:
    python scripts/generate_master_examples.py

Output:
    - master_examples.json - All examples in template order (JSON format)
    - master_examples.md - All examples in template order (Markdown format)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from pptx import Presentation


class MasterExamplesGenerator:
    """Generates master example files from individual test examples."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_files_dir = self.project_root / "src/deckbuilder/structured_frontmatter_patterns/test_files"
        self.templates_dir = self.project_root / "templates"
        self.output_dir = self.project_root
        self.assets_dir = self.project_root / "src/deckbuilder/assets"

        # Ensure directories exist
        if not self.test_files_dir.exists():
            raise FileNotFoundError(f"Test files directory not found: {self.test_files_dir}")
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

    def get_template_layout_order(self, template_name: str = "default") -> List[str]:
        """
        Get the layout order from the PowerPoint template.

        Args:
            template_name: Name of template (without .pptx extension)

        Returns:
            List of layout names in template order
        """
        template_path = self.templates_dir / f"{template_name}.pptx"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        try:
            prs = Presentation(str(template_path))
            layout_order = [layout.name for layout in prs.slide_layouts]
            print(f"📋 Found {len(layout_order)} layouts in template: {template_name}.pptx")
            return layout_order
        except Exception as e:
            raise RuntimeError(f"Failed to read template {template_path}: {e}")

    def discover_example_files(self) -> Dict[str, Tuple[Path, Path]]:
        """
        Discover all example JSON and Markdown files.

        Returns:
            Dict mapping layout names to (json_path, md_path) tuples
        """
        examples = {}
        json_files = list(self.test_files_dir.glob("example_*.json"))

        for json_file in json_files:
            # Extract layout name from filename: example_title_slide.json -> title_slide
            layout_key = json_file.stem.replace("example_", "")
            md_file = json_file.with_suffix(".md")

            if md_file.exists():
                examples[layout_key] = (json_file, md_file)
            else:
                print(f"⚠️  Warning: Missing markdown file for {json_file.name}")

        print(f"📁 Discovered {len(examples)} complete example pairs")
        return examples

    def load_example_data(self, json_path: Path, md_path: Path) -> Dict[str, Any]:
        """
        Load example data from JSON and Markdown files.

        Args:
            json_path: Path to JSON example file
            md_path: Path to Markdown example file

        Returns:
            Combined example data with metadata
        """
        try:
            # Load JSON data
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Load Markdown content
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # Extract layout from JSON (first slide)
            slides = json_data.get("slides", [])
            layout_name = slides[0].get("layout") if slides else "Unknown"

            return {"layout": layout_name, "json_data": json_data, "markdown_content": md_content, "json_filename": json_path.name, "md_filename": md_path.name}
        except Exception as e:
            raise RuntimeError(f"Failed to load example data from {json_path}: {e}")

    def map_examples_to_layouts(self, examples: Dict[str, Tuple[Path, Path]], layout_order: List[str]) -> List[Dict[str, Any]]:
        """
        Map examples to template layouts and order them correctly.
        Select ONLY ONE example per layout for clean output.

        Args:
            examples: Dict of example files by layout key
            layout_order: Template layout order

        Returns:
            List of example data in template order (one per layout)
        """
        ordered_examples = []
        layout_to_examples = {}

        # First, load all example data and group by actual layout name
        for _layout_key, (json_path, md_path) in examples.items():
            example_data = self.load_example_data(json_path, md_path)
            actual_layout = example_data["layout"]

            if actual_layout not in layout_to_examples:
                layout_to_examples[actual_layout] = []
            layout_to_examples[actual_layout].append(example_data)

        # Order examples according to template layout order - ONE PER LAYOUT
        for template_layout in layout_order:
            if template_layout in layout_to_examples:
                # Select the best example (prefer longer content, more comprehensive)
                examples_for_layout = layout_to_examples[template_layout]
                if len(examples_for_layout) > 1:
                    # Sort by content length and pick the most comprehensive
                    best_example = max(examples_for_layout, key=lambda x: len(str(x.get("json_data", {}).get("slides", [{}])[0].get("placeholders", {}))))
                    print(f"✅ Selected best: {best_example['json_filename']} → {template_layout} (from {len(examples_for_layout)} options)")
                else:
                    best_example = examples_for_layout[0]
                    print(f"✅ Mapped: {best_example['json_filename']} → {template_layout}")

                ordered_examples.append(best_example)

        # Report any unmapped layouts
        all_mapped_layouts = {example["layout"] for example in ordered_examples}
        all_template_layouts = set(layout_order)
        unmapped = all_template_layouts - all_mapped_layouts

        if unmapped:
            print(f"⚠️  Missing: {len(unmapped)} template layouts without examples:")
            for layout in unmapped:
                print(f"   • {layout}")

        print(f"📊 Final result: {len(ordered_examples)} examples (one per layout) in template order")
        return ordered_examples

    def generate_master_json(self, ordered_examples: List[Dict[str, Any]]) -> str:
        """
        Generate master JSON file content.

        Args:
            ordered_examples: List of example data in template order

        Returns:
            JSON string for master file
        """
        # Combine all slides from all examples
        all_slides = []
        metadata = {"generated_by": "scripts/generate_master_examples.py", "total_examples": len(ordered_examples), "layout_order": []}

        for example in ordered_examples:
            slides = example["json_data"].get("slides", [])
            all_slides.extend(slides)
            metadata["layout_order"].append({"layout": example["layout"], "source_files": [example["json_filename"], example["md_filename"]]})

        master_data = {"metadata": metadata, "slides": all_slides}

        return json.dumps(master_data, indent=2, ensure_ascii=False)

    def generate_master_markdown(self, ordered_examples: List[Dict[str, Any]]) -> str:
        """
        Generate master Markdown file content.

        Args:
            ordered_examples: List of example data in template order

        Returns:
            Markdown string for master file
        """
        lines = [
            "# Master Examples - All Structured Frontmatter Patterns",
            "",
            "Generated by: `scripts/generate_master_examples.py`",
            f"Total Examples: {len(ordered_examples)}",
            "Template Order: Based on PowerPoint template layout sequence",
            "",
            "---",
            "",
        ]

        for i, example in enumerate(ordered_examples, 1):
            lines.extend(
                [f"## Example {i}: {example['layout']}", "", f"**Source Files:** `{example['json_filename']}`, `{example['md_filename']}`", "", example["markdown_content"].strip(), "", "---", ""]
            )

        return "\n".join(lines)

    def write_master_files(self, ordered_examples: List[Dict[str, Any]]) -> Tuple[Path, Path]:
        """
        Write master JSON and Markdown files to both output and assets directories.

        Args:
            ordered_examples: List of example data in template order

        Returns:
            Tuple of (json_path, md_path) for generated files
        """
        # Generate content
        json_content = self.generate_master_json(ordered_examples)
        md_content = self.generate_master_markdown(ordered_examples)

        # Write to output directory (for reference)
        json_path = self.output_dir / "master_examples.json"
        md_path = self.output_dir / "master_examples.md"

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Write to assets directory (for packaging)
        assets_json_path = self.assets_dir / "master_default_presentation.json"
        assets_md_path = self.assets_dir / "master_default_presentation.md"

        with open(assets_json_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        with open(assets_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"📄 Generated: {json_path.relative_to(self.project_root)}")
        print(f"📄 Generated: {md_path.relative_to(self.project_root)}")
        print(f"📦 Updated: {assets_json_path.relative_to(self.project_root)}")
        print(f"📦 Updated: {assets_md_path.relative_to(self.project_root)}")

        return json_path, md_path

    def generate_master_files(self, template_name: str = "default") -> Tuple[Path, Path]:
        """
        Main method to generate master files.

        Args:
            template_name: Name of PowerPoint template to use for ordering

        Returns:
            Tuple of (json_path, md_path) for generated master files
        """
        print("🚀 Starting Master Examples Generation")
        print("=" * 50)

        # Step 1: Get template layout order
        layout_order = self.get_template_layout_order(template_name)

        # Step 2: Discover example files
        examples = self.discover_example_files()

        # Step 3: Map examples to layouts and order them
        ordered_examples = self.map_examples_to_layouts(examples, layout_order)

        # Step 4: Generate master files
        json_path, md_path = self.write_master_files(ordered_examples)

        print("=" * 50)
        print("✅ Master Examples Generation Complete!")
        return json_path, md_path


def main():
    """Main entry point for the script."""
    try:
        generator = MasterExamplesGenerator()
        json_path, md_path = generator.generate_master_files()

        print("\n🎯 Master files ready for packaging:")
        print(f"   📦 JSON: {json_path}")
        print(f"   📦 Markdown: {md_path}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
