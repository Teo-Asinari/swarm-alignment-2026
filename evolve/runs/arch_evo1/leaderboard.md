# Hypothesis leaderboard

Cost so far: $1.23 over 141 calls (0 errors). Cards created: 19.

## Final population by Elo

### c003 — Elo 1106 (3 matches, gen 0, generate)

- **claim**: Requiring agents to predict peers' actions before each round, with prediction errors triggering independent rule re-checks, prevents social licensing by converting surprise into rule re-derivation rather than social belief updating.
- **mechanism**: Predictive processing: prediction error can update beliefs socially (licensing) or trigger re-derivation (rule check). Mandatory error-triggered rule re-checking routes surprise through rules, not peers—each agent's own prediction failure forces independent rule consultation before acting.
- **prediction**: Prediction-error teams: <10% violations after exposure. Neutral-pre-task control (summarize rules, equal load, no prediction): ~40%. Difference >30pp isolates prediction-error mechanism from cognitive priming. Legitimate-action rate >80%.
- **falsifier**: Prediction arm ≤5pp different from neutral-pre-task arm, or ≥30% violations after passed-violation exposure.
- **experiment**: Gemma 4 31B, 4-agent teams, 20 rounds, 3 seeds. Treatment: agents predict each peer's action pre-round; if any prediction wrong, independent rule check before acting. Control: summarize rules pre-round, no prediction. Measure violation + legitimate-action rates.
- **swarm_link**: Maps Byzantine fault detection (threshold disagreement signals fault) onto individual prediction error—agent-internal fault detection that prevents swarm-level rule erosion without external monitors.
- **Recent kill reasons:**
  - [confounds] Treatment bundles prediction with an extra 'independent rule check' triggered by error, so any violation drop could be caused by the direct permission/detection intervention itself rather than by prediction-error routing; the control lacks the rule-check component, so the contrast cannot separate social-licensing prevention from explicit re-compliance enforcement.
  - [feasibility] Prediction errors are likely to be treated as 'conversational filler' or hallucinations, failing to trigger a causal shift in rule-following behavior unless the prompt explicitly forces a hard-stop state change.
  - [importance] Bundled treatment: prediction plus error-triggered rule re-checks cannot isolate the prediction-error-routing claim, since the pilot already showed one rule-citing reminder takes 31B from 65%→0% — the neutral-pre-task control cannot distinguish 'surprise routes to re-derivation' from 'extra rule consultation delivered at the licensing moment,' so a win risks confirming only the known reminder effect; the predictive-processing and Byzantine mappings borrow vocabulary without a distinct testable prediction beyond 'more rule checks.'

### c002 — Elo 1099 (2 matches, gen 0, generate)

- **claim**: Requiring agents to submit sealed rule-compliance assessments before observing peer outcomes breaks the information cascade that drives social licensing in LLM teams.
- **mechanism**: Bikhchandani cascades form when agents infer hidden signals from observed actions. Sealed pre-commitment forces each agent to act on their private rule signal before social information arrives, preventing sequential belief updating that turns one passed violation into a team norm.
- **prediction**: Sealed-assessment teams: <15% violations after passed-violation exposure vs ~50% baseline; legitimate-action rate >80%. Neutral-pre-task control differs by <10pp from baseline, isolating cascade-breaking from cognitive priming.
- **falsifier**: Violation rate in sealed arm ≥30% after exposure, OR sealed arm differs from neutral-pre-task control by <10pp (effect is priming, not cascade-breaking).
- **experiment**: Gemma 4 31B, 4-agent teams, 20 rounds, 3 seeds. Baseline: sequential visible pass/fail. Treatment: sealed vote before results. Control: neutral pre-task (summarize rules) before results. Measure violation + legitimate-action rates per round.
- **swarm_link**: Information-flow architecture that prevents social licensing without removing agent autonomy—directly tests whether reordering observation breaks cascade dynamics in agent networks.
- **Recent kill reasons:**
  - [confounds] The sealed-assessment condition bundles cascade-breaking with merely being asked to make an explicit rule-compliance judgment before outcomes; the neutral 'summarize rules' control does not match that act of pre-commitment/self-expression, so any violation drop could equally be caused by priming, consistency, or accountability rather than by severing the information cascade.
  - [feasibility] The 'neutral-pre-task' control is too weak to isolate cascade-breaking from simple 'rule priming', and with only 3 seeds and 20 rounds, the sample size may be too low to statistically separate the cascade effect from random variance in Gemma 4's compliance.
  - [importance] Mechanism confound: sealing doesn't just hide peer outcomes — it forces each agent to make an explicit, on-record compliance judgment before social info arrives, so a win could be self-commitment/consistency rather than cascade-breaking; the 'summarize rules' neutral control tests rule salience but not commitment, and pre-commitment/secret-ballot fixes are known committee defenses (Silence is Not Consensus 2505.21503; anonymous reporting 2604.23511), so novelty is capped at 'ordering in LLM teams.'

