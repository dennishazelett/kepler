function cross_staff_fixture_collection(
    ;
    fiducial_width::String = "25.4",
    staff_reading::String = "250.0",
    calibration::String = "",
    primary_target::String = "Target-A",
    secondary_target::String = "Target-B",
    include_calibration_column::Bool = true,
)
    mktempdir() do root
        archive = write_fixture_archive(
            root,
            "SURVEY-CROSS-STAFF-TRANSFORM";
            tables = [
                fixture_table(
                    path = "observations/cross-staff.csv",
                    specification_name = "cross-staff-observation",
                    specification_version = "0.3",
                ),
            ],
        )

        columns = [
            "observation_id",
            "survey_id",
            "instrument_instance_id",
            "fiducial_width",
            "staff_reading",
            "calibration",
            "field_observation.primary_target_id",
            "field_observation.secondary_target_id",
        ]

        values = [
            "CS-FIXTURE",
            "SURVEY-CROSS-STAFF-TRANSFORM",
            "INS-0001",
            fiducial_width,
            staff_reading,
            calibration,
            primary_target,
            secondary_target,
        ]

        if !include_calibration_column
            deleteat!(columns, 6)
            deleteat!(values, 6)
        end

        write(
            joinpath(archive, "observations", "cross-staff.csv"),
            join([
                join(columns, ","),
                join(values, ","),
                "",
            ], "\n"),
        )

        assemble_analysis_data(
            archive;
            validate_archive = fixture_validation_result,
        )
    end
end

const CROSS_STAFF_KEY = ObservationSpecificationKey(
    "cross-staff-observation",
    "0.3",
)

@testset "canonical pilot cross-staff nominal geometry" begin
    collection = assemble_analysis_data(PILOT_ARCHIVE)

    derived = derive_cross_staff_nominal_separation(
        collection,
        CROSS_STAFF_KEY,
    )

    @test size(derived, 1) == 19

    @test isapprox(
        derived.nominal_geometric_separation_deg[1],
        5.38856858;
        atol = 1e-8,
    )

    @test isapprox(
        derived.nominal_geometric_separation_deg[14],
        29.59352449;
        atol = 1e-8,
    )

    @test isapprox(
        derived.nominal_geometric_separation_deg[15],
        38.580092438;
        atol = 1e-8,
    )

    @test all(
        derived.analysis_transform .==
        "cross_staff_nominal_geometry@0.1",
    )

    @test derived.observation_id == observations(
        collection,
        CROSS_STAFF_KEY,
    ).observation_id

    @test derived.source_table_id == observations(
        collection,
        CROSS_STAFF_KEY,
    ).source_table_id

    @test !(:nominal_geometric_separation_deg in propertynames(
        observations(collection, CROSS_STAFF_KEY),
    ))
end

@testset "cross-staff transform uses exact geometry" begin
    collection = cross_staff_fixture_collection(
        fiducial_width = "10.0",
        staff_reading = "10.0",
    )

    derived = derive_cross_staff_nominal_separation(
        collection,
        CROSS_STAFF_KEY,
    )

    @test isapprox(
        derived.nominal_geometric_separation_deg[1],
        53.130102354;
        atol = 1e-8,
    )
end

@testset "cross-staff transform rejects invalid rows" begin
    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(fiducial_width = "0.0"),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(staff_reading = "-1.0"),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(staff_reading = ""),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(fiducial_width = "not-a-number"),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(primary_target = ""),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(calibration = "{\"target_id\":\"REF\"}"),
        CROSS_STAFF_KEY,
    )

    @test_throws ArgumentError derive_cross_staff_nominal_separation(
        cross_staff_fixture_collection(
            include_calibration_column = false,
        ),
        CROSS_STAFF_KEY,
    )
end
