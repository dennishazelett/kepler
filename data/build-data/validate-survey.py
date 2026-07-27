#!/usr/bin/env python3
"""Validate a Kepler multi-table survey package.

Usage:
    python validate-survey.py PATH/TO/SURVEY \
        --schemas-dir PATH/TO/data/schemas

Requires:
    pip install jsonschema

The validator reads ``survey.json.observation_tables`` as the authoritative
manifest. Each table is validated against ``<name>.schema.json`` in the
schemas directory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install it with: pip install jsonschema"
    ) from exc


SURVEY_SCHEMA_FILENAME = "survey.schema.json"
VALIDATION_LOG_FILENAME = "validation.log"
CHECKSUM_FILENAME = "checksums.sha256"
VALIDATOR_VERSION = "0.3.1"


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError as exc:
        raise ValueError(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    schema = load_json(path)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"Invalid JSON Schema in {path}: {exc.message}") from exc
    return schema


def format_jsonschema_error(prefix: str, error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{prefix}: {location}: {error.message}"


def safe_archive_path(survey_dir: Path, relative_path: str, label: str) -> Path:
    """Resolve a POSIX-style relative archive path without allowing traversal."""
    posix_path = PurePosixPath(relative_path)
    if posix_path.is_absolute() or ".." in posix_path.parts:
        raise ValueError(f"{label}: path must remain inside the survey archive: {relative_path!r}")
    if not posix_path.parts:
        raise ValueError(f"{label}: path must not be empty")

    resolved = survey_dir.joinpath(*posix_path.parts).resolve()
    try:
        resolved.relative_to(survey_dir.resolve())
    except ValueError as exc:
        raise ValueError(
            f"{label}: path resolves outside the survey archive: {relative_path!r}"
        ) from exc
    return resolved


def schema_types(schema: dict[str, Any]) -> list[str]:
    value = schema.get("type")
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def property_schema_for_column(schema: dict[str, Any], column: str) -> dict[str, Any]:
    node = schema
    for part in column.split("."):
        properties = node.get("properties")
        if not isinstance(properties, dict):
            return {}
        child = properties.get(part)
        if not isinstance(child, dict):
            return {}
        node = child
    return node


def coerce_value(value: str, schema: dict[str, Any]) -> Any:
    """Coerce a CSV cell according to its local JSON Schema property."""
    if value == "":
        allowed = schema_types(schema)
        if "null" in allowed:
            return None
        return ""

    allowed = schema_types(schema)
    if "integer" in allowed:
        try:
            return int(value)
        except ValueError:
            return value
    if "number" in allowed:
        try:
            return float(value)
        except ValueError:
            return value
    if "boolean" in allowed:
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    if "null" in allowed and value.lower() == "null":
        return None
    return value


def unflatten_dotted_keys(row: dict[str, Any]) -> dict[str, Any]:
    """Convert dotted CSV headers into nested dictionaries."""
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


def read_observations(
    path: Path, schema: dict[str, Any]
) -> tuple[list[str], list[tuple[int, dict[str, Any]]]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"Missing header row in {path}")

            headers = [header.strip() for header in reader.fieldnames]
            if any(not header for header in headers):
                raise ValueError(f"Blank column name in {path}")
            if len(headers) != len(set(headers)):
                raise ValueError(f"Duplicate column names in {path}")

            rows: list[tuple[int, dict[str, Any]]] = []
            for line_number, raw_row in enumerate(reader, start=2):
                if None in raw_row:
                    raise ValueError(
                        f"Row {line_number} in {path} has more values than headers"
                    )
                typed_flat: dict[str, Any] = {}
                all_blank = True
                for raw_column, raw_value in raw_row.items():
                    assert raw_column is not None
                    column = raw_column.strip()
                    value = "" if raw_value is None else raw_value.strip()
                    if value:
                        all_blank = False
                    typed_flat[column] = coerce_value(
                        value, property_schema_for_column(schema, column)
                    )
                if all_blank:
                    raise ValueError(f"Blank observation row at line {line_number} in {path}")
                rows.append((line_number, unflatten_dotted_keys(typed_flat)))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing observation table: {path}") from exc

    return headers, rows


def expected_schema_version_matches(
    schema: dict[str, Any], declared_version: str
) -> bool | None:
    """Return whether a schema's explicit schema_version rule accepts a version."""
    property_schema = schema.get("properties", {}).get("schema_version")
    if not isinstance(property_schema, dict):
        return None
    validator = Draft202012Validator(property_schema)
    return not any(validator.iter_errors(declared_version))


