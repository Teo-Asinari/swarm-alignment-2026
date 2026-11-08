"""Gemma 4 31B on Modal: decision logits + residual activations, and steering.

  modal run modal_app.py::smoke
  modal run modal_app.py::extract          -> volume gemma4-interp:/out/acts.npz
  modal run modal_app.py::steer --spec steer_spec.npz
"""
import io, json
import modal

MODEL = "google/gemma-4-31B-it"
app = modal.App("swarm-interp")
vol = modal.Volume.from_name("gemma4-interp", create_if_missing=True)
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("torch==2.6.0", "transformers", "accelerate", "hf_transfer", "numpy", "safetensors")
         .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": "/vol/hf"})
         .add_local_python_source("scenarios"))


@app.cls(image=image, gpu="A100-80GB", volumes={"/vol": vol}, timeout=3600, scaledown_window=300)
class G:
    @modal.enter()
    def load(self):
        import torch, transformers
        from transformers import AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(MODEL)
        cls = getattr(transformers, "Gemma4ForConditionalGeneration", None) or transformers.AutoModelForImageTextToText
        self.model = cls.from_pretrained(MODEL, torch_dtype=torch.bfloat16, device_map="cuda")
        self.model.eval()
        vol.commit()
        n = self.model.config.text_config.num_hidden_layers
        self.layers = None
        for name, m in self.model.named_modules():
            if isinstance(m, torch.nn.ModuleList) and len(m) == n and name.endswith("layers"):
                self.layers = m; self.layers_name = name; break
        print("transformers", transformers.__version__, "layers at", self.layers_name, n)

    def text(self, row):
        msgs = [{"role": "system", "content": row["system"]}, {"role": "user", "content": row["user"]}]
        try:
            t = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        except Exception:
            msgs = [{"role": "user", "content": row["system"] + "\n\n" + row["user"]}]
            t = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return t + row["prefill"]

    def opt_ids(self, row):
        return [self.tok.encode(o, add_special_tokens=False)[0] for o in row["options"]]

    def forward(self, row, want_hidden):
        torch = self.torch
        ids = self.tok(self.text(row), return_tensors="pt", add_special_tokens=False).to("cuda")
        with torch.no_grad():
            out = self.model(**ids, output_hidden_states=want_hidden)
        lg = out.logits[0, -1].float()
        a, b = self.opt_ids(row)
        p = torch.softmax(lg[[a, b]], 0)[0].item()  # P(first option): act / approve
        top = self.tok.decode([int(lg.argmax())])
        hs = None
        if want_hidden:
            hs = torch.stack([h[0, -1] for h in out.hidden_states]).half().cpu().numpy()
        return p, top, hs

    @modal.method()
    def smoke(self, rows):
        res = []
        for r in rows:
            p, top, _ = self.forward(r, False)
            res.append(dict(role=r["role"], world=r["world"], scen=r["scen"], p_first=p, top=top))
        return res

    @modal.method()
    def extract(self, rows):
        import numpy as np
        P, H, T = [], [], []
        for i, r in enumerate(rows):
            p, top, hs = self.forward(r, True)
            P.append(p); H.append(hs); T.append(top)
            if i % 50 == 0:
                print(i, r["role"], r["world"], r["scen"], round(p, 3), repr(top))
        buf = io.BytesIO()
        np.savez_compressed(buf, p=np.array(P), h=np.stack(H), top=np.array(T))
        with open("/vol/out_acts.npz", "wb") as f:
            f.write(buf.getvalue())
        vol.commit()
        return dict(n=len(P), shape=list(np.stack(H).shape))

    @modal.method()
    def steer(self, rows, vecs, layer, alphas):
        """Add alpha * unit vector to the residual output of decoder layer `layer` at every position."""
        torch = self.torch
        v = torch.tensor(vecs, dtype=torch.bfloat16, device="cuda")
        state = {"a": 0.0}

        def hook(mod, inp, out):
            if state["a"] == 0.0:
                return out
            if isinstance(out, tuple):
                return (out[0] + state["a"] * v,) + tuple(out[1:])
            return out + state["a"] * v

        h = self.layers[layer - 1].register_forward_hook(hook)  # hidden_states[k] is the output of layer k-1
        res = []
        try:
            for a in alphas:
                state["a"] = float(a)
                for i, r in enumerate(rows):
                    p, top, _ = self.forward(r, False)
                    res.append(dict(i=i, alpha=a, p_first=p, top=top))
        finally:
            h.remove()
        return res


@app.local_entrypoint()
def smoke():
    from scenarios import build
    rows = build()
    pick = [r for r in rows if r["me"] == "Dee" and r["prop"] == "Rex"]
    res = G().smoke.remote(pick)
    for role in ("actor", "judge"):
        print(role, "P(act/approve) by scenario x world")
        for sc in sorted({x["scen"] for x in res}):
            print(f"  {sc:8s}", "  ".join(f"{w}={x['p_first']:.3f}" for w in ("none", "passed", "hearsay", "signed")
                  for x in res if x["role"] == role and x["scen"] == sc and x["world"] == w))


@app.local_entrypoint()
def extract():
    from scenarios import build
    rows = build()
    print(G().extract.remote(rows))


@app.local_entrypoint()
def steer(spec: str = "steer_spec.json"):
    from scenarios import build
    sp = json.load(open(spec))
    rows = [r for r in build() if r["role"] == sp["role"] and r["world"] in sp["worlds"]]
    res = G().steer.remote(rows, sp["vec"], sp["layer"], sp["alphas"])
    meta = [dict(scen=r["scen"], world=r["world"], me=r["me"], prop=r["prop"]) for r in rows]
    for x in res:
        x.update(meta[x["i"]])
    json.dump(res, open(sp["out"], "w"))
    print("saved", sp["out"], len(res))
