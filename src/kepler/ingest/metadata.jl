struct ObservationSpecificationKey
    name::String
    version::String
end

struct SourceTableManifest
    manifest_index::Int
    relative_path::String
    instrument_instance_id::String
    specification::ObservationSpecificationKey
    measurement_reference_json::Union{Nothing,String}
    azimuth_reference::Union{Nothing,String}
    magnetic_declination_deg::Union{Nothing,Float64}
    declination_sign_convention::Union{Nothing,String}
    magnetic_declination_evaluated_at::Union{Nothing,String}
    magnetic_declination_source::Union{Nothing,String}
end

struct SurveyManifest
    archive_path::String
    schema_version::String
    survey_id::String
    title::Union{Nothing,String}
    survey_type::String
    scientific_question::String
    observer_ids::Vector{String}
    protocol_id::Union{Nothing,String}
    protocol_version::Union{Nothing,String}
    observing_location_json::String
    site_id::Union{Nothing,String}
    started_at::Union{Nothing,String}
    ended_at::Union{Nothing,String}
    submitted_at::Union{Nothing,String}
    attachments_json::String
    raw_manifest_json::String
    source_tables::Vector{SourceTableManifest}
end

function required_value(object, key::String, label::String)
    haskey(object, key) || throw(ArgumentError("Missing required $label: $key"))
    value = object[key]
    isnothing(value) && throw(ArgumentError("Required $label is null: $key"))
    return value
end

function required_string(object, key::String, label::String)
    String(required_value(object, key, label))
end

function optional_string(object, key::String)
    haskey(object, key) || return nothing
    value = object[key]
    isnothing(value) && return nothing
    return String(value)
end

function optional_float(object, key::String)
    haskey(object, key) || return nothing
    value = object[key]
    isnothing(value) && return nothing
    value isa Number || throw(ArgumentError("Expected numeric value for $key"))
    return Float64(value)
end

function optional_json(object, key::String)
    haskey(object, key) || return nothing
    value = object[key]
    isnothing(value) && return nothing
    return JSON3.write(value)
end

function source_table_manifest(table, manifest_index::Int)
    specification = required_value(
        table,
        "observation_specification",
        "observation-table manifest field",
    )

    key = ObservationSpecificationKey(
        required_string(specification, "name", "observation specification field"),
        required_string(specification, "version", "observation specification field"),
    )

    reference = haskey(table, "measurement_reference") ?
        table["measurement_reference"] : nothing

    return SourceTableManifest(
        manifest_index,
        required_string(table, "path", "observation-table manifest field"),
        required_string(
            table,
            "instrument_instance_id",
            "observation-table manifest field",
        ),
        key,
        isnothing(reference) ? nothing : JSON3.write(reference),
        isnothing(reference) ? nothing : optional_string(reference, "azimuth_reference"),
        isnothing(reference) ? nothing : optional_float(
            reference,
            "magnetic_declination_deg",
        ),
        isnothing(reference) ? nothing : optional_string(
            reference,
            "declination_sign_convention",
        ),
        isnothing(reference) ? nothing : optional_string(reference, "evaluated_at"),
        isnothing(reference) ? nothing : optional_string(reference, "source"),
    )
end

function load_survey_manifest(survey_path::AbstractString)
    archive_path = abspath(survey_path)
    manifest_path = joinpath(archive_path, "survey.json")

    isfile(manifest_path) || throw(ArgumentError(
        "Survey manifest does not exist: $manifest_path",
    ))

    raw_manifest_json = read(manifest_path, String)
    manifest = JSON3.read(raw_manifest_json)

    observing_location = required_value(
        manifest,
        "observing_location",
        "survey manifest field",
    )

    tables = required_value(
        manifest,
        "observation_tables",
        "survey manifest field",
    )

    source_tables = SourceTableManifest[
        source_table_manifest(table, index)
        for (index, table) in enumerate(tables)
    ]

    isempty(source_tables) && throw(ArgumentError(
        "Survey manifest must contain at least one observation table",
    ))

    observer_ids = String.(
        collect(required_value(manifest, "observer_ids", "survey manifest field")),
    )

    return SurveyManifest(
        archive_path,
        required_string(manifest, "schema_version", "survey manifest field"),
        required_string(manifest, "survey_id", "survey manifest field"),
        optional_string(manifest, "title"),
        required_string(manifest, "survey_type", "survey manifest field"),
        required_string(manifest, "scientific_question", "survey manifest field"),
        observer_ids,
        optional_string(manifest, "protocol_id"),
        optional_string(manifest, "protocol_version"),
        JSON3.write(observing_location),
        optional_string(manifest, "site_id"),
        optional_string(manifest, "started_at"),
        optional_string(manifest, "ended_at"),
        optional_string(manifest, "submitted_at"),
        something(optional_json(manifest, "attachments"), "[]"),
        raw_manifest_json,
        source_tables,
    )
end