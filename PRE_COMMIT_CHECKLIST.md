# Kepler Pre-Commit Checklist

This checklist governs all commits to the Kepler repository.

The checklist is organized in layers. Complete only the sections appropriate to the scope of the commit.

---

# Layer 1 — Required for Every Commit

Complete this section for **every** commit.

## Scope

- [ ] The commit has a single coherent purpose.
- [ ] Unrelated changes have been excluded or split into separate commits.

## Repository Hygiene

- [ ] `git status` contains only intended changes.
- [ ] No obsolete or duplicate artifacts remain.
- [ ] No temporary or debugging files are included.

## Documentation

- [ ] Documentation affected by the change has been updated.
- [ ] Internal links remain valid.
- [ ] Repository entry points remain discoverable (major relocations preserve clear README-based entry points for users and contributors).

## Validation

- [ ] Appropriate tests, validation, or manual checks have been performed.
- [ ] The change does not knowingly break existing functionality.

## Commit Metadata

- [ ] The commit message accurately summarizes the change.
- [ ] LLM provenance has been updated where required.

---

# Layer 2 — Architectural Changes

Complete this section only if the commit changes repository architecture, shared components, or project organization.

## Repository Architecture

- [ ] Shared and project-specific responsibilities remain clearly separated.
- [ ] No redundant or competing architectural patterns have been introduced.
- [ ] Entry-point documentation reflects the updated architecture.

## Cross-Repository Consistency

- [ ] Directory organization remains internally consistent.
- [ ] Shared utilities remain reusable across investigations.
- [ ] Existing investigations continue to integrate cleanly with shared infrastructure.

---

# Layer 3 — Specialized Reviews

Complete only the subsection(s) relevant to the commit.

## Scientific Methodology

- [ ] Scientific terminology remains internally consistent.
- [ ] Methodological changes are documented.
- [ ] Existing conceptual documents remain coherent.

## Data and Schema

- [ ] Data contracts remain internally consistent.
- [ ] Schema changes are versioned appropriately.
- [ ] Backward compatibility has been considered where applicable.

## Instruments and Protocols

- [ ] Calibration documentation is updated.
- [ ] Observation protocols remain consistent with the measurement model.
- [ ] Instrument documentation reflects implementation changes.

## Investigations

- [ ] Investigation documents remain participant-facing.
- [ ] Shared concepts have not been duplicated into investigations.
- [ ] Knowledge documents and project guidance remain synchronized.

## Release or Data Freeze

- [ ] Version identifiers have been updated.
- [ ] Freeze or release documentation is complete.
- [ ] Reproducibility has been verified.

---

# Final Review

Before committing, confirm:

- [ ] This commit improves the repository without introducing unnecessary complexity.
- [ ] The repository remains more internally consistent than before the change.
- [ ] The commit history accurately reflects the evolution of the project.