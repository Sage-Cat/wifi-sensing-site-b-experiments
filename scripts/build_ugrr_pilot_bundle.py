#!/usr/bin/env python3
"""Export one complete UGRR pilot action table as aggregate public data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ACTIONS = ("switch_to_11", "switch_to_6", "keep")
FIELDS = ("sensing", "goodput", "latency_ms", "loss_rate")
CLAIM_BOUNDARY = (
    "One engineering pilot table under unlabelled general activity; descriptive "
    "aggregate only. It is not model-training, efficacy, uncertainty-calibration, "
    "human-activity, occupancy, or multi-site evidence."
)


def finite_number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("outcome_value_not_numeric")
    rendered = float(value)
    if not math.isfinite(rendered):
        raise ValueError("outcome_value_not_finite")
    return rendered


def outcome(value: object) -> dict[str, float]:
    if not isinstance(value, dict) or set(value) != set(FIELDS):
        raise ValueError("outcome_schema_mismatch")
    return {field: finite_number(value[field]) for field in FIELDS}


def validated_table(document: object) -> tuple[dict[str, float], list[dict[str, Any]]]:
    if not isinstance(document, dict):
        raise TypeError("source_not_object")
    campaign = document.get("campaign")
    restoration = document.get("restoration")
    if (
        document.get("evidence") != "P1 PILOT / NOT MODEL DATA"
        or document.get("success") is not True
        or document.get("controller_route_preserved") is not True
        or not isinstance(restoration, dict)
        or not restoration
        or any(
            not isinstance(item, dict) or item.get("verified") is not True
            for item in restoration.values()
        )
        or not isinstance(campaign, dict)
        or campaign.get("status") != "complete"
        or campaign.get("abort_reason") is not None
        or campaign.get("planned_arm_order") != list(ACTIONS)
    ):
        raise ValueError("source_not_complete_pilot_table")
    shared = outcome(campaign.get("shared_pre_outcome"))
    arms = campaign.get("arms")
    if not isinstance(arms, list) or len(arms) != len(ACTIONS):
        raise ValueError("action_table_incomplete")
    validated: list[dict[str, Any]] = []
    for expected, arm in zip(ACTIONS, arms, strict=True):
        if (
            not isinstance(arm, dict)
            or arm.get("action") != expected
            or arm.get("delivered_action") != expected
            or arm.get("itt_eligible") is not True
            or arm.get("per_protocol_eligible") is not True
            or arm.get("target_acknowledged") is not True
            or arm.get("post_target_verified") is not True
            or arm.get("recovery_status") != "verified"
            or arm.get("qc_flags") != []
        ):
            raise ValueError("action_qc_failed")
        validated.append(
            {"action": expected, "outcome": outcome(arm.get("post_outcome"))}
        )
    return shared, validated


def numeric(value: float) -> str:
    return format(value, ".12g")


def write_json(path: Path, value: object) -> None:
    payload = (
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)


def export(source: Path, output: Path) -> None:
    if output.exists() or source.is_symlink() or not source.is_file():
        raise ValueError("unsafe_source_or_output")
    shared, arms = validated_table(json.loads(source.read_text(encoding="utf-8")))
    output.mkdir(parents=True)
    rows = [{"action": "shared_pre", "outcome": shared}, *arms]
    csv_path = output / "outcomes.csv"
    with csv_path.open("x", encoding="utf-8", newline="") as stream:
        fieldnames = [
            "window_index",
            "action",
            "sensing_score",
            "goodput_mbps",
            "p95_latency_ms",
            "loss_rate",
            "delta_sensing",
            "delta_goodput_mbps",
            "delta_latency_ms",
            "delta_loss_rate",
            "service_slo_pass",
            "nonkeep_sensing_threshold_pass",
            "qc_pass",
        ]
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for index, row in enumerate(rows):
            values = row["outcome"]
            deltas = {field: values[field] - shared[field] for field in FIELDS}
            action = str(row["action"])
            writer.writerow(
                {
                    "window_index": index,
                    "action": action,
                    "sensing_score": numeric(values["sensing"]),
                    "goodput_mbps": numeric(values["goodput"]),
                    "p95_latency_ms": numeric(values["latency_ms"]),
                    "loss_rate": numeric(values["loss_rate"]),
                    "delta_sensing": numeric(deltas["sensing"]),
                    "delta_goodput_mbps": numeric(deltas["goodput"]),
                    "delta_latency_ms": numeric(deltas["latency_ms"]),
                    "delta_loss_rate": numeric(deltas["loss_rate"]),
                    "service_slo_pass": str(
                        values["goodput"] >= 4.5
                        and values["latency_ms"] <= 35.0
                        and values["loss_rate"] <= 0.01
                    ).lower(),
                    "nonkeep_sensing_threshold_pass": str(
                        action.startswith("switch_to_") and deltas["sensing"] >= 0.05
                    ).lower(),
                    "qc_pass": "true",
                }
            )
    nonkeep = rows[1:3]
    write_json(
        output / "summary.json",
        {
            "schema_version": 1,
            "evidence_status": "published-not-claim-grade",
            "human_context": "unlabelled-environment",
            "table_count": 1,
            "window_count": len(rows),
            "nonkeep_action_count": len(nonkeep),
            "service_slo_pass_count": sum(
                item["outcome"]["goodput"] >= 4.5
                and item["outcome"]["latency_ms"] <= 35.0
                and item["outcome"]["loss_rate"] <= 0.01
                for item in nonkeep
            ),
            "nonkeep_sensing_threshold_pass_count": sum(
                item["outcome"]["sensing"] - shared["sensing"] >= 0.05
                for item in nonkeep
            ),
            "contract": {
                "goodput_floor_mbps": 4.5,
                "latency_ceiling_ms": 35.0,
                "loss_rate_ceiling": 0.01,
                "sensing_minimum_improvement": 0.05,
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_summary", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args(argv)
    try:
        export(args.source_summary, args.output_directory)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
