# SUR-CAL-002 — Quadrant Calibration Survey 002

## Scientific question

Given a known reference, how does a particular observer–instrument measurement system behave?

## Survey type

Instrument Calibration Survey

## Instrument and observers

- Instrument design: quadrant
- Instrument instance: `INS-0002`
- Measuring observer: `OBS-0001`
- Recorder: `OBS-0002`
- Site: `SITE-0001` (`34.40732`, `-118.56714`, WGS84)
- Observation date: 2026-07-25 UTC

## Canonical observation table

`observations/quadrant-calibration-observations.csv` contains 48 raw quadrant calibration readings and conforms to the Quadrant Calibration Observation Specification Draft 0.1.

Each row preserves the target identifier, known target vertical offset relative to eye level, raw quadrant angle, observer, instrument, and UTC observation time.

## Representational normalization

- `reference_target_id` was normalized to `target_id`.
- Target vertical offsets recorded in inches were converted deterministically to meters and stored as `target_vertical_offset_m`.
- `observed_time_utc` was normalized to `observed_at`.
- The supplied date, `2026-07-25`, was combined with each UTC time to form ISO 8601 timestamps.
- Raw `angle_deg` values were preserved without alteration.
- No predicted angles, residuals, fitted corrections, or inferred calibration parameters were added.

## Attachments

The archive preserves the original raw and working tables, normalized working table, calibration geometry, calibration-range photograph, calibration protocol, and supplied survey and observation specifications under `attachments/`.

## Assumptions and unresolved metadata

- The supplied calendar date applies to every observation row.
- `OBS-0002` is included as a survey observer because the calibration geometry identifies that participant as recorder.
- Elevation, protocol identifier, and protocol version were not supplied and are recorded as `null`.
- The horizontal calibration distance remains in the supplied geometry attachment and is not duplicated in each observation row because it is shared campaign context.
