---
tags:
  - prediction/confidence
  - prediction/complexes
created: "2026-08-25"
modified: "2026-08-25T10:16:02"
---
#### Summary
**[[notes/TM-score|ipTM]] can change when irrelevant domains or [[Intrinsically disordered regions|disordered residues]] are trimmed even if the predicted binding interface is unchanged** [@dunbrack2025]. The direction depends on construct composition: extra residues can increase ipTM when one partner is a compact domain, but can substantially decrease it when both chains contain disorder or accessory domains. This follows from scoring whole chains and using a length-dependent $d_0$, rather than from a change in the interface itself. ipSAE mitigates the dependence by restricting the score to residue pairs with good interchain [[notes/Predicted aligned error|PAE]].

#### See also
- [[Antigen size biases AlphaFold3 antibody-antigen confidence]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
