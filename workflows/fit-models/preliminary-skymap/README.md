# Preliminary Skymap Workflow

This workflow produces a preliminary sky reconstruction from canonical Kepler
survey archives using nonlinear least squares.

It is an end-to-end analysis exercise for the Kepler ingest and analysis
framework:

```text
canonical survey archives
        ↓
AnalysisCollection assembly
        ↓
deterministic derived observations
        ↓
atomic observational constraints
        ↓
nonlinear least-squares fit
        ↓
preliminary north-polar skymap
```

## Scope

The workflow fits one right ascension and one declination for each target that
has a quadrant/compass initialization estimate. It uses three constraint types:

- quadrant nominal altitude;
- compass true azimuth; and
- cross-staff nominal geometric separation.

The fit is deliberately a baseline. It does not yet include:

- an instrument calibration model;
- atmospheric-refraction correction;
- uncertainty weights;
- observer or instrument bias parameters;
- hierarchical or Bayesian inference; or
- catalog-frame astrometry.

Coordinates should be interpreted as preliminary topocentric equatorial
coordinates of date, using UTC as a practical approximation to UT1.

## Inputs

Edit `survey_paths` in `preliminary-skymap.qmd` to list one or more canonical
survey archive directories.

Every input archive must validate as canonical through the Kepler ingest layer.
For a survey to contribute to a selected observation type, its observation
specification name, version, table layout, and element types must be compatible
with that workflow's selected analysis group.

The current baseline configuration is intended for:

```text
quadrant-observation@UNSPECIFIED
compass-observation@UNSPECIFIED
cross-staff-observation@0.3
```

Different observation-specification versions are not silently merged. Inspect
and reconcile version differences through the data-curation workflow before
adding version-specific support to this model.

## Requirements

The Kepler root Julia environment must contain:

- `Kepler`
- `Optim`
- `CairoMakie`
- `QuartoNotebookRunner` is managed by Quarto's normal Julia environment; it
  does not need to be added to Kepler's project environment.

The Kepler analysis module must provide:

- `assemble_analysis_data`
- `materialize_context`
- `derive_quadrant_nominal_altitude`
- `derive_compass_true_azimuth`
- `derive_cross_staff_nominal_separation`

## Render

From the repository root, run:

```bash
quarto render workflows/fit-models/preliminary-skymap/preliminary-skymap.qmd
```

Do not set `QUARTO_JULIA_PROJECT` for the normal render command. The document
activates the Kepler root environment inside its setup cell; Quarto starts its
own Julia execution runner before that cell executes.

For iterative work:

```bash
quarto preview workflows/fit-models/preliminary-skymap/preliminary-skymap.qmd
```

## Outputs

A successful render produces:

- survey and source-table metadata summaries;
- an inventory of derived observation constraints;
- nonlinear optimizer convergence and objective summaries;
- fitted target coordinates;
- residual summaries for quadrant, compass, and cross-staff constraints; and
- a preliminary north-polar skymap of the joint fitted coordinates.

The north-polar map displays the joint fit rather than pre-fit independent
quadrant/compass estimates.

## Reproducibility

The workflow reads canonical archives without modifying them. Derived values
are analysis-frame columns labeled with their deterministic transform, and
source-table/survey context is retained for each observation.

Record the exact survey paths, package manifest, rendered report, and source
revision whenever using the workflow for a scientific comparison.
