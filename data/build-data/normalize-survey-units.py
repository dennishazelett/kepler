#!/usr/bin/env python3
"""Create a canonical-unit copy of a valid Kepler survey archive.

The utility converts supported noncanonical physical quantities to their
canonical units. Observation-table source units are declared in
``survey.json.working_representation`` and resolved against the corresponding
observation JSON Schemas. Structured survey metadata quantities, currently
``observing_location.elevation``, carry their units directly.

The utility removes ``working_representation`` from the normalized output,
rewrites supported survey metadata quantities in canonical units, regenerates
``checksums.sha256``, and validates both source and output archives using the
sibling ``validate-survey.py`` utility.

Usage:
    python normalize-survey-units.py SOURCE_DIR OUTPUT_DIR \
        --schemas-dir PATH/TO/data/schemas [--overwrite]

The source archive is never modified.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any

NORMALIZER_VERSION = "0.3.0"
CHECKSUM_FILENAME = "checksums.sha256"
VALIDATION_LOG_FILENAME = "validation.log"

# Factors relative to a dimension-specific base unit.
UNIT_DEFINITIONS: dict[str, tuple[str, Decimal]] = {
    "mm": ("length", Decimal("0.001")),
    "cm": ("length", Decimal("0.01")),
    "m": ("length", Decimal("1")),
    "km": ("length", Decimal("1000")),
    "in": ("length", Decimal("0.0254")),
    "ft": ("length", Decimal("0.3048")),
    "yd": ("length", Decimal("0.9144")),
    "rad": ("angle", Decimal("1")),
    "deg": ("angle", Decimal("0.017453292519943295769236907684886")),
    "arcmin": ("angle", Decimal("0.00029088820866572159615394846141477")),
    "arcsec": ("angle", Decimal("0.0000048481368110953599358991410235795")),
}

UNIT_ALIASES: dict[str, str] = {
    "millimeter": "mm", "millimeters": "mm",
    "millimetre": "mm", "millimetres": "mm",
    "centimeter": "cm", "centimeters": "cm",
    "centimetre": "cm", "centimetres": "cm",
    "meter": "m", "meters": "m", "metre": "m", "metres": "m",
    "kilometer": "km", "kilometers": "km",
    "kilometre": "km", "kilometres": "km",
    "inch": "in", "inches": "in",
    "foot": "ft", "feet": "ft",
    "yard": "yd", "yards": "yd",
    "degree": "deg", "degrees": "deg",
    "radian": "rad", "radians": "rad",
    "arcminute": "arcmin", "arcminutes": "arcmin",
    "arcsecond": "arcsec", "arcseconds": "arcsec",
}


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


def normalize_unit_name(unit: str) -> str:
    normalized = UNIT_ALIASES.get(unit.strip().lower(), unit.strip().lower())
    if normalized not in UNIT_DEFINITIONS:
        raise ValueError(f"Unsupported unit {unit!r}")
    return normalized


def safe_archive_path(root: Path, relative: str, label: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or not posix.parts or ".." in posix.parts:
        raise ValueError(f"{label}: unsafe archive-relative path {relative!r}")
    resolved = root.joinpath(*posix.parts).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label}: path resolves outside archive: {relative!r}") from exc
    return resolved


def schema_for_column(schema: dict[str, Any], dotted_column: str) -> dict[str, Any]:
    node = schema
    for part in dotted_column.split("."):
        properties = node.get("properties")
        if not isinstance(properties, dict):
            return {}
        child = properties.get(part)
        if not isinstance(child, dict):
            return {}
        node = child
    return node


def decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text

def decimal_json_number(value: Decimal) -> int | float:
    """Return a JSON-serializable number without unnecessary decimal places."""
    normalized = value.normalize()
    if normalized == normalized.to_integral_value():
        return int(normalized)
    return float(normalized)

def convert_value(raw: str, source_unit: str, target_unit: str) -> str:
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(f"nonnumeric value {raw!r}") from exc
    source_dimension, source_factor = UNIT_DEFINITIONS[source_unit]
    target_dimension, target_factor = UNIT_DEFINITIONS[target_unit]
    if source_dimension != target_dimension:
        raise ValueError(
            f"dimensionally incompatible units {source_unit!r} and {target_unit!r}"
        )
    return decimal_text(value * source_factor / target_factor)

def convert_elevation(survey: dict[str, Any]) -> str | None:
    """Convert observing-location elevation to canonical metres.

    Returns a human-readable report entry when conversion occurs.
    Returns ``None`` when elevation is absent, null, or already canonical.
    """
    observing_location = survey.get("observing_location")
    if not isinstance(observing_location, dict):
        return None

    elevation = observing_location.get("elevation")
    if elevation is None:
        return None

    if not isinstance(elevation, dict):
        raise ValueError(
            "survey.json: observing_location.elevation must be an object or null"
        )

    value = elevation.get("value")
    raw_unit = elevation.get("unit")

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(
            "survey.json: observing_location.elevation.value must be numeric"
        )
    if not isinstance(raw_unit, str) or not raw_unit:
        raise ValueError(
            "survey.json: observing_location.elevation.unit must be a string"
        )

    source_unit = normalize_unit_name(raw_unit)
    source_dimension = UNIT_DEFINITIONS[source_unit][0]

    if source_dimension != "length":
        raise ValueError(
            "survey.json: observing_location.elevation.unit "
            f"{raw_unit!r} is not a length unit"
        )

    canonical_unit = "m"
    if source_unit == canonical_unit:
        return None

    converted_text = convert_value(
        str(value),
        source_unit,
        canonical_unit,
    )

    converted_decimal = Decimal(converted_text)
    elevation["value"] = decimal_json_number(converted_decimal)
    elevation["unit"] = canonical_unit

    return (
        "survey.json: observing_location.elevation: "
        f"{source_unit} -> {canonical_unit}"
    )

def observation_tables(survey: dict[str, Any]) -> list[dict[str, Any]]:
    raw_tables = survey.get("observation_tables")
    if not isinstance(raw_tables, list) or not raw_tables:
        raise ValueError("survey.json must contain a nonempty observation_tables array")
    tables: list[dict[str, Any]] = []
    for index, entry in enumerate(raw_tables):
        if not isinstance(entry, dict):
            raise ValueError(f"observation_tables[{index}] must be an object")
        path = entry.get("path")
        specification = entry.get("observation_specification")
        if not isinstance(path, str) or not isinstance(specification, dict):
            raise ValueError(f"observation_tables[{index}] is incomplete")
        name = specification.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(
                f"observation_tables[{index}].observation_specification.name is missing"
            )
        tables.append(entry)
    return tables


def working_representation(survey: dict[str, Any]) -> dict[str, dict[str, str]]:
    raw = survey.get("working_representation")
    if raw in (None, {}):
        return {}
    if not isinstance(raw, dict):
        raise ValueError("working_representation must be an object")
    parsed: dict[str, dict[str, str]] = {}
    for specification_name, fields in raw.items():
        if not isinstance(specification_name, str) or not specification_name:
            raise ValueError("working_representation specification names must be strings")
        if not isinstance(fields, dict) or not fields:
            raise ValueError(
                f"working_representation.{specification_name} must be a nonempty object"
            )
        parsed[specification_name] = {}
        for field_name, unit in fields.items():
            if not isinstance(field_name, str) or not isinstance(unit, str):
                raise ValueError(
                    f"working_representation.{specification_name} field names and units "
                    "must be strings"
                )
            parsed[specification_name][field_name] = normalize_unit_name(unit)
    return parsed


def convert_table(
    table_path: Path,
    schema: dict[str, Any],
    field_units: dict[str, str],
) -> list[str]:
    try:
        with table_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"Missing header row in {table_path}")
            headers = list(reader.fieldnames)
            rows = list(reader)
    except FileNotFoundError as exc:
        raise ValueError(f"Missing observation table: {table_path}") from exc

    changes: list[str] = []
    for field_name, source_unit in field_units.items():
        if field_name not in headers:
            raise ValueError(f"{table_path}: declared field {field_name!r} is absent")
        field_schema = schema_for_column(schema, field_name)
        canonical_raw = field_schema.get("x-kepler-unit")
        if not isinstance(canonical_raw, str):
            raise ValueError(
                f"{table_path}: schema has no x-kepler-unit for {field_name!r}"
            )
        canonical_unit = normalize_unit_name(canonical_raw)
        schema_dimension = field_schema.get("x-kepler-dimension")
        source_dimension = UNIT_DEFINITIONS[source_unit][0]
        canonical_dimension = UNIT_DEFINITIONS[canonical_unit][0]
        if source_dimension != canonical_dimension:
            raise ValueError(
                f"{table_path}: {field_name!r} uses {source_unit}, which is not "
                f"convertible to canonical {canonical_unit}"
            )
        if isinstance(schema_dimension, str) and schema_dimension != canonical_dimension:
            raise ValueError(
                f"{table_path}: schema dimension for {field_name!r} conflicts with "
                f"canonical unit {canonical_unit}"
            )

        for row_number, row in enumerate(rows, start=2):
            raw = row.get(field_name)
            if raw is None:
                raise ValueError(
                    f"{table_path} row {row_number}: missing field {field_name!r}"
                )
            stripped = raw.strip()
            if stripped == "":
                continue
            try:
                converted = convert_value(stripped, source_unit, canonical_unit)
            except ValueError as exc:
                raise ValueError(
                    f"{table_path} row {row_number}, field {field_name!r}: {exc}"
                ) from exc
            if source_unit != canonical_unit and Decimal(stripped) != 0 and Decimal(converted) == Decimal(stripped):
                raise ValueError(
                    f"{table_path} row {row_number}, field {field_name!r}: "
                    "conversion produced an unchanged nonzero value"
                )
            row[field_name] = converted
        changes.append(f"{field_name}: {source_unit} -> {canonical_unit} ({len(rows)} row(s))")

    with table_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # Re-open the persisted CSV and verify every converted cell exactly.
    with table_path.open("r", encoding="utf-8-sig", newline="") as handle:
        persisted = list(csv.DictReader(handle))
    if len(persisted) != len(rows):
        raise ValueError(f"{table_path}: row count changed during conversion")
    for row_number, (expected_row, actual_row) in enumerate(zip(rows, persisted), start=2):
        for field_name in field_units:
            expected = (expected_row.get(field_name) or "").strip()
            actual = (actual_row.get(field_name) or "").strip()
            if expected != actual:
                raise ValueError(
                    f"{table_path} row {row_number}, field {field_name!r}: "
                    f"persisted value {actual!r} does not equal converted value {expected!r}"
                )
    return changes


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums(root: Path) -> None:
    excluded = {CHECKSUM_FILENAME, VALIDATION_LOG_FILENAME}
    files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.name not in excluded
    )
    lines = [
        f"{sha256_file(path)}  {path.relative_to(root).as_posix()}"
        for path in files
    ]
    (root / CHECKSUM_FILENAME).write_text(
        "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8"
    )


def run_validator(validator: Path, survey_dir: Path, schemas_dir: Path) -> None:
    command = [
        sys.executable,
        str(validator),
        str(survey_dir),
        "--schemas-dir",
        str(schemas_dir),
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        raise ValueError(f"Validation failed for {survey_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a valid preliminary Kepler survey to canonical units."
    )
    parser.add_argument("--version", action="version", version=f"normalize-survey-units-v2.py {NORMALIZER_VERSION}")
    parser.add_argument("source_dir", type=Path, help="Valid preliminary survey archive")
    parser.add_argument("output_dir", type=Path, help="Canonical archive destination")
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        required=True,
        help="Directory containing survey and observation JSON Schemas",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace OUTPUT_DIR if it already exists",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()
    schemas_dir = args.schemas_dir.resolve()
    validator = Path(__file__).resolve().with_name("validate-survey.py")

    try:
        if not source_dir.is_dir():
            raise ValueError(f"Source survey directory does not exist: {source_dir}")
        if not schemas_dir.is_dir():
            raise ValueError(f"Schemas directory does not exist: {schemas_dir}")
        if not validator.is_file():
            raise ValueError(
                f"Required sibling validator was not found: {validator}"
            )
        if source_dir == output_dir:
            raise ValueError("Source and output directories must be different")
        if output_dir.exists():
            if not args.overwrite:
                raise ValueError(
                    f"Output directory already exists: {output_dir}. Use --overwrite."
                )
            if output_dir.is_dir():
                shutil.rmtree(output_dir)
            else:
                output_dir.unlink()

        print(f"Normalizer version: {NORMALIZER_VERSION}")
        print("Validating source archive...")
        run_validator(validator, source_dir, schemas_dir)

        source_survey = load_json(source_dir / "survey.json")
        tables = observation_tables(source_survey)
        working = working_representation(source_survey)

        manifest_by_spec: dict[str, list[dict[str, Any]]] = {}
        for table in tables:
            specification = table["observation_specification"]
            name = specification["name"]
            manifest_by_spec.setdefault(name, []).append(table)

        undeclared = sorted(set(working) - set(manifest_by_spec))
        if undeclared:
            raise ValueError(
                "working_representation references specifications absent from the "
                f"manifest: {', '.join(undeclared)}"
            )

        shutil.copytree(source_dir, output_dir)
        stale_log = output_dir / VALIDATION_LOG_FILENAME
        if stale_log.exists():
            stale_log.unlink()

        output_survey_path = output_dir / "survey.json"
        output_survey = load_json(output_survey_path)
        conversion_report: list[str] = []

        elevation_change = convert_elevation(output_survey)
        if elevation_change is not None:
            conversion_report.append(elevation_change)

        for specification_name, field_units in working.items():            
            schema_path = schemas_dir / f"{specification_name}.schema.json"
            schema = load_json(schema_path)
            for table in manifest_by_spec[specification_name]:
                relative_path = table["path"]
                table_path = safe_archive_path(
                    output_dir,
                    relative_path,
                    f"observation table for {specification_name}",
                )
                changes = convert_table(table_path, schema, field_units)
                conversion_report.extend(
                    f"{relative_path}: {change}" for change in changes
                )

        output_survey.pop("working_representation", None)
        output_survey_path.write_text(
            json.dumps(output_survey, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        write_checksums(output_dir)

        print("Validating canonical output archive...")
        run_validator(validator, output_dir, schemas_dir)

        verified = load_json(output_survey_path)

        if "working_representation" in verified:
            raise ValueError("Output still contains working_representation")

        verified_location = verified.get("observing_location")
        if isinstance(verified_location, dict):
            verified_elevation = verified_location.get("elevation")
            if isinstance(verified_elevation, dict):
                verified_unit = verified_elevation.get("unit")
                if verified_unit != "m":
                    raise ValueError(
                        "Output elevation is not represented in canonical metres"
                    )

        if not conversion_report:
            raise ValueError(
                "No noncanonical values required conversion"
            )
            
        print(f"PASS: canonical archive written to {output_dir}")
        for item in conversion_report:
            print(f"- {item}")
        print("- working_representation removed from output survey.json")
        print("- checksums.sha256 regenerated")
        return 0

    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
