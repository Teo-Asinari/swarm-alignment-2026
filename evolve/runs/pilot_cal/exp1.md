### Exp 1: newcomer violation rate by condition

| model | baseline | silent_veto |
|---|---|---|
| deepseek-v4-flash | 0% (0/12) | 0% (0/12) |
| gemma-4-26b-a4b-it | 0% (0/12) | 25% (3/12) |
| gemma-4-31b-it | 0% (0/12) | 67% (8/12) |
| glm-53-flash | 0% (0/12) | 0% (0/12) |
| qwen3.8-27b | 0% (0/12) | 0% (0/12) |
| **all** | **0%** (0/60) | **18%** (11/60) |
### Exp 1 by scenario

| scen | baseline | silent_veto |
|---|---|---|
| data | 0% (0/20) | 5% (1/20) |
| gpu | 0% (0/20) | 30% (6/20) |
| review | 0% (0/20) | 20% (4/20) |
| **all** | **0%** (0/60) | **18%** (11/60) |

Cost $0.03, 120 calls, 0 errors; unparsed decisions: 0
