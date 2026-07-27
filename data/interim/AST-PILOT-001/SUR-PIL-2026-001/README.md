# Pilot Astronomical Survey 001

**Survey ID:** `SUR-PIL-2026-001`  
**Survey type:** `astronomical_observation`  
**Scientific question:** Where is Ursa Major?

## Observational context

- Observers: `OBS-0001`, `OBS-0002`
- `OBS-0001` performed the instrument measurements.
- `OBS-0002` assisted by recording times and other values.
- Location: 34.40732° N, 118.56714° W (WGS84)
- Recorded elevation: 1230 ft; represented in `survey.json` as 374.904 m.
- Observation interval: 2026-07-26T04:22:57Z to 2026-07-26T07:54:47Z
- Protocol: no specific protocol identifier or version was assigned.

## Observation tables

- `observations/quadrant-observations.csv` — provisional quadrant working format Draft 0.1; instrument instance `INS-0002`.
- `observations/compass-observations.csv` — provisional compass working format Draft 0.1; instrument instance `INS-0003`.
- `observations/cross-staff-observations.csv` — cross-staff working format Draft 0.3; instrument instance `INS-0001`.

Each table preserves its instrument-native measurements. The quadrant and compass tables were split from the reconciled combined working table without changing row values.

## Files

- `survey.json` — survey metadata and observation-table manifest.
- `observations/` — instrument-specific reconciled working tables.
- `notes.csv` — empty; no narrative notes were recorded.
- `attachments/raw_values.csv` — original quadrant and compass source data.
- `attachments/cross-staff-raw.csv` — original cross-staff source data.
- `reconciliation.log` — survey-level reconciliation record.
- `checksums.sha256` — SHA-256 hashes for archive files.

## Archive status

This is a **preliminary archive**, not a submission-ready archive.

- Cross-staff `fiducial_width` and `staff_reading` remain in their recorded source unit of inches.
- Canonical-unit normalization has not yet been performed.
- Quadrant and compass observation schemas remain to be authored and validated.
- `INS-0003` is used for the compass in this archive and should be checked against the instrument registry before submission readiness.
- No derived angles, coordinates, residuals, predictions, or fitted values are included.
