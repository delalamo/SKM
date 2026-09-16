# Note proposals from issue annotations

Drafts for the nine papers retained after triage, excluding PANDA (#854), with the subsequent LLM-design MOC and supporting papers. Each new note follows the garden's Summary / Details / Figures / See also structure where applicable, uses the topic taxonomy, and links to existing concepts. The ESM3 references resolve to the existing ESM entry through `[[ESM|ESM3]]`.

## Placement and duplicate checks

The note filenames, note bodies, and bibliography were searched for the paper identifiers, named methods, and related findings. None of the nine papers already had a bibliography record. Four existing notes received supporting evidence; distinct findings received new notes.

| Issue and paper | Proposed placement | Reason |
| --- | --- | --- |
| [#845: Super-compensatory substitutions](https://github.com/delalamo/SKM/issues/845) | Append to [Highly thermostable sequences make better starting points to evolve new functions](<../content/notes/Highly thermostable sequences make better starting points to evolve new functions.md>) | Mutational buffering extends the existing stability/evolvability finding. Distinguishes measured fitness from predicted stabilization and from the untested acquisition of new functions. |
| [#838: De novo CARs](https://github.com/delalamo/SKM/issues/838) | New: [Redesigning non-interface residues can reduce off-target activation by de novo CAR binders](<../content/notes/Redesigning non-interface residues can reduce off-target activation by de novo CAR binders.md>) | Existing non-interface affinity-maturation and CDR-charge notes address related but different outcomes. |
| [#828: MSFold](https://github.com/delalamo/SKM/issues/828) | New: [Parallel tempering of ESM3 structure tokens can recover alternative conformations](<../content/notes/Parallel tempering of ESM3 structure tokens can recover alternative conformations.md>) | Existing replica-exchange and conformational-sampling notes do not describe sampling in ESM3's discrete token space. |
| [#824: Inverse FoldDir](https://github.com/delalamo/SKM/issues/824) | New finding: [Inverse folding by flow matching resolves residue identities at different times](<../content/notes/Inverse folding by flow matching resolves residue identities at different times.md>); new method entry: [Inverse FoldDir](<../content/notes/Inverse FoldDir.md>) | Separates residue-level convergence from the existing joint sequence/structure scheduling result. The method entry answers the training-data comparison with ESM-IF. |
| [#812: Ligand design with LLMs](https://github.com/delalamo/SKM/issues/812) | New: [General-purpose language models can propose ligand binders but do not reliably satisfy design constraints](<../content/notes/General-purpose language models can propose ligand binders but do not reliably satisfy design constraints.md>) | Existing PLM and design-validation notes do not cover this experiment with general-purpose text models. |
| [#805: ABAG-Rank](https://github.com/delalamo/SKM/issues/805) | Append to [Aggregate benchmark correlations can mask weak within-category performance](<../content/notes/Aggregate benchmark correlations can mask weak within-category performance.md>) | Direct example of the existing pooled-versus-within-group correlation finding. Structural quality is distinguished from affinity. |
| [#802: Natalizumab](https://github.com/delalamo/SKM/issues/802) | New: [Natalizumab can adopt a compact closed conformation that shields the Fc region](<../content/notes/Natalizumab can adopt a compact closed conformation that shields the Fc region.md>) | No existing note addresses this full-length antibody arrangement. Generalization and antigen-triggered opening are qualified. |
| [#796: ADP-3D](https://github.com/delalamo/SKM/issues/796) | New: [Diffusion priors improve reconstruction from sparse distances without guaranteeing a unique structure](<../content/notes/Diffusion priors improve reconstruction from sparse distances without guaranteeing a unique structure.md>); append density-fitting evidence to [Protein backbone design diffusion models can be repurposed for fitting structures into electron density](<../content/notes/Protein backbone design diffusion models can be repurposed for fitting structures into electron density.md>) | Density fitting already exists; sparse-distance reconstruction and ambiguity are a distinct finding. |
| [#736: Foldseek-Interface](https://github.com/delalamo/SKM/issues/736) | Reframe and rename the existing note as [Protein interface space remains far from complete despite recurring local geometries](<../content/notes/Protein interface space remains far from complete despite recurring local geometries.md>); new: [Protein interface clusters rarely span experimental structure determination methods](<../content/notes/Protein interface clusters rarely span experimental structure determination methods.md>) | Give the broader Foldseek-Interface analysis priority for claims about coverage. Retain the narrower observation of local geometric reuse, remove the unsupported 10,000-fragment count, and preserve the old title as an alias. Experimental-method coverage is separate. |

## LLM-design follow-up

[Large language models in molecular and protein design](<../content/notes/Large language models in molecular and protein design.md>) connects the #812 ligand-design note to three additional findings:

- [PG-LLM: variant ranking without specialist tools](<../content/notes/General-purpose language models can rank protein variants without specialist tools.md>), using the August 19, 2026 paper revision and its ranking figure.
- [OpenDDE-Harness: mutation proposals guided by structural feedback](<../content/notes/LLM-proposed antibody mutations can yield binders when guided by structural feedback.md>), using the September 10, 2026 technical-report revision and its experimental-binding figure.
- [Anthropic: autonomous coordination of protein-design campaigns](<../content/notes/LLM agents can autonomously coordinate protein design campaigns that yield experimental binders.md>), using the August 18, 2026 report and its tool-orchestration figure. The existing bibliography entry and separate filtering-ensemble note are reused.

The MOC distinguishes retrospective ranking, direct sequence proposals, feedback-guided search, and autonomous computational campaign management. It links to related notes and the Design overview. Numerical comparisons and experimental outcomes are written as text tables rather than table screenshots.

## Figures and tables

- Retained the three issue-attached plots: His3p rescuability (Figure 1E), Inverse FoldDir convergence (Figure 2A-C), and ADP-3D sparse-distance reconstruction (Figure 4).
- Extracted the natalizumab open/closed schematic (Figure 8), with a caption distinguishing the proposed antigen-triggered mechanism from direct measurements.
- Recreated the complete numerical ABAG-Rank Table 1 as Markdown. Its statistical-significance symbols are explicitly omitted; timing qualifications and metric directions are retained. The 123 KB table screenshot was not added.
- Added small text tables for the CAR activation comparison, Inverse FoldDir refolding benchmark, and LLM design outcomes.

## Primary sources inspected

| Citation key | Full text |
| --- | --- |
| `jiang2026supercompensators` | [Jiang et al., bioRxiv version 5](https://www.biorxiv.org/content/10.1101/2025.01.11.631697v5), particularly Figures 1-5 and S6 |
| `chow2026` | [Chow et al., Nature Biomedical Engineering](https://www.nature.com/articles/s41551-026-01790-9), particularly the off-target CAR results and Figure 6 |
| `wang2026msfold` | [Wang et al., bioRxiv version 3](https://www.biorxiv.org/content/10.64898/2026.03.03.708411v3), particularly Sections 2.1, 2.3, 2.5, and 2.6 |
| `tartici2026` | [Tartici et al., bioRxiv version 2](https://www.biorxiv.org/content/10.64898/2026.09.06.749733v2), particularly Figures 2-3, Figure S1, Tables 1 and 3, and Section 5.4 |
| `kim2026llmdesign` | [Kim et al., bioRxiv version 1](https://www.biorxiv.org/content/10.64898/2026.09.02.748987v1), metal and PFOA results and Discussion |
| `tadiello2026` | [Tadiello et al., accepted manuscript](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btag663/8785291), evaluation definitions and Table 1 |
| `chrone2026` | [Chrone et al., version of record](https://doi.org/10.1016/j.bbapap.2026.141174), retrieved through the [authors' university repository](https://orbit.dtu.dk/en/publications/native-structure-of-the-therapeutic-igg4-%CE%B14%CE%B25-integrin-antibody-n/), particularly Discussion and Figure 8 |
| `levy2024` | [Levy et al., arXiv version 2](https://arxiv.org/html/2406.04239v2), particularly Figure 4, Discussion, and Appendix G.1 |
| `strom2026` | [Strom et al., bioRxiv version 2](https://www.biorxiv.org/content/10.64898/2026.08.24.746585v2), particularly Figure 3, Figure S2h, and Discussion |

The Inverse FoldDir data comparison also uses its [released model card](https://huggingface.co/AlpTartici/inversefolddir#training-data) and the [ESM-IF paper](https://proceedings.mlr.press/v162/hsu22a.html). Inverse FoldDir uses roughly 2.8 million filtered predicted structures, compared with ESM-IF's roughly 12 million; these are different corpora, and the benchmark does not isolate an architectural advantage.

## Review checks

- Twelve new pages (eleven notes and one MOC), eleven bibliography entries, and seven retained figures, with existing findings and navigation updated.
- All newly added note links, figure embeds, and citation keys resolve.
- The Quartz site build passed. The rendered benchmark table scrolls horizontally within the note, and the retained antibody schematic and caption were visually checked.
