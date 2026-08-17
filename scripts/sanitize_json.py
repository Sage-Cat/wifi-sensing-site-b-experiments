#!/usr/bin/env python3
"""Deterministically redact risky fields from JSON or NDJSON text only."""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


def join(*parts: str) -> str:
    return "".join(parts)


DROP_KEYS = {
    join("em", "ail"), join("ip", "address"), join("mac", "address"),
    join("b", "ssid"), join("s", "sid"), join("device", "path"),
    join("latitude", ""), join("longitude", ""), join("coord", "inate"),
    join("location", ""), join("address", ""), join("serial", ""),
    join("token", ""), join("secret", ""), join("password", ""),
    join("participant", ""), join("consent", ""), join("schedule", ""),
    join("router", ""), join("host", "name"), join("floor", "plan"),
    join("room", "name"),
}
EMAIL_RE = re.compile(r"(?<![\w@])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w@])")
IP_RE = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
MAC_RE = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])")
HOME_RE = re.compile(r"(?:^|[\s'\"])/(?:home|Users)/[^\s/'\"]+")
PRIVATE_MARKER = join("-----BEGIN ", "PRIVATE ", "KEY-----")
ASSIGNMENT_RE = re.compile(
    join(r"(?i)\b(?:", "pass", "word|", "sec", "ret|", "to", "ken|api", "_key)",
         r"\s*[:=]\s*[^\s]{6,}")
)
COORDINATE_RE = re.compile(r"(?i)\b(?:lat|lon|latitude|longitude)\s*[:=]\s*-?\d{1,3}\.\d+")


def risky_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", key.lower())
    return any(fragment in normalized for fragment in DROP_KEYS)


def redact_string(value: str) -> str:
    for pattern in (EMAIL_RE, IP_RE, MAC_RE, HOME_RE, ASSIGNMENT_RE, COORDINATE_RE):
        if pattern.search(value):
            return "<redacted>"
    if PRIVATE_MARKER in value:
        return "<redacted>"
    return value


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: sanitize(child)
            for key, child in sorted(value.items())
            if not risky_key(str(key))
        }
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        return redact_string(value)
    return value


def read_source(path: Path) -> str:
    if path.suffix.lower() == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="strict") as handle:
            return handle.read()
    return path.read_text(encoding="utf-8", errors="strict")


def write_output(path: Path, payload: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    if path.suffix.lower() == ".gz":
        with path.open("xb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
                zipped.write(payload.encode("utf-8"))
    else:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)


def parse_records(text: str, fmt: str) -> Any:
    if fmt == "json":
        return sanitize(json.loads(text))
    records = []
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip():
            try:
                records.append(sanitize(json.loads(line)))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid NDJSON record {number}") from exc
    return records


def render(records: Any, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for record in records)


def infer_format(path: Path) -> str:
    suffixes = path.suffixes
    effective = suffixes[-2] if path.suffix.lower() == ".gz" and len(suffixes) > 1 else path.suffix
    if effective.lower() == ".json":
        return "json"
    if effective.lower() in {".jsonl", ".ndjson"}:
        return "ndjson"
    raise ValueError("input name must end in .json, .jsonl, .ndjson, or one of those plus .gz")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--format", choices=("auto", "json", "ndjson"), default="auto")
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        fmt = infer_format(args.input) if args.format == "auto" else args.format
        records = parse_records(read_source(args.input), fmt)
        write_output(args.output, render(records, fmt))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"sanitize failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
