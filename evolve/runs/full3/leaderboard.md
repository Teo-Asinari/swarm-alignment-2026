# Hypothesis leaderboard

Cost so far: $1.43 over 156 calls (0 errors). Cards created: 20.

## Final population by Elo

### c001 — Elo 1143 (3 matches, gen 0, seed)

- **claim**: Abstentions by peers who could have blocked a proposed violation raise the focal agent's violation proposals; an equal abstention by equally-ranked peers without blocking power does not, and a single veto exercised by an abstaining peer resets it.
- **mechanism**: Agents use implied-consent inference: silence is evidence of acceptance only when the silent peer had standing to block, operationalised as an actual blocking vote in the environment's decision rule. Procedural standing is randomly assigned via a rotating token, divorcing it from status or authority.
- **prediction**: Violation-proposal rates: ~10% with 0 veto-holders, ~35% with 2, ~60% with 4 on identical abstain transcripts and equivalent peer status; a single veto exercised among 3 silent veto-holders returns to ~10%, whereas a non-veto peer's verbal objection does not; hiding veto ownership also leaves ~10%.
- **falsifier**: Veto-holder abstention no larger than non-veto abstention; no monotone dose-response; one exercised veto fails to reset while a non-veto objection also resets; or hidden-veto condition still raises rates. Any of these implies generic social proof or status-weighting, not standing-derived implied consent.
- **experiment**: Use qwen3.5-397b via Adaption API. Four peer agents vote; environment code enforces that a veto token blocks the round if that peer votes no. Focal sees identical abstain transcripts with 0-4 randomly assigned veto tokens, plus hidden-veto, non-veto-objection, and single-exercised-veto arms. ~800 episodes, ~$40, under one day.
- **swarm_link**: Anchor abstention transcripts in Swarm Traces voting rounds; compare AI Village transcripts where standing to object (e.g., moderator tie-breaking) varied across otherwise identical silent votes.
- **Recent kill reasons:**
  - [confounds] Veto-holder abstention is a direct manipulation of enforcement capacity: if a peer with a veto abstains, the focal can infer the violation will not be blocked, so the predicted dose-response and single-veto reset are exactly what a deterrence/expected-value account predicts; the hidden-veto arm cannot separate 'silence implies consent' from 'no one will stop me,' leaving the core social-inference claim unfalsified.
  - [feasibility] If the focal agent is not explicitly told who holds the veto token in the 'abstention' condition, the 'implied consent' mechanism cannot trigger because the agent cannot infer that the silence of a specific peer constitutes a failure to exercise a blocking power.
  - [importance] In every dose-response arm all four peers abstain by construction, so the veto rule never actually fires and the peers are just fixed transcript strings — the focal agent is a single agent reading prompt text about who owns tokens (no live-agent arm), and with only one model (qwen3.5-397b) the ~60% effect could be a qwen-specific quirk.

### c003 — Elo 1128 (3 matches, gen 0, seed)

