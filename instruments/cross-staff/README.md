# Kepler Cross-staff

## Purpose

The Kepler Cross-staff is the primary angular measurement instrument used throughout the Kepler project.

Its purpose is not to recreate a historical artifact, but to provide an inexpensive, understandable, and scientifically useful instrument that allows participants to measure angular separations between objects in the sky.

These measurements become the raw observations upon which every subsequent scientific investigation is built.

The cross-staff is therefore one of the foundational instruments of the Kepler Observatory.

The current reference implementation (Prototype 0.2) uses a sliding cardboard sleeve, a fixed wooden crosspiece, and permanently mounted fiducials providing multiple measurement ranges. Future revisions may refine this implementation while preserving compatibility with the overall measurement model.

---

# Why a Cross-staff?

The cross-staff occupies a unique place in the history of astronomy.

Long before telescopes, astronomers measured the heavens by comparing angles between celestial objects.

Those measurements allowed astronomers such as Regiomontanus, Gemma Frisius, and Tycho Brahe to construct increasingly accurate maps of the sky and ultimately provided the observational foundation for Johannes Kepler's discovery of the laws of planetary motion.

A brief discussion of the historical cross-staff and the design philosophy of the Kepler implementation is provided in [Design Specification](design.md).

The Kepler project begins with the same fundamental activity:

**carefully measuring angles.**

---

# Scientific Role

The cross-staff does **not** measure:

* distances,
* planetary orbits,
* brightness,
* velocity,
* physical size.

Instead, it measures one thing exceptionally well:

> **The angular separation between two objects on the celestial sphere.**

This simple measurement becomes surprisingly powerful when combined with:

* repeated observations,
* accurate timestamps,
* known reference stars,
* observations contributed by many participants.

Every observation collected using the cross-staff contributes to a shared representation of the sky from which increasingly sophisticated scientific models can be developed.

---

# Design Philosophy

The Kepler Cross-staff is designed according to four principles.

## Accessibility

A participant anywhere in the world should be able to build or obtain a compatible instrument using inexpensive materials.

Scientific participation should not depend upon financial resources.

---

## Transparency

Every measurement should arise from geometry that the participant can understand.

The instrument should make measurement visible rather than hiding it behind electronics or automation.

---

## Reproducibility

Different participants using independently constructed instruments should be capable of producing measurements that are comparable after calibration.

The objective is not identical instruments but reproducible observations.

---

## Evolution

The Kepler Cross-staff is a living instrument.

Its design may evolve over time as participants discover improvements.

Every design revision should remain scientifically documented and reproducible.

Older instruments remain valuable contributors to the project.

---

# Functional Requirements

Every Kepler-compatible cross-staff should be capable of:

* measuring angular separation between two visible celestial objects;
* producing repeated measurements with documented uncertainty;
* supporting calibration against known angular separations;
* being uniquely identified by instrument ID;
* recording the instrument revision used to collect observations.

---

# Expected Performance

The objective of the Kepler Cross-staff is **not** maximum precision.

Instead, the instrument should produce measurements whose uncertainty is understood and documented.

Initial project goals are approximately:

* construction cost below USD $10;
* construction time less than one hour;
* typical repeatability on the order of one degree or better after calibration;
* operation without electricity or specialized equipment.

These values may evolve as the project develops.

---

# Relationship to Other Instruments

The cross-staff is one component of the Kepler Measurement System.

Together with the quadrant and gnomon it provides complementary information.

| Instrument  | Primary Measurement                          |
| ----------- | -------------------------------------------- |
| Cross-staff | Angular separation between celestial objects |
| Quadrant    | Altitude above the local horizon             |
| Gnomon      | Solar position and local reference geometry  |

Each instrument measures a different aspect of the observable sky.

Together they allow participants to locate celestial objects within a common observational framework.

---

# Measurement Before Theory

The cross-staff embodies one of the central ideas of the Kepler project.

Before scientists can explain the heavens, they must first describe them.

The instrument therefore precedes every scientific investigation.

Participants use the cross-staff to create observations.

Those observations become evidence.

Only then do investigations ask what conclusions are justified.

---

# Repository Structure

This directory contains the complete specification for the Kepler Cross-staff.

* **`design.md`** — engineering design and measurement geometry
* **`build-guide.md`** — step-by-step construction instructions
* **`calibration.md`** — calibration procedures and uncertainty estimation

Together these documents define the current reference implementation of the instrument.

---

# Versioning

The Kepler Cross-staff should be treated as scientific infrastructure.

Design revisions are expected.

Each revision should improve one or more aspects of the instrument while preserving compatibility with previous observations whenever practical.

Observations should always record the instrument revision used to obtain them.

---

# Looking Ahead

The first task performed with a Kepler Cross-staff is deceptively simple:

Measure the angle between two objects in the sky.

Everything that follows—from celestial maps, to planetary motion, to competing cosmological models, to Bayesian inference and machine learning—begins with that single act of careful measurement.

The cross-staff is therefore not simply a measuring device.

It is the participant's first contribution to a shared scientific enterprise.
