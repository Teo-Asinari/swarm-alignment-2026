"""Hypothesis evolver: GA exploration with an adversarial LLM panel, then a hill climb.

Phases:
  digest  - compress research notes into a prior-art list (cached).
  evolve  - seed population, pairwise adversarial panel -> Elo, selection, variation.
  climb   - critic/reviser hill climb on the top cards; accept only on panel majority.
Outputs go to --out: cards.jsonl, matches.jsonl, leaderboard.md, cost.json.
"""
import argparse, json, os, random, re, sys, threading, time, traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from adaption import Adaption

HERE = Path(__file__).resolve().parent
KEY_FILE = Path(os.environ.get("ADAPTION_KEY_FILE", "adaption.key"))
NOTES_DIR = Path("/home/tasinari/my_repos/research_notes")

CRITICS = ["glm-5.2", "deepseek-v4-flash", "qwen3.5-397b"]
T0 = __import__("time").time()
GENERATORS = ["glm-5.2", "qwen3.5-397b", "deepseek-v4-flash"]
REVIEWERS = {
    "prior_art": ("glm-5.2", "You are a prior-art hawk. Judge which hypothesis is more genuinely NEW given the prior-art list and your own knowledge. Already-published behaviour, standard methods applied to an obvious new domain, or replications of known human results count as NOT new."),
    "falsifiability": ("qwen3.5-397b", "You are a falsificationist. Judge which hypothesis makes a sharper, riskier prediction with a concrete result that would refute it. Penalize framings where every outcome confirms the thesis."),
    "confounds": ("deepseek-v4-flash", "You are a confound hunter. Judge which hypothesis's experiment better rules out alternative explanations (information vs permission vs detection vs wording vs length, lexical artifacts, circular directions, probe reading the request)."),
    "feasibility": ("gemma-4-31b-it", "You are a feasibility realist. Judge which hypothesis can produce a credible, well-powered result within ~1 day using one 16 GB GPU and cheap hosted open-weight models. Penalize fine-tuning sweeps, single seeds, huge models, unvalidated pipelines."),
    "importance": ("glm-53-flash", "You are a swarm-alignment judge. Judge which hypothesis matters more for multi-agent AI safety and is genuinely about agent networks or multi-agent oversight rather than single-agent work relabelled. Also weigh conceptual depth."),
}
CARD_FIELDS = ["claim", "mechanism", "prediction", "falsifier", "experiment", "swarm_link"]
MAX_FIELD_WORDS = 70

_client = None
_lock = threading.Lock()
COST = {"usd": 0.0, "calls": 0, "errors": 0}
BUDGET = 25.0


def client():
    global _client
    if _client is None:
        _client = Adaption(api_key=KEY_FILE.read_text().strip(), timeout=150, max_retries=1)
    return _client


FALLBACK = {"deepseek-v4-flash": "glm-53-flash", "qwen3.5-397b": "glm-5.2", "gemma-4-31b-it": "gemma-4-26b-a4b-it",
            "glm-53-flash": "glm-5.2", "glm-5.2": "qwen3.5-397b", "gemma-4-26b-a4b-it": "glm-53-flash"}


def call(model, instructions, prompt, retries=3):
    for attempt in range(retries):
        if attempt == retries - 1 and model in FALLBACK:
            model = FALLBACK[model]
        if COST["usd"] > BUDGET:
            raise RuntimeError(f"budget exceeded: ${COST['usd']:.2f}")
        try:
            # stream to keep the gateway connection alive (non-streamed calls 504 after ~60 s)
            text, usage = [], None
            for ev in client().responses.create(model=model, instructions=instructions, input=prompt, stream=True):
                t = getattr(ev, "type", "")
                if t == "response.output_text.delta":
                    text.append(ev.delta)
                elif t in ("response.completed", "response.incomplete"):
                    usage = getattr(ev.response, "usage", None)
                elif t in ("response.failed", "error"):
                    raise RuntimeError(f"stream {t}: {str(ev)[:200]}")
            with _lock:
                COST["calls"] += 1
                COST["usd"] += float(getattr(usage, "cost", 0) or 0)
            out = "".join(text)
            if not out.strip():
                raise RuntimeError("empty output")
            return out
        except Exception as e:
            with _lock:
                COST["errors"] += 1
            if attempt == retries - 1:
                raise
            time.sleep(61 if '429' in str(e) else 2 * (attempt + 1) + random.random())


