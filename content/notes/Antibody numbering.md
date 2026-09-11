---
title: Antibody numbering
created: 2026-04-10T14:02:57
modified: "2026-09-11T12:44:28"
aliases:
  - Antibody numbering conventions
  - Antibody numbering schemes
  - Kabat numbering
  - Chothia numbering
  - Martin numbering
  - Enhanced Chothia numbering
  - IMGT numbering
  - AHo numbering
  - Gelfand numbering
  - WolfGuy numbering
  - EU numbering
tags:
  - antibodies/architecture
---

**Antibody numbering assigns comparable labels to residues in variable-length immunoglobulin domains.** This is the reference page for numbering conventions in these notes, including [[tags/antibodies|antibodies]], [[Nanobodies|VHHs]], [[T-cell receptors|TCRs]], and shark IgNARs. Use it alongside [[Complementarity-determining regions]] for loop biology and [[PyRosetta convert mAb structure numbering]] for a structure-conversion recipe.

A residue label needs a **scheme, domain/chain, number, and any insertion code**: for example, Kabat H100A. It is neither a sequence-array index nor necessarily the number already present in a PDB file. **Numbering and CDR definition are separate choices**: an antibody can use one set of residue labels and another set of CDR boundaries. Renumbering does not change the molecule or establish which residues contact antigen.

## Schemes and their origins

| Scheme | How it was obtained | What the labels mean; original reference |
| --- | --- | --- |
| **Kabat** | **Sequence alignment and variability.** Hypervariable segments were identified from aligned Bence Jones/myeloma light-chain sequences; the reference collection subsequently expanded. | Separate heavy- and light-chain coordinates; extra residues receive letters such as H35A or H100A. Foundation: Wu & Kabat (1970) [@wukabat1970]; standard compilation: Kabat et al. (1991), *Sequences of Proteins of Immunological Interest*, 5th ed. [@kabat1991]. |
| **Chothia** | **Structures, refining Kabat.** Crystal-structure comparisons identified canonical loop conformations and placed insertions at structurally corresponding sites. | Retains much of Kabat's framework numbering, but changes loop insertion placement, notably H1 and L1. Cite Chothia & Lesk (1987) and the later Al-Lazikani et al. (1997) convention; historical versions differ [@chothia1987; @allazikani1997]. |
| **Martin / enhanced Chothia** | **Sequence and structure audit.** Corrected inconsistent Kabat annotations and extended structural corrections into the frameworks. | Refines Chothia, including relocation of heavy-chain framework insertions from H82 to H72 and a light-chain deletion convention. This is distinct from the AbM CDR definition. Abhinandan & Martin (2008) [@abhinandan2008]. |
| **IMGT, V-domain** | **Sequence alignment constrained by structure.** Developed from thousands of sequences together with conserved framework residues, crystallographic structures, and loop information. | A common 1–128 coordinate system for IG/TR variable domains and IgSF V-like domains; unused positions are gaps and unusually long loops add positions. Introduced by Lefranc (1997); full V-domain treatment by Lefranc et al. (2003) [@lefranc1997; @lefranc2003]. |
| **AHo / Honegger–Plückthun** | **Structural superposition.** Alignments of variable-domain structures established corresponding core residues and preferred gap locations. | A shared 1–149 coordinate system across antibody and TCR variable domains, reserving space for long loops. A gap is an unoccupied label, not a missing experimental residue. Honegger & Plückthun (2001) [@honegger2001]. |
| **Gelfand–Kister** | **Sequence statistics plus secondary/tertiary structure.** Compared conserved sequence patterns and contacts in antibody structures. | Describes the fold through structural “words,” with positions within those segments, rather than just one continuous integer series. Gelfand & Kister (1995) [@gelfand1995]. |
| **WolfGuy** | **Structure-oriented modeling convention.** Uses loop length and, in some cases, sequence to label the two sides of a loop. | Separate heavy/light number blocks and ascending/descending loop sections; its CDR definition combines Kabat and Chothia. Bujotzek et al. (2015), with implementation details in *MoFvAb* [@bujotzek2015; @bujotzek2015mofvab]. |
| **EU index** | **Reference protein sequence.** Derived from the experimentally determined human IgG1 Eu sequence. | Commonly used for IgG constant-region/Fc mutations, such as N297. “EU numbering as in Kabat” is not Kabat variable-domain numbering. Edelman et al. (1969) [@edelman1969]. |
| **IMGT, C-domain** | **Sequence/structure correspondence between constant domains.** Extends homologous positions across IG/TR C-domains and IgSF C-like domains. | Numbering is local to each domain: name CH1, CH2, CH3, CL, etc. It does not continue the V-domain's residue count. Lefranc et al. (2005) [@lefranc2005]. |

A structurally derived scheme can still be assigned **from sequence alone**. ANARCI uses profile hidden Markov models and then converts the alignment into the requested scheme; ANARCII predicts numbering with a trained sequence model. These are assignment tools, not additional numbering schemes [@dunbar2016; @greenshieldswatson2026].

## Which molecules can use each scheme?

The relevant unit is the **domain**, not the antibody's isotype. The VH/VL domains of IgG, IgM, IgA, IgE, and IgD use the same kinds of variable-domain conventions. Fab, Fv, scFv, and antibody-derived CAR modules inherit the numbering of their constituent domains; linkers and constant regions require separate annotation.

**Standard** means explicitly established for that domain family; **VH use** means applying the antibody heavy-domain convention; **specialized** means an adapted/validated assignment is needed. A dash means this is not the scheme's standard scope, not that no historical paper has ever used an adaptation.

| Scheme | Conventional IG VH/Vκ/Vλ, any isotype | Camelid VHH | TCR Vα/Vβ | TCR Vγ/Vδ | Shark VNAR (IgNAR variable domain) | Constant or other IgSF domains |
| --- | --- | --- | --- | --- | --- | --- |
| Kabat | Standard | VH use | Historical conventions; not standard modern output | Historical conventions; not standard modern output | Specialized | Separate constant-region conventions; see EU |
| Chothia | Standard | VH use | — | — | Specialized | — |
| Martin | Standard | VH use | — | — | Specialized | — |
| IMGT V-domain | Standard | Standard | Standard | Standard | Specialized IMGT assignment | IgSF **V-like** domains |
| AHo | Standard | VH use | Standard | Standard | Structural adaptation; validate | Variable domains; not a general C-domain scheme |
| Gelfand–Kister | Antibody structural alignment | Structural adaptation | — | — | Structural adaptation | No general constant-domain index |
| WolfGuy | Antibody modeling convention | VH use; check implementation | — | — | Specialized | — |
| EU | Use a V-domain scheme for comparisons | — | — | — | — | IgG reference sequence, especially CH1/hinge/Fc |
| IMGT C-domain | — | — | — | — | Not a VNAR scheme | IG/TR **C-domains** and IgSF **C-like** domains |

