from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUILD_DATA_DIR = REPOSITORY_ROOT / "data" / "build-data"
SCHEMAS_DIR = REPOSITORY_ROOT / "data" / "schemas"
PROFILE_PATH = SCHEMAS_DIR / "survey-package-registration-profile-v1.json"
MODEL_PATH = BUILD_DATA_DIR / "survey_package_model.py"


def load_model():
    sys.path.insert(0, str(BUILD_DATA_DIR))
    spec = importlib.util.spec_from_file_location("survey_package_model", MODEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load model module: {MODEL_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MODEL = load_model()
PROFILE_BYTES = PROFILE_PATH.read_bytes()
PROFILE = json.loads(PROFILE_BYTES.decode("utf-8"))
PROFILE_SHA256 = hashlib.sha256(PROFILE_BYTES).hexdigest()


class SurveyPackageRegistrationTests(unittest.TestCase):
    def make_package(self) -> tempfile.TemporaryDirectory[str]:
        temporary_directory = tempfile.TemporaryDirectory()
        root = Path(temporary_directory.name)

        survey = {
            "schema_version": "0.3",
            "survey_id": "survey_001",
            "survey_type": "demonstration",
            "scientific_question": "Does the registration layer derive package metadata?",
            "observer_ids": ["OBS-0001"],
            "observing_location": {
                "latitude_deg": 34.0,
                "longitude_deg": -118.0,
                "coordinate_reference_system": "WGS84",
            },
            "observation_tables": [
                {
                    "path": "observations/compass.csv",
                    "instrument_instance_id": "INS-0001",
                    "observation_specification": {
                        "name": "compass-observation",
                        "version": "1.0.0",
                    },
                }
            ],
            "attachments": [
                {
                    "attachment_id": "ATT-0001",
                    "path": "attachments/readme.txt",
                    "description": "Declared supporting attachment.",
                }
            ],
        }

        observations = (
            "observation_id,observer_id,instrument,target_name,angle_deg,observed_at\n"
            "obs_001,OBS-0001,compass, Polaris ,12.5,2026-01-02T03:04:05+00:00\n"
        )

        (root / "observations").mkdir()
        (root / "attachments").mkdir()
        (root / "survey.json").write_text(
            json.dumps(survey, indent=2) + "\n",
            encoding="utf-8",
        )
        (root / "observations" / "compass.csv").write_text(
            observations,
            encoding="utf-8",
        )
        (root / "attachments" / "readme.txt").write_text(
            "declared attachment\n",
            encoding="utf-8",
        )

        declared_paths = [
            "attachments/readme.txt",
            "observations/compass.csv",
            "survey.json",
        ]
        checksums = "\n".join(
            f"{hashlib.sha256((root / path).read_bytes()).hexdigest()}  {path}"
            for path in declared_paths
        )
        (root / "checksums.sha256").write_text(
            checksums + "\n",
            encoding="utf-8",
        )

        return temporary_directory

    def test_digest_is_deterministic_and_ignores_generated_artifacts(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)

            first = MODEL.compute_package_digest(root)

            (root / "registry.json").write_text(
                '{"generated":"registry"}\n',
                encoding="utf-8",
            )
            (root / "validation-report.json").write_text(
                '{"generated":"report"}\n',
                encoding="utf-8",
            )

            second = MODEL.compute_package_digest(root)

            self.assertEqual(first.algorithm, "sha256")
            self.assertEqual(first.value, second.value)

    def test_digest_ignores_undeclared_file_but_changes_for_declared_file(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)

            original = MODEL.compute_package_digest(root)

            (root / "incidental.txt").write_text(
                "not declared by survey.json\n",
                encoding="utf-8",
            )
            with_incidental_file = MODEL.compute_package_digest(root)

            attachment = root / "attachments" / "readme.txt"
            attachment.write_text("changed declared attachment\n", encoding="utf-8")
            changed_declared_file = MODEL.compute_package_digest(root)

            self.assertEqual(original.value, with_incidental_file.value)
            self.assertNotEqual(original.value, changed_declared_file.value)

    def test_declared_missing_file_is_an_error(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)
            (root / "attachments" / "readme.txt").unlink()

            with self.assertRaises(MODEL.PackageLayoutError):
                MODEL.compute_package_digest(root)

    def test_declared_symlink_is_an_error(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)
            attachment = root / "attachments" / "readme.txt"
            replacement = root / "attachments" / "replacement.txt"
            replacement.write_text("replacement\n", encoding="utf-8")
            attachment.unlink()

            try:
                attachment.symlink_to(replacement.name)
            except OSError as exc:
                self.skipTest(f"Symbolic links are unavailable: {exc}")

            with self.assertRaises(MODEL.PackageLayoutError):
                MODEL.compute_package_digest(root)

    def test_validation_warns_for_undeclared_file(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)
            (root / "incidental.txt").write_text(
                "not declared by survey.json\n",
                encoding="utf-8",
            )

            result = MODEL.validate_declared_package(
                root,
                profile=PROFILE,
                profile_sha256=PROFILE_SHA256,
            )

            findings = [
                finding
                for finding in result.findings
                if (
                    finding.code == "UNDECLARED_PACKAGE_FILE"
                    and finding.relative_path == "incidental.txt"
                )
            ]

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].severity, "warning")


    def test_validation_report_is_deterministic_and_has_package_identity(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)

            first = MODEL.validation_report_for_cli(
                root,
                profile=PROFILE,
                profile_sha256=PROFILE_SHA256,
            )
            second = MODEL.validation_report_for_cli(
                root,
                profile=PROFILE,
                profile_sha256=PROFILE_SHA256,
            )

            self.assertEqual(first, second)
            self.assertEqual(
                first["package"]["survey_id"],
                "survey_001",
            )
            self.assertRegex(
                first["package"]["content_sha256"],
                r"^[a-f0-9]{64}$",
            )
            self.assertEqual(
                first["validator"]["name"],
                "validate-survey.py",
            )
            self.assertEqual(
                first["validator"]["version"],
                MODEL.validate_survey.VALIDATOR_VERSION,
            )
            self.assertNotIn("package_id", first["package"])
            self.assertNotIn("package_version", first["package"])

    def test_registry_generation_requires_registration_ready_package(self) -> None:
        with self.make_package() as directory:
            root = Path(directory)

            record = MODEL.registry_record_for_cli(
                root,
                profile=PROFILE,
                profile_sha256=PROFILE_SHA256,
                generator_version="test",
            )

            self.assertEqual(
                record["package"]["survey_id"],
                "survey_001",
            )
            self.assertEqual(
                record["sampling_summary"]["observation_count"],
                1,
            )
            self.assertEqual(
                record["sampling_summary"]["target_reference_count"],
                1,
            )
            self.assertEqual(
                record["sampling_summary"]["target_count"],
                1,
            )
            self.assertEqual(
                record["sampling_summary"]["targets"],
                [
                    {
                        "target_id": "Polaris",
                        "observation_reference_count": 1,
                    }
                ],
            )

            survey_path = root / "survey.json"
            survey = json.loads(survey_path.read_text(encoding="utf-8"))
            survey["working_representation"] = {
                "compass-observation": {
                    "angle_deg": "rad",
                }
            }
            survey_path.write_text(
                json.dumps(survey, indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(MODEL.RegistrationGenerationError):
                MODEL.registry_record_for_cli(
                    root,
                    profile=PROFILE,
                    profile_sha256=PROFILE_SHA256,
                    generator_version="test",
                )


if __name__ == "__main__":
    unittest.main()
