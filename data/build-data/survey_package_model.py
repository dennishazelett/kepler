from __future__ import annotations

import hashlib
import importlib.util
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

MODULE_DIR = Path(__file__).resolve().parent
DATA_DIR = MODULE_DIR.parent
SCHEMAS_DIR = DATA_DIR / "schemas"
VALIDATE_SURVEY_PATH = MODULE_DIR / "validate-survey.py"
PROFILE_ID = "kepler-survey-package-registration-v1"
PROFILE_VERSION = "1.0.0"
DIGEST_ALGORITHM = "sha256"
GENERATED_ARTIFACT_PATHS = frozenset({"registry.json", "validation-report.json"})


class SurveyPackageError(Exception):
    """Base error for expected registration-model failures."""


class PackageLayoutError(SurveyPackageError):
    """Raised when a package root or declared path is unusable."""


class PackageParseError(SurveyPackageError):
    """Raised when a package artifact cannot be parsed."""


class RegistrationGenerationError(SurveyPackageError):
    """Raised when registry generation is requested for an ineligible survey."""


class OperationalError(SurveyPackageError):
    """Raised when required repository validation infrastructure is unavailable."""


@dataclass(frozen=True)
class PackageDigest:
    algorithm: str
    value: str


@dataclass(frozen=True)
class ObservationTable:
    relative_path: str
    observation_specification_name: str
    observation_specification_version: str
    instrument_instance_id: str


@dataclass(frozen=True)
class DeclaredSurveyPackage:
    root: Path
    survey: Mapping[str, Any]
    survey_id: str
    observation_tables: tuple[ObservationTable, ...]
    declared_relative_paths: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    relative_path: str | None = None
    row_number: int | None = None
    field: str | None = None
    json_pointer: str | None = None
    context: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ValidationResult:
    survey_id: str
    package_digest: PackageDigest
    findings: tuple[Finding, ...]
    archive_status: str
    submission_ready: bool

    @property
    def error_count(self) -> int:
        return sum(finding.severity == "error" for finding in self.findings)

    @property
    def warning_count(self) -> int:
        return sum(finding.severity == "warning" for finding in self.findings)

    @property
    def status(self) -> str:
        return "invalid" if self.error_count else "valid"


@dataclass(frozen=True)
class _TableRows:
    table: ObservationTable
    rows: tuple[tuple[int, Mapping[str, Any]], ...]