def validate_notes(
    survey_dir: Path, referenced_notes: set[str], errors: list[str]
) -> None:
    notes_path = survey_dir / "notes.csv"
    if not notes_path.exists():
        if referenced_notes:
            errors.append("Observation tables reference notes, but notes.csv is missing")
        return

    try:
        with notes_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                errors.append("notes.csv: missing header row")
                return
            note_key = "notes_id" if "notes_id" in reader.fieldnames else (
                "note_id" if "note_id" in reader.fieldnames else None
            )
            if note_key is None:
                errors.append("notes.csv: required column 'note_id' or 'notes_id' is missing")
                return
            defined_notes: set[str] = set()
            for line_number, row in enumerate(reader, start=2):
                note_id = (row.get(note_key) or "").strip()
                if not note_id:
                    continue
                if note_id in defined_notes:
                    errors.append(f"notes.csv row {line_number}: duplicate notes_id {note_id!r}")
                defined_notes.add(note_id)
    except OSError as exc:
        errors.append(f"Could not read notes.csv: {exc}")
        return

    for note_id in sorted(referenced_notes - defined_notes):
        errors.append(f"Observation tables: notes_id {note_id!r} is not defined in notes.csv")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_checksums(path: Path) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return {}, [f"Missing required file: {path}"]
    except OSError as exc:
        return {}, [f"Could not read {path}: {exc}"]

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            errors.append(f"{path.name} line {line_number}: invalid checksum entry")
            continue
        digest, raw_name = parts
        relative_name = raw_name.lstrip(" *")
        if any(char not in "0123456789abcdefABCDEF" for char in digest):
            errors.append(f"{path.name} line {line_number}: invalid SHA-256 digest")
            continue
        if relative_name in entries:
            errors.append(f"{path.name} line {line_number}: duplicate path {relative_name!r}")
            continue
        entries[relative_name] = digest.lower()
    return entries, errors


def iter_archive_files(survey_dir: Path) -> Iterable[Path]:
    excluded = {CHECKSUM_FILENAME, VALIDATION_LOG_FILENAME}
    for path in survey_dir.rglob("*"):
        if path.is_file() and path.name not in excluded:
            yield path


def validate_checksums(survey_dir: Path, errors: list[str]) -> None:
    checksum_path = survey_dir / CHECKSUM_FILENAME
    entries, parse_errors = parse_checksums(checksum_path)
    errors.extend(parse_errors)
    if parse_errors and not entries:
        return

    expected_paths = {
        path.relative_to(survey_dir).as_posix(): path for path in iter_archive_files(survey_dir)
    }

    for relative_path, expected_digest in entries.items():
        if relative_path == VALIDATION_LOG_FILENAME:
            continue
        try:
            file_path = safe_archive_path(
                survey_dir, relative_path, f"{CHECKSUM_FILENAME}"
            )
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not file_path.is_file():
            errors.append(f"{CHECKSUM_FILENAME}: listed file does not exist: {relative_path}")
            continue
        actual_digest = sha256_file(file_path)
        if actual_digest != expected_digest:
            errors.append(
                f"{CHECKSUM_FILENAME}: checksum mismatch for {relative_path}"
            )

    listed_paths = set(entries)
    for relative_path in sorted(set(expected_paths) - listed_paths):
        errors.append(f"{CHECKSUM_FILENAME}: archive file is not listed: {relative_path}")
    for relative_path in sorted(listed_paths - set(expected_paths)):
        if relative_path not in {VALIDATION_LOG_FILENAME, CHECKSUM_FILENAME}:
            errors.append(f"{CHECKSUM_FILENAME}: lists unexpected file: {relative_path}")


