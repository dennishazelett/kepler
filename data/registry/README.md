# Kepler Survey Registry

## Status

The Kepler Survey Registry is not yet operational. This directory documents the current intended workflow for registering externally hosted survey-package snapshots with Kepler.

The repository includes versioned schemas, a registration profile, local generation tools, and test coverage for declared survey-package registration artifacts. Registry submission tooling and any public discovery interface remain under development. Nothing in this document creates a requirement that Kepler host, preserve, independently retrieve, independently validate, certify, or endorse contributor data.

## Purpose

The registry is intended to help the Kepler community discover survey packages that contributors have chosen to host and share elsewhere.

A registry entry will identify one specific immutable survey-package snapshot and may preserve contributor-supplied declared validation evidence for that snapshot. The registry is not a survey archive: the contributor or a designated custodian retains ownership and control of the external package source.

## What Registration Means

Registration is a Kepler-maintained discovery record for one externally hosted survey-package snapshot. It does not:

- transfer ownership, copyright, custody, or hosting responsibility to Kepler;
- create a Kepler archive or preservation guarantee;
- certify the package, contributor, observations, data quality, or scientific conclusions;
- independently establish that the external package is complete, accurate, safe, lawful, private, or suitable for every audience; or
- require Kepler to independently retrieve or rerun validation against the external package.

A merged registry entry is expected to have the public status `registered`. That status means that Kepler accepted a reference to the identified external package snapshot and its declared validation evidence into the registry. It does not imply endorsement or certification.

## Survey Archive Model

Contributors may maintain multiple survey packages in one repository or other supported external archive that they control. Each package occupies its own package directory.

For a Git-hosted survey archive, a registration identifies exactly one package through all of the following:

- the source repository locator;
- the full resolved Git commit SHA;
- the package-relative path within that commit; and
- the canonical SHA-256 digest of the package contents.

The commit SHA identifies the repository tree; the package path and package digest identify the exact survey package within that tree. A commit may contain other changes elsewhere in the archive without changing the identity of the registered package at its declared path and digest.

## Preliminary Registration Workflow

The intended order is important. Contributors should validate the exact package contents before designating a commit for public registration.

1.  Prepare or revise one survey package directory in an external archive under the contributor's or custodian's control.
2.  Generate the declared-package validation report for that exact working-tree package using `data/build-data/generate-validation-report.py`.
3.  Resolve reported errors and repeat validation until the report has no errors, the archive status is `valid_canonical_archive`, and submission readiness is `true`.
4.  Generate the registry record using `data/build-data/generate-registry-record.py`. Registry-record generation refuses packages that do not meet those eligibility conditions.
5.  Commit the validated survey package and its generated `registry.json` and `validation-report.json`. This commit creates the source snapshot intended for registration.
6.  Record the full commit SHA, package-relative path, and declared-package SHA-256 digest. Confirm that they identify the package represented by the generated report and registry record.
7.  Fork the Kepler repository and open a pull request containing only the registry artifacts described below.
8.  A Kepler maintainer reviews the submitted registry claim and evidence for completeness, internal consistency, and policy conformance. Kepler does not independently retrieve or rerun validation against the external package unless this is explicitly stated by a future process.
9.  Merging the pull request registers the identified external snapshot in the Kepler discovery registry.

## Local Registration Artifacts

The local registration tools operate on one survey package directory. They derive package identity only from declared survey inputs:

- `survey.json`;
- every path in `survey.json.observation_tables`;
- every path in `survey.json.attachments`.

The digest excludes `registry.json` and `validation-report.json`. It also ignores unreferenced workspace files when calculating identity. Undeclared regular files and symbolic links produce warnings in the declared-package validation report; a manifest-declared symbolic link, a missing declared file, or a declared path that escapes the package directory is an error.

The digest processes declared files in normalized package-relative POSIX-path order, using Unicode code-point ordering. For each file, it appends the UTF-8 encoded relative path, a NUL byte, the raw file bytes, and a final NUL byte to the digest input stream. The resulting identity digest is SHA-256.

Run the tools from the repository root:

```bash
python data/build-data/generate-package-digest.py PATH/TO/SURVEY
python data/build-data/generate-validation-report.py PATH/TO/SURVEY > PATH/TO/SURVEY/validation-report.json
python data/build-data/generate-registry-record.py PATH/TO/SURVEY > PATH/TO/SURVEY/registry.json
```

The generated registry record and validation report identify the package as:

```json
{
  "survey_id": "…",
  "content_sha256": "…"
}
```

`survey_id` comes from `survey.json`; the tools do not define or require a separate package ID or package version. The validation report records the identity and version of the validator that performed validation, as well as the versioned registration profile used for derivation.

## Intended Pull Request Contents

A registration pull request is expected to contain:

- one human-readable YAML registry record under `data/registry/records/`;
- one linked, structured validation report under `data/registry/validation-reports/`; and
- no copied survey observation tables, attachments, or survey-package archive.

The registry record will be a concise discovery and identity document. The validation report will preserve the potentially detailed contributor-supplied evidence for the declared validation result. The two artifacts bind to the same `survey_id` and declared-package digest. The pull request also identifies the external source revision and package-relative path for the registered snapshot. The validation report records the profile and the validator identity and version that produced the declared result.

The registry-record schema, declared-package validation-report schema, and registration profile live in `data/schemas/`. Submission review and public-discovery processes remain under development.

## Validation Evidence

A registry entry may include contributor-supplied declared validation evidence for a specified Kepler validation profile. Until an explicitly labeled future process exists, Kepler does not independently retrieve or rerun validation against the external package.

Registry materials must not describe a package as unqualifiedly validated, verified, approved, trusted, recommended, or certified. They should instead identify the declared validation profile, validator version, result, and source of the submitted evidence.

## Updates and Corrections

A registration applies to one immutable package snapshot. If package contents change, the contributor must create a new validated snapshot and submit a new registration request with:

- a new full commit SHA;
- a new package digest;
- new declared validation evidence; and
- a new registry record and validation report.

Existing registry records and their historical validation claims must not be silently rewritten. Future status changes may mark an entry as `withdrawn`, `delisted`, or `unavailable`, but do not alter the package identity originally registered.

## Public-Disclosure Notice

Contributors are responsible for deciding whether they have the right to publish their package and request registry listing. They should review their package, attachments, metadata, rendered materials, and source-repository history before public release.

**Location and privacy warning:** Public survey packages may disclose exact coordinates, observing times, observer identities, routines, photographs, device metadata, filenames, attachments, or repository history. These details may reveal a home, school, observing site, or other sensitive location. Kepler registration may make externally hosted material easier to discover.

Kepler does not host, comprehensively monitor, or comprehensively screen externally hosted packages for personal, private, sensitive, legally restricted, or otherwise unsuitable information. Contributors are responsible for what they publish through their chosen host.

## Related Policy

This workflow is governed by Kepler's Data Curation and Registration Policy. That policy defines the broader responsibilities and limitations of contributors, external hosts, Kepler registry curation, optional future preservation, and potential future aggregate data products.

The registry may later support optional preservation copies or generated aggregate collections. Neither capability is currently implemented, required for registration, or a substitute for the contributor-controlled source package.
