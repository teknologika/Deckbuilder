#!/usr/bin/env python3
"""
Test Runner for Deck Builder MCP

Provides a convenient command-line interface for running different test suites
and generating reports. Can be used from VS Code or command line.
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "tests"))


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> int:
    """Run a command and return the exit code."""
    if cwd is None:
        cwd = PROJECT_ROOT

    print(f"Running: {' '.join(cmd)}")
    print(f"Working directory: {cwd}")
    print("-" * 50)

    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


def run_pytest_command(args: List[str]) -> int:
    """Run pytest with given arguments."""
    python_executable = sys.executable
    cmd = [python_executable, "-m", "pytest"] + args
    return run_command(cmd)


def run_all_tests(verbose: bool = True, coverage: bool = False) -> int:
    """Run all tests."""
    args = ["tests/"]

    if verbose:
        args.extend(["--verbose", "--tb=short"])

    if coverage:
        args.extend(["--cov=src", "--cov-report=html:htmlcov", "--cov-report=term-missing"])

    return run_pytest_command(args)


def run_deckbuilder_tests(verbose: bool = True) -> int:
    """Run deckbuilder-specific tests."""
    args = ["tests/deckbuilder/", "-m", "deckbuilder"]

    if verbose:
        args.extend(["--verbose", "--tb=short"])

    return run_pytest_command(args)


def run_mcp_server_tests(verbose: bool = True) -> int:
    """Run MCP server-specific tests."""
    args = ["tests/mcp_server/", "-m", "mcp_server"]

    if verbose:
        args.extend(["--verbose", "--tb=short"])

    return run_pytest_command(args)


def run_unit_tests(verbose: bool = True) -> int:
    """Run unit tests only."""
    args = ["tests/", "-m", "unit"]

    if verbose:
        args.extend(["--verbose", "--tb=short"])

    return run_pytest_command(args)


def run_integration_tests(verbose: bool = True) -> int:
    """Run integration tests only."""
    args = ["tests/", "-m", "integration"]

    if verbose:
        args.extend(["--verbose", "--tb=short"])

    return run_pytest_command(args)


def run_specific_test(test_path: str, verbose: bool = True) -> int:
    """Run a specific test file or test function."""
    args = [test_path]

    if verbose:
        args.extend(["--verbose", "--tb=long", "-s"])

    return run_pytest_command(args)


def generate_coverage_report() -> int:
    """Generate HTML coverage report."""
    args = [
        "tests/",
        "--cov=src",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
    ]

    exit_code = run_pytest_command(args)

    if exit_code == 0:
        coverage_file = PROJECT_ROOT / "htmlcov" / "index.html"
        if coverage_file.exists():
            print(f"\nCoverage report generated: {coverage_file}")
            print("Open in browser to view detailed coverage analysis.")

    return exit_code


def generate_test_report() -> int:
    """Generate HTML test report."""
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    args = ["tests/", "--html=reports/test_report.html", "--self-contained-html", "--verbose"]

    exit_code = run_pytest_command(args)

    if exit_code == 0:
        report_file = PROJECT_ROOT / "reports" / "test_report.html"
        if report_file.exists():
            print(f"\nTest report generated: {report_file}")
            print("Open in browser to view detailed test results.")

    return exit_code


def run_parallel_tests(num_workers: int = 4) -> int:
    """Run tests in parallel using pytest-xdist."""
    args = ["tests/", "-n", str(num_workers), "--verbose"]

    return run_pytest_command(args)


def validate_environment() -> bool:
    """Validate that the test environment is properly set up."""
    print("Validating test environment...")

    # Check Python executable
    python_executable = sys.executable
    print(f"Python executable: {python_executable}")

    # Check if pytest is available
    try:
        import pytest

        print(f"pytest version: {pytest.__version__}")
    except ImportError:
        print("ERROR: pytest not installed")
        return False

    # Check if required packages are available
    required_packages = ["pptx", "yaml"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} available")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} missing")

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False

    # Check test directory structure
    test_dirs = ["tests/deckbuilder", "tests/mcp_server", "tests/utils", "tests/shared"]

    for test_dir in test_dirs:
        test_path = PROJECT_ROOT / test_dir
        if test_path.exists():
            print(f"✓ {test_dir} exists")
        else:
            print(f"✗ {test_dir} missing")

    print("Environment validation complete.")
    return len(missing_packages) == 0


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description="Test Runner for Deck Builder MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py --all                    # Run all tests
  python test_runner.py --deckbuilder           # Run deckbuilder tests
  python test_runner.py --unit                  # Run unit tests only
  python test_runner.py --coverage              # Run with coverage
  python test_runner.py --specific "tests/deckbuilder/unit/test_engine.py"
  python test_runner.py --validate              # Validate environment
        """,
    )

    # Test suite options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--deckbuilder", action="store_true", help="Run deckbuilder tests")
    parser.add_argument("--mcp-server", action="store_true", help="Run MCP server tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")

    # Specific test options
    parser.add_argument("--specific", type=str, help="Run specific test file or function")

    # Report options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--report", action="store_true", help="Generate HTML test report")
    parser.add_argument(
        "--parallel", type=int, metavar="N", help="Run tests in parallel with N workers"
    )

    # Utility options
    parser.add_argument("--validate", action="store_true", help="Validate test environment")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    args = parser.parse_args()

    # Set verbosity
    verbose = not args.quiet

    # Validate environment if requested
    if args.validate:
        is_valid = validate_environment()
        return 0 if is_valid else 1

    # Determine which tests to run
    exit_code = 0

    if args.specific:
        exit_code = run_specific_test(args.specific, verbose)
    elif args.all:
        exit_code = run_all_tests(verbose, args.coverage)
    elif args.deckbuilder:
        exit_code = run_deckbuilder_tests(verbose)
    elif args.mcp_server:
        exit_code = run_mcp_server_tests(verbose)
    elif args.unit:
        exit_code = run_unit_tests(verbose)
    elif args.integration:
        exit_code = run_integration_tests(verbose)
    elif args.coverage:
        exit_code = generate_coverage_report()
    elif args.report:
        exit_code = generate_test_report()
    elif args.parallel:
        exit_code = run_parallel_tests(args.parallel)
    else:
        # Default: run all tests
        print("No specific test suite specified, running all tests...")
        exit_code = run_all_tests(verbose)

    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
