# Contributing to Kepler

Thank you for your interest in contributing to Kepler.

Kepler is an open educational and research project exploring scientific measurement, inference, and reproducible research through naked-eye astronomy. Contributions of many kinds are welcome.

## Guiding Principle

Contributions should advance the project's mission of improving scientific understanding through careful observation, transparent methodology, reproducible analysis, and open collaboration.

Please read the project charter before contributing.

------------------------------------------------------------------------

# Contributions

Examples of welcomed contributions include:

- observational surveys;
- instrument designs and improvements;
- calibration studies;
- software and tooling;
- data validation;
- statistical analyses;
- simulations;
- documentation;
- educational materials;
- bug reports;
- feature proposals.

Contributions from educators, students, citizen scientists, engineers, historians, statisticians, software developers, and researchers are equally valued.

------------------------------------------------------------------------

# Data Contributions

Observational data should be submitted as complete survey packages conforming to the published survey specification.

Before submitting a survey, contributors should:

1.  validate the survey package using the published validation tools;
2.  include all required metadata, observations, notes, and supporting attachments;
3.  ensure the survey passes validation without errors and that the validation log is included in the submission package.

At present, validated survey packages are contributed to the `data/` directory of this repository through the normal GitHub pull request workflow.

Each survey should be submitted as a complete package under:

``` text
data/surveys/<survey_id>/
```

For example:

``` text
data/surveys/SUR-2026-0002/
├── survey.json
├── observations.csv
├── notes.csv
├── attachments/
├── checksums.sha256
└── validation.log
```

Submitted surveys are reviewed for scientific integrity, reproducibility, and conformance to the Kepler data model before being merged.

The current `data/` directory serves as the incubator for the future **kepler-data** repository. As the project matures, accepted survey packages will migrate to that dedicated repository with minimal changes to the submission workflow.

------------------------------------------------------------------------

# Review Process

All submissions are reviewed before acceptance.

Review is intended to ensure:

- scientific integrity;
- reproducibility;
- consistency with project standards;
- compatibility with the evolving data model.

Review should be viewed as collaborative rather than gatekeeping.

------------------------------------------------------------------------

# Discussion

Questions, ideas, and proposals are encouraged.

If you are unsure whether an idea fits the project, please open a discussion or issue before investing substantial effort.

------------------------------------------------------------------------

# Code of Conduct

Participation in this project is governed by the Contributor Covenant Code of Conduct.

By participating, you agree to abide by its terms.
