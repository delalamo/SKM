---
title: Uncrowded hypervolume improvement
aliases:
  - UHVI
created: "2026-07-19"
modified: "2026-07-20T09:52:04"
---

#### Summary

**Uncrowded hypervolume improvement** (UHVI) extends hypervolume improvement to provide selection pressure for dominated solutions in multi-objective optimization. For a point that improves the Pareto front, UHVI equals its positive hypervolume improvement; for a dominated point, it assigns a negative value based on distance to the front instead of the flat value of zero returned by ordinary HVI [@maree2020].

This makes the objective informative on both sides of the Pareto frontier.
