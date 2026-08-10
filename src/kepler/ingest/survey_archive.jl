struct ArchiveValidationResult
    source_path::String
    validator_path::String
    schemas_dir::String
    exit_code::Int
    stdout::String
    stderr::String
    validation_log::String
    status::Symbol
end

function default_validator_path()
    joinpath(pkgdir(@__MODULE__), "data", "build-data", "validate-survey.py")
end

function default_schemas_dir()
    joinpath(pkgdir(@__MODULE__), "data", "schemas")
end

function validation_status(exit_code::Int, validation_log::AbstractString)
    exit_code == 0 || return :invalid

    if occursin("Archive status: VALID CANONICAL ARCHIVE", validation_log) &&
       occursin("Submission ready: YES", validation_log)
        return :canonical
    elseif occursin("Archive status: VALID PRELIMINARY ARCHIVE", validation_log)
        return :preliminary
    end

    return :invalid
end

function python_supports_jsonschema(python_path::AbstractString)
    command = Cmd([python_path, "-c", "import jsonschema"])

    process = run(pipeline(
        ignorestatus(command);
        stdout = devnull,
        stderr = devnull,
    ))

    return success(process)
end

function default_python_path()
    configured = get(ENV, "KEPLER_PYTHON", nothing)

    candidates = isnothing(configured) ?
        ["python3", "python"] :
        [configured, "python3", "python"]

    for candidate in candidates
        python_path = isabspath(candidate) ? candidate : Sys.which(candidate)
        isnothing(python_path) && continue

        python_supports_jsonschema(python_path) && return python_path
        
    end

    throw(ArgumentError(
        "Could not find a Python interpreter with the jsonschema package. " *
        "Set KEPLER_PYTHON to the intended interpreter path."
    ))
end

function validate_canonical_archive(
    survey_path::AbstractString;
    validator_path::AbstractString = default_validator_path(),
    schemas_dir::AbstractString = default_schemas_dir(),
    python::Union{Nothing,AbstractString} = nothing,
)
    source_path = abspath(survey_path)
    isdir(source_path) || throw(ArgumentError("Survey directory does not exist: $source_path"))
    isfile(validator_path) || throw(ArgumentError("Validator does not exist: $validator_path"))
    isdir(schemas_dir) || throw(ArgumentError("Schemas directory does not exist: $schemas_dir"))

    python_path = isnothing(python) ? default_python_path() : python

    mktempdir() do temporary_root
        staged_path = joinpath(temporary_root, basename(source_path))
        cp(source_path, staged_path; force = true)

        command = Cmd([
            python_path,
            validator_path,
            staged_path,
            "--schemas-dir",
            schemas_dir,
        ])

        stdout_buffer = IOBuffer()
        stderr_buffer = IOBuffer()

        process = run(pipeline(
            ignorestatus(command);
            stdout = stdout_buffer,
            stderr = stderr_buffer,
        ))

        validation_log_path = joinpath(staged_path, "validation.log")
        validation_log = isfile(validation_log_path) ?
            read(validation_log_path, String) : ""

        return ArchiveValidationResult(
            source_path,
            abspath(validator_path),
            abspath(schemas_dir),
            process.exitcode,
            String(take!(stdout_buffer)),
            String(take!(stderr_buffer)),
            validation_log,
            validation_status(process.exitcode, validation_log),
        )
    end
end