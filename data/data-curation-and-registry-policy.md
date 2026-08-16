------------------------------------------------------------------------

editor_options: markdown: wrap: 72 ---

# Data Curation and Registration Policy

## Status

This policy states Kepler’s current approach to data curation and registration. It will evolve as Kepler’s standards, validation practices, registry design, and community needs mature.

## Purpose

Kepler develops shared scientific standards, protocols, software, and educational resources for observational astronomy. It also aims to help the community discover survey packages that contributors have chosen to share.

Kepler does not require contributors to transfer ownership or custody of their data in order to participate.

## Data Ownership and Hosting

Contributors, or the custodians they designate, retain ownership and control of their survey packages. They choose where and how those packages are hosted, published, maintained, revised, or withdrawn.

A publicly discoverable source repository is one possible hosting arrangement, but Kepler does not require a particular hosting platform or provider.

Kepler does not host contributor survey packages, provide contributor accounts, or operate a general-purpose data archive.

## Registration

Contributors may voluntarily request that an externally hosted survey package be registered with Kepler.

Registration is intended to make a package discoverable to the Kepler community and, when applicable standards and procedures exist, to record that a specific package snapshot satisfied a declared Kepler validation profile.

A registration concerns a specific, immutable package snapshot. It must not refer only to a moving branch, mutable directory, or other unspecified current version of a source repository.

Registration does not transfer ownership, copyright, custody, or responsibility for the underlying package to Kepler.

## Scope of Kepler Review

Kepler may maintain shared specifications, validation tools, registry records, and discovery information for registered packages. Registry intake may be reviewed manually.

A registry entry records only the scope of the stated registration and any contributor-supplied declared technical validation evidence. It does not certify that a package is complete, scientifically correct, safe, lawful, suitable for every audience, or free of personal, private, sensitive, or restricted
information.

Kepler does not comprehensively monitor or screen externally hosted packages. It does not provide identity verification, age verification, parental-consent management, legal review, content moderation, or data-custody services.

A registry entry may include contributor-supplied declared validation evidence for a specified Kepler profile. Unless explicitly stated otherwise, Kepler does not independently retrieve or rerun validation against the external package.

## Contributor Responsibilities

Contributors are responsible for deciding whether they have the right to publish their package and request Kepler registration.

Contributors are also responsible for reviewing their package, attachments, metadata, rendered materials, and source-repository history before making it public or requesting registration.

**Location and privacy warning:** Public survey packages may disclose exact coordinates, observing times, observer identities, routines, photographs, device metadata, filenames, attachments, or repository history. These details may reveal a home, school, observing site, or other sensitive location. Kepler registration may make externally hosted material easier to discover.

Contributors should publish only information they are comfortable making public. When appropriate, they may choose public observing locations, reduce location precision, omit unnecessary personal metadata, or retain sensitive source materials outside the public package.

## Availability, Delisting, and Source Restrictions

Kepler does not guarantee that an externally hosted package will remain available, unchanged, accessible, or preserved.

Kepler may decline a registration request, delist or remove a registry entry, or restrict registrations from particular source hosts at its discretion. This may occur in response to a credible request from a contributor, parent or guardian, rights holder, lawful authority, or another legitimately affected party, or when a source host becomes unsuitable for Kepler registry use.

Removing a registry entry removes Kepler’s discovery and registration record; it does not remove material from an external host.

## Optional Preservation and Aggregation

Kepler may in the future provide optional preservation copies of selected externally hosted package snapshots, or generate aggregate data products from compatible registered packages. Neither capability is currently implemented.

Registration does not require a contributor to deposit, transfer, or license a copy of a survey package to Kepler. A preservation copy, if offered, requires explicit permission and an appropriate license. It remains a retained copy of a specified package snapshot and does not replace the contributor-controlled source.

Any future aggregate collection will be a separately identified, versioned Kepler-generated data product. It will record its source package snapshots, selection criteria, applicable specifications, transformations, and provenance. It will not silently replace, alter, or obscure the original observations or their package-level context.

## Future Development

Kepler is still developing its policies and mechanisms for:

- Technical validation criteria and declared-validation evidence practices.
- Immutable package identification and integrity verification.
- Registry fields, identifiers, status definitions, and discovery workflows.
- Revalidation, withdrawal, delisting, and historical-status practices.
- Any optional aggregation, preservation, or checksum-verified mirror.
- Alignment of earlier centralized-archive and `kepler-data` planning documents with this federated approach.

Until these mechanisms are established, this policy describes the intended architectural direction rather than an implemented registry service.