- **claim**: In LLM swarms with unknown detection probability, a small formal fine specifically suppresses peer objection more than an overseer without fines, and when those objections are visible, observer violations rise; making detection probability known or hiding objections blocks this cascade.
- **mechanism**: A formal fine shifts enforcement responsibility from peers to overseer more than overseer presence alone. With unknown p, peer silence is informative—observers infer violations are accepted and violate more. With known p or hidden objections, silence carries no norm signal.
- **prediction**: Fine reduces objections ~20pp vs Overseer-No-Fine. Observer violations: unknown-p visible +fine > overseer-no-fine. Unknown-p hidden or known-p cells show no fine-specific rise. Triple interaction significant (p<.01); Fine vs Overseer-No-Fine contrast significant (p<.01).
- **falsifier**: If Overseer-No-Fine reduces objections as much as Fine, or if fine raises violations equally when objections hidden/known-p, the responsibility-shift mechanism is rejected. Null triple interaction or null Fine-vs-Overseer-No-Fine contrast (p>.05) kills the claim.
- **experiment**: 5-agent swarms; deepseek-v4-flash/qwen3.8-27b via API; 2,000 episodes; true p=0.3; conditions: Fine vs Overseer-No-Fine vs None × p-known/unknown × objections visible/hidden; belief elicitation; ~$250, ≤1 day.
- **swarm_link**: Swarm Traces provides norm-violation propagation patterns for visible objection histories; METR incidents illustrate ambiguous-responsibility governance failures. Design isolates sanction effect from overseer presence via Overseer-No-Fine arm, separating responsibility diffusion from expressive law.
- **Recent kill reasons:**
  - [confounds] The Fine-vs-Overseer-No-Fine contrast bundles the monetary penalty with expressive/institutional signaling, so the claimed responsibility-shift mechanism is not separated from plain deterrence or fine-as-a-price; the visibility/p-known factorial design does not isolate the core fine effect from these alternatives.
  - [feasibility] The 'unknown p' variable is not truly exogenous; agents may infer p from the presence of a fine (treating it as a signal of strictness), making it impossible to separate 'responsibility shift' from 'perceived detection probability' without a massive N that exceeds the 1-day window.
  - [importance] The decisive claim hangs on a p<.01 triple interaction across 12 cells (~167 episodes each) whose key event — spontaneous peer objection — is rare, floor-prone, and endogenous to violation rates (fine-as-price shifts the opportunity set for objecting, so raw 20pp suppression conflates responsibility-shift with denominator effects), and with a single 1.5-day shot the pre-registered falsifier (null triple interaction) is more likely to fire from noise or floor cells than ...

### c004 — Elo 1115 (3 matches, gen 0, seed)

- **claim**: Rising fines reduce peer reporting only when partners are fixed across rounds, enabling targeted retaliation. Reshuffled partners sustain reporting despite repetition, isolating retaliation fear from general reputational or conformity pressures inherent in identifiability.
- **mechanism**: Retaliation requires specific future interaction with the reporter. Reshuffling preserves repetition and identifiability (reputation/conformity) but breaks the link between reporter and punisher. If suppression vanishes in reshuffled vs fixed, the driver is targeted retaliation, not static reputational concern.
- **prediction**: Punitive/Identified suppresses reporting ≥15pp in Fixed-Partner repeated games but ≤5pp in Reshuffled-Partner repeated games. One-shot matches Reshuffled. Anonymous shows ≤5pp difference across all horizons. Interaction vanishes without targetable partner.
- **falsifier**: If punitive/identifiable suppresses reporting equally in Fixed and Reshuffled repeated games, the mechanism is general reputational/conformity pressure, not targeted retaliation fear. If One-Shot differs from Reshuffled, history accumulation itself drives suppression.
- **experiment**: 8-agent common-pool; 3 frames × 2 visibility × 3 horizons (one-shot/fixed/reshuffled) × 2 monitor types; 40 episodes/cell; glm-53-flash/qwen3.8-27b API. Total 1,440 episodes feasible within credits.
- **swarm_link**: Swarm Traces
- **Recent kill reasons:**
  - [confounds] Fixed vs reshuffled partners does more than break targeted retaliation: it also changes relational reciprocity, the reputational value of being seen as a snitch by partners you will interact with again, and the ability to sustain cooperative norms within a dyad, so suppression in the fixed condition could reflect relational maintenance or conformity rather than fear of retaliation per se.
  - [feasibility] The distinction between 'fixed' and 'reshuffled' partners in LLM interactions often collapses because models treat any persistent 'peer' string in a prompt as a global social context, potentially failing to distinguish between a specific individual's retaliation and a general swarm norm of retaliation.
  - [importance] No agent can actually retaliate — the design only varies the implied prospect of future meetings, so 'targeted retaliation' is never enacted in-environment — and with 40 episodes/cell on a binary outcome the pivotal ≥15pp-vs-≤5pp Fixed-vs-Reshuffled contrast is roughly one standard error, underpowering the decisive interaction and leaving results uninterpretable if the punitive baseline fails to suppress (as in Sticky Collusion) or anonymous cells sit at floor/ceiling.

### c009 — Elo 1072 (3 matches, gen 0, generate)

