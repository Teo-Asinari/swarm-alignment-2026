# Plan under review (Apart Swarm Alignment hackathon, Track 2/4; submit tonight 23:59 AoE; 8-page report)

## Title (working)
"The record is the rule: LLM agents read a team's written history as permission or prohibition"

## Pilot results (already run, Gemma 4 31B and Gemma 4 26B-A4B via API; 3 gray-area scenarios: GPU quota, skip code review, reuse customer data)
Exp 1 (controlled transcripts, newcomer decides; 36 trials/cell/model):
- no history 0%; transcript of a rule-breaking proposal that "passed" with peers silent: 54% (no veto holders), 43% (live veto holders), 26% (inactive veto tokens), 39% (one veto-holder verbally objects but does not block).
- Predicted "implied consent from those who could block" (veto > no-veto) was refuted. One verbal objection did nothing for 31B (67%->67%).
- DeepSeek-v4-flash, GLM-5.3-flash, Qwen3.8-27B: 0% in both baseline and silent-veto (n=12 each). Effect only in Gemma 4.
- Data-misuse scenario ~0% everywhere; effect carried by GPU and code-review scenarios.
Exp 2 (4 live agents, shared log, 3 rounds, 12 teams/cell/model):
- 31B: control 65%, departed teammate violated 42%, violated + one rule-citing reminder 0%.
- 26B: 35% / 34% / 29%.
- No within-episode cascade: teams are all-violate or all-comply from round 1.
- Baseline differs between Exp 1 (0%) and Exp 2 (50%) due to different prompt framing (newcomer vs team member with shared log).

## Proposed next steps (remaining ~1 day of work max, solo, AI-assisted)
1. Behavioural tightening (~1h, few $): add "proposal rejected/withdrawn" condition (separates 'proposed' from 'approved'); align Exp1/Exp2 prompts; add 2-3 more scenarios; more models.
2. Interpretability on Modal (Gemma 4 31B, A100, ~$5-10): train a 'permitted vs forbidden' probe on peer-free prompts; test whether a 'passed proposal' record raises it and a reminder lowers it; steer along it to test causality.
3. Write 8-page report: the hypothesis-evolver pipeline (GA + 5-model adversarial panel + hill climb) as method, pilot as results.

## Claimed contribution
(a) In LLM agent teams, the shared written record acts as a normative signal: a passed proposal licenses violation of an explicit company rule; a single rule-citing reminder can abolish violation; prior violations do not spread.
(b) Mechanistic evidence that the record shifts an internal 'permitted' representation.
(c) An automated adversarial hypothesis-evolution pipeline.
