---
tags:
  - conformational-dynamics
  - protein-language-models/training
created: "2025-04-24T03:21:39"
modified: "2026-04-11T06:06:39"
---
#### Summary
**Alternate sequence [[Clustering|clustering]] schemes outperform uniform sampling when training [[Protein language models|protein language models]]** [^bhatnagar2025]. Uniform sampling, which is standard in the field, performed worse than sampling strategies that account for the increased presence of some protein families, and even worse than simply sampling all sequences (after 90% clustering). This suggests that sequence propensity may encode some useful information.

#### Figures
\![[LANE-ROSE-HAS.png]]
*Figure from [^bhatnagar2025]*

#### See also
- [[Sequence clustering of training data affects variant effect prediction performance by PLMs]]

[^bhatnagar2025]: Bhatnagar et al. (2025) "Scaling Unlocks Broader Generation and Deeper Functional Understanding of Proteins." https://doi.org/10.1101/2025.04.15.649055
