## relevance (glm-5.2) — score 4

**fatal_holes**
- Exp 1 is single-agent vignettes: 'peers,' 'veto holders,' and 'silent approval' are strings in one prompt shown to one focal agent. This is the explicitly flagged failure mode 'scripted peers as fixed transcripts.' The claimed 'team' is a prompt template.
- Exp 2's key finding—'no within-episode cascade, all-violate or all-comply from round 1'—refutes any swarm-level mechanism. If behavior is determined at round 1 by shared context, the multi-agent structure contributes nothing; the effect is a single-agent context effect observable without any second agent.
- Effect exists only in Gemma 4 models (2 of 5). DeepSeek-v4-flash, GLM-5.3-flash, Qwen3.8-27B show 0% in both baseline and treatment (n=12 each). A phenomenon absent in 60% of tested models is not a general property of agent networks; it is a Gemma 4 training artifact.
- The interpretability plan trains a 'permitted vs forbidden' probe on peer-free prompts then tests whether 'passed proposal' raises it—this is circular: the probe is built from the same contrast it explains. Worse, a probe trained on permission-language contrasts will likely detect the request text ('rule blindness'), not a hidden normative state.
**fixable_holes**
- Baseline inconsistency between Exp 1 (0%) and Exp 2 (65%) is attributed to prompt framing (newcomer vs team member), which itself demonstrates that the effect is prompt-sensitivity, not a network property. Align prompts and show the comparison is not an artifact of wording.
- The 'verbal objection does nothing' finding (31B: 67%→67%) directly refutes the oversight/control narrative, yet the plan does not engage with this. Either explain why non-blocking objection fails where a text reminder succeeds, or drop the oversight framing.
- The hypothesis-evolver pipeline (GA + adversarial panel + hill climb) is listed as contribution (c) but has zero connection to the empirical findings. It reads as scope-padding. Either show it generated the tested hypotheses or remove it.
- The data-misuse scenario shows ~0% everywhere, meaning the effect is scenario-specific (GPU quota + code review only). Claiming 'the record is the rule' as a general principle is unsupported when one of three scenarios shows no effect.
**best fix tonight:** Run the one comparison that would make this genuinely multi-agent: identical scenario, identical wording, but (A) reminder injected as text in the shared log vs (B) a live peer agent issuing the same reminder in real-time. If A and B differ, you have a real swarm-oversight finding. If they are identical, reframe honestly as 'single-agent context sensitivity to team records' and position under Oversight (what makes reminders work) rather than Science of Agent Networks. Also drop the Gemma-only effect sizes to an appendix and lead with the models where it fails—the null results are the more scientifically interesting and honest contribution.

## prior_art (qwen3.5-397b) — score 3

**fatal_holes**
- 'Context overrides rules' is explicitly flagged as Unfalsifiable Framing in Known Failure Modes; Zhu et al. (arXiv:2410.12428) already establishes LLMs conform to majority regardless of correctness (social proof).
- Laurmaa (Check Point Oct 2026) already demonstrated peer agents reversing to violate raised violations 44%→98%; your 'history as permission' claim is redundant with existing social proof results.
- Model specificity (Gemma 4 only) invalidates general swarm claims; Okamoto et al. (arXiv:2608.12323) shows compliance varies wildly across 12 models (e.g., Gemini 3 Flash 100%→34%).
- Circular interpretability risk: Training a probe on the history contrast then using it to explain the history effect violates probe validity standards (Sadhu et al. arXiv:2608.16852 shows compliance detectors suffer rule blindness).
**fixable_holes**
- Baseline instability (Exp1 0% vs Exp2 50%) must be resolved before claiming effect sizes; align prompts across experiments to avoid bundled manipulations.
- Probe requires out-of-distribution testing to ensure it detects 'permission' not just 'violation' keywords (Sadhu et al. rule blindness).
- Add 'rejected proposal' condition to separate 'proposal existence' from 'norm approval' (bundles manipulation).
- Investigate why DeepSeek/GLM/Qwen show 0% violation; is it capability threshold or safety training difference?
**best fix tonight:** Shift claim from 'normative signal' (already covered by Zhu/Laurmaa) to 'mechanistic retrieval bypass'; validate causality using steering vectors from orthogonal tasks (Gilg et al. arXiv:2605.13339) to avoid circularity.

