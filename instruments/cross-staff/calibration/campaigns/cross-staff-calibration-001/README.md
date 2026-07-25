# Cross-Staff Calibration Campaign 001 Analysis

This directory contains the reproducible analysis of the first Kepler cross-staff calibration survey.

The purpose of this analysis is to characterize the performance of the reference cross-staff, evaluate its calibration data, and provide a baseline against which future instruments and calibration campaigns can be compared.

The canonical survey package remains:

```
data/examples/SUR-CAL-2026-001/
```

All analyses contained here are derived from that survey package. They do not modify or replace the canonical observations.

---

# Objectives

This project seeks to:

- characterize the repeatability of cross-staff measurements,
- estimate measurement uncertainty,
- investigate systematic bias,
- evaluate calibration performance,
- provide quantitative summaries of the calibration campaign,
- establish a reproducible workflow for future calibration analyses.

---

# Philosophy

Kepler distinguishes between **observations** and **analysis**.

Observations are preserved exactly as they were recorded.

Analysis derives additional quantities, statistical summaries, visualizations, models, and interpretations from those observations.

Only the raw observations belong in the canonical survey package.

---

# Repository Organization

Conceptual documents for this project are stored here.

Generated analysis artifacts are organized within this campaign directory, with notebooks under `notebooks/` and derived tables under `tables/`.

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Reproducible analysis scripts |
| `figures/` | Generated figures |
| `tables/` | Derived tables |
| `reports/` | Written reports |
| `notebooks/` | Exploratory notebooks |
---

# Planned Analyses

The initial investigation is expected to include:

1. exploratory visualization
2. descriptive statistics
3. repeatability analysis
4. calibration model development
5. residual analysis
6. uncertainty estimation

Additional analyses may be added as the project evolves.

---

# Reproducibility

Every figure, table, and result produced by this project should be reproducible from the canonical survey package using version-controlled analysis code.

Manual editing of derived results should be avoided.

Whenever possible, analysis products should be regenerated automatically from the raw observations.