Coverage follows the original IMGT/AHo papers and the [ANARCI authors' supported schemes](https://github.com/oxpig/ANARCI#schemes); a particular program can support fewer species or chains than the convention itself [@lefranc2003; @lefranc2005; @honegger2001; @dunbar2016]. Camelid VHH numbering is illustrated experimentally by the [[The solubilization tetrad allows camelid nanobodies to remain soluble in the absence of a light chain|VHH humanization work]] [@vincke2009].

**VNAR needs special care.** It lacks the conventional antibody CDR2 architecture, so calling every assigned IMGT 56–65 residue “CDR2” is misleading. ANARCII's VNAR study required conditioned or specialized models to place the large gap consistently across the CDR2/framework region. A successful generic antibody-numbering run is insufficient validation [@greenshieldswatson2026].

## CDR definitions are not numbering schemes

Chothia boundaries vary among historical publications; the commonly used convention is shown here. These common boundaries are stated in **each row's named coordinates**, including insertion labels within the interval. They describe the conventional definitions, not the measured paratope of an individual antibody. For insertion-bearing H1/L1 loops, use the [IMGT length-specific correspondence tables](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTcorrespondence.html) rather than treating identical-looking endpoint numbers as identical residues [@wukabat1970; @chothia1987; @allazikani1997; @lefranc2003].

| CDR definition and coordinate system | H1 | H2 | H3 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- | --- | --- |
| Kabat definition, **Kabat** coordinates | 31–35, including 35A/B when present | 50–65 | 95–102 | 24–34 | 50–56 | 89–97 |
| Common Chothia definition, **Chothia** coordinates | 26–32 | 52–56 | 95–102 | 24–34 | 50–56 | 89–97 |
| IMGT definition, **IMGT** coordinates | 27–38 | 56–65 | 105–117 | 27–38 | 56–65 | 105–117 |

Other frequently encountered labels belong here:

- **AbM:** modeling-oriented CDR boundaries associated with antibody loop modeling; not a synonym for Martin numbering [@martin1989].
- **Contact / MacCallum:** boundaries derived from contacts in antibody–antigen crystal structures. A generic contact definition does not identify every contact in a new complex [@maccallum1996].
- **North–Dunbrack / PyIgClassify:** loop boundaries and conformational classes based on structural alignments and stable flanking anchors. State the numbering separately, including when these loops are expressed in AHo coordinates [@north2011].

For example, **Kabat H93/H94 are outside Kabat-defined H3 but correspond to IMGT 105/106, inside CDR3-IMGT**. Similarly, Kabat H71 remains a framework residue even though it can determine H2 conformation. Functional importance, structural-loop membership, and a chosen CDR definition are related but distinct [@lefranc2003; @tramontano1990].

## Residue-to-structure equivalence

### Frameworks, loops, and conserved landmarks

The IMGT coordinate system provides the common structural reference below. These ranges are **numbering/annotation boundaries**, not a DSSP assignment for every crystal structure. Short loops leave gaps; long loops add positions. Conserved identities are typical evolutionary anchors, not requirements that every engineered sequence must satisfy [@lefranc2003].

| IMGT positions | Region | Structural interpretation |
| --- | --- | --- |
| 1–26 | FR1 | N-terminal framework, including strands A/B; first conserved cysteine at 23 |
| 27–38 | CDR1 | BC loop between strands B and C |
| 39–55 | FR2 | Framework around strands C/C′; conserved core Trp41 |
| 56–65 | CDR2 | C′C″ loop in conventional antibody/TCR V-domains |
| 66–104 | FR3 | C″/D/E/F framework and intervening turns, including the DE loop; hydrophobic 89 and second cysteine 104 |
| 105–117 | CDR3 | FG loop; 104 and 118 are its flanking anchors, not part of CDR3-IMGT |
| 118–128 | FR4 | J-derived G-strand framework, beginning with the conserved aromatic/Gly motif |

Here H and L refer to heavy- and light-domain labels, not the arbitrary chain IDs in a PDB. The numeric assignments match the examples below and the primary IMGT/AHo references. The Martin H77 versus Kabat/Chothia H80 difference reflects the common heavy-framework insertion convention [@abhinandan2008; @honegger2001; @lefranc2003].

| Landmark | IMGT | AHo | Kabat H / L | Chothia H / L | Martin H / L |
| --- | --- | --- | --- | --- | --- |
| First conserved Cys; strand B | 23 | 23 | H22 / L23 | H22 / L23 | H22 / L23 |
| Conserved Trp; strand C, hydrophobic core | 41 | 43 | H36 / L35 | H36 / L35 | H36 / L35 |
| H2-supporting framework site (VH) | 80 | 82 | H71 | H71 | H71 |
| Conserved hydrophobic residue; strand E | 89 | 91 | H80 / L73 | H80 / L73 | H77 / L73 |
| Second conserved Cys; strand F | 104 | 106 | H92 / L88 | H92 / L88 | H92 / L88 |
| J Phe/Trp; strand G, start of FR4 | 118 | 139 | H103 / L98 | H103 / L98 | H103 / L98 |
| First Gly of J motif | 119 | 140 | H104 / L99 | H104 / L99 | H104 / L99 |
| Second Gly of J motif | 121 | 142 | H106 / L101 | H106 / L101 | H106 / L101 |

The two conserved cysteines usually form the **intradomain B–F disulfide**. Extra cysteines in VHHs and VNARs may form other disulfides; they should not be mistaken for these anchors. The [[The solubilization tetrad allows camelid nanobodies to remain soluble in the absence of a light chain|VHH solubility tetrad]] is another useful cross-check: **IMGT 42/49/50/52 = Kabat H37/H44/H45/H47** [@lefranc2003; @vincke2009].

### Full position correspondence

The expandable tables map **every occupied residue** of three deposited example domains across **IMGT, Kabat, Chothia, Martin, AHo, and WolfGuy**, and identify its IMGT region and conserved landmarks. Heavy, κ, and λ examples are separate because their correspondences differ. These are **sequence-specific assigned labels**, not a universal structural alignment or a list of every possible insertion.

[Download the residue crosswalk](../assets/antibody-numbering-crosswalk.csv) and [frozen input sequences and provenance](../assets/antibody-numbering-inputs.json). Generated with **ANARCII 2.0.8, antibody accuracy model**, on 2026-09-11. IMGT assignments were converted by its bundled Kabat/Chothia/Martin/AHo routines; WolfGuy was assigned to the same alignment using the [ANARCI authors' pinned conversion implementation](https://github.com/oxpig/ANARCI/blob/79f6c575056dedef86cb8f405ebb039197923eec/lib/python/anarci/schemes.py). Amino-acid identity/order, unique labels, and conserved anchors were checked. The [reproduction script](https://github.com/delalamo/SKM/blob/main/scripts/generate_antibody_numbering.py) also validates the frozen data without rerunning a model [@greenshieldswatson2026; @dunbar2016].

<!-- BEGIN GENERATED CROSSWALK -->

<details>
<summary>Herceptin VH: 120 residues; IMGT CDR lengths 8.8.13</summary>


[PDB 1N8Z](https://www.rcsb.org/structure/1N8Z), author chain **B**, entity **2**. Sequence position counts from the beginning of the deposited sequence; it is not a PDB residue label.


| Seq. | AA | IMGT | Kabat | Chothia | Martin | AHo | WolfGuy | Region / landmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | E | 1 | H1 | H1 | H1 | 1 | 101 | FR1 |
| 2 | V | 2 | H2 | H2 | H2 | 2 | 102 | FR1 |
| 3 | Q | 3 | H3 | H3 | H3 | 3 | 103 | FR1 |
| 4 | L | 4 | H4 | H4 | H4 | 4 | 104 | FR1 |
| 5 | V | 5 | H5 | H5 | H5 | 5 | 105 | FR1 |
| 6 | E | 6 | H6 | H6 | H6 | 6 | 106 | FR1 |
| 7 | S | 7 | H7 | H7 | H7 | 7 | 107 | FR1 |
| 8 | G | 8 | H8 | H8 | H8 | 9 | 108 | FR1 |
| 9 | G | 9 | H9 | H9 | H9 | 10 | 109 | FR1 |
| 10 | G | 11 | H10 | H10 | H10 | 11 | 110 | FR1 |
| 11 | L | 12 | H11 | H11 | H11 | 12 | 111 | FR1 |
| 12 | V | 13 | H12 | H12 | H12 | 13 | 112 | FR1 |
| 13 | Q | 14 | H13 | H13 | H13 | 14 | 113 | FR1 |
| 14 | P | 15 | H14 | H14 | H14 | 15 | 114 | FR1 |
| 15 | G | 16 | H15 | H15 | H15 | 16 | 115 | FR1 |
| 16 | G | 17 | H16 | H16 | H16 | 17 | 116 | FR1 |
| 17 | S | 18 | H17 | H17 | H17 | 18 | 117 | FR1 |
| 18 | L | 19 | H18 | H18 | H18 | 19 | 118 | FR1 |
| 19 | R | 20 | H19 | H19 | H19 | 20 | 119 | FR1 |
| 20 | L | 21 | H20 | H20 | H20 | 21 | 120 | FR1 |
| 21 | S | 22 | H21 | H21 | H21 | 22 | 121 | FR1 |
| 22 | C | 23 | H22 | H22 | H22 | 23 | 122 | FR1; Cys; B strand / disulfide |
| 23 | A | 24 | H23 | H23 | H23 | 24 | 123 | FR1 |
| 24 | A | 25 | H24 | H24 | H24 | 25 | 124 | FR1 |
| 25 | S | 26 | H25 | H25 | H25 | 26 | 125 | FR1 |
| 26 | G | 27 | H26 | H26 | H26 | 27 | 151 | CDR1 |
| 27 | F | 28 | H27 | H27 | H27 | 29 | 152 | CDR1 |
| 28 | N | 29 | H28 | H28 | H28 | 30 | 153 | CDR1 |
| 29 | I | 30 | H29 | H29 | H29 | 31 | 154 | CDR1 |
| 30 | K | 35 | H30 | H30 | H30 | 32 | 155 | CDR1 |
| 31 | D | 36 | H31 | H31 | H31 | 33 | 156 | CDR1 |
| 32 | T | 37 | H32 | H32 | H32 | 39 | 196 | CDR1 |
| 33 | Y | 38 | H33 | H33 | H33 | 40 | 197 | CDR1 |
| 34 | I | 39 | H34 | H34 | H34 | 41 | 198 | FR2 |
| 35 | H | 40 | H35 | H35 | H35 | 42 | 199 | FR2 |
| 36 | W | 41 | H36 | H36 | H36 | 43 | 201 | FR2; Trp; C strand / core |
| 37 | V | 42 | H37 | H37 | H37 | 44 | 202 | FR2 |
| 38 | R | 43 | H38 | H38 | H38 | 45 | 203 | FR2 |
| 39 | Q | 44 | H39 | H39 | H39 | 46 | 204 | FR2 |
| 40 | A | 45 | H40 | H40 | H40 | 47 | 205 | FR2 |
| 41 | P | 46 | H41 | H41 | H41 | 48 | 206 | FR2 |
| 42 | G | 47 | H42 | H42 | H42 | 49 | 207 | FR2 |
| 43 | K | 48 | H43 | H43 | H43 | 50 | 208 | FR2 |
| 44 | G | 49 | H44 | H44 | H44 | 51 | 209 | FR2 |
| 45 | L | 50 | H45 | H45 | H45 | 52 | 210 | FR2 |
| 46 | E | 51 | H46 | H46 | H46 | 53 | 211 | FR2 |
| 47 | W | 52 | H47 | H47 | H47 | 54 | 212 | FR2 |
| 48 | V | 53 | H48 | H48 | H48 | 55 | 213 | FR2 |
| 49 | A | 54 | H49 | H49 | H49 | 56 | 214 | FR2 |
| 50 | R | 55 | H50 | H50 | H50 | 57 | 251 | FR2 |
| 51 | I | 56 | H51 | H51 | H51 | 58 | 252 | CDR2 |
| 52 | Y | 57 | H52 | H52 | H52 | 59 | 253 | CDR2 |
| 53 | P | 58 | H52A | H52A | H52A | 60 | 254 | CDR2 |
| 54 | T | 59 | H53 | H53 | H53 | 61 | 255 | CDR2 |
| 55 | N | 62 | H54 | H54 | H54 | 65 | 288 | CDR2 |
| 56 | G | 63 | H55 | H55 | H55 | 66 | 289 | CDR2 |
| 57 | Y | 64 | H56 | H56 | H56 | 67 | 290 | CDR2 |
| 58 | T | 65 | H57 | H57 | H57 | 68 | 291 | CDR2 |
| 59 | R | 66 | H58 | H58 | H58 | 69 | 292 | FR3 |
| 60 | Y | 67 | H59 | H59 | H59 | 70 | 293 | FR3 |
| 61 | A | 68 | H60 | H60 | H60 | 71 | 294 | FR3 |
| 62 | D | 69 | H61 | H61 | H61 | 72 | 295 | FR3 |
| 63 | S | 70 | H62 | H62 | H62 | 73 | 296 | FR3 |
| 64 | V | 71 | H63 | H63 | H63 | 74 | 297 | FR3 |
| 65 | K | 72 | H64 | H64 | H64 | 75 | 298 | FR3 |
| 66 | G | 74 | H65 | H65 | H65 | 76 | 299 | FR3 |
| 67 | R | 75 | H66 | H66 | H66 | 77 | 301 | FR3 |
| 68 | F | 76 | H67 | H67 | H67 | 78 | 302 | FR3 |
| 69 | T | 77 | H68 | H68 | H68 | 79 | 303 | FR3 |
| 70 | I | 78 | H69 | H69 | H69 | 80 | 304 | FR3 |
| 71 | S | 79 | H70 | H70 | H70 | 81 | 305 | FR3 |
| 72 | A | 80 | H71 | H71 | H71 | 82 | 306 | FR3; H2-supporting H71 site (VH only) |
| 73 | D | 81 | H72 | H72 | H72 | 83 | 307 | FR3 |
| 74 | T | 82 | H73 | H73 | H72A | 84 | 308 | FR3 |
| 75 | S | 83 | H74 | H74 | H72B | 85 | 309 | FR3 |
| 76 | K | 84 | H75 | H75 | H72C | 86 | 310 | FR3 |
| 77 | N | 85 | H76 | H76 | H73 | 87 | 311 | FR3 |
| 78 | T | 86 | H77 | H77 | H74 | 88 | 312 | FR3 |
| 79 | A | 87 | H78 | H78 | H75 | 89 | 313 | FR3 |
| 80 | Y | 88 | H79 | H79 | H76 | 90 | 314 | FR3 |
| 81 | L | 89 | H80 | H80 | H77 | 91 | 315 | FR3; Hydrophobic; E strand / core |
| 82 | Q | 90 | H81 | H81 | H78 | 92 | 316 | FR3 |
| 83 | M | 91 | H82 | H82 | H79 | 93 | 317 | FR3 |
| 84 | N | 92 | H82A | H82A | H80 | 94 | 318 | FR3 |
| 85 | S | 93 | H82B | H82B | H81 | 95 | 319 | FR3 |
| 86 | L | 94 | H82C | H82C | H82 | 96 | 320 | FR3 |
| 87 | R | 95 | H83 | H83 | H83 | 97 | 321 | FR3 |
| 88 | A | 96 | H84 | H84 | H84 | 98 | 322 | FR3 |
| 89 | E | 97 | H85 | H85 | H85 | 99 | 323 | FR3 |
| 90 | D | 98 | H86 | H86 | H86 | 100 | 324 | FR3 |
| 91 | T | 99 | H87 | H87 | H87 | 101 | 325 | FR3 |
| 92 | A | 100 | H88 | H88 | H88 | 102 | 326 | FR3 |
| 93 | V | 101 | H89 | H89 | H89 | 103 | 327 | FR3 |
| 94 | Y | 102 | H90 | H90 | H90 | 104 | 328 | FR3 |
| 95 | Y | 103 | H91 | H91 | H91 | 105 | 329 | FR3 |
| 96 | C | 104 | H92 | H92 | H92 | 106 | 330 | FR3; Cys; F strand / disulfide |
| 97 | S | 105 | H93 | H93 | H93 | 107 | 331 | CDR3 |
| 98 | R | 106 | H94 | H94 | H94 | 108 | 332 | CDR3 |
| 99 | W | 107 | H95 | H95 | H95 | 109 | 351 | CDR3 |
| 100 | G | 108 | H96 | H96 | H96 | 110 | 352 | CDR3 |
| 101 | G | 109 | H97 | H97 | H97 | 111 | 353 | CDR3 |
| 102 | D | 110 | H98 | H98 | H98 | 112 | 354 | CDR3 |
| 103 | G | 111 | H99 | H99 | H99 | 113 | 355 | CDR3 |
| 104 | F | 112 | H100 | H100 | H100 | 133 | 394 | CDR3 |
| 105 | Y | 113 | H100A | H100A | H100A | 134 | 395 | CDR3 |
| 106 | A | 114 | H100B | H100B | H100B | 135 | 396 | CDR3 |
| 107 | M | 115 | H100C | H100C | H100C | 136 | 397 | CDR3 |
| 108 | D | 116 | H101 | H101 | H101 | 137 | 398 | CDR3 |
| 109 | Y | 117 | H102 | H102 | H102 | 138 | 399 | CDR3 |
| 110 | W | 118 | H103 | H103 | H103 | 139 | 401 | FR4; Phe/Trp; G strand / J motif |
| 111 | G | 119 | H104 | H104 | H104 | 140 | 402 | FR4; Gly; J motif |
| 112 | Q | 120 | H105 | H105 | H105 | 141 | 403 | FR4 |
| 113 | G | 121 | H106 | H106 | H106 | 142 | 404 | FR4; Gly; J motif |
| 114 | T | 122 | H107 | H107 | H107 | 143 | 405 | FR4 |
| 115 | L | 123 | H108 | H108 | H108 | 144 | 406 | FR4 |
| 116 | V | 124 | H109 | H109 | H109 | 145 | 407 | FR4 |
| 117 | T | 125 | H110 | H110 | H110 | 146 | 408 | FR4 |
| 118 | V | 126 | H111 | H111 | H111 | 147 | 409 | FR4 |
| 119 | S | 127 | H112 | H112 | H112 | 148 | 410 | FR4 |
| 120 | S | 128 | H113 | H113 | H113 | 149 | 411 | FR4 |

</details>

<details>
<summary>MS6-12 Vκ: 112 residues; IMGT CDR lengths 11.3.9</summary>


[PDB 1MJU](https://www.rcsb.org/structure/1MJU), author chain **L**, entity **1**. Sequence position counts from the beginning of the deposited sequence; it is not a PDB residue label.


| Seq. | AA | IMGT | Kabat | Chothia | Martin | AHo | WolfGuy | Region / landmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | D | 1 | L1 | L1 | L1 | 1 | 501 | FR1 |
| 2 | I | 2 | L2 | L2 | L2 | 2 | 502 | FR1 |
| 3 | V | 3 | L3 | L3 | L3 | 3 | 503 | FR1 |
| 4 | M | 4 | L4 | L4 | L4 | 4 | 504 | FR1 |
| 5 | T | 5 | L5 | L5 | L5 | 5 | 505 | FR1 |
| 6 | Q | 6 | L6 | L6 | L6 | 6 | 506 | FR1 |
| 7 | A | 7 | L7 | L7 | L7 | 7 | 507 | FR1 |
| 8 | A | 8 | L8 | L8 | L8 | 8 | 508 | FR1 |
| 9 | P | 9 | L9 | L9 | L9 | 9 | 509 | FR1 |
| 10 | S | 10 | L10 | L10 | L10 | 10 | 510 | FR1 |
| 11 | V | 11 | L11 | L11 | L11 | 11 | 511 | FR1 |
| 12 | P | 12 | L12 | L12 | L12 | 12 | 512 | FR1 |
| 13 | V | 13 | L13 | L13 | L13 | 13 | 513 | FR1 |
| 14 | T | 14 | L14 | L14 | L14 | 14 | 514 | FR1 |
| 15 | P | 15 | L15 | L15 | L15 | 15 | 515 | FR1 |
| 16 | G | 16 | L16 | L16 | L16 | 16 | 516 | FR1 |
| 17 | E | 17 | L17 | L17 | L17 | 17 | 517 | FR1 |
| 18 | S | 18 | L18 | L18 | L18 | 18 | 518 | FR1 |
| 19 | V | 19 | L19 | L19 | L19 | 19 | 519 | FR1 |
| 20 | S | 20 | L20 | L20 | L20 | 20 | 520 | FR1 |
| 21 | I | 21 | L21 | L21 | L21 | 21 | 521 | FR1 |
| 22 | S | 22 | L22 | L22 | L22 | 22 | 522 | FR1 |
| 23 | C | 23 | L23 | L23 | L23 | 23 | 523 | FR1; Cys; B strand / disulfide |
| 24 | R | 24 | L24 | L24 | L24 | 24 | 551 | FR1 |
| 25 | S | 25 | L25 | L25 | L25 | 25 | 552 | FR1 |
| 26 | S | 26 | L26 | L26 | L26 | 26 | 553 | FR1 |
| 27 | K | 27 | L27 | L27 | L27 | 29 | 556 | CDR1 |
| 28 | S | 28 | L27A | L28 | L28 | 30 | 561 | CDR1 |
| 29 | L | 29 | L27B | L29 | L29 | 31 | 562 | CDR1 |
| 30 | L | 30 | L27C | L30 | L30 | 32 | 563 | CDR1 |
| 31 | H | 31 | L27D | L30A | L30A | 33 | 581 | CDR1 |
| 32 | S | 32 | L27E | L30B | L30B | 34 | 582 | CDR1 |
| 33 | N | 34 | L28 | L30C | L30C | 35 | 583 | CDR1 |
| 34 | G | 35 | L29 | L30D | L30D | 37 | 594 | CDR1 |
| 35 | N | 36 | L30 | L30E | L30E | 38 | 595 | CDR1 |
| 36 | T | 37 | L31 | L31 | L31 | 39 | 596 | CDR1 |
| 37 | Y | 38 | L32 | L32 | L32 | 40 | 597 | CDR1 |
| 38 | L | 39 | L33 | L33 | L33 | 41 | 598 | FR2 |
| 39 | Y | 40 | L34 | L34 | L34 | 42 | 599 | FR2 |
| 40 | W | 41 | L35 | L35 | L35 | 43 | 601 | FR2; Trp; C strand / core |
| 41 | F | 42 | L36 | L36 | L36 | 44 | 602 | FR2 |
| 42 | L | 43 | L37 | L37 | L37 | 45 | 603 | FR2 |
| 43 | Q | 44 | L38 | L38 | L38 | 46 | 604 | FR2 |
| 44 | R | 45 | L39 | L39 | L39 | 47 | 605 | FR2 |
| 45 | P | 46 | L40 | L40 | L40 | 48 | 606 | FR2 |
| 46 | G | 47 | L41 | L41 | L41 | 49 | 607 | FR2 |
| 47 | Q | 48 | L42 | L42 | L42 | 50 | 608 | FR2 |
| 48 | S | 49 | L43 | L43 | L43 | 51 | 609 | FR2 |
| 49 | P | 50 | L44 | L44 | L44 | 52 | 610 | FR2 |
| 50 | Q | 51 | L45 | L45 | L45 | 53 | 611 | FR2 |
| 51 | L | 52 | L46 | L46 | L46 | 54 | 612 | FR2 |
| 52 | L | 53 | L47 | L47 | L47 | 55 | 613 | FR2 |
| 53 | I | 54 | L48 | L48 | L48 | 56 | 614 | FR2 |
| 54 | Y | 55 | L49 | L49 | L49 | 57 | 615 | FR2 |
| 55 | R | 56 | L50 | L50 | L50 | 58 | 651 | CDR2 |
| 56 | M | 57 | L51 | L51 | L51 | 67 | 694 | CDR2 |
| 57 | S | 65 | L52 | L52 | L52 | 68 | 695 | CDR2 |
| 58 | N | 66 | L53 | L53 | L53 | 69 | 696 | FR3 |
| 59 | L | 67 | L54 | L54 | L54 | 70 | 697 | FR3 |
| 60 | A | 68 | L55 | L55 | L55 | 71 | 698 | FR3 |
| 61 | S | 69 | L56 | L56 | L56 | 72 | 699 | FR3 |
| 62 | G | 70 | L57 | L57 | L57 | 73 | 701 | FR3 |
| 63 | V | 71 | L58 | L58 | L58 | 74 | 702 | FR3 |
| 64 | P | 72 | L59 | L59 | L59 | 75 | 703 | FR3 |
| 65 | D | 74 | L60 | L60 | L60 | 76 | 704 | FR3 |
| 66 | R | 75 | L61 | L61 | L61 | 77 | 705 | FR3 |
| 67 | F | 76 | L62 | L62 | L62 | 78 | 706 | FR3 |
| 68 | S | 77 | L63 | L63 | L63 | 79 | 707 | FR3 |
| 69 | G | 78 | L64 | L64 | L64 | 80 | 708 | FR3 |
| 70 | S | 79 | L65 | L65 | L65 | 81 | 709 | FR3 |
| 71 | G | 80 | L66 | L66 | L66 | 82 | 710 | FR3 |
| 72 | S | 83 | L67 | L67 | L67 | 83 | 711 | FR3 |
| 73 | G | 84 | L68 | L68 | L68 | 84 | 712 | FR3 |
| 74 | T | 85 | L69 | L69 | L69 | 87 | 715 | FR3 |
| 75 | A | 86 | L70 | L70 | L70 | 88 | 716 | FR3 |
| 76 | F | 87 | L71 | L71 | L71 | 89 | 717 | FR3 |
| 77 | T | 88 | L72 | L72 | L72 | 90 | 718 | FR3 |
| 78 | L | 89 | L73 | L73 | L73 | 91 | 719 | FR3; Hydrophobic; E strand / core |
| 79 | R | 90 | L74 | L74 | L74 | 92 | 720 | FR3 |
| 80 | I | 91 | L75 | L75 | L75 | 93 | 721 | FR3 |
| 81 | S | 92 | L76 | L76 | L76 | 94 | 722 | FR3 |
| 82 | R | 93 | L77 | L77 | L77 | 95 | 723 | FR3 |
| 83 | V | 94 | L78 | L78 | L78 | 96 | 724 | FR3 |
| 84 | E | 95 | L79 | L79 | L79 | 97 | 725 | FR3 |
| 85 | A | 96 | L80 | L80 | L80 | 98 | 726 | FR3 |
| 86 | E | 97 | L81 | L81 | L81 | 99 | 727 | FR3 |
| 87 | D | 98 | L82 | L82 | L82 | 100 | 728 | FR3 |
| 88 | V | 99 | L83 | L83 | L83 | 101 | 729 | FR3 |
| 89 | G | 100 | L84 | L84 | L84 | 102 | 730 | FR3 |
| 90 | V | 101 | L85 | L85 | L85 | 103 | 731 | FR3 |
| 91 | Y | 102 | L86 | L86 | L86 | 104 | 732 | FR3 |
| 92 | Y | 103 | L87 | L87 | L87 | 105 | 733 | FR3 |
| 93 | C | 104 | L88 | L88 | L88 | 106 | 734 | FR3; Cys; F strand / disulfide |
| 94 | L | 105 | L89 | L89 | L89 | 107 | 751 | CDR3 |
| 95 | Q | 106 | L90 | L90 | L90 | 108 | 752 | CDR3 |
| 96 | H | 107 | L91 | L91 | L91 | 109 | 753 | CDR3 |
| 97 | L | 108 | L92 | L92 | L92 | 110 | 754 | CDR3 |
| 98 | E | 109 | L93 | L93 | L93 | 111 | 755 | CDR3 |
| 99 | Y | 114 | L94 | L94 | L94 | 135 | 796 | CDR3 |
| 100 | P | 115 | L95 | L95 | L95 | 136 | 797 | CDR3 |
| 101 | F | 116 | L96 | L96 | L96 | 137 | 798 | CDR3 |
| 102 | T | 117 | L97 | L97 | L97 | 138 | 799 | CDR3 |
| 103 | F | 118 | L98 | L98 | L98 | 139 | 801 | FR4; Phe/Trp; G strand / J motif |
| 104 | G | 119 | L99 | L99 | L99 | 140 | 802 | FR4; Gly; J motif |
| 105 | A | 120 | L100 | L100 | L100 | 141 | 803 | FR4 |
| 106 | G | 121 | L101 | L101 | L101 | 142 | 804 | FR4; Gly; J motif |
| 107 | T | 122 | L102 | L102 | L102 | 143 | 805 | FR4 |
| 108 | K | 123 | L103 | L103 | L103 | 144 | 806 | FR4 |
| 109 | L | 124 | L104 | L104 | L104 | 145 | 807 | FR4 |
| 110 | E | 125 | L105 | L105 | L105 | 146 | 808 | FR4 |
| 111 | L | 126 | L106 | L106 | L106 | 147 | 809 | FR4 |
| 112 | K | 127 | L107 | L107 | L107 | 148 | 810 | FR4 |

</details>

<details>
<summary>Avelumab Vλ: 110 residues; IMGT CDR lengths 9.3.10</summary>


[PDB 5GRJ](https://www.rcsb.org/structure/5GRJ), author chain **L**, entity **2**. Sequence position counts from the beginning of the deposited sequence; it is not a PDB residue label.


| Seq. | AA | IMGT | Kabat | Chothia | Martin | AHo | WolfGuy | Region / landmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Q | 1 | L1 | L1 | L1 | 1 | 501 | FR1 |
| 2 | S | 2 | L2 | L2 | L2 | 2 | 502 | FR1 |
| 3 | A | 3 | L3 | L3 | L3 | 3 | 503 | FR1 |
| 4 | L | 4 | L4 | L4 | L4 | 4 | 504 | FR1 |
| 5 | T | 5 | L5 | L5 | L5 | 5 | 505 | FR1 |
| 6 | Q | 6 | L6 | L6 | L6 | 6 | 506 | FR1 |
| 7 | P | 7 | L7 | L7 | L7 | 7 | 507 | FR1 |
| 8 | A | 8 | L8 | L8 | L8 | 9 | 509 | FR1 |
| 9 | S | 9 | L9 | L9 | L9 | 10 | 510 | FR1 |
| 10 | V | 11 | L11 | L11 | L11 | 11 | 511 | FR1 |
| 11 | S | 12 | L12 | L12 | L12 | 12 | 512 | FR1 |
| 12 | G | 13 | L13 | L13 | L13 | 13 | 513 | FR1 |
| 13 | S | 14 | L14 | L14 | L14 | 14 | 514 | FR1 |
| 14 | P | 15 | L15 | L15 | L15 | 15 | 515 | FR1 |
| 15 | G | 16 | L16 | L16 | L16 | 16 | 516 | FR1 |
| 16 | Q | 17 | L17 | L17 | L17 | 17 | 517 | FR1 |
| 17 | S | 18 | L18 | L18 | L18 | 18 | 518 | FR1 |
| 18 | I | 19 | L19 | L19 | L19 | 19 | 519 | FR1 |
| 19 | T | 20 | L20 | L20 | L20 | 20 | 520 | FR1 |
| 20 | I | 21 | L21 | L21 | L21 | 21 | 521 | FR1 |
| 21 | S | 22 | L22 | L22 | L22 | 22 | 522 | FR1 |
| 22 | C | 23 | L23 | L23 | L23 | 23 | 523 | FR1; Cys; B strand / disulfide |
| 23 | T | 24 | L24 | L24 | L24 | 24 | 551 | FR1 |
| 24 | G | 25 | L25 | L25 | L25 | 25 | 552 | FR1 |
| 25 | T | 26 | L26 | L26 | L26 | 26 | 554 | FR1 |
| 26 | S | 27 | L27 | L27 | L27 | 27 | 555 | CDR1 |
| 27 | S | 28 | L27A | L28 | L28 | 29 | 556 | CDR1 |
| 28 | D | 29 | L27B | L29 | L29 | 30 | 557 | CDR1 |
| 29 | V | 30 | L27C | L30 | L30 | 31 | 561 | CDR1 |
| 30 | G | 31 | L28 | L30A | L30A | 32 | 562 | CDR1 |
| 31 | G | 35 | L29 | L30B | L30B | 33 | 571 | CDR1 |
| 32 | Y | 36 | L30 | L30C | L30C | 38 | 572 | CDR1 |
| 33 | N | 37 | L31 | L31 | L31 | 39 | 596 | CDR1 |
| 34 | Y | 38 | L32 | L32 | L32 | 40 | 597 | CDR1 |
| 35 | V | 39 | L33 | L33 | L33 | 41 | 598 | FR2 |
| 36 | S | 40 | L34 | L34 | L34 | 42 | 599 | FR2 |
| 37 | W | 41 | L35 | L35 | L35 | 43 | 601 | FR2; Trp; C strand / core |
| 38 | Y | 42 | L36 | L36 | L36 | 44 | 602 | FR2 |
| 39 | Q | 43 | L37 | L37 | L37 | 45 | 603 | FR2 |
| 40 | Q | 44 | L38 | L38 | L38 | 46 | 604 | FR2 |
| 41 | H | 45 | L39 | L39 | L39 | 47 | 605 | FR2 |
| 42 | P | 46 | L40 | L40 | L40 | 48 | 606 | FR2 |
| 43 | G | 47 | L41 | L41 | L41 | 49 | 607 | FR2 |
| 44 | K | 48 | L42 | L42 | L42 | 50 | 608 | FR2 |
| 45 | A | 49 | L43 | L43 | L43 | 51 | 609 | FR2 |
| 46 | P | 50 | L44 | L44 | L44 | 52 | 610 | FR2 |
| 47 | K | 51 | L45 | L45 | L45 | 53 | 611 | FR2 |
| 48 | L | 52 | L46 | L46 | L46 | 54 | 612 | FR2 |
| 49 | M | 53 | L47 | L47 | L47 | 55 | 613 | FR2 |
| 50 | I | 54 | L48 | L48 | L48 | 56 | 614 | FR2 |
| 51 | Y | 55 | L49 | L49 | L49 | 57 | 615 | FR2 |
| 52 | D | 56 | L50 | L50 | L50 | 58 | 651 | CDR2 |
| 53 | V | 57 | L51 | L51 | L51 | 67 | 694 | CDR2 |
| 54 | S | 65 | L52 | L52 | L52 | 68 | 695 | CDR2 |
| 55 | N | 66 | L53 | L53 | L53 | 69 | 696 | FR3 |
| 56 | R | 67 | L54 | L54 | L54 | 70 | 697 | FR3 |
| 57 | P | 68 | L55 | L55 | L55 | 71 | 698 | FR3 |
| 58 | S | 69 | L56 | L56 | L56 | 72 | 699 | FR3 |
| 59 | G | 70 | L57 | L57 | L57 | 73 | 701 | FR3 |
| 60 | V | 71 | L58 | L58 | L58 | 74 | 702 | FR3 |
| 61 | S | 72 | L59 | L59 | L59 | 75 | 703 | FR3 |
| 62 | N | 74 | L60 | L60 | L60 | 76 | 704 | FR3 |
| 63 | R | 75 | L61 | L61 | L61 | 77 | 705 | FR3 |
| 64 | F | 76 | L62 | L62 | L62 | 78 | 706 | FR3 |
| 65 | S | 77 | L63 | L63 | L63 | 79 | 707 | FR3 |
| 66 | G | 78 | L64 | L64 | L64 | 80 | 708 | FR3 |
| 67 | S | 79 | L65 | L65 | L65 | 81 | 709 | FR3 |
| 68 | K | 80 | L66 | L66 | L66 | 82 | 710 | FR3 |
| 69 | S | 83 | L67 | L67 | L67 | 83 | 711 | FR3 |
| 70 | G | 84 | L68 | L68 | L68 | 84 | 712 | FR3 |
| 71 | N | 85 | L69 | L69 | L69 | 87 | 715 | FR3 |
| 72 | T | 86 | L70 | L70 | L70 | 88 | 716 | FR3 |
| 73 | A | 87 | L71 | L71 | L71 | 89 | 717 | FR3 |
| 74 | S | 88 | L72 | L72 | L72 | 90 | 718 | FR3 |
| 75 | L | 89 | L73 | L73 | L73 | 91 | 719 | FR3; Hydrophobic; E strand / core |
| 76 | T | 90 | L74 | L74 | L74 | 92 | 720 | FR3 |
| 77 | I | 91 | L75 | L75 | L75 | 93 | 721 | FR3 |
| 78 | S | 92 | L76 | L76 | L76 | 94 | 722 | FR3 |
| 79 | G | 93 | L77 | L77 | L77 | 95 | 723 | FR3 |
| 80 | L | 94 | L78 | L78 | L78 | 96 | 724 | FR3 |
| 81 | Q | 95 | L79 | L79 | L79 | 97 | 725 | FR3 |
| 82 | A | 96 | L80 | L80 | L80 | 98 | 726 | FR3 |
| 83 | E | 97 | L81 | L81 | L81 | 99 | 727 | FR3 |
| 84 | D | 98 | L82 | L82 | L82 | 100 | 728 | FR3 |
| 85 | E | 99 | L83 | L83 | L83 | 101 | 729 | FR3 |
| 86 | A | 100 | L84 | L84 | L84 | 102 | 730 | FR3 |
| 87 | D | 101 | L85 | L85 | L85 | 103 | 731 | FR3 |
| 88 | Y | 102 | L86 | L86 | L86 | 104 | 732 | FR3 |
| 89 | Y | 103 | L87 | L87 | L87 | 105 | 733 | FR3 |
| 90 | C | 104 | L88 | L88 | L88 | 106 | 734 | FR3; Cys; F strand / disulfide |
| 91 | S | 105 | L89 | L89 | L89 | 107 | 751 | CDR3 |
| 92 | S | 106 | L90 | L90 | L90 | 108 | 752 | CDR3 |
| 93 | Y | 107 | L91 | L91 | L91 | 109 | 753 | CDR3 |
| 94 | T | 108 | L92 | L92 | L92 | 110 | 754 | CDR3 |
| 95 | S | 109 | L93 | L93 | L93 | 111 | 755 | CDR3 |
| 96 | S | 113 | L94 | L94 | L94 | 112 | 795 | CDR3 |
| 97 | S | 114 | L95 | L95 | L95 | 135 | 796 | CDR3 |
| 98 | T | 115 | L95A | L95A | L95A | 136 | 797 | CDR3 |
| 99 | R | 116 | L96 | L96 | L96 | 137 | 798 | CDR3 |
| 100 | V | 117 | L97 | L97 | L97 | 138 | 799 | CDR3 |
| 101 | F | 118 | L98 | L98 | L98 | 139 | 801 | FR4; Phe/Trp; G strand / J motif |
| 102 | G | 119 | L99 | L99 | L99 | 140 | 802 | FR4; Gly; J motif |
| 103 | T | 120 | L100 | L100 | L100 | 141 | 803 | FR4 |
| 104 | G | 121 | L101 | L101 | L101 | 142 | 804 | FR4; Gly; J motif |
| 105 | T | 122 | L102 | L102 | L102 | 143 | 805 | FR4 |
| 106 | K | 123 | L103 | L103 | L103 | 144 | 806 | FR4 |
| 107 | V | 124 | L104 | L104 | L104 | 145 | 807 | FR4 |
| 108 | T | 125 | L105 | L105 | L105 | 146 | 808 | FR4 |
| 109 | V | 126 | L106 | L106 | L106 | 147 | 809 | FR4 |
| 110 | L | 127 | L107 | L107 | L107 | 148 | 810 | FR4 |

</details>

<!-- END GENERATED CROSSWALK -->

**WolfGuy's allocated blocks** help interpret any example: VH frameworks begin at **101/201/301/401**, with CDR1/2/3 in **151–199 / 251–299 / 351–399**; VL frameworks begin at **501/601/701/801**, with CDRs in **551–599 / 651–699 / 751–799**. Unoccupied integers are reserved space, not missing residues. L1 placement can depend on sequence/canonical class as well as length [@bujotzek2015; @bujotzek2015mofvab].

**Gelfand–Kister structural words** use a different kind of address: the index restarts within each word, word lengths vary, and the original method does not place internal gaps within words. The [original definitions and residue table](https://pmc.ncbi.nlm.nih.gov/articles/PMC40535/) provide the structural reference [@gelfand1995].

| Word(s) | Substructure |
| --- | --- |
| OA | First three N-terminal residues, preceding strand A |
| A, A′, B, C, C′, C″, D, E, F, G | The named β-strands |
| AA′, A′B, CC′, C′C″, C″D, DE, EF, FG | Connections between the named strands |
| BC, CB | Two portions of the B-to-C connection |

Their sequence order is **OA → A → AA′ → A′ → A′B → B → BC → CB → C → CC′ → C′ → C′C″ → C″ → C″D → D → DE → E → EF → F → FG → G**. Shared landmarks give the following **inferred correspondence** to modern IMGT: **B6/C3/E4/F5/G2/G3/G5 ↔ 23/41/89/104/118/119/121** (first Cys, Trp, hydrophobic core, second Cys, J aromatic, and two glycines). This inference links structural anchors; it does not extend the 1995 paper into a sequence-independent loop converter [@gelfand1995; @lefranc2003].

### Insertions, gaps, and conversion limits

**There is no sequence-independent, one-to-one lookup for every possible loop length.** A published alignment is a reference scaffold. The insertion code, chain type, loop length, historical scheme version, and assignment program can change the correspondence. In particular:

- Kabat places heavy H1 additions at H35, whereas Chothia places them at H31; light L1 insertions also differ. Martin additionally corrects framework insertion/deletion placement [@abhinandan2008].
- IMGT fills shorter CDRs with defined internal gaps. For a CDR3 longer than 13 residues, additional labels occur between 111 and 112: in sequence order, a 15-residue example includes **111, 111.1, 112.1, 112**. Decimal suffixes are labels, not fractional sequence indices. ANARCI may serialize them with letter insertion codes [@lefranc2003; @dunbar2016].
- AHo's unoccupied numbers are alignment gaps. A numbered gap is different from a residue that exists in the sequence but lacks coordinates in a structure [@honegger2001].

For an actual molecule, number the **same complete domain sequence** under each requested scheme, join the results by original sequence position, and retain insertion codes. Verify the conserved landmarks and inspect unusual loop/framework insertions before transferring mutations or CDR selections. For primary length-dependent reference alignments, see [VH](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VH.html), [Vκ](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VK.html), and [Vλ](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VL.html). These distinguish historical Kabat/Chothia versions instead of silently merging them.

## Constant regions: EU versus IMGT

An Fc label such as **EU N297** belongs to an IgG reference sequence. An IMGT constant-domain label must also name its domain: **CH2 N84.4**, for example. Neither belongs in the variable-domain crosswalk. The same IMGT number can recur in CH1, CH2, and CH3 because each domain has its own coordinates [@edelman1969; @lefranc2005].

The following is **human IGHG1*01 (J00228) aligned to the EU index**, not the literal Eu protein sequence. The full [IMGT author correspondence table](https://www.imgt.org/IMGTScientificChart/Numbering/Hu_IGHGnber.html) also distinguishes the older Kabat constant-region count. A [local, searchable CSV](../assets/antibody-numbering-igg1-eu-imgt.csv) maps **all 330 residues, EU 118–447**, to domain, IMGT label, amino acid, and substructure; this reference alignment must not be transferred blindly to other subclasses.

| Constant-domain landmark | IMGT position within domain | CH1 EU | CH2 EU | CH3 EU |
| --- | --- | --- | --- | --- |
| First conserved Cys, strand B | 23 | 144 | 261 | 367 |
| Conserved Trp, strand C | 41 | 158 | 277 | 381 |
| Hydrophobic core, strand E | 89 | 186 | 306 | 410 |
| Second conserved Cys, strand F | 104 | 200 | 321 | 425 |
| Fc N-glycosylation site, DE turn | 84.4 | — | **N297** | — |

In this reference's exon/domain partition, CH1 is EU **118–215**, the hinge exon **216–230**, CH2 **231–340**, CH3 domain **341–445**, and secretory tail **446–447**. The structural “lower hinge” can include the N-terminal CH2 segment, so exon boundaries and structural hinge definitions should not be conflated.

## Reporting a numbered sequence or structure

Record the domain/chain identity, numbering scheme and implementation/version, CDR definition, insertion codes, and the correspondence to original sequence/PDB positions. For a composite construct such as an scFv, identify each VH/VL domain separately. This makes a statement such as “mutate H71” reproducible and avoids conflating variable-domain, full-chain, and constant-domain indices.