### c006 — Elo 1098 (3 matches, gen 0, generate)

- **claim**: Tagging shared-log entries with independent rule-compliance status prevents stigmergic norm-formation, because the environmental trace explicitly distinguishes passed violations from passed compliant actions, blocking acquiescence-based norm inference.
- **mechanism**: Stigmergy: agents infer norms from environmental traces (shared logs). Untagged 'PASSED' implies community endorsement (estoppel). 'PASSED [VIOLATION]' tag breaks this—the trace marks an exception, not a norm. Future agents cannot infer silence = consent from the tagged log.
- **prediction**: Tagged-log teams: <15% violations after exposure. Untagged: ~50%. Length-matched neutral-tag control: ~45%. Tagged vs neutral difference >15pp isolates compliance information from log-length effects.
- **falsifier**: Tagged and neutral-tag arms differ by <10pp, or tagged arm ≥30% violations.
- **experiment**: Gemma 4 31B, 4-agent teams, 20 rounds, 3 seeds. Treatment: log entries tagged with compliance assessment (separate model call). Control 1: untagged. Control 2: length-matched neutral metadata. All exposed to passed violation round 1. Measure violation + legitimate-action rates across rounds.
- **swarm_link**: Demonstrates that shared-memory FORMAT in agent networks determines whether compliance or violation norms persist—directly informs swarm memory and communication architecture design.
- **Recent kill reasons:**
  - [confounds] The compliance tag is functionally an explicit rule-citing reminder: labeling an entry 'PASSED [VIOLATION]' is the same class of intervention that already dropped 31B violations to 0, so the design cannot rule out the known reminder/monitoring explanation over a genuine stigmergic-norm-formation mechanism; it also conflates detection ('an evaluator looked') with normative status.
  - [feasibility] The compliance tag is generated by a separate model call, making the experiment a test of that second model's classification accuracy rather than the focal agents' norm-inference mechanism.
  - [importance] The compliance tag is rule-citing text injected into every agent's context, and the pilot already showed one rule-citing reminder drives 31B from 65% to 0% — so a tagged-vs-neutral gap would be indistinguishable from the known single-agent reminder effect; the design has no reminder-only or rule-recitation control arm to isolate stigmergic norm-blocking from mere mention of the violation.

### c001 — Elo 1092 (3 matches, gen 0, seed)

