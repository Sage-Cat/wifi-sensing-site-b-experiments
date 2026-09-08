# Local--Central CSI Descriptor Verification Results

This bundle reports a sanitized projection of experiments that checked whether
one frozen CSI descriptor extractor produced the same result when it ran on
physical sensing processors and when the same sealed input archives were
replayed centrally. It also reports whether five qualification rules accepted
or rejected nine predeclared deterministic fault transformations.

The evaluated procedure is the paired-path centralized-raw / node-local-feature
comparison method. Its owner definition specifies the procedure; this bundle
reports only the bounded verification results.

## Design and denominators

The fixed campaign contained 12 completed and passing confirmation units,
distributed as four units in each of three anonymized UTC date strata. Each
unit compared three physical local outputs with central replay of the same
sealed inputs, giving 36 local--central path pairs. The 108 fault cases are nine
derived transformations applied once per unit; they are not 108 independent
physical captures.

The original, unmodified output in each unit was also evaluated as a clean
self-reference case. That 12-case check confirms that a rule did not reject its
own unmodified input. Independent evidence that the physical and central paths
agreed comes from the 36 path pairs, not from the self-reference check.

## Main results

- All 36 local--central descriptor pairs were byte-identical across 5,588
  windows and 67,056 ordered feature components. The squared-error sum, linear
  normalized mean squared error (NMSE), and maximum component-wise absolute gap
  were all 0.0.
- The full paired-path rule and the exact checksum-only rule each falsely
  qualified 0 of 108 fault cases and rejected 0 of 12 clean self-reference
  cases. These data therefore show no advantage over exact checksum-only.
- Timestamp-only, serialized-vector-parity, and no-gate controls falsely
  qualified 36/108, 60/108, and 108/108 fault cases, respectively. Relative to
  the two incomplete checks, the full rule reduced false qualification by 33.3
  and 55.6 percentage points within this registered fault set; the no-gate
  control accepted every faulty output.
- A separate, claim-ineligible technical qualification ran the extractor on
  three physical processors. Its 327 descriptor windows matched same-archive
  central replay in shape and serialized bytes, with a maximum component gap
  of 0.0 at a tolerance of 1e-9. It consumed no confirmation unit.

Here, a *false qualification* means that a rule accepted a package containing
a known deterministic fault. Linear NMSE is computed as the total squared
local--central error divided by the squared magnitude of the central reference.
The denominator was 609,598,293.4807463 and the numerator was 0.0.

## Files

- `metadata.json`: bundle identity, scope, privacy boundary, and file map;
- `data/results.json`: canonical machine-readable aggregate;
- `data/stratum-summary.csv`: independent date-stratum totals;
- `data/gate-summary.csv`: aggregate clean and fault outcomes for each rule;
- `data/fault-by-gate.csv`: false qualifications by fault type and rule;
- `data/physical-qualification.csv`: separate technical qualification results;
- `CITATION.cff`: citation metadata;
- `SHA256SUMS`: SHA-256 digest for every other file in this bundle.

## Scope and privacy boundary

The endpoint is processing-path fidelity and deterministic fault
qualification. It does not measure sensing or classification accuracy,
occupancy, presence, motion, compression, transport cost, latency, throughput,
energy, or cross-site/device generalization. Background activity was neither
controlled nor labelled and is not ground truth.

Upstream acquisition records belong to a separate timing study and are not
counted as results of this method. Raw CSI archives, private site records,
calendar dates and times, source/run/node identifiers, exact device inventory,
network identifiers, host paths, upstream hashes, and resource measurements are
not included. The public processor and stratum labels are abstract.

## Citation and license

Suggested citation:

> Sage-Cat (2026). *Local--Central CSI Descriptor Verification Results*
> [Data set]. GitHub.
> https://github.com/Sage-Cat/wifi-sensing-site-b-experiments

When reproducibility requires an immutable version, cite the full Git commit
that contains the bundle. The material is licensed under
[Creative Commons Attribution 4.0 International](../../LICENSE).
