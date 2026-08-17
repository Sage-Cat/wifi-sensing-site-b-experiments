# Multi-Story Building Public Experiments

Public scripts, schemas, privacy policies, and future privacy-reviewed dataset
manifests for the **MSB** research series. Scientific research development is
maintained outside this public-data repository.

No datasets are published and this repository makes no empirical claims. It
deliberately contains no measured or raw data.

Only repository/privacy/dataset documentation, standard-library scripts,
schemas, and manifest-approved sanitized bundles may be public. See the
[publication policy](docs/privacy/publication-policy.md) and run the gate before
any public-data change:

```sh
python3 -m unittest discover -s tests
python3 scripts/validate_publication.py --root .
```

Licensing is intentionally undecided. No license grant is made by this
repository at this time.
