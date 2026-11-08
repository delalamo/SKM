"""Default locations of the vault, the bibliography and the tool data."""

from __future__ import annotations

from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_VAULT = REPO_ROOT / "content"
DEFAULT_BIB = REPO_ROOT / "bibliography.bib"
DEFAULT_DATA = TOOLS_DIR / "data"

# Folders of the annotated knowledge base (spec section 3, plus Concepts).
PAPERS = "Papers"
CLAIMS = "Claims"
TOPICS = "Topics"
CONCEPTS = "Concepts"
GLOSSARY = "Glossary"
DATASETS = "Datasets"
INDEXES = "Indexes"
TEMPLATES = "Templates"
ATTACHMENTS = "attachments"

KB_FOLDERS = (PAPERS, CLAIMS, TOPICS, CONCEPTS, GLOSSARY, DATASETS, INDEXES)

# The pre-migration zone. Nothing new may be added here; it is emptied and
# deleted at the end of the migration.
LEGACY_FOLDERS = ("notes", "tags", "review")
