struct AnalysisCollection
    observations::Dict{ObservationSpecificationKey,DataFrame}
    surveys::DataFrame
    source_tables::DataFrame
    lineage::Dict{ObservationSpecificationKey,DataFrame}
    assembly_record::NamedTuple
end

function deterministic_source_table_id(
    manifest::SurveyManifest,
    table::SourceTableManifest,
)
    identity = join([
        manifest.survey_id,
        string(table.manifest_index),
        table.relative_path,
        table.instrument_instance_id,
        table.specification.name,
        table.specification.version,
    ], "\0")

    digest = bytes2hex(SHA.sha256(identity))
    return "source-table-" * digest
end

tabular_value(value) = isnothing(value) ? missing : value

function survey_metadata_frame(manifests::Vector{SurveyManifest})
    rows = NamedTuple[]

    for manifest in manifests
        push!(rows, (
            survey_id = manifest.survey_id,
            schema_version = manifest.schema_version,
            title = tabular_value(manifest.title),
            survey_type = manifest.survey_type,
            scientific_question = manifest.scientific_question,
            observer_ids = join(manifest.observer_ids, ","),
            protocol_id = tabular_value(manifest.protocol_id),
            protocol_version = tabular_value(manifest.protocol_version),
            observing_location_json = manifest.observing_location_json,
            site_id = tabular_value(manifest.site_id),
            started_at = tabular_value(manifest.started_at),
            ended_at = tabular_value(manifest.ended_at),
            submitted_at = tabular_value(manifest.submitted_at),
            attachments_json = manifest.attachments_json,
            archive_path = manifest.archive_path,
            raw_manifest_json = manifest.raw_manifest_json,
        ))
    end

    DataFrame(rows)
end

function source_table_metadata_frame(manifests::Vector{SurveyManifest})
    rows = NamedTuple[]

    for manifest in manifests
        for table in manifest.source_tables
            push!(rows, (
                source_table_id = deterministic_source_table_id(manifest, table),
                survey_id = manifest.survey_id,
                manifest_index = table.manifest_index,
                relative_path = table.relative_path,
                instrument_instance_id = table.instrument_instance_id,
                observation_specification_name = table.specification.name,
                observation_specification_version = table.specification.version,
                measurement_reference_json =
                    tabular_value(table.measurement_reference_json),
                azimuth_reference = tabular_value(table.azimuth_reference),
                magnetic_declination_deg =
                    tabular_value(table.magnetic_declination_deg),
                declination_sign_convention =
                    tabular_value(table.declination_sign_convention),
                magnetic_declination_evaluated_at =
                    tabular_value(table.magnetic_declination_evaluated_at),
                magnetic_declination_source =
                    tabular_value(table.magnetic_declination_source),
            ))
        end
    end

    DataFrame(rows)
end

function canonical_survey_paths(survey_paths)
    raw_paths = survey_paths isa AbstractString ?
        [survey_paths] :
        String.(collect(survey_paths))

    isempty(raw_paths) && throw(ArgumentError(
        "At least one survey path is required",
    ))

    paths = realpath.(raw_paths)

    length(unique(paths)) == length(paths) || throw(ArgumentError(
        "Duplicate survey inputs are not allowed",
    ))

    return sort(paths)
end

function specification_is_selected(
    key::ObservationSpecificationKey,
    specifications,
)
    isnothing(specifications) && return true

    candidates = specifications isa AbstractString ||
        specifications isa ObservationSpecificationKey ?
        (specifications,) :
        collect(specifications)

    for candidate in candidates
        if candidate isa ObservationSpecificationKey
            candidate == key && return true
        elseif candidate isa AbstractString
            candidate == key.name && return true
        else
            throw(ArgumentError(
                "Specifications must contain strings or ObservationSpecificationKey values",
            ))
        end
    end

    return false
end

function require_exact_table_layout(
    frames::Vector{DataFrame},
    key::ObservationSpecificationKey,
)
    reference = first(frames)
    reference_names = names(reference)
    reference_types = eltype.(eachcol(reference))

    for frame in Iterators.drop(frames, 1)
        names(frame) == reference_names || throw(ArgumentError(
            "Incompatible columns for $(compatibility_label(key))",
        ))

        eltype.(eachcol(frame)) == reference_types || throw(ArgumentError(
            "Incompatible column types for $(compatibility_label(key)); " *
            "no coercion is performed during assembly",
        ))
    end
end

