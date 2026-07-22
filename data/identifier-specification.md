# Identifier Specification (Draft 0.1)

## Purpose

Identifiers provide stable references to the scientific objects that comprise the Kepler data model.

Identifiers are intended to support reproducibility, provenance, and unambiguous linkage between surveys, observations, instruments, notes, attachments, and future data products.

Identifiers are not scientific measurements and should never encode scientific conclusions.

------------------------------------------------------------------------

# General Principles

Identifiers should be:

- unique within their intended scope;
- stable once assigned;
- human-readable where practical;
- independent of file names and directory structure.

Identifiers should not be reassigned.

------------------------------------------------------------------------

# Identifier Scope

## Survey

A survey identifier uniquely identifies one submitted survey.

Example:

``` text
SUR-2026-0001
```

Survey identifiers are assigned by the contributor when creating the survey.

------------------------------------------------------------------------

## Observation

An observation identifier uniquely identifies one observation.

Observation identifiers should be unique within a survey.

A recommended convention is:

``` text
<survey-id>-0001
<survey-id>-0002
...
```

Examples:

``` text
SUR-2026-0001-0001
SUR-2026-0001-0002
```

Observation identifiers are assigned by the contributor.

------------------------------------------------------------------------

## Observer

Observers are identified by stable observer identifiers.

Example:

``` text
OBS-0001
```

Observer identifiers should remain constant across multiple surveys.

------------------------------------------------------------------------

## Instrument Instance

Each physical instrument receives a stable identifier.

Example:

``` text
INS-0001
```

Instrument identifiers refer to physical instruments rather than instrument designs.

The same instrument may participate in multiple surveys.

------------------------------------------------------------------------

## Notes

Narrative notes may be referenced by note identifiers.

Example:

``` text
NOTE-0001
```

Notes should reference observations rather than duplicate observational data.

------------------------------------------------------------------------

## Attachments

Supporting files may be assigned attachment identifiers.

Example:

``` text
ATT-0001
```

Attachment identifiers allow photographs, sketches, and other materials to be referenced independently of file names.

------------------------------------------------------------------------

# Repository Identifiers

After validation and acceptance, repositories may assign additional identifiers (for example, cryptographic hashes or accession identifiers).

Repository identifiers supplement contributor-assigned identifiers and do not replace them.

------------------------------------------------------------------------

# Reserved Prefixes

Current prefixes include:

| Prefix | Entity              |
|--------|---------------------|
| SUR    | Survey              |
| OBS    | Observer            |
| INS    | Instrument Instance |
| NOTE   | Note                |
| ATT    | Attachment          |

Additional prefixes may be introduced as the data model evolves.

------------------------------------------------------------------------

# Status

This specification defines identifier conventions for Draft 0.1 of the Kepler data model and is expected to evolve alongside the survey specification.
