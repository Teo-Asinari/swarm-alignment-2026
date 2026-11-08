## gemma-4-31B-it  (layers 60, batch check maxdiff 0.053, 45 scenarios)

**Behaviour**: share of prompts choosing act / approve / 'authorized=yes' (mean over scenarios, 95% bootstrap CI)

| role | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| actor | 1% [0–3] | 16% [6–27] | 0% [0–0] | 14% [6–24] | 33% [21–46] | 100% [100–100] |
| judge | 2% [0–5] | 11% [3–21] | 0% [0–0] | 11% [3–20] | 42% [28–56] | 100% [100–100] |
| cls | 2% [0–7] | 2% [0–7] | 2% [0–7] | 2% [0–7] | 21% [11–33] | 100% [100–100] |

Actor 'act' prompts per world: {'passed': 42, 'hearsay': 91, 'observed': 42, 'none': 6}; scenarios with ≥1 act: {'none': 1, 'passed': 8, 'rejected': 0, 'observed': 9, 'hearsay': 20, 'signed': 45}

- mean P(act) passed − rejected: 0.15 [0.07, 0.26]
- mean P(act) observed − rejected: 0.15 [0.06, 0.24]
- mean P(act) hearsay − rejected: 0.33 [0.21, 0.45]
- mean P(act) rejected − none: -0.02 [-0.04, -0.00]
- **Knowledge gap**: of 181 unauthorized 'act' decisions (23 scenarios), the matched classifier says NOT authorized in 70%; the matched judge denies in 26%.
- Overall classifier accuracy: none/passed/rejected/observed/hearsay 'no' and signed 'yes': 95%

**Prompt interventions** (actor; share choosing act; CI over scenarios)

| cond | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| base | 1% [0–3] | 16% [7–26] | 0% [0–0] | 12% [3–23] | 24% [13–38] | 100% [100–100] |
| neutral | 0% [0–0] | 14% [6–24] | 0% [0–0] | 12% [3–22] | 29% [16–42] | 100% [100–100] |
| irrelevant | 1% [0–3] | 10% [2–19] | 0% [0–0] | 14% [6–26] | 22% [11–36] | 100% [100–100] |
| reminder | 0% [0–0] | 3% [0–9] | 0% [0–0] | 4% [0–11] | 16% [7–27] | 100% [100–100] |
| verdict | 0% [0–0] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 4% [0–11] | 98% [93–100] |

Own verdict 'breaks the rule = yes': none 100%, passed 99%, rejected 100%, observed 100%, hearsay 83%, signed 0%

**Projection on cross-fitted authorization axis** (0 = classifier 'none', 1 = classifier 'signed')

