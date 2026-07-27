# Quadrant Observation Specification (Draft 0.1)

## Purpose

This document defines the canonical raw observation format for astronomical observations made with a quadrant.

A quadrant observation preserves the instrument-native angular reading obtained for one identified target. Predicted altitude, residuals, celestial coordinates, fitted corrections, and other derived quantities are excluded from the raw observation table.

## Observation Table

Each row represents one intentional act of measurement.

Required columns, in order:

1. `observation_id`
2. `observer_id`
3. `instrument`
4. `target_id`
5. `angle_deg`
6. `observed_at`

## Field Definitions

| Field | Type | Semantic class | Canonical unit or format | Description |
|---|---|---|---|---|
| `observation_id` | string | identifier | not applicable | Stable identifier for the observation. |
| `observer_id` | string | identifier | not applicable | Participant who performed the measurement. |
| `instrument` | string | categorical value | `quadrant` | Instrument design used for the observation. |
| `target_id` | string | target label | not applicable | Target name recorded by the observer. |
| `angle_deg` | number | physical quantity | degree | Raw quadrant angle reading. Positive values represent targets above the instrument's level reference; negative values are permitted when supported by the instrument reading. |
| `observed_at` | string | temporal value | ISO 8601 date-time | UTC timestamp of the measurement. |

## Survey Context

Survey-level metadata, including observing location, physical instrument instance, protocol, and scientific question, are recorded in `survey.json`. The corresponding `observation_tables` entry identifies the physical instrument instance and this observation specification.

## Standardization

Every table conforming to the same version of this specification must use identical column names, column order, data types, and units so that validated tables can be concatenated without manual restructuring.

## Derived Data

Predicted altitude, astronomical coordinates, calibration corrections, residuals, and model estimates are analysis products and must not appear in the canonical raw observation table.

## Status

Draft 0.1 was developed from Pilot Astronomical Survey 001.
