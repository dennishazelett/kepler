# Survey Specification (Draft 0.3)

## Purpose

A survey is the primary unit of scientific contribution to Kepler.

A survey represents a coherent collection of observations acquired to answer a specific scientific question under a shared observational context.

The survey, rather than the individual observation, is the object submitted to the Kepler data repository.

A survey consists of metadata, raw observations, optional notes, and optional supporting materials.

---

# Design Principles

A survey is designed to answer a scientific question.

The survey determines:

* the purpose of the observations;
* the required contextual metadata;
* the observation specification;
* the expected downstream analyses.

The canonical dataset records what was measured, not what was inferred.

Derived quantities (angles, celestial coordinates, residuals, predictions, fitted model parameters, etc.) are products of analysis and are not part of the canonical raw observational record.

---

# Survey Structure

Every survey consists of four conceptual components.

## 1. Survey Metadata

Survey metadata describes the shared context for every observation within the survey.

Examples include:

* survey identifier
* survey type
* scientific question
* observer(s)
* instrument instance(s)
* protocol version
* observing site
* submission date
* schema version

Metadata common to every observation should appear here rather than being repeated in the observation table.

---

## 2. Raw Observations

The observation table contains the canonical scientific evidence.

Requirements:

* one observation per row;
* one header row;
* no embedded formulas;
* no derived quantities;
* instrument-native measurements only;
* stable column definitions;
* directly appendable to the canonical dataset without manual editing.

Each survey type defines the observation specification appropriate to its scientific objective.

---

## 3. Notes

Narrative observations that cannot be represented naturally within the canonical observation table.

Examples include:

* unexpected events;
* environmental conditions;
* mechanical issues;
* observer comments;
* deviations from protocol.

Notes should reference observations through stable observation identifiers whenever appropriate.

---

## 4. Attachments

Optional supporting materials.

Examples include:

* photographs;
* sketches;
* calibration targets;
* scanned notebooks;
* original working tables;
* supplementary documentation.

Attachments support interpretation but are not part of the canonical observation table.

---

# Observation

An observation is the atomic unit of scientific evidence.

Each observation represents one intentional act of measurement.

Each observation occupies exactly one row in the canonical observation table.

Observations remain instrument-specific.

Kepler preserves the quantities directly measured by each instrument rather than forcing premature translation into a universal measurement format.

---

# Survey Types

All surveys satisfy the same structural specification.

Different survey types answer different scientific questions and therefore collect different observational data.

Initial survey types include:

## Instrument Calibration Survey

Scientific question:

> Given a known reference, how does a particular observer–instrument measurement system behave?

These surveys characterize the performance of a specific measurement system under controlled conditions.

Typical observations may include:

* fiducial selection;
* instrument reading;
* reference target identifier;
* reference geometry.

Calibration surveys characterize the complete measurement system, including the observer, instrument instance, and protocol.

## Astronomical Observation Survey

Scientific question:

> What measurements of celestial objects were obtained under the specified observing conditions?

These surveys collect observations intended for astronomical inference.

The observation payload will differ from calibration surveys according to the instrument employed.

Future survey types may include:

* replication surveys;
* validation surveys;
* benchmark surveys;
* educational investigations;
* other scientifically motivated activities.

---

# Canonical Observation Tables

Each survey type defines its own observation specification.

However, every canonical observation table must satisfy the following requirements:

* identical column names for a given specification;
* identical column order;
* identical data types;
* canonical units and formats;
* no derived variables;
* no formatting dependencies;
* directly concatenable with every other accepted table conforming to the same specification.

Instrument-specific observation tables may differ from one another while remaining individually standardized.

## Units and Formats

Every observation specification must define the canonical representation of each field.

For fields representing physical quantities, the observation specification must declare one canonical unit. This requirement applies to all physical quantities, including instrument readings, calibration reference geometry, environmental conditions, and observational setup quantities.

Contributors may collect and retain working data in other units. Before validation and submission, all physical quantities in the canonical observation table must be converted to the units declared by the applicable observation specification.

Deterministic unit conversion is representational normalization, not scientific inference. Conversion must not introduce quantities that were not present in the source record.

The original working table may be retained as an attachment. When conversion is required, the survey package should preserve a conversion record identifying the source unit and canonical unit for each converted field.

Fields that do not represent physical quantities use the representation appropriate to their semantic class:

* temporal fields use the canonical date or date-time format declared by the specification;
* identifiers and categorical fields have no applicable unit;
* mathematically dimensionless numerical quantities use the unit `1`.

Temporal values should preserve the precision supported by the source record. A calendar date is valid when only the date is known or scientifically relevant; a date-time should be used when the time is known and required. Precision must not be invented during survey preparation.

---

# Validation

Every submitted survey should undergo automated validation before acceptance.

Validation includes:

* required metadata;
* observation specification;
* data types;
* canonical units and formats;
* identifier uniqueness;
* schema version;
* referential integrity where applicable.

A successful structural validation confirms that a submitted value is represented according to its specification. It cannot independently establish that a contributor converted a source measurement correctly. Survey preparation utilities and conversion records therefore form part of the submission workflow when noncanonical working units were used.

Accepted surveys become immutable components of the scientific record.

Corrections should be represented through new submissions or explicit revision records rather than silent modification of accepted observations.

---

# Status

This document describes the preliminary survey specification developed from the first cross-staff calibration survey.

The specification is expected to evolve as additional instruments, survey types, and observation protocols are incorporated into Kepler.
