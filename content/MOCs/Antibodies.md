---
title: Antibodies
tags:
  - antibodies
created: "2026-04-10T14:30:55"
modified: "2026-04-11T06:15:31"
---

**Antibodies** are proteins with two [[Heavy chains|heavy chains]] and two [[Light chains|light chains]] produced by [[B cells]], central to the adaptive immune system. Their structure consists of a variable region (containing [[Complementarity-determining regions|CDRs]] and a framework region) and three constant regions (CH1, CH2, CH3). The variable region and CH1 form the [[Fab]], while the remainder forms the Fc region. [[B-cell receptors|B cell receptors]] are antibodies with an additional CH4 domain.

## Types of antibodies

**IgA** is found in mucous membranes, cannot activate the complement system, and makes up roughly two-thirds of antibodies in healthy adults. It is notable for being double-sided.

**IgE** has only one binding site, mainly protects against large organisms like parasites, and is responsible for allergic reactions.

**IgG** is the standard antibody class used in therapeutic design. Cannot activate the complement system and can pass through the placenta.
- *IgG1* makes up 67% of all antibodies in the human body, is capable of antibody-dependent cellular phagocytosis, and has the longest hinge region. IgG1 immune repertoires consist mostly of just a few dozen dominant clones and are unique to each individual, remaining largely stable over time.
- *IgG2* — mice have IgG2a and IgG2b instead; some strains have IgG2c instead of IgG2a.
- *IgG3* makes up ~7% of IgGs and has a notably shorter half-life due to poor binding to [[FcRn]], attributed to an H435R mutation.
- *IgG4* is the rarest IgG and undergoes Fab-arm exchange, dissociating into half-bodies and forming novel combinations via R409 in the hinge. Therapeutic IgG4 antibodies use the S228P substitution to stabilize the hinge and prevent this.

**IgM** is far less subject to [[Affinity maturation|affinity maturation]] than IgG, responds to lipids and polysaccharides, and activates the complement system.

## Datasets

SAbDab is a database of all antibody and [[Nanobodies|nanobody]] structures in the PDB. The full list can be downloaded with:

```bash
curl -s https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab/summary/all/
```

<!-- generated -->

## Structure Prediction

- [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]

## Miscellaneous

