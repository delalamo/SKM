---
title: Inverse folding
aliases:
  - Inverse folding
created: "2026-04-10T14:02:57"
modified: "2026-04-20T10:13:23"
---

**Inverse folding** describes the problem of designing a sequence for a structure. Typically these are limited to the twenty canonical amino acids.

## Methods

_See [[Hybrid sequence-structure models]] for a list of methods that incorporate [[Protein language models|PLMs]]_

- **[[ProteinMPNN]]** and its derivatives
- **[[ESM-IF]]**
- **GearNet**
- **Frame2seq**
- **[[Geometric Vector Perceptrons|GVP-GNN]]**

## Notes

#### Training

- **Training inverse folding models with backbone dihedral angles as features usually improved sequence recovery** [@jamasb2024].
 ![[Pasted-image-20240117115655.png]]
 _Figure from [@jamasb2024]_

#### Execution

- **Forward-folding is a stronger predictor of inverse folding success than sequence recovery** ([@yang2023b], citing Watson et al. [@watson2023; @dauparas2022]).

#### Datasets

- **PDBench** is a dataset of 595 protein structures with diverse, evenly divided topologies for benchmarking of [[Inverse folding]] methods [@castorina2023].
 ![[Alpha-Beta-Barre.png]]
 _Figure 2 from Castorina et al. [@castorina2023]_
