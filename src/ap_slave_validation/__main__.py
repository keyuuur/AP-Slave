from __future__ import annotations

import argparse
from pathlib import Path

from .validator import validate_repository


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AP Slave repository contracts offline")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    args = parser.parse_args()
    root = args.root.resolve()
    issues = validate_repository(root)
    if issues:
        for issue in issues:
            print(issue.render(root))
        print(f"Validation failed with {len(issues)} issue(s).")
        return 1
    print("Validation passed: repository contracts are internally consistent and network-free.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
