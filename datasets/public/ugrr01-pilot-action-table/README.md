# UGRR01 pilot action table

Four aggregate windows from one complete engineering pilot table: shared-pre,
two channel actions, and keep. Activity was not controlled or labelled, so the
human context is `unlabelled-environment`.

- `data/outcomes.csv` contains absolute outcomes and shared-pre deltas.
- `data/summary.json` records the frozen thresholds and aggregate QC counts.
- `deployment.md` records only anonymized relative placement roles.
- `analysis.md` gives the bounded descriptive result.
- `scripts/build_ugrr_pilot_bundle.py` deterministically recreates both files
  from an authorized source summary.

This one-table dataset is descriptive and not claim-grade. It cannot support
efficacy, learned-policy, uncertainty-calibration, activity-recognition,
occupancy, or generalization claims.
