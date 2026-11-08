import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import evolve as E
E.BUDGET = 5
plan = Path(sys.argv[1]).read_text()
prior = (E.HERE / "runs" / "prior_art.md").read_text()
seeds = json.loads((E.HERE / "seeds3.json").read_text())
ctx = E.ctx_block(seeds, prior)
AXES = {
 "relevance": ("glm-5.2", "Attack its RELEVANCE to the hackathon tracks (Science of Agent Networks; Multi-Agent Oversight and Control). Is this really multi-agent/swarm research or single-agent prompt sensitivity relabelled? Would judges care?"),
 "prior_art": ("qwen3.5-397b", "Attack its PRIOR ART. Name specific known results (LLM conformity, social proof, descriptive norms, precedent/authority prompts, many-shot, jailbreak via fake history, norm reminders, Cialdini focus theory, sycophancy) that already establish these findings. Be concrete."),
 "impact": ("deepseek-v4-flash", "Attack its IMPACT and validity. What confounds, underpowered cells, model-specificity, floor/ceiling, prompt-wording artifacts and interpretability pitfalls would make a reviewer discount the result? What would make the result matter for safety?"),
 "novelty": ("gemma-4-31b-it", "Attack its CONCEPTUAL NOVELTY. Is 'the record is the rule' a genuinely new idea or a renaming of in-context learning / few-shot imitation / social proof? What would make it conceptually new?"),
 "chair": ("glm-5.2", "You are the program-committee chair. Give the single most likely reason this gets a low score, and the single highest-leverage change to make tonight."),
}
INSTR = ("You are a hostile but fair senior reviewer. {p} Return JSON: "
         '{{"score_1_to_10": int, "fatal_holes": [str, ...max 4], "fixable_holes": [str, ...max 4], "best_fix_tonight": str}}')
def do(k):
    m, p = AXES[k]
    try:
        return k, m, E.call_json(m, INSTR.format(p=p), f"{ctx}\n\nPLAN UNDER REVIEW:\n{plan}")
    except Exception as e:
        return k, m, {"error": str(e)}
with ThreadPoolExecutor(5) as ex:
    res = list(ex.map(do, AXES))
out = []
for k, m, r in res:
    out.append(f"## {k} ({m}) — score {r.get('score_1_to_10')}\n")
    for h in ("fatal_holes", "fixable_holes"):
        out.append(f"**{h}**"); out += [f"- {x}" for x in r.get(h, [])]
    out.append(f"**best fix tonight:** {r.get('best_fix_tonight')}\n")
Path(sys.argv[2]).write_text("\n".join(out)); print("\n".join(out)); print(E.COST)
