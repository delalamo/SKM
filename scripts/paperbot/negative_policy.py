"""Shared policy for the frozen PubMed biological-negative corpus.

The bootstrapper and model validator import this module so corpus generation
and freshness checks cannot silently drift apart.  It intentionally has no
network or third-party dependencies.
"""

from __future__ import annotations

import re


NEGATIVE_DATASET = "pubmed-negatives-v1"
NEGATIVE_SEED = "skm-pubmed-negatives-v1"
NEGATIVE_START_YEAR = 2018
NEGATIVE_END_YEAR = 2025

# The first five strata are deliberately clear biological negatives.  The
# remaining strata are harder, near-domain negatives drawn from the broad
# biomedical themes that leaked through the original physics/math classifier.
# Each tuple is (quota, accepted MeSH major-topic descriptors).
NEGATIVE_GROUPS: dict[str, tuple[int, tuple[str, ...]]] = {
  "ecology": (107, ("Ecology",)),
  "plant_biology": (107, ("Plant Physiological Phenomena",)),
  "animal_behavior": (107, ("Behavior, Animal",)),
  "developmental_biology": (107, ("Embryonic Development",)),
  "environmental_microbiology": (107, ("Environmental Microbiology",)),
  "genomics_transcriptomics": (23, ("Genomics", "Transcriptome")),
  "biosensors": (23, ("Biosensing Techniques",)),
  "microfluidics": (22, ("Microfluidic Analytical Techniques",)),
  "biomaterials_drug_delivery": (
    22,
    ("Biocompatible Materials", "Drug Delivery Systems"),
  ),
  "clinical_genetics": (
    22,
    ("Genetic Diseases, Inborn", "Genetic Predisposition to Disease"),
  ),
  "signaling_proteomics": (22, ("Signal Transduction", "Proteomics")),
}
NEGATIVE_QUOTAS = {
  group: quota for group, (quota, _major_topics) in NEGATIVE_GROUPS.items()
}

# A complete manual review of the small hard-negative strata found four papers
# that are formally in the selected off-field MeSH groups but still study the
# target molecular-design problem closely enough to be poor negatives.  Keep
# this explicit and PMID-based: broadening the text filter would also remove
# useful adjacent examples that teach the classifier the actual boundary.
MANUALLY_EXCLUDED_PMIDS = frozenset(
  {
    "31071601",  # designed/self-assembling virus capsid biomaterials
    "34199271",  # engineered enzyme mutants used as biosensor probes
    "39352000",  # functional/dimerization characterization of a protein variant
    "40727582",  # engineered self-assembling peptide amphiphile hydrogel
  }
)

# These are narrow target-field concepts, not generic biological terms.  In
# particular, words such as "protein", "structure", and "machine learning"
# remain allowed: papers using them for an unrelated biological question are
# useful hard negatives.
TARGET_MESH_HEADINGS = (
  "Allosteric Regulation",
  "Antibodies",
  "Directed Molecular Evolution",
  "Protein Conformation",
  "Protein Engineering",
  "Protein Folding",
  "Protein Structure, Tertiary",
)

TARGET_TEXT_PHRASES = (
  "antibody engineering",
  "antibody design",
  "binder design",
  "de novo protein design",
  "directed evolution",
  "inverse folding",
  "protein design",
  "protein engineering",
  "protein language model",
  "protein structure prediction",
  "affinity maturation",
  "AlphaFold",
  "RoseTTAFold",
  "RFdiffusion",
  "ProteinMPNN",
)

_TERM_JOIN = r"[\s\-\u2010-\u2015]*"
TARGET_TEXT_RE = re.compile(
  rf"\b(?:"
  rf"antibod(?:y|ies){_TERM_JOIN}(?:engineering|design)|"
  rf"binder{_TERM_JOIN}design|"
  rf"de{_TERM_JOIN}novo{_TERM_JOIN}protein{_TERM_JOIN}design|"
  rf"directed{_TERM_JOIN}(?:molecular{_TERM_JOIN})?evolution|"
  rf"inverse{_TERM_JOIN}folding|"
  rf"protein{_TERM_JOIN}(?:design|engineering|language{_TERM_JOIN}models?|"
  rf"structure{_TERM_JOIN}prediction)|"
  rf"affinity{_TERM_JOIN}maturation|"
  rf"alphafold|rosettafold|rfdiffusion|proteinmpnn"
  rf")\b",
  re.IGNORECASE,
)


def is_target_topic(
  title: str,
  abstract: str,
  mesh_headings: tuple[str, ...] | list[str] = (),
) -> bool:
  """Return whether a PubMed record belongs to the positive target field."""

  target_mesh = {heading.casefold() for heading in TARGET_MESH_HEADINGS}
  if any(heading.casefold() in target_mesh for heading in mesh_headings):
    return True
  return TARGET_TEXT_RE.search(f"{title}\n{abstract}") is not None


__all__ = [
  "NEGATIVE_DATASET",
  "NEGATIVE_END_YEAR",
  "NEGATIVE_GROUPS",
  "NEGATIVE_QUOTAS",
  "NEGATIVE_SEED",
  "NEGATIVE_START_YEAR",
  "MANUALLY_EXCLUDED_PMIDS",
  "TARGET_MESH_HEADINGS",
  "TARGET_TEXT_PHRASES",
  "TARGET_TEXT_RE",
  "is_target_topic",
]
