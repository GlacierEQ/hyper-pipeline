#!/usr/bin/env python3
"""
Hyper-Pipeline — Unified Test Runner
Runs all test suites across architect, forge, and production.
"""

import subprocess
import sys
from pathlib import Path


def run_tests(test_dir: Path, name: str) -> bool:
    """Run a test suite and return success."""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short", "-q"],
        cwd=str(test_dir.parent),
    )
    return result.returncode == 0


def main() -> int:
    base = Path(__file__).parent
    tests_dir = base / "tests"

    results = {}

    # Run all test suites
    for test_file in tests_dir.glob("test_*.py"):
        name = test_file.stem.replace("test_", "").replace("_", " ").title()
        results[name] = run_tests(test_file, name)

    # Summary
    print(f"\n{'='*60}")
    print("  HYPER-PIPELINE TEST SUMMARY")
    print(f"{'='*60}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for name, success in results.items():
        icon = "✓" if success else "✗"
        print(f"  {icon} {name}")

    print(f"\n  Total: {passed}/{total} suites passed")
    print(f"{'='*60}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
