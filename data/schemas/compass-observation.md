# Compass Observation Specification (Draft 0.1)

## Purpose

This document defines the canonical raw observation format for astronomical observations made with a compass.

A compass observation preserves the instrument-native bearing obtained for one identified target. True-azimuth corrections, magnetic-declination corrections, predicted azimuth, residuals, celestial coordinates, and other derived quantities are excluded from the raw observation table.

## Observation Table

Each row represents one intentional act of measurement.

Required columns, in order:

1. `observation_id`
2. `observer_id`
3. `instrument`
4. `target_name`
5. `angle_deg`
6. `observed_at`

## Field Definitions

| Field | Type | Semantic class | Canonical unit or format | Description |
|---|---|---|---|---|
| `observation_id` | string | identifier | not applicable | Stable identifier for the observation. |
| `observer_id` | string | identifier | not applicable | Participant who performed the measurement. |
| `instrument` | string | categorical value | `compass` | Instrument design used for the observation. |
| `target_name` | string | target label | not applicable | Target name recorded by the observer. |
| `angle_deg` | number | physical quantity | degree | Raw compass bearing, measured clockwise from the instrument's north reference. |
| `observed_at` | string | temporal value | ISO 8601 date-time | UTC timestamp of the measurement. |

## Bearing Reference

`angle_deg` records the compass reading as observed. It is not corrected to true north unless the physical instrument itself directly reports a true-north bearing. Any magnetic-declination correction belongs in analysis and must preserve linkage to the raw bearing.

## Survey Context

Survey-level metadata, including observing location, physical instrument instance, protocol, and scientific question, are recorded in `survey.json`. The corresponding `observation_tables` entry identifies the physical instrument instance and this observation specification.

## Standardization

Every table conforming to the same version of this specification must use identical column names, column order, data types, and units so that validated tables can be concatenated without manual restructuring.

## Derived Data

Corrected azimuth, magnetic declination, predicted azimuth, residuals, celestial coordinates, and model estimates are analysis products and must not appear in the canonical raw observation table.

## Status

Draft 0.1 was developed from Pilot Astronomical Survey 001 using a Brunton Type 7 compass.
