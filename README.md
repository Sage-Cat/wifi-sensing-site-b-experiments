# Wi-Fi sensing data: site B

Sanitized record-level CSI data from two engineering pilots at anonymized
`site-b` are stored in `datasets/ugrr-csi-rssi-2026/data/`:

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
accuracy, generalization, occupancy inference, or calibration. Data are
licensed under [CC BY 4.0](LICENSE).
