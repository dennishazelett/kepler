# Schemas

This directory contains the formal machine-readable definitions used to validate Kepler data.

Schemas implement the standards described in the data documentation. They define the required structure, field names, data types, and validation rules for data submitted to the Kepler ecosystem.

Schemas describe **how data are represented**, not **why they are collected**.

## Relationship to the Data Model

The conceptual data model is documented in:

- [`../data/data-philosophy.md`](../data/data-philosophy.md)
- [`../data/survey-specification.md`](../data/survey-specification.md)

Schemas are implementations of those specifications.

## Purpose

Schemas enable:

- automated validation of submitted surveys;
- consistent data representation;
- interoperability between software components;
- reproducible dataset construction.

## Planned Schemas

Examples include:

- survey schema
- observation schema(s)
- instrument schema
- observer schema
- site schema
- data dictionary

Different survey and instrument types may require different observation schemas while remaining compatible with the overall survey specification.

## Versioning

Schemas are versioned.

Accepted surveys should record the schema version against which they were validated to ensure long-term reproducibility.

As the project evolves, newer schemas may be introduced without invalidating historical submissions.