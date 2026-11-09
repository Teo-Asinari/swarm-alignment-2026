# What the Log Says Three Times

Code, data and report for an Apart Research Swarm Alignment Sprint project (November 6–8, 2026).

**Question.** Why does an LLM agent that normally follows a rule break it after its team "approves" breaking it, and does it still know the action is unauthorized?

**Report:** [`paper/report.pdf`](paper/report.pdf). Running log of every experiment, including the ones that did not replicate: [`FINDINGS.md`](FINDINGS.md).

## Layout

| Path | What it is |
|---|---|
| `interp/big.py` | Stimuli: 45 scenarios × 6 team-log worlds × name variants × 3 roles (actor, approver, classifier), plus prompt interventions |
| `interp/scale_app.py` | Modal job: runs 4 open models, reads decisions from next-token probabilities, cross-fitted steering with norm-matched random controls |
| `interp/analyze_scale.py` | Scenario-level bootstrap summaries → `interp/results/summary.md` |
| `interp/results/` | Per-prompt results for each model |
| `interp/scenarios.py`, `modal_app.py`, `analyze.py` | The earlier 12-scenario Gemma 4 31B study (superseded at scale) |
| `evolve/` | Hypothesis evolver (LLM generators + adversarial review panel), pilots, architecture and judge-first tests |
| `paper/` | LaTeX source, figures (`make_figures.py`), watermarks |

## Reproducing

```bash
pip install modal && modal setup
cd interp && modal run scale_app.py::main          # ~1 h on 4×H100
python3 analyze_scale.py results/*.json > results/summary.md
cd ../paper && python3 make_figures.py && pdflatex report.tex
```

The `evolve/` scripts call the Adaption API; set `ADAPTION_KEY_FILE` to a file containing your key.

## Provenance

All code and results in this repository were produced during the sprint weekend; nothing is pre-existing. The work was heavily AI-assisted: Claude (Anthropic) wrote most of the code and drafted the report under the author's direction.
