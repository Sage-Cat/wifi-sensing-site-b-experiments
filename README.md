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

## Same-attempt evidence admission

Sanitized derived results from three separately frozen evidence-admission
phases are in
[`datasets/same-attempt-evidence-admission-2026/`](datasets/same-attempt-evidence-admission-2026/).
The bundle reports fixed-denominator dispositions, operational timing
envelopes, nominal comparator accounting, and deterministic fault-reason
coverage for a composed structural-and-timing admission rule. It preserves the
negative multidate endpoint and the associated safety--availability trade-off;
it contains no raw CSI or private site, run, network, or device identifiers.

## Local--central descriptor verification

Sanitized derived results from a fixed 12-unit verification campaign are in
[`datasets/local-central-descriptor-verification-2026/`](datasets/local-central-descriptor-verification-2026/).
The bundle reports same-archive local--central descriptor fidelity and the
outcomes of nine deterministic fault transformations under five qualification
rules. It contains no raw CSI, source captures, private identifiers, or
resource-performance claims.

## Stability-aware configuration maintenance

Sanitized derived results from a live same-floor inter-zone WLAN comparison are
in
[`datasets/stability-aware-configuration-maintenance-live-2026/`](datasets/stability-aware-configuration-maintenance-live-2026/).
The bundle reports six complete matched 30-minute intervals, verified
configuration changes, local actuator accounting, repeated service outcomes,
and explicit dispositions for excluded or incomplete follow-up campaigns. It
contains no raw radio traces, private site or run identifiers, network or device
identifiers, or exact topology.

All material is licensed under [CC BY 4.0](LICENSE).
