function quadrant_required_column(
    frame::DataFrame,
    column::Symbol,
)
    hasproperty(frame, column) || throw(ArgumentError(
        "Quadrant transformation requires column: $column",
    ))
end

function quadrant_required_angle(
    value,
    observation_id,
)
    (ismissing(value) || isnothing(value)) && throw(ArgumentError(
        "Quadrant observation $observation_id has no angle_deg value",
    ))

    value isa Real || throw(ArgumentError(
        "Quadrant observation $observation_id has non-numeric angle_deg",
    ))

    isfinite(value) || throw(ArgumentError(
        "Quadrant observation $observation_id has non-finite angle_deg",
    ))

    Float64(value)
end

function quadrant_source_table_ids(
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

function derive_quadrant_nominal_altitude(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    raw = observations(collection, key)

    for column in [
        :observation_id,
        :angle_deg,
        :source_table_id,
    ]
        quadrant_required_column(raw, column)
    end

    source_table_ids = quadrant_source_table_ids(collection, key)
    nominal_altitude_deg = Float64[]

    for row in eachrow(raw)
        observation_id = row.observation_id
        source_table_id = row.source_table_id

        (ismissing(source_table_id) || isnothing(source_table_id)) && throw(
            ArgumentError(
                "Quadrant observation $observation_id has no source_table_id",
            ),
        )

        source_table_id isa AbstractString || throw(ArgumentError(
            "Quadrant observation $observation_id has non-string source_table_id",
        ))

        String(source_table_id) in source_table_ids || throw(ArgumentError(
            "No matching source-table metadata for $source_table_id",
        ))

        push!(
            nominal_altitude_deg,
            quadrant_required_angle(row.angle_deg, observation_id),
        )
    end

    derived = copy(raw)

    derived[!, :nominal_altitude_deg] = nominal_altitude_deg
    derived[!, :analysis_transform] = fill(
        "quadrant_nominal_altitude@0.1",
        size(derived, 1),
    )

    derived
end