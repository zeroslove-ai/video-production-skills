from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from previs_pipeline.package import create_zip_archive, validate_package
from previs_pipeline.synthetic import build_demo_r1_package


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Previs → AI video handoff (R1)")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Build synthetic R1 demo package (~12s)")
    demo.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("previs/out/demo_r1"),
        help="Output directory for package folder",
    )
    demo.add_argument("--zip", type=Path, default=None, help="Optional zip archive path")

    val = sub.add_parser("validate", help="Validate an existing package directory")
    val.add_argument("package_dir", type=Path)

    args = parser.parse_args(argv)

    if args.command == "demo":
        result = build_demo_r1_package(args.output)
        report = validate_package(result["package_dir"])
        print(json.dumps({"package_dir": str(result["package_dir"]), "validation": report}, indent=2))
        if args.zip:
            create_zip_archive(result["package_dir"], args.zip)
            print(f"Wrote archive: {args.zip}")
        return 0 if report["valid"] else 1

    if args.command == "validate":
        report = validate_package(args.package_dir)
        print(json.dumps(report, indent=2, default=str))
        return 0 if report["valid"] else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
