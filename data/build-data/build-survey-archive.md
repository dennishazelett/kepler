# Build Kepler Survey Archive

Using the attached files and the Kepler Survey Specification, construct a complete Kepler survey package.

## Inputs

The prompt will provide:

* Survey Specification (`survey-specification.md`)
* Observation Specification (if applicable)
* Source observational data (CSV, XLSX, etc.)
* Optional notes
* Optional photographs or other attachments
* Survey metadata supplied below

## Survey Metadata

Survey ID:
Survey Type:
Scientific Question:
Observer(s):
Instrument Instance:
Instrument Design:
Protocol Version:
Observation Specification:
Site:
Date(s):
Schema Version:

## Requirements

1. Preserve only raw observations.
2. Exclude all derived quantities unless explicitly requested.
3. Preserve instrument-native measurements.
4. Normalize all physical quantities to the canonical units defined by the applicable Observation Specification before generating the canonical observation table.
5. Preserve the measured quantity during normalization. Unit conversion is representational normalization, not scientific derivation.
6. Separate narrative notes from the observation table.
7. Preserve all supplied attachments.
8. Do not invent metadata or observations. If required information is missing, leave a placeholder or report it.
9. Produce a survey that conforms to the attached Survey Specification and applicable Observation Specification.

## Output

Generate the following directory:

```text
<survey-id>/
├── README.md
├── survey.json
├── observations.csv
├── notes.csv
├── attachments/
└── checksums.sha256
```

### README.md

Summarize:

* scientific question
* survey type
* instrument
* observer(s)
* files included
* assumptions made during archive construction
* unit conversions or other representational normalizations performed

### survey.json

Record survey metadata only.

### observations.csv

Canonical raw observation table.

Requirements:

* one header row
* one observation per row
* no formulas
* no derived variables
* standardized column names
* all physical quantities expressed in the canonical units required by the applicable Observation Specification

### notes.csv

Store narrative observations linked by `observation_id`.

### attachments/

Copy all supplied attachments unchanged.

The original observational data supplied by the contributor may be included unchanged when appropriate to preserve provenance.

### checksums.sha256

Generate SHA-256 hashes for every file in the survey package.

## Final Report

Summarize:

* files created
* assumptions made
* unit conversions or other representational normalizations performed
* missing information
* validation concerns

Before declaring the survey package complete, verify that:

* all physical quantities use the canonical units required by the Observation Specification;
* required metadata are present;
* the observation table conforms to the applicable Observation Specification;
* the survey metadata conform to the Survey Specification;
* the completed survey package is ready for validation.
