#!/usr/bin/env python3
"""Fail-closed validation for the multi-study public publication surface."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT_FILES = {"README.md", "SECURITY.md", ".gitignore", ".gitattributes"}
ROOT_DIRS = {".github", "datasets", "docs", "schemas", "scripts", "tests"}
TEXT_EXTENSIONS = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".csv", ".tsv", ".jsonl", ".ndjson", ".gz"}
TEXT_BASENAMES = {".gitignore", ".gitattributes", "SHA256SUMS"}
BINARY_EXTENSIONS = {".pcap", ".pcapng", ".cap", ".bin", ".raw", ".wav", ".mp3", ".mp4", ".avi", ".mov", ".jpg", ".jpeg", ".png", ".webp", ".tif", ".geojson", ".kml", ".gpx", ".pdf", ".zip", ".tar", ".7z"}
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TEXT_BYTES = 20 * 1024 * 1024
PUBLIC_STATUSES = {
    "publication-candidate-not-claim-grade",
    "published",
    "published-not-claim-grade",
    "published-claim-grade",
}
MANIFEST_ENTRY_KEYS = {
    "id", "path", "program_id", "status", "source_record_id",
    "included_surfaces", "excluded_surfaces", "sanitization_summary",
    "claim_boundary",
}
METADATA_KEYS = {
    "schema_version", "dataset_id", "series", "program_id", "description",
    "evidence_status", "abstract_site", "abstract_levels", "abstract_zones",
    "time_basis", "human_context", "privacy_review", "claim_boundary",
}


def join(*parts: str) -> str:
    return "".join(parts)


FORBIDDEN_SEGMENTS = {
    join("pri", "vate"), join("r", "aw"), join("incom", "ing"), join("stag", "ing"),
    join("scr", "atch"), join("mapp", "ings"), join("sess", "ions"),
    join("site", "-media"), join("floor", "plans"), join("experi", "ments"),
    join("r", "uns"), join("cons", "ent"), join("access", "-control"),
}
RISKY_NAME_PARTS = {
    join("cred", "ential"), join("sec", "ret"), join("to", "ken"),
    join("pass", "word"), join("router", ""), join("config", ""),
    join("partici", "pant"), join("con", "sent"), join("access", "-control"),
    join("floor", "plan"), join("sched", "ule"), join("time", "table"),
    join("known", "_hosts"), join("authorized", "_keys"),
}
PRIVATE_MARKER = join("-----BEGIN ", "PRIVATE ", "KEY-----")
EMAIL_RE = re.compile(r"(?<![\w@])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w@])")
IP_RE = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
MAC_RE = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])")
HOME_RE = re.compile(r"(?:^|[\s'\"])/(?:home|Users)/[^\s/'\"]+")
ASSIGNMENT_RE = re.compile(
    join(r"(?i)\b(?:", "pass", "word|", "sec", "ret|", "to", "ken|api", "_key)",
         r"\s*[:=]\s*[^\s]{6,}")
)
COORDINATE_RE = re.compile(r"(?i)\b(?:lat|lon|latitude|longitude)\s*[:=]\s*-?\d{1,3}\.\d+")
COMMON_TOKEN_RE = re.compile(join(r"\b(?:gh", "p_|glpat-|AKIA)[A-Za-z0-9_-]{12,}\b"))
BEARER_RE = re.compile(join(r"(?i)\bBear", r"er\s+[A-Za-z0-9._~+/-]{16,}"))
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")
IPV6_RE = re.compile(r"(?i)(?<![0-9a-f:])(?:[0-9a-f]{1,4}:){3,7}[0-9a-f]{1,4}(?![0-9a-f:])")
DEVICE_RE = re.compile(join(r"(?:^|[\s'\"])/", "dev", r"/[A-Za-z0-9._/-]+"))
AUTH_URL_RE = re.compile(r"(?i)https?://[^\s/:]+:[^\s/@]+@[^\s/]+")


def issue(issues: list[str], path: Path, message: str) -> None:
    issues.append(f"{path.as_posix()}: {message}")


def relative(root: Path, path: Path) -> Path:
    return path.relative_to(root)


def forbidden_path(path: Path) -> bool:
    lowered = [part.lower() for part in path.parts]
    return any(part in FORBIDDEN_SEGMENTS for part in lowered) or any(
        marker in part for marker in RISKY_NAME_PARTS for part in lowered
    )


def risky_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", key.lower())
    blocked_fragments = {
        join("em", "ail"), join("ip", "address"), join("mac", "address"),
        join("b", "ssid"), join("s", "sid"), join("device", "path"),
        join("latitude", ""), join("longitude", ""), join("coord", "inate"),
        join("location", ""), join("address", ""), join("serial", ""),
        join("token", ""), join("secret", ""), join("password", ""),
        join("router", ""), join("host", "name"), join("participant", ""),
        join("consent", ""), join("schedule", ""), join("floor", "plan"),
        join("room", "name"),
    }
    return any(fragment in normalized for fragment in blocked_fragments)


def inspect_json(value: Any, path: Path, issues: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if risky_key(str(key)):
                issue(issues, path, "contains a privacy-risk field name")
            inspect_json(child, path, issues)
    elif isinstance(value, list):
        for child in value:
            inspect_json(child, path, issues)


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="strict") as handle:
            return handle.read(MAX_TEXT_BYTES + 1)
    return path.read_text(encoding="utf-8", errors="strict")


def inspect_text(path: Path, display: Path, issues: list[str]) -> None:
    try:
        text = read_text(path)
    except (OSError, UnicodeDecodeError):
        issue(issues, display, "is not readable UTF-8 text")
        return
    if len(text.encode("utf-8")) > MAX_TEXT_BYTES:
        issue(issues, display, "expanded text exceeds the public gate limit")
        return
    patterns = (
        (PRIVATE_MARKER, "contains a private-key marker"),
        (EMAIL_RE, "contains an email-like value"),
        (IP_RE, "contains an IP-like value"),
        (MAC_RE, "contains a hardware-address-like value"),
        (HOME_RE, "contains a home-directory path"),
        (ASSIGNMENT_RE, "contains a credential-like assignment"),
        (COMMON_TOKEN_RE, "contains a token-like value"),
        (BEARER_RE, "contains a bearer-token-like value"),
        (JWT_RE, "contains a JWT-like value"),
        (IPV6_RE, "contains an IPv6-like value"),
        (DEVICE_RE, "contains a device-path-like value"),
        (AUTH_URL_RE, "contains a credential-bearing URL"),
        (COORDINATE_RE, "contains a coordinate-like assignment"),
    )
    for pattern, message in patterns:
        if (pattern in text) if isinstance(pattern, str) else pattern.search(text):
            issue(issues, display, message)
    suffixes = path.suffixes
    data_suffix = suffixes[-2].lower() if path.suffix.lower() == ".gz" and len(suffixes) > 1 else path.suffix.lower()
    if data_suffix in {".json", ".jsonl", ".ndjson"}:
        try:
            if data_suffix == ".json":
                inspect_json(json.loads(text), display, issues)
            else:
                for line in text.splitlines():
                    if line.strip():
                        inspect_json(json.loads(line), display, issues)
        except json.JSONDecodeError:
            issue(issues, display, "is not valid JSON text")


def safe_relative_surface(value: object) -> bool:
    return isinstance(value, str) and bool(
        re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", value)
    )


def validate_manifest(root: Path, issues: list[str]) -> dict[str, dict[str, Any]]:
    manifest_path = root / "datasets" / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        issue(issues, manifest_path, "is missing or invalid JSON")
        return {}
    expected = {"schema_version", "repository", "series", "generated_at", "datasets", "excluded_candidates"}
    if set(manifest) != expected:
        issue(issues, manifest_path, "does not have the exact required keys")
        return {}
    if manifest["schema_version"] != 1 or manifest["repository"] != "multi-story-building-public-experiments" or manifest["series"] != "MULTI-STUDY":
        issue(issues, manifest_path, "has an invalid repository identity")
    if manifest["generated_at"] is not None and not isinstance(manifest["generated_at"], str):
        issue(issues, manifest_path, "has invalid generated_at")
    if not isinstance(manifest["datasets"], list) or not isinstance(manifest["excluded_candidates"], list):
        issue(issues, manifest_path, "has invalid collection fields")
        return {}
    if not all(isinstance(item, str) for item in manifest["excluded_candidates"]):
        issue(issues, manifest_path, "has non-string excluded candidates")
    allowed: dict[str, dict[str, Any]] = {}
    for entry in manifest["datasets"]:
        if not isinstance(entry, dict) or set(entry) != MANIFEST_ENTRY_KEYS:
            issue(issues, manifest_path, "has an invalid dataset entry")
            continue
        ident, bundle_path = entry["id"], entry["path"]
        expected_path = f"datasets/public/{ident}"
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident) or bundle_path != expected_path:
            issue(issues, manifest_path, "has a non-canonical dataset allowlist entry")
            continue
        if not isinstance(entry["program_id"], str) or not re.fullmatch(r"(?:MSB|UGRR)[0-9]{2}", entry["program_id"]):
            issue(issues, manifest_path, "has an invalid program identifier")
        if not isinstance(entry["status"], str) or entry["status"] not in PUBLIC_STATUSES:
            issue(issues, manifest_path, "has an invalid publication status")
        if not isinstance(entry["source_record_id"], str) or not re.fullmatch(r"SRC-[A-Z0-9]{12}", entry["source_record_id"]):
            issue(issues, manifest_path, "has an invalid opaque source record identifier")
        included = entry["included_surfaces"]
        excluded = entry["excluded_surfaces"]
        summary = entry["sanitization_summary"]
        if (
            not isinstance(included, list)
            or len(included) < 3
            or not all(safe_relative_surface(value) for value in included)
            or len(set(included)) != len(included)
        ):
            issue(issues, manifest_path, "has invalid included surfaces")
        if not isinstance(excluded, list) or not all(isinstance(value, str) and value for value in excluded):
            issue(issues, manifest_path, "has invalid excluded surfaces")
        if not isinstance(summary, list) or not summary or not all(isinstance(value, str) and value for value in summary):
            issue(issues, manifest_path, "has an invalid sanitization summary")
        if not isinstance(entry["claim_boundary"], str) or not entry["claim_boundary"].strip():
            issue(issues, manifest_path, "has an invalid claim boundary")
        if ident in allowed:
            issue(issues, manifest_path, "contains a duplicate dataset identifier")
        allowed[ident] = entry
    return allowed


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_bundle(root: Path, entry: dict[str, Any], issues: list[str]) -> None:
    name = entry["id"]
    bundle = root / "datasets" / "public" / name
    required = {"README.md", "metadata.json", "SHA256SUMS"}
    present = {child.name for child in bundle.iterdir()} if bundle.is_dir() else set()
    if not bundle.is_dir() or not required.issubset(present):
        issue(issues, bundle, "does not contain required README.md, metadata.json, and SHA256SUMS")
        return
    metadata_path = bundle / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        issue(issues, metadata_path, "is missing or invalid JSON")
        return
    if (
        set(metadata) != METADATA_KEYS
        or metadata.get("schema_version") != 1
        or metadata.get("dataset_id") != name
        or metadata.get("series") not in {"MSB", "UGRR"}
        or not str(metadata.get("program_id", "")).startswith(str(metadata.get("series", "")))
        or metadata.get("program_id") != entry["program_id"]
        or metadata.get("evidence_status") != entry["status"]
        or not re.fullmatch(r"site-S[0-9]{2}", str(metadata.get("abstract_site", "")))
        or not isinstance(metadata.get("abstract_levels"), list)
        or not metadata["abstract_levels"]
        or not all(re.fullmatch(r"level-L[0-9]{2}", str(value)) for value in metadata["abstract_levels"])
        or not isinstance(metadata.get("abstract_zones"), list)
        or not metadata["abstract_zones"]
        or not all(re.fullmatch(r"zone-Z[0-9]{2}", str(value)) for value in metadata["abstract_zones"])
        or metadata.get("time_basis") not in {"relative", "coarsened"}
        or metadata.get("human_context") not in {"instrument-only", "controlled-consented", "unlabelled-environment"}
        or not isinstance(metadata.get("description"), str)
        or not metadata["description"].strip()
        or not isinstance(metadata.get("privacy_review"), str)
        or not metadata["privacy_review"].strip()
        or metadata.get("claim_boundary") != entry["claim_boundary"]
    ):
        issue(issues, metadata_path, "does not match the public metadata profile")
    sums = bundle / "SHA256SUMS"
    try:
        checksums = {}
        for line in sums.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)", line)
            if not match:
                issue(issues, sums, "has a non-canonical checksum entry")
                break
            checksums[match.group(2)] = match.group(1)
        expected_files = {
            child.relative_to(bundle).as_posix()
            for child in bundle.rglob("*")
            if child.is_file() and child != sums
        }
        if set(checksums) != expected_files:
            issue(issues, sums, "does not exactly cover bundle files")
        included_surfaces = entry.get("included_surfaces")
        if not isinstance(included_surfaces, list) or not all(isinstance(value, str) for value in included_surfaces):
            included_surface_set: set[str] = set()
        else:
            included_surface_set = set(included_surfaces)
        if included_surface_set != expected_files:
            issue(issues, sums, "does not match manifest included surfaces")
        for surface, digest in checksums.items():
            candidate = bundle / surface
            if candidate.is_file() and file_sha256(candidate) != digest:
                issue(issues, sums, "does not match a bundle file")
                break
    except UnicodeDecodeError:
        issue(issues, sums, "is not UTF-8 text")


def run_validation(root: Path) -> list[str]:
    root = root.resolve()
    issues: list[str] = []
    if not root.is_dir():
        return [f"{root}: not a directory"]
    for child in root.iterdir():
        if child.name == ".git":
            continue
        if child.is_file() and child.name not in ROOT_FILES:
            issue(issues, child, "is not an allowed top-level file")
        if child.is_dir() and child.name not in ROOT_DIRS:
            issue(issues, child, "is not an allowed top-level directory")
    allowed_bundles = validate_manifest(root, issues)
    public_dir = root / "datasets" / "public"
    if public_dir.is_dir():
        actual_bundles = {child.name for child in public_dir.iterdir() if child.is_dir()}
        unexpected = actual_bundles - set(allowed_bundles)
        missing = set(allowed_bundles) - actual_bundles
        for name in sorted(unexpected | missing):
            issue(issues, public_dir / name, "does not exactly match the manifest allowlist")
        for name in sorted(actual_bundles & set(allowed_bundles)):
            validate_bundle(root, allowed_bundles[name], issues)
        for child in public_dir.iterdir():
            if child.is_file() and child.name != "README.md":
                issue(issues, child, "is not an allowed loose public-dataset file")
    for path in root.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        rel = relative(root, path)
        if path.is_symlink():
            issue(issues, rel, "symbolic links are not permitted")
            continue
        if path.is_dir():
            continue
        if forbidden_path(rel):
            issue(issues, rel, "uses a forbidden privacy-risk path")
        if path.suffix.lower() in BINARY_EXTENSIONS:
            issue(issues, rel, "uses a forbidden binary or media extension")
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in TEXT_BASENAMES:
            issue(issues, rel, "uses an unexpected file extension")
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            issue(issues, rel, "exceeds the public file-size limit")
            continue
        inspect_text(path, rel, issues)
    return issues


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    issues = run_validation(args.root)
    if issues:
        print("Publication gate failed:", file=sys.stderr)
        for item in issues:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("Publication gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
