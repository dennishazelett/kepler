#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
GIT_SHA_RE = re.compile(r"^[a-f0-9]{40}$")
SURVEY_ID_RE = re.compile(r"^SUR-[A-Z0-9][A-Z0-9-]*$")


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Required file is missing: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"Expected a JSON object in {path}")
    return value


def validate_provenance(repository_url: str, commit_sha: str, package_relative_path: str) -> None:
    parsed = urlparse(repository_url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail("--repository-url must be an absolute HTTPS URL")
    if not GIT_SHA_RE.fullmatch(commit_sha):
        fail("--commit-sha must be a lowercase 40-character Git SHA")
    path = Path(package_relative_path)
    if path.is_absolute() or ".." in path.parts or package_relative_path in {"", "."}:
        fail("--package-relative-path must be a non-empty relative path without '..'")
    if "\\" in package_relative_path:
        fail("--package-relative-path must use '/' separators")


def package_identity(registry: dict) -> tuple[str, str]:
    survey_id = registry.get("survey_id")
    content_sha256 = registry.get("content_sha256")
    if not isinstance(survey_id, str) or not SURVEY_ID_RE.fullmatch(survey_id):
        fail("registry.json must contain a valid survey_id")
    if not isinstance(content_sha256, str) or not SHA256_RE.fullmatch(content_sha256):
        fail("registry.json must contain a lowercase 64-character content_sha256")
    return survey_id, content_sha256


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def assert_validation_report_matches(report: dict, survey_id: str, content_sha256: str) -> None:
    report_text = json.dumps(report, sort_keys=True)
    if survey_id not in report_text or content_sha256 not in report_text:
        fail("validation-report.json does not contain the registry survey_id and content_sha256")
    status_values = [report.get(key) for key in ("status", "validation_status", "result", "valid")]
    if any(value in {"failed", "invalid", False} for value in status_values):
        fail("validation-report.json indicates unsuccessful validation")


def ensure_schema_exists(kepler_root: Path) -> None:
    schema = kepler_root / "data/schemas/kepler-registration.schema.json"
    if not schema.is_file():
        fail(f"Kepler registration schema is missing: {schema}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an immutable Kepler registration record from a validated survey package."
    )
    parser.add_argument("--package-root", required=True, type=Path)
    parser.add_argument("--kepler-root", required=True, type=Path)
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--package-relative-path", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    kepler_root = args.kepler_root.resolve()
    validate_provenance(args.repository_url, args.commit_sha, args.package_relative_path)
    ensure_schema_exists(kepler_root)

    registry_path = package_root / "registry.json"
    report_path = package_root / "validation-report.json"
    registry = load_json(registry_path)
    report = load_json(report_path)
    survey_id, content_sha256 = package_identity(registry)
    assert_validation_report_matches(report, survey_id, content_sha256)

    target_name = f"{survey_id}--{content_sha256[:16]}"
    target = kepler_root / "data/registry/records" / target_name
    if target.exists():
        fail(f"Registration target already exists: {target}")

    generated = {
        "registration_format": "kepler.survey-registration",
        "registration_version": "1.0.0",
        "registration_status": "registered",
        "package": {
            "survey_id": survey_id,
            "content_sha256": content_sha256,
        },
        "source_snapshot": {
            "repository_url": args.repository_url,
            "commit_sha": args.commit_sha,
            "package_relative_path": args.package_relative_path,
        },
        "artifacts": {
            "copied_registry_record": "registry.json",
            "copied_validation_report": "validation-report.json",
            "registry_json_sha256": sha256_file(registry_path),
            "validation_report_json_sha256": sha256_file(report_path),
        },
    }

    if args.dry_run:
        print(json.dumps({"target": str(target), "kepler_registration": generated}, indent=2))
        return 0

    target.mkdir(parents=True)
    try:
        shutil.copyfile(registry_path, target / "registry.json")
        shutil.copyfile(report_path, target / "validation-report.json")
        (target / "kepler-registration.json").write_text(
            json.dumps(generated, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise

    print(f"Created {target}")
    print("Review the three generated files, validate them, then commit them to Kepler.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
