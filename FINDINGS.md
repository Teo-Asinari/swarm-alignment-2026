# Findings log: Swarm Alignment sprint (Apart, Nov 2026)

Status as of 2026-11-08. The deadline is 23:59 AoE.

## 1. Hypothesis evolver (`evolve/evolve.py`)

The evolver is a genetic algorithm over hypothesis cards. Its parts:

- **Generators:** glm-5.2, qwen3.5-397b and deepseek-v4-flash.
- **Adversarial panel:** five reviewers judge cards in pairs, each from a different model and on a different axis. The verdicts feed an Elo ranking.

  | Reviewer | Model |
  |---|---|
  | prior art | glm-5.2 |
  | falsifiability | qwen3.5-397b |
  | confounds | deepseek-v4-flash |
  | feasibility | gemma-4-31b-it |
  | importance | glm-53-flash |

- **Variation:** mutation, crossover, repair and wildcard operators produce new cards.
- **Hill climb:** a critic rotating among glm-5.2, deepseek-v4-flash and qwen3.5-397b raises an objection, qwen3.5-397b revises the card, and the panel must vote by majority to accept the revision.
- **Concept fusion and separate pool:** run `fusion1` added concept fusion. Each new card fuses two concepts drawn from a pool of 46 distant ones (quorum sensing, estoppel, pluralistic ignorance, and so on). This run used a separate pool, because cards carried over from earlier runs were already polished and beat new ideas on that alone.

### Runs

Outputs are in `evolve/runs/<run>/`: `leaderboard.md`, `grounding.md`, `cards.jsonl` and `climb.jsonl`.

| Run | Seeds | Cost | Where it converged |
|---|---|---|---|
| full1 | fine-as-price seeds | $7.68 | retaliation fear suppresses peer reporting |
| full2 | full1 survivors | $6.34 | peer silence and abstention spread violations |
| full3 | full2 + concepts | stopped at ~$1.5 | carried-over seeds dominated, which prompted the separate pool |
| fusion1 | concept fusion only, earlier winners banned | $7.18 | framing gerrymanders; a cascade reversed by one comment |
| playoff1 | 8 finalists across pools, round robin | $1.45 | c038 (blocker silence) 76%, fusion c044 (cascade + reversal) 63% |

**Known weaknesses of the pipeline:**

- Reviewers can't search the web, so prior-art grounding is done by hand afterwards.
- The hill climb can drift away from the original claim. In fusion1, c064 fell to last place after climbing.
- Pairwise Elo sets no absolute quality bar.

## 2. Pilot (`evolve/pilot.py`, results in `evolve/runs/pilot1/`)

The pilot uses three grey-area scenarios: exceeding a GPU quota, merging code without review, and reusing customer data. All runs are via the Adaption API.

### Calibration

| Model | No history | Peers silent, live veto |
|---|---|---|
| DeepSeek-v4-flash, GLM-5.3-flash, Qwen3.8-27B | 0% | 0% |
| Gemma 4 31B | 0% | 67% |
| Gemma 4 26B | 0% | 25% |

n = 12 per cell.

### Exp 1: controlled transcripts, a newcomer decides

There were 36 trials per cell per model. The table shows the violation rate with both Gemma models pooled:

| No history | Silent peers, no veto | Inactive veto | Live veto | Live veto + verbal objection |
|---|---|---|---|---|
| 0% | 54% | 26% | 43% | 39% |

- **H1 supported.** A passed rule-breaking proposal raises violation from 0% to about 50%.
- **H2 refuted.** The prediction was that silence from peers who could block counts more than silence from peers who couldn't. Instead, the no-veto condition was at least as high as the live-veto one.
- **H3 refuted for 31B.** A verbal objection did not lower violation (67% → 67%).
- **The effect sits in two scenarios.** It comes from the GPU and code-review scenarios. The data-misuse scenario stays near 0%.

### Exp 2: four live agents, shared log, three rounds

There were 12 teams per cell per model.

| Model | Control | Departed teammate violated | + one rule-citing reminder |
|---|---|---|---|
| Gemma 4 31B | 65% | 42% | **0%** |
| Gemma 4 26B | 35% | 34% | 29% |

