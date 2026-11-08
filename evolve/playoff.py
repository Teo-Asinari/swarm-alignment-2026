"""Cross-pool playoff: round-robin of chosen cards before the same 5-reviewer panel."""
import json, sys, itertools, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import evolve as E

def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    entries = [a.split(":") for a in sys.argv[2:]]  # run:cid
    seeds = json.loads((E.HERE / "seeds3.json").read_text())
    ctx = E.ctx_block(seeds, E.digest(E.HERE / "runs"))
    E.BUDGET = 10
    cards = []
    for run, cid in entries:
        c = {x["id"]: x for x in json.load(open(E.HERE / "runs" / run / "final_cards.json"))}[cid]
        cards.append(dict(c, id=f"{run}:{cid}", kills=[]))
    pairs = list(itertools.combinations(range(len(cards)), 2))
    random.seed(7)
    def do(p):
        return p, E.panel(ctx, cards[p[0]], cards[p[1]])
    wins = {c["id"]: 0 for c in cards}; votes = {c["id"]: 0 for c in cards}
    kills = {c["id"]: [] for c in cards}; log = []
    with ThreadPoolExecutor(6) as ex:
        for (i, j), v in ex.map(do, pairs):
            a, b = cards[i]["id"], cards[j]["id"]
            for x in v:
                w = a if x["winner"] == "A" else b
                wins[w] += 1; votes[a] += 1; votes[b] += 1
                kills[a].append(f"[{x['role']}] {x['kill_A']}"); kills[b].append(f"[{x['role']}] {x['kill_B']}")
            log.append({"a": a, "b": b, "verdicts": v})
    (out / "matches.json").write_text(json.dumps(log, indent=1))
    rank = sorted(cards, key=lambda c: -wins[c["id"]] / max(1, votes[c["id"]]))
    lines = [f"# Cross-pool playoff\n\nCost ${E.COST['usd']:.2f}, {E.COST['calls']} calls.\n"]
    for c in rank:
        k = c["id"]
        lines.append(f"## {k}: {wins[k]}/{votes[k]} panel votes ({100*wins[k]/max(1,votes[k]):.0f}%)\n")
        lines += [f"- **{f}**: {c[f]}" for f in E.CARD_FIELDS]
        lines.append("- **Kill reasons:**"); lines += [f"  - {x}" for x in kills[k][-5:]]; lines.append("")
    (out / "playoff.md").write_text("\n".join(lines))
    for c in rank: print(f"{wins[c['id']]:3d}/{votes[c['id']]:3d}  {c['id']}  {c['claim'][:110]}")
    print(E.COST)

if __name__ == "__main__":
    main()
