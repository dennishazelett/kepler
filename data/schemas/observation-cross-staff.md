# Cross-Staff Observation Specification (Draft 0.1)

## Purpose

This document defines the canonical raw observation formats for cross-staff surveys.

Cross-staff observations preserve the instrument-native measurements used to estimate angular separation. Calculated angles, residuals, coordinate estimates, and other derived quantities are excluded from raw observation tables.

## Shared Requirements

Every observation table must contain:

- `schema_version`
- `survey_id`
- `observation_id`
- `observed_at`
- `observer_id`
- `instrument_instance_id`
- `fiducial_id`
- `staff_reading`
- `notes_id`

Each row represents one independent act of measurement.

Units and instrument geometry must be defined by the applicable instrument specification or survey metadata.

## Calibration Observations

Calibration surveys characterize an observer–instrument measurement system using known reference geometry.

Additional required fields:

- `target_id`
- `target_width`
- `target_distance`

Optional fields may describe target orientation, lighting, or controlled setup conditions.

## Field Observations

Field surveys measure angular relationships between celestial or terrestrial targets.

Additional required fields:

- `primary_target_id`
- `secondary_target_id`

Possible future fields include instrument orientation, observing site, eye used, and target acquisition method. These should not become required until supported by practical field experience.

## Notes

Narrative comments should be stored separately and linked through `notes_id`.

## Status

This preliminary specification is based on Cross-Staff Calibration Survey 001 and will be revised after the first astronomical field survey.
