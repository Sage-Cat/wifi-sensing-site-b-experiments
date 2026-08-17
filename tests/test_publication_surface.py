from __future__ import annotations

import json
import io
import hashlib
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from scripts import sanitize_json, validate_publication  # noqa: E402


def dataset_entry(
    ident: str = "msb01-summary",
    included_surfaces: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": ident,
        "path": f"datasets/public/{ident}",
        "program_id": "MSB01",
        "status": "published-not-claim-grade",
        "source_record_id": "SRC-000000000001",
        "included_surfaces": included_surfaces or ["README.md", "metadata.json", "data/summary.json"],
        "excluded_surfaces": ["private source evidence"],
        "sanitization_summary": ["retained aggregate instrument fields only"],
        "claim_boundary": "Instrument integrity only; no human-state inference.",
    }


def manifest(datasets: list[dict[str, object]] | None = None) -> dict[str, object]:
    return {
        "schema_version": 1,
        "repository": "multi-story-building-public-experiments",
        "series": "MSB",
        "generated_at": None,
        "datasets": datasets or [],
        "excluded_candidates": [],
    }


def public_root(base: Path, datasets: list[dict[str, object]] | None = None) -> Path:
    (base / "datasets" / "public").mkdir(parents=True)
    (base / "datasets" / "manifest.json").write_text(
        json.dumps(manifest(datasets)), encoding="utf-8"
    )
    (base / "datasets" / "public" / "README.md").write_text("empty\n", encoding="utf-8")
    return base


class PublicationSurfaceTests(unittest.TestCase):
    def test_empty_manifest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(validate_publication.run_validation(public_root(Path(temp))), [])

    def test_forbidden_path_and_content_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = public_root(Path(temp))
            (root / ("pri" + "vate")).mkdir()
            (root / ("pri" + "vate") / "note.txt").write_text("x\n", encoding="utf-8")
            (root / "docs").mkdir()
            value = "198" + "." + "51" + "." + "100" + "." + "17"
            (root / "docs" / "note.txt").write_text(value, encoding="utf-8")
            findings = validate_publication.run_validation(root)
            self.assertTrue(any("forbidden privacy-risk path" in item for item in findings))
            self.assertTrue(any("IP-like" in item for item in findings))

    def test_sanitizer_is_deterministic_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.json"
            destination = root / "public.json"
            payload = {
                "safe": "value",
                "b" + "ssid": "not retained",
                "contact": "a" + "@" + "example" + "." + "invalid",
            }
            source.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(sanitize_json.main([str(source), str(destination)]), 0)
            rendered = json.loads(destination.read_text(encoding="utf-8"))
            self.assertNotIn("b" + "ssid", rendered)
            self.assertEqual(rendered["contact"], "<redacted>")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(sanitize_json.main([str(source), str(destination)]), 1)

    def test_sanitizer_refuses_dangling_output_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.json"
            target = root / "outside.json"
            destination = root / "public.json"
            source.write_text('{"safe": "value"}', encoding="utf-8")
            destination.symlink_to(target)

            with redirect_stderr(io.StringIO()):
                self.assertEqual(sanitize_json.main([str(source), str(destination)]), 1)
            self.assertFalse(target.exists())

    def test_manifest_bundle_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            data = [dataset_entry()]
            findings = validate_publication.run_validation(public_root(Path(temp), data))
            self.assertTrue(any("manifest allowlist" in item for item in findings))

    def test_recursive_bundle_is_manifested_and_checksummed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            surfaces = ["README.md", "metadata.json", "data/summary.json"]
            root = public_root(Path(temp), [dataset_entry(included_surfaces=surfaces)])
            bundle = root / "datasets" / "public" / "msb01-summary"
            (bundle / "data").mkdir(parents=True)
            (bundle / "README.md").write_text("# Aggregate summary\n", encoding="utf-8")
            metadata = {
                "schema_version": 1,
                "dataset_id": "msb01-summary",
                "series": "MSB",
                "program_id": "MSB01",
                "description": "Aggregate instrument summary",
                "evidence_status": "published-not-claim-grade",
                "abstract_site": "site-S01",
                "abstract_levels": ["level-L01"],
                "abstract_zones": ["zone-Z01"],
                "time_basis": "relative",
                "human_context": "instrument-only",
                "privacy_review": "approved public aggregate",
                "claim_boundary": "Instrument integrity only; no human-state inference.",
            }
            (bundle / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            (bundle / "data" / "summary.json").write_text(
                json.dumps({"complete": True}), encoding="utf-8"
            )
            checksum_lines = []
            for surface in surfaces:
                payload = (bundle / surface).read_bytes()
                checksum_lines.append(f"{hashlib.sha256(payload).hexdigest()}  {surface}")
            (bundle / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
            self.assertEqual(validate_publication.run_validation(root), [])


if __name__ == "__main__":
    unittest.main()
