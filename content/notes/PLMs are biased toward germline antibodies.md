---
tags:
  - protein-language-models/antibodies
  - affinity-maturation
created: "2026-04-05T17:12:20"
modified: "2026-04-21T07:03:26"
---
#### Summary
**[[tags/protein-language-models|Protein language models]] are biased toward residues found in [[Germline|germline]] sequences** [@olsen2022; @nijkamp2023; @olsen2024]. Reasons include the fact that blood samples that are sequenced contain mostly naive [[tags/b-cells|B cells]], and fewer memory B cells and plasma cells. [@olsen2024] found that [[Focal loss]] improves prediction of non-germline. Paired antibody language models are less sensitive to this bias (Burbach and [@burbach2024]).

#### Details
Relatedly, non-antibody [[tags/protein-language-models|PLMs]] are also biased towards [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt|sequences from model organisms]], which arises from the same sensitivity to training data.

#### Figures
| | Germline residues | | | | Non-germline residues | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|
| | **Heavy** | | **Light** | | **Heavy** | | | **Light** | | |
| | FRW | CDR1/2 | FRW | CDR1/2 | FRW | CDR1/2 | CDR3 | FRW | CDR1/2 | CDR3 |
|---|---|---|---|---|---|---|---|---|---|---|
| ESM-2 | 1.91 | 4.12 | 2.54 | 6.11 | 32.03 | 24.36 | 20.85 | 23.20 | 19.37 | 24.29 |
| AntiBERTy | 1.05 | 1.10 | 1.17 | 1.28 | 29.64 | 21.51 | 18.44 | 40.14 | 21.75 | 16.95 |
| AbLang-1 | **1.03** | 1.08 | 1.07 | 1.16 | 25.80 | 17.73 | 14.47 | 52.14 | 25.72 | 16.75 |
| Ab-Unpaired | **1.02** | 1.07 | **1.01** | 1.05 | 26.81 | 18.95 | 14.42 | 37.60 | 19.37 | 17.25 |
| Ab-Paired | **1.02** | 1.06 | **1.02** | 1.05 | 27.24 | 18.70 | 14.23 | 38.95 | 19.25 | 16.98 |
| Ab-FL | 1.10 | 1.17 | 1.09 | 1.16 | 10.33 | 11.18 | 12.69 | 10.82 | 10.24 | 11.04 |
| Ab-ModMask | 1.11 | 1.18 | 1.09 | 1.17 | 10.26 | **11.13** | 13.18 | 10.78 | 10.19 | 11.42 |
| Ab-FT | 1.11 | 1.18 | 1.10 | 1.18 | 10.88 | 11.91 | 13.67 | 11.25 | 10.63 | 12.29 |
| AbLang-2 | 1.10 | 1.17 | 1.09 | 1.16 | **9.92** | **11.13** | **12.47** | **10.09** | **9.54** | **10.77** |
*Table 3 from [@olsen2024]*

![[Pasted-image-20240516151725.png]]
*Figure 3 from Burbach and [@burbach2024]*

#### See also
- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[ML models must trade off bias and variance]]
