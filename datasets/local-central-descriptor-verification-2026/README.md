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

## Input origins and reuse

The 12 verification units used 12 retained capture sets. Eight capture sets
were reused as fixed inputs from a separate experiment on record completeness
and timing; four were collected for descriptor verification. No reused capture
is counted as a new acquisition. All 36 local--central processing comparisons
and all 108 descriptor-fault copies belong to the verification evaluation.

[`data/input-reuse.csv`](data/input-reuse.csv) documents every verification
unit using the public aliases `V01`--`V12`. For shared inputs, it links to rows
in the already published
[`Same-Attempt Evidence Admission` dataset](../same-attempt-evidence-admission-2026/),
specifically
[`data/operational-unit-outcomes.csv`](../same-attempt-evidence-admission-2026/data/operational-unit-outcomes.csv):

- `V01`--`V04` in verification stratum `S1` reuse the capture sets identified
  by `single-01`--`single-04` in its `single_date_operational` phase.
- `V09`--`V12` in verification stratum `S3` reuse the capture sets identified
  by `three-01`--`three-04` in its `independent_three_date` phase.
- `V05`--`V08` in verification stratum `S2` use dedicated capture sets and
  have no parent row in that admission dataset.

Stratum labels are local to each dataset: verification `S3` corresponds here
to admission `S1`. They must not be joined by stratum label alone. The CSV's
source-dataset, phase and unit fields identify the shared parent explicitly.
Empty source fields mean a dedicated input, not missing provenance.

The admission experiment evaluates whether the original records meet
completeness and timing requirements. Descriptor verification evaluates whether
local and central processing of a fixed archive produces the same output and
whether altered descriptor outputs are detected. These are distinct questions.
Passing descriptor verification does not establish that the underlying records
pass a timing-admission rule. Neither evaluation's outcomes should be counted
as independent replications of the other. The two experiments also use
separately defined fault transformations; their fault counts must not be pooled.

This public mapping documents input reuse and links published derived results;
it does not publish the raw capture sets or allow the full extraction to be
rerun from this bundle alone. Exact private-source identities and checksums are
retained in private export provenance. The existing numerical result files are
unchanged in version 1.1.0.

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
- `data/input-reuse.csv`: all 12 input origins and the eight shared-parent links;
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

Eight upstream capture sets belong to the separate admission experiment and
are reused only as verification inputs. Its timing conclusions are not
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
