function compass_fixture_collection(
    ;
    angle_deg::Real = 10.0,
    measurement_reference = nothing,
)
    mktempdir() do root
        archive = write_fixture_archive(
            root,
            "SURVEY-COMPASS-TRANSFORM";
            tables = [
                fixture_table(
                    path = "observations/compass.csv",
                    specification_name = "compass-observation",
                    specification_version = "0.3",
                    measurement_reference = measurement_reference,
                ),
            ],
        )

        write(
            joinpath(archive, "observations", "compass.csv"),
            join([
                "observation_id,survey_id,instrument_instance_id,angle_deg",
                "CMP-FIXTURE,SURVEY-COMPASS-TRANSFORM,INS-0001,$angle_deg",
                "",
            ], "\n"),
        )

        assemble_analysis_data(
            archive;
            validate_archive = fixture_validation_result,
        )
    end
end

@testset "canonical pilot compass true azimuth" begin
    collection = assemble_analysis_data(PILOT_ARCHIVE)

    key = ObservationSpecificationKey(
        "compass-observation",
        "UNSPECIFIED",
    )

    derived = derive_compass_true_azimuth(collection, key)

    @test derived.true_azimuth_deg == [
        327.5,
        321.5,
        317.5,
        320.5,
        316.5,
        315.5,
        308.5,
        356.5,
        340.5,
    ]

    @test all(derived.declination_applied_deg .== 11.5)
    @test all(
        derived.azimuth_transform_method .== "magnetic_declination",
    )

    @test all(
        derived.analysis_transform .== "compass_true_azimuth@0.1",
    )

    @test all(.!derived.declination_metadata_complete)

    @test derived.observation_id == observations(
        collection,
        key,
    ).observation_id

    @test derived.source_table_id == observations(
        collection,
        key,
    ).source_table_id

    @test !(:true_azimuth_deg in propertynames(
        observations(collection, key),
    ))
end

@testset "compass transform supports wraparound and true north" begin
    magnetic_collection = compass_fixture_collection(
        angle_deg = 355.0,
        measurement_reference = Dict(
            "azimuth_reference" => "magnetic_north",
            "magnetic_declination_deg" => 11.5,
            "declination_sign_convention" => "east_positive",
            "evaluated_at" => "2026-01-01T00:00:00Z",
            "source" => "fixture",
        ),
    )

    key = ObservationSpecificationKey(
        "compass-observation",
        "0.3",
    )

    magnetic = derive_compass_true_azimuth(
        magnetic_collection,
        key,
    )

    @test magnetic.true_azimuth_deg == [6.5]
    @test magnetic.declination_applied_deg == [11.5]
    @test magnetic.declination_metadata_complete == [true]

    true_collection = compass_fixture_collection(
        angle_deg = 355.0,
        measurement_reference = Dict(
            "azimuth_reference" => "true_north",
            "magnetic_declination_deg" => nothing,
            "declination_sign_convention" => nothing,
            "evaluated_at" => nothing,
            "source" => nothing,
        ),
    )

    true_north = derive_compass_true_azimuth(
        true_collection,
        key,
    )

    @test true_north.true_azimuth_deg == [355.0]
    @test true_north.declination_applied_deg == [0.0]
    @test true_north.azimuth_transform_method == [
        "already_true_north",
    ]

    @test true_north.declination_metadata_complete == [true]
end

@testset "compass transform supports west-positive declination" begin
    collection = compass_fixture_collection(
        angle_deg = 5.0,
        measurement_reference = Dict(
            "azimuth_reference" => "magnetic_north",
            "magnetic_declination_deg" => 11.5,
            "declination_sign_convention" => "west_positive",
            "evaluated_at" => "2026-01-01T00:00:00Z",
            "source" => "fixture",
        ),
    )

    key = ObservationSpecificationKey(
        "compass-observation",
        "0.3",
    )

    derived = derive_compass_true_azimuth(collection, key)

    @test derived.declination_applied_deg == [-11.5]
    @test derived.true_azimuth_deg == [353.5]
end

@testset "compass transform rejects incomplete reference metadata" begin
    key = ObservationSpecificationKey(
        "compass-observation",
        "0.3",
    )

    missing_declination = compass_fixture_collection(
        measurement_reference = Dict(
            "azimuth_reference" => "magnetic_north",
            "declination_sign_convention" => "east_positive",
        ),
    )

    @test_throws ArgumentError derive_compass_true_azimuth(
        missing_declination,
        key,
    )

    unsupported_convention = compass_fixture_collection(
        measurement_reference = Dict(
            "azimuth_reference" => "magnetic_north",
            "magnetic_declination_deg" => 11.5,
            "declination_sign_convention" => "unknown",
        ),
    )

    @test_throws ArgumentError derive_compass_true_azimuth(
        unsupported_convention,
        key,
    )

    unsupported_reference = compass_fixture_collection(
        measurement_reference = Dict(
            "azimuth_reference" => "grid_north",
        ),
    )

    @test_throws ArgumentError derive_compass_true_azimuth(
        unsupported_reference,
        key,
    )
end