# Multi-Study Public Experiments

Public scripts, schemas, privacy policies, and privacy-reviewed aggregate
datasets for Wi-Fi sensing studies. The repository path retains its historical
MSB name; each bundle declares its own series.

The UGRR bundles contain one descriptive action table and one labelled absolute
pilot segment. Neither is claim-grade; neither contains raw or record-level data.

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
