---
tags:
  - design/sequence-generation
  - model-design/architectures
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Raygun generates length-controlled variants of a template protein using a fixed-dimensional representation derived from [[ESM|ESM-2]] embeddings** [@devkota2026]. Target length controls insertions and deletions, while a noise parameter controls sequence variation.

#### Details

The encoder divides the representation into 50 contiguous blocks, summarized by two 50 × 1280 arrays of means and standard deviations. These describe blockwise distributions, rather than one whole-protein average. The decoder expands the sampled representation to the requested sequence length through repetition/broadcasting. Reduction and expansion accommodate lengths not divisible by 50; feature-refinement blocks combine transformer and convolution layers [@devkota2026].

#### Recycling and ranking

A single recycling step, using a generated sequence as the next template, improved quality and diversity in the reported evaluation. Candidates of different lengths are ranked using the [[Sequence perplexity|length-adjusted pseudo-log-likelihood]] already described in the scoring note [@devkota2024; @devkota2026].

#### Related approaches

[[Enzymes can be miniaturized with Monte Carlo sampling and embedding similarity of catalytic residues|Monte Carlo miniaturization]] instead searches through deletion proposals while preserving catalytic-site embedding similarity. Raygun directly generates a candidate at the requested length.