def _load_validate_survey() -> Any:
    if not VALIDATE_SURVEY_PATH.is_file():
        raise OperationalError(
            f"Missing required validator: {VALIDATE_SURVEY_PATH}"
        )
    spec = importlib.util.spec_from_file_location(
        "kepler_validate_survey", VALIDATE_SURVEY_PATH
    )
    if spec is None or spec.loader is None:
        raise OperationalError(
            f"Could not load required validator: {VALIDATE_SURVEY_PATH}"
        )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise OperationalError(
            f"Could not initialize required validator: {VALIDATE_SURVEY_PATH}"
        ) from exc
    required = (
        "VALIDATOR_VERSION",
        "evaluate_submission_readiness",
        "load_json",
        "load_schema",
        "read_observations",
        "safe_archive_path",
        "validate_package",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise OperationalError(
            "Required validator does not expose expected API: "
            + ", ".join(missing)
        )
    return module


validate_survey = _load_validate_survey()


def _validated_root(package_root: Path) -> Path:
    root = Path(package_root).resolve()
    if not root.is_dir():
        raise PackageLayoutError(f"Survey directory does not exist: {root}")
    return root


def _normalized_relative_path(value: str, label: str) -> str:

    if not isinstance(value, str) or not value:
        raise PackageLayoutError(f"{label}: path must not be empty")

    path = PurePosixPath(value)

    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise PackageLayoutError(
            f"{label}: path must remain inside the survey archive: {value!r}"
        )

    normalized = path.as_posix()

    if normalized == ".":
        raise PackageLayoutError(f"{label}: path must name a file: {value!r}")

    return normalized


def _declared_file(root: Path, relative_path: str, label: str) -> Path:
    normalized = _normalized_relative_path(relative_path, label)
    candidate = root.joinpath(*PurePosixPath(normalized).parts)

    if candidate.is_symlink():
        raise PackageLayoutError(f"{label}: symbolic links are not allowed: {normalized}")
    try:
        resolved = validate_survey.safe_archive_path(root, normalized, label)
    except ValueError as exc:
        raise PackageLayoutError(str(exc)) from exc

    if not resolved.exists():
        raise PackageLayoutError(f"{label}: file does not exist: {normalized}")

    if not resolved.is_file():
        raise PackageLayoutError(f"{label}: not a regular file: {normalized}")

    return resolved


def _required_string(mapping: Mapping[str, Any], key: str, label: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise PackageParseError(f"{label}: required string {key!r} is missing")
    return value


def _load_json_object(path: Path, relative_path: str) -> dict[str, Any]:
    try:
        value = validate_survey.load_json(path)
    except ValueError as exc:
        raise PackageParseError(str(exc)) from exc
    if not isinstance(value, dict):
        raise PackageParseError(f"Expected JSON object in {relative_path}")
    return value


def _parse_observation_tables(survey: Mapping[str, Any]) -> tuple[ObservationTable, ...]:
    entries = survey.get("observation_tables")
    if not isinstance(entries, list):
        raise PackageParseError("survey.json: observation_tables must be an array")
    tables: list[ObservationTable] = []
    for index, entry in enumerate(entries):
        label = f"survey.json observation_tables[{index}]"
        if not isinstance(entry, Mapping):
            raise PackageParseError(f"{label}: entry must be an object")
        relative_path = _required_string(entry, "path", label)
        specification = entry.get("observation_specification")
        if not isinstance(specification, Mapping):
            raise PackageParseError(f"{label}: observation_specification must be an object")
        tables.append(
            ObservationTable(
                relative_path=_normalized_relative_path(relative_path, label),
                observation_specification_name=_required_string(
                    specification, "name", label
                ),
                observation_specification_version=_required_string(
                    specification, "version", label
                ),
                instrument_instance_id=_required_string(
                    entry, "instrument_instance_id", label
                ),
            )
        )
    return tuple(tables)


def _declared_relative_paths(
    root: Path, survey: Mapping[str, Any], tables: Sequence[ObservationTable]
) -> tuple[str, ...]:
    paths = {"survey.json"}
    for table in tables:
        _declared_file(root, table.relative_path, "survey.json observation table")
        paths.add(table.relative_path)
    attachments = survey.get("attachments", [])
    if attachments is None:
        attachments = []
    if not isinstance(attachments, list):
        raise PackageParseError("survey.json: attachments must be an array")
    for index, attachment in enumerate(attachments):
        label = f"survey.json attachments[{index}]"
        if not isinstance(attachment, Mapping):
            raise PackageParseError(f"{label}: entry must be an object")
        relative_path = _required_string(attachment, "path", label)
        normalized = _normalized_relative_path(relative_path, label)
        _declared_file(root, normalized, label)
        paths.add(normalized)
    return tuple(sorted(paths))


def load_declared_package(package_root: Path) -> DeclaredSurveyPackage:
    root = _validated_root(package_root)
    survey_path = _declared_file(root, "survey.json", "survey metadata")
    survey = _load_json_object(survey_path, "survey.json")
    survey_id = _required_string(survey, "survey_id", "survey.json")
    tables = _parse_observation_tables(survey)
    return DeclaredSurveyPackage(
        root=root,
        survey=survey,
        survey_id=survey_id,
        observation_tables=tables,
        declared_relative_paths=_declared_relative_paths(root, survey, tables),
    )


def compute_package_digest(package_root: Path) -> PackageDigest:
    package = load_declared_package(package_root)
    digest = hashlib.sha256()
    for relative_path in package.declared_relative_paths:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        path = _declared_file(package.root, relative_path, "declared package artifact")
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return PackageDigest(algorithm=DIGEST_ALGORITHM, value=digest.hexdigest())


def _path_get(value: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = value
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _profile_specification(profile: Mapping[str, Any], name: str) -> Mapping[str, Any] | None:
    specifications = profile.get("observation_specifications")
    if not isinstance(specifications, Mapping):
        return None
    specification = specifications.get(name)
    return specification if isinstance(specification, Mapping) else None


def _trimmed_target(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _extract_targets(
    row: Mapping[str, Any], field_sets: Sequence[Any]
) -> tuple[str, ...] | None:
    for field_set in field_sets:
        if not isinstance(field_set, list) or not field_set:
            continue
        values = tuple(_trimmed_target(_path_get(row, field)) for field in field_set)
        if all(values):
            return tuple(value for value in values if value is not None)
    return None


def _parse_offset_aware_utc(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or len(text) == 10:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _format_utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _load_table_rows(package: DeclaredSurveyPackage) -> tuple[_TableRows, ...]:
    loaded: list[_TableRows] = []
    for table in package.observation_tables:
        schema_path = SCHEMAS_DIR / f"{table.observation_specification_name}.schema.json"
        try:
            schema = validate_survey.load_schema(schema_path)
            _, rows = validate_survey.read_observations(
                _declared_file(package.root, table.relative_path, "observation table"),
                schema,
            )
        except ValueError as exc:
            raise PackageParseError(str(exc)) from exc
        loaded.append(_TableRows(table, tuple(rows)))
    return tuple(loaded)


def _finding_key(finding: Finding) -> tuple[Any, ...]:
    context = None
    if finding.context:
        context = json.dumps(
            finding.context, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        )
    return (
        finding.severity,
        finding.code,
        finding.message,
        finding.relative_path,
        finding.row_number,
        finding.field,
        finding.json_pointer,
        context,
    )


def _finalize_findings(findings: Iterable[Finding]) -> tuple[Finding, ...]:
    unique = {_finding_key(finding): finding for finding in findings}
    return tuple(unique[key] for key in sorted(unique))


def _validator_findings(errors: Iterable[str]) -> list[Finding]:
    return [
        Finding(severity="error", code="SURVEY_VALIDATION_ERROR", message=str(error))
        for error in errors
    ]


def _registration_findings(
    package: DeclaredSurveyPackage,
    profile: Mapping[str, Any],
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        rows_by_table = _load_table_rows(package)
    except SurveyPackageError as exc:
        return [Finding("error", "OBSERVATION_TABLE_READ_ERROR", str(exc))]
    for table_rows in rows_by_table:
        rule = _profile_specification(
            profile, table_rows.table.observation_specification_name
        )
        if rule is None:
            findings.append(
                Finding(
                    "error",
                    "UNSUPPORTED_OBSERVATION_SPECIFICATION",
                    "Observation specification is not supported by the registration profile.",
                    relative_path=table_rows.table.relative_path,
                    context={"name": table_rows.table.observation_specification_name},
                )
            )
            continue
        field_sets = rule.get("target_field_sets")
        if not isinstance(field_sets, list):
            findings.append(
                Finding(
                    "error",
                    "INVALID_PROFILE_TARGET_RULE",
                    "Registration profile target-field rule is malformed.",
                    relative_path=table_rows.table.relative_path,
                )
            )
            continue
        for line_number, row in table_rows.rows:
            targets = _extract_targets(row, field_sets)
            if targets is None:
                findings.append(
                    Finding(
                        "error",
                        "MISSING_DECLARED_TARGET",
                        "Observation does not provide a nonblank target field set required by the registration profile.",
                        relative_path=table_rows.table.relative_path,
                        row_number=line_number,
                        context={"target_field_sets": field_sets},
                    )
                )
                continue
            if len(targets) == 2 and targets[0] == targets[1]:
                findings.append(
                    Finding(
                        "error",
                        "INVALID_TARGET_PAIR",
                        "A paired target observation must name two distinct targets after trim-only normalization.",
                        relative_path=table_rows.table.relative_path,
                        row_number=line_number,
                        context={"target_id": targets[0]},
                    )
                )
    return findings


def _warn_for_undeclared_files(package: DeclaredSurveyPackage) -> list[Finding]:
    declared = set(package.declared_relative_paths) | GENERATED_ARTIFACT_PATHS
    findings: list[Finding] = []
    for path in sorted(package.root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(package.root).as_posix()
        if relative in declared:
            continue
        if path.is_symlink():
            findings.append(
                Finding(
                    "warning",
                    "UNDECLARED_PACKAGE_SYMLINK",
                    "Symbolic link is not a declared package artifact.",
                    relative_path=relative,
                )
            )
        elif path.is_file():
            findings.append(
                Finding(
                    "warning",
                    "UNDECLARED_PACKAGE_FILE",
                    "File is not declared by survey.json and is excluded from package identity.",
                    relative_path=relative,
                )
            )
    return findings


def _archive_status(errors: Sequence[str], submission_ready: bool) -> str:
    if errors:
        return "invalid_archive"
    if submission_ready:
        return "valid_canonical_archive"
    return "valid_preliminary_archive"


def validate_declared_package(
    package_root: Path,
    *,
    profile: Mapping[str, Any],
    profile_sha256: str,
) -> ValidationResult:
    del profile_sha256
    root = _validated_root(package_root)
    expected_validation = profile.get("required_survey_validation")
    if not isinstance(expected_validation, Mapping):
        raise OperationalError(
            "Registration profile is missing required_survey_validation."
        )

    validator = expected_validation.get("validator")
    if not isinstance(validator, Mapping) or validator.get("name") != "validate-survey.py":
        raise OperationalError(
            "Registration profile does not identify validate-survey.py."
        )
    errors = validate_survey.validate_package(root, SCHEMAS_DIR, check_checksums=True)
    survey: Mapping[str, Any] = {}
    submission_ready = False
    readiness_errors: list[str] = []
    if not errors:
        try:
            survey = validate_survey.load_json(root / "survey.json")
            submission_ready, _, readiness_errors = validate_survey.evaluate_submission_readiness(
                survey, SCHEMAS_DIR
            )
        except ValueError as exc:
            readiness_errors.append(str(exc))
    all_validator_errors = [*errors, *readiness_errors]
    try:
        package = load_declared_package(root)
        digest = compute_package_digest(root)
        survey_id = package.survey_id
    except SurveyPackageError as exc:
        digest = PackageDigest(DIGEST_ALGORITHM, hashlib.sha256(b"").hexdigest())
        survey_id = str(survey.get("survey_id", "unknown"))
        all_validator_errors.append(str(exc))
        package = None
    findings = _validator_findings(all_validator_errors)
    if package is not None:
        findings.extend(_registration_findings(package, profile))
        findings.extend(_warn_for_undeclared_files(package))
    finalized = _finalize_findings(findings)
    return ValidationResult(
        survey_id=survey_id,
        package_digest=digest,
        findings=finalized,
        archive_status=_archive_status(all_validator_errors, submission_ready),
        submission_ready=submission_ready and not all_validator_errors,
    )


def _sampling_summary(
    package: DeclaredSurveyPackage, profile: Mapping[str, Any]
) -> dict[str, Any]:
    rows_by_table = _load_table_rows(package)
    target_counts: dict[str, int] = {}
    table_summaries: list[dict[str, Any]] = []
    timestamps: list[datetime] = []
    temporal_tables: set[str] = set()
    total_observations = 0
    total_references = 0
    for table_rows in rows_by_table:
        table = table_rows.table
        rule = _profile_specification(profile, table.observation_specification_name)
        if rule is None:
            raise RegistrationGenerationError(
                f"Unsupported observation specification: {table.observation_specification_name}"
            )
        field_sets = rule.get("target_field_sets")
        timestamp_field = rule.get("observed_at_field")
        if not isinstance(field_sets, list) or not isinstance(timestamp_field, str):
            raise RegistrationGenerationError("Registration profile contains malformed observation rules.")
        total_observations += len(table_rows.rows)
        for _, row in table_rows.rows:
            targets = _extract_targets(row, field_sets)
            if targets is None:
                raise RegistrationGenerationError("Cannot summarize an observation without a declared target.")
            for target in targets:
                target_counts[target] = target_counts.get(target, 0) + 1
                total_references += 1
            if rule.get("derived_utc_extent_allowed") == "only_offset_aware_date_time":
                parsed = _parse_offset_aware_utc(_path_get(row, timestamp_field))
                if parsed is not None:
                    timestamps.append(parsed)
                    temporal_tables.add(table.relative_path)
        table_summaries.append(
            {
                "relative_path": table.relative_path,
                "observation_specification": {
                    "name": table.observation_specification_name,
                    "version": table.observation_specification_version,
                },
                "instrument_instance_id": table.instrument_instance_id,
                "observation_count": len(table_rows.rows),
            }
        )
    summary: dict[str, Any] = {
        "observation_count": total_observations,
        "target_reference_count": total_references,
        "target_count": len(target_counts),
        "observation_tables": table_summaries,
        "targets": [
            {"target_id": target, "observation_reference_count": target_counts[target]}
            for target in sorted(target_counts)
        ],
    }
    started_at = package.survey.get("started_at")
    ended_at = package.survey.get("ended_at")
    if isinstance(started_at, str) and isinstance(ended_at, str):
        summary["temporal_extent"] = {
            "status": "available",
            "provenance": {
                "method": "contributor_declared_survey_interval",
                "source": "survey.json",
            },
            "started_at": started_at,
            "ended_at": ended_at,
        }
    elif timestamps and len(timestamps) == total_observations:
        summary["temporal_extent"] = {
            "status": "available",
            "provenance": {
                "method": "min_max_normalized_utc_observation_timestamp_v1",
                "included_observation_tables": sorted(temporal_tables),
            },
            "started_at": _format_utc(min(timestamps)),
            "ended_at": _format_utc(max(timestamps)),
        }
    return summary


def build_validation_report(
    result: ValidationResult,
    *,
    profile: Mapping[str, Any],
    profile_sha256: str,
) -> dict[str, Any]:
    findings = _finalize_findings(result.findings)
    report_findings: list[dict[str, Any]] = []
    for finding in findings:
        item: dict[str, Any] = {
            "severity": finding.severity,
            "code": finding.code,
            "message": finding.message,
        }
        location: dict[str, Any] = {}
        if finding.relative_path is not None:
            location["relative_path"] = finding.relative_path
        if finding.row_number is not None:
            location["row_number"] = finding.row_number
        if finding.field is not None:
            location["field"] = finding.field
        if finding.json_pointer is not None:
            location["json_pointer"] = finding.json_pointer
        if location:
            item["location"] = location
        if finding.context:
            item["context"] = dict(finding.context)
        report_findings.append(item)
    error_count = sum(finding.severity == "error" for finding in findings)
    warning_count = sum(finding.severity == "warning" for finding in findings)
    return {
        "report_format": "kepler.declared-survey-package-validation-report",
        "report_version": "1.0.0",
        "validator": {
            "name": "validate-survey.py",
            "version": validate_survey.VALIDATOR_VERSION,
        },
        "profile": {
            "id": profile.get("profile_id", PROFILE_ID),
            "version": profile.get("profile_version", PROFILE_VERSION),
            "content_sha256": profile_sha256,
        },
        "package": {
            "survey_id": result.survey_id,
            "content_sha256": result.package_digest.value,
        },
        "status": "invalid" if error_count else "valid",
        "summary": {
            "error_count": error_count,
            "warning_count": warning_count,
        },
        "findings": report_findings,
    }


def build_registry_record(
    package: DeclaredSurveyPackage,
    *,
    package_digest: PackageDigest,
    profile: Mapping[str, Any],
    generator_version: str,
) -> dict[str, Any]:
    summary = _sampling_summary(package, profile)
    return {
        "record_format": "kepler.survey-package-registration",
        "record_version": "1.0.0",
        "package": {
            "survey_id": package.survey_id,
            "content_sha256": package_digest.value,
        },
        "sampling_summary": {
            "summary_derivation": {
                "profile_id": profile.get("profile_id", PROFILE_ID),
                "profile_version": profile.get("profile_version", PROFILE_VERSION),
                "generator": {
                    "name": "generate-registry-record.py",
                    "version": generator_version,
                },
                "source_manifest": {
                    "relative_path": "survey.json",
                    "observation_table_manifest_field": "observation_tables",
                },
                "target_identity_normalization": profile.get(
                    "target_identity_normalization", "trim_only_v1"
                ),
            },
            **summary,
        },
        "validation_report": {
            "relative_path": "validation-report.json",
            "format": "kepler.validation-report+json",
            "schema_version": "1.0.0",
        },
    }


def digest_for_cli(package_root: Path) -> dict[str, str]:
    digest = compute_package_digest(package_root)
    return {"algorithm": digest.algorithm, "value": digest.value}


def validation_report_for_cli(
    package_root: Path,
    *,
    profile: Mapping[str, Any],
    profile_sha256: str,
) -> dict[str, Any]:
    result = validate_declared_package(
        package_root, profile=profile, profile_sha256=profile_sha256
    )
    return build_validation_report(
        result, profile=profile, profile_sha256=profile_sha256
    )


def registry_record_for_cli(
    package_root: Path,
    *,
    profile: Mapping[str, Any],
    profile_sha256: str,
    generator_version: str,
) -> dict[str, Any]:
    result = validate_declared_package(
        package_root, profile=profile, profile_sha256=profile_sha256
    )
    required = profile.get("required_survey_validation", {})
    if (
        result.error_count
        or result.archive_status != required.get("required_archive_status")
        or result.submission_ready != required.get("required_submission_ready")
    ):
        raise RegistrationGenerationError(
            "Cannot generate registry record: survey is not registration-ready."
        )
    package = load_declared_package(package_root)
    return build_registry_record(
        package,
        package_digest=result.package_digest,
        profile=profile,
        generator_version=generator_version,
    )