def parse_json(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    m = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    if m:
        text = m.group(1)
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = text.find(opener), text.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(text[i:j + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("no JSON in: " + text[:300])


def call_json(model, instructions, prompt, tries=2):
    last = None
    for _ in range(tries):
        try:
            return parse_json(call(model, instructions + "\nRespond with JSON only, no prose.", prompt))
        except ValueError as e:
            last = e
    raise last


def trim(s):
    words = str(s).split()
    return " ".join(words[:MAX_FIELD_WORDS]) + (" ..." if len(words) > MAX_FIELD_WORDS else "")


def clean_card(d):
    return {f: trim(d.get(f, "")) for f in CARD_FIELDS}


def card_text(c):
    return "\n".join(f"{f.upper()}: {c[f]}" for f in CARD_FIELDS)


# ---------------------------------------------------------------- digest
def digest(out):
    path = out / "prior_art.md"
    if path.exists():
        return path.read_text()
    files = sorted(NOTES_DIR.glob("*/*.md"))
    instr = ("Extract a compact prior-art list from research notes. One line per distinct paper/project/post: "
             "'- <short cite> (<id/venue>): <what was done and found, <=25 words>'. Keep numbers. Skip duplicates and background textbooks unless central. Max 40 lines.")

    def one(f):
        try:
            return call("glm-5.2", instr, f.read_text()[:40000])
        except Exception as e:
            print("digest skip", f.name, e, file=sys.stderr)
            return ""

    with ThreadPoolExecutor(6) as ex:
        parts = list(ex.map(one, files))
    merged = call("glm-5.2",
                  "Merge these prior-art lists into one deduplicated list, grouped under short headings. Keep each line <=30 words with key numbers. Max 120 lines. Output markdown only.",
                  "\n\n".join(parts))
    path.write_text(merged)
    return merged


CONCEPTS = [
    "quorum sensing (bacteria act only once signal concentration crosses a threshold)",
    "immune tolerance and autoimmunity (self/non-self boundary learned, then misfires)",
    "epidemic thresholds R0 and herd immunity",
    "phase transitions and critical slowing down before a tipping point",
    "Ising model / spin glasses (local alignment produces global order or frustration)",
    "Gricean implicature (what is NOT said carries meaning)",
    "speech-act theory: performatives that change the world by being uttered",
    "legal doctrine of acquiescence and estoppel (silence creates rights)",
    "common knowledge vs mutual knowledge (Aumann, coordinated attack problem)",
    "costly signaling / handicap principle",
    "Byzantine fault tolerance (honest majority thresholds)",
    "stigmergy (coordination via traces left in the environment, ants/termites)",
    "ecological succession and keystone species",
    "Goodhart's law and Campbell's law",
    "normalization of deviance (Vaughan, Challenger)",
    "Overton window",
    "pluralistic ignorance (everyone privately rejects a norm they think others accept)",
    "information cascades and herding (Bikhchandani)",
    "moral licensing and moral credentialing",
    "broken-windows theory",
    "Schelling focal points",
    "error-correcting codes and redundancy",
    "predictive processing / free-energy principle (agents minimise surprise)",
    "Hebbian learning (cells that fire together wire together)",
    "prion-like misfolding templating (one misfolded unit converts neighbours)",
    "autocatalytic sets and origin-of-life chemistry",
    "market microstructure: bid-ask spread, adverse selection, informed traders",
    "regulatory capture",
    "principal-agent slack and moral hazard",
    "ritual and liturgy as commitment devices",
    "games of incomplete information with cheap talk (Crawford-Sobel)",
    "evolutionary stable strategies and invasion fitness",
    "Red Queen dynamics / co-evolutionary arms races",
    "hysteresis (state depends on history; path-dependent return)",
    "Simpson's paradox / aggregation reversals",
    "the tragedy of the anticommons",
    "linguistic drift and semantic bleaching (words lose force with use)",
    "inoculation theory (weak exposure confers resistance)",
    "mechanism design: revelation principle, incentive compatibility",
    "Kuramoto synchronisation of coupled oscillators",
    "sleeper cells / latent states activated by a trigger",
    "double-entry bookkeeping and audit trails",
    "trust as a decaying resource (half-life of credibility)",
    "the Abilene paradox (group does what nobody wants)",
    "ironic process theory (suppressing a thought strengthens it)",
    "gerrymandering: boundary drawing changes aggregate outcome",
]


# ---------------------------------------------------------------- population
class Pop:
    def __init__(self, out):
        self.out = out
        self.cards = {}
        self.n = 0

    def add(self, fields, gen, op, parents=(), model=None):
        self.n += 1
        cid = f"c{self.n:03d}"
        c = dict(clean_card(fields), id=cid, gen=gen, op=op, parents=list(parents), model=model,
                 elo=1000.0, matches=0, kills=[], alive=True)
        self.cards[cid] = c
        with open(self.out / "cards.jsonl", "a") as f:
            f.write(json.dumps(c) + "\n")
        return c

    def alive(self):
        return [c for c in self.cards.values() if c["alive"]]


def ctx_block(seeds, prior):
    fm = "\n".join("- " + x for x in seeds["known_failure_modes"])
    return f"CONTEXT:\n{seeds['context']}\n\nKNOWN FAILURE MODES:\n{fm}\n\nPRIOR ART:\n{prior}"


CARD_SCHEMA = ('Each hypothesis card is a JSON object with string fields: "claim" (one sentence), "mechanism", '
               '"prediction" (a direction or number), "falsifier" (the result that kills it), "experiment" '
               '(doable in <=1 day with the stated resources), "swarm_link". Each field <=60 words.')


def gen_cards(model, ctx, k, negatives):
    instr = ("You are a creative but rigorous AI-safety researcher generating research hypotheses. " + CARD_SCHEMA +
             " Aim for conceptual novelty, not incremental tweaks. Avoid the known failure modes.")
    seeds_c = [random.sample(CONCEPTS, 2) for _ in range(k)]
    lens = "\n".join(f"- card {i+1}: fuse '{a}' with '{b}'" for i, (a, b) in enumerate(seeds_c))
    prompt = (f"{ctx}\n\nKILLED IDEAS (do not repeat; learn from why they died):\n{negatives}\n\n"
              f"CONCEPTUAL LENSES (one pair per card; transplant the STRUCTURE of each concept into the RESEARCH OBJECTIVE, "
              f"not just its vocabulary; drop a lens only if it truly cannot yield a testable idea):\n{lens}\n\n"
              f"Generate {k} diverse hypothesis cards as a JSON array.")
    arr = call_json(model, instr, prompt)
    return [a for a in (arr if isinstance(arr, list) else [arr]) if isinstance(a, dict) and a.get("claim")]


VAR_OPS = {
    "mutate_sharpen": "Make this hypothesis sharper and riskier: a more precise prediction and a cleaner falsifier.",
    "mutate_invert": "Invert or contradict the core claim to produce a plausible rival hypothesis worth testing.",
    "mutate_mechanism": "Keep the phenomenon but propose a different underlying mechanism, with a test that distinguishes it.",
    "mutate_scale": "Move the hypothesis to a different scale of the multi-agent system (single decision -> network/population dynamics, or the reverse) while keeping it testable in a day.",
    "fuse_concept": "FUSION: Transplant the causal STRUCTURE of the distant concept(s) below into this hypothesis, so the mechanism and the experiment change, not just the vocabulary. The result should predict something the original could not.",
    "repair": "Rewrite this hypothesis to answer the reviewers' kill reasons below, without making it vaguer.",
}


def vary(op, model, ctx, a, b=None):
    instr = "You are an AI-safety researcher refining hypotheses. " + CARD_SCHEMA + " Return ONE card as a JSON object."
    if op == "crossover":
        prompt = (f"{ctx}\n\nPARENT A:\n{card_text(a)}\n\nPARENT B:\n{card_text(b)}\n\n"
                  "Combine the strongest idea of A with the strongest idea or experiment of B into one coherent, novel hypothesis.")
    elif op == "fuse_distant":
        c = random.choice(CONCEPTS)
        prompt = (f"{ctx}\n\nPARENT A:\n{card_text(a)}\n\nPARENT B (deliberately the most DIFFERENT card in the population):\n{card_text(b)}\n\n"
                  f"DISTANT CONCEPT: {c}\n\nFuse A, B and the concept into ONE hypothesis whose mechanism needs all three; "
                  "it should not be reducible to either parent. Keep it testable in a day.")
    elif op == "wildcard":
        cs = random.sample(CONCEPTS, 2)
        prompt = (f"{ctx}\n\nThe current best ideas are (do NOT stay near them):\n{a}\n\n"
                  f"RANDOM CONCEPTS: '{cs[0]}' and '{cs[1]}'.\n"
                  "Be contrarian: using the structure of these concepts, propose one hypothesis serving the RESEARCH OBJECTIVE in "
                  "the context that the field would find surprising, "
                  "that most researchers would bet against, but that is testable in a day.")
    elif op == "fuse_concept":
        cs = random.sample(CONCEPTS, random.choice([1, 2]))
        kills = "\n".join("- " + k for k in a["kills"][-4:]) or "(none yet)"
        prompt = (f"{ctx}\n\nHYPOTHESIS:\n{card_text(a)}\n\nREVIEWER KILL REASONS:\n{kills}\n\n"
                  f"DISTANT CONCEPT(S): {'; '.join(cs)}\n\nTASK: {VAR_OPS[op]}")
    else:
        kills = "\n".join("- " + k for k in a["kills"][-6:]) or "(none yet)"
        prompt = f"{ctx}\n\nHYPOTHESIS:\n{card_text(a)}\n\nREVIEWER KILL REASONS:\n{kills}\n\nTASK: {VAR_OPS[op]}"
    return call_json(model, instr, prompt)


# ---------------------------------------------------------------- judging
def judge(role, ctx, a, b):
    model, persona = REVIEWERS[role]
    instr = (persona + " You are adversarial: for EACH hypothesis first state its single strongest kill reason "
             "(the objection most likely to sink it), then pick the better one on your criterion. "
             'Return JSON: {"kill_A": str, "kill_B": str, "winner": "A" or "B", "margin": 1-3}.')
    flip = random.random() < 0.5  # randomize position to cancel order bias
    x, y = (b, a) if flip else (a, b)
    prompt = f"{ctx}\n\nHYPOTHESIS A:\n{card_text(x)}\n\nHYPOTHESIS B:\n{card_text(y)}"
    r = call_json(model, instr, prompt)
    w = str(r.get("winner", "")).strip().upper()[:1]
    if w not in ("A", "B"):
        raise ValueError("bad winner")
    ka, kb = r.get("kill_A", ""), r.get("kill_B", "")
    if flip:
        w = "B" if w == "A" else "A"
        ka, kb = kb, ka
    try:
        margin = max(1, min(3, int(r.get("margin", 1))))
    except (TypeError, ValueError):
        margin = 1
    return {"role": role, "winner": w, "margin": margin, "kill_A": trim(ka), "kill_B": trim(kb)}


def panel(ctx, a, b):
    with ThreadPoolExecutor(len(REVIEWERS)) as ex:
        futs = [ex.submit(judge, role, ctx, a, b) for role in REVIEWERS]
        out = []
        for f in futs:
            try:
                out.append(f.result())
            except Exception as e:
                print("judge error:", e, file=sys.stderr)
    return out


def elo_update(pop, a, b, verdicts, k=24):
    for v in verdicts:
        ea = 1 / (1 + 10 ** ((b["elo"] - a["elo"]) / 400))
        sa = 1.0 if v["winner"] == "A" else 0.0
        delta = k * (0.5 + 0.25 * v["margin"]) * (sa - ea)
        a["elo"] += delta
        b["elo"] -= delta
        a["kills"].append(f"[{v['role']}] {v['kill_A']}")
        b["kills"].append(f"[{v['role']}] {v['kill_B']}")
    a["matches"] += 1
    b["matches"] += 1
    with open(pop.out / "matches.jsonl", "a") as f:
        f.write(json.dumps({"a": a["id"], "b": b["id"], "verdicts": verdicts}) + "\n")


def run_matches(pop, ctx, cards, per_card, workers):
    pairs = []
    ids = [c["id"] for c in cards]
    for _ in range(per_card):
        random.shuffle(ids)
        pairs += [(ids[i], ids[i + 1]) for i in range(0, len(ids) - 1, 2)]

    def do(p):
        a, b = pop.cards[p[0]], pop.cards[p[1]]
        return a, b, panel(ctx, a, b)

    with ThreadPoolExecutor(workers) as ex:
        for a, b, v in ex.map(do, pairs):
            if v:
                with _lock:
                    elo_update(pop, a, b, v)


def similar(a, b):
    wa = set(re.findall(r"[a-z]{4,}", a["claim"].lower()))
    wb = set(re.findall(r"[a-z]{4,}", b["claim"].lower()))
    return len(wa & wb) / max(1, len(wa | wb))


# ---------------------------------------------------------------- phases
def evolve(args, pop, ctx, seeds):
    negatives = "\n".join(f"- {c['claim']} :: {'; '.join(c.get('kill_reasons', []))}"
                          for c in seeds["cards"] if c["claim"].startswith("[KILLED"))
    for c in seeds["cards"]:
        if not c["claim"].startswith("[KILLED"):
            pop.add(c, 0, "seed")
    need = args.pop - len(pop.alive())
    per = max(1, -(-need // len(GENERATORS)))
    with ThreadPoolExecutor(len(GENERATORS)) as ex:
        futs = {ex.submit(gen_cards, m, ctx, per, negatives): m for m in GENERATORS}
        for f, m in futs.items():
            try:
                for d in f.result():
                    pop.add(d, 0, "generate", model=m)
            except Exception as e:
                print("gen error:", m, e, file=sys.stderr)

    for g in range(1, args.gens + 1):
        alive = pop.alive()
        run_matches(pop, ctx, alive, args.matches, args.workers)
        alive.sort(key=lambda c: -c["elo"])
        # diversity: drop near-duplicates of better cards
        for i, c in enumerate(alive):
            if any(similar(c, d) > 0.55 for d in alive[:i] if d["alive"]):
                c["alive"] = False
        alive = [c for c in alive if c["alive"]]
        keep = alive[: max(2, args.pop // 2)]
        for c in alive[len(keep):]:
            c["alive"] = False
        print(f"gen {g}: best {keep[0]['id']} elo {keep[0]['elo']:.0f} | ${COST['usd']:.2f} {COST['calls']} calls", flush=True)
        write_board(pop, args.out)
        if g == args.gens or (args.minutes and time.time() - T0 > 0.65 * 60 * args.minutes):
            break
        # variation
        jobs = []
        n_child = args.pop - len(keep)
        best_text = "\n".join("- " + c["claim"] for c in keep[:5])
        for i in range(n_child):
            r = random.random()
            m = random.choice(GENERATORS)
            if i < args.immigrants:
                jobs.append(("wildcard", m, best_text, None, []))
            elif r < args.fusion:
                a = tournament(keep)
                if random.random() < 0.4:
                    b = min((c for c in keep if c is not a), key=lambda c: similar(a, c))
                    jobs.append(("fuse_distant", m, a, b, [a["id"], b["id"]]))
                else:
                    jobs.append(("fuse_concept", m, a, None, [a["id"]]))
            elif r < args.fusion + 0.15:
                a, b = tournament(keep), tournament(keep)
                if a is b:
                    b = random.choice(keep)
                jobs.append(("crossover", m, a, b, [a["id"], b["id"]]))
            elif r < args.fusion + 0.35:
                a = tournament(keep)
                jobs.append(("repair", m, a, None, [a["id"]]))
            else:
                a = tournament(keep)
                op = random.choice(["mutate_sharpen", "mutate_invert", "mutate_mechanism", "mutate_scale"])
                jobs.append((op, m, a, None, [a["id"]]))

        def do(j):
            op, m, a, b, parents = j
            return j, vary(op, m, ctx, a, b)

        with ThreadPoolExecutor(args.workers) as ex:
            futs = [ex.submit(do, j) for j in jobs]
            for f in futs:
                try:
                    (op, m, a, b, parents), d = f.result()
                    child = pop.add(d, g, op, parents, m)
                    # children start at mean parent elo to reduce cold-start noise
                    ps = [pop.cards[p]["elo"] for p in parents]
                    child["elo"] = sum(ps) / len(ps) if ps else 1000.0
                except Exception as e:
                    print("vary error:", e, file=sys.stderr)


def tournament(cards, k=3):
    return max(random.sample(cards, min(k, len(cards))), key=lambda c: c["elo"])


def climb(args, pop, ctx):
    tops = sorted(pop.alive(), key=lambda c: -c["elo"])[: args.climb_top]
    with ThreadPoolExecutor(len(tops)) as ex:
        finals = list(ex.map(lambda st: climb_one(args, pop, ctx, st), tops))
    return finals


def climb_one(args, pop, ctx, start):
    if True:
        cur, fails, rnd = start, 0, 0
        while fails < args.patience and rnd < args.climb_rounds:
            rnd += 1
            try:
                crit = call_json(CRITICS[rnd % len(CRITICS)],
                                 "You are the harshest reviewer. Name the SINGLE strongest objection that would sink this hypothesis "
                                 "(novelty, confound, falsifiability, feasibility, or swarm relevance). "
                                 'Return JSON: {"objection": str, "minimal_fix_hint": str}.',
                                 f"{ctx}\n\nHYPOTHESIS:\n{card_text(cur)}")
                cand_d = call_json("qwen3.5-397b",
                                   "You revise research hypotheses. " + CARD_SCHEMA +
                                   " Make the SMALLEST change that answers the objection without making the hypothesis vaguer "
                                   "or less risky. Return ONE card as a JSON object.",
                                   f"{ctx}\n\nHYPOTHESIS:\n{card_text(cur)}\n\nOBJECTION: {crit.get('objection')}\n"
                                   f"HINT: {crit.get('minimal_fix_hint')}")
            except Exception as e:
                print("climb error:", e, file=sys.stderr)
                fails += 1
                continue
            with _lock:
                cand = pop.add(cand_d, 99, "climb", [cur["id"]], "qwen3.5-397b")
            cand["alive"] = False
            cand["objection"] = trim(crit.get("objection", ""))
            v = panel(ctx, cand, cur)
            wins = sum(1 for x in v if x["winner"] == "A")
            with open(pop.out / "climb.jsonl", "a") as f:
                f.write(json.dumps({"from": cur["id"], "cand": cand["id"], "objection": cand["objection"],
                                    "wins": wins, "of": len(v), "verdicts": v}) + "\n")
            print(f"climb {start['id']} r{rnd}: {cand['id']} wins {wins}/{len(v)}", flush=True)
            if wins * 2 > len(v):
                cand["climb_root"] = start["id"]
                cur, fails = cand, 0
                with _lock:
                    start["climb_best"] = cur["id"]
                    write_board(pop, args.out)
            else:
                fails += 1
        return (start, cur)


# ---------------------------------------------------------------- output
def write_board(pop, out, finals=None):
    alive = sorted(pop.alive(), key=lambda c: -c["elo"])
    lines = [f"# Hypothesis leaderboard\n\nCost so far: ${COST['usd']:.2f} over {COST['calls']} calls "
             f"({COST['errors']} errors). Cards created: {pop.n}.\n"]
    if finals is None:
        finals = [(c, pop.cards[c["climb_best"]]) for c in pop.cards.values() if c.get("climb_best")]
    if finals:
        lines.append("## Hill-climbed finalists\n")
        for i, (start, cur) in enumerate(finals, 1):
            lines.append(f"### Finalist {i}: {cur['id']} (climbed from {start['id']}, Elo {start['elo']:.0f})\n")
            lines += [f"- **{f}**: {cur[f]}" for f in CARD_FIELDS]
            ks = [k for k in start["kills"]][-5:]
            lines.append("- **Surviving objections (from panel):**")
            lines += [f"  - {k}" for k in ks]
            lines.append("")
    lines.append("## Final population by Elo\n")
    for c in alive:
        lines.append(f"### {c['id']} — Elo {c['elo']:.0f} ({c['matches']} matches, gen {c['gen']}, {c['op']}"
                     f"{', parents ' + ','.join(c['parents']) if c['parents'] else ''})\n")
        lines += [f"- **{f}**: {c[f]}" for f in CARD_FIELDS]
        lines.append("- **Recent kill reasons:**")
        lines += [f"  - {k}" for k in c["kills"][-3:]]
        lines.append("")
    (out / "leaderboard.md").write_text("\n".join(lines))
    (out / "cost.json").write_text(json.dumps(COST))
    with open(out / "final_cards.json", "w") as f:
        json.dump(list(pop.cards.values()), f, indent=1)


def main():
    global BUDGET
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--pop", type=int, default=16)
    ap.add_argument("--gens", type=int, default=5)
    ap.add_argument("--matches", type=int, default=3, help="matches per card per generation")
    ap.add_argument("--climb-top", type=int, default=3)
    ap.add_argument("--climb-rounds", type=int, default=8)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=25.0)
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--seeds", default="seeds.json")
    ap.add_argument("--fusion", type=float, default=0.45, help="share of children made by concept fusion")
    ap.add_argument("--immigrants", type=int, default=2, help="fresh random-concept wildcards per generation")
    ap.add_argument("--minutes", type=float, default=0, help="wall-clock budget; GA stops at 65%, rest for climbing")
    args = ap.parse_args()
    BUDGET = args.budget
    random.seed(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    args.out = out
    seeds = json.loads((HERE / args.seeds).read_text())
    (HERE / "runs").mkdir(exist_ok=True)
    prior = digest(HERE / "runs")
    ctx = ctx_block(seeds, prior)
    pop = Pop(out)
    try:
        evolve(args, pop, ctx, seeds)
        finals = climb(args, pop, ctx)
        write_board(pop, out, finals)
    except Exception:
        traceback.print_exc()
        write_board(pop, out)
        sys.exit(1)
    print(f"done: ${COST['usd']:.2f}, {COST['calls']} calls, {COST['errors']} errors", flush=True)


if __name__ == "__main__":
    main()