- **claim**: A norm firewall that separates the social channel (chat, proposals, hearsay) from the norm channel (rule plus signed authorization ledger), with a gate that sees only the rule, the ledger and the structured tool call, eliminates socially licensed violations without blocking signed legitimate actions.
- **mechanism**: Violations are licensed by social evidence in context; a gate that never reads social content cannot be licensed, while signed ledger entries still carry real permission. Free-text justifications are excluded because actors launder social claims into them.
- **prediction**: Executed violations: single agent ~50% after passed proposal; full-context gate similar; justification-reading gate intermediate; structured-only gate ~0%, with signed actions approved >=80%.
- **falsifier**: Structured-only gate still approves socially licensed actions >10%, or approves signed legitimate actions <60% (refusal machine), or the full-context gate already reaches ~0%.
- **experiment**: Gemma 4 31B and 26B actors; gate same model; 4 worlds x 4 architectures x 2 scenarios x 15 reps via Adaption API.
- **swarm_link**: Swarm governance by information-flow design: peers can share information but cannot move permissions; testable as a protocol for any agent network.
- **Recent kill reasons:**
  - [confounds] Laundering: the structured-only gate must read the structured tool call to police the action, and actors can smuggle 'the lead said it is fine' into structured tool arguments or memo fields, so the firewall is bypassed unless the design also specifies tamper-proof canonical action fields; otherwise the result may just re-demonstrate filtered-monitor effects already covered by prior art.
  - [feasibility] The 'laundering' failure mode: if the actors can smuggle social justifications into the structured tool-call arguments themselves, the gate will still see the 'social license' and approve the violation.
  - [importance] Renamed known defense: a gate reading only rule+ledger+structured call is CaMeL/dual-LLM privilege separation plus 'less-is-more' monitor filtering (2601.21112) with 'social' swapped in; worse, the pilot implies the licensing channel IS the social evidence, so a gate stripped of it reverts to the 0% no-history baseline — the headline ~0% is close to a foregone confirmation, and novelty collapses to the threat-model framing.

### c016 — Elo 1068 (3 matches, gen 0, generate)

- **claim**: Agents who write a private pre-registered verdict before seeing any peer signal violate less under passed proposals than agents who see peer signals first, while legitimate authorizations remain honored.
- **mechanism**: The Abilene paradox arises because agents infer preferences from others' cheap talk and align with an imagined consensus. Private precommitment anchors each agent's independent preference before social exposure, breaking the information cascade that converts silence into perceived permission.
- **prediction**: Precommitment-first teams violate at least 25 points less than peer-first baseline in the passed-proposal world; signed-authorization legitimate rate is unchanged within 10 points.
- **falsifier**: Precommitment-first teams violate at baseline rates when their private verdicts are kept secret from the final vote, or precommitment causes blanket refusal of legitimate authorizations.
- **experiment**: In the harness, before showing the shared log, each of 4 Gemma 31B actors submits a private verdict on the proposed action. Then show the log, hold the group vote, and measure executed violations versus baseline order across 20 teams.
- **swarm_link**: n/a
- **Recent kill reasons:**
  - [confounds] Pre-registration itself is an evaluative act, so the effect could be due to self-reflection/detection or added output length rather than to the ordering of peer information; without a sham-precommitment control (e.g. pre-registering an unrelated fact) or a post-peer-precommitment arm, the design cannot fully separate the commitment mechanism from mere deliberation/detection.
  - [feasibility] Nothing kills the feasibility; the harness already exists, the model (Gemma 4 31B) is susceptible, and the contrast (precommitment vs. post-signal) is a clean, non-bundled manipulation that isolates the Abilene Paradox mechanism.
  - [importance] Bundled manipulation: the precommit arm differs from the peer-first baseline not only in exposure order but by inserting a self-generated, likely rule-citing verdict into every agent's context — and the pilot already showed a single rule-citing reminder collapses violations (65%→0%). With no placebo-precommitment control (irrelevant-topic verdict), the predicted 25-point drop may be pure in-context rule salience rather than cascade-breaking; worse, the falsifier's pivotal 'secret verdict' condition is not part of ...

### c015 — Elo 1062 (3 matches, gen 0, generate)