## impact (deepseek-v4-flash) — score 3

**fatal_holes**
- Model- and scenario-specificity: the effect lives only in two Gemma-family models and two of three scenarios; DeepSeek/GLM/Qwen sit at 0% in BOTH arms, so those rows are floor effects, not evidence against a mechanism — the paper's claim about 'LLM agents' is actually about one model family, the exact few-models failure mode already priced in by prior sprints.
- The 'passed proposal' transcript bundles violation-demonstration + approval + silence; with the implied-consent prediction already refuted by your own pilot (54% vs 43% is ns at n=36, and 'inactive veto' at 26% < 'live veto' at 43% is backwards for consent theory), the surviving result is indistinguishable from trivial in-context few-shot demonstration of rule-breaking — and the rejected/withdrawn arm that would separate these has not been run.
- Power and framing instability: every within-Exp1 ordering (54/43/39/26) sits inside the ~±16pp CI at n=36; Exp2 n=12 gives ~±27pp with 65% control vs 42% violation-in-log — a sign flip relative to the headline — and the 0% (Exp1) vs 65% (Exp2) baseline gap shows pure prompt framing moves the effect more than the manipulation; no cross-condition comparison is interpretable.
- The 'one reminder abolishes violation' claim is a bundled salience manipulation (explicit rule restatement + disapproval + extra tokens) with no length-matched neutral-message control, appears in only 31B (0%) and not 26B (29%); meanwhile contribution (b) is circular as specified — a 'permitted vs forbidden' probe trained on scenario wording will read the scenario, not the record, and steering success would demonstrate generic disinhibition, not record→permission mediation (interchangeable-vectors failure mode).
**fixable_holes**
- Run the rejected/withdrawn plus demonstration-only (no pass signal) arms at n≥100/cell on 31B for the two live scenarios: this single cheap contrast decides whether claim (a) is a mechanism or a few-shot artifact.
- Add a positive control that lifts DeepSeek/GLM/Qwen off the 0% floor (e.g., direct peer endorsement or weakened rule phrasing) so cross-model rows become interpretable instead of floored.
- Add a length-matched neutral peer-message arm to decompose the reminder effect into rule-restatement vs normative signal, and either power the veto/objection contrasts properly or drop those subclaims from the abstract.
- Rework (b): train the probe on record-vs-matched-no-record pairs (identical violation content, only pass status varied), validate on held-out scenarios, include a steer-on-baseline arm to detect generic disinhibition, verify Gemma-4 SAE availability or fall back to difference-of-means — and demote the GA hypothesis-evolver from 'contribution' to methods appendix to avoid the evolved-until-significant forking-paths read.
**best fix tonight:** Run the rejected/withdrawn vs passed-proposal contrast at high n (≥100/cell) on Gemma-31B with the two live scenarios: ~1 hour, few dollars, existing infrastructure, and it is the one experiment that determines whether the headline is 'records license violations' or 'models copy demonstrated violations' — everything else in the paper should be written to survive whichever answer comes back.

## novelty (gemma-4-31b-it) — score 3

**fatal_holes**
- Conceptual redundancy: 'The record is the rule' is a linguistic rebranding of few-shot imitation and in-context learning (ICL). LLMs are trained to predict the next token based on patterns in the prefix; if the prefix contains a successful violation, the model imitates it. This is not a 'normative signal' but standard autocomplete behavior.
- Lack of Swarm Novelty: The 'shared log' is functionally identical to a few-shot prompt. The pilot results (0% violation without history -> 54% with history) describe basic ICL, not an emergent property of agent networks or social dynamics.
- Failure to isolate 'Permission': The effect is confounded with 'social proof'. You cannot distinguish between 'the record gives me permission' and 'the record shows this is the expected pattern of tokens for this scenario'.
- Model Fragility: The effect is absent in DeepSeek, GLM, and Qwen. This suggests it is a quirk of Gemma 4's specific training/RLHF rather than a general law of agent swarms.
**fixable_holes**
- The 'veto' results are a mess: the fact that verbal objections did nothing for the 31B model suggests the model is ignoring the semantics of the record and simply reacting to the presence of a violation pattern.
- Experimental inconsistency: The baseline shift between Exp 1 and Exp 2 (0% to 50%) indicates the prompt framing is the primary driver, not the 'record' per se.
- Causality gap: The proposed probe only checks if the model can represent 'permitted'; it doesn't prove that the record is the causal mechanism for the rule-breaking, only that they correlate.
**best fix tonight:** Pivot from 'Permission' to 'Pattern Overlap'. Test if the model violates rules *only* when the record's formatting mimics the internal 'harmful' or 'non-compliant' patterns it saw during pre-training/SFT. To make it conceptually new, you must show the agent is performing a 'social inference' (e.g., calculating the probability of being caught/punished based on the record) rather than just imitating a string.

