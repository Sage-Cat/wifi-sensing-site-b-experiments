# Descriptive result

Both channel actions passed the frozen service SLO in this table. Neither met
the required `+0.05` sensing-score improvement over shared-pre.

| Action | Sensing delta | Goodput delta (Mbit/s) | p95 latency delta (ms) | Loss-rate delta | Service SLO | Sensing threshold |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| switch to 11 | -0.03063 | +0.00225 | -3.15 | -0.000463 | pass | fail |
| switch to 6 | -0.04872 | +0.00198 | -3.42 | -0.000463 | pass | fail |
| keep | +0.09399 | -0.00011 | +9.50 | +0.000019 | pass | not applicable |

This is one engineering pilot table under unlabelled general activity. It
supports pipeline and abstention-case illustration only, not efficacy or
generalization.
