# Public-data publication policy

This repository is a deny-by-default public boundary. Its allowed content is
documentation, scripts, schemas, and approved bundles under `datasets/public/`.
No raw data, private mappings, operational logs, consent material, or source
evidence may be added.

Before a bundle is public, the designated privacy and publication owners must
approve a written review covering re-identification, linkage, location,
network/device, schedule, and participant risks. The bundle must be aggregate
and de-identified; retain no direct identifier, stable equipment/network ID,
absolute timestamp, detailed spatial attribute, media, or raw signal.

Each bundle needs an allowlisted manifest entry, `README.md`, metadata matching
the schema, `SHA256SUMS`, and a passing publication gate. Every nested bundle
file must be named in `included_surfaces` and covered by the checksum ledger;
private provenance is represented only by an opaque public source-record ID.
A passing gate does not grant permission to publish, commit, tag, release, or
push; explicit current authorization remains required. If privacy cannot be
demonstrated, keep the material private and publish only the method
description.
