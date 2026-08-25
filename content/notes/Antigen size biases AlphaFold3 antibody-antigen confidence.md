---
tags:
  - alphafold3
  - structure-prediction/complex-prediction
  - antibody-antigen-interactions/complex-prediction
  - pae
  - tm-score
created: "2026-08-25"
modified: "2026-08-25T10:16:02"
---
#### Summary
**[[alphafold3|AlphaFold3]] antibody-antigen confidence is biased by antigen size and experimental structure source, but showed no detectable preference for antibody CDR composition or length** [@solanki2026]. Across 3,401 experimental complexes and 23,798 negative controls, the positive prediction rate decreased with target size and surface area, and nonbinders against larger targets had worse mean [[pae|PAE]]. Predictions from X-ray structures were favored over electron-microscopy structures, whereas CDR amino-acid composition, CDR length, training-data leakage, and antibody framework or scaffold identity were not significant biases.

The maximum recall was 53% at 100 inference seeds, with an innate false-positive rate of about 3%. Approximately 34% of false negatives retained the correct epitope location despite poor structural alignment.

#### See also
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[ipTM is sensitive to construct length even when predicted interfaces are unchanged]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
