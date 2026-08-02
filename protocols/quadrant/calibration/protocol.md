# Quadrant Calibration Protocol

**Protocol ID:** `quadrant-calibration` **Protocol Version:** `0.1.0` **Status:** Draft

------------------------------------------------------------------------

# Purpose

This protocol describes a standardized procedure for characterizing the performance of a quadrant observer–instrument measurement system under controlled conditions.

The observer measures calibration-target geometry and records quadrant readings. Reference angles are subsequently inferred from the measured target height, observer distance, and target height relative to eye level. These inferred angles are compared with the quadrant readings during analysis.

Calibration documents measurement performance; it does not modify or correct subsequent observations.

------------------------------------------------------------------------

# Scope

This protocol applies to calibration surveys performed using the Kepler quadrant instrument.

It is intended for initial instrument characterization, post-repair verification, instructional exercises, and periodic performance checks.

This protocol is not intended for astronomical field observations.

------------------------------------------------------------------------

# Scientific Question

> How do quadrant readings obtained by this observer–instrument system compare with angles inferred from independently measured calibration geometry?

------------------------------------------------------------------------

# Required Equipment

- Kepler quadrant

<!-- -->

- 5 calibration targets at 1 ft (or 0.3m) intervals, starting at eye level

- Measuring device suitable for determining horizontal observer distance

- Measuring device suitable for determining target and eye-level heights

- Recording materials or electronic data collection device

- Applicable quadrant calibration observation specification

------------------------------------------------------------------------

# Prerequisites

Before beginning the calibration survey:

- the quadrant should be complete and mechanically functional;

- the plumb line should move freely without obstruction;

- the observer should be familiar with normal quadrant operation;

- the observer position and calibration target should remain fixed while observations associated with that geometry are collected; and

- the required distances and heights should be measurable independently of the quadrant.

------------------------------------------------------------------------

# Observation Procedure

For each marked reference point on the calibration target:

1.  Establish the observer position and calibration target.

2.  Measure and record the calibration geometry as required by the applicable observation specification.

3.  Sight the marked reference point using the quadrant.

4.  Allow the plumb line to stabilize.

5.  Record the quadrant reading exactly as observed.

6.  Lower the quadrant away from the target before beginning the next observation.

7.  Repeat Steps 3–6 until **five independent observations** have been recorded for the same reference point.

8.  Repeat for each remaining marked reference point.

9.  Repeat the geometry measurements whenever the observer position, target position, eye height, or other relevant setup geometry changes.

Reference angles must not be entered into the canonical observation table unless they were directly supplied as source measurements. Angles calculated from the recorded geometry are derived quantities and belong in the subsequent analysis.

------------------------------------------------------------------------

# Data Requirements

Observations produced by this protocol shall conform to the applicable quadrant calibration observation specification.

The observation specification defines:

- required observation fields;
- field semantics;
- canonical representations;
- permitted data types; and
- required metadata.

This protocol does not redefine those requirements.

------------------------------------------------------------------------

# Quality Control

Observers should:

- verify that the instrument remains mechanically stable throughout the survey;
- avoid disturbing the plumb line before readings are recorded;
- ensure that each observation represents a single intentional measurement;
- record observations directly without retrospective reconstruction; and
- document any unusual conditions affecting measurement quality.

> Consecutive observations should represent independent measurement attempts. Observers should not record multiple readings from a single instrument alignment. Whenever practical, observations of the same reference point should be interleaved with observations of other reference points. When consecutive observations of the same reference point are necessary, the quadrant should be completely lowered and realigned before each observation.

If an observation cannot reasonably be trusted, retain the observation only when its circumstances are fully documented. Otherwise, repeat the measurement and record the replacement observation.

------------------------------------------------------------------------

# Deviations from Protocol

Departures from this protocol do not automatically invalidate a survey.

Any deviation that could influence interpretation should be documented in the survey notes, including sufficient information for later review.

Examples include:

- equipment malfunction;
- environmental disturbances;
- changes to calibration geometry;
- interrupted observation sequences; and
- observer errors recognized during data collection.

------------------------------------------------------------------------

# Expected Outputs

A survey produced using this protocol should include:

- `survey.json`
- one or more quadrant calibration observation tables conforming to the applicable observation specification;
- `notes.csv`, when applicable;
- supporting attachments, when applicable; and
- any required provenance information.

------------------------------------------------------------------------

# References

- Kepler Survey Specification
- Quadrant Calibration Observation Specification
- Kepler Quadrant Instrument Documentation
