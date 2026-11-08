import numpy as np, json, collections
from scenarios import build
rows = build(); d = np.load("acts.npz"); P = d["p"]; H = d["h"].astype(np.float32)  # [N, 61, 5376]
for i, r in enumerate(rows): r["p"] = float(P[i]); r["i"] = i
# behaviour
print("Mean P(act|approve):")
for role in ("actor", "judge"):
    print(f" {role}: " + "  ".join(f"{w}={np.mean([r['p'] for r in rows if r['role']==role and r['world']==w]):.2f}" for w in ("none","passed","hearsay","signed")))
viol = collections.Counter((r["role"], r["world"], r["scen"]) for r in rows if not r["authorized"] and r["p"] > .5)
print("Unauthorized 'yes' decisions (role, world, scen): count of 6 variants"); [print("  ", k, v) for k, v in sorted(viol.items())]
L = H.shape[1]
def groups(role):
    g = {}
    U = [r for r in rows if r["role"] == role and not r["authorized"]]
    g["yes_social"] = [r for r in U if r["world"] != "none" and r["p"] > .5]
    g["no_social"] = [r for r in U if r["world"] != "none" and r["p"] <= .5]
    g["none"] = [r for r in U if r["world"] == "none" and r["p"] <= .5]
    g["signed"] = [r for r in rows if r["role"] == role and r["authorized"]]
    return g
out = {}
for src in ("actor", "judge"):           # role whose none/signed means define the axis
    for tgt in ("actor", "judge"):       # role whose prompts are projected
        g = groups(tgt); res = collections.defaultdict(list)
        for l in range(L):
            for name, rs in g.items():
                if not rs: continue
                ts = []
                for r in rs:  # leave-one-scenario-out axis
                    tr_none = [q["i"] for q in rows if q["role"]==src and q["world"]=="none" and q["scen"]!=r["scen"] and q["p"]<=.5]
                    tr_sig = [q["i"] for q in rows if q["role"]==src and q["world"]=="signed" and q["scen"]!=r["scen"]]
                    mn, ms = H[tr_none, l].mean(0), H[tr_sig, l].mean(0); ax = ms - mn
                    ts.append(float((H[r["i"], l] - mn) @ ax / (ax @ ax)))
                res[name].append(float(np.mean(ts)))
        out[f"{src}_axis->{tgt}"] = {k: v for k, v in res.items()}
        print(f"\naxis from {src} (0=unauthorized none, 1=signed), prompts of {tgt}; n:", {k: len(v) for k, v in g.items()})
        for l in range(0, L, 4):
            print(f"  L{l:02d} " + "  ".join(f"{k}={res[k][l]:+.2f}" for k in res))
json.dump(out, open("axis_results.json", "w"))