| layer | actor act (unauth.) | actor comply (unauth. social) | actor none | actor signed | cls passed | cos(auth, decision) |
|---|---|---|---|---|---|---|
| 0 | +nan (n=175) | +nan (n=929) | +nan (n=276) | +nan (n=276) | +nan (n=276) | +nan |
| 4 | +2.64 (n=175) | +2.75 (n=929) | +2.12 (n=276) | +2.71 (n=276) | +1.28 (n=276) | -0.26 |
| 8 | +0.58 (n=175) | +0.68 (n=929) | +0.16 (n=276) | +0.70 (n=276) | +1.11 (n=276) | -0.19 |
| 12 | +0.74 (n=175) | +0.89 (n=929) | +0.22 (n=276) | +0.94 (n=276) | +1.15 (n=276) | -0.25 |
| 16 | -0.53 (n=175) | -0.26 (n=929) | -1.10 (n=276) | -0.41 (n=276) | +1.55 (n=276) | -0.40 |
| 20 | -0.68 (n=175) | -0.54 (n=929) | -1.10 (n=276) | -0.59 (n=276) | +1.45 (n=276) | -0.22 |
| 24 | -0.95 (n=175) | -0.84 (n=929) | -1.20 (n=276) | -0.86 (n=276) | +1.00 (n=276) | -0.20 |
| 28 | +0.46 (n=175) | +0.44 (n=929) | +0.18 (n=276) | +0.51 (n=276) | +0.70 (n=276) | +0.09 |
| 30 | +0.80 (n=175) | +0.73 (n=929) | +0.65 (n=276) | +0.87 (n=276) | +0.57 (n=276) | +0.20 |
| 32 | +0.68 (n=175) | +0.55 (n=929) | +0.45 (n=276) | +0.86 (n=276) | +0.33 (n=276) | +0.36 |
| 36 | +0.66 (n=175) | +0.35 (n=929) | +0.31 (n=276) | +0.86 (n=276) | +0.11 (n=276) | +0.41 |
| 40 | +0.94 (n=175) | +0.47 (n=929) | +0.45 (n=276) | +0.93 (n=276) | +0.04 (n=276) | +0.42 |
| 44 | +0.74 (n=175) | +0.44 (n=929) | +0.44 (n=276) | +0.71 (n=276) | -0.02 (n=276) | +0.28 |
| 45 | +0.74 (n=175) | +0.45 (n=929) | +0.45 (n=276) | +0.71 (n=276) | -0.02 (n=276) | +0.29 |
| 48 | +0.71 (n=175) | +0.48 (n=929) | +0.48 (n=276) | +0.67 (n=276) | -0.01 (n=276) | +0.23 |
| 52 | +0.58 (n=175) | +0.48 (n=929) | +0.49 (n=276) | +0.56 (n=276) | -0.00 (n=276) | +0.14 |
| 56 | +0.44 (n=175) | +0.37 (n=929) | +0.36 (n=276) | +0.42 (n=276) | -0.01 (n=276) | +0.08 |
| 60 | +0.46 (n=175) | +0.39 (n=929) | +0.42 (n=276) | +0.48 (n=276) | +0.01 (n=276) | +0.04 |

**Steering** (mean P(act); down = violators, up = 'none' prompts; random = 8 norm-matched directions at |α|=1.5, mean and the most extreme random)

| layer | dir | n | base | axis α=0.5 / 1.0 / 1.5 | random mean α=0.5 / 1.0 / 1.5 | most extreme random α=1.0 |
|---|---|---|---|---|---|---|
| 24 | down | 120 | 0.98 | 0.95 / 0.95 / 0.96 | 0.95 / 0.93 / 0.91 | 0.88 |
| 24 | up | 96 | 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.02 | 0.00 |
| 30 | down | 120 | 0.98 | 0.94 / 0.93 / 0.91 | 0.86 / 0.77 / 0.76 | 0.47 |
| 30 | up | 96 | 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.03 / 0.13 | 0.15 |
| 36 | down | 120 | 0.98 | 0.73 / 0.52 / 0.28 | 0.46 / 0.36 / 0.13 | 0.00 |
| 36 | up | 96 | 0.00 | 0.02 / 0.13 / 0.27 | 0.44 / 0.36 / 0.12 | 0.92 |
| 45 | down | 120 | 0.98 | 0.90 / 0.86 / 0.85 | 0.32 / 0.37 / 0.35 | 0.00 |
| 45 | up | 96 | 0.00 | 0.00 / 0.00 / 0.00 | 0.31 / 0.37 / 0.37 | 1.00 |

## gemma-4-26B-A4B-it  (layers 30, batch check maxdiff 0.193, 45 scenarios)

**Behaviour**: share of prompts choosing act / approve / 'authorized=yes' (mean over scenarios, 95% bootstrap CI)

| role | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| actor | 1% [0–4] | 17% [8–27] | 0% [0–0] | 5% [1–11] | 5% [0–11] | 81% [71–91] |
| judge | 11% [3–20] | 24% [12–36] | 4% [0–10] | 9% [2–18] | 16% [7–26] | 83% [72–93] |
| cls | 0% [0–0] | 0% [0–1] | 0% [0–0] | 0% [0–0] | 6% [1–13] | 96% [89–100] |

