#!/usr/bin/env python3
"""Write the deterministic digest for a declared Kepler survey package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from survey_package_model import SurveyPackageError, digest_for_cli


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute the deterministic digest of a declared Kepler survey package."
    )
    parser.add_argument(
        "survey_dir",
        type=Path,
        help="Path to the survey package directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        result = digest_for_cli(args.survey_dir)
    except SurveyPackageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
