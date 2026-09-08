# Same-Attempt Evidence Admission: Sanitized Three-Phase Results

This bundle reports a privacy-screened projection of experiments that evaluated
whether one evidence package from cooperative Wi-Fi sensing should be admitted
for downstream scientific analysis. The evaluated rule composes structural and
baseline completeness with failure-aware timing admission on the same retained
attempt. Every mandatory condition is fail-closed: incomplete or technically
unavailable evidence remains in its scheduled denominator and is not silently
promoted.

The experiments used two sensing zones on the same floor of anonymized
`site-b`. No cross-floor experiment was performed. Independent event and fault
truth was recorded outside the method verdict. The three phases had different
frozen purposes and contracts, so their outcomes are reported separately and
must not be pooled.

## Design and denominators

- The initial fixed-denominator phase scheduled 12 units. Nine produced
  complete parents, three passed every phase-specific frozen gate, six complete
  units failed at least one gate, and three were partial or technically
  fail-closed. Its intention-to-treat (ITT) yield was 3/12 = 0.2500 (Wilson 95%
  interval 0.0889--0.5323). The phase closed as a negative diagnostic result;
  failed units were not replaced.
- The separate single-date operational phase completed and passed 4/4 units
  under its own 200/100/60-ms gap/uncertainty/residual profile. Its ITT yield
  was 1.0000 (Wilson 95% interval 0.5101--1.0000). A separately frozen
  secondary full-window monitor nevertheless found two gaps above 200 ms among
  12,010 intervals in one anonymized stream. The 0.0001665 rate stayed below
  its 0.0002 cap, but the 990.653861-ms maximum exceeded its 700-ms bound.
- The independent three-date phase consumed all 12 scheduled units: seven
  passed, three were complete scientific failures, and two failed closed for
  technical availability. ITT yield was 7/12 = 0.5833 (Wilson 95% interval
  0.3195--0.8067); the complete-unit fraction was 7/10 = 0.7000 (Wilson 95%
  interval 0.3968--0.8922). The predeclared endpoint of at least 10/12 passes
  plus zero fault-copy admissions was not met. Even granting both technical
  units as passes would give only 9/12. No post-outcome tuning was performed.

One complete parent supplied one untransformed case and ten predeclared fault
copies. Those copies are repeated deterministic transformations, not
independent physical trials. Across the 9, 4, and 10 complete parents in the
three phases, respectively, the composed rule admitted 0/90, 0/40, and 0/100
fault copies. Baseline-only admitted 36/90, 16/40, and 40/100; pass-through
admitted every copy. The ten fault classes produced structural reasons in six
classes and timing reasons in five, with counter discontinuity as the sole
overlap and all ten classes covered by their union.

## Safety--availability interpretation

Zero fault-copy admission is a bounded containment result, not proof of
end-to-end reliability. Under the retained nominal comparator, the composed
rule admitted only 3/9 untransformed parents in the initial phase and 0/4 and
0/10 in the two later phases. The later operational evaluator and the nominal
comparator were not equivalent: the operational rule used source/checkpoint
closure and CSI-pair 200/100/60-ms dimensions, whereas the comparator also used
a diagnostic eligibility scope and different timing dimensions. Therefore an
untransformed-parent rejection is reported as nominal accounting, not as an
operational false-rejection rate.

The results support auditable fail-closed containment for the evaluated fault
set. They do not establish the predeclared multidate operational endpoint,
population reliability, sensing or classification accuracy, occupancy
inference, cross-floor or cross-building generalization, or superiority over a
method evaluated in a different experiment.

## Files

- `metadata.json`: bundle identity, scope, privacy boundary, and file map;
- `data/results.json`: canonical machine-readable aggregate and interpretation;
- `data/phase-summary.csv`: fixed denominators, dispositions, ITT estimates,
  and phase endpoint outcomes;
- `data/operational-unit-outcomes.csv`: anonymized unit-level maxima for the
  two phases that used the 200/100/60-ms operational profile;
- `data/comparator-summary.csv`: nominal untransformed-parent and fault-copy
  accounting for four rules;
- `data/fault-reason-families.csv`: structural/timing reason coverage by
  deterministic fault class;
- `data/reason-family-summary.csv`: phase totals for reason-producing fault
  copies;
- `data/secondary-monitoring-summary.csv`: the bounded single-date
  full-window diagnostic;
- `CITATION.cff`: citation metadata;
- `SHA256SUMS`: SHA-256 digest for every other file in this bundle.

Timing maxima in `operational-unit-outcomes.csv` are maxima across the required
directed pairs and are rounded to six decimal places. Blank maxima represent
technical fail-closed units and are not imputed. Boolean values are `true` or
`false`.

## Scope and privacy boundary

Only allowlisted derived fields are published. The bundle excludes raw CSI and
radio captures, absolute timestamps and calendar dates, private experiment and
run identifiers, exact location and topology, network and device identifiers,
inventory, host paths, private hashes, credentials, source-linked health
records, operator details, and natural-occupancy information. Unit and stratum
labels are abstract. Results of other methods that used related captures are
not included.

## Citation and license

Suggested citation:

> Sage-Cat (2026). *Same-Attempt Evidence Admission: Sanitized Three-Phase
> Results* [Data set]. GitHub.
> https://github.com/Sage-Cat/wifi-sensing-site-b-experiments

For an immutable citation, use the full Git commit that contains this bundle.
The material is licensed under
[Creative Commons Attribution 4.0 International](../../LICENSE).
