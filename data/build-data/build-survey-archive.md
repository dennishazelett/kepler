---
editor_options: 
  markdown: 
    wrap: 72
---

# Build Kepler Survey Archive

Using the attached files and the Kepler Survey Specification, construct
a complete Kepler survey package.

Archive construction interprets and structures the data; the
normalization utility converts representations.

Archive construction is a semantic reconstruction task rather than a
format conversion task. The objective is to preserve the scientific
meaning of the contributor's observations while expressing that meaning
using the structures required by the applicable observation
specifications.

## Inputs

The prompt will provide:

- Survey Specification (`survey-specification.md`)
- Observation Specification (if applicable)
- Source observational data (CSV, XLSX, etc.)
- Optional notes
- Optional photographs or other attachments
- Survey metadata supplied below

## 

## Mixed Source Tables

Contributor-supplied raw data may contain observations from multiple
instrument designs, instrument instances, observation types, or
observation specifications in a single table or text record.

Mixed source data are acceptable when the available headers, instrument
labels, registered instrument identifiers, units, notes, protocol
documentation, value patterns, or other contextual information are
sufficient to identify and separate the observations.

During archive construction, the archive builder should:

1.  interpret the semantic meaning of each source field using the
    complete observational context;

2.  distinguish instrument design from instrument instance. Use the
    documented instrument design to determine the applicable observation
    specification and observation table. When a registered instrument
    instance identifier is supplied, preserve it as the table's
    `instrument_instance_id` in `survey.json`;

3.  separate observations according to their applicable observation
    specification and instrument instance when appropriate;

4.  reconstruct one or more working observation tables using the
    canonical field names and column order defined by the applicable
    observation specification; these working tables may retain
    documented noncanonical representations (such as source units) until
    representational normalization is performed;

5.  generate one observation table for each observation specification
    represented in the survey; and

6.  list every generated observation table in
    `survey.json.observation_tables`.

Working representations are intermediate artifacts used during archive
preparation and need not themselves satisfy the canonical observation
schema. Only the submission-ready canonical observation tables are
expected to validate against the applicable observation specification.

The original mixed source file should be preserved unchanged as an
attachment when appropriate.

If the available evidence is insufficient to assign a row or field
confidently to an observation specification or instrument instance, the
archive builder must request clarification rather than silently infer or
discard the observation.

When a required interpretation cannot be established from the supplied
evidence, producing an incomplete archive with explicit placeholders is
preferred to silently inventing metadata or making unsupported semantic
assignments.

Mixed data types are permitted only in the contributor-supplied source
or intermediate working representation. Submission-ready canonical
observation tables must each conform to one applicable observation
specification.

Generate tables only for observation types actually evidenced by the
supplied source records. Schema branches, optional objects, or
alternative row forms must not be treated as separate represented
datasets unless the source contains corresponding observations.

## Survey Metadata

(Ideally, most of these should be gleaned from the raw data file
headers)

Survey ID:

Survey Type:

Scientific Question:

Observer(s):

Instrument Instance:

Instrument Design:

Protocol ID (if available):

Protocol Version (if available):

Observation Specification:

Site:

Date(s):

Schema Version:

### Observation Table Metadata:

- Path:

- Instrument Instance ID:

- Observation Specification Name:

- Observation Specification Version:

- The `Observation Specification Name` must exactly match the filename
  stem of the applicable observation schema.

  For example:

  - `cross-staff-observation` corresponds to
    `cross-staff-observation.schema.json`;
  - `quadrant-observation` corresponds to
    `quadrant-observation.schema.json`;
  - `compass-observation` corresponds to
    `compass-observation.schema.json`.

  Do not use the human-readable schema title, document heading, or
  display name in
  `survey.json.observation_tables[].observation_specification.name`
  unless it exactly matches the schema filename stem.

- Azimuth Reference (if applicable):

  - magnetic_north
  - true_north

For observation tables referenced to magnetic north, also provide:

- Magnetic Declination (degrees)
- Declination Sign Convention
- Declination Evaluation Time (optional)
- Declination Source (optional)

For observation tables referenced to true north, set:

- Magnetic Declination: null
- Declination Sign Convention: null

Declination metadata are not applicable when observations are already
referenced to true north.

When attached JSON Schemas conflict with prior examples, previous
archives, earlier conversation, or model memory, the attached JSON
Schemas are authoritative.

## Requirements

1.  Preserve only raw observations.

2.  Exclude all derived quantities unless explicitly requested.

3.  Preserve instrument-native measurements.

4.  Preserve physical quantities in their documented source units when
    constructing the initial working survey archive. Do not convert
    physical values during archive construction unless the user
    explicitly requests normalization. Record every noncanonical
    representation in `survey.json.working_representation`. Omit
    `working_representation` entirely when every physical quantity is
    already expressed in canonical units.

5.  The top-level keys of `survey.json.working_representation` must
    exactly match values used in
    `survey.json.observation_tables[].observation_specification.name`.

    Do not use observation-table paths as `working_representation` keys.

    For example:

``` json
"working_representation": { 
  "cross-staff-observation": { 
    "fiducial_width": "in", 
    "staff_reading": "in" 
  } 
}
```

6.  Representational normalization is a separate deterministic
    processing step performed by the approved normalization utility
    after the working survey archive has been constructed and validated.
    The archive builder must not duplicate or replace that normalization
    step.

7.  Separate narrative notes from the observation table.

8.  Preserve all supplied attachments.

9.  Do not invent metadata or observations. If required information is
    missing, leave a placeholder or report it.

10. Preserve the documented semantic meaning of every source field, even
    when source field names are informal, ambiguous, or noncanonical.

