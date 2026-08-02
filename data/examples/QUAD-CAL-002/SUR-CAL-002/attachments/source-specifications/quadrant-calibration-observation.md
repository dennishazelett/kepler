# Quadrant Calibration Observation Specification (Draft 0.1)

## Purpose

This document defines the canonical raw observation format for calibration observations made with a quadrant.

A quadrant calibration observation preserves the instrument-native angular reading obtained for one identified calibration target together with the known vertical geometry required to interpret that reading. Predicted angles, residuals, fitted corrections, inferred observer parameters, and other derived quantities are excluded from the raw observation table.

The calibration target geometry is part of the reference setup supplied to the observation and is not a derived quantity.

## Observation Table

Each row represents one intentional act of measurement.

Required columns, in order:

1. `observation_id`
2. `observer_id`
3. `instrument`
4. `target_id`
5. `target_vertical_offset_m`
6. `angle_deg`
7. `observed_at`

## Field Definitions

| Field | Type | Semantic class | Canonical unit or format | Description |
|---|---|---|---|---|
| `observation_id` | string | identifier | not applicable | Stable identifier for the observation. |
| `observer_id` | string | identifier | not applicable | Participant who performed the measurement. |
| `instrument` | string | categorical value | `quadrant` | Instrument design used for the observation. |
| `target_id` | string | target identifier | not applicable | Stable identifier or recorded label for the calibration target intentionally measured by the observer. |
| `target_vertical_offset_m` | number | physical quantity | meter | Signed vertical displacement of the calibration target relative to the observer's eye-level reference. Positive values are above eye level, zero is at eye level, and negative values are below eye level. |
| `angle_deg` | number | physical quantity | degree | Raw quadrant angle reading. Positive values represent targets above the instrument's level reference; negative values are permitted when supported by the instrument reading. |
| `observed_at` | string | temporal value | ISO 8601 date-time | UTC timestamp of the measurement. |

## Survey Context

Survey-level metadata, including observing location, physical instrument instance, protocol, scientific question, and calibration campaign context, are recorded in `survey.json`. The corresponding `observation_tables` entry identifies the physical instrument instance and this observation specification.

Any additional calibration geometry shared by all observations may be preserved in survey metadata or supporting attachments. Values required to interpret individual rows must remain in the canonical observation table.

## Standardization

Every table conforming to the same version of this specification must use identical column names, column order, data types, and units so that validated tables can be concatenated without manual restructuring.

Source measurements recorded in feet or other units must be converted deterministically to meters before inclusion in the canonical observation table. The original working representation may be retained as an attachment for provenance.

## Derived Data

Predicted angles, calibration corrections, residuals, fitted model parameters, inferred eye height, and other model estimates are analysis products and must not appear in the canonical raw observation table.

## Status

Draft 0.1 was developed from the first Kepler quadrant calibration campaign.
