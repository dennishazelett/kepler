#!/usr/bin/env python3
"""Validate a Kepler survey package.

Usage:
    python validate-survey.py PATH/TO/SURVEY \
        --schemas-dir PATH/TO/data/schemas

Requires:
    pip install jsonschema
"""

from __future__ import annotations
from datetime import datetime, timezone

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install it with: pip install jsonschema"
    ) from exc


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return schema


def format_jsonschema_error(prefix: str, error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path)
    if not location:
        location = "<root>"
    return f"{prefix}: {location}: {error.message}"


def unflatten_dotted_keys(row: dict[str, Any]) -> dict[str, Any]:
    """Convert {'calibration.target_id': 'A'} to nested dictionaries."""
    result: dict[str, Any] = {}
    for key, value in row.items():
        parts = key.split(".")
        cursor = result
        for part in parts[:-1]:
            existing = cursor.get(part)
            if existing is None:
                cursor[part] = {}
            elif not isinstance(existing, dict):
                raise ValueError(f"Column path collision at {key!r}")
            cursor = cursor[part]
        cursor[parts[-1]] = value
    return result


def coerce_value(value: str, schema: dict[str, Any]) -> Any:
    """Coerce CSV strings using the local JSON Schema property definition."""
    if value == "":
        types = schema.get("type")
        if isinstance(types, list) and "null" in types:
            return None
        return ""

    schema_type = schema.get("type")
    allowed = schema_type if isinstance(schema_type, list) else [schema_type]

    if "number" in allowed:
        try:
            return float(value)
        except ValueError:
            return value
    if "integer" in allowed:
        try:
            return int(value)
        except ValueError:
            return value
    if "boolean" in allowed:
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    return value


def property_schema_for_column(schema: dict[str, Any], column: str) -> dict[str, Any]:
    node = schema
    for part in column.split("."):
        properties = node.get("properties", {})
        node = properties.get(part, {})
        if not isinstance(node, dict):
            return {}
        node_type = node.get("type")
        if isinstance(node_type, list) and "object" in node_type:
            # Nullable object; properties remain on the same node.
            pass
    return node


def read_observations(
    path: Path, schema: dict[str, Any]
) -> tuple[list[str], list[dict[str, Any]]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"Missing header row in {path}")
            headers = list(reader.fieldnames)
            if len(headers) != len(set(headers)):
                raise ValueError(f"Duplicate column names in {path}")

            rows: list[dict[str, Any]] = []
            for line_number, raw_row in enumerate(reader, start=2):
                if None in raw_row:
                    raise ValueError(
                        f"Row {line_number} in {path} has more values than headers"
                    )
                typed_flat: dict[str, Any] = {}
                for column, raw_value in raw_row.items():
                    assert column is not None
                    value = "" if raw_value is None else raw_value.strip()
                    typed_flat[column] = coerce_value(
                        value, property_schema_for_column(schema, column)
                    )
                rows.append(unflatten_dotted_keys(typed_flat))
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {path}")

    return headers, rows


def validate_package(survey_dir: Path, schemas_dir: Path) -> list[str]:
    errors: list[str] = []

    survey_path = survey_dir / "survey.json"
    observations_path = survey_dir / "observations.csv"
    survey_schema_path = schemas_dir / "survey.schema.json"
    observation_schema_path = schemas_dir / "cross-staff-observation.schema.json"

    try:
        survey = load_json(survey_path)
        survey_schema = load_schema(survey_schema_path)
        observation_schema = load_schema(observation_schema_path)
    except (ValueError, Exception) as exc:
        # SchemaError and JSON errors are fatal to meaningful validation.
        return [str(exc)]

    survey_validator = Draft202012Validator(
        survey_schema, format_checker=FormatChecker()
    )
    for error in sorted(survey_validator.iter_errors(survey), key=str):
        errors.append(format_jsonschema_error("survey.json", error))

    try:
        _, observations = read_observations(observations_path, observation_schema)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    observation_validator = Draft202012Validator(
        observation_schema, format_checker=FormatChecker()
    )

    observation_ids: set[str] = set()
    survey_id = survey.get("survey_id")
    notes_ids: set[str] = set()

    for index, observation in enumerate(observations, start=1):
        prefix = f"observations.csv row {index + 1}"
        for error in sorted(observation_validator.iter_errors(observation), key=str):
            errors.append(format_jsonschema_error(prefix, error))

        observation_id = observation.get("observation_id")
        if isinstance(observation_id, str):
            if observation_id in observation_ids:
                errors.append(f"{prefix}: duplicate observation_id {observation_id!r}")
            observation_ids.add(observation_id)

        if survey_id is not None and observation.get("survey_id") != survey_id:
            errors.append(
                f"{prefix}: survey_id does not match survey.json ({survey_id!r})"
            )

        notes_id = observation.get("notes_id")
        if isinstance(notes_id, str) and notes_id:
            notes_ids.add(notes_id)

    # Validate notes references when notes.csv is present.
    notes_path = survey_dir / "notes.csv"
    if notes_path.exists():
        with notes_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None or "notes_id" not in reader.fieldnames:
                errors.append("notes.csv: required column 'notes_id' is missing")
            else:
                defined_notes = {
                    (row.get("notes_id") or "").strip()
                    for row in reader
                    if (row.get("notes_id") or "").strip()
                }
                missing_notes = sorted(notes_ids - defined_notes)
                for note_id in missing_notes:
                    errors.append(
                        f"observations.csv: notes_id {note_id!r} is not defined in notes.csv"
                    )
    elif notes_ids:
        errors.append("observations.csv references notes, but notes.csv is missing")

    # Validate attachment paths declared in survey.json.
    for attachment in survey.get("attachments", []):
        if not isinstance(attachment, dict):
            continue
        relative_path = attachment.get("path")
        if isinstance(relative_path, str):
            attachment_path = survey_dir / relative_path
            if not attachment_path.is_file():
                errors.append(
                    f"survey.json: attachment path does not exist: {relative_path}"
                )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Kepler survey package against JSON Schemas."
    )
    parser.add_argument("survey_dir", type=Path, help="Survey package directory")
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        required=True,
        help="Directory containing survey.schema.json and cross-staff-observation.schema.json",
    )
    return parser.parse_args()

def write_validation_log(
    survey_dir: Path,
    errors: list[str],
) -> None:
    status = "PASS" if not errors else "FAIL"
    timestamp = datetime.now(timezone.utc).isoformat()

    lines = [
        "Kepler Survey Validation Report",
        "===============================",
        f"Survey directory: {survey_dir}",
        f"Validated at: {timestamp}",
        f"Status: {status}",
        "",
    ]

    if errors:
        lines.append("Errors")
        lines.append("------")
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("No validation errors were found.")

    lines.append("")
    lines.append(f"Error count: {len(errors)}")

    log_path = survey_dir / "validation.log"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> int:
    args = parse_args()
    survey_dir = args.survey_dir.resolve()
    schemas_dir = args.schemas_dir.resolve()

    errors = validate_package(survey_dir, schemas_dir)
    write_validation_log(survey_dir, errors)

    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        for error in errors:
            print(f"- {error}")
        print(f"Log written to: {survey_dir / 'validation.log'}")
        return 1

    print("PASS: survey package conforms to the current schemas")
    print(f"Log written to: {survey_dir / 'validation.log'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