function assemble_analysis_data(
    survey_paths;
    specifications = nothing,
    validate_archive::Function = validate_canonical_archive,
)
    paths = canonical_survey_paths(survey_paths)

    validation_results = [
        validate_archive(path)
        for path in paths
    ]

    for result in validation_results
        result.status == :canonical || throw(ArgumentError(
            "Archive is not a valid canonical survey: $(result.source_path)\n" *
            result.validation_log,
        ))
    end

    manifests = sort(
        [load_survey_manifest(path) for path in paths];
        by = manifest -> manifest.survey_id,
    )

    survey_ids = [manifest.survey_id for manifest in manifests]

    length(unique(survey_ids)) == length(survey_ids) || throw(ArgumentError(
        "Duplicate survey_id values are not allowed in one collection",
    ))

    observation_parts = Dict{
        ObservationSpecificationKey,
        Vector{DataFrame},
    }()

    source_row_indices = Dict{
        ObservationSpecificationKey,
        Vector{Int},
    }()

    included_source_table_ids = Set{String}()

    for manifest in manifests
        for table in manifest.source_tables
            key = table.specification

            specification_is_selected(key, specifications) || continue

            table_path = joinpath(manifest.archive_path, table.relative_path)
            isfile(table_path) || throw(ArgumentError(
                "Manifest observation table does not exist: $table_path",
            ))

            observations = CSV.read(table_path, DataFrame; stringtype = String)

            hasproperty(observations, :source_table_id) && throw(ArgumentError(
                "Canonical observation table already contains reserved column " *
                "source_table_id: $table_path",
            ))

            hasproperty(observations, :observation_id) || throw(ArgumentError(
                "Observation table lacks required observation_id column: $table_path",
            ))

            source_table_id = deterministic_source_table_id(manifest, table)

            observations[!, :source_table_id] = fill(
                source_table_id,
                size(observations, 1),
            )

            push!(
                get!(
                    () -> DataFrame[],
                    observation_parts,
                    key,
                ),
                observations,
            )

            append!(
                get!(
                    () -> Int[],
                    source_row_indices,
                    key,
                ),
                1:size(observations, 1),
            )

            push!(included_source_table_ids, source_table_id)
        end
    end

    isempty(observation_parts) && throw(ArgumentError(
        "No observation tables matched the requested specifications",
    ))

    assembled_observations = Dict{
        ObservationSpecificationKey,
        DataFrame,
    }()

    assembled_lineage = Dict{
        ObservationSpecificationKey,
        DataFrame,
    }()

    for key in sort(
        collect(keys(observation_parts));
        by = compatibility_label,
    )
        frames = observation_parts[key]

        require_exact_table_layout(frames, key)

        assembled = vcat(frames...; cols = :orderequal)

        assembled_observations[key] = assembled
        assembled_lineage[key] = DataFrame(
            assembled_row_index = collect(1:size(assembled, 1)),
            observation_id = copy(assembled[!, :observation_id]),
            source_table_id = copy(assembled[!, :source_table_id]),
            source_row_index = source_row_indices[key],
        )
    end

    surveys = survey_metadata_frame(manifests)

    all_source_tables = source_table_metadata_frame(manifests)

    source_tables = all_source_tables[
        in.(
            all_source_tables.source_table_id,
            Ref(included_source_table_ids),
        ),
        :,
    ]

    assembly_record = (
        input_paths = paths,
        survey_ids = survey_ids,
        survey_schema_versions = sort(unique(
            [manifest.schema_version for manifest in manifests],
        )),
        validator_paths = sort(unique(
            [result.validator_path for result in validation_results],
        )),
        validator_exit_codes = [
            result.exit_code for result in validation_results
        ],
        compatibility_groups = sort([
            compatibility_label(key)
            for key in keys(assembled_observations)
        ]),
        warnings = String[],
    )

    AnalysisCollection(
        assembled_observations,
        surveys,
        source_tables,
        assembled_lineage,
        assembly_record,
    )
end

function observation_key(
    collection::AnalysisCollection,
    name::AbstractString;
    version::Union{Nothing,AbstractString} = nothing,
)
    matching_keys = [
        key for key in keys(collection.observations)
        if key.name == name &&
           (isnothing(version) || key.version == version)
    ]

    isempty(matching_keys) && throw(ArgumentError(
        "No assembled observations match $name" *
        (isnothing(version) ? "" : "@$version"),
    ))

    if length(matching_keys) > 1
        available = join(sort(
            [compatibility_label(key) for key in matching_keys],
        ), ", ")

        throw(ArgumentError(
            "Observation specification $name is ambiguous. " *
            "Specify version=. Available groups: $available",
        ))
    end

    only(matching_keys)
end

function observations(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    haskey(collection.observations, key) || throw(ArgumentError(
        "No assembled observations match $(compatibility_label(key))",
    ))

    copy(collection.observations[key])
end

function observations(
    collection::AnalysisCollection,
    name::AbstractString;
    version::Union{Nothing,AbstractString} = nothing,
)
    observations(collection, observation_key(collection, name; version))
end

survey_metadata(collection::AnalysisCollection) = copy(collection.surveys)

table_metadata(collection::AnalysisCollection) = copy(collection.source_tables)

function lineage(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey,
)
    haskey(collection.lineage, key) || throw(ArgumentError(
        "No lineage matches $(compatibility_label(key))",
    ))

    copy(collection.lineage[key])
end

function lineage(
    collection::AnalysisCollection,
    name::AbstractString;
    version::Union{Nothing,AbstractString} = nothing,
)
    lineage(collection, observation_key(collection, name; version))
end
