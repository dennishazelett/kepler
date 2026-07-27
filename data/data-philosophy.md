# Data Philosophy

## Purpose

Why Kepler collects observations rather than conclusions.

## Scientific Objects

Observation
Survey
Instrument
Observer
Protocol

## Raw Data First

Only directly observed quantities belong in the canonical raw dataset.

Derived quantities belong in analyses.

## Surveys

A survey is the primary unit of contribution.

A survey consists of observations made for a common scientific purpose under a shared context.

## Observations

An observation is one atomic act of measurement.

One observation corresponds to one row in the canonical observation table.

## Instrument-specific Measurements

Different instruments measure different physical quantities.

The submission standard preserves those measurements rather than forcing premature translation into a universal measurement format.

## Reproducibility

Every observation must be traceable to

- observer
- instrument instance
- protocol
- survey

## Immutability

Accepted raw observations are never silently modified.

Corrections produce new records.

## Standardization

The canonical observation table must be directly appendable without manual cleanup.

Every accepted submission conforms to a published schema.

Observation specifications define canonical units and formats. Contributors may work in other units, but submitted observations must be deterministically normalized to the declared canonical representation before validation. This normalization changes representation, not scientific content; original working data and conversion provenance may be preserved with the survey.

## Derived Data

Angles
Coordinates
Residuals
Predictions

are products of analysis, not observations.

They remain linked to the raw observations but are stored separately.
