function cross_staff_required_column(
    frame::DataFrame,
    column::Symbol,
)
    hasproperty(frame, column) || throw(ArgumentError(
        "Cross-staff transformation requires column: $column",
    ))
end

function cross_staff_has_value(value)
    (ismissing(value) || isnothing(value)) && return false

    value isa AbstractString || return true

    !isempty(strip(value))
end

function cross_staff_required_string(
    value,
    label::AbstractString,
)
    cross_staff_has_value(value) || throw(ArgumentError(
        "Cross-staff transformation requires $label",
    ))

    value isa AbstractString || throw(ArgumentError(
        "Cross-staff transformation requires string $label",
    ))

    String(value)
end

function cross_staff_positive_length(
    value,
    label::AbstractString,
    observation_id,
)
    cross_staff_has_value(value) || throw(ArgumentError(
        "Cross-staff observation $observation_id has no $label value",
    ))

    value isa Real || throw(ArgumentError(
        "Cross-staff observation $observation_id has non-numeric $label",
    ))

    isfinite(value) && value > 0 || throw(ArgumentError(
        "Cross-staff observation $observation_id requires positive finite " *
        label,
    ))

    Float64(value)
end

function cross_staff_source_table_ids(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    source_table_ids = Set{String}()

    for row in eachrow(table_metadata(collection))
        row.observation_specification_name == key.name || continue
        row.observation_specification_version == key.version || continue

        source_table_id = String(row.source_table_id)

        source_table_id in source_table_ids && throw(ArgumentError(
            "Duplicate source-table metadata row: $source_table_id",
        ))

        push!(source_table_ids, source_table_id)
    end

    isempty(source_table_ids) && throw(ArgumentError(
        "No source-table metadata matches $(compatibility_label(key))",
    ))

    source_table_ids
end

function derive_cross_staff_nominal_separation(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    raw = observations(collection, key)

    calibration_column = :calibration

    primary_target_column = Symbol(
        "field_observation.primary_target_id",
    )

    secondary_target_column = Symbol(
        "field_observation.secondary_target_id",
    )

    for column in [
        :observation_id,
        :fiducial_width,
        :staff_reading,
        :source_table_id,
        calibration_column,
        primary_target_column,
        secondary_target_column,
    ]
        cross_staff_required_column(raw, column)
    end

    source_table_ids = cross_staff_source_table_ids(collection, key)

    nominal_geometric_separation_deg = Float64[]

    for row in eachrow(raw)
        observation_id = row.observation_id

        source_table_id = cross_staff_required_string(
            row.source_table_id,
            "source_table_id for observation $observation_id",
        )

        source_table_id in source_table_ids || throw(ArgumentError(
            "No matching source-table metadata for $source_table_id",
        ))

        calibration_present = cross_staff_has_value(
            row[calibration_column],
        )

        primary_target_present = cross_staff_has_value(
            row[primary_target_column],
        )

        secondary_target_present = cross_staff_has_value(
            row[secondary_target_column],
        )

        calibration_present && throw(ArgumentError(
            "Cross-staff calibration observations require a separate " *
            "calibration transform: $observation_id",
        ))

        primary_target_present && secondary_target_present || throw(
            ArgumentError(
                "Cross-staff field observation requires both target IDs: " *
                "$observation_id",
            ),
        )

        fiducial_width = cross_staff_positive_length(
            row.fiducial_width,
            "fiducial_width",
            observation_id,
        )

        staff_reading = cross_staff_positive_length(
            row.staff_reading,
            "staff_reading",
            observation_id,
        )

        push!(
            nominal_geometric_separation_deg,
            (180.0 / pi) *
            2.0 *
            atan(fiducial_width / (2.0 * staff_reading)),
        )
    end

    derived = copy(raw)

    derived[!, :nominal_geometric_separation_deg] =
        nominal_geometric_separation_deg

    derived[!, :analysis_transform] = fill(
        "cross_staff_nominal_geometry@0.1",
        size(derived, 1),
    )

    derived
end