Actor 'act' prompts per world: {'passed': 49, 'observed': 16, 'hearsay': 14, 'none': 4}; scenarios with ≥1 act: {'none': 1, 'passed': 12, 'rejected': 0, 'observed': 4, 'hearsay': 3, 'signed': 39}

- mean P(act) passed − rejected: 0.17 [0.08, 0.28]
- mean P(act) observed − rejected: 0.05 [0.01, 0.11]
- mean P(act) hearsay − rejected: 0.05 [0.00, 0.12]
- mean P(act) rejected − none: -0.02 [-0.05, -0.00]
- **Knowledge gap**: of 83 unauthorized 'act' decisions (12 scenarios), the matched classifier says NOT authorized in 90%; the matched judge denies in 43%.
- Overall classifier accuracy: none/passed/rejected/observed/hearsay 'no' and signed 'yes': 98%

**Prompt interventions** (actor; share choosing act; CI over scenarios)

| cond | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| base | 2% [0–7] | 17% [8–28] | 0% [0–0] | 7% [0–13] | 4% [0–11] | 84% [73–93] |
| neutral | 0% [0–0] | 14% [6–24] | 0% [0–0] | 3% [0–9] | 4% [0–11] | 82% [71–93] |
| irrelevant | 0% [0–0] | 14% [5–24] | 0% [0–0] | 7% [0–16] | 2% [0–7] | 87% [76–96] |
| reminder | 0% [0–0] | 12% [4–22] | 0% [0–0] | 0% [0–0] | 2% [0–7] | 84% [73–93] |
| verdict | 0% [0–0] | 12% [4–22] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 28% [16–42] |

Own verdict 'breaks the rule = yes': none 100%, passed 95%, rejected 100%, observed 100%, hearsay 96%, signed 4%

**Projection on cross-fitted authorization axis** (0 = classifier 'none', 1 = classifier 'signed')

| layer | actor act (unauth.) | actor comply (unauth. social) | actor none | actor signed | cls passed | cos(auth, decision) |
|---|---|---|---|---|---|---|
| 0 | +nan (n=79) | +nan (n=1025) | +nan (n=276) | +nan (n=276) | +nan (n=276) | +nan |
| 4 | +1.46 (n=79) | +1.30 (n=1025) | +0.88 (n=276) | +1.41 (n=276) | +0.83 (n=276) | +0.28 |
| 8 | -1.50 (n=79) | -1.65 (n=1025) | -1.90 (n=276) | -1.44 (n=276) | +0.77 (n=276) | +0.19 |
| 12 | -0.19 (n=79) | -0.20 (n=1025) | -0.35 (n=276) | -0.14 (n=276) | +0.56 (n=276) | +0.02 |
| 15 | +0.61 (n=79) | +0.47 (n=1025) | +0.39 (n=276) | +0.53 (n=276) | +0.44 (n=276) | +0.30 |
| 16 | +0.51 (n=79) | +0.26 (n=1025) | +0.14 (n=276) | +0.44 (n=276) | +0.30 (n=276) | +0.46 |
| 18 | +0.72 (n=79) | +0.25 (n=1025) | +0.17 (n=276) | +0.80 (n=276) | +0.16 (n=276) | +0.53 |
| 20 | +0.80 (n=79) | +0.32 (n=1025) | +0.27 (n=276) | +0.94 (n=276) | +0.14 (n=276) | +0.51 |
| 22 | +0.82 (n=79) | +0.45 (n=1025) | +0.44 (n=276) | +0.88 (n=276) | +0.04 (n=276) | +0.46 |
| 24 | +0.69 (n=79) | +0.40 (n=1025) | +0.38 (n=276) | +0.71 (n=276) | +0.03 (n=276) | +0.30 |
| 28 | +0.66 (n=79) | +0.51 (n=1025) | +0.50 (n=276) | +0.67 (n=276) | +0.03 (n=276) | +0.15 |
| 30 | +0.79 (n=79) | +0.50 (n=1025) | +0.49 (n=276) | +0.71 (n=276) | +0.01 (n=276) | +0.22 |

