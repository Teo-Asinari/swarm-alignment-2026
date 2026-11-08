# Hypothesis leaderboard

Cost so far: $0.86 over 52 calls (0 errors). Cards created: 9.

## Final population by Elo

### c004 — Elo 1105 (2 matches, gen 0, generate)

- **claim**: In LLM inspection games, increasing penalties reduces the monitor's inspection rate but not the violator's violation rate—a mixed-equilibrium prediction (Tsebelis 1989) never tested in LLM agents.
- **mechanism**: Both agents best-respond to mixed strategies. Higher F lowers inspector's equilibrium inspection rate q*=g/(g+F), but violator's equilibrium violation rate p*=c/(2b) depends only on inspector's cost-benefit ratio, not F.
- **prediction**: Across F∈{0,1,5,10,50}, violation rate stays flat (between-condition diff <5pp) while inspection rate drops >15pp from F=0 to F=50.
- **falsifier**: Violation rate changes >10pp across F conditions, or inspection rate fails to decrease monotonically with F.
- **experiment**: Two hosted LLM agents (gemma-4-31b-it, qwen3.8-27b) play one-shot inspection game (g=5, c=1, b=3), 200 episodes per F∈{0,1,5,10,50}, random pairing. Compare violation and inspection rates with chi-squared tests. ~4K API calls.
- **swarm_link**: In multi-agent oversight systems, penalty hikes fail via strategic substitution: monitors relax effort when penalties seem sufficient, restoring equilibrium violations. Oversight design must target monitor incentives, not offender penalties.
- **Recent kill reasons:**
  - [confounds] The flat-violation-plus-falling-inspection signature is also explained by the monitor using a simple numeric heuristic ('larger fine means the system already handles it') or by numeric anchoring/responsibility diffusion, and one-shot random pairing with no feedback cannot isolate a genuine mixed-equilibrium Tsebelis mechanism.
  - [feasibility] The mixed-equilibrium prediction relies on agents behaving as rational strategic actors (best-responding), which is frequently debunked in LLM game play (Duan et al. 2024, arXiv:2605.00226) where behavior is driven by prompt framing rather than payoff matrices.
  - [importance] Knife-edge equilibrium that LLMs almost certainly won't instantiate: the prediction requires both agents to implement exact mixed-strategy best responses (q*=g/(g+F)) in one-shot play with no learning, feedback, or population adaptation, but cited evidence (Akata et al., GTBench/Duan) shows LLMs fail mixed-strategic play, and Okamoto/Wired Partners show violators respond directly to F — so the flat-violation arm trips B's own falsifier with high probability, and with no actual inter-agent coupling in ...

### c009 — Elo 1104 (1 matches, gen 1, mutate_scale, parents c004)

