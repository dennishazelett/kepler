# Data

This directory contains the emerging data architecture for Kepler.

Its purpose is to define how observations are represented, validated, archived, and ultimately combined into a shared scientific dataset.

During early development, this directory serves as a staging area for the future **`kepler-data`** repository. Once the data model and submission workflow have matured, this directory will be migrated into its own repository while remaining closely coupled to the main Kepler project.

## Organization

- [`data-philosophy.md`](data-philosophy.md) — Guiding principles governing the representation and stewardship of scientific data.
- [`survey-specification.md`](survey-specification.md) — The canonical specification describing the structure of a Kepler survey.
- [`examples/`](examples/) — Reference implementations of valid survey packages.
- [`build-data/`](build-data/) — Prompts, workflows, and utilities for constructing and validating survey archives.

## Design Principles

The Kepler data model is built around several core ideas:

- observations are the atomic units of scientific evidence;
- surveys are the primary units of contribution;
- raw observations are preserved exactly as measured;
- derived quantities are generated through analysis and stored separately;
- all accepted observation tables are standardized and directly appendable without manual preprocessing.

These principles are described in greater detail in the accompanying documentation.

## Relationship to the Kepler Repository

The main Kepler repository defines:

- instruments;
- protocols;
- documentation;
- software;
- educational materials.

The future **`kepler-data`** repository will contain the scientific record itself:

- submitted surveys;
- canonical observation tables;
- metadata;
- derived datasets.

Keeping these responsibilities separate allows the data archive to evolve independently while remaining reproducible against the methodologies defined in the Kepler project.
