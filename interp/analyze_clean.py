import json, numpy as np, collections
B = json.load(open("steer_batch.json"))
for job in B:
    res = job["res"]; by = collections.defaultdict(dict)
    for x in res: by[x["i"]][x["alpha"]] = x["p_first"]
    alphas = sorted({x["alpha"] for x in res}, key=abs)
    if "down" in job["name"]:
        viol = [i for i in by if by[i][0] > .5]
        s = "  ".join(f"a={a}: viol {np.mean([by[i][a] for i in viol]):.3f} all {np.mean([by[i][a] for i in by]):.3f}" for a in alphas)
        print(f"{job['name']:14s} n_viol={len(viol)}  {s}")
    else:
        print(f"{job['name']:14s} (base 0.083)  " + "  ".join(f"a={a}: {np.mean([by[i][a] for i in by]):.3f}" for a in alphas))
