# Stability-Aware Configuration Maintenance: Sanitized Live Matched-Interval Results

This bundle reports a privacy-screened projection of a live WLAN experiment on
configuration maintenance. An upstream controller supplied one already tested
candidate configuration. The evaluated policy then decided whether to replace
the current configuration, retain it when its benefit did not cover the change
cost, or use an all-inactive fallback if neither configuration was feasible.

The experiment took place between two zones on the same floor of an anonymized
indoor site. The building has multiple floors, but no cross-floor experiment was
conducted.

## Design and denominators

The primary comparison used six complete 30-minute observation intervals: two
for the stability-aware policy, two for immediate replacement, and two for an
adapted hysteresis policy. Each interval contains six five-minute measurement
records, for three hours and 36 records in total. The observation interval—not
an individual five-minute record—is the primary statistical unit; the 36 rows
are repeated measurements and are not independent replicates.

Seven primary intervals were attempted. One adapted-hysteresis interval stopped
after three of six measurements because of a management-connection timeout. It
was excluded and replaced by a separately frozen interval assigned to the same
policy. `campaign_disposition.csv` also accounts for three later campaigns but
does not pool them into the balanced primary comparison.

## Main results

- The stability-aware policy made 0 verified configuration changes in one hour,
  compared with 12 changes per hour for each comparator. This is a 100%
  within-study reduction against either matched comparator.
- It accepted 0 of six optional change opportunities and required no subsequent
  feasibility-forced return. Each comparator made six optional changes and six
  forced returns per hour.
- Local actuator command-and-acknowledgement artifacts totalled 0 bytes for the
  stability-aware policy and 32,526 bytes per hour for each comparator. These
  are application-layer accounting bytes, not IEEE 802.11 airtime or management
  traffic.
- The composite service criterion passed 6/12 repeated records under the
  stability-aware policy, 5/12 under immediate replacement, and 4/12 under
  adapted hysteresis. All 36 records passed the sensing-quality,
  received-throughput, UDP-loss, and ICMP-reply gates; the ICMP-latency gate
  passed 15/36 records. These repeated-record counts are descriptive and do not
  support population-level significance claims.

The results support transition suppression for this frozen candidate stream at
one site and in one session. They do not establish end-to-end
candidate-selection superiority, generalize to other sites or workloads, or
constitute a head-to-head comparison with a different external experiment.

## Files

- `metadata.json`: bundle identity, scope, privacy boundary, and file map;
- `data/primary_policy_summary.csv`: one aggregate row per evaluated policy;
- `data/primary_included_intervals.csv`: the six complete included intervals;
- `data/primary_epoch_outcomes.csv`: 36 repeated within-interval measurements;
- `data/campaign_disposition.csv`: attempted, included, excluded, supporting,
  and technical-only campaign accounting;
- `CITATION.cff`: citation metadata;
- `SHA256SUMS`: SHA-256 digest for every other file in this bundle.

Column names carry units where needed. Boolean values are `true` or `false`.
`configuration_changes_per_hour` uses verified state changes; `change_type`
separates optional changes from feasibility-forced returns; and
`composite_service_pass` requires all listed service gates to pass.

## Scope and privacy boundary

Only allowlisted aggregate and repeated-measurement fields are published. The
bundle excludes raw radio traces, absolute timestamps, private experiment and
run identifiers, network and device identifiers, exact inventory and topology,
host paths, source hashes, credentials, and natural-occupancy information.
Public interval and campaign identifiers are abstract labels.

The diagnostic protocol-deviation campaign, the incomplete all-device
follow-up, and the continuous-operation postmortem are represented only by
disposition counts and limitations. They are not additional policy-comparison
observations.

## Citation and license

Suggested citation:

> Sage-Cat (2026). *Stability-Aware Configuration Maintenance: Sanitized Live
> Matched-Interval Results* [Data set]. GitHub.
> https://github.com/Sage-Cat/wifi-sensing-site-b-experiments

For an immutable citation, use the full Git commit that contains this bundle.
The material is licensed under
[Creative Commons Attribution 4.0 International](../../LICENSE).