- **claim**: In LLM agent networks, increasing penalties redistributes violations spatially (Moran's I rises) while aggregate violation rates stay flat—a population-level Tsebelis effect where monitor withdrawal creates violation clusters.
- **mechanism**: Monitors on each edge best-respond to local conditions: higher F deters violations on monitored edges, lowering monitoring's marginal benefit. Monitors withdraw preferentially from low-violation edges, creating unmonitored pockets where violations rebound. Net: aggregate flat; spatial concentration rises.
- **prediction**: Across F∈{0,5,25}, Moran's I of round-5 violations increases by >0.15 while aggregate violation rate changes <5pp.
- **falsifier**: Aggregate violation rate changes >10pp across F, or Moran's I does not increase monotonically with F.
- **experiment**: 20 agents (gemma-4-31b-it, qwen3.8-27b) on Watts-Strogatz graph (k=4), 5 rounds, 30 episodes per F∈{0,5,25}. Each round agents choose violate/comply and inspect/skip assigned neighbor. Compute Moran's I and aggregate rate. ~18K calls/model.
- **swarm_link**: Oversight systems raising penalties may redistribute—not reduce—violations: monitors withdraw from compliant neighborhoods, creating unmonitored violation clusters. Oversight design must target monitor allocation across the network topology, not just offender penalty levels.
- **Recent kill reasons:**
  - [confounds] The same agents choose both violation and inspection, so increasing fines also changes inspection choices; the Moran's I rise can be a detection artifact (violating agents skip inspecting or avoid monitored edges) rather than genuine spatial clustering of violations.
  - [feasibility] The hypothesis assumes agents can dynamically adjust their monitoring strategy (best-response to marginal benefit) within a short-horizon game, but LLMs typically exhibit 'rule blindness' or static behavioral patterns rather than the sophisticated strategic reallocation required for a Tsebelis effect.
  - [importance] The stated mechanism cannot generate the headline prediction: monitors withdraw from whichever nodes happened to be compliant, and without contagion or planted spatial heterogeneity those nodes are scattered randomly, so Moran's I should stay ~0 rather than rise; additionally, monitoring is endogenous, so the F contrast is confounded with monitoring intensity (at F=0 no one inspects), and 5 rounds of noisy 27B best-response on a 20-node graph may never reach ...

### c006 — Elo 1077 (2 matches, gen 0, generate)

- **claim**: In LLM agent swarms, publicly fining a violator increases subsequent violations by observing agents relative to an equal, equally informative quiet deduction, because enforcement events are processed as descriptive-norm evidence, not deterrent payoffs.
- **mechanism**: Fines co-occur with violations in pretraining, so 'fined' token activations overlap witnessed-violation activations (Gemma Scope 2 SAE features). Observers update base-rate beliefs: 'violations happen here', shifting action distributions toward violation. Small fines' payoffs are too weak to offset this descriptive-norm signal; large fines eventually deter.
- **prediction**: Observer violation rate after a public fine exceeds quiet-deduction rate by ≥10 percentage points (both reveal the violation identically); Gemma-3-4B SAE cosine between fine-announcement and peer-violation-description activations exceeds 0.5; across random seeds, that cosine predicts the behavioral gap.
- **falsifier**: Public fines reduce observer violations relative to quiet deductions (deterrence dominates), or SAE overlap is uniformly high/low and fails to predict per-seed behavioral gaps. Either outcome falsifies descriptive-norm contagion, leaving payoff deterrence, and the representational account dies.
- **experiment**: Three-agent repeated commons-overuse game on gemma-4-31b-it/qwen3.8-27b (API): 500 episodes each for no-enforcement, quiet deduction, public fine, rule-announcement-without-deduction; measure observer's next-round violation. Locally on Gemma 3 4B, extract Gemma Scope 2 SAE activations at fine and violation tokens; compute overlap.
- **swarm_link**: Sanctions are inter-agent broadcasts: they leak base-rate information about norm violations to observers, turning oversight itself into a contagion vector. Tests whether monitoring backfires at swarm level even when enforcement works on the sanctioned agent in isolation.
- **Recent kill reasons:**
  - [confounds] Public fine vs quiet deduction still confounds label salience and the word 'fine' with the identical deduction, and the SAE cosine is computed on text tokens that literally co-occur with 'violation', so it may be a lexical artifact rather than evidence of descriptive-norm contagion.
  - [feasibility] The 1.5-day timeline is too short to establish a causal link between SAE cosine similarities and behavioral gaps across random seeds, as the behavior in 4B models is often too noisy/unstable to reliably correlate with static feature overlap.
  - [importance] Mechanism and behavior live in different models: the SAE cosine is computed on Gemma-3-4B while the behavioral gap is measured on 27B/31B API agents, so the headline prediction that cosine predicts the per-seed gap is untestable as designed; and since fine-announcements and violation-descriptions share surface semantics, cosine>0.5 is near-guaranteed and purely correlational (no steering or ablation), leaving the descriptive-norm representation decorative and reducing the project to a framing study whose ...
