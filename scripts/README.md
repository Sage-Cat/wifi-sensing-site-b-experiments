# Scripts

`validate_publication.py` is the fail-closed public-surface gate. It checks the
allowlisted layout, manifest, bundles, risky paths/extensions, oversized files,
and likely privacy or credential indicators without echoing detected values.

`sanitize_json.py` is a deterministic helper for JSON or NDJSON inputs. It
removes dangerous fields and replaces dangerous free-text values. It refuses to
overwrite output and is not a sanitizer for arbitrary binary or media.

`build_ugrr_pilot_bundle.py` validates one complete P1 pilot table and exports
only aggregate action outcomes, shared-pre deltas, and bounded QC counts.

`build_ugrr_labelled_segment.py` exports one validated labelled pilot segment
as aggregate sensing, service, QC, and alignment data.
