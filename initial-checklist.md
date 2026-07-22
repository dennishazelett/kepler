# Initial Repository State Checklist

Use this temporary checklist to track the initial creation of files for the Kepler repository.

## Repository identity

- [x] `README.md`
- [x] `LICENSE`
- [x] `CONTRIBUTING.md`
- [x] `CODE_OF_CONDUCT.md`
- [ ] `CHANGELOG.md`
- [x] `.gitignore`
- [ ] `.editorconfig`
- [ ] `.pre-commit-config.yaml`
- [ ] `CITATION.cff`

## `docs/`

 - [x] `docs/project-charter.md`
 - [x] `docs/scientific-program.md`
 - [ ] `docs/pedagogical-goals.md`
 - [x] `docs/measurement-model.md`
 - [x] `docs/celestial-coordinate-systems.md`
 - [ ] `docs/roadmap.md`
 - [x] `docs/glossary.md`

## `instruments/`

- [ ] `instruments/README.md`

### `instruments/cross-staff/`

- [x] `instruments/cross-staff/README.md`
- [x] `instruments/cross-staff/design.md`
- [x] `instruments/cross-staff/build-guide.md`
- [ ] `instruments/cross-staff/calibration.md`

### `instruments/quadrant/`

- [ ] `instruments/quadrant/README.md`
- [ ] `instruments/quadrant/design.md`
- [ ] `instruments/quadrant/build-guide.md`
- [ ] `instruments/quadrant/calibration.md`
- [ ] `instruments/quadrant/bill-of-materials.md`

### `instruments/reference-instruments/`

- [ ] `instruments/reference-instruments/README.md`

## `protocols/`

- [ ] `protocols/README.md`
- [ ] `protocols/observation.md`
- [ ] `protocols/calibration.md`
- [ ] `protocols/observer-onboarding.md`
- [ ] `protocols/instrument-registration.md`
- [ ] `protocols/quality-control.md`
- [ ] `protocols/safety.md`
- [ ] `protocols/data-submission.md`

## `data/schemas/`

- [x] `schemas/README.md`
- [ ] `schemas/observation.schema.json`
- [ ] `schemas/observer.schema.json`
- [ ] `schemas/instrument.schema.json`
- [ ] `schemas/calibration.schema.json`
- [ ] `schemas/site.schema.json`
- [ ] `schemas/course-run.schema.json`
- [ ] `schemas/data-dictionary.md`
- [ ] `schemas/submission.schema.json`
- [ ] `schemas/data-dictionary.md`

## data/

- [x] data/README.md
- [x] data/data-philosophy.md
- [x] data/survey-specification.md
- [x] data/identifier-specification.md

### data/build-data/

- [x] validate-survey.py
- [x] build-survey-archive.md

### data/examples/

- [x] SUR-CAL-2026-001/

## `simulation/`

- [ ] `simulation/README.md`
- [ ] `simulation/celestial-process/README.md`
- [ ] `simulation/observation-geometry/README.md`
- [ ] `simulation/instruments/README.md`
- [ ] `simulation/observers/README.md`
- [ ] `simulation/environment/README.md`
- [ ] `simulation/missingness/README.md`
- [ ] `simulation/generate-synthetic-data/README.md`

## `src/`

- [ ] `src/kepler/__init__.py`
- [ ] `src/kepler/config.py`

## `inference/`

- [ ] `inference/README.md`
- [ ] `inference/baselines/README.md`
- [ ] `inference/probabilistic/README.md`
- [ ] `inference/supervised/README.md`
- [ ] `inference/unsupervised/README.md`
- [ ] `inference/sequential/README.md`
- [ ] `inference/causal/README.md`
- [ ] `inference/neural/README.md`

## `experiments/`

- [ ] `experiments/README.md`
- [ ] `experiments/configs/README.md`
- [ ] `experiments/runs/README.md`
- [ ] `experiments/benchmarks.md`

## `analysis/`

- [ ] `analysis/README.md`
- [ ] `analysis/analysis-style-guide.md`

## `course/`

- [ ] `course/README.md`
- [ ] `course/syllabus.md`
- [ ] `course/curriculum-map.md`

### `course/training/`

- [ ] `course/training/README.md`

#### `course/training/01-describing-the-sky/`

- [ ] `README.md`

#### `course/training/02-measuring-the-sky/`

- [ ] `README.md`

#### `course/training/03-mapping-the-sky/`

- [ ] `README.md`

#### `course/training/04-the-moving-sky/`

- [ ] `README.md`

#### `course/training/05-contributing-observations/`

- [ ] `README.md`

### `course/investigations/`

- [ ] `course/investigations/README.md`

#### `course/investigations/01-earth-centered-cosmos/`

- [ ] `README.md`

#### `course/investigations/02-perfect-heavens/`

- [ ] `README.md`

## `apps/`

- [ ] `apps/README.md`

## `tests/`

- [ ] `tests/README.md`

## `workflows/`

- [ ] `workflows/README.md`

## `.github/`

- [ ] `.github/ISSUE_TEMPLATE/bug_report.yml`
- [ ] `.github/ISSUE_TEMPLATE/feature_request.yml`
- [ ] `.github/ISSUE_TEMPLATE/protocol_revision.yml`
- [ ] `.github/ISSUE_TEMPLATE/instrument_revision.yml`
- [ ] `.github/ISSUE_TEMPLATE/model_proposal.yml`

## `references/`

- [ ] `references/README.md`
- [ ] `references/bibliography.bib`

## `assets/`

- [ ] `assets/README.md`

## `decisions/`

 - [ ] `decisions/README.md`
 - [ ] `decisions/0001-project-scope.md`
 - [ ] `decisions/0002-data-contract.md`
 - [ ] `decisions/0003-instrument-philosophy.md`
 - [ ] `decisions/0004-multiple-learning-paths.md`
 
## Validator improvements

- Summarize repeated errors instead of listing every occurrence.
- Produce a portable validation.log (no absolute paths).
- Optionally omit timestamps or provide a `--timestamp` flag.
- Print schema versions used during validation.
- Add PASS summary by component (survey, observations, notes, attachments).
- Return distinct exit codes for schema vs. package errors.