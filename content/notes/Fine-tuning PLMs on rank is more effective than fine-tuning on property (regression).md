#### Summary

**Fine-tuning [[Protein language models]] using rank information is more effective than fine-tuning using absolute property measurements (regression;** [@hawkinshooker2024]). It also converts a dataset of $N$ sequences to $N^{2}$ pairwise comparisons, while generalizing better to unseen positions.

#### Figures
| Model Name | Scoring Function | Loss | single n=32 | single n=128 | single n=512 | multi n=32 | multi n=128 | multi n=512 |
|---|---|---|---|---|---|---|---|---|
| ESM-1v (650M) | linear head | mse | 0.263 | 0.415 | 0.535 | 0.494 | 0.637 | **0.771** |
| | wt-marginals | **ranking** | **0.479** | **0.552** | **0.641** | **0.577** | **0.642** | 0.753 |
| ESM-2 (650M) | linear head | mse | 0.280 | 0.398 | 0.535 | 0.427 | 0.596 | 0.743 |
| | wt-marginals | **ranking** | **0.455** | **0.530** | **0.627** | **0.593** | **0.651** | **0.758** |
| PoET | linear head | mse | 0.443 | 0.553 | 0.646 | 0.571 | 0.714 | 0.793 |
| | likelihood | **ranking** | **0.513** | **0.591** | **0.672** | **0.667** | **0.737** | **0.806** |
| ProteinNPT (MSAT) | | mse | 0.415 | 0.533 | 0.637 | 0.517 | 0.692 | 0.791 |
| ProteinNPT (ESM-1v) | | mse | 0.410 | 0.497 | 0.607 | 0.438 | 0.645 | 0.769 |
| Emb. aug. (MSAT) | | mse | 0.424 | 0.507 | 0.553 | 0.581 | 0.696 | 0.764 |
| Emb. aug. (ESM-1v) | | mse | 0.451 | 0.505 | 0.550 | 0.440 | 0.624 | 0.702 |
| OHE aug. (MSAT) | | mse | 0.429 | 0.467 | 0.496 | 0.616 | 0.684 | 0.763 |
| OHE aug. (ESM-1v) | | mse | 0.466 | 0.502 | 0.526 | 0.460 | 0.566 | 0.711 |
| OHE | | mse | 0.144 | 0.314 | 0.488 | 0.268 | 0.473 | 0.664 |

| Model | Scoring fn. | Loss | Seen | Unseen |
|---|---|---|---|---|
| ESM-1v (650M) | linear head | mse | 0.460 | 0.331 |
| | wt-marginals | rank | **0.592** | **0.509** |
| ESM-2 (650M) | linear head | mse | 0.453 | 0.297 |
| | wt-marginals | rank | **0.568** | **0.455** |
| PoET | linear head | mse | 0.571 | 0.517 |
| | likelihood | rank | **0.612** | **0.549** |
| PNPT (MSAT) | - | mse | 0.563 | 0.462 |
| PNPT (ESM-1v) | - | mse | 0.529 | 0.420 |

*Tables from [@hawkinshooker2024]*

#### See also
* [[Fine-tuning almost always improves property prediction]]
