# UGRR CSI/RSSI Experimental Dataset

Downloadable record-level Wi-Fi sensing data from two UGRR engineering pilots.
The repository name is historical: these files are **UGRR data, not evidence
from a multi-story-building campaign**.

## Download

The current dataset is in [`datasets/ugrr-csi-rssi-2026`](datasets/ugrr-csi-rssi-2026):

- [`action_campaign_csi.csv.gz`](datasets/ugrr-csi-rssi-2026/data/action_campaign_csi.csv.gz) — 31,748 CSI frames from four channel-action windows and two receivers;
- [`labelled_motion_csi.csv.gz`](datasets/ugrr-csi-rssi-2026/data/labelled_motion_csi.csv.gz) — 7,235 CSI frames aligned to six controlled STILL/MOVE cycles;
- [`window_metrics.csv`](datasets/ugrr-csi-rssi-2026/data/window_metrics.csv) — RSSI, sensing-score, goodput, latency, loss, and capture-status summaries;
- [`phase_intervals.csv`](datasets/ugrr-csi-rssi-2026/data/phase_intervals.csv) — relative boundaries for the labelled phases.

The compressed CSV files use only standard CSV and JSON-array syntax. Python,
R, Julia, MATLAB, spreadsheets with gzip support, and command-line tools can
read them without a project-specific library.

## What was measured

Two fixed Wi-Fi sensing receivers recorded CSI I/Q vectors and radio
metadata while a protected traffic flow was active. The action campaign covers
a shared pre-action state, two channel-switch states, and a keep state under
unlabelled general activity. The labelled pilot covers six controlled
STILL/MOVE cycles at one channel state.

These are engineering-pilot observations, not a representative population
sample. The action windows do not establish causal action effects, and the
labelled segment does not establish activity-recognition accuracy,
generalization, occupancy inference, or uncertainty calibration.

## Privacy and security

The published rows were reconstructed from checksum-verified capture bundles.
MAC addresses, network names, absolute timestamps, source/session identifiers,
host paths, device labels, credentials, exact topology, and site details were
removed. Relative timing, abstract receiver IDs, channel numbers, RSSI/RF
metadata, service outcomes, and CSI values were retained because they are
needed for analysis. No executable capture tooling or firmware is included.

Report a suspected sensitive-data leak through a private GitHub security report
instead of a public issue. Do not use the data to infer or identify a physical
site, network, device, or person.

## Integrity and license

Run `python3 validate_dataset.py` to verify checksums, row structure, CSI vector
lengths and ranges, relative timing, labels, and the absence of direct network
identifiers. Dataset files are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see [`LICENSE`](LICENSE).
Attribution: “UGRR CSI/RSSI Experimental Dataset, 2026, Sage-Cat research
workspace contributors,” with a link to this repository and the version or
commit used.
