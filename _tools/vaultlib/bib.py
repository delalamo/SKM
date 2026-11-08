"""Bibliography access, reusing paperbot's dependency-free BibTeX parser.

The parser module is loaded straight from its file so that the paperbot
package (and its configuration) is never imported by the vault tools.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .paths import REPO_ROOT

_PARSER_PATH = REPO_ROOT / "scripts" / "paperbot" / "bibliography.py"


@lru_cache(maxsize=1)
def _parser():
  spec = importlib.util.spec_from_file_location("_skm_bibliography", _PARSER_PATH)
  module = importlib.util.module_from_spec(spec)
  sys.modules[spec.name] = module
  spec.loader.exec_module(module)
  return module


@dataclass(frozen=True)
class Author:
  family: str
  given: str

  @property
  def initial(self) -> str:
    return self.given[:1].upper() if self.given else ""

  @property
  def key(self) -> str:
    """Normalised "surname, initial" used to compare authors across papers."""
    return f"{fold(self.family)}, {fold(self.initial)}"

  def display(self) -> str:
    return f"{self.given} {self.family}".strip()


@dataclass(frozen=True)
class Entry:
  key: str
  entry_type: str
  fields: dict

  @property
  def title(self) -> str:
    return clean(self.fields.get("title", ""))

  @property
  def year(self) -> str:
    return self.fields.get("year", "").strip()

  @property
  def doi(self) -> str:
    doi = self.fields.get("doi", "").strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)

  @property
  def venue(self) -> str:
    for name in ("journal", "booktitle", "publisher", "howpublished", "institution"):
      if self.fields.get(name):
        return clean(self.fields[name])
    return ""

  @property
  def authors(self) -> list[Author]:
    return parse_authors(self.fields.get("author", ""))

  def short_label(self) -> str:
    """``Surname (Year)`` as used in evidence headings and block-link labels."""
    authors = self.authors
    name = authors[0].family if authors else self.key
    return f"{name} ({self.year})" if self.year else name

  def aliases(self) -> list[str]:
    authors = self.authors
    if not authors or not self.year:
      return []
    first = authors[0].family
    out = [f"{first} {self.year}"]
    if len(authors) == 2:
      out.append(f"{first} and {authors[1].family} {self.year}")
    elif len(authors) > 2:
      out.append(f"{first} et al. {self.year}")
    return out


def clean(value: str) -> str:
  return re.sub(r"\s+", " ", value).strip()


def fold(value: str) -> str:
  """Lowercase ASCII fold for comparisons (Fernández → fernandez)."""
  value = unicodedata.normalize("NFKD", value)
  return "".join(ch for ch in value if not unicodedata.combining(ch)).lower().strip()


def parse_authors(value: str) -> list[Author]:
  authors = []
  for part in re.split(r"\s+and\s+", clean(value)):
    part = part.strip()
    if not part:
      continue
    if "," in part:
      family, given = part.split(",", 1)
    else:
      pieces = part.split()
      family, given = pieces[-1], " ".join(pieces[:-1])
    authors.append(Author(clean(family), clean(given)))
  return authors


def load(path: Path | str) -> dict[str, Entry]:
  entries = _parser().load_bibliography(Path(path))
  return {entry.key: Entry(entry.key, entry.entry_type, dict(entry.fields)) for entry in entries}


def surnames(entries: dict[str, Entry]) -> set[str]:
  """Every author surname in the bibliography (each hyphen/space part too)."""
  names: set[str] = set()
  for entry in entries.values():
    for author in entry.authors:
      family = author.family.strip("{} ")
      if len(family) < 2:
        continue
      names.add(family)
      for piece in re.split(r"[\s-]+", family):
        if len(piece) >= 3 and piece[:1].isupper():
          names.add(piece)
  return names
