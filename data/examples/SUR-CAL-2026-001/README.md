# SUR-CAL-2026-001

Preliminary Kepler survey package generated from the first cross-staff terrestrial calibration dataset.

## Contents

- `survey.json` — survey-level metadata and units
- `observations.csv` — canonical raw observation table; one header row and one observation per row
- `notes.csv` — free-text notes linked by `observation_id`
- `attachments/` — supporting photographs or other files
- `checksums.sha256` — SHA-256 checksums for the package files

## Important provisional assignments

The source CSV did not provide stable identifiers or explicit unit metadata. This package provisionally assigns:

- observer ID: `OBS-D-HAZELETT`
- instrument instance ID: `CS-0001`
- length units: inches (`in`)

These assignments should be confirmed before this package is treated as an accepted submission.

Calculated fields from the source workbook (`expected`, `measured`, and `residual`) are not included.

## Attachments

| File | Description |
|----|----|
| calibration-range.jpeg | Photograph of the terrestrial calibration range used during this survey. |
| assembled_crossstaff.jpeg | Photograph of the instrument used during the survey. |
| crosspiece_detail.jpeg | Close-up of the crosspiece and fiducial markings used for measurement. |

These attachments document the experimental context and instrument configuration. They supplement, but do not replace, the canonical observation table.