11. Produce a survey that conforms to the attached Survey Specification
    and applicable Observation Specification.

For compass observation tables recorded relative to magnetic north,
include table-level `measurement_reference` metadata in `survey.json`,
including:

- `azimuth_reference`
- `magnetic_declination_deg`
- `declination_sign_convention`
- optional `evaluated_at`
- optional `source`

Omit `measurement_reference` for observation tables that do not require
additional measurement-context metadata.

## Output

Generate one working observation table for each observation
specification represented in the survey. Each table must use the
canonical field names, column order, data types, and semantic meanings
defined by its applicable observation specification. Physical quantities
may remain in documented source units when those units are declared in
`survey.json.working_representation`.

``` text
<survey-id>/
├── README.md
├── survey.json
├── observations/
│   ├── <table-1>.csv
│   ├── <table-2>.csv
│   └── ...
├── notes.csv
├── attachments/
└── checksums.sha256
```

### README.md

Summarize:

- scientific question
- survey type
- instrument
- observer(s)
- files included
- assumptions made during archive construction
- unit conversions or other representational normalizations performed

### survey.json

Record survey metadata only.

### Observation tables

One canonical raw observation table is produced for each observation
specification represented in the survey.

Requirements:

- one header row
- one observation per row
- no formulas
- no derived variables
- standardized column names
- physical quantities preserved in documented source units for the
  working archive;
- every noncanonical unit declared in
  `survey.json.working_representation`;
- no unit conversion performed unless normalization is explicitly
  requested.

Raw contributor data are not required to use canonical field names or
column order. During survey preparation, the archive builder should
infer the semantic meaning of each source field from the available
headers, units, protocol documentation, notes, value patterns, and
survey context. The resulting working table(s) should use the canonical
field names defined by the applicable observation specification.

Semantic interpretation must be evidence-based. When multiple
interpretations remain plausible, the archive builder must ask a
targeted clarification question rather than silently assigning meaning.

### Nested Fields in CSV Tables

When an observation schema contains nested objects, represent their
scalar properties as flattened CSV columns using dot-separated field
names.

For example:

- `field_observation.primary_target_id`
- `field_observation.secondary_target_id`
- `calibration.target_id`
- `calibration.target_width`
- `calibration.target_distance`

Do not serialize nested objects as JSON strings inside individual CSV
cells unless an applicable observation specification explicitly requires
that representation.

Flattened columns are the canonical CSV serialization because they
preserve one scalar value per cell and remain directly usable in
spreadsheets, R, Python, and other tabular-data tools.

When a schema requires a nullable object property, preserve that
top-level property as an explicit CSV column when the object is null,
even when the alternative populated object is represented through
flattened, dot-separated columns.

For example, a cross-staff field-observation table must include:

- an empty `calibration` column, representing `calibration: null`;
- `field_observation.primary_target_id`; and
- `field_observation.secondary_target_id`.

Conversely, a cross-staff calibration table must include:

- the flattened `calibration.*` columns; and
- an empty `field_observation` column, representing
  `field_observation: null`.

Do not omit required nullable object properties merely because their
value is null for that observation type.

### notes.csv

Store narrative observations separately from observation tables.

The canonical notes table uses the following columns:

``` text

notes_id,note_text,observation_id,source_path
```

where:

- `notes_id` is a stable identifier for the note;

- `note_text` preserves the contributor's narrative comment as free
  text;

- `observation_id` is optional and links the note to a specific
  observation when applicable;

- `source_path` is optional and identifies the archive-relative path of
  the source file from which the note was extracted.

Construct `notes_id` according to the provenance of the note:

- observation-specific notes: `NOTE-OBS-...`

- source-file notes: `NOTE-SRC-...`

- survey-level notes: `NOTE-SUR-...`

Prefer the most specific provenance supported by the available evidence:

1.  observation;

2.  source file or attachment;

3.  survey.

Preserve contributor wording whenever possible. Minor formatting edits
required for CSV representation are acceptable, but do not summarize,
reinterpret, or strengthen the scientific meaning of contributor notes.

If a contributor supplies notes in raw-data headers, attached notebooks,
or separate notes files, preserve them in `notes.csv` and record the
originating archive file in `source_path` when appropriate.

When no notes are present, either omit `notes.csv` entirely or include
an empty table containing only the required header row.attachments/

Copy all supplied attachments unchanged.

The original observational data supplied by the contributor may be
included unchanged when appropriate to preserve provenance.

### checksums.sha256

Generate a populated \`checksums.sha256\` file containing one SHA-256
hash for every stable archive file, excluding:

\- \`checksums.sha256\`

\- \`validation.log\`

\- platform metadata such as \`.DS_Store\`

The builder should verify that every listed file exists before computing
its checksum.

## Final Report

Summarize:

- files created
- assumptions made
- unit conversions or other representational normalizations performed
- missing information
- validation concerns

Before declaring the working survey package complete, verify that:

- every physical quantity preserves the documented source measurement;
- every noncanonical unit is declared accurately in
  `survey.json.working_representation`;
- every top-level key in \`working_representation\` exactly matches an
  \`observation_specification.name\` represented in
  \`survey.json.observation_tables\`;
- required metadata are present;
- each observation table uses the field names, column order, data types,
  and semantic meanings required by its applicable Observation
  Specification;
- the survey metadata conform to the Survey Specification;
- no representational normalization has been performed unless explicitly
  requested;
- every \`observation_specification.name\` exactly matches the filename
  stem of the schema used to validate that observation table; and
- nested observation fields are represented using the established
  flattened, dot-separated CSV column convention rather than embedded
  JSON objects;
- the completed working survey package is ready for structural
  validation and subsequent normalization by the approved utility.
