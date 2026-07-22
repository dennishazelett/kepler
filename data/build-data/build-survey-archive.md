# Build Kepler Survey Archive

Using the attached files and the Kepler Survey Specification, construct a complete Kepler survey package.

## Inputs

The prompt will provide:

- Survey Specification (`survey-specification.md`)
- Source observational data (CSV, XLSX, etc.)
- Optional notes
- Optional photographs or other attachments
- Survey metadata supplied below

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
4. Separate narrative notes from the observation table.
5. Preserve all supplied attachments.
6. Do not invent metadata or observations. If required information is missing, leave a placeholder or report it.
7. Produce a survey that conforms to the attached Survey Specification.

## Output

Generate the following directory:

```
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

- scientific question
- survey type
- instrument
- observer(s)
- files included
- assumptions made during archive construction

### survey.json

Record survey metadata only.

### observations.csv

Canonical raw observation table.

Requirements:

- one header row
- one observation per row
- no formulas
- no derived variables
- standardized column names

### notes.csv

Store narrative observations linked by `observation_id`.

### attachments/

Copy all supplied attachments unchanged.

### checksums.sha256

Generate SHA-256 hashes for every file in the survey package.

## Final Report

Summarize:

- files created
- assumptions made
- missing information
- validation concerns