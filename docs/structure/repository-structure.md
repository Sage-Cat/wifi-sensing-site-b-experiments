# Repository structure

- `docs/` — prospective campaign, method, privacy, and structure documents.
- `scripts/` — standard-library validation and JSON sanitization helpers.
- `schemas/` — machine-readable manifest and bundle metadata schemas.
- `datasets/manifest.json` — the sole public-bundle allowlist.
- `datasets/public/` — empty until an approved bundle is allowlisted.
- `tests/` — publication-gate regression tests.

Private research material belongs outside this repository. The directory names
ignored by `.gitignore` are deliberately not part of the public structure.
