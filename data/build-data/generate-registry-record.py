#!/usr/bin/env python3
"""Write a Kepler survey-package registry record for an eligible survey."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from survey_package_model import (
    OperationalError,
    RegistrationGenerationError,
    SurveyPackageError,
    registry_record_for_cli,
)

MODULE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = (
    MODULE_DIR.parent
    / "schemas"
    / "survey-package-registration-profile-v1.json"
)
GENERATOR_VERSION = "1.0.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a registry record for a Kepler survey package."
    )
    parser.add_argument(
        "survey_dir",
        type=Path,
        help="Path to the survey package directory.",
    )
    return parser.parse_args()


def load_profile(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OperationalError(f"Could not read registration profile: {path}") from exc

    try:
        profile = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OperationalError(f"Invalid registration profile JSON: {path}") from exc

    if not isinstance(profile, dict):
        raise OperationalError(f"Registration profile must be a JSON object: {path}")

    return profile, hashlib.sha256(raw).hexdigest()


def main() -> int:
    args = parse_args()

    try:
        profile, profile_sha256 = load_profile(PROFILE_PATH)
        record = registry_record_for_cli(
            args.survey_dir,
            profile=profile,
            profile_sha256=profile_sha256,
            generator_version=GENERATOR_VERSION,
        )
    except (OperationalError, RegistrationGenerationError, SurveyPackageError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json.dump(record, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
