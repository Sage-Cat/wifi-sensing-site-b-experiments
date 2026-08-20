# Public data dictionary

Metadata describes only approved aggregate variables. A bundle records an MSB
or UGRR program, abstract site/level/zone aliases, relative or coarsened time,
one evidence status, a privacy-review record, and an explicit claim boundary.
The manifest uses only an opaque `SRC-XXXXXXXXXXXX` source record.

Definitions must avoid direct identifiers, exact times, detailed spatial
attributes, network/device identifiers, and natural-occupancy ground truth.

UGRR action-table fields are sensing score, goodput, p95 latency, loss rate,
shared-pre deltas, service-SLO pass, sensing-threshold pass, and aggregate QC.
UGRR deployment notes use only five relative zone roles: near-end, mid-zone,
boundary, adjacent-zone, and far-end. They contain no coordinates or exact
environment description.
