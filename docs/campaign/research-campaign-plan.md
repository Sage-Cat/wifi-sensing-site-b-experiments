# MSB prospective research campaign

## Scope and research questions

The MSB campaign is prospective and unexecuted. It investigates whether
privacy-reviewed, aggregate sensing features can support reproducible
environmental comparisons across abstracted building levels. It uses only
abstract site identifiers (`site-S01`), levels (`level-Lxx`), and zones
(`zone-Zxx`).

Research questions:

1. Can instrument stability be characterized without collecting identifiable
   environmental or network evidence?
2. Under controlled, consented conditions, are predefined aggregate features
   sufficiently stable within a level?
3. Can pre-registered features distinguish or transfer across abstract levels
   without releasing site-identifying artifacts?
4. Do conclusions remain robust across planned time windows after privacy and
   quality gates?

Natural occupancy, if present as contextual background, is never person or
occupancy ground truth and is not a label, target, or released attribute.

## Staged evidence plan

| Stage | Purpose | Public-safe outcome | Abort gate |
| --- | --- | --- | --- |
| MSB00 | Governance, threat model, consent and privacy review | Internal go/no-go record; no public evidence | Missing ownership, privacy basis, or safety approval |
| MSB01 | Instrument-only baseline | Calibration and quality protocol; aggregate integrity summary | Unstable instrument, unsafe collection route, or unavailable controls |
| MSB02 | Controlled, consented within-level sensing | Predefined within-level aggregate metrics and uncertainty | Consent/control failure, privacy risk, or inadequate quality |
| MSB03 | Cross-level transfer/discrimination | Held-out aggregate comparison report | Leakage, confounding, or pre-registered threshold failure |
| MSB04 | Temporal robustness | Planned-window robustness assessment | Drift, missing evidence, or privacy/publication failure |

No stage can manufacture positive results; an aborted or null outcome remains a
valid outcome. Each stage produces internal evidence first. Public release is
considered only for reviewed, aggregate, de-identified artifacts.

## Outcomes and metrics

Pre-register the feature definitions, sampling windows, exclusion criteria,
quality thresholds, uncertainty method, and comparison metric before MSB02.
Candidate outcomes include instrument completeness, feature missingness,
repeatability, held-out discrimination performance, transfer degradation, and
time-window robustness. Report uncertainty and all exclusions. Do not publish
raw traces, identifiers, absolute times, spatial coordinates, or records that
could reconstruct a place or routine.

## Privacy and publication gates

Before data collection, MSB00 must approve the threat model, consent basis,
data minimization plan, retention route, owner roles, and private storage.
Before any public artifact, an independent reviewer must confirm that it has no
site, person, network, device, natural-occupancy-ground-truth, schedule, or
location disclosure; the artifact must pass the repository validator and be
explicitly allowlisted in `datasets/manifest.json`.

## Owner-decision register

| Decision | Required owner | Status |
| --- | --- | --- |
| Governance and safety approval | Study owner | Unresolved |
| Privacy threat-model approval | Privacy owner | Unresolved |
| Consent basis and withdrawal procedure | Consent owner | Unresolved |
| Instrument configuration and calibration criteria | Technical owner | Unresolved |
| Pre-registration and analysis plan | Analysis owner | Unresolved |
| Public-release review and authorization | Publication owner | Unresolved |
