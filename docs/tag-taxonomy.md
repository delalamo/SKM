# Tagging notes

Tag the question or finding, then add up to two substantive connections. Keep notes in `content/notes/`; use `content/tags/` for topic navigation. The Antibodies overview remains on its original tag page to preserve its content and section links.

## Rules

- Store one to three specific topic tags, without also storing their parent.
- Separate biology from prediction and design. Physical folding is not structure prediction; complex geometry is not affinity; in-vivo maturation is not laboratory optimization.
- Use links to named models, proteins, metrics, and mathematical concepts. A mention does not by itself justify a tag.
- Keep opposing findings together. Use evidence/generalization or evidence/design-validation when transfer or experimental success is the point.
- Fine-tuning updates model parameters, including at test time. Guidance operates through a fixed model, even when it backpropagates to inputs.
- Feature extraction concerns using embeddings or probes; representation geometry concerns the meaning of distances, clusters, and manifolds.
- Training/fine-tuning also covers reuse and merging of task-specific parameter updates. Inference/ensembling combines model outputs, not weights.
- Citation work belongs in `review: [citation-fix]` or `review: [citation-needed]`, not in tags. Keep the [citation queue](../content/review/citations.md) synchronized when adding or resolving these flags.
- A sparse mathematical reference or unfinished note can remain untagged until it has a useful topical connection. Do not create a miscellaneous tag.

## Vocabulary

### biophysics

| Tag                               | Scope                                                                                                                                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `biophysics/stability`            | What determines thermodynamic or thermal stability, and how stability couples to other properties. Keep melting temperature, folding free energy, and kinetic stability distinct in the notes. |
| `biophysics/folding`              | Physical folding and unfolding pathways, rates, cooperativity, and intermediates; not the computational task of predicting a structure.                                                        |
| `biophysics/dynamics`             | Conformational equilibria, flexibility, allostery, and their functional consequences.                                                                                                          |
| `biophysics/interactions`         | Physical determinants of binding, specificity, interfaces, oligomerization, and assembly.                                                                                                      |
| `biophysics/catalysis`            | Catalytic mechanisms, active-site organization, substrate turnover, and enzyme function.                                                                                                       |
| `biophysics/molecular-simulation` | Molecular dynamics, force fields, simulation setup, and enhanced sampling of physical trajectories.                                                                                            |
| `biophysics/ensemble-analysis`    | Inferring populations, kinetics, collective variables, and reduced descriptions from ensembles or trajectories.                                                                                |
| `biophysics/thermodynamics`       | Free energies, statistical ensembles, partition functions, and the mathematical foundations of equilibrium sampling.                                                                           |

### evolution

| Tag                          | Scope                                                                                                                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `evolution/selection`        | Natural selection, evolutionary constraints, adaptation, evolvability, and the natural distribution of sequence and fold space.                                              |
| `evolution/mutation-effects` | Biological effects of substitutions and indels, fitness landscapes, epistasis, and accessible evolutionary paths. Prediction algorithms go under prediction/variant-effects. |
| `evolution/ancestry`         | Ancestral reconstruction, consensus sequences, historical inference, and their uses in engineering.                                                                          |
| `evolution/homology`         | Homology detection, sequence and structural alignment, remote similarity, and conservation across related proteins.                                                          |

### antibodies

| Tag                       | Scope                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `antibodies/architecture` | CDR and framework organization, heavy/light-chain pairing, loop geometry, numbering, and antibody formats as structures.                                                    |
| `antibodies/repertoires`  | Repertoire diversity, germline usage, V(D)J recombination, chain pairing across populations, and sequencing-derived repertoire patterns.                                    |
| `antibodies/maturation`   | Somatic mutation and selection during in-vivo affinity maturation, including effects on stability, specificity, and expression. Laboratory optimization goes under design.  |
| `antibodies/recognition`  | Paratopes, epitopes, binding modes, cross-reactivity, and the molecular basis of antibody recognition.                                                                      |
| `antibodies/nanobodies`   | Findings specific to single-domain antibodies, especially their differences from conventional antibodies; do not add merely because a generic method was tested on one VHH. |

### prediction

| Tag                               | Scope                                                                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `prediction/structure`            | Predicting protein structures, contacts, sidechains, and structural refinement; includes relevant tool/reference notes.                         |
| `prediction/antibody-structure`   | Predicting isolated antibody and nanobody structures, CDR conformations, and interdomain orientations.                                          |
| `prediction/complexes`            | Predicting macromolecular complex geometry, including antibody-antigen complexes and oligomer stoichiometry; distinct from predicting affinity. |
| `prediction/ligand-docking`       | Predicting small-molecule binding pockets and poses, including co-folding; distinct from affinity prediction.                                   |
| `prediction/ensembles`            | Predicting multiple conformations, populations, or conformational landscapes with learned models.                                               |
| `prediction/stability-expression` | Predicting stability, folding cooperativity, expression, solubility, and related physical developability properties.                            |
| `prediction/binding`              | Predicting affinity, binding versus nonbinding, specificity, and ligand-binding residues; does not imply a predicted complex geometry.          |
| `prediction/function`             | Predicting functional annotations, catalytic activity, and enzyme specificity.                                                                  |
| `prediction/variant-effects`      | Predicting mutation-induced effects on fitness or pathogenicity. Add a property-specific tag only when that property is a substantive focus.    |
| `prediction/confidence`           | What model confidence scores and uncertainty estimates mean, how they are calibrated, and what they fail to predict.                            |

