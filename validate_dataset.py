#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "datasets/ugrr-csi-rssi-2026"
DATA = DATASET / "data"
FRAME_HEADER = [
    "dataset_id", "window_index", "action", "receiver_id", "frame_index",
    "relative_time_ms", "device_time_us", "device_sequence", "rssi_dbm",
    "rate", "signal_mode", "mcs", "bandwidth", "smoothing", "not_sounding",
    "aggregation", "stbc", "fec_coding", "short_guard_interval",
    "noise_floor_dbm", "ampdu_count", "channel", "secondary_channel",
    "antenna", "signal_length", "rx_state", "csi_length",
    "first_word_invalid", "phase", "cycle_index", "csi_iq",
]
FRAME_FILES = {
    "action_campaign_csi.csv.gz": ("ugrr-action-campaign", 31_748),
    "labelled_motion_csi.csv.gz": ("ugrr-labelled-motion-pilot", 7_235),
}
MAC = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])")
ABSOLUTE_TIME = re.compile(r"20\d\d-\d\d-\d\d[T ]\d\d:\d\d")
PRIVATE_TOKENS = ("session_id", "source_id", "station_mac", "/var/lib/", "/home/")


def fail(message: str) -> None:
    raise ValueError(message)


def verify_checksums() -> None:
    checksum_path = DATASET / "SHA256SUMS"
    expected: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        expected[relative] = digest
    actual_files = {
        path.relative_to(DATASET).as_posix()
        for path in DATASET.rglob("*")
        if path.is_file() and path != checksum_path
    }
    if set(expected) != actual_files:
        fail("SHA256SUMS does not enumerate the exact dataset file set")
    for relative, digest in expected.items():
        observed = hashlib.sha256((DATASET / relative).read_bytes()).hexdigest()
        if observed != digest:
            fail(f"checksum mismatch: {relative}")


def validate_frames(filename: str, dataset_id: str, expected_rows: int) -> None:
    path = DATA / filename
    if path.read_bytes()[4:8] != b"\x00\x00\x00\x00":
        fail(f"gzip timestamp is not deterministic: {filename}")
    previous_index: dict[tuple[str, str], int] = {}
    previous_time: dict[tuple[str, str], float] = {}
    rows = 0
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FRAME_HEADER:
            fail(f"unexpected frame schema: {filename}")
        for row in reader:
            rows += 1
            text = "\t".join(row.values())
            if MAC.search(text) or ABSOLUTE_TIME.search(text):
                fail(f"direct identifier or absolute time in {filename} row {rows}")
            if any(token in text for token in PRIVATE_TOKENS):
                fail(f"private token in {filename} row {rows}")
            if row["dataset_id"] != dataset_id:
                fail(f"wrong dataset_id in {filename} row {rows}")
            if row["receiver_id"] not in {"receiver-01", "receiver-02"}:
                fail(f"invalid receiver alias in {filename} row {rows}")
            if row["phase"] not in {"unlabelled", "still", "move", "transition"}:
                fail(f"invalid phase in {filename} row {rows}")
            if row["phase"] in {"still", "move"}:
                if row["cycle_index"] not in {str(index) for index in range(6)}:
                    fail(f"invalid labelled cycle in {filename} row {rows}")
            elif row["cycle_index"]:
                fail(f"unexpected cycle outside labelled phase in {filename} row {rows}")
            key = (row["window_index"], row["receiver_id"])
            frame_index = int(row["frame_index"])
            if frame_index != previous_index.get(key, -1) + 1:
                fail(f"non-contiguous frame index in {filename} row {rows}")
            previous_index[key] = frame_index
            relative_time = float(row["relative_time_ms"])
            if relative_time < previous_time.get(key, relative_time):
                fail(f"relative time regression in {filename} row {rows}")
            previous_time[key] = relative_time
            rssi = int(row["rssi_dbm"])
            noise = int(row["noise_floor_dbm"])
            if not (-127 <= rssi <= 20 and -127 <= noise <= 20):
                fail(f"RF value outside documented range in {filename} row {rows}")
            iq = json.loads(row["csi_iq"])
            if len(iq) != int(row["csi_length"]) or len(iq) % 2:
                fail(f"CSI length mismatch in {filename} row {rows}")
            if any(not isinstance(value, int) or value < -128 or value > 127 for value in iq):
                fail(f"CSI value outside signed-byte range in {filename} row {rows}")
            if row["rx_state"] != "0" or row["first_word_invalid"] != "0":
                fail(f"invalid CSI admission flag in {filename} row {rows}")
    if rows != expected_rows:
        fail(f"expected {expected_rows} rows in {filename}, observed {rows}")


def validate_public_surface() -> None:
    forbidden_dirs = {"docs", "schemas", "scripts", "tests"}
    present = forbidden_dirs & {path.name for path in ROOT.iterdir() if path.is_dir()}
    if present:
        fail(f"obsolete scaffold directories remain: {sorted(present)}")
    json_files = [path for path in ROOT.rglob("*.json") if ".git" not in path.parts]
    if json_files:
        fail(f"unexpected JSON files: {json_files}")
    for path in DATASET.rglob("*"):
        if not path.is_file() or path.suffix == ".gz":
            continue
        text = path.read_text(encoding="utf-8")
        if MAC.search(text) or ABSOLUTE_TIME.search(text):
            fail(f"identifier or absolute timestamp in {path.relative_to(ROOT)}")


def main() -> int:
    try:
        verify_checksums()
        for filename, (dataset_id, expected_rows) in FRAME_FILES.items():
            validate_frames(filename, dataset_id, expected_rows)
        validate_public_surface()
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: 38,983 CSI frames; checksums, structure, labels, and privacy checks verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
