# Multi-Story Building Public Experiments

Public planning, methods, scripts, schemas, and future privacy-reviewed dataset
manifests for the **MSB** research series.

The research campaign is planned and unexecuted. No datasets are published and
this repository makes no empirical claims. It deliberately contains no measured
or raw data.

Only documentation, standard-library scripts, schemas, and manifest-approved
sanitized bundles may be public. See the [publication policy](docs/privacy/publication-policy.md)
and run the gate before any public-data change:

```sh
python3 -m unittest discover -s tests
python3 scripts/validate_publication.py --root .
```

Licensing is intentionally undecided. No license grant is made by this
repository at this time.