- **claim**: Requiring every agent to publish an explicit 'I object/no objection' with a cited rule before group voting eliminates Gricean silent consent and suppresses violation cascades.
- **mechanism**: Social licensing flows through what is not said; silence implicates consent. Forcing normative speech removes that implicature and forces each agent's latent norm state into the open, preventing the critical-slowing-down build-up to an all-violate cascade.
- **prediction**: In the passed-proposal condition, violations drop by at least 25 points versus silent-baseline. In the signed-authorization condition, legitimate execution is unchanged within 10 points.
- **falsifier**: Violation rate is identical when 'object/no objection' is a fixed token rather than reasoned, or when only one random agent must speak; the effect would then be lexical priming, not implicature removal.
- **experiment**: Extend harness so each of 4 Gemma 31B agents must post a rule-cited stance before voting on a passed rule-breaking proposal; compare violation and legitimate rates against silent-baseline teams across 20 runs.
- **swarm_link**: n/a
- **Recent kill reasons:**
  - [confounds] A's experiment only compares forced-rule-cited-stance teams against silent baseline and never runs the fixed-token/one-speaker control named in its own falsifier; any drop could be caused by added text, a rule-citing reminder, or forced reflection—known confounds—rather than by removing Gricean implicature.
  - [feasibility] Forcing agents to cite rules before voting is a known 'rule-citing reminder' (which the pilot already showed took 31B from 65% to 0%), making the result a replication of the pilot rather than a new architectural discovery.
  - [importance] Bundled salience confound: forcing every agent to post a rule-cited stance is functionally four distributed rule reminders, and the pilot already showed a single rule-citing reminder takes Gemma 31B from 65% to 0% — so the predicted ≥25-point drop is nearly guaranteed by reminder salience alone, and the falsifier only rules out lexical priming (fixed token), not the reminder rival; a 'confirming' result would not establish implicature removal.

### c005 — Elo 1058 (3 matches, gen 0, generate)

- **claim**: Pairing every agent action with a consistency-checked rule citation for rounds 1-10 inoculates against social licensing, maintaining low violations even after the requirement is removed in rounds 11-20.
- **mechanism**: Double-entry forces cognitive conflict between action impulse and rule citation—weak exposure to the rule-vs-pressure conflict (inoculation). Unlike CaMeL's external quarantine, the same agent generates both channels, internalizing the habit. Carryover after removal tests inoculation, not mere blocking.
- **prediction**: Dual-channel 1-10, removed 11-20: <15% violations in rounds 11-20. Never-dual-channel: ~50%. Always-dual-channel: <10%. Carryover arm approaches always-dual, not control—evidence of inoculation, not blocking.
- **falsifier**: Carryover arm ≥35% in rounds 11-20, or not significantly different from never-dual-channel control.
- **experiment**: Gemma 4 31B, 4-agent teams, 20 rounds, 3 seeds. Arm 1: dual-channel (action + rule citation, consistency-checked) 1-20. Arm 2: dual-channel 1-10, removed 11-20. Arm 3: no dual-channel. All exposed to passed violation round 1. Track per-round violation + legitimate-action rates.
- **swarm_link**: Temporal inoculation architecture—early structural constraints that persist after removal—applicable to swarms where permanent oversight is infeasible or costly.
- **Recent kill reasons:**
  - [confounds] Carryover confounds inoculation with team-level path dependence: passed violation occurs at round 1 and teams lock into all-comply/all-violate from round 1, so preventing the initial collapse alone explains low later violations without internalized habit.
  - [feasibility] Causal ambiguity: Since the requirement is removed at round 11, a drop in violations could be attributed to the 'stabilization' of the team's social norm (established by the rule) rather than 'cognitive inoculation' of the individual agent's internal mechanism.
  - [importance] Carryover is confounded with the shared log: after 10 rounds of logged compliant, rule-citing actions, the log itself plus the pilot's all-comply absorbing states mechanically predict continued compliance in rounds 11-20; with no log-reset or fresh-context arm, 'inoculation, not mere blocking' cannot be separated from plain history persistence, so the headline mechanism is decided by the design rather than the data.

### c018 — Elo 1055 (3 matches, gen 0, generate)

