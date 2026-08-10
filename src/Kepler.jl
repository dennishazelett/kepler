module Kepler

using CSV
using DataFrames
using JSON3
using SHA

include("kepler/ingest/survey_archive.jl")
include("kepler/ingest/metadata.jl")
include("kepler/ingest/compatibility.jl")
include("kepler/analysis/collection.jl")
include("kepler/analysis/materialize_context.jl")

export AnalysisCollection
export ObservationSpecificationKey
export assemble_analysis_data
export observations
export survey_metadata
export table_metadata
export lineage
export materialize_context

end