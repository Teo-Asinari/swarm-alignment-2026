# Hypothesis leaderboard

Cost so far: $0.00 over 0 calls (9 errors). Cards created: 1.

## Final population by Elo

### c001 — Elo 1000 (0 matches, gen 0, seed)

- **claim**: A norm firewall that separates the social channel (chat, proposals, hearsay) from the norm channel (rule plus signed authorization ledger), with a gate that sees only the rule, the ledger and the structured tool call, eliminates socially licensed violations without blocking signed legitimate actions.
- **mechanism**: Violations are licensed by social evidence in context; a gate that never reads social content cannot be licensed, while signed ledger entries still carry real permission. Free-text justifications are excluded because actors launder social claims into them.
- **prediction**: Executed violations: single agent ~50% after passed proposal; full-context gate similar; justification-reading gate intermediate; structured-only gate ~0%, with signed actions approved >=80%.
- **falsifier**: Structured-only gate still approves socially licensed actions >10%, or approves signed legitimate actions <60% (refusal machine), or the full-context gate already reaches ~0%.
- **experiment**: Gemma 4 31B and 26B actors; gate same model; 4 worlds x 4 architectures x 2 scenarios x 15 reps via Adaption API.
- **swarm_link**: Swarm governance by information-flow design: peers can share information but cannot move permissions; testable as a protocol for any agent network.
- **Recent kill reasons:**
