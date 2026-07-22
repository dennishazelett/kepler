# Kepler

**Learning science by doing science.**

Kepler is an open educational and research project that uses naked-eye astronomy to teach scientific measurement, statistical inference, machine learning, and reproducible research.

Participants build simple astronomical instruments from inexpensive materials, make observations of the night sky, and contribute those observations to a growing shared dataset. Those measurements become the foundation for exploring a wide range of inferential methods, from descriptive statistics to Bayesian hierarchical models and modern machine learning.

The project is inspired by the work of Tycho Brahe and Johannes Kepler, but its purpose is not historical reenactment. Instead, it recreates one of the central challenges of science:

> **How can we infer the hidden structure of the world from imperfect observations?**

------------------------------------------------------------------------

# Why Kepler?

Modern science education often presents scientific knowledge as a collection of established facts. Kepler approaches science differently.

Participants experience science as a process:

- building instruments,
- making measurements,
- characterizing uncertainty,
- combining evidence,
- comparing competing models,
- refining explanations.

The project emphasizes that uncertainty is not a flaw in science—it is the raw material from which scientific understanding is built.

------------------------------------------------------------------------

# Project Philosophy

Every observation begins with the real world and ends with an inference.

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
```

Every component of this repository exists to support one or more stages of that process.

For a complete discussion of the conceptual framework, see:

- [`docs/measurement-model.md`](docs/measurement-model.md)

------------------------------------------------------------------------

# What Makes Kepler Different?

Many astronomy projects teach astronomy.

Many statistics courses analyze existing datasets.

Many machine learning courses begin with data that have already been cleaned and curated.

Kepler begins much earlier.

Participants create the data themselves.

The project treats the entire measurement process as an object of study. Instruments differ. Observers differ. Conditions differ. Those differences are not problems to eliminate—they are information to model.

This makes the project a natural environment for studying:

- measurement error
- uncertainty quantification
- hierarchical models
- simulation
- causal reasoning
- model comparison
- reproducible scientific workflows

------------------------------------------------------------------------

# Project Goals

Kepler has four complementary goals.

## 1. Teach Scientific Measurement

Participants learn how observations are produced, calibrated, and evaluated.

## 2. Build an Open Astronomical Dataset

Observations collected across multiple course offerings contribute to a growing longitudinal dataset suitable for research and education.

## 3. Compare Inferential Methods

The repository is designed to support multiple approaches to inference, including:

- descriptive statistics
- regression
- mixed-effects models
- Bayesian inference
- state-space models
- Gaussian processes
- supervised learning
- unsupervised learning
- deep learning

No single framework is considered the "correct" approach.

## 4. Promote Reproducible Research

All aspects of the project—including instrument designs, observation protocols, data schemas, simulations, analyses, and software—are version controlled and openly documented.

------------------------------------------------------------------------

# Repository Organization

The repository is organized around the measurement process rather than around a particular software language or statistical framework.

| Directory | Purpose |
|----|----|
| [`docs/`](docs/) | Project vision and conceptual documentation |
| [`instruments/`](instruments/) | Instrument designs, build guides, and calibration procedures |
| [`protocols/`](protocols/) | Standardized observation and quality-control procedures |
| [`schemas/`](schemas/) | Data definitions and validation schemas |
| [`data/`](data/) | Example, synthetic, and processed datasets |
| [`simulation/`](simulation/) | Synthetic data generation and measurement-process simulation |
| [`src/`](src/) | Core software utilities |
| [`inference/`](inference/) | Statistical and machine learning methods |
| [`analysis/`](analysis/) | Reproducible analyses and reports |
| [`course/`](course/) | Educational materials |
| [`tests/`](tests/) | Validation and reproducibility tests |

------------------------------------------------------------------------

# Current Status

Kepler is in active early development.

The current focus is establishing:

- project architecture,
- measurement protocols,
- instrument designs,
- data standards,
- simulation framework,
- reproducible software infrastructure.

Development priorities and longer-term milestones are maintained in:

- [`docs/roadmap.md`](docs/roadmap.md)

------------------------------------------------------------------------

# Getting Started

If you are new to the project, the recommended reading order is:

1.  [`docs/project-charter.md`](docs/project-charter.md)
2.  [`docs/measurement-model.md`](docs/measurement-model.md)
3.  [`docs/scientific-questions.md`](docs/scientific-questions.md)
4.  [`docs/pedagogical-goals.md`](docs/pedagogical-goals.md)

These documents describe the motivation, conceptual framework, and long-term direction of the project.

------------------------------------------------------------------------

# Contributing

Contributions are welcome.

The project benefits from expertise in astronomy, statistics, machine learning, software engineering, education, history of science, instrument design, and scientific visualization.

Please read:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

before submitting changes.

------------------------------------------------------------------------

# Citation

If you use Kepler in research or teaching, please cite the project using the metadata provided in:

- [`CITATION.cff`](CITATION.cff)

------------------------------------------------------------------------

# License

This project is released under the terms described in:

- [`LICENSE`](LICENSE)

------------------------------------------------------------------------

# Acknowledgments

Kepler draws inspiration from centuries of observational astronomy, particularly the work of Tycho Brahe and Johannes Kepler, whose commitment to careful measurement transformed our understanding of the Solar System.

Their work reminds us that scientific revolutions begin not with certainty, but with observations that are just accurate enough to reveal that our current explanations are incomplete.
