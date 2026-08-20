# Repository structure

- `docs/` — public data dictionary, privacy policy, and repository structure.
- `scripts/` — standard-library validation, sanitization, and bundle exporters.
- `schemas/` — machine-readable manifest and bundle metadata schemas.
- `datasets/manifest.json` — the sole public-bundle allowlist.
- `datasets/public/` — allowlisted aggregate public bundles.
- `tests/` — publication-gate regression tests.

Private research material belongs outside this repository. The directory names
ignored by `.gitignore` are deliberately not part of the public structure.
