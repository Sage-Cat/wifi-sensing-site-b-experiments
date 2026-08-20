# UGRR CSI/RSSI dataset (2026 pilot captures)

This release contains two de-identified record-level subsets from UGRR
engineering experiments. Both use two abstract receivers and preserve the full
256-value signed-byte CSI I/Q vector for each admitted frame.

## Subsets

### Action campaign

`data/action_campaign_csi.csv.gz` contains 31,748 valid CSI frames from a
successful four-window campaign:

| Window | Action | Frames | Activity context |
| ---: | --- | ---: | --- |
| 1 | `shared_pre` | 7,900 | unlabelled general activity |
| 2 | `switch_to_11` | 7,873 | unlabelled general activity |
| 3 | `switch_to_6` | 8,062 | unlabelled general activity |
| 4 | `keep` | 7,913 | unlabelled general activity |

The original checksums passed before extraction. The source contained 32,067
collector envelopes. The public file retains 31,748 valid CSI frames; 318
timing-heartbeat envelopes, one unrelated malformed serial fragment, and six
malformed CSI fragments were excluded. Every retained frame has `rx_state=0`,
`first_word_invalid=0`, and a 256-value I/Q vector.

The four windows are not randomized or paired experimental replicates. Their
scores and service measurements are descriptive outcomes only.

### Labelled motion pilot

`data/labelled_motion_csi.csv.gz` contains 7,235 valid CSI frames from a
controlled pilot with six STILL/MOVE cycles. All 12 planned ten-second phases
completed, collector checksums passed, collector errors were zero, the
protected-flow service constraint passed, and the deployment was restored.

The launcher reported a post-capture analysis error. A separately recorded
reanalysis classified the completed capture as a valid labelled pilot segment,
not as a canonical action-effect table or model-validation dataset. The source
contained 7,307 envelopes. The public file excludes 72 timing heartbeats and
two malformed CSI fragments. It contains 2,403 `still`, 2,412 `move`, and 2,420
`transition` frames. `transition` covers deliberate gaps and time outside the
labelled phase intervals; it must not be merged silently into either class.

## Files

- `data/action_campaign_csi.csv.gz`: record-level action-campaign CSI/RSSI data.
- `data/labelled_motion_csi.csv.gz`: record-level phase-labelled pilot data.
- `data/window_metrics.csv`: window-level RF and protected-service summaries.
- `data/phase_intervals.csv`: labelled phase boundaries relative to the first
  retained frame.
- `DATA_DICTIONARY.md`: column definitions and units.
- `SHA256SUMS`: integrity hashes for every other file in this directory.

## Reading the files

```python
import csv
import gzip
import json

with gzip.open("data/labelled_motion_csi.csv.gz", "rt", newline="") as stream:
    for row in csv.DictReader(stream):
        iq = json.loads(row["csi_iq"])
        # iq[0], iq[1] are the first I/Q pair.
```

Rows are ordered by window, receiver, and capture order. Use
`relative_time_ms` to align receivers within a window. The receiver IDs are
dataset-local aliases and must not be interpreted as stable hardware IDs.

## Appropriate use

The data support format/parser development, CSI preprocessing, descriptive RF
analysis, labelled-pilot exploration, and reproducibility checks. They do not
support claims of causal remediation efficacy, population performance,
multi-site or multi-story generalization, activity-recognition accuracy,
occupancy inference, or calibrated predictive uncertainty.
