function context_includes(include)
    values = include isa Symbol ? (include,) : Tuple(include)
    requested = Set(Symbol.(values))
    supported = Set([:survey, :source_table])

    issubset(requested, supported) || throw(ArgumentError(
        "Unsupported context selection: $(collect(requested))",
    ))

    requested
end

function prefixed_context(
    frame::DataFrame,
    prefix::AbstractString;
    excluded_columns::Vector{Symbol} = Symbol[],
)
    context = copy(frame)

    rename!(
        context,
        [
            name => Symbol(prefix * String(name))
            for name in propertynames(context)
            if !(name in excluded_columns)
        ],
    )

    context
end

function materialize_context(
    collection::AnalysisCollection,
    key::ObservationSpecificationKey;
    include = (:survey, :source_table),
)
    requested = context_includes(include)
    materialized = observations(collection, key)

    if :source_table in requested
        source_context = prefixed_context(
            collection.source_tables,
            "source_table__";
            excluded_columns = [:source_table_id],
        )

        leftjoin!(
            materialized,
            source_context;
            on = :source_table_id,
        )
    end

    if :survey in requested
        hasproperty(materialized, :__kepler_context_survey_id) && throw(
            ArgumentError(
                "Reserved internal column already exists: __kepler_context_survey_id",
            ),
        )

        survey_lookup = select(
            collection.source_tables,
            :source_table_id,
            :survey_id,
        )

        rename!(
            survey_lookup,
            :survey_id => :__kepler_context_survey_id,
        )

        leftjoin!(
            materialized,
            survey_lookup;
            on = :source_table_id,
        )

        survey_context = prefixed_context(
            collection.surveys,
            "survey__";
            excluded_columns = [:survey_id],
        )

        leftjoin!(
            materialized,
            survey_context;
            on = :__kepler_context_survey_id => :survey_id,
        )

        select!(materialized, Not(:__kepler_context_survey_id))
    end

    materialized
end

function materialize_context(
    collection::AnalysisCollection,
    name::AbstractString;
    include = (:survey, :source_table),
    version::Union{Nothing,AbstractString} = nothing,
)
    key = observation_key(collection, name; version)

    materialize_context(collection, key; include)
end