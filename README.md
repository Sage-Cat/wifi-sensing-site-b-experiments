# Wi-Fi sensing data and results: site B

This repository contains privacy-screened Wi-Fi sensing datasets and derived
experiment results from anonymized `site-b`.

## Record-level CSI/RSSI data

Sanitized record-level CSI data from two engineering pilots are stored in
`datasets/ugrr-csi-rssi-2026/data/`:

- `action_campaign_csi.csv.gz`: 31,748 frames from four channel-action windows
  and two abstract receivers;
- `labelled_motion_csi.csv.gz`: 7,235 frames from six controlled `STILL`/`MOVE`
  cycles;
- `phase_intervals.csv`: relative ground-truth intervals for those cycles.

The compressed files are ordinary CSV. They contain relative time, abstract
receiver and window IDs, CSI I/Q arrays, RSSI, channel, PHY metadata, phase,
and cycle labels. They do not contain absolute timestamps, network names,
IP/MAC addresses, host paths, exact topology, credentials, device identities,
or location details.

These pilots do not establish causal remediation effects, activity-recognition
accuracy, generalization, occupancy inference, or calibration.

## Local--central descriptor verification

Sanitized derived results from a fixed 12-unit verification campaign are in
[`datasets/local-central-descriptor-verification-2026/`](datasets/local-central-descriptor-verification-2026/).
The bundle reports same-archive local--central descriptor fidelity and the
outcomes of nine deterministic fault transformations under five qualification
rules. It contains no raw CSI, source captures, private identifiers, or
resource-performance claims.

All material is licensed under [CC BY 4.0](LICENSE).
