#!/usr/bin/env python3
"""
Development script to copy master presentation files FROM assets TO tests

This ensures test files stay synchronized with the master presentation files
that are bundled with the package. Assets are the source of truth.
"""

import shutil
from pathlib import Path


def sync_master_to_tests():
    """Copy master presentation files from assets to test directory"""

    # Define source and destination paths (reversed logic)
    project_root = Path(__file__).parent.parent
    source_dir = project_root / "src" / "deckbuilder" / "assets"
    dest_dir = project_root / "tests" / "deckbuilder"

    # Ensure destination directory exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Files to copy (master files are source of truth)
    files_to_copy = [
        ("master_default_presentation.md", "test_comprehensive_layouts.md"),
        ("master_default_presentation.json", "test_comprehensive_layouts.json"),
    ]

    copied_files = []

    for source_name, dest_name in files_to_copy:
        source_file = source_dir / source_name
        dest_file = dest_dir / dest_name

        if source_file.exists():
            shutil.copy2(source_file, dest_file)
            copied_files.append(dest_name)
            print(f"✓ Synced {source_name} -> {dest_name}")
        else:
            print(f"✗ Master file not found: {source_file}")

    if copied_files:
        print(f"\n✅ Successfully synced {len(copied_files)} master files to tests")
        print("📁 Test files updated:")
        for file in copied_files:
            print(f"   - {file}")
    else:
        print("❌ No master files were synced")
        return False

    return True


if __name__ == "__main__":
    success = sync_master_to_tests()
    exit(0 if success else 1)
