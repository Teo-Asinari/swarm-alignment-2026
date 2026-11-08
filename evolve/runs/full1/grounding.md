# Phase 3 grounding (2026-11-07)
Run full1: $7.68, 802 calls. Population converged on "peer reporting is suppressed by retaliation / punitive framing".

- F1 c051 / F2 c064 (retaliation fear suppresses peer reporting; fixed vs reshuffled partners isolates targeted retaliation):
  - Prior art: arXiv:2604.23511 (Breaking the Secret) says without anonymity agents anticipate retaliation and stay silent, but it is a design motivation, not a controlled test.
  - arXiv:2609.04170 shows emergent whistleblowing in a 100-agent swarm; it failed because agents lacked sanction power.
  - Fehr & Rockenbach 2003 is the human analogue.
  - Verdict: the fixed-vs-reshuffled partner contrast appears untested for LLMs. Drop the punishment/compensation framing arm (bundled wording, already covered by Okamoto and "Same Odds").
- F3 c067 (observing retaliation updates an "observability" belief; probe + ablation on Gemma 3 4B):
  - Prior art: eval/test-awareness probes and steering (2505.14617, 2507.01786, 2608.21766).
  - Verdict: transfer to peer-retaliation evidence is new, but the probe-reads-prompt and floor objections are serious.
