---
tags:
  - alphafold3
  - structure-prediction/complex-prediction
  - antibody-antigen-interactions/complex-prediction
  - pae
  - tm-score
created: "2026-08-25"
modified: "2026-08-25T10:55:31"
---
#### Summary
**[[alphafold3|AlphaFold3]] antibody-antigen confidence is biased by antigen size** [@solanki2026]. Larger antigens lead to broader [[pae|PAE]] distributions, presumably because there are more ways to be very wrong in larger antigens than smaller antigens.

#### Figures
![[af3-antibody-antigen-pae-by-target-size.png]]
*Ref [@solanki2026]*

#### See also
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[ipTM is sensitive to construct length even when predicted interfaces are unchanged]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
