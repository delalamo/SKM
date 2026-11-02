# Decision-model comparison (tranche of 29 October 2026)

Do open-source "System One" decision models pick the same papers as the
current SPECTER2 workflow? All runs used a 4-vCPU, 15 GB RAM, CPU-only
container, which is comparable to a default `ubuntu-latest` GitHub runner.

## Setup

- **Tranche:** paperbot's own fetchers over 2026-10-29 00:00 to 2026-10-30
  00:00 UTC. That gave 5,788 papers: PubMed 4,935, arXiv 420, bioRxiv 223,
  ChemRxiv 121, medRxiv 94. Every paper had an abstract.
- **Baseline:** the trained SPECTER2 classifier on `main` scored all 5,788
  papers in 28 minutes (about 0.29 s per paper). With the strict cutoff of
  `score > 0.80` it opens **10 issues**. 78 more papers score 0.5 to 0.8,
  459 score 0.2 to 0.5, and 5,241 score below 0.2.
- **Sample:** a stratified sample of 60 papers. It has all 10 accepts, plus 20,
  15 and 15 random papers from the lower bands. Each paper carries a weight
  (stratum size divided by sample size), so per-day estimates extrapolate to
  the whole tranche.
- **Models:** each model got the same yes/no `noul` question and the same
  bibliography context built by `scripts/paperbot/jev.py`. Each ran alone with
  all four CPUs.
  - The "prefix" layout (about 5k tokens) puts a fixed block of recent
    bibliography titles first, then 4 similar papers with abstracts, then the
    candidate.
  - The "short" layout (about 1.5k tokens, candidate near the top) was used for
    the small encoders. They truncate long input, and with the prefix layout
    they never saw the candidate. Laya's prefix run returned a constant 0.7267
    for every paper.
- **Not tested:** hosted Jev, because no `TYPESAFE_API_KEY` was available.
  Kev 4B, 9B and 27B were not tested, because the reference implementation is
  bf16/fp32 PyTorch and the 0.8B model already needs 33 s per paper on this
  CPU.

## Results

The `rho` column is the Spearman rank correlation with SPECTER2. `Top-10`
is the overlap of each model's 10 highest-scoring papers with SPECTER2's 10
accepts. `Est. issues/day` is the weighted estimate at a 0.5 cutoff.

| Model (licence) | s/paper (CPU) | Full day | rho | Top-10 | Est. issues/day |
|---|---:|---:|---:|---:|---:|
| **SPECTER2 + LR (current)** | **0.29** | **28 min** | 1 | 10/10 | **10** |
| Kev 0.8B (Apache-2.0), prefix | 33 | ~53 h | 0.70 | 5/10 | 51 |
| Rizzo Flow 1.7B Q4 (Apache-2.0), prefix | 35 | ~56 h | 0.62 | 5/10 | ~1,700 (83 at a 0.9 cutoff) |
| Rizzo Flow 4B Q4 (Apache-2.0), prefix* | 84 | ~135 h | – | – | – |
| Von 1.3 (Apache-2.0, archived), prefix | 43 | ~69 h | 0.02 | 2/10 | every paper |
| Von 1.3, short | 8 | ~13 h | −0.07 | 0/10 | every paper |
| Laya 421M (Apache-2.0), short | 1.5 | ~2.4 h | 0.30 | 2/10 | every paper |
| LiquidAI d1-omni-600M (LFM 1.0), prefix | 15 | ~23 h | −0.02 | 1/10 | 65 |
| d1-omni-600M, short | 4.2 | ~6.8 h | −0.18 | 0/10 | 825 |

\* Rizzo Flow 4B was run only on the 30 papers that SPECTER2 scored 0.5 or
higher (see below).

No open-source model can replace SPECTER2 as the filter for a whole day on a
default runner. The models that track SPECTER2 (Kev, Rizzo Flow) need 33 to
84 s per paper, so a full day would take 53 to 135 hours, against a 6-hour
job limit. The models fast enough to fit (Laya, Von, d1) have little or no
agreement with SPECTER2, and their probabilities cluster around 0.5 to 0.7.

A dependency-free BM25 match against the bibliography is not a usable cheap
pre-filter either. Its top 1,000 papers contained only 4 of SPECTER2's 10
accepts.

### As a second stage on SPECTER2's shortlist

A realistic open-source design keeps SPECTER2 and adds a second stage. SPECTER2
uses a looser cutoff (`> 0.5`, about 88 papers a day), and a decision model
then re-judges that shortlist with the bibliography as context. The table
covers the 30 sampled shortlist papers, each borderline paper weighted 3.9.
AUC is the chance that a SPECTER2 accept ranks above a borderline paper
(0.5 is chance).

| Model | AUC | At 0.9 cutoff: accepts kept | Borderline promoted/day | Runner time for 88 papers |
|---|---:|---:|---:|---:|
| Rizzo Flow 4B Q4 | **0.79** | 9/10 | ~35 | ~2.1 h |
| Rizzo Flow 1.7B Q4 | 0.74 | 6/10 | ~16 | ~50 min |
| Kev 0.8B | 0.69 | 0/10 (outputs stay within 0.38–0.60) | 0 | ~50 min |
| Laya, short | 0.66 | – | – | ~2 min |
| Von, short | 0.58 | – | – | ~12 min |
| d1-omni, short | 0.56 | – | – | ~6 min |

The disagreements are only partly errors. Rizzo Flow 4B gave low scores to
generic machine-learning papers that SPECTER2 placed in the 0.5 to 0.65 band.
Examples include an RLVR paper (0.13), a synthetic-data statistics paper
(0.12), and an LLM-distillation paper (0.33). It also gave high scores to
borderline antibody papers that SPECTER2 placed just under its cutoff, such
as an aggregation study of glycoengineered monoclonal antibodies (0.98) and a
pipeline for modification-specific intracellular antibodies (0.96). On the other
hand, it accepts almost any structural-biology paper (CAR-T, curli proteins,
docking) at 0.95 or above. That is broader than the bibliography's
protein-ML and antibody focus. Per-paper scores are in
`2026-10-29-decision-models.csv`.

## Reproducing

Kev, Rizzo Flow, Von and Laya serve TypeSafe's `/v1/systemone` API, so the
paperbot Jev client talks to them unchanged. Set `[jev] endpoint` (or
`PAPERBOT_JEV_ENDPOINT`) to `http://127.0.0.1:<port>/v1/systemone`; loopback
endpoints need no key. d1-omni has no server, so
`scripts/paperbot_eval/d1_shim.py` wraps it in that API.

- `scripts/paperbot_eval/decide.py SAMPLE OUT ENDPOINT MODEL BUDGET [SIMILAR] [REJECTED]`
  runs one server over a sample. Set `LAYOUT=prefix` or `LAYOUT=ranked`.
- `compare.py SAMPLE name=OUT[@threshold] ...` reports agreement with SPECTER2.
- `stage2.py name=OUT ...` reports the shortlist (second-stage) view.

Model servers used:
- `python -m kev.serve --run jaredpalmer/kev-0.8b --device cpu` (model name `kev-latest`)
- `rizzo serve --size 1.7b|4b --quant q4_k_m --device cpu` (model name `rizzo-latest`)
- `von serve --device cpu --noul-decision raw`
- `laya-serve`, with `LAYA_PORT`
