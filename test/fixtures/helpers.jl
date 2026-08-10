using JSON3

function fixture_table(
    ;
    path::String,
    specification_name::String = "compass-observation",
    specification_version::String = "0.3",
    instrument_instance_id::String = "INS-0001",
    measurement_reference = nothing,
)
    (
        path = path,
        specification_name = specification_name,
        specification_version = specification_version,
        instrument_instance_id = instrument_instance_id,
        measurement_reference = measurement_reference,
    )
end

function write_fixture_archive(
    root::AbstractString,
    survey_id::String;
    tables,
)
    archive_path = joinpath(root, survey_id)
    mkpath(archive_path)

    manifest_tables = Any[]

    for (index, table) in enumerate(tables)
        table_path = joinpath(archive_path, table.path)
        mkpath(dirname(table_path))

        observation_id = "FIXTURE-$(survey_id)-$(index)"

        write(
            table_path,
            join([
                "observation_id,survey_id,instrument_instance_id,reading",
                "$(observation_id),$(survey_id),$(table.instrument_instance_id),$(index)",
                "",
            ], "\n"),
        )

        table_manifest = Dict(
            "path" => table.path,
            "instrument_instance_id" => table.instrument_instance_id,
            "observation_specification" => Dict(
                "name" => table.specification_name,
                "version" => table.specification_version,
            ),
        )

        if !isnothing(table.measurement_reference)
            table_manifest["measurement_reference"] =
                table.measurement_reference
        end

        push!(manifest_tables, table_manifest)
    end

    manifest = Dict(
        "schema_version" => "0.3",
        "survey_id" => survey_id,
        "survey_type" => "Test Fixture",
        "scientific_question" => "Does assembly preserve provenance?",
        "observer_ids" => ["OBS-0001"],
        "observing_location" => Dict(
            "latitude_deg" => 34.0,
            "longitude_deg" => -118.0,
            "coordinate_reference_system" => "WGS84",
        ),
        "observation_tables" => manifest_tables,
    )

    write(
        joinpath(archive_path, "survey.json"),
        JSON3.write(manifest),
    )

    archive_path
end

function fixture_validation_result(
    path::AbstractString;
    status::Symbol = :canonical,
)
    validation_log = if status == :canonical
        "Archive status: VALID CANONICAL ARCHIVE\nSubmission ready: YES\n"
    elseif status == :preliminary
        "Archive status: VALID PRELIMINARY ARCHIVE\nSubmission ready: NO\n"
    else
        "Archive status: INVALID ARCHIVE\nSubmission ready: NO\n"
    end

    Kepler.ArchiveValidationResult(
        abspath(path),
        "test-validator",
        "test-schemas",
        status == :invalid ? 1 : 0,
        "",
        "",
        validation_log,
        status,
    )
end
