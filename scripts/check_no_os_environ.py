#!/usr/bin/env python3
"""
Pre-commit hook to prevent os.environ usage.

Ensures that code uses proper parameter passing and path_manager
instead of modifying environment variables directly.
"""

import ast
import sys
from pathlib import Path


def check_file_for_os_environ(file_path: Path) -> list[str]:
    """Check a Python file for os.environ usage."""
    violations = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the Python AST
        tree = ast.parse(content)

        for node in ast.walk(tree):
            # Check for os.environ attribute access
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == "os" and node.attr == "environ":
                    violations.append(f"{file_path}:{node.lineno}: Found os.environ usage")

            # Check for direct environ import and usage
            elif isinstance(node, ast.Name) and node.id == "environ":
                # Check if it's being used (not just imported)
                if isinstance(node.ctx, (ast.Load, ast.Store)):
                    violations.append(f"{file_path}:{node.lineno}: Found direct environ usage")

    except Exception as e:
        # Skip files that can't be parsed (not Python, syntax errors, etc.)
        # Could log error if debugging: print(f"Warning: Could not parse {file_path}: {e}")
        _ = e  # Acknowledge exception variable

    return violations


def main():
    """Main function to check for os.environ usage."""
    violations = []

    # Check only src/ directory - tests can use os.environ for mocking
    src_dir = Path("src")

    if src_dir.exists():
        for py_file in src_dir.rglob("*.py"):
            file_violations = check_file_for_os_environ(py_file)
            violations.extend(file_violations)

    if violations:
        print("❌ PROHIBITED os.environ USAGE DETECTED!")
        print()
        print("The following files use os.environ which is not allowed:")
        print()

        for violation in violations:
            print(f"  🚫 {violation}")

        print()
        print("💡 SOLUTION:")
        print("  - Use path_manager for path resolution")
        print("  - Pass parameters explicitly instead of environment variables")
        print("  - Use dependency injection for configuration")
        print("  - Only read environment variables with os.getenv() if absolutely necessary")
        print()
        print("🔧 ALLOWED PATTERNS:")
        print("  ✅ os.getenv('VAR_NAME')  # Reading only")
        print("  ✅ path_manager.get_template_folder()  # Proper abstraction")
        print("  ✅ Passing parameters to functions/classes")
        print()
        print("🚫 FORBIDDEN PATTERNS:")
        print("  ❌ os.environ['VAR'] = value  # Setting environment variables")
        print("  ❌ os.environ.get('VAR')     # Use os.getenv() instead")
        print("  ❌ from os import environ   # Direct environ usage")
        print()

        return 1
    else:
        print("✅ No prohibited os.environ usage detected")
        return 0


if __name__ == "__main__":
    sys.exit(main())