### design

| Tag                          | Scope                                                                                                                                                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `design/sequence-generation` | Generating and optimizing sequences with sequence models, evolutionary profiles, or hallucination, including general sequence-search strategies. Fixed-structure sequence design goes under design/inverse-folding. |
| `design/inverse-folding`     | Designing or scoring amino-acid sequences conditioned on a structure or structural ensemble; includes inverse-folding training and applications to property prediction.                                             |
| `design/backbones`           | Generating backbones, folds, and motif scaffolds; includes designability and structural-diversity limitations.                                                                                                      |
| `design/antibodies`          | Computational antibody discovery, CDR design, and in-vitro or in-silico affinity optimization.                                                                                                                      |
| `design/binders`             | Designing non-antibody protein binders and cross-format binder workflows; antibody-only work goes under design/antibodies.                                                                                          |
| `design/enzymes`             | Engineering catalytic activity, enzyme specificity, active sites, and functional enzyme designs.                                                                                                                    |
| `design/directed-evolution`  | Iterative experimental optimization, library design, mutagenesis, selection, and model-guided experimental search.                                                                                                  |
| `design/developability`      | Expression, solubility, nonspecific binding, self-association, immunogenicity, humanization, and other constraints on making usable protein products.                                                               |
| `design/modular-proteins`    | Domain insertion, fusion, oligomerization modules, and engineering proteins as structural or functional tools.                                                                                                      |

### evidence

| Tag                          | Scope                                                                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `evidence/datasets`          | Dataset resources, composition, clustering, taxonomic bias, negative examples, synthetic data, and coverage.                                                       |
| `evidence/generalization`    | Memorization, leakage, out-of-distribution performance, shortcuts, robustness, and when apparent progress does not transfer.                                       |
| `evidence/design-validation` | Whether computational design scores, refolding tests, or rankings predict useful experimental outcomes; includes appropriate prospective and baseline comparisons. |
| `evidence/measurements`      | Assay definitions, reproducibility, experimental artifacts, structural evidence, and interpretation of evaluation statistics.                                      |

### cell-biology

| Tag                                   | Scope                                                                                                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `cell-biology/immune-signaling`       | Immune cells, antigen presentation, cytokines, receptors, and signaling biology.                                                          |
| `cell-biology/therapeutic-mechanisms` | How therapeutics act: receptor modulation, multivalency, payload delivery, targeted degradation, and circulation or clearance mechanisms. |

### training

| Tag                                    | Scope                                                                                                                                                                             |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `training/pretraining-and-scaling`     | Pretraining objectives, masking, model/data/compute scaling, and foundation-model learning dynamics. Dataset composition is covered by evidence/datasets when central.            |
| `training/fine-tuning`                 | Updating or adapting pretrained parameters: fine-tuning, adapters, forgetting, transfer, and combining task-specific weights. Test-time parameter updates still belong here.      |
| `training/objectives-and-optimization` | Training losses, auxiliary objectives, regularization, optimization schedules, and gradient estimators. Optimizing inputs through frozen models belongs under inference/guidance. |

### inference

| Tag                             | Scope                                                                                                                                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inference/conditioning`        | How runtime inputs such as MSAs, homolog prompts, templates, ligands, and initial structures affect predictions. Active reward-driven changes to conditioning also belong under inference/guidance.                     |
| `inference/feature-extraction`  | Using learned embeddings, attention-derived features, pooling, or probes for downstream prediction and retrieval. A frozen base model may supply features to a separately trained head.                                 |
| `inference/sampling-and-search` | Exploring candidate sequences, structures, or designs through sampling, recycles, decoding order, search algorithms, and increased inference compute. Physical MD sampling stays under biophysics/molecular-simulation. |
| `inference/guidance`            | Steering a fixed model with rewards, constraints, gradients, activation edits, or importance reweighting. Backpropagation to an input is not model fine-tuning.                                                         |
| `inference/ensembling`          | Combining predictions, scores, prompts, or samples from multiple model runs. Weight merging is documented separately under training/fine-tuning.                                                                        |

### model-design

| Tag                              | Scope                                                                                                                                        |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `model-design/architectures`     | Network components and architecture choices, including attention, equivariance, graph networks, and computational efficiency.                |
| `model-design/multimodal`        | Combining sequence, structure, or other modalities; structural tokenization, feature fusion, and hybrid models.                              |
| `model-design/generative-models` | Diffusion, flow matching, VAEs, and energy-based generative formulations. Pair with the substantive design or prediction task when relevant. |

### model-analysis

| Tag                                      | Scope                                                                                                                                                                                                    |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model-analysis/representation-geometry` | How similarities, clusters, distances, and manifolds in model representations relate to sequence, structure, or function. Practical feature extraction is a separate inference topic.                    |
| `model-analysis/interpretability`        | What models internally encode and how they use it: attention analysis, layer-wise probing, sparse autoencoders, and mechanistic explanations. Generalization tests remain under evidence/generalization. |

## Legacy links

Former concept pages have moved into `content/notes/` with their prose, citations, section headings, and dates preserved. Their `tags/...` aliases retain old URLs. Internal concept links now point directly to the canonical note. Retired topic-listing URLs redirect to the nearest new topic; a formerly mixed group may now be spread across several topics.

The hierarchy replaces the old `learning` umbrella with `training`, `inference`, `model-design`, and `model-analysis`. There is no general statistical-methods tag; supporting methods are linked from the task they serve.
