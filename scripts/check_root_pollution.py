#!/usr/bin/env python3
"""
Pre-commit hook to check for root directory pollution.

Ensures that only approved directories and files exist in the project root,
preventing test outputs and temporary files from being committed.
"""

import sys
from pathlib import Path


def get_allowed_items():
    """Get the list of allowed files and directories in project root."""
    return {
        # Core project files
        ".git/",
        ".gitignore",
        ".pre-commit-config.yaml",
        "LICENSE",
        "README.md",
        "CLAUDE.md",
        "PLANNING.md",
        "TASK.md",
        "DISCOVERY.md",
        "FOLDER_STRUCTURE.md",
        "GEMINI.md",
        "MANIFEST.in",
        "pyproject.toml",
        "requirements.txt",
        "pytest.ini",
        "bandit.yaml",
        "uv.lock",
        "run_server.sh",
        "Deckbuilder.code-workspace",
        "mkdocs.yml",
        # Development/CI files
        ".github/",
        ".coverage",
        ".python-version",
        ".venv/",
        ".claude/",
        ".mypy_cache/",
        ".DS_Store",
        # Test and development artifacts
        "htmlcov/",  # Coverage reports
        ".deckbuilder_assets/",  # Asset cache directory
        # Core directories
        "src/",
        "tests/",
        "docs/",
        "assets/",
        "output/",  # Official output directory
        "temp/",  # Official temp directory
        "build/",  # Build artifacts
        "dist/",  # Distribution artifacts
        "scripts/",  # Utility scripts
        ".specs/",  # Spec server specifications
        "templates/",  # Template symlink
        # Python build artifacts
        "src/deckbuilder.egg-info/",
        ".pytest_cache/",
        "__pycache__/",
        # IDE/Editor files
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "*~",
    }


def check_for_pollution():
    """Check for unauthorized files/directories in project root."""
    project_root = Path(__file__).parent.parent
    allowed_items = get_allowed_items()

    # Common pollution patterns to specifically flag (for future use)
    # pollution_patterns = {
    #     "templates/": "Templates should be in assets/templates/, not project root",
    #     "tmp/": "Use proper test directories or tempfile",
    #     "*.pptx": "PowerPoint files should be in tests/output/ or temp directories",
    #     "*.json": "JSON files should be in appropriate subdirectories",
    # }

    pollution_found = []

    for item in project_root.iterdir():
        item_name = item.name
        item_path = f"{item_name}/" if item.is_dir() else item_name

        # Check if item is allowed
        if item_path not in allowed_items and item_name not in allowed_items:
            # Check for glob patterns (like *.swp)
            is_allowed = False
            for allowed in allowed_items:
                if "*" in allowed:
                    import fnmatch

                    if fnmatch.fnmatch(item_name, allowed):
                        is_allowed = True
                        break

            if not is_allowed:
                pollution_found.append(item_path)

    return pollution_found


def main():
    """Main function to run pollution check."""
    pollution = check_for_pollution()

    if pollution:
        print("❌ ROOT DIRECTORY POLLUTION DETECTED!")
        print("The following unauthorized files/directories were found in project root:")
        print()

        for item in sorted(pollution):
            print(f"  🚫 {item}")

        print()
        print("💡 SOLUTION:")
        print("  - Remove test output files and temporary directories")
        print("  - Use /tests/output/ for test outputs")
        print("  - Use /temp/ for temporary files")
        print("  - Never create files/directories directly in project root")
        print()
        print("🧹 CLEANUP COMMAND:")
        print("  rm -rf " + " ".join(pollution))
        print()

        return 1
    else:
        print("✅ Root directory is clean - no pollution detected")
        return 0


if __name__ == "__main__":
    sys.exit(main())
