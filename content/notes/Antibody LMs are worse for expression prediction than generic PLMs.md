---
tags:
  - protein-language-models/antibodies
  - antibody-developability/expression
created: "2026-04-05T17:07:03"
modified: "2026-04-20T08:16:13"
---
#### Summary
**[[Antibodies|Antibody]]-specific [[Protein language models|protein language models]] are worse for antibody [[Developability|expression prediction]] than generic [[Protein language models|PLMs]]** [^kenlay2024].

#### Figures
| Model | Binding *N* = 422 (Shanehsazzadeh et al., 2023) | Binding *N* = 2048 (Warszawski et al., 2019) | Binding *N* = 4275 (Koenig et al., 2017) | Expression *N* = 4275 (Koenig et al., 2017) |
| -------------------------------- | ----------------------------------------------- | -------------------------------------------- | ---------------------------------------- | ------------------------------------------- |
| AbLang (Olsen et al., 2022b) | *0.293* ± 0.117 | *0.246* ± 0.038 | *0.244* ± 0.034 | 0.439 ± 0.027 |
| AntiBERTy (Ruffolo et al., 2021) | 0.239 ± 0.102 | 0.217 ± 0.056 | 0.199 ± 0.025 | 0.401 ± 0.032 |
| ProtBert (Elnaggar et al., 2022) | 0.200 ± 0.106 | 0.149 ± 0.024 | 0.101 ± 0.017 | 0.491 ± 0.029 |
| IgBert-unpaired | 0.278 ± 0.094 | 0.181 ± 0.040 | 0.177 ± 0.018 | 0.347 ± 0.023 |
| IgBert | **0.306** ± 0.114 | 0.131 ± 0.047 | 0.174 ± 0.032 | 0.400 ± 0.023 |
| ProtT5 (Elnaggar et al., 2022) | 0.290 ± 0.105 | 0.186 ± 0.037 | *0.206* ± 0.029 | **0.697** ± 0.02 |
| IgT5-unpaired | 0.299 ± 0.119 | *0.245* ± 0.049 | 0.179 ± 0.014 | 0.567 ± 0.025 |
| IgT5 | 0.274 ± 0.070 | **0.297** ± 0.057 | **0.25** ± 0.019 | *0.548* ± 0.067 |

*Ref [^kenlay2024]*

#### See also
- [[Antibody LMs outperform generic PLMs on intrafamily thermostability prediction]]

[^kenlay2024]: Kenlay et al. (2024) "Large scale paired antibody language models." PLoS Comput. Biol.. https://doi.org/10.1371/JOURNAL.PCBI.1012646