def validate_package(
    survey_dir: Path, schemas_dir: Path, check_checksums: bool = True
) -> list[str]:
    errors: list[str] = []

    if not survey_dir.is_dir():
        return [f"Survey directory does not exist: {survey_dir}"]
    if not schemas_dir.is_dir():
        return [f"Schemas directory does not exist: {schemas_dir}"]

    try:
        survey = load_json(survey_dir / "survey.json")
        survey_schema = load_schema(schemas_dir / SURVEY_SCHEMA_FILENAME)
    except ValueError as exc:
        return [str(exc)]

    survey_validator = Draft202012Validator(
        survey_schema, format_checker=FormatChecker()
    )
    for error in sorted(survey_validator.iter_errors(survey), key=str):
        errors.append(format_jsonschema_error("survey.json", error))

    survey_id = survey.get("survey_id")
    declared_observers = {
        item for item in survey.get("observer_ids", []) if isinstance(item, str)
    }
    tables = survey.get("observation_tables")
    if not isinstance(tables, list):
        tables = []

    seen_table_paths: set[str] = set()
    global_observation_ids: dict[str, str] = {}
    referenced_notes: set[str] = set()

    for table_index, table in enumerate(tables, start=1):
        table_prefix = f"survey.json observation_tables[{table_index - 1}]"
        if not isinstance(table, dict):
            continue

        relative_path = table.get("path")
        specification = table.get("observation_specification")
        instrument_instance_id = table.get("instrument_instance_id")
        if not isinstance(relative_path, str) or not isinstance(specification, dict):
            continue

        if relative_path in seen_table_paths:
            errors.append(f"{table_prefix}: duplicate observation table path {relative_path!r}")
        seen_table_paths.add(relative_path)

        schema_name = specification.get("name")
        declared_version = specification.get("version")
        if not isinstance(schema_name, str) or not isinstance(declared_version, str):
            continue

        try:
            observation_path = safe_archive_path(survey_dir, relative_path, table_prefix)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not observation_path.is_file():
            errors.append(f"{table_prefix}: observation table does not exist: {relative_path}")
            continue

        schema_path = schemas_dir / f"{schema_name}.schema.json"
        try:
            observation_schema = load_schema(schema_path)
        except ValueError as exc:
            errors.append(f"{table_prefix}: {exc}")
            continue

        version_match = expected_schema_version_matches(
            observation_schema, declared_version
        )
        if version_match is False:
            errors.append(
                f"{table_prefix}: declared specification version {declared_version!r} "
                f"is not accepted by {schema_path.name}"
            )

        try:
            _, observations = read_observations(observation_path, observation_schema)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        validator = Draft202012Validator(
            observation_schema, format_checker=FormatChecker()
        )
        for line_number, observation in observations:
            row_prefix = f"{relative_path} row {line_number}"
            for error in sorted(validator.iter_errors(observation), key=str):
                errors.append(format_jsonschema_error(row_prefix, error))

            observation_id = observation.get("observation_id")
            if isinstance(observation_id, str) and observation_id:
                prior = global_observation_ids.get(observation_id)
                if prior is not None:
                    errors.append(
                        f"{row_prefix}: duplicate observation_id {observation_id!r}; "
                        f"first seen at {prior}"
                    )
                else:
                    global_observation_ids[observation_id] = row_prefix

            row_survey_id = observation.get("survey_id")
            if row_survey_id is not None and survey_id is not None and row_survey_id != survey_id:
                errors.append(
                    f"{row_prefix}: survey_id {row_survey_id!r} does not match "
                    f"survey.json ({survey_id!r})"
                )

            row_instrument = observation.get("instrument_instance_id")
            if (
                row_instrument is not None
                and isinstance(instrument_instance_id, str)
                and row_instrument != instrument_instance_id
            ):
                errors.append(
                    f"{row_prefix}: instrument_instance_id {row_instrument!r} does not "
                    f"match observation_tables manifest ({instrument_instance_id!r})"
                )

            observer_id = observation.get("observer_id")
            if (
                isinstance(observer_id, str)
                and declared_observers
                and observer_id not in declared_observers
            ):
                errors.append(
                    f"{row_prefix}: observer_id {observer_id!r} is not declared in survey.json"
                )

            notes_id = observation.get("notes_id")
            if isinstance(notes_id, str) and notes_id:
                referenced_notes.add(notes_id)

    validate_notes(survey_dir, referenced_notes, errors)

    for index, attachment in enumerate(survey.get("attachments", []), start=1):
        if not isinstance(attachment, dict):
            continue
        relative_path = attachment.get("path")
        if not isinstance(relative_path, str):
            continue
        prefix = f"survey.json attachments[{index - 1}]"
        try:
            attachment_path = safe_archive_path(survey_dir, relative_path, prefix)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not attachment_path.is_file():
            errors.append(f"{prefix}: attachment path does not exist: {relative_path}")
            continue
        expected_digest = attachment.get("sha256")
        if isinstance(expected_digest, str) and expected_digest:
            actual_digest = sha256_file(attachment_path)
            if actual_digest.lower() != expected_digest.lower():
                errors.append(f"{prefix}: SHA-256 mismatch for {relative_path}")

    if check_checksums:
        validate_checksums(survey_dir, errors)

    return errors




