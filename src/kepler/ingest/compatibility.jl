function compatible_specifications(
    left::ObservationSpecificationKey,
    right::ObservationSpecificationKey,
)
    left == right
end

function compatibility_label(key::ObservationSpecificationKey)
    "$(key.name)@$(key.version)"
end