# Survey Archive: SUR-PIL-2026-002

## Scientific Question

Where is the Big Dipper?

## Survey Type

Pilot Field Survey

## Instruments

- **INS-0001 — Cross-staff** (`observations/cross-staff-observation.csv`): manual cross-staff readings of angular separation between star pairs, fiducial width and staff position recorded in imperial inches.
- **INS-0002 — Quadrant** (`observations/quadrant-observation.csv`): quadrant altitude-angle readings, in degrees.
- **INS-0005 — Compass (iPhone + clipboard)** (`observations/compass-observation.csv`): bearing readings taken with the native Apple Compass app on an iPhone mounted on a clipboard, set to magnetic north (first-time use of this setup).

## Observer(s)

OBS-0001 — D. Hazelett

## Site

Valencia, CA — 34°24'27"N 118°34'2"W (34.4075, -118.567222, WGS84), elevation 1250 ft.

## Date(s)

Field session began the evening of 2026-07-27 local time (Pacific); the UTC-timestamped raw observations fall on 2026-07-28, from 04:13:30Z to 05:35:52Z.

## Files Included

```text
SUR-PIL-2026-002/
├── README.md
├── survey.json
├── observations/
│   ├── cross-staff-observation.csv   (19 observations)
│   ├── quadrant-observation.csv      (9 observations)
│   └── compass-observation.csv       (9 observations)
├── notes.csv
├── attachments/
│   ├── raw_values.txt        (original mixed quadrant + compass source file)
│   └── raw-cs-values.txt     (original cross-staff source file)
└── checksums.sha256
```

## Assumptions Made During Archive Construction

- The raw data headers labeled instrument instances as `INS-001`, `INS-002`, and `INS-005` (3-digit codes). The Survey Specification (`survey.schema.json`) requires `instrument_instance_id` values to match `^INS-[0-9]{4}$` (exactly 4 digits). These identifiers were zero-padded to `INS-0001`, `INS-0002`, and `INS-0005` respectively to conform to the required format; no new instrument identity was invented.
- The source field `instrument` in `raw_values.txt` (values `quadrant` and `compass-iPhone-clipb`) records the instrument instance/label rather than the canonical `instrument` enum required by the observation specifications. Rows were split by this field into the `quadrant-observation` table (canonical `instrument: "quadrant"`) and the `compass-observation` table (canonical `instrument: "compass"`), with the descriptive label preserved only as the basis for instrument-instance assignment (`INS-0005`).
- In `raw-cs-values.txt`, the header row (`targ1,targ,fiducial,staff,timeutc`) has 5 fields but each data row has 6 comma-separated values. This was interpreted as the `timeutc` column being split across two raw values (UTC date, then UTC time), consistent with the two-column date/time layout used in `raw_values.txt`. Both were combined into a single ISO 8601 `observed_at` timestamp (e.g. `07/28/2026` + `04:59:35` → `2026-07-28T04:59:35Z`).
- All 19 cross-staff rows contain two named targets (`targ1`, `targ`) with no calibration target/width/distance fields, so all rows were classified as `field_observation` entries (`calibration: null`). `targ1` was mapped to `field_observation.primary_target_id` and `targ` to `field_observation.secondary_target_id`.
- `observation_id` values are not present in either raw source file. Stable sequential identifiers were generated per table, in the original row order of the source files: `QUAD-0001`…`QUAD-0009`, `CMP-0001`…`CMP-0009`, `CS-0001`…`CS-0019`.
- Target names/spellings (e.g. "Merok") were preserved exactly as recorded in the raw source files, including any apparent misspellings, per the instruction to preserve raw observations without correction.
- Latitude/longitude were converted from the DMS values in the raw headers (`34°24'27"N 118°34'2"W`) to decimal degrees (34.4075, -118.567222) as required by `survey.schema.json`, which only accepts numeric `latitude_deg`/`longitude_deg`. `coordinate_reference_system` was set to `WGS84`, the only value permitted by the schema.
- `survey.started_at`/`survey.ended_at` were derived from the minimum/maximum `observed_at` values across all three observation tables (2026-07-28T04:13:30Z to 2026-07-28T05:35:52Z), since no explicit survey start/end timestamps were supplied.
- Per user confirmation: `protocol_id` and `protocol_version` are recorded as `null` — no protocol was documented in the raw source files.
- Per user confirmation: `observation_specification.version` was set per-schema rather than copied across schemas. `cross-staff-observation.schema.json` explicitly requires row-level `schema_version` = `"0.3"`, so `"0.3"` was used for that table's specification version. Neither `quadrant-observation.schema.json` nor `compass-observation.schema.json` declares any version, draft label, or version field, so their `observation_specification.version` is recorded as the explicit placeholder `"UNSPECIFIED"` in `survey.json` — **this is a known gap requiring follow-up** if a real version number exists for those two specifications.
- The compass table's `measurement_reference` records `azimuth_reference: "magnetic_north"` (per the header note `setting:magneticN`) and `magnetic_declination_deg: 11.5` (per the header note `declination 11.5° (11° 29' East)`), with `declination_sign_convention: "east_positive"` as required by the schema. Per user confirmation, `source` is recorded as "Google Search (magnetic declination looked up for the survey's latitude/longitude)"; no `evaluated_at` timestamp was documented, so that optional field is omitted.
- The narrative note in `raw_values.txt` (about iPhone-compass and quadrant technique) was extracted into `notes.csv` as a source-level note (`NOTE-SRC-0001`), since it is not tied to any single observation.
- No `measurement_reference` was added to the quadrant table; quadrant altitude-angle readings do not have a documented azimuth reference requiring this metadata.

## Unit Conversions / Representational Normalizations Performed

**None.** All physical quantities are preserved in their documented source units for this working archive:

- `quadrant-observation.angle_deg` and `compass-observation.angle_deg` are already in the canonical unit (degrees); no `working_representation` entry is needed for these tables.
- `cross-staff-observation.fiducial_width` and `cross-staff-observation.staff_reading` are preserved in imperial inches (per the source header "Units: Imperial inches (fiducial & staff fields)"), the canonical schema unit is millimetres, and this noncanonical unit is declared in `survey.json.working_representation.cross-staff-observation`. Conversion to millimetres is left to the approved normalization utility, per the archive-construction specification.

## Known Gaps / Follow-up Needed

- `observation_specification.version` for `quadrant-observation` and `compass-observation` is `"UNSPECIFIED"` — no version is documented in the supplied schema files or raw data. Please supply the correct version(s) if available.
- `protocol_id` / `protocol_version` are `null` — no protocol documentation was found.