def evaluate_submission_readiness(
    survey: dict[str, Any], schemas_dir: Path
) -> tuple[bool, list[str], list[str]]:
    """Evaluate whether a structurally valid survey uses canonical units.

    Returns (submission_ready, reasons, errors). Declared working units are
    allowed in preliminary archives, but they must refer to real physical
    fields and recognized canonical units in the corresponding schemas.
    """
    working = survey.get("working_representation")
    if working in (None, {}):
        return True, [], []
    if not isinstance(working, dict):
        return False, [], ["survey.json: working_representation must be an object"]

    tables = survey.get("observation_tables")
    if not isinstance(tables, list):
        return False, [], ["survey.json: observation_tables must be an array"]

    by_name: dict[str, dict[str, Any]] = {}
    for table in tables:
        if not isinstance(table, dict):
            continue
        spec = table.get("observation_specification")
        if isinstance(spec, dict) and isinstance(spec.get("name"), str):
            by_name[spec["name"]] = table

    reasons: list[str] = []
    errors: list[str] = []
    for schema_name, fields in working.items():
        if not isinstance(schema_name, str) or not isinstance(fields, dict):
            errors.append("survey.json: each working_representation entry must map a specification name to an object")
            continue
        if schema_name not in by_name:
            errors.append(f"survey.json: working_representation references unknown observation specification {schema_name!r}")
            continue
        schema_path = schemas_dir / f"{schema_name}.schema.json"
        try:
            schema = load_schema(schema_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for field_name, source_unit in fields.items():
            if not isinstance(field_name, str) or not isinstance(source_unit, str) or not source_unit:
                errors.append(f"survey.json: invalid working unit declaration for {schema_name!r}")
                continue
            field_schema = property_schema_for_column(schema, field_name)
            if not field_schema:
                errors.append(f"survey.json: working_representation field {schema_name}.{field_name} is not defined by the observation schema")
                continue
            canonical_unit = field_schema.get("x-kepler-unit")
            dimension = field_schema.get("x-kepler-dimension")
            if not isinstance(canonical_unit, str):
                errors.append(f"survey.json: working_representation field {schema_name}.{field_name} has no canonical unit in the observation schema")
                continue
            if not isinstance(dimension, str):
                errors.append(f"survey.json: working_representation field {schema_name}.{field_name} is not declared as a physical quantity")
                continue
            if source_unit != canonical_unit:
                reasons.append(f"{schema_name}.{field_name} uses {source_unit} instead of canonical {canonical_unit}")

    return not reasons and not errors, reasons, errors

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Kepler multi-table survey package against JSON Schemas."
    )
    parser.add_argument("--version", action="version", version=f"validate-survey.py {VALIDATOR_VERSION}")
    parser.add_argument("survey_dir", type=Path, help="Survey package directory")
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        required=True,
        help="Directory containing survey.schema.json and observation schemas",
    )
    parser.add_argument(
        "--skip-checksums",
        action="store_true",
        help="Skip checksums.sha256 verification",
    )
    return parser.parse_args()