- [[Abs modeled using MD are better for featurization than those modeled using homology modeling]]
- [[Agonist antibodies benefit from low affinity due to antigen clustering]]
- [[Antibodies and BCRs have different binding kinetics]]
- [[Antibodies and nanobodies can desymmetrize proteins for cryoEM]]
- [[Antibodies from different repertoires within a given species targeting the same epitope often have the same light chain isotype and share critical residues]]
- [[Antibodies with distinct V genes and CDRH3 loops can convergently evolve to bind the same epitope]]
- [[Antibody affinity can be improved by stabilization]]
- [[Autoimmune diseases involve the constant activation and reactivation of new B cells]]
- [[B-cell proliferation is driven by both antigen binding and surface expression]]
- [[Biparatopic antibodies can induce clustering beyond what is observed in monoparatopic antibodies]]
- [[Broadly neutralizing antibodies against HIV evolve in a subset of patients]]
- [[CDR3 far more likely to be part of paratope of nanobodies compared to antibodies]]
- [[CDR3 loops encode specificity while CDR1 and CDR2 encode cross-reactivity]]
- [[CDR3 mediates heavy-light chain pairing preferences by making contacts to framework residues]]
- [[CDRH3 conformational rigidity reduces cross reactivity]]
- [[CDRH3 has most contacts with antigen]]
- [[CDRH3 is necessary but insufficient to guarantee binding to a particular epitope]]
- [[CDRH3 is shorter in mice and therapeutic Abs]]
- [[Classifiers can be used as predictors of continuous properties]]
- [[Composition of negative data affects rule discovery in binary classification tasks]]
- [[Conformational entropy in antibodies is inversely proportional to antigen affinity]]
- [[Contrastive learning on whole structures leads to learning of substructures]]
- [[Cytokines can be added to antibody CDRs]]
- [[DL antibody prediction tools introduce D-amino acids and cis-amide bonds]]
- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
- [[Different antibody lineages can undergo convergent evolution during affinity maturation]]
- [[Dynamic time warping]]
- [[ESM-IF outperforms ProteinMPNN on Ab inverse folding and affinity prediction]]
- [[Ensemble samplers and Gaussian process equally useful for automated antibody design]]
- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[Hallucination of CDRs]]
- [[Heavy and light chains of de novo designed antibodies with the same framework and binding mode can be exchanged]]
- [[Heavy chain scFvs are stronger binders than light chain scFv]]
- [[Individual D genes are evolutionarily selected for well-defined antigen-binding capabilities]]
- [[Individual V, D, and J gene usage is highly uneven]]
- [[Insufficient ddG data on Abs for training]]
- [[Inverse folding of CDRs benefits from span masking during training]]
- [[Kappa light chains are far more common in antibody therapeutics]]
- [[Lambda light chains are less thermostable]]
- [[Light chain CDR charges can shorten half-life by slowing release from FcRn]]
- [[Light chain coherence]]
- [[Light chain determines autospecificity]]
- [[ML optimized Ab libraries have more mutations than PSSM libraries]]
- [[Membrane proteins can be bulked up for cryo-EM by inserting designed domains, including those with predefined epitopes for antibodies]]
- [[Most nanobodies do not bind using all three CDRs]]
- [[Multiple nanobodies can bind simultaneously]]
- [[NGS sequence abundance does not correlate with binding affinity]]
- [[Nanobodies and Abs target different epitopes but with similar accessibility and number of contacts]]
- [[Nanobodies designed de novo from sequence are more flexible than either those designed from structure or those occurring in nature]]
- [[Nanobodies designed de novo from sequence are more flexible than those designed from structure or occurring in nature]]
- [[No one-size-fits-all approach to scoring antibody structures]]
- [[PSSMs for Ab engineering outperforms random]]
- [[Paratope losses are required to enforce CDR-mediated antigen binding during de novo antibody design by hallucination]]
- [[Protein-protein interaction interfaces are highly degenerate]]
- [[PyRosetta convert mAb structure numbering]]
- [[Secondary structure losses are required to enforce CDR loopiness during de novo antibody design by hallucination]]
- [[Simultaneous design of scFv loops predicted to lead to more fit sequences]]
- [[Some light chain V-genes are more likely to be found in dysfunctional antibodies]]
- [[Source of immunogenicity in VHH nanobodies]]
- [[Subset of mutations obtained during affinity maturation contribute disproportionately to affinity]]
- [[There are 4.6 million possible combinations of human antibodies given VDJ and VJ scrambling alone]]
- [[Transgenic mice with only a single VH gene are nonetheless able to make effective antibodies against many targets]]
- [[Up to 22 percent of antigen binding residues are outside CDRs]]
- [[Variable regions can adopt multiple interchain arrangements, and these are difficult to predict]]
- [[Wildtype antibody frameworks can accommodate CDRs that bind to virtually any target]]
- [[Zero-shot protein stability prediction using inverse folding models can be improved by subtracting predictions from residue in isolation]]

## Nanobodies

- [[Anti-nanobody immunogenic reactions disproportionately target their C-termini]]
- [[CabBCII-10 is a universal nanobody framework capable of accepting diverse CDRs]]
- [[Germline usage determines whether nanobody CDR3 is kinked or extended]]
- [[Kinked nanobody CDR3s are longer than extended CDR3s]]
- [[Kinks in nanobody CDR3 loops are correctly predicted by structure prediction methods]]
- [[Most camelid-derived nanobodies have high sequence identity with human IGHV3]]
- [[Nanobody CDR1 and CDR2 do not conform to the canonical clustering patterns found in traditional antibodies]]
- [[Nanobody CDRH3 loops are longer but more compact]]
- [[Nanobody FR2 is more hydrophilic than that of antibodies]]
- [[Nanobody framework residues more likely to be part of paratope than those of antibodies]]
- [[Partial diffusion of de novo designed binders and VHHs improves refoldability and designability scores]]
- [[Source of immunogenicity in VHH nanobodies]]
- [[The solubilization tetrad allows camelid nanobodies to remain soluble in the absence of a light chain]]
