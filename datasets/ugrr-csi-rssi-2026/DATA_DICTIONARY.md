# Data dictionary

## Frame files

Both compressed frame files share this schema:

| Column | Meaning |
| --- | --- |
| `dataset_id` | `ugrr-action-campaign` or `ugrr-labelled-motion-pilot`. |
| `window_index` | One-based window number within the subset. |
| `action` | Window-level controller action label. |
| `receiver_id` | De-identified receiver alias: `receiver-01` or `receiver-02`. |
| `frame_index` | Zero-based retained-frame index within receiver and window. |
| `relative_time_ms` | Host ingest time relative to the first retained frame in that window, milliseconds. It is not an absolute clock. |
| `device_time_us` | Device receive time relative to that receiver's first retained frame in the window, modulo 2^32 microseconds. |
| `device_sequence` | Firmware CSI sequence counter retained for gap/order analysis. |
| `rssi_dbm` | Received signal strength indicator, dBm. |
| `rate` | Numeric receive-rate field emitted by the receiver firmware metadata; no categorical interpretation is imposed here. |
| `signal_mode` | Numeric PHY signal-mode field. |
| `mcs` | Modulation and coding scheme field. |
| `bandwidth` | Numeric channel-bandwidth flag from receive metadata. |
| `smoothing` | Receive-metadata smoothing flag. |
| `not_sounding` | Receive-metadata not-sounding flag. |
| `aggregation` | Receive-metadata aggregation flag. |
| `stbc` | Space-time block coding flag. |
| `fec_coding` | Forward-error-correction coding flag. |
| `short_guard_interval` | Short guard interval flag. |
| `noise_floor_dbm` | Reported noise floor, dBm. |
| `ampdu_count` | A-MPDU counter from receive metadata. |
| `channel` | Observed Wi-Fi channel number. |
| `secondary_channel` | Numeric secondary-channel field. |
| `antenna` | Numeric antenna field from receive metadata. |
| `signal_length` | Reported received signal length. |
| `rx_state` | Receive-state code; all retained rows are zero. |
| `csi_length` | Number of signed-byte values in `csi_iq`; all retained rows contain 256. |
| `first_word_invalid` | Receiver CSI first-word validity flag; all retained rows are zero. |
| `phase` | `still`, `move`, `transition`, or `unlabelled`. |
| `cycle_index` | Zero-based controlled cycle for `still`/`move`; empty otherwise. |
| `csi_iq` | JSON array of interleaved signed-byte I/Q values: `[I0,Q0,I1,Q1,...]`. |

CSI positions are the emitted receiver-buffer order. This release does not
assert a universal subcarrier mapping or remove null/pilot positions; analyses
must apply a mapping appropriate to the hardware/PHY configuration and state
their assumptions.

## `window_metrics.csv`

Each row summarizes one capture window. `rssi_*` values are computed over the
published CSI frames. `sensing_score`, `goodput_mbps`, `p95_latency_ms`,
`loss_rate`, and `service_slo_pass` are observed window-level outputs and must
not be treated as per-frame labels. `capture_status` preserves the distinction
between the completed action campaign and the valid labelled segment whose
launcher failed after capture.

## `phase_intervals.csv`

`start_ms` and `end_ms` use the same relative-time origin as
`labelled_motion_csi.csv.gz`. The intervals record the observed phase start and
completion boundaries. `planned_duration_seconds` is the protocol target;
actual interval duration is `end_ms - start_ms`.