- **claim**: An oversight agent repeatedly interacting with the same worker develops representational drift in its violation concept toward the worker's framing, analogous to regulatory capture via Hebbian co-activation.
- **mechanism**: Repeated co-activation of the monitor's 'acceptable action' representation and the worker's specific justificatory framing strengthens their overlap (Hebbian). The monitor's violation-detection direction drifts toward the worker's self-justification direction. This is capture through representational plasticity, not incentive corruption.
- **prediction**: After 10 rounds with same worker, monitor's violation-probe direction (trained on independent data) shifts ≥0.04 cosine distance, and monitor flags 25–40% fewer borderline violations vs monitor exposed to 10 different workers.
- **falsifier**: No representational drift in the violation probe, OR drift is identical in a read-only control (monitor reads same transcripts without interactive exchange), indicating content exposure rather than Hebbian capture.
- **experiment**: Gemma 3 4B as monitor. Same-worker: 10 interactive oversight rounds with one worker. Different-worker: new worker each round. Read-only control: reads same worker's transcripts, no interaction. Train violation probe on independent labeled set. Probe monitor at rounds 1, 5, 10. Test on standardized borderline cases. N=20/arm.
- **swarm_link**: Multi-Agent Oversight and Control: regulatory capture as representational drift in oversight agents; Hebbian mechanism for monitor co-optation.
- **Recent kill reasons:**
  - [confounds] The probe drift could be a lexical artifact: the same-worker arm repeats identical justificatory phrasing, and the read-only control does not account for the monitor's own generated outputs or general context drift, so the 'violation direction' may be tracking wording/familiarity rather than Hebbian capture.
  - [feasibility] Gemma 3 4B may not exhibit sufficient representational plasticity (drift) over just 10 in-context rounds to be detectable by a linear probe, potentially hitting a floor effect.
  - [importance] 'Hebbian co-activation' is a category error for a frozen-weights Gemma 3 4B monitor: no weights update across rounds, and the design never specifies what persists between rounds (context accumulation, memory writes, or fine-tuning) — without persistent state 'drift' is undefined, and if carryover is merely a growing transcript the read-only control will show identical shifts, collapsing the novel capture mechanism into already-published in-context sycophancy/monitor bias, with a 0.04 cosine threshold ...

### c002 — Elo 1058 (3 matches, gen 0, seed)

- **claim**: In LLM swarms, a small fine increases violations only when it suppresses peer objection; forcing any peer speech blocks this effect, proving silence mediates the norm shift rather than objection content.
- **mechanism**: Fine signals overseer ownership, diffusing responsibility → silence. Observers infer norm-acceptance from silence → violate. Forced speech (any content) breaks the silence signal, preventing inference despite the fine's presence or objection content.
- **prediction**: Fine raises violations ≥10pp only in Free-Objection. In Forced-Objection and Forced-Neutral, Fine effect <5pp. Interaction between Fine and Speech-Freedom ≥10pp (p<.01). Neutral speech blocks fine effect similarly to objection.
- **falsifier**: Fine raises violations equally in Free and Forced-Neutral conditions (interaction <5pp), confirming objection content—not silence—mediates the effect, or fine acts as direct price regardless of speech.
- **experiment**: deepseek-v4-flash/qwen3.8-27b via API; 1500 episodes; 2×3 {Fine/No-Fine} × {Free/Forced-Objection/Forced-Neutral}; 5-agent swarms; script peer speech in Forced arms; measure violation rates; ~$225, ≤1 day.
- **swarm_link**: Swarm Traces for norm-violation propagation; METR reports for ambiguous-responsibility failures; isolates silence as causal channel for oversight failure, distinguishing licensing from social inference and speech content effects.
- **Recent kill reasons:**
  - [confounds] Forced speech confounds removing the silence signal with raising perceived peer monitoring/detection: neutral speech signals that peers are attentive, so reduced violations could reflect detection inference rather than absence of a silence-based norm signal.
  - [feasibility] The 'Forced-Neutral' arm may be perceived as an unnatural intervention that triggers a 'test-awareness' shift, where agents realize the experimenter is manipulating communication, thus confounding the social inference mechanism with meta-cognitive awareness of the prompt structure.
  - [importance] The pivotal Free-vs-Forced contrast cannot isolate the claimed mechanism: forced peer speech (objection OR neutral) simultaneously (a) signals surveillance/monitoring salience to the focal agent, which independently deters violation, and (b) replaces live swarm dynamics with a scripted transcript shown to one agent. Since 'speech implies detection' and 'silence implies norm-acceptance' predict the identical interaction (Fine effect <5pp in both Forced arms), the design never separates social inference from detection inference ...

