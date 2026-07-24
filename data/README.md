# Data

This directory contains the emerging data architecture for Kepler.

Its purpose is to define how observations are represented, validated, archived, and ultimately combined into a shared scientific dataset.

During early development, this directory serves as a staging area for the future **`kepler-data`** repository. Once the data model and submission workflow have matured, this directory will be migrated into its own repository while remaining closely coupled to the main Kepler project.

## Organization

- [`data-philosophy.md`](data-philosophy.md) — Guiding principles governing the representation and stewardship of scientific data.
- [`survey-specification.md`](survey-specification.md) — The canonical specification describing the structure of a Kepler survey.
- [`examples/`](examples/) — Reference implementations of valid survey packages.
- [`surveys/`](surveys/) — Accepted community survey packages. During early development this directory serves as the canonical archive of contributed surveys and will eventually migrate unchanged into the dedicated **`kepler-data`** repository.
- [`build-data/`](build-data/) — Prompts, workflows, and utilities for constructing and validating survey archives.

## Design Principles

The Kepler data model is built around several core ideas:

- observations are the atomic units of scientific evidence;
- surveys are the primary units of contribution;
- raw observations are preserved exactly as measured;
- derived quantities are generated through analysis and stored separately;
- all accepted observation tables are standardized and directly appendable without manual preprocessing.

These principles are described in greater detail in the accompanying documentation.

## Survey Lifecycle

The canonical unit of contribution to the Kepler data archive is a **survey package**.

A typical survey follows the lifecycle below:

```text
Observation
      ↓
Survey Package
      ↓
Validation
      ↓
Pull Request
      ↓
Scientific Review
      ↓
Accepted Survey
      ↓
Community Dataset
```

Survey packages are submitted as complete, validated archives rather than as individual observations. This preserves scientific provenance, allows contributors to document their methodology, and ensures that every accepted survey remains independently reproducible.

During the development of the main Kepler repository, accepted survey packages are stored under:

```text
data/surveys/<survey_id>/
```

The submission workflow is designed so that this directory can later migrate directly into the standalone **`kepler-data`** repository without changing the contributor experience.

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
