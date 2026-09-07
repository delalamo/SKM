---
tags:
  - prediction/structure
  - prediction/complexes
created: "2026-07-28"
modified: "2026-07-28T14:12:17"
---

#### Summary

**[[Multi-sequence protein language models|MSA protein language models]] can identify intermolecular contacts and generalize from single-chain training to heterooligomeric [[notes/Protein-protein interactions|protein-protein interactions]].** [[MSA Transformer]] extracts intermolecular contacts from correctly paired, but not incorrectly paired, MSAs [@lupo2024]. MSA Pairformer predicts protein-protein interface contacts and distinguishes binding from non-binding sequences despite being trained exclusively on individual chains [@akiyama2026]. This extends the observation that [[Structure prediction and design tools trained on monomers generalize to oligomers|structure prediction and design models trained on monomers can generalize to oligomers]] to MSA-based language models.

#### Details
The findings in MSA Pairformer were obtained by using a specific pairing strategy[@akiyama2026]:
> We integrated a proximity-based pairing scheme that infers genomic proximity directly from protein accessions. First, we translate UniProt and UniParc accessions into structured integers, based on the convention that sequentially numbered accessions reflect neighboring genes. Beginning from the highest scoring protein identified through an MMseqs2 search against the UniRef100, we iteratively select the closest unmatched protein within a predefined numerical threshold (default distance ≤ 20). This process is repeated until all suitable protein pairs have been identified. We allow either greedily pairing all possible matches or enforcing that all protein chains must be covered by paired database proteins.

#### Figures

![[akiyama2026-msa-pairformer-interface-scoring.png]]
*MSA Pairformer scores distinguish high-fitness from low-fitness toxin-antitoxin interface sequences. Ref [@akiyama2026]*

#### See also

- [[Query-conditioned outer product]]
- [[Coevolutionary patterns in multiple sequence alignments do not contribute to protein-protein complex prediction]]
- [[Training protein structure prediction neural networks on both positive and negative protein-protein interactions improves PPI discrimination]]
- [[Correct protomer structure prediction is necessary but insufficient for accurate protein-protein docking]]
