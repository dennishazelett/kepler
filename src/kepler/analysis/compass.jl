function compass_required_column(
    frame::DataFrame,
    column::Symbol,
)
    hasproperty(frame, column) || throw(ArgumentError(
        "Compass transformation requires column: $column",
    ))
end

function compass_required_string(
    value,
    label::AbstractString,
)
    (ismissing(value) || isnothing(value)) && throw(ArgumentError(
        "Compass transformation requires $label",
    ))

    value isa AbstractString || throw(ArgumentError(
        "Compass transformation requires string $label",
    ))

    String(value)
end

function compass_required_angle(
    value,
    observation_id,
)
    (ismissing(value) || isnothing(value)) && throw(ArgumentError(
        "Compass observation $observation_id has no angle_deg value",
    ))

    value isa Real || throw(ArgumentError(
        "Compass observation $observation_id has non-numeric angle_deg",
    ))

    isfinite(value) || throw(ArgumentError(
        "Compass observation $observation_id has non-finite angle_deg",
    ))

    Float64(value)
end

function compass_source_table_lookup(
    collection::AnalysisCollection,
)
    lookup = Dict{String,Any}()

    for row in eachrow(table_metadata(collection))
        source_table_id = String(row.source_table_id)

        haskey(lookup, source_table_id) && throw(ArgumentError(
            "Duplicate source-table metadata row: $source_table_id",
        ))

        lookup[source_table_id] = NamedTuple(row)
    end

    lookup
end

function compass_table_correction(
    table,
    source_table_id::AbstractString,
)
    reference = compass_required_string(
        table.azimuth_reference,
        "azimuth_reference for $source_table_id",
    )

    if reference == "true_north"
        return (
            declination_applied_deg = 0.0,
            azimuth_transform_method = "already_true_north",
            declination_metadata_complete = true,
        )
    end

    reference == "magnetic_north" || throw(ArgumentError(
        "Unsupported azimuth_reference for $source_table_id: $reference",
    ))

    declination = table.magnetic_declination_deg

    (ismissing(declination) || isnothing(declination)) && throw(
        ArgumentError(
            "Magnetic-north table lacks magnetic_declination_deg: " *
            source_table_id,
        ),
    )

    declination isa Real && isfinite(declination) || throw(ArgumentError(
        "Magnetic-north table has non-finite magnetic_declination_deg: " *
        source_table_id,
    ))

    convention = compass_required_string(
        table.declination_sign_convention,
        "declination_sign_convention for $source_table_id",
    )

    applied_declination = if convention == "east_positive"
        Float64(declination)
    elseif convention == "west_positive"
        -Float64(declination)
    else
        throw(ArgumentError(
            "Unsupported declination_sign_convention for " *
            "$source_table_id: $convention",
        ))
    end

    metadata_complete =
        !ismissing(table.magnetic_declination_evaluated_at) &&
        !ismissing(table.magnetic_declination_source)

    (
        declination_applied_deg = applied_declination,
        azimuth_transform_method = "magnetic_declination",
        declination_metadata_complete = metadata_complete,
    )
end

function derive_compass_true_azimuth(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    raw = observations(collection, key)

    compass_required_column(raw, :observation_id)
    compass_required_column(raw, :angle_deg)
    compass_required_column(raw, :source_table_id)

    source_tables = compass_source_table_lookup(collection)

    true_azimuth_deg = Float64[]
    declination_applied_deg = Float64[]
    azimuth_transform_method = String[]
    declination_metadata_complete = Bool[]

    for row in eachrow(raw)
        observation_id = row.observation_id
        source_table_id = compass_required_string(
            row.source_table_id,
            "source_table_id for observation $observation_id",
        )

        haskey(source_tables, source_table_id) || throw(ArgumentError(
            "No source-table metadata matches $source_table_id",
        ))

        table = source_tables[source_table_id]

        table.observation_specification_name == key.name ||
            throw(ArgumentError(
                "Source-table specification name does not match " *
                "requested key for $source_table_id",
            ))

        table.observation_specification_version == key.version ||
            throw(ArgumentError(
                "Source-table specification version does not match " *
                "requested key for $source_table_id",
            ))

        angle_deg = compass_required_angle(row.angle_deg, observation_id)
        correction = compass_table_correction(table, source_table_id)

        push!(
            true_azimuth_deg,
            mod(angle_deg + correction.declination_applied_deg, 360.0),
        )

        push!(
            declination_applied_deg,
            correction.declination_applied_deg,
        )

        push!(
            azimuth_transform_method,
            correction.azimuth_transform_method,
        )

        push!(
            declination_metadata_complete,
            correction.declination_metadata_complete,
        )
    end

    derived = copy(raw)

    derived[!, :true_azimuth_deg] = true_azimuth_deg
    derived[!, :declination_applied_deg] = declination_applied_deg
    derived[!, :azimuth_transform_method] = azimuth_transform_method
    derived[!, :analysis_transform] = fill(
        "compass_true_azimuth@0.1",
        size(derived, 1),
    )
    derived[!, :declination_metadata_complete] =
        declination_metadata_complete

    derived
end