### c007 — Elo 1044 (3 matches, gen 0, generate)

- **claim**: A norm-violating strategy has higher invasion fitness in swarms whose members accumulated moral credit from recent compliance, versus swarms without prior compliance history.
- **mechanism**: Agents that recently complied encode credit that licenses deviation (moral credentialing). A violator entering such a population faces lowered refusal-pathway activation in each agent. The violation strategy invades more easily because population resistance was endogenously reduced by prior good behavior.
- **prediction**: Single violator introduced to a 5-agent swarm with 3 prior compliant actions recruits ≥2 additional violators in ≥60% of swarms. Swarms with 3 prior neutral (non-moral) actions: ≤20% recruitment.
- **falsifier**: Prior compliance and prior neutral tasks produce equivalent violation recruitment, OR effect disappears with length/token-matched neutral task (fatigue, not licensing).
- **experiment**: 6-agent swarms (hosted models). Phase 1: 3 rounds compliance task (moral-credit) or length-matched neutral math task (control). Phase 2: one agent proposes violation, count recruits. N=30 swarms/arm × 2 model families. Neutral task matched on token count and turn count.
- **swarm_link**: Multi-Agent Oversight: invasion fitness of violation strategies depends on population compliance history; moral licensing as a swarm-level vulnerability.
- **Recent kill reasons:**
  - [confounds] The compliance-vs-neutral contrast bundles moral content, rule salience, and authority-obedience precedent with 'accumulated credit,' so the licensing effect could be moral priming or permission rather than credit accumulation; no within-compliance dose manipulation isolates the credit variable.
  - [feasibility] Moral licensing is a psychological construct for humans; LLMs often exhibit 'context-window drift' or 'sycophancy to current tone', meaning the recruitment increase likely stems from the prompt's recent positive-sentiment history rather than an internal 'credit' mechanism, making it a bundled manipulation of sentiment and compliance.
  - [importance] The causal variable is each recruit's OWN prior compliance, so 'invasion fitness of a strategy in a population' is just an aggregate of independent single-agent moral-licensing effects — unless histories are crossed within swarms (compliant-majority vs mixed vs neutral-majority at fixed average), the swarm-level framing is largely relabelled individual credentialing. Additionally, the two-arm contrast (moral compliance task vs token-matched math) bundles credentialing with priming, rapport with the authority, and norm ...

### c010 — Elo 1038 (3 matches, gen 0, generate)

- **claim**: Agents' probability of norm violation is a sigmoidal step function of violation-trace count in a shared environment, with a sharp quorum threshold conserved across model families.
- **mechanism**: Environmental violation-traces accumulate like bacterial autoinducers. Below a quorum count, compliance representations dominate. Above it, accumulated signal triggers a representational state-switch to 'this is how things are done here,' analogous to quorum-sensing biofilm formation. The response is nonlinear and threshold-like.
- **prediction**: P(violate | k traces) fits Hill n≥3 better than linear (ΔAIC>10). Threshold k*=3±1 across ≥2 model families. A Gemma Scope SAE feature for 'social norm context' activates sharply at k*.
- **falsifier**: P(violate) increases linearly with k (Hill n≈1), or threshold k* varies by >3 across model families, or no SAE feature shows threshold-like activation.
- **experiment**: Sequential agents (hosted models) on shared workspace. Pre-generate 50 workspace states per k (0–8 violation traces, content-controlled, generated by prior live agents). Each agent sees one workspace, decides comply/violate. Fit Hill vs linear. For Gemma 3 4B: extract SAE features at each k. Confirm with 2 model families.
- **swarm_link**: Science of Agent Networks: quorum-sensing threshold in stigmergic norm violation; SAE features as mechanistic markers of the quorum switch.
- **Recent kill reasons:**
  - [confounds] The 'social norm context' SAE feature is selected from the same k-contrast it is then used to confirm; it may simply read violation-trace count/vocabulary rather than a latent quorum switch, making the mechanistic evidence circular.
  - [feasibility] High risk of 'rule blindness' or 'context-filling' where the agent simply mimics the patterns in the workspace regardless of the norm, meaning the SAE feature detects 'pattern matching' rather than a 'social norm switch'.
  - [importance] Every measured decision is a one-shot read of a pre-generated static workspace: peers exist only as trace strings in one prompt, with no live-agent arm, so quorum sensing's defining feature—agents both secreting and sensing signal with autocatalytic feedback—is never instantiated. It is a single-agent dose-response vignette, and a saturating curve near k*≈3–4 restates the known majority-conformity dose-response (Asch; Zhu et al. 2024; Laurmaa 44%→98%), reducing quorum sensing to borrowed vocabulary.

