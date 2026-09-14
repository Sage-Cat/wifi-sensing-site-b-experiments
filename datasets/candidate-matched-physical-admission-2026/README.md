# Candidate-Matched Physical Admission: Sanitized Same-Floor Inter-Zone Wi-Fi Selection Results

This bundle is a privacy-screened projection of a candidate-matched physical
admission experiment for cooperative Wi-Fi node selection. Four abstract
anchor-preserving candidates were evaluated on a shared sensing capture within
each analyzable block and then received candidate-specific protected-service
trials. C1 is anchor-only, C2A and C2B add one abstract peer each, C3 is the
three-node full reference, and CTRL0 is a zero-sensing service control.

The experiment covered two zones on the same floor of anonymized site-b. The
evaluated article-level layer composes
`budget_matched_cooperative_subset_fusion` for candidate, quality-control,
relative-quality, and native node/record objectives with
`airtime_qos_penalty_aware_measurement_coordination` for same-candidate measured
airtime and protected-service feasibility. It does not create a new method
identity, and it was not a cross-floor experiment.

## Design and denominators

Twelve scheduled blocks were consumed: one complete primary-per-protocol block,
one complete deviation-aware block, and ten incomplete blocks. The primary
complete-block yield was 1/12 (8.3%; Wilson 95% CI 1.49%--35.39%); the analyzable
yield was 2/12 (16.7%; 4.70%--44.80%). There were 75/180 completed service
trials, of which 30 belonged to the two analyzable blocks and 15 to the primary
block. Incomplete blocks remain in the denominator; partial trials are
diagnostic and are not treated as independent replications.

Across eight candidate-block observations, all eight passed data QC,
reference-relative quality, and the frozen 12% airtime gate, while four failed
only protected service. Six of 24 candidate-tier observations failed; every one
was uniquely limited by the 100 ms p95-latency component. The six CTRL0 tiers
are contextual rather than candidate observations, and CTRL0 failed protected
service in both analyzable blocks.

## Main descriptive results

The admissible-set intersection was C1. The maximum capture-derived airtime was
0.96872%, only 8.0727% of the 12% budget. Relative to C3, C1 used 66.6667% fewer
nodes, 50.4607% fewer
raw rows, and 92.3115%
less airtime in deviation-aware B03; the respective primary-B08 reductions were
66.6667%, 51.0907%, and
60.4094%.

The two equal-cardinality candidates show why raw-row count cannot substitute
for measured airtime. C2B used
47.6259% fewer rows
but 42.7720% more
airtime than C2A in B03; in B08 the corresponding values were
47.9237% fewer rows
and 42.9788% more
airtime. In the primary block C1 dominated C2A and C3 on the stated axes, but it
was incomparable with C2B because C2B had a 5.5556-percentage-point three-state
balanced-accuracy advantage.

Absolute prediction behavior was weak: in the primary block C1, C2A, and C3
had binary balanced accuracy 0.5417 and three-state balanced accuracy 0.3333;
C2B had 0.5417 and 0.3889. The binary predictions were 17/18 in one class for
every candidate; the three-state predictions were entirely one class for C1,
C2A, and C3 and 17/18 in one class for C2B. These counts are descriptive and do
not establish useful absolute recognition.

Exhaustive enumeration and QISS selected C1 in both analyzable blocks after
each evaluated the full four-candidate universe. QISS is supportive classical
search here: agreement establishes neither speedup, solver efficiency, quantum
computation, nor quantum advantage. Authoritative physical outputs for the
planned deterministic-pipeline and greedy comparators were absent, so no such
comparison is imputed.

## Files

- `data/campaign_disposition.csv`: all 12 scheduled-block dispositions and
  generic technical-failure categories;
- `data/candidate_block_results.csv`: eight candidate-block quality, resource,
  airtime, service, and selection outcomes;
- `data/service_tier_results.csv`: 24 candidate tiers and six contextual-control
  tiers, including independently recomputed component gates;
- `data/solver_results.csv`: abstract candidate traversal and selection ledgers;
- `data/results.json`: compact derived summaries and interpretation boundaries;
- `metadata.json`, `CITATION.cff`, and `SHA256SUMS`: scope, citation, and
  exact-file verification metadata.

Column names carry units. Throughput, loss, and p95-latency thresholds are 90%
of assigned throughput, 2%, and 100 ms, respectively.

## Scope and privacy boundary

This incomplete diagnostic campaign does not support campaign-level positive
validation, a causal sensing-effect estimate, population inference, or
cross-site/cross-floor generalization. Because the zero-sensing controls also
failed service, latency cannot be attributed to sensing alone. Private site,
run, node, hardware, network, time, topology, path, source-digest, and raw
capture information is excluded by an allowlisted export.

## Citation and license

Suggested citation:

> Sage-Cat (2026). *Candidate-Matched Physical Admission: Sanitized Same-Floor Inter-Zone Wi-Fi Selection Results* [Data set]. GitHub.
> https://github.com/Sage-Cat/wifi-sensing-site-b-experiments

For an immutable citation, use the full Git commit that contains this bundle.
The material is licensed under
[Creative Commons Attribution 4.0 International](../../LICENSE).
