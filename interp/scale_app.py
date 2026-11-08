"""Scaled study on Modal: 4 open models, 46 scenarios, 6 worlds, 3 roles, prompt interventions,
cross-fitted authorization-axis steering at 4 depths with 8 norm-matched random controls.

  modal run scale_app.py::smoke --model google/gemma-4-31B-it
  modal run scale_app.py::main                       (all models in parallel -> results/<model>.json)
"""
import json, os, random as pyrandom
import modal

MODELS = ["google/gemma-4-31B-it", "google/gemma-4-26B-A4B-it", "google/gemma-4-12B-it", "Qwen/Qwen3.8-27B"]
app = modal.App("swarm-interp-scale")
vol = modal.Volume.from_name("gemma4-interp", create_if_missing=True)
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch==2.6.0", "transformers", "accelerate", "hf_transfer", "numpy", "safetensors", "pillow", "torchvision==0.21.0")
         .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": "/vol/hf"})
         .add_local_python_source("scenarios", "big")
         .add_local_file("scen_new.json", "/root/scen_new.json"))


class Runner:
    def __init__(self, model_id):
        import torch, transformers
        from transformers import AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(model_id)
        self.tok.padding_side = "left"
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        m = None
        names = (["Gemma4ForConditionalGeneration"] if "gemma-4" in model_id else []) + ["AutoModelForCausalLM", "AutoModelForImageTextToText"]
        for n in names:
            try:
                m = getattr(transformers, n).from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="cuda"); break
            except Exception as e:
                print("load via", n, "failed:", str(e)[:200])
        self.model = m.eval()
        cfg = getattr(m.config, "text_config", None) or m.config
        self.n = cfg.num_hidden_layers
        self.layers = next(mod for name, mod in m.named_modules()
                           if isinstance(mod, torch.nn.ModuleList) and len(mod) == self.n and name.endswith("layers"))
        self.bs = 8
        self.vec = None
        print(model_id, "layers", self.n, "transformers", transformers.__version__)

    def text(self, r):
        msgs = [{"role": "system", "content": r["system"]}, {"role": "user", "content": r["user"]}]
        try:
            t = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        except Exception:
            msgs = [{"role": "user", "content": r["system"] + "\n\n" + r["user"]}]
            t = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        return t + r["prefill"]

    def opt(self, r):
        a, b = (self.tok.encode(o, add_special_tokens=False)[0] for o in r["options"])
        assert a != b, r["options"]
        return a, b

    def run(self, rows, layers=None, bs=None):
        """Returns P(first option) per row and (optionally) last-token hidden states at `layers` (hidden_states index)."""
        import numpy as np
        torch = self.torch; bs = bs or self.bs
        P, H = [], []
        for i in range(0, len(rows), bs):
            ch = rows[i:i + bs]
            enc = self.tok([self.text(r) for r in ch], return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
            with torch.no_grad():
                try:
                    out = self.model(**enc, output_hidden_states=layers is not None, logits_to_keep=1)
                except TypeError:
                    out = self.model(**enc, output_hidden_states=layers is not None)
            lg = out.logits[:, -1].float()
            for j, r in enumerate(ch):
                a, b = self.opt(r)
                P.append(torch.softmax(lg[j, [a, b]], 0)[0].item())
            if layers is not None:
                H.append(torch.stack([out.hidden_states[l][:, -1] for l in layers], 1).half().cpu().numpy())
        return np.array(P), (np.concatenate(H) if H else None)

    def steered(self, rows, layer, vec, alpha):
        torch = self.torch
        v = torch.tensor(vec, dtype=torch.bfloat16, device="cuda") * float(alpha)

        def hook(mod, inp, out):
            if isinstance(out, tuple):
                return (out[0] + v,) + tuple(out[1:])
            return out + v
        h = self.layers[layer - 1].register_forward_hook(hook)  # hidden_states[layer] = output of layers[layer-1]
        try:
            return self.run(rows)[0]
        finally:
            h.remove()


def study(model_id, quick=False):
    import numpy as np, big
    rng = np.random.default_rng(0); pyrandom.seed(0)
    R = Runner(model_id)
    log = {"model": model_id, "n_layers": R.n}
    # batching sanity check: batched vs unbatched P must agree
    probe = big.build_grid(1)[:16]
    p1, _ = R.run(probe, bs=1); p8, _ = R.run(probe, bs=8)
    log["batch_maxdiff"] = float(np.abs(p1 - p8).max())
    if log["batch_maxdiff"] > 0.10:
        R.bs = 1
    print("batch maxdiff", log["batch_maxdiff"], "bs", R.bs, flush=True)

    grid = big.build_grid(1 if quick else 3)
    if quick:
        grid = [r for r in grid if r["scen"] in {s["id"] for s in big.S[:8]}]
    LS = sorted(set(list(range(0, R.n + 1, 4)) + [round(R.n * f) for f in (0.4, 0.5, 0.6, 0.75)] + [R.n]))
    SL = [round(R.n * f) for f in (0.4, 0.5, 0.6, 0.75)]
    P, H = R.run(grid, LS)
    print("grid done", len(grid), flush=True)
    meta = [{k: r[k] for k in ("scen", "world", "role", "me", "prop", "cond")} for r in grid]
    for m, p in zip(meta, P):
        m["p"] = float(p)

    # cross-fitted authorization axis from decision-free classifier prompts (2 folds by scenario)
    scen_ids = [s["id"] for s in big.S]; fold_of = {s: i % 2 for i, s in enumerate(scen_ids)}
    idx = lambda f: np.array([i for i, r in enumerate(grid) if f(r)], dtype=int)
    axes, mns, scale = {}, {}, {}
    for li, L in enumerate(LS):
        A = idx(lambda r: r["role"] == "actor" and r["world"] == "signed"); B = idx(lambda r: r["role"] == "actor" and r["world"] == "none")
        scale[L] = float(np.linalg.norm(H[A, li].astype(np.float32).mean(0) - H[B, li].astype(np.float32).mean(0)))
        for f in (0, 1):
            sg = idx(lambda r: r["role"] == "cls" and r["world"] == "signed" and fold_of[r["scen"]] == f)
            nn = idx(lambda r: r["role"] == "cls" and r["world"] == "none" and fold_of[r["scen"]] == f)
            mn = H[nn, li].astype(np.float32).mean(0); ax = H[sg, li].astype(np.float32).mean(0) - mn
            axes[(L, f)], mns[(L, f)] = ax, mn
    proj = np.zeros((len(grid), len(LS)), dtype=np.float32)
    for i, r in enumerate(grid):
        f = 1 - fold_of[r["scen"]]  # axis from the OTHER fold
        for li, L in enumerate(LS):
            ax, mn = axes[(L, f)], mns[(L, f)]
            proj[i, li] = float((H[i, li].astype(np.float32) - mn) @ ax / (ax @ ax))
    # decision direction (actor act vs comply within unauthorized social worlds) and cosines
    cos = {}
    for li, L in enumerate(LS):
        U = [i for i, r in enumerate(grid) if r["role"] == "actor" and r["world"] in big.UNAUTH_SOCIAL]
        y = [i for i in U if P[i] > .5]; n_ = [i for i in U if P[i] <= .5]
        if len(y) >= 3 and len(n_) >= 3:
            d = H[y, li].astype(np.float32).mean(0) - H[n_, li].astype(np.float32).mean(0)
            a = (axes[(L, 0)] + axes[(L, 1)]) / 2
            cos[L] = float(a @ d / np.linalg.norm(a) / np.linalg.norm(d))
    log.update(layers_saved=LS, steer_layers=SL, scale={str(k): v for k, v in scale.items()}, cos_auth_decision={str(k): v for k, v in cos.items()},
               axis_fold_cos={str(L): float(axes[(L, 0)] @ axes[(L, 1)] / np.linalg.norm(axes[(L, 0)]) / np.linalg.norm(axes[(L, 1)])) for L in LS})
    np.savez_compressed(f"/vol/big_{model_id.split('/')[-1]}.npz", h=H, p=P, layers=np.array(LS))
    vol.commit()
    del H

    # two-step prompt interventions on the actor
    fq = big.first_questions(1)
    if quick:
        fq = [r for r in fq if r["scen"] in {s["id"] for s in big.S[:8]}]
    pf, _ = R.run(fq)
    ans = {(r["scen"], r["world"], r["me"], r["prop"], r["cond"]): ("yes" if p > .5 else "no") for r, p in zip(fq, pf)}
    iv = [r for r in big.interventions(ans, 1) if (r["scen"], r["world"], r["me"], r["prop"], "verdict") in ans]
    pi, _ = R.run(iv)
    first = [dict(scen=r["scen"], world=r["world"], me=r["me"], prop=r["prop"], cond=r["cond"], p=float(p)) for r, p in zip(fq, pf)]
    inter = [dict(scen=r["scen"], world=r["world"], me=r["me"], prop=r["prop"], cond=r["cond"], p=float(p)) for r, p in zip(iv, pi)]
    print("interventions done", len(iv), flush=True)

    # steering: down on violators, up on 'none' actor prompts; cross-fitted axis; 8 random controls
    act_rows = [(i, r) for i, r in enumerate(grid) if r["role"] == "actor"]
    viol = [(i, r) for i, r in act_rows if not r["authorized"] and P[i] > .5]
    pyrandom.shuffle(viol); viol = viol[:24 if quick else 120]
    nonep = [(i, r) for i, r in act_rows if r["world"] == "none" and P[i] <= .5]
    pyrandom.shuffle(nonep); nonep = nonep[:16 if quick else 96]
    steer = []
    rand_dirs = rng.standard_normal((6, H_dim := axes[(SL[0], 0)].shape[0])).astype(np.float32)
    rand_dirs /= np.linalg.norm(rand_dirs, axis=1, keepdims=True)
    for L in SL:
        for tag, tgt, alphas in (("down", viol, [-0.5, -1.0, -1.5]), ("up", nonep, [0.5, 1.0, 1.5])):
            if not tgt:
                continue
            for f in (0, 1):  # rows whose scenario is in fold 1-f get the axis from fold f
                sub = [(i, r) for i, r in tgt if fold_of[r["scen"]] != f]
                if not sub:
                    continue
                ax = axes[(L, f)]; vec = ax / np.linalg.norm(ax) * scale[L]
                for a in alphas:
                    ps = R.steered([r for _, r in sub], L, vec, a)
                    steer += [dict(layer=L, dir=tag, kind="axis", alpha=a, i=int(i), scen=r["scen"], world=r["world"], p0=float(P[i]), p=float(p))
                              for (i, r), p in zip(sub, ps)]
            for k in range(6 if not quick else 2):
              for a in (0.5, 1.0, 1.5):
                ps = R.steered([r for _, r in tgt], L, rand_dirs[k] * scale[L], a)
                steer += [dict(layer=L, dir=tag, kind=f"rand{k}", alpha=a, i=int(i), scen=r["scen"], world=r["world"], p0=float(P[i]), p=float(p))
                          for (i, r), p in zip(tgt, ps)]
            print("steer", L, tag, flush=True)
    log.update(grid=meta, proj=proj.tolist(), first=first, inter=inter, steer=steer)
    return log


@app.function(image=image, gpu="H100", volumes={"/vol": vol}, timeout=4 * 3600)
def run_model(model_id: str, quick: bool = False):
    out = study(model_id, quick)
    vol.commit()
    return out


@app.local_entrypoint()
def smoke(model: str = MODELS[0]):
    res = run_model.remote(model, True)
    os.makedirs("results", exist_ok=True)
    json.dump(res, open(f"results/smoke_{model.split('/')[-1]}.json", "w"))
    print("batch maxdiff", res["batch_maxdiff"], "cos", res["cos_auth_decision"])


@app.local_entrypoint()
def main(models: str = ",".join(MODELS)):
    os.makedirs("results", exist_ok=True)
    ms = models.split(",")
    for m, res in zip(ms, run_model.map(ms, [False] * len(ms), return_exceptions=True)):
        if isinstance(res, Exception):
            print("FAILED", m, repr(res)[:500]); continue
        json.dump(res, open(f"results/{m.split('/')[-1]}.json", "w"))
        print("saved", m)