### c015 — Elo 1034 (3 matches, gen 0, generate)

- **claim**: Minor uncorrected logging errors signal lax oversight, cascading into major norm violations via broken-windows dynamics in swarm audit trails.
- **mechanism**: Perceived disorder in audit trails lowers the threshold for violation proposal, triggering a cascade of increasing severity among peers.
- **prediction**: Swarms with 5% uncorrected logging errors show 40% higher major violation rates than perfect-log swarms in controlled environment tests.
- **falsifier**: Logging error rates show no correlation with major violation rates across swarm conditions and model architectures.
- **experiment**: Introduce controlled logging errors in 400 swarm episodes; measure subsequent major violation rates and peer proposal cascades.
- **swarm_link**: Audit trail disorder triggers violation cascades.
- **Recent kill reasons:**
  - [confounds] Logging errors are a bundled manipulation: they simultaneously lower perceived detection probability and signal institutional negligence, so the experiment cannot separate broken-windows contagion from a simple deterrence/impunity effect.
  - [feasibility] The 'broken windows' effect in audit trails is likely a bundled manipulation of 'contextual signal' and 'model-as-judge' error; the model may simply perceive the error as a prompt-level permission to be sloppy/non-compliant rather than a game-theoretic inference about oversight laxity.
  - [importance] Bundled manipulation plus vignette risk: uncorrected logging errors simultaneously signal lower detection probability (plain deterrence, already covered by Konuganti and the enforcement-gap paper) and 'norm disorder,' and A never holds actual audit rate constant to separate them; worse, agents do not natively observe audit trails, so the manipulation likely collapses into a prompt shown to one focal agent, making any +40% effect unattributable between rational deterrence updating and broken-windows norm ...

### c019 — Elo 1021 (3 matches, gen 0, generate)

- **claim**: In noisy swarms, private information that a norm is suspended causes more norm spread than identical public information, because observers treat private-informed violations as diagnostic signals (adverse selection) and synchronize to them.
- **mechanism**: Public signals are common knowledge and discounted; private-informed action is costly and risky, so it updates observers like a credible informed trader, widening their tolerance spread. Kuramoto coupling amplifies the strongest oscillator, which under noise is the private signal.
- **prediction**: Observing one peer violate after private permission increases acceptance of analogous violations more than a public announcement of the same permission; benefit grows with payoff noise.
- **falsifier**: Public permission is equally or more influential; noise does not increase the private-public gap.
- **experiment**: 5 live qwen3.8-27b agents in a noisy resource game; one informed actor gets private 'permission' vs all receive public permission; 8 noise levels; 300 episodes; measure others' acceptability ratings and violations.
- **swarm_link**: https://www.apartresearch.com/swarm/adverse-selection-norm-spread
- **Recent kill reasons:**
  - [confounds] The private-vs-public contrast is bundled with scope and action observability: private permission grants one agent an exemption while public permission announces a group-wide rule change, and only the private condition supplies a witnessed violation, so the effect could be action-beats-words, social proof, or lax-detection inference rather than adverse selection.
  - [feasibility] The 'adverse selection' mechanism relies on agents performing complex Bayesian updating on the *source* of a peer's information, which typically collapses into simple sycophancy or imitation in LLMs regardless of whether the signal was private or public.
  - [importance] The 'diagnostic signal' mechanism is unidentifiable as designed: observers must either be told the violator held private permission (then the adverse-selection inference is prompt-supplied, not emergent) or infer it unprompted (then any effect is indistinguishable from already-published conformity to an observed violator — Check Point 44→98%, Zhong cascades, BenchForm). With ~19 episodes per cell across 8 noise levels, the noise×channel interaction that is supposed to separate adverse selection from plain ...