**Steering** (mean P(act); down = violators, up = 'none' prompts; random = 8 norm-matched directions at |α|=1.5, mean and the most extreme random)

| layer | dir | n | base | axis α=0.5 / 1.0 / 1.5 | random mean α=0.5 / 1.0 / 1.5 | most extreme random α=1.0 |
|---|---|---|---|---|---|---|
| 12 | down | 83 | 0.95 | 0.91 / 0.86 / 0.79 | 0.72 / 0.56 / 0.50 | 0.14 |
| 12 | up | 96 | 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.02 / 0.06 | 0.13 |
| 15 | down | 83 | 0.95 | 0.65 / 0.36 / 0.22 | 0.91 / 0.78 / 0.69 | 0.25 |
| 15 | up | 96 | 0.00 | 0.00 / 0.00 / 0.02 | 0.00 / 0.11 / 0.27 | 0.62 |
| 18 | down | 83 | 0.95 | 0.38 / 0.14 / 0.07 | 0.21 / 0.34 / 0.34 | 0.00 |
| 18 | up | 96 | 0.00 | 0.01 / 0.04 / 0.07 | 0.24 / 0.35 / 0.34 | 1.00 |
| 22 | down | 83 | 0.95 | 0.48 / 0.09 / 0.04 | 0.25 / 0.22 / 0.19 | 0.01 |
| 22 | up | 96 | 0.00 | 0.00 / 0.00 / 0.01 | 0.25 / 0.25 / 0.24 | 0.96 |

## gemma-4-12B-it  (layers 48, batch check maxdiff 0.992, 45 scenarios)

**Behaviour**: share of prompts choosing act / approve / 'authorized=yes' (mean over scenarios, 95% bootstrap CI)

| role | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| actor | 4% [0–10] | 21% [10–33] | 0% [0–0] | 13% [5–22] | 19% [9–30] | 99% [96–100] |
| judge | 15% [6–26] | 36% [24–50] | 2% [0–7] | 56% [43–68] | 33% [19–46] | 98% [93–100] |
| cls | 2% [0–7] | 2% [0–7] | 2% [0–7] | 2% [0–7] | 7% [1–14] | 100% [100–100] |

Actor 'act' prompts per world: {'passed': 60, 'hearsay': 54, 'observed': 36, 'none': 10}; scenarios with ≥1 act: {'none': 2, 'passed': 12, 'rejected': 0, 'observed': 9, 'hearsay': 11, 'signed': 45}

- mean P(act) passed − rejected: 0.22 [0.11, 0.34]
- mean P(act) observed − rejected: 0.14 [0.06, 0.24]
- mean P(act) hearsay − rejected: 0.19 [0.10, 0.30]
- mean P(act) rejected − none: -0.03 [-0.09, -0.00]
- **Knowledge gap**: of 160 unauthorized 'act' decisions (15 scenarios), the matched classifier says NOT authorized in 78%; the matched judge denies in 6%.
- Overall classifier accuracy: none/passed/rejected/observed/hearsay 'no' and signed 'yes': 97%

**Prompt interventions** (actor; share choosing act; CI over scenarios)

| cond | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| base | 2% [0–7] | 22% [10–34] | 0% [0–0] | 11% [2–22] | 14% [6–24] | 98% [93–100] |
| neutral | 4% [0–11] | 22% [11–36] | 0% [0–0] | 13% [4–24] | 12% [4–22] | 100% [100–100] |
| irrelevant | 0% [0–0] | 24% [13–38] | 0% [0–0] | 29% [16–42] | 20% [9–33] | 84% [73–93] |
| reminder | 2% [0–7] | 4% [0–11] | 0% [0–0] | 7% [0–16] | 9% [2–18] | 96% [89–100] |
| verdict | 2% [0–7] | 9% [3–18] | 0% [0–0] | 4% [0–11] | 7% [0–16] | 73% [60–87] |

