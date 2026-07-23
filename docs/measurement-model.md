# Measurement Model

## Purpose

The Kepler project is built around a single idea:

> Scientific knowledge is obtained by making imperfect measurements of the physical world and reasoning carefully about the uncertainty in those measurements.

The project uses naked-eye astronomy as a concrete, historically authentic setting in which participants build simple instruments, collect observations, and use statistical and machine learning methods to infer underlying physical processes. The emphasis is not on reproducing professional astronomy, but on understanding how evidence is generated, evaluated, and accumulated.

This document defines the conceptual measurement model that underlies every component of the project. Instrument design, observation protocols, data schemas, simulation, statistical inference, machine learning, and course materials should all remain consistent with this model.

------------------------------------------------------------------------

# The Measurement Process

The project views every observation as one realization of the following causal process:

``` text
Solar System
      ↓
Observable Sky
      ↓
Instrument
      ↓
Observer
      ↓
Measurement
      ↓
Dataset
      ↓
Inference
      ↓
Scientific Understanding
      ↓
Scientific Communication
```

Each stage introduces information while potentially introducing uncertainty, bias, or error.

The purpose of the project is not to eliminate these imperfections, but to characterize and reason about them.

------------------------------------------------------------------------

# Stage 1 — Solar System

The physical state of the Solar System exists independently of the observer.

Examples include:

- planetary positions
- planetary velocities
- Earth's rotation
- Earth's orbital position
- lunar position
- stellar reference frame

These quantities are treated as latent variables. Participants never observe them directly.

------------------------------------------------------------------------

# Stage 2 — Observable Sky

The physical state produces an apparent sky as viewed from a specific location and time.

This stage includes effects such as:

- observer latitude and longitude
- date and time
- Earth's rotation
- atmospheric refraction
- horizon obstruction
- visibility conditions

The observable sky is the interface between celestial mechanics and measurement.

------------------------------------------------------------------------

# Stage 3 — Instrument

The instrument transforms the observable sky into measurable quantities.

Initially the project focuses on simple, participant-built instruments such as:

- cross-staffs
- quadrants

Each instrument has measurable properties including:

- design revision
- construction materials
- dimensions
- calibration history
- estimated precision

The instrument is considered part of the measurement process rather than merely a passive tool.

------------------------------------------------------------------------

# Stage 4 — Observer

Observers use instruments to produce measurements.

Observers contribute their own characteristics, including:

- experience
- calibration skill
- consistency
- recording accuracy
- decision making

Different observers are expected to produce systematically different measurements under identical conditions.

This variability is a feature of the project rather than a defect.

------------------------------------------------------------------------

# Stage 5 — Measurement

Measurements are the primary observations recorded by the project.

Examples include:

- angular separations
- altitudes
- azimuths
- timestamps
- calibration measurements

Every measurement is accompanied by metadata describing the circumstances under which it was obtained.

Measurements are immutable records.

Corrections, calibrations, or quality assessments should be stored separately rather than replacing original observations.

------------------------------------------------------------------------

# Stage 6 — Dataset

Individual measurements become useful only after aggregation.

The project dataset consists of:

- observations
- observers
- instruments
- sites
- calibration records
- course runs
- environmental information

The dataset therefore represents both astronomical observations and the complete measurement process that produced them.

------------------------------------------------------------------------

# Stage 7 — Inference

Inference attempts to recover latent quantities from observed measurements.

Multiple approaches are intentionally supported.

Examples include:

- descriptive statistics
- regression models
- hierarchical Bayesian models
- state-space models
- Gaussian processes
- supervised machine learning
- unsupervised learning
- anomaly detection
- deep learning

No inference method is considered privileged within the project architecture.

Inference methods should be viewed as competing explanations for the same observations.

------------------------------------------------------------------------

# Stage 8 — Scientific Understanding

Scientific understanding emerges from comparing models against observations.

Participants should experience science as an iterative process of:

1.  proposing explanations,
2.  collecting evidence,
3.  refining models,
4.  evaluating uncertainty,
5.  improving predictions.

The project therefore emphasizes scientific reasoning over obtaining correct answers.

------------------------------------------------------------------------

# Stage 9 — Scientific Communication

Scientific understanding becomes durable only when it can be communicated.

Participants are encouraged to communicate not only their conclusions, but also the observations, assumptions, methods, uncertainties, and reasoning that produced them.

Communication allows investigations to be examined, reproduced, criticized, refined, and extended by others.

Scientific arguments therefore become part of the measurement process rather than merely a final report.

------------------------------------------------------------------------

# Simulation

Simulation occupies a unique role within the project.

A simulator begins with known latent quantities and generates synthetic observations by modeling each stage of the measurement process.

This allows inference methods to be evaluated under controlled conditions where the underlying truth is known.

Simulation supports:

- software development
- model validation
- educational exercises
- benchmarking
- model recovery studies

The simulation architecture should mirror the real measurement process as closely as practical.

------------------------------------------------------------------------

# Design Principles

The project follows several guiding principles.

## Measure first

Observations should always precede inference.

Models are built to explain measurements rather than generate them.

## Preserve provenance

Raw observations should never be overwritten.

Derived quantities should remain reproducible from original measurements.

Shared community standards exist to make independently collected observations interoperable while preserving the provenance of every measurement.

## Model uncertainty

Uncertainty is an essential property of scientific measurement.

The objective is to understand uncertainty rather than eliminate it.

## Support multiple inferential frameworks

The repository should encourage comparison among statistical and machine learning methods.

Architectural decisions should avoid privileging any single implementation or software ecosystem.

## Build from simple components

The project should begin with simple instruments, simple observations, and simple analyses before introducing additional complexity.

------------------------------------------------------------------------

# Scope

The Kepler project is not intended to reproduce professional astrometry or compete with modern astronomical surveys.

Its purpose is to create a rich, authentic measurement environment in which participants can learn:

- observational science,
- measurement theory,
- uncertainty quantification,
- statistical inference,
- machine learning,
- reproducible research,
- collaborative scientific practice.

Astronomy provides the setting.

Inference is the subject.

Scientific reasoning is the objective.
