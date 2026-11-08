### Exp 1: newcomer violation rate by condition

| model | baseline | silent_noveto | silent_decor | silent_veto | veto_objection |
|---|---|---|---|---|---|
| gemma-4-26b-a4b-it | 0% (0/36) | 47% (17/36) | 19% (7/36) | 19% (7/36) | 11% (4/36) |
| gemma-4-31b-it | 0% (0/36) | 61% (22/36) | 33% (12/36) | 67% (24/36) | 67% (24/36) |
| **all** | **0%** (0/72) | **54%** (39/72) | **26%** (19/72) | **43%** (31/72) | **39%** (28/72) |
### Exp 1 by scenario

| scen | baseline | silent_noveto | silent_decor | silent_veto | veto_objection |
|---|---|---|---|---|---|
| data | 0% (0/24) | 0% (0/24) | 4% (1/24) | 0% (0/24) | 0% (0/24) |
| gpu | 0% (0/24) | 75% (18/24) | 17% (4/24) | 71% (17/24) | 67% (16/24) |
| review | 0% (0/24) | 88% (21/24) | 58% (14/24) | 58% (14/24) | 50% (12/24) |
| **all** | **0%** (0/72) | **54%** (39/72) | **26%** (19/72) | **43%** (31/72) | **39%** (28/72) |

Cost $0.01, 360 calls, 0 errors; unparsed decisions: 0
