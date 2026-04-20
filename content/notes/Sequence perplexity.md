---
tags:
created: 2026-04-05T17:41:51
modified: "2026-04-20T07:46:00"
---
#### Summary
Sequence perplexity is a metric used by [[Protein language models|protein language models]] and [[Inverse folding|inverse folding]] to quantify sequence recovery. Self-consistency perplexity is a derived metric where the perplexity is calculated using a [[Structure prediction|forward-folded model]] rather than the original model/structure.

#### Details
The perplexity values of null models was calculated below by [@ingraham2019]:

![[Table-1-Null-perplexities-for-common-statistical-models-of-proteins.png]]
*Table from [@ingraham2019]*

Hie et al. found that sequence length does not consistently correlate with perplexity values within protein families.[@hie2022]

Meier et al. introduced ways of calculating probabilities or "energies" of sequences using masked [[Protein language models|LMs]] (e.g., how favored or disfavored they are given evolution). The authors of [[ESM]]-1v propose four approaches for this:[@meier2022]

- **Masked marginal probability:** Masks are introduced at all mutation residues and probabilities relative to the wildtype residue are calculated: $\sum{\log{p(x_{i}=x_{i}^{mnt}|x_{-M}) - \log{p(x_{i}=x_{i}^{wt}|x_{-M})}}}$
- **Mutant marginal probability:** Requires a single forward pass for each mutation: $\sum{\log{p(x_{i}=x_{i}^{mnt}|x^{mnt}) - \log{p(x_{i}=x_{i}^{wt}|x^{mnt})}}}$. The entire sequence is kept fixed except for one mutation and the preference for the mutation of interest, normalized to the WT residue, is calculated. This was used for structure-based [[Fitness prediction|fitness prediction]] in [@ding2024] with Spearman $R$ values ranging from 0.39–0.71.
- **Wildtype marginal probability:** The same as mutant marginal probability, except the background is the wildtype sequence: $\sum{\log{p(x_{i}=x_{i}^{mnt}|x^{wt}) - \log{p(x_{i}=x_{i}^{wt}|x^{wt})}}}$
- **Pseudo-likelihood:** [@devkota2024] found that [[ESM]]2 pseudo-log likelihood values scaled linearly with the length of the sequence. They introduced a length-invariant correction ($pLL_{invar}$): $pLL(S)=\sum{\log{p(x_{i}=x_{i}^{mnt}|x_{i-1}^{mnt}) - \log{p(x_{i}=x_{i}^{wt}|x_{i-1}^{wt})}}}$, $pLL_{invar}(S)=\frac{pLL(S)}{|-0.406*len(S)+1.363|}$

![[Pasted-image-20240820153913.png]]
*Figure from [@devkota2024]*

The Spearman correlations against [[ProteinGym]] were: masked marginal 0.582, mutant marginal 0.578, wildtype marginal 0.572, pseudolikelihood 0.552.

Gordon et al. propose a way to approximate sequence log-likelihood in a single pass using masked LMs:[@gordon2024]

![[Pasted-image-20241004100612.png]]
![[Pseudo-Likelihoods.png]]
*Figures from [@gordon2024]*

#### See also
- [[Self-consistency perplexity is correlated with pLDDT]]
- [[Sequence perplexity and TM-score are negatively correlated when predicting structure using protein language models]]
- [[Spearman correlations of protein property prediction methods do not correlate perfectly with absolute error]]
- [[Fréchet distance]]