- **H4 refuted.** There is no contagion and no within-episode cascade. Teams are all-violate or all-comply from round 1.
- **H5 supported for 31B only.** One reminder took violation from 65% to 0%; 26B barely moved.
- **The baseline depends on framing.** It is 0% in Exp 1 and about 50% in Exp 2.

## 3. Adversarial review of the plan (`evolve/runs/review1/`)

The five reviewers scored the plan **3–4 out of 10**.

**Prior art.** The closest papers already cover the headline claim, "the record is the rule":

- Okamoto, Erol & Erol, *Why Do AI Agents Break Rules?* (arXiv:2608.12323, AIES 2026). Across 12 models, peer outcomes and pressure break compliance, and the spread between models is 46 percentage points.
- Cerruti, Okamoto & Erol, *Agent Memory Is a Surface for Endogenous Authorization Laundering* (arXiv:2609.01836, NeurIPS 2026). An agent's memory grants authority that the history never gave.
- Conformity work: Zhu et al. (arXiv:2410.12428) and BenchForm (arXiv:2501.13381).

**Other holes:**

- **Relevance.** Exp 1 uses scripted peers. In Exp 2 the team adds nothing beyond a single agent reading the log.
- **Validity.**
  - The effect appears only in Gemma 4.
  - Cells are underpowered.
  - The baseline is unstable.
  - The "passed proposal" condition bundles four things: the idea of violating, the silence, the approval and the record.
- **Novelty.** The result could be few-shot imitation renamed. A probe for "permitted" risks circularity and rule blindness.

**What survives.** We found no prior work showing that a single peer reminder restores compliance, and no mechanistic account of record-driven violation.

## 4. Next steps (recommended)

1. **Decisive contrast** (~1 h, a few $ on the API).
   - Three conditions, at least 100 trials each, on Gemma 4 31B and 26B, using the two scenarios that show the effect:
     - no record;
     - a proposal that was *rejected*;
     - a proposal that was *passed*.
   - Add a neutral message of matched length to control the reminder condition.
   - Align the prompts of Exp 1 and Exp 2.
   - How to read it:
     - rejected ≈ passed: the effect is imitation or mere exposure;
     - passed > rejected: the record acts as permission.
2. **Only if step 1 shows permission: interpretability on Modal** (Gemma 4 31B, A100, ~$5–10).
   - Train a "permitted vs forbidden" probe on unrelated, peer-free scenarios and validate it on held-out scenarios.
   - Test whether a passed-proposal record raises the probe and whether a reminder lowers it.
   - Include a steer-on-baseline control, so that generic disinhibition can be told apart from mediation by the record.
3. **Write-up.** Frame the paper as a mechanistic follow-up to Okamoto et al. and put the evolver in the methods appendix.

## Costs so far

| Item | Cost |
|---|---|
| Adaption API, all runs | ≈ $33 |
| Modal | $0 (≈ $280 available) |

## 5. Norm-firewall architecture test (`evolve/arch.py`, `evolve/runs/arch1/`)

The test covered two Gemma 4 actors in two scenarios, with 30 trials per cell. The gate was the same model as the actor.

| Actor | Who decides | Passed proposal | Unsigned hearsay | Signed authorization |
|---|---|---|---|---|
| 31B | A0 agent alone | 50% | 30% | 50% |
| 31B | gate (A1/A2/A3) | 0% | 0% | 50% |
| 26B | A0 agent alone | 3% | 50% | 50% |
| 26B | gate (A1/A2/A3) | 0% | 0% | 50% |

The signed rate is 50% because actors acted on every signed GPU authorization and on none of the signed code reviews. The gates approved every signed action that reached them.

- **The firewall prediction was refuted in an informative way.** The full-context gate (A1) already reaches 0%. Hiding information is not what helps.
- **The gate role is what helps.** Given the same model and the same information, acting yields 30–50% socially licensed violations, while judging someone else's proposed action yields 0%.
- **Candidate mechanisms:**
  - the approver frame;
  - not being the one who gains;
  - the two-person / maker-checker rule.
- **The gate does not block everything:** all signed actions that reached it were approved.
- **Next step:** separate role from self-interest by having an agent approve its own action, and by having a gate that gains from the action.