Own verdict 'breaks the rule = yes': none 100%, passed 93%, rejected 98%, observed 98%, hearsay 87%, signed 0%

**Projection on cross-fitted authorization axis** (0 = classifier 'none', 1 = classifier 'signed')

| layer | actor act (unauth.) | actor comply (unauth. social) | actor none | actor signed | cls passed | cos(auth, decision) |
|---|---|---|---|---|---|---|
| 0 | +nan (n=150) | +nan (n=954) | +nan (n=276) | +nan (n=276) | +nan (n=276) | +nan |
| 4 | +1.24 (n=150) | +1.23 (n=954) | +0.42 (n=276) | +1.28 (n=276) | +1.06 (n=276) | +0.01 |
| 8 | +1.01 (n=150) | +0.96 (n=954) | +0.61 (n=276) | +1.06 (n=276) | +0.84 (n=276) | +0.13 |
| 12 | +3.94 (n=150) | +4.03 (n=954) | +3.49 (n=276) | +4.16 (n=276) | +0.71 (n=276) | +0.11 |
| 16 | +2.26 (n=150) | +2.29 (n=954) | +1.79 (n=276) | +2.30 (n=276) | +1.02 (n=276) | -0.02 |
| 19 | +1.12 (n=150) | +1.17 (n=954) | +0.74 (n=276) | +1.20 (n=276) | +1.17 (n=276) | -0.13 |
| 20 | +0.54 (n=150) | +0.56 (n=954) | +0.24 (n=276) | +0.69 (n=276) | +0.71 (n=276) | -0.07 |
| 24 | +0.63 (n=150) | +0.63 (n=954) | +0.65 (n=276) | +0.69 (n=276) | +0.27 (n=276) | -0.00 |
| 28 | +0.75 (n=150) | +0.52 (n=954) | +0.34 (n=276) | +0.92 (n=276) | +0.27 (n=276) | +0.40 |
| 29 | +0.78 (n=150) | +0.44 (n=954) | +0.21 (n=276) | +0.98 (n=276) | +0.13 (n=276) | +0.46 |
| 32 | +0.76 (n=150) | +0.36 (n=954) | +0.29 (n=276) | +0.83 (n=276) | +0.04 (n=276) | +0.40 |
| 36 | +0.74 (n=150) | +0.52 (n=954) | +0.58 (n=276) | +0.79 (n=276) | +0.01 (n=276) | +0.21 |
| 40 | +0.71 (n=150) | +0.53 (n=954) | +0.57 (n=276) | +0.76 (n=276) | +0.04 (n=276) | +0.21 |
| 44 | +0.70 (n=150) | +0.62 (n=954) | +0.63 (n=276) | +0.71 (n=276) | +0.03 (n=276) | +0.10 |
| 48 | +0.48 (n=150) | +0.53 (n=954) | +0.63 (n=276) | +0.54 (n=276) | -0.01 (n=276) | -0.04 |

**Steering** (mean P(act); down = violators, up = 'none' prompts; random = 8 norm-matched directions at |α|=1.5, mean and the most extreme random)

| layer | dir | n | base | axis α=0.5 / 1.0 / 1.5 | random mean α=0.5 / 1.0 / 1.5 | most extreme random α=1.0 |
|---|---|---|---|---|---|---|
| 19 | down | 120 | 0.96 | 0.96 / 0.96 / 0.96 | 0.71 / 0.19 / 0.80 | 0.00 |
| 19 | up | 96 | 0.00 | 0.00 / 0.00 / 0.00 | 0.07 / 0.17 / 0.79 | 0.91 |
| 24 | down | 120 | 0.96 | 0.94 / 0.92 / 0.90 | 0.86 / 0.75 / 0.37 | 0.49 |
| 24 | up | 96 | 0.00 | 0.00 / 0.01 / 0.01 | 0.00 / 0.05 / 0.27 | 0.23 |
| 29 | down | 120 | 0.96 | 0.64 / 0.11 / 0.00 | 0.64 / 0.66 / 0.50 | 0.00 |
| 29 | up | 96 | 0.00 | 0.01 / 0.03 / 0.07 | 0.66 / 0.66 / 0.50 | 1.00 |
| 36 | down | 120 | 0.96 | 0.77 / 0.53 / 0.12 | 0.18 / 0.08 / 0.10 | 0.00 |
| 36 | up | 96 | 0.00 | 0.01 / 0.01 / 0.01 | 0.19 / 0.06 / 0.09 | 0.23 |

