# Kepler

**Learning science by doing science.**

Kepler is an open educational and research project that uses naked-eye astronomy to teach scientific measurement and the computational sciences—from statistical inference to modern machine learning and artificial intelligence—through reproducible observational research.

Participants build simple astronomical instruments from inexpensive materials, make observations of the night sky, and contribute those observations to a growing shared dataset. Those measurements become the foundation for exploring a wide range of inferential methods while developing the practices of reproducible scientific investigation.

The project culminates not simply in models or predictions, but in scientific explanation. Participants evaluate competing hypotheses, communicate evidence, and produce scientific writing that justifies their conclusions. Many investigations invite participants to reexamine historical astronomical claims using modern standards of evidence, drawing their own conclusions from observations rather than reproducing established narratives.

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
      ↓
Scientific Communication
```

Scientific understanding is not complete until it can be communicated, scrutinized, and reproduced by others.

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
|------------------------------------|------------------------------------|
| [`docs/`](docs/) | Project vision and conceptual documentation |
| [`instruments/`](instruments/) | Instrument designs, build guides, and calibration procedures |
| [`protocols/`](protocols/) | Standardized observation and quality-control procedures |
| [`data/`](data/) | Data contract, schemas, example surveys, and validation tooling |
| [`simulation/`](simulation/) | Synthetic data generation and measurement-process simulation |
| [`src/`](src/) | Core software utilities |
| [`inference/`](inference/) | Statistical and machine learning methods |
| [`analysis/`](analysis/) | Reproducible analyses and reports |
| [`course/`](course/) | Educational materials |
| [`tests/`](tests/) | Validation and reproducibility tests |

------------------------------------------------------------------------

# Current Status

Kepler is in active early development.

The repository already includes:

- a complete cross-staff instrument design and build guide,
- a validated calibration survey,
- an initial data specification and JSON schemas,
- survey validation tools,
- contributor documentation.

The project will continue to evolve as additional instruments, observation protocols, datasets, simulations, and educational materials are developed.

The repository already contains a complete reference implementation of the initial data contract, including a validated cross-staff calibration survey.

Development priorities and longer-term milestones are still being defined.

------------------------------------------------------------------------

# Getting Started

If you are new to the project, the recommended reading order is:

1.  [`docs/project-charter.md`](docs/project-charter.md)
2.  [`docs/measurement-model.md`](docs/measurement-model.md)
3.  [`docs/celestial-coordinate-systems.md`](docs/celestial-coordinate-systems.md)
4.  [`instruments/cross-staff/README.md`](instruments/cross-staff/README.md)

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

If you use Kepler in research or teaching, please cite the Git repository.

A formal `CITATION.cff` file and versioned citation guidance will be added before the first public release.

------------------------------------------------------------------------

# License

Kepler is released under the terms of the MIT License.

See [\`LICENSE\`](LICENSE) for the full license text.

------------------------------------------------------------------------

# Acknowledgments

Kepler draws inspiration from centuries of observational astronomy, particularly the work of Tycho Brahe and Johannes Kepler, whose commitment to careful measurement transformed our understanding of the Solar System.

Their work reminds us that scientific revolutions begin not with certainty, but with observations that are just accurate enough to reveal that our current explanations are incomplete.
