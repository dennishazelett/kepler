Cross-Staff Observation Specification (Draft 0.3)

## Purpose

This document defines the raw observation formats for cross-staff surveys.

Cross-staff observations preserve the instrument-native measurements used to estimate angular separation. Calculated angles, residuals, coordinate estimates, fitted parameters, and other derived quantities are excluded from raw observation tables.

## Shared Requirements

Every observation table must contain:

- `schema_version`

- `survey_id`

- `observation_id`

- `observed_at`

- `observer_id`

- `instrument_instance_id`

- `fiducial_width`

- `staff_reading`

- `notes_id`

- `calibration`

- `field_observation`

Each row represents one independent act of measurement.

Physical measurements may initially be archived in their documented source units during reconciliation and preliminary archive construction. Before validation and submission, all physical quantities in the canonical observation table must be normalized to the canonical units defined by this specification.

Original working data may be retained unchanged as a survey attachment. A separate conversion record is optional when the source values, source units, and deterministic normalization rule are otherwise recoverable.

## Shared Field Definitions

| Field | Type | Semantic class | Canonical unit or format | Description |
|----|----|----|----|----|
| `schema_version` | string | schema identifier | not applicable | Version of this observation specification. |
| `survey_id` | string | identifier | not applicable | Survey containing the observation. |
| `observation_id` | string | identifier | not applicable | Stable identifier for the observation. |
| `observed_at` | string | temporal value | ISO 8601 date or date-time | Date or timestamp of the measurement. Preserve the precision supported by the source record. |
| `observer_id` | string | identifier | not applicable | Observer responsible for the measurement. |
| `instrument_instance_id` | string | identifier | not applicable | Physical cross-staff used for the measurement. |
| `fiducial_width` | number | physical quantity | `mm` | Width of the crosspiece segment used to span the observed targets. |
| `staff_reading` | number | physical quantity | `mm` | Position of the crosspiece measured from the instrument origin along the staff. |
| `notes_id` | string or null | identifier | not applicable | Optional link to a separate narrative note. |
| `calibration` | object or null | observation context | not applicable | Calibration reference geometry. Non-null only for calibration observations. |
| `field_observation` | object or null | observation context | not applicable | Target pair measured in a field observation. Non-null only for field observations. |

`fiducial_width` and `staff_reading` must use compatible length units during analysis. In a submission-ready canonical observation table, both are expressed in millimetres.

## Calibration Observations

Calibration surveys characterize an observer–instrument measurement system using known reference geometry.

For a calibration observation:

- `calibration` must contain a calibration object;

- `field_observation` must be null.

Required calibration fields:

- `target_id`

- `target_width`

- `target_distance`

| Field | Type | Semantic class | Canonical unit or format | Description |
|----|----|----|----|----|
| `target_id` | string | identifier | not applicable | Identifier of the calibration target. |
| `target_width` | number | physical quantity | `mm` | Known physical width of the calibration target. |
| `target_distance` | number | physical quantity | `mm` | Distance from the observer or instrument origin to the calibration target, as defined by the calibration protocol. |

These fields describe the calibration reference and setup rather than attributes of the cross-staff.

## Field Observations

Field surveys measure angular relationships between celestial or terrestrial targets.

For a field observation:

- `field_observation` must contain a field-observation object;

- `calibration` must be null.

Required field-observation fields:

- `primary_target_id`

- `secondary_target_id`

| Field | Type | Semantic class | Canonical unit or format | Description |
|----|----|----|----|----|
| `primary_target_id` | string | identifier | not applicable | Identifier of the target aligned with one edge of the fiducial. |
| `secondary_target_id` | string | identifier | not applicable | Identifier of the target aligned with the opposite edge of the fiducial. |

Target ordering must be preserved from the source record. The specification does not assert that the order has geometric or directional meaning beyond the executed observing protocol.

Possible future fields include instrument orientation, eye used, target-acquisition method, and observing conditions. These should not become required until supported by field experience.

## Notes

Narrative comments should be stored separately and linked through `notes_id`.

## Versioning Note

Draft 0.3 replaces `fiducial_id` with `fiducial_width`.

Data created under Drafts 0.1 or 0.2 must not be migrated by renaming alone unless the original `fiducial_id` value is confirmed to represent a physical fiducial width. Its source unit must also be established before normalization.

Draft 0.3 retains millimetres as the canonical unit for all length fields.

## Status

This specification incorporates evidence from Cross-Staff Calibration Survey 001 and the first astronomical cross-staff field observations. It remains preliminary and may be revised after the pilot survey has been archived, validated, and analyzed.