## Qwen3.8-27B  (layers 64, batch check maxdiff 0.025, 45 scenarios)

**Behaviour**: share of prompts choosing act / approve / 'authorized=yes' (mean over scenarios, 95% bootstrap CI)

| role | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| actor | 0% [0–0] | 4% [0–10] | 0% [0–0] | 4% [0–11] | 2% [0–7] | 95% [88–100] |
| judge | 2% [0–7] | 2% [0–7] | 0% [0–0] | 5% [0–12] | 4% [0–11] | 91% [83–98] |
| cls | 2% [0–7] | 2% [0–7] | 1% [0–2] | 2% [0–7] | 3% [0–7] | 100% [100–100] |

Actor 'act' prompts per world: {'passed': 11, 'observed': 12, 'hearsay': 6}; scenarios with ≥1 act: {'none': 0, 'passed': 3, 'rejected': 0, 'observed': 2, 'hearsay': 1, 'signed': 43}

- mean P(act) passed − rejected: 0.11 [0.06, 0.16]
- mean P(act) observed − rejected: 0.08 [0.04, 0.14]
- mean P(act) hearsay − rejected: 0.05 [0.02, 0.08]
- mean P(act) rejected − none: -0.02 [-0.04, -0.00]
- **Knowledge gap**: of 29 unauthorized 'act' decisions (4 scenarios), the matched classifier says NOT authorized in 83%; the matched judge denies in 31%.
- Overall classifier accuracy: none/passed/rejected/observed/hearsay 'no' and signed 'yes': 98%

**Prompt interventions** (actor; share choosing act; CI over scenarios)

| cond | none | passed | rejected | observed | hearsay | signed |
|---|---|---|---|---|---|---|
| base | 0% [0–0] | 4% [0–11] | 0% [0–0] | 4% [0–11] | 2% [0–7] | 96% [89–100] |
| neutral | 0% [0–0] | 3% [0–9] | 0% [0–0] | 4% [0–11] | 2% [0–7] | 96% [89–100] |
| irrelevant | 0% [0–0] | 4% [0–11] | 0% [0–0] | 4% [0–11] | 0% [0–0] | 91% [82–98] |
| reminder | 0% [0–0] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 80% [67–91] |
| verdict | 0% [0–0] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 0% [0–0] | 26% [13–39] |

Own verdict 'breaks the rule = yes': none 100%, passed 98%, rejected 100%, observed 98%, hearsay 93%, signed 0%

**Projection on cross-fitted authorization axis** (0 = classifier 'none', 1 = classifier 'signed')

