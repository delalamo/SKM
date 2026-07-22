# Abstract and model-data notice

This directory contains derived scholarly-paper embeddings, model parameters, and
source metadata used by SKM's paper relevance automation. Abstract text in the
repository and generated GitHub issues remains subject to the rights and licences
declared by its original authors, repositories, and publishers; it is not relicensed
under the surrounding source-code licence.

In particular, both [NLM](https://www.nlm.nih.gov/databases/download.html) and
[Crossref](https://www.crossref.org/documentation/retrieve-metadata/) warn that
publisher-supplied abstract text may remain copyrighted even when its metadata
record is available through their services. The provenance manifest records the
source-reported licence without treating it as a relicensing grant.

The `pubmed-negatives-v1` corpus contains PubMed bibliographic metadata and
abstract text retrieved through NCBI services. The presence of a record in
PubMed does not place its abstract in the public domain; the same source-rights
warning above applies to this corpus.
[Semantic Scholar Academic Graph](https://www.semanticscholar.org/product/api)
identifiers and citation relationships are used only to audit graph distance
from the bibliography and do not change the rights in the underlying paper
metadata.

Model weights for [SPECTER2](https://github.com/allenai/SPECTER2) are downloaded
from their pinned upstream revisions and are never committed here.
