---
tags:
  - inverse-folding/evaluation
  - protein-backbone-design/designability
created: "2026-04-05T17:57:34"
modified: "2026-04-21T07:28:09"
summary: Sheets are less designable than helices
---
#### Summary
Beta-sheets are less designable than alpha helices using [[inverse-folding|Inverse folding]] models [@wang2023]. This was true for a range of models.

#### Figures
| Design method | EHEE_3 | EHEE_4 | EHEE_5 | EHEE_6 | HHH_54 | HHH_82 | HHH_84 | HHH_86 | mean |
|---|---|---|---|---|---|---|---|---|---|
| **GVP** | 0.158 | 0.285 | 0.299 | 0.271 | 0.682 | 0.593 | 0.588 | 0.658 | 0.442 |
| **PiFold** | 0.158 | 0.287 | 0.269 | 0.267 | 0.688 | 0.607 | 0.556 | 0.641 | 0.434 |
| **ProteinMPNN** | 0.176 | 0.282 | 0.314 | 0.274 | 0.688 | 0.584 | 0.570 | 0.626 | 0.439 |
| **ESMIF** | 0.171 | 0.335 | 0.331 | 0.282 | 0.678 | 0.660 | 0.625 | 0.691 | 0.472 |
| **ByProt** | 0.191 | 0.297 | 0.296 | 0.270 | 0.688 | 0.631 | 0.571 | 0.626 | 0.446 |
| **AF-Design** | **0.252** | **0.366** | **0.402** | **0.353** | **0.699** | **0.672** | **0.661** | **0.723** | **0.516** |
| **ESM-Design** | 0.153 | 0.259 | 0.291 | 0.189 | 0.622 | 0.369 | 0.303 | 0.362 | 0.319 |
*Figure by [@wang2023]*
