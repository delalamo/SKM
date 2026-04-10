---
title: Antibodies
tags:
  - antibodies
created: "2026-04-10T14:30:55"
modified: "2026-04-10T15:51:38"
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

- [[Ab embeddings can distinguish engineered from human-derived Abs]]
- [[Ab-Ag inverse folding methods benefit from pretraining]]
- [[Abs modeled using MD are better for featurization than those modeled using homology modeling]]
- [[Affinity maturation also selects for lower self-association]]
- [[Affinity matured antibodies can adopt distinct binding poses from germline precursors]]
- [[Affinity matured antibodies have lower thermostability than germline antibodies, up to a threshold]]
- [[Affinity-specificity tradeoff in antibodies is partially mediated by varying the magnitude of rigidification]]
- [[Agonist antibodies benefit from low affinity due to antigen clustering]]
- [[AlphaFold2 recapitulates interaction biases from PDB when modeling antibodies]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Anti-nanobody immunogenic reactions disproportionately target their C-termini]]
- [[Antibodies and BCRs have different binding kinetics]]
- [[Antibodies and nanobodies can desymmetrize proteins for cryoEM]]
- [[Antibodies can be humanized using AlphaFold2 models]]
- [[Antibodies from different repertoires within a given species targeting the same epitope often have the same light chain isotype and share critical residues]]
- [[Antibodies from naive B cells are more polyreactive]]
- [[Antibodies with distinct V genes and CDRH3 loops can convergently evolve to bind the same epitope]]
- [[Antibody LMs are worse for expression prediction than generic PLMs]]
- [[Antibody LMs outperform generic PLMs on intrafamily thermostability prediction]]
- [[Antibody PLMs match or outperform generic PLMs on specificity prediction]]
- [[Antibody affinity can be improved by stabilization]]
- [[Antibody developability parameters predicted from sequence are more correlated with each other than those predicted from structure]]
- [[Antibody developability predictions are relatively stable to single point mutations]]
- [[Antibody developability predictions from computational models are sensitive to the structure prediction method]]
- [[Antibody hydrophobicity, polyspecificity, and thermostability are not correlated]]
- [[Antibody language models are able to distinguish correctly and incorrectly paired sequences, but are sensitive to scale and training dataset size]]
- [[Antibody on and off rates are capped by the affinity maturation process]]
- [[Antibody sequence similarity is not correlated with developability similarity]]
- [[Antibody structure prediction improved with AlphaFold2 features]]
- [[Antibody thermostability decreases during affinity maturation]]
- [[Antibody-antigen binding modes are not necessarily defined by induced fit]]
- [[Antigen context improves CDRH3 structure prediction]]
- [[Arginine residues in CDRH3 increases promiscuity]]
- [[Attention matrices from antibody LMs can be used for paratope prediction]]
- [[Attention matrices of antibody language models do not correspond to contacts]]
- [[Autoimmune diseases involve the constant activation and reactivation of new B cells]]
- [[B-cell proliferation is driven by both antigen binding and surface expression]]
- [[Biparatopic antibodies can induce clustering beyond what is observed in monoparatopic antibodies]]
- [[Broadly neutralizing antibodies against HIV evolve in a subset of patients]]
- [[Broadly neutralizing antibodies are more evolutionarily distant from germline sequences than less polyspecific antibodies]]
- [[CDR representations segregate into distinct clusters]]
- [[CDR3 far more likely to be part of paratope of nanobodies compared to antibodies]]
- [[CDR3 loops encode specificity while CDR1 and CDR2 encode cross-reactivity]]
- [[CDR3 mediates heavy-light chain pairing preferences by making contacts to framework residues]]
- [[CDRH3 conformation is affected by interdomain orientation]]
- [[CDRH3 conformational rigidity reduces cross reactivity]]
- [[CDRH3 flanking residues more conserved and easier to predict than those in the center]]
- [[CDRH3 has most contacts with antigen]]
- [[CDRH3 is necessary but insufficient to guarantee binding to a particular epitope]]
- [[CDRH3 is shorter in mice and therapeutic Abs]]
- [[CabBCII-10 is a universal nanobody framework capable of accepting diverse CDRs]]
- [[Changes to hydrophobicity and charge correlate with antibody escape]]
- [[Circulating antibodies can undergo further affinity maturation against new antigen variants]]
- [[Classifiers can be used as predictors of continuous properties]]
- [[Clonal expansion correlates with antigen binding]]
- [[Composition of negative data affects rule discovery in binary classification tasks]]
- [[Conformational entropy in antibodies is inversely proportional to antigen affinity]]
- [[Contrastive fine-tuning PLMs on inverse folding embeddings of experimental structures but not computational models improves downstream tasks]]
- [[Contrastive learning on whole structures leads to learning of substructures]]
- [[Correct CDRH3 prediction is necessary but insufficient for correct Ab-Ag docking]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
- [[Cytokines can be added to antibody CDRs]]
- [[DL antibody prediction tools introduce D-amino acids and cis-amide bonds]]
- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
- [[Deep learning methods produce different CDRH3 conformers]]
- [[Different CDRL3 lengths are found in functional and dysfunctional antibodies]]
- [[Different antibody lineages can undergo convergent evolution during affinity maturation]]
- [[Dropout improves AF2 multimer prediction, including for antibody-antigen complexes]]
- [[Dynamic time warping]]
- [[ESM-IF outperforms ProteinMPNN on Ab inverse folding and affinity prediction]]
- [[Ensemble samplers and Gaussian process equally useful for automated antibody design]]
- [[Epistasis in antibodies during affinity maturation can be driven by CDR rearrangements]]
- [[Features for antibody property prediction derived from MD simulations outperform those from language models and static structures]]
- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[Germline precursors bind to their antigens with nanomolar affinity]]
- [[Germline usage determines whether nanobody CDR3 is kinked or extended]]
- [[Hallucination of CDRs]]
- [[Heavy and light chains of de novo designed antibodies with the same framework and binding mode can be exchanged]]
- [[Heavy chain scFvs are stronger binders than light chain scFv]]
- [[Humanization can destabilize antibodies]]
- [[Improvements in antigen binding are correlated with decreases in expression]]
- [[Inclusion of adjacent loops can improve CDRH3 structural modeling]]
- [[Individual D genes are evolutionarily selected for well-defined antigen-binding capabilities]]
- [[Individual V, D, and J gene usage is highly uneven]]
- [[Insufficient ddG data on Abs for training]]
- [[Inverse folding models can predict antibody-antigen binding affinities with higher accuracy by correcting with predictions from unbound state]]
- [[Inverse folding models trained on all proteins outperform those trained on Abs for CDR prediction]]
- [[Inverse folding of CDRs benefits from span masking during training]]
- [[Kappa light chains are far more common in antibody therapeutics]]
- [[Kappa subtype restricts CDRH3 dynamics]]
- [[Kinked nanobody CDR3s are longer than extended CDR3s]]
- [[Kinks in nanobody CDR3 loops are correctly predicted by structure prediction methods]]
- [[LM-based antibody structure prediction methods work equally well with generic and Ab PLMs]]
- [[Lambda light chains are less thermostable]]
- [[Lambda light chains are more hydrophobic]]
- [[Length independent clustering improves CDR prediction]]
- [[Light chain CDR charges can shorten half-life by slowing release from FcRn]]
- [[Light chain coherence]]
- [[Light chain determines autospecificity]]
- [[Light chain representations affected by heavy chain, but not vice versa]]
- [[Longer CDRH3 correlates with higher polyspecificity and hydrophobicity]]
- [[Loops from one V-region chain affect the conformations and dynamics of loops in the other chain]]
- [[Lower antibody affinity is desirable for minimizing on-target off-tumor binding]]
- [[ML optimized Ab libraries have more mutations than PSSM libraries]]
- [[Membrane proteins can be bulked up for cryo-EM by inserting designed domains, including those with predefined epitopes for antibodies]]
- [[Most camelid-derived nanobodies have high sequence identity with human IGHV3]]
- [[Most commercially available tool antibodies are nonspecific]]
- [[Most nanobodies do not bind using all three CDRs]]
- [[Most point mutations that antibodies obtain during affinity maturation are the result of single nucleotide changes]]
- [[Multiple nanobodies can bind simultaneously]]
- [[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding]]
- [[NGS sequence abundance does not correlate with binding affinity]]
- [[Nanobodies and Abs target different epitopes but with similar accessibility and number of contacts]]
- [[Nanobodies are more easily expressed in bacteria and yeast than IgG antibodies]]
- [[Nanobodies designed de novo from sequence are more flexible than either those designed from structure or those occurring in nature]]
- [[Nanobodies designed de novo from sequence are more flexible than those designed from structure or occurring in nature]]
- [[Nanobody CDR1 and CDR2 do not conform to the canonical clustering patterns found in traditional antibodies]]
- [[Nanobody CDRH3 loops are longer but more compact]]
- [[Nanobody FR2 is more hydrophilic than that of antibodies]]
- [[Nanobody framework residues more likely to be part of paratope than those of antibodies]]
- [[Net charge of CDRs strongly predicts nonspecific binding]]
- [[No one-size-fits-all approach to scoring antibody structures]]
- [[Optimal scaling of antibody LMs improves prediction of masked CDRH3 residues but not framework residues]]
- [[PAE weakly correlates with Ab-Ag binding]]
- [[PLMs are better at reproducing sequence-based developability predictions than structure-based predictions]]
- [[PLMs are biased toward germline antibodies]]
- [[PLMs can separate Abs by origin]]
- [[PLMs cluster antibodies from the same repertoire by maturation status]]
- [[PSSMs for Ab engineering outperforms random]]
- [[Paired antibody LMs outperform equivalent unpaired LMs on sequence recovery for various regions]]
- [[Paratope losses are required to enforce CDR-mediated antigen binding during de novo antibody design by hallucination]]
- [[Partial diffusion of de novo designed binders and VHHs improves refoldability and designability scores]]
- [[Protein-protein interaction interfaces are highly degenerate]]
- [[Psi torsion angles are effective metadynamic CVs for CDRH3 and CDRL3]]
- [[PyRosetta convert mAb structure numbering]]
- [[QM-MM and unbiased MD are insufficient to correctly determine CDRH3 conformation]]
- [[Secondary structure losses are required to enforce CDR loopiness during de novo antibody design by hallucination]]
- [[Sequence clusters and structural clusters of CDRH3 do not overlap]]
- [[Simultaneous design of scFv loops predicted to lead to more fit sequences]]
- [[Somatic hypermutation correlates with lower hydrophobicity]]
- [[Somatic hypermutation correlates with lower polyreactivity]]
- [[Some light chain V-genes are more likely to be found in dysfunctional antibodies]]
- [[Source of immunogenicity in VHH nanobodies]]
- [[Structural modeling introduces bias toward larger hydrophobic patches in antibodies]]
- [[Structure-based methods outperform sequence-based methods on antigen-dependent antibody design]]
- [[Subset of mutations obtained during affinity maturation contribute disproportionately to affinity]]
- [[Template CDR retrieval using embeddings]]
- [[The solubilization tetrad allows camelid nanobodies to remain soluble in the absence of a light chain]]
- [[The structures of nanobodies with kinked CDR3 loops are more difficult to predict in complex with their antigen]]
- [[There are 4.6 million possible combinations of human antibodies given VDJ and VJ scrambling alone]]
- [[Transgenic mice with only a single VH gene are nonetheless able to make effective antibodies against many targets]]
- [[Up to 22 percent of antigen binding residues are outside CDRs]]
- [[Variable regions can adopt multiple interchain arrangements, and these are difficult to predict]]
- [[Wildtype antibody frameworks can accommodate CDRs that bind to virtually any target]]
- [[Zero-shot protein stability prediction using inverse folding models can be improved by subtracting predictions from residue in isolation]]
- [[pLDDT is inversely correlated with CDRH3 length]]
