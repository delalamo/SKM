---
title: Effective sample size
aliases:
  - ESS
created: "2026-07-22"
modified: "2026-07-22T09:05:16"
tags:
  - biophysics/thermodynamics
  - inference/guidance
---

#### Summary

**Effective sample size** (ESS) estimates how many equally weighted samples a weighted particle population effectively contains:

$$
\mathrm{ESS}=\frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}=\frac{1}{\sum_i \widetilde{w}_i^2},
$$

where $w_i$ are unnormalized weights and $\widetilde{w}_i=w_i/\sum_j w_j$ are normalized weights. For $k$ particles, $1\leq\mathrm{ESS}\leq k$: values near $1$ indicate that a few particles dominate, whereas $k$ indicates uniform weights. Low ESS therefore diagnoses weight degeneracy and can trigger adaptive resampling [@singhal2025]. This is used in [[Feynman-Kac steering]] to decide when to resample.
