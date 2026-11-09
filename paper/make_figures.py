"""Figures for the paper from interp/results/*.json (scenario-level bootstrap CIs)."""
import json, collections, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = "../interp/results/"; MODELS = [("gemma-4-31B-it", "Gemma 4 31B"), ("gemma-4-26B-A4B-it", "Gemma 4 26B-A4B"),
                                    ("gemma-4-12B-it", "Gemma 4 12B"), ("Qwen3.8-27B", "Qwen3.8 27B")]
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"; INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3de"
rng = np.random.default_rng(0)
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "font.family": "serif"})

def ci(rows, f=lambda r: r["p"] > .5):
    d = collections.defaultdict(list)
    for r in rows: d[r["scen"]].append(float(f(r)))
    v = np.array([np.mean(x) for x in d.values()]); b = rng.choice(v, (2000, len(v))).mean(1)
    return v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)

W = ["none", "rejected", "passed", "observed", "hearsay"]; WL = ["none", "rejected", "passed", "peer did it", "hearsay"]
fig, axs = plt.subplots(1, 4, figsize=(7, 1.9), sharey=True)
for ax, (m, name) in zip(axs, MODELS):
    G = [r for r in json.load(open(R + m + ".json"))["grid"] if r["role"] == "actor"]
    s = [ci([r for r in G if r["world"] == w]) for w in W]
    x = np.arange(len(W)); mu = [100 * a for a, _, _ in s]
    ax.bar(x, mu, width=0.62, color=BLUE, zorder=2)
    ax.errorbar(x, mu, yerr=[[100 * (a - lo) for a, lo, _ in s], [100 * (hi - a) for a, _, hi in s]], fmt="none", ecolor=INK, lw=0.8, capsize=1.5, zorder=3)
    for xi, v, (_, _, hi) in zip(x, mu, s): ax.text(xi, 100 * hi + 1.5, f"{v:.0f}", ha="center", va="bottom", fontsize=6.5, color=INK)
    ax.set_xticks(x, WL, rotation=40, ha="right"); ax.set_title(name, fontsize=8, color=INK)
    ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_ylim(0, 60)
axs[0].set_ylabel("violation rate (%)")
fig.tight_layout(); fig.savefig("fig_worlds.pdf", bbox_inches="tight"); fig.savefig("/tmp/claude-1000/-home-tasinari-my-repos/b5d233bf-e54f-46cf-a8e5-3039711d411d/scratchpad/w.png", dpi=130, bbox_inches="tight")

# interventions (actor): base / reminder / verdict
C = [("base", "no intervention", BLUE), ("reminder", "rule reminder", ORANGE), ("verdict", "own verdict", AQUA)]
W2 = ["passed", "observed", "hearsay", "signed"]; W2L = ["passed", "peer did it", "hearsay", "signed (legit.)"]
fig, axs = plt.subplots(1, 4, figsize=(7, 1.9), sharey=True)
for ax, (m, name) in zip(axs, MODELS):
    D = json.load(open(R + m + ".json")); base = [r for r in D["grid"] if r["role"] == "actor" and r["me"] == "Dee"]
    x = np.arange(len(W2))
    for k, (c, lab, col) in enumerate(C):
        rs = base if c == "base" else [r for r in D["inter"] if r["cond"] == c]
        mu = [100 * ci([r for r in rs if r["world"] == w])[0] for w in W2]
        ax.bar(x + (k - 1) * 0.27, mu, width=0.25, color=col, label=lab, zorder=2, edgecolor="white", linewidth=0.5)
    ax.set_xticks(x, W2L, rotation=40, ha="right"); ax.set_title(name, fontsize=8, color=INK)
    ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_ylim(0, 105)
axs[0].set_ylabel("act rate (%)"); fig.legend(*axs[0].get_legend_handles_labels(), frameon=False, fontsize=7, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.08))
fig.tight_layout(); fig.savefig("fig_interventions.pdf", bbox_inches="tight"); fig.savefig("/tmp/claude-1000/-home-tasinari-my-repos/b5d233bf-e54f-46cf-a8e5-3039711d411d/scratchpad/i.png", dpi=130, bbox_inches="tight")
print("ok")
