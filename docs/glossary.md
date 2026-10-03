# Kepler Glossary

## Purpose

This glossary defines terms used with specific meanings in Kepler.

It is a reference for participants, educators, contributors, translators, and
maintainers. It supports consistent interpretation across the project’s
scientific, educational, data, and software documentation.

This glossary does not replace the project charter, measurement model, data
specifications, protocols, instrument guides, or investigations. Those
documents remain the authoritative sources for the project’s principles,
methods, requirements, and procedures.

## How to use this glossary

Entries define how a term should be understood when it appears in Kepler
documentation.

Where a term has a broader disciplinary or everyday meaning, the definition
below identifies its intended Kepler meaning. Related documents provide fuller
explanations, methods, and technical detail.

---

## Analysis

In Kepler, analysis is reproducible work that examines observations or other
documented inputs to produce descriptive, comparative, inferential, or
predictive results.

Analysis may include calculation, visualization, statistical modeling, machine
learning, simulation, or qualitative interpretation. Its outputs are derived
from documented inputs and should remain distinguishable from the original
observations.

See also: [Derived quantity](#derived-quantity),
[Inference](#inference), [Model](#model).

## Calibration

In Kepler, calibration is the empirical characterization of how an
observer--instrument measurement system behaves under known or otherwise
well-characterized conditions.

Calibration does not erase or replace original observations. It produces
information that may help interpret measurements, characterize uncertainty, or
support later analysis.

See also: [Instrument](#instrument), [Measurement](#measurement),
[Observer](#observer), [Uncertainty](#uncertainty).

## Dataset

In Kepler, a dataset is a structured collection of observations and associated
records that supports reuse, comparison, analysis, and scientific inquiry.

A Kepler dataset represents both observations of the sky and information about
the measurement process that produced them, including relevant observers,
instruments, protocols, surveys, and metadata.

See also: [Metadata](#metadata), [Observation](#observation),
[Provenance](#provenance), [Survey](#survey).

## Derived quantity

In Kepler, a derived quantity is a value produced from one or more observations
through calculation, transformation, calibration, simulation, modeling, or
inference.

Derived quantities may be scientifically valuable, but they do not replace the
observations from which they were produced. Coordinates, residuals, predictions,
and fitted parameters are examples of derived quantities.

See also: [Analysis](#analysis), [Inference](#inference),
[Observation](#observation).

## Inference

In Kepler, inference is the process of using observations and explicit
assumptions to constrain, compare, or estimate unknown states, explanations,
relationships, or claims.

Kepler treats individual measurements as constraints on possible explanations,
not as direct and complete access to the physical world. Multiple inferential
methods may be used to examine the same observations.

See also: [Latent state](#latent-state), [Model](#model),
[Observation](#observation), [Uncertainty](#uncertainty).

## Instrument

In Kepler, an instrument is a physical system used to transform features of the
observable sky into quantities that can be measured and recorded.

An instrument is part of the measurement process. Its design, construction,
configuration, calibration history, and limitations can affect the observations
it helps produce.

See also: [Calibration](#calibration), [Measurement](#measurement),
[Measurement process](#measurement-process).

## Latent state

In Kepler, the latent state is the underlying physical state of the world that
exists independently of an observer but cannot be observed directly in full.

Examples include the positions and motions of celestial objects. Observations
provide constraints on the latent state; inference combines those constraints
with explicit assumptions to develop and evaluate explanations.

See also: [Inference](#inference), [Observable sky](#observable-sky),
[Observation](#observation).

## Measurement

In Kepler, a measurement is the act or result of determining a quantity from
the observable sky, ordinarily by an observer using an instrument under
particular conditions.

A measurement may be imperfect, but its imperfections are part of the
scientific information that Kepler seeks to characterize rather than conceal.
When preserved with the context needed to interpret how it was produced, a
measurement becomes an observation.

See also: [Observation](#observation), [Observer](#observer),
[Uncertainty](#uncertainty).

## Measurement process

In Kepler, the measurement process is the complete causal pathway through which
a physical state becomes a recorded observation and, later, a possible basis for
inference.

It includes the physical world, the observable sky, the instrument, the
observer, the act of measurement, and the contextual information required to
interpret the resulting record.

See also: [Instrument](#instrument), [Metadata](#metadata),
[Observation](#observation), [Observable sky](#observable-sky).

## Metadata

In Kepler, metadata is information that describes the context, origin,
structure, or interpretation of an observation, survey, dataset, or derived
result.

Metadata may include observation time, location, observer, instrument,
protocol, units, calibration context, schema version, and other information
needed to interpret, compare, reproduce, or reuse scientific records.

See also: [Observation](#observation), [Protocol](#protocol),
[Provenance](#provenance), [Survey](#survey).

## Model

In Kepler, a model is an explicit representation of assumptions about a system,
measurement process, or relationship that can be used to reason from evidence.

Models connect observations, hypotheses, explanations, and predictions. They
are tools for thinking and comparison, rather than direct equivalents of
reality or final repositories of truth.

See also: [Inference](#inference), [Latent state](#latent-state),
[Uncertainty](#uncertainty).

## Observable sky

In Kepler, the observable sky is the apparent sky available to an observer at a
particular location and time under particular viewing conditions.

It connects the physical state of the Solar System to the measurements a
participant can make. It is shaped by factors including location, time, Earth’s
rotation, atmospheric effects, horizon obstruction, and visibility conditions.

See also: [Latent state](#latent-state), [Measurement process](#measurement-process),
[Observation](#observation).

## Observation

In Kepler, an observation is an immutable primary record of an act or result of
measurement, preserved with the context needed to interpret how it was
produced.

An observation preserves what was recorded, together with the information
needed to interpret how it was produced. It is not a conclusion, corrected
value, coordinate estimate, prediction, fitted parameter, or other derived
result.

See also: [Derived quantity](#derived-quantity), [Measurement](#measurement),
[Metadata](#metadata), [Provenance](#provenance).

## Observer

In Kepler, an observer is a person who participates in the measurement process
by using an instrument, making judgments, recording observations, or otherwise
contributing directly to the generation of scientific evidence.

Observer experience, technique, consistency, and decisions may influence
measurement. Kepler treats this variability as part of the measurement process
to document and study, rather than as information to discard.

See also: [Instrument](#instrument), [Measurement](#measurement),
[Measurement process](#measurement-process).

## Protocol

In Kepler, a protocol is a documented and repeatable procedure for carrying out
a defined part of scientific work, especially observation, measurement,
calibration, recording, or validation.

Protocols make independently collected observations more interpretable and
interoperable. They standardize aspects of evidence collection, but do not
prescribe a single scientific question, analysis, or conclusion.

See also: [Metadata](#metadata), [Survey](#survey),
[Validation](#validation).

## Provenance

In Kepler, provenance is the documented history and traceable relationships
that connect a scientific record or result to the observations, observers,
instruments, protocols, surveys, transformations, and analyses from which it
arose.

Provenance allows others to examine how a result was produced, reproduce
documented steps, assess limitations, and distinguish primary observations from
derived products.

See also: [Metadata](#metadata), [Observation](#observation),
[Reproducibility](#reproducibility).

## Reproducibility

In Kepler, reproducibility is the capacity for another person to inspect,
understand, and repeat a documented scientific workflow using its recorded
observations, metadata, methods, assumptions, and computational materials.

Reproducibility does not require identical observations under changed
conditions or guarantee identical conclusions. It requires sufficient
documentation and provenance to evaluate how evidence was transformed into a
result.

See also: [Analysis](#analysis), [Metadata](#metadata),
[Provenance](#provenance).

## Survey

In Kepler, a survey is the primary unit of scientific contribution: a coherent
collection of observations assembled to address a shared scientific purpose
within