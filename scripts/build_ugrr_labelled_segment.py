#!/usr/bin/env python3
"""Export one validated UGRR labelled segment as a public aggregate."""

from __future__ import annotations

import argparse
import json
import math
import os
from collections.abc import Iterable
from pathlib import Path

CLAIM_BOUNDARY = (
    "One controlled labelled absolute pilot window; descriptive aggregate only. "
    "It is not a paired action effect, canonical table, model-training, efficacy, "
    "uncertainty-calibration, occupancy, or generalization evidence."
)


def finite(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("aggregate_value_not_numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("aggregate_value_not_finite")
    return result


def export(source: Path, output: Path) -> None:
    if source.is_symlink() or not source.is_file() or output.exists():
        raise ValueError("unsafe_source_or_output")
    value = json.loads(source.read_text(encoding="utf-8"))
    protocol = value.get("operator_protocol")
    qc = value.get("capture_qc")
    observed = value.get("outcome")
    alignment = value.get("service_alignment")
    if (
        value.get("evidence")
        != "LABELLED SEGMENTED P1 PILOT / NOT CANONICAL TABLE / NOT MODEL DATA"
        or value.get("reanalysis_status") != "valid-labelled-segment"
        or not isinstance(protocol, dict)
        or protocol.get("still_phases") != 6
        or protocol.get("move_phases") != 6
        or protocol.get("completed_phases") != 12
        or protocol.get("interrupted_phases") != 0
        or not isinstance(qc, dict)
        or qc.get("receiver_count") != 2
        or qc.get("collector_errors") != 0
        or qc.get("collector_checksums_verified") is not True
        or qc.get("protected_flow_slo_pass") is not True
        or qc.get("deployment_restored") is not True
        or qc.get("controller_route_preserved") is not True
        or not isinstance(observed, dict)
        or not isinstance(alignment, dict)
    ):
        raise ValueError("labelled_segment_qc_failed")
    public = {
        "schema_version": 1,
        "evidence_status": "published-not-claim-grade",
        "human_context": "controlled-consented",
        "segment_count": 1,
        "action": "switch_to_11",
        "operator_protocol": {
            "cycles": 6,
            "phase_duration_seconds": 10,
            "still_phases": 6,
            "move_phases": 6,
        },
        "qc": {
            "receiver_count": 2,
            "collector_record_count": int(qc["collector_records"]),
            "collector_error_count": 0,
            "checksums_verified": True,
            "service_slo_pass": True,
            "restoration_verified": True,
        },
        "score": {
            "sensing": finite(observed["sensing_score"]),
            "task": finite(observed["task_component"]),
            "acquisition": finite(observed["acquisition_component"]),
            "consistency": finite(observed["consistency_component"]),
        },
        "service": {
            "goodput_mbps": finite(observed["goodput_mbps"]),
            "p95_latency_ms": finite(observed["p95_latency_ms"]),
            "loss_rate": finite(observed["loss_rate"]),
        },
        "alignment": {
            "first_phase_start_minus_service_start_ms": finite(
                alignment["first_phase_start_minus_service_start_ms"]
            ),
            "accepted_tolerance_ms": finite(alignment["accepted_tolerance_ms"]),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    output.mkdir(parents=True)
    payload = (
        json.dumps(public, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode()
    descriptor = os.open(
        output / "segment-summary.json",
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o644,
    )
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_annotation", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args(argv)
    try:
        export(args.source_annotation, args.output_directory)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
