using SHA

const REPOSITORY_ROOT = normpath(joinpath(@__DIR__, ".."))

const PILOT_ARCHIVE = joinpath(
    REPOSITORY_ROOT,
    "data",
    "examples",
    "AST-PILOT-002",
    "SUR-PIL-2026-002-canonical",
)

function archive_fingerprint(root::AbstractString)
    files = String[]

    for (directory, _, names) in walkdir(root)
        append!(files, joinpath(directory, name) for name in names)
    end

    sort!(files)

    [
        (
            relpath(path, root),
            bytes2hex(SHA.sha256(read(path))),
        )
        for path in files
    ]
end

@testset "canonical pilot assembly" begin
    before = archive_fingerprint(PILOT_ARCHIVE)

    collection = assemble_analysis_data(PILOT_ARCHIVE)

    after = archive_fingerprint(PILOT_ARCHIVE)

    @test before == after

    @test size(survey_metadata(collection), 1) == 1
    @test size(table_metadata(collection), 1) == 3
    @test length(collection.observations) == 3

    @test collection.assembly_record.compatibility_groups == [
        "compass-observation@UNSPECIFIED",
        "cross-staff-observation@0.3",
        "quadrant-observation@UNSPECIFIED",
    ]

    compass = observations(collection, "compass-observation")

    @test size(compass, 1) == 9
    @test :source_table_id in propertynames(compass)
    @test !(:source_table__azimuth_reference in propertynames(compass))
    @test !(:survey__observing_location_json in propertynames(compass))

    compass_lineage = lineage(collection, "compass-observation")

    @test size(compass_lineage, 1) == size(compass, 1)
    @test compass.source_table_id == compass_lineage.source_table_id

    context = materialize_context(collection, "compass-observation")

    @test :source_table__azimuth_reference in propertynames(context)
    @test :source_table__magnetic_declination_deg in propertynames(context)
    @test :survey__observing_location_json in propertynames(context)

    @test all(context.source_table__azimuth_reference .== "magnetic_north")
    @test all(context.source_table__magnetic_declination_deg .== 11.5)

    context[!, :test_only_column] = fill(true, size(context, 1))

    @test !(:test_only_column in propertynames(
        observations(collection, "compass-observation"),
    ))
end

@testset "duplicate survey input rejection" begin
    @test_throws ArgumentError assemble_analysis_data([
        PILOT_ARCHIVE,
        PILOT_ARCHIVE,
    ])
end

@testset "repeated compatible tables preserve source identity" begin
    mktempdir() do root
        archive = write_fixture_archive(
            root,
            "SURVEY-REPEATED";
            tables = [
                fixture_table(
                    path = "observations/compass-magnetic.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                    instrument_instance_id = "INS-0001",
                    measurement_reference = Dict(
                        "azimuth_reference" => "magnetic_north",
                        "magnetic_declination_deg" => 11.5,
                        "declination_sign_convention" => "east_positive",
                        "evaluated_at" => "2026-01-01T00:00:00Z",
                        "source" => "fixture",
                    ),
                ),
                fixture_table(
                    path = "observations/compass-true.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                    instrument_instance_id = "INS-0002",
                    measurement_reference = Dict(
                        "azimuth_reference" => "true_north",
                        "magnetic_declination_deg" => nothing,
                        "declination_sign_convention" => nothing,
                        "evaluated_at" => nothing,
                        "source" => nothing,
                    ),
                ),
            ],
        )

        collection = assemble_analysis_data(
            archive;
            validate_archive = fixture_validation_result,
        )

        compass = observations(
            collection,
            "compass-observation";
            version = "0.3",
        )

        compass_lineage = lineage(
            collection,
            "compass-observation";
            version = "0.3",
        )

        @test size(table_metadata(collection), 1) == 2
        @test size(compass, 1) == 2
        @test size(compass_lineage, 1) == 2
        @test length(unique(compass.source_table_id)) == 2
        @test compass.source_table_id == compass_lineage.source_table_id

        context = materialize_context(
            collection,
            "compass-observation";
            version = "0.3",
        )

        @test context.source_table__azimuth_reference == [
            "magnetic_north",
            "true_north",
        ]

        @test context.source_table__magnetic_declination_deg[1] == 11.5
        @test ismissing(context.source_table__magnetic_declination_deg[2])
        @test context.source_table__declination_sign_convention[1] ==
            "east_positive"
        @test ismissing(
            context.source_table__declination_sign_convention[2],
        )
    end
end

@testset "incompatible specification versions remain separate" begin
    mktempdir() do root
        archive = write_fixture_archive(
            root,
            "SURVEY-VERSIONS";
            tables = [
                fixture_table(
                    path = "observations/compass-v03.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                ),
                fixture_table(
                    path = "observations/compass-v04.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.4",
                ),
            ],
        )

        collection = assemble_analysis_data(
            archive;
            validate_archive = fixture_validation_result,
        )

        @test length(collection.observations) == 2

        @test_throws ArgumentError observations(
            collection,
            "compass-observation",
        )

        @test size(observations(
            collection,
            "compass-observation";
            version = "0.3",
        ), 1) == 1

        @test size(observations(
            collection,
            "compass-observation";
            version = "0.4",
        ), 1) == 1
    end
end

@testset "invalid and preliminary archives are rejected" begin
    mktempdir() do root
        archive = write_fixture_archive(
            root,
            "SURVEY-REJECTED";
            tables = [
                fixture_table(
                    path = "observations/compass.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                ),
            ],
        )

        @test_throws ArgumentError assemble_analysis_data(
            archive;
            validate_archive = path -> fixture_validation_result(
                path;
                status = :invalid,
            ),
        )

        @test_throws ArgumentError assemble_analysis_data(
            archive;
            validate_archive = path -> fixture_validation_result(
                path;
                status = :preliminary,
            ),
        )
    end
end

@testset "input path order does not change assembly" begin
    mktempdir() do root
        archive_a = write_fixture_archive(
            root,
            "SURVEY-A";
            tables = [
                fixture_table(
                    path = "observations/compass.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                    instrument_instance_id = "INS-0001",
                ),
            ],
        )

        archive_b = write_fixture_archive(
            root,
            "SURVEY-B";
            tables = [
                fixture_table(
                    path = "observations/compass.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                    instrument_instance_id = "INS-0002",
                ),
            ],
        )

        first = assemble_analysis_data(
            [archive_a, archive_b];
            validate_archive = fixture_validation_result,
        )

        second = assemble_analysis_data(
            [archive_b, archive_a];
            validate_archive = fixture_validation_result,
        )

        key = ObservationSpecificationKey("compass-observation", "0.3")

        @test isequal(first.observations[key], second.observations[key])
        @test isequal(first.lineage[key], second.lineage[key])
        @test isequal(first.source_tables, second.source_tables)
        @test first.assembly_record.input_paths ==
            second.assembly_record.input_paths
        @test first.assembly_record.survey_ids ==
            second.assembly_record.survey_ids
    end
end