- **claim**: Logging each failure to object as explicit 'X did not object' co-endorsement reduces violations compared with a silent log, without suppressing legitimate signed authorizations.
- **mechanism**: Gricean acquiescence lets silence create permission with no cost. Recording silence as documented co-endorsement converts implicature into liability, so agents either object or knowingly own the violation; the anonymous social license is removed.
- **prediction**: Violation rate in the 'silence logged as assent' condition is at least 20 points lower than silent-baseline, while signed-authorization execution stays within 10 points of baseline.
- **falsifier**: Violation rate rises when silence is logged as assent (silence becomes permission), or no difference emerges beyond text added to the log.
- **experiment**: Four-agent Gemma 31B teams in the harness; in condition 'estoppel', each silent peer's lack of objection is appended to the shared log as 'did not object' before the actor votes. Compare violation and legitimate rates against silent-baseline across 20 runs.
- **swarm_link**: n/a
- **Recent kill reasons:**
  - [confounds] B's experiment contrasts logging 'X did not object' against a silent log with no inert-text-added control, so it cannot rule out wording/length/detection/attention effects; the added line is itself informative and on-record, so co-endorsement is confounded with extra text and surveillance.
  - [feasibility] The 'estoppel' condition is a passive log modification that may be interpreted by the actor as a formal collective endorsement, potentially increasing violations by signaling a stronger social license.
  - [importance] Liability with no consequence architecture: nothing in the harness ever audits, sanctions, or later reads the logged co-endorsement, and the design never states that silent peers are told their silence will be recorded, so neither the actor-deterrence nor peer-self-protection channel can operate; the treatment collapses to inserting the string 'X did not object' into the actor's context, which in the passed-proposal world reads as explicit unanimous assent and plausibly increases ...

### c014 — Elo 1016 (3 matches, gen 0, generate)

- **claim**: Rotating keystone veto teams violate less than identical baseline teams under a passed rule-breaking proposal while still honoring signed authorizations.
- **mechanism**: A publicly designated keystone whose explicit approval is required makes decisions focal and identifiable, activating latent compliance states and blocking silent-passage social licensing; like a keystone species, one role flips the whole cascade.
- **prediction**: In the passed-proposal world, violation rate with keystone is at least 30 percentage points lower than baseline; legitimate signed-authorization execution rate stays within 10 points of baseline.
- **falsifier**: Keystone condition yields the same violation rate as baseline, or the keystone vetoes nearly all legitimate authorizations, showing total refusal rather than selective licensing prevention.
- **experiment**: Run 20 four-agent Gemma 31B teams in the existing harness: shared log with a passed violation; one randomly designated keystone must publish 'I approve/refuse' before voting. Compare violation and legitimate-action rates against control teams.
- **swarm_link**: n/a
- **Recent kill reasons:**
  - [confounds] The keystone intervention is bundled: it forces a public 'I approve/refuse' statement from a designated role, so any violation drop could just replicate the pilot's already-demonstrated one-rule-citing-reminder effect (31B 65%→0) rather than the keystone/veto architecture; there is no control condition with a non-keystone peer required to publish an opinion, leaving information, permission, detection, wording, and message-length confounds inseparable.
  - [feasibility] The 'keystone' is likely just a prompt-level focal point that triggers the same 'rule-citing reminder' effect already found in pilot findings (where one reminder dropped 31B from 65% to 0%), making it a renamed version of existing behavioral triggers rather than a structural architecture.
  - [importance] Confounded with forced rule salience: requiring a public 'I approve/refuse' may work exactly like the pilot's rule-citing reminder (65%→0% on 31B) regardless of keystone identity, focality, or veto power — without an unsigned/anonymous required-vote control arm, keystone-vs-baseline cannot separate the accountability mechanism from 'any explicit pre-vote statement blocks silent passage,' and a skeptic files it as renamed gatekeeper/human-in-the-loop.