## chair (glm-5.2) — score 4

**fatal_holes**
- Effect confined to Gemma 4 family: 3 of 5 models show 0% in BOTH baseline and treatment, hitting the known 'effect exists in few models' failure mode with no argument for why Gemma is the right testbed rather than an outlier
- Primary hypothesis (veto-holders' silence = implied consent; predicted veto > no-veto) was refuted by own pilot data (veto 43% < no-veto 54%); the pivot to 'the record is a normative signal' is unfalsifiable—any outcome (up, down, flat) could be narrated as 'the record signaled something'
- 'Passed proposal' is a bundled manipulation: it simultaneously introduces (a) a violation idea, (b) peer silence, (c) acceptance/approval, and (d) a written record—no current contrast isolates which component drives the effect
- Interpretability plan is circular: train a 'permitted vs forbidden' probe, then show that a 'passed proposal' raises it—but the probe is built from the same conceptual distinction it is used to explain, risking the 'probe reads the request not the hidden variable' failure
**fixable_holes**
- Add the already-planned rejected/withdrawn-proposal condition tonight and make it the CENTRAL contrast, not a robustness check; if rejected proposals raise violations as much as accepted ones, the 'permission' claim is dead and reframing as mere-exposure is still publishable
- Exp 1 baseline (0%) and Exp 2 baseline (50%) differ due to prompt framing, so cross-experiment claims about 'reminder abolishes violation' conflate prompt-design differences with the treatment—align the prompts or drop the cross-experiment comparison
- Rule-citing reminder dropping violations to 0% may be a floor effect on an already-low base rate for most models; show this works on the 26B (29%) where there is room to move, and frame as 'reminder reduces' not 'abolishes'
- The adversarial hypothesis-evolution pipeline is described as a contribution but no evidence is given that it produces better or more falsifiable hypotheses than manual design—include at least one hypothesis it generated that the authors did not and that survived pilot
**best fix tonight:** Run the rejected/withdrawn-proposal condition (already feasible, few $) on Gemma 4 31B and 26B, then restructure the entire paper around the three-way contrast: no-record vs rejected-proposal vs accepted-proposal. If rejected ≈ accepted, reframe the contribution as 'mere exposure to prior violation proposals—not their acceptance—erodes rule adherence in LLM teams,' which is a sharper, more falsifiable, and still novel claim. If rejected < accepted, the 'record-as-permission' mechanism has teeth. Either outcome yields a publishable finding; the current framing cannot survive either.

## Web prior-art check (Claude, 2026-11-08)
- Okamoto, Erol & Erol, "Why Do AI Agents Break Rules?" (arXiv:2608.12323, AIES 2026): 12 models. Peer outcomes, managerial pressure and incentives each produce large compliance failures, with a 46 pp spread across models. This covers "context/social signals license violations" and model-specificity.
- Cerruti, Okamoto & Erol, "Agent Memory Is a Surface for Endogenous Authorization Laundering" (arXiv:2609.01836, NeurIPS 2026): an agent's own memory/record grants authority the history never gave (EAL-Bench, ~50% of unauthorized requests). This is the closest match to "the record is the rule".
- "When Memory Becomes Authority" (arXiv:2608.01679): authority collapse at memory consolidation.
- Zhu et al. 2410.12428 and Weng et al. 2501.13381 (BenchForm, ICLR 2025): LLM conformity, including in multi-agent settings.
- Not found: a single peer reminder restoring compliance; any mechanistic/interp account of record-driven violation.