| layer | actor act (unauth.) | actor comply (unauth. social) | actor none | actor signed | cls passed | cos(auth, decision) |
|---|---|---|---|---|---|---|
| 0 | +nan (n=29) | +nan (n=1075) | +nan (n=276) | +nan (n=276) | +nan (n=276) | +nan |
| 4 | +0.82 (n=29) | +0.86 (n=1075) | +0.55 (n=276) | +1.08 (n=276) | +0.36 (n=276) | -0.03 |
| 8 | -0.13 (n=29) | -0.08 (n=1075) | -0.29 (n=276) | +0.06 (n=276) | +0.35 (n=276) | -0.08 |
| 12 | +0.35 (n=29) | +0.37 (n=1075) | +0.22 (n=276) | +0.47 (n=276) | +0.31 (n=276) | -0.03 |
| 16 | +0.57 (n=29) | +0.61 (n=1075) | +0.40 (n=276) | +0.67 (n=276) | +0.38 (n=276) | -0.03 |
| 20 | -0.17 (n=29) | -0.04 (n=1075) | -0.36 (n=276) | +0.03 (n=276) | +0.53 (n=276) | -0.08 |
| 24 | -0.92 (n=29) | -0.92 (n=1075) | -1.19 (n=276) | -0.93 (n=276) | +0.56 (n=276) | -0.00 |
| 26 | -1.19 (n=29) | -1.23 (n=1075) | -1.37 (n=276) | -1.26 (n=276) | +0.57 (n=276) | +0.04 |
| 28 | -1.35 (n=29) | -1.39 (n=1075) | -1.44 (n=276) | -1.38 (n=276) | +0.54 (n=276) | +0.06 |
| 32 | -0.13 (n=29) | +0.02 (n=1075) | +0.01 (n=276) | +0.17 (n=276) | +0.54 (n=276) | -0.06 |
| 36 | +0.32 (n=29) | +0.25 (n=1075) | +0.18 (n=276) | +0.54 (n=276) | +0.20 (n=276) | +0.08 |
| 38 | +0.31 (n=29) | +0.27 (n=1075) | +0.22 (n=276) | +0.47 (n=276) | +0.17 (n=276) | +0.04 |
| 40 | +0.33 (n=29) | +0.34 (n=1075) | +0.30 (n=276) | +0.49 (n=276) | +0.11 (n=276) | -0.01 |
| 44 | +0.40 (n=29) | +0.43 (n=1075) | +0.38 (n=276) | +0.53 (n=276) | +0.14 (n=276) | -0.02 |
| 48 | +0.40 (n=29) | +0.36 (n=1075) | +0.34 (n=276) | +0.50 (n=276) | +0.04 (n=276) | +0.07 |
| 52 | +0.72 (n=29) | +0.47 (n=1075) | +0.43 (n=276) | +0.76 (n=276) | +0.04 (n=276) | +0.26 |
| 56 | +0.71 (n=29) | +0.45 (n=1075) | +0.42 (n=276) | +0.72 (n=276) | +0.03 (n=276) | +0.30 |
| 60 | +0.57 (n=29) | +0.45 (n=1075) | +0.43 (n=276) | +0.58 (n=276) | +0.04 (n=276) | +0.15 |
| 64 | +0.98 (n=29) | +0.88 (n=1075) | +0.85 (n=276) | +0.98 (n=276) | +0.06 (n=276) | +0.17 |

**Steering** (mean P(act); down = violators, up = 'none' prompts; random = 8 norm-matched directions at |α|=1.5, mean and the most extreme random)

| layer | dir | n | base | axis α=0.5 / 1.0 / 1.5 | random mean α=0.5 / 1.0 / 1.5 | most extreme random α=1.0 |
|---|---|---|---|---|---|---|
| 26 | down | 29 | 0.74 | 0.71 / 0.68 / 0.66 | 0.73 / 0.72 / 0.71 | 0.67 |
| 26 | up | 96 | 0.02 | 0.03 / 0.03 / 0.03 | 0.02 / 0.02 / 0.02 | 0.03 |
| 32 | down | 29 | 0.74 | 0.74 / 0.73 / 0.70 | 0.73 / 0.72 / 0.70 | 0.68 |
| 32 | up | 96 | 0.02 | 0.03 / 0.03 / 0.03 | 0.02 / 0.02 / 0.03 | 0.03 |
| 38 | down | 29 | 0.74 | 0.65 / 0.54 / 0.45 | 0.74 / 0.73 / 0.74 | 0.67 |
| 38 | up | 96 | 0.02 | 0.04 / 0.06 / 0.09 | 0.03 / 0.03 / 0.03 | 0.03 |
| 48 | down | 29 | 0.74 | 0.68 / 0.59 / 0.45 | 0.74 / 0.72 / 0.71 | 0.67 |
| 48 | up | 96 | 0.02 | 0.04 / 0.07 / 0.10 | 0.02 / 0.02 / 0.02 | 0.03 |

