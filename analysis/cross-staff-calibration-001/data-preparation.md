# Data Preparation

## Purpose

This document describes how the canonical survey package is transformed into analysis-ready datasets.

The objective is to preserve complete provenance from the original observations to every derived quantity used during analysis.

The canonical survey package remains unchanged.

------------------------------------------------------------------------

# Source Data

The analysis uses the validated survey package:

```         
data/examples/SUR-CAL-2026-001/
```

Specifically:

- `survey.json`
- `observations.csv`
- `notes.csv`

No values within these files are modified.

------------------------------------------------------------------------

# Philosophy

Kepler distinguishes between:

- observations,
- derived variables,
- analytical results.

Only observations belong in the canonical survey package.

All derived quantities are created during analysis.

------------------------------------------------------------------------

# Data Preparation Workflow

The preparation stage consists of:

1.  Load the canonical observations.
2.  Verify survey integrity.
3.  Import survey metadata.
4.  Construct derived analysis variables.
5.  Produce analysis-ready tables.

No preprocessing step should overwrite the original observations.

------------------------------------------------------------------------

# Derived Variables

Examples of variables that may be created include:

- calculated observation angle
- predicted calibration angle
- calibration residual
- repeated-measurement identifiers
- target grouping variables

Additional derived variables may be introduced as required by specific analyses.

------------------------------------------------------------------------

# Reproducibility

Every derived dataset should be generated automatically from the canonical survey package.

Generated tables should never become the authoritative source of information.

The complete preparation workflow should be executable using version-controlled analysis scripts.

------------------------------------------------------------------------

# Outputs

Prepared datasets should be written to:

```         
analysis/tables/cross-staff-calibration-001/
```

These tables are considered temporary analytical products and may be regenerated at any time.