def write_validation_log(
    survey_dir: Path,
    errors: list[str],
    submission_ready: bool,
    readiness_reasons: list[str],
) -> Path:
    status = "PASS" if not errors else "FAIL"
    timestamp = datetime.now(timezone.utc).isoformat()
    archive_status = (
        "VALID CANONICAL ARCHIVE" if submission_ready and not errors
        else "VALID PRELIMINARY ARCHIVE" if not errors
        else "INVALID ARCHIVE"
    )
    lines = [
        "Kepler Survey Validation Report",
        "===============================",
        f"Validator version: {VALIDATOR_VERSION}",
        f"Survey directory: {survey_dir}",
        f"Validated at: {timestamp}",
        f"Status: {status}",
        f"Archive status: {archive_status}",
        f"Submission ready: {'YES' if submission_ready and not errors else 'NO'}",
        "",
    ]
    if errors:
        lines.extend(["Errors", "------"])
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("No validation errors were found.")
        if readiness_reasons:
            lines.extend(["", "Canonicalization required", "-------------------------"])
            lines.extend(f"- {reason}" for reason in readiness_reasons)
    lines.extend(["", f"Error count: {len(errors)}"])

    log_path = survey_dir / VALIDATION_LOG_FILENAME
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path

def main() -> int:
    args = parse_args()
    survey_dir = args.survey_dir.resolve()
    schemas_dir = args.schemas_dir.resolve()

    errors = validate_package(
        survey_dir, schemas_dir, check_checksums=not args.skip_checksums
    )

    submission_ready = False
    readiness_reasons: list[str] = []
    if not errors:
        try:
            survey = load_json(survey_dir / "survey.json")
            submission_ready, readiness_reasons, readiness_errors = (
                evaluate_submission_readiness(survey, schemas_dir)
            )
            errors.extend(readiness_errors)
        except ValueError as exc:
            errors.append(str(exc))

    log_path: Path | None = None
    if survey_dir.is_dir():
        try:
            log_path = write_validation_log(
                survey_dir, errors, submission_ready, readiness_reasons
            )
        except OSError as exc:
            errors.append(f"Could not write validation log: {exc}")

    print(f"Validator version: {VALIDATOR_VERSION}")
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        print("STATUS: INVALID ARCHIVE")
        print("SUBMISSION READY: NO")
        for error in errors:
            print(f"- {error}")
        if log_path is not None:
            print(f"Log written to: {log_path}")
        return 1

    print("PASS: survey package conforms to the current schemas")
    if submission_ready:
        print("STATUS: VALID CANONICAL ARCHIVE")
        print("SUBMISSION READY: YES")
    else:
        print("STATUS: VALID PRELIMINARY ARCHIVE")
        print("SUBMISSION READY: NO")
        if readiness_reasons:
            print("Canonicalization required for:")
            for reason in readiness_reasons:
                print(f"- {reason}")
    if log_path is not None:
        print(f"Log written to: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
