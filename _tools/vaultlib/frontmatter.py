"""Read and write YAML frontmatter deterministically.

Values are loaded without timestamp or boolean-word magic beyond YAML 1.2
basics, so dates such as ``created: 2024-04-26T11:38:01`` survive a
round-trip as the same text. The emitter writes a small, stable YAML subset:
plain or double-quoted scalars, flow lists of short scalars, block lists and
nested mappings.
"""

from __future__ import annotations

import json
import re
from typing import Any

import yaml

FENCE = "---"


class _Loader(yaml.SafeLoader):
  """SafeLoader that keeps timestamps as strings."""


# Drop the implicit timestamp resolver so dates stay strings.
_Loader.yaml_implicit_resolvers = {
  key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
  for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def split(text: str) -> tuple[str | None, str]:
  """Return (frontmatter text or None, body). The body keeps its newlines."""
  if not text.startswith(FENCE + "\n"):
    return None, text
  end = text.find("\n" + FENCE + "\n", len(FENCE))
  if end == -1:
    if text.endswith("\n" + FENCE):
      return text[len(FENCE) + 1 : -len(FENCE) - 1], ""
    return None, text
  return text[len(FENCE) + 1 : end + 1], text[end + len(FENCE) + 2 :]


def parse(text: str) -> tuple[dict[str, Any] | None, str]:
  fm_text, body = split(text)
  if fm_text is None:
    return None, body
  data = yaml.load(fm_text, Loader=_Loader) if fm_text.strip() else {}
  if data is None:
    data = {}
  if not isinstance(data, dict):
    raise ValueError("frontmatter is not a mapping")
  return data, body


def body_offset(text: str) -> int:
  """Number of lines before the body starts (0 when there is no frontmatter)."""
  fm_text, _ = split(text)
  if fm_text is None:
    return 0
  return fm_text.count("\n") + 2


_PLAIN_RE = re.compile(r"^[A-Za-z0-9_(][A-Za-z0-9 _.,;()'’/+\-–—]*$")
_RESERVED = {"true", "false", "yes", "no", "on", "off", "null", "~", "y", "n"}
_NUMBER_RE = re.compile(r"^[-+]?(\d[\d_]*)?(\.\d+)?([eE][-+]?\d+)?$")


def _scalar(value: Any) -> str:
  if value is None:
    return "null"
  if isinstance(value, bool):
    return "true" if value else "false"
  if isinstance(value, (int, float)):
    return repr(value)
  text = str(value)
  if (
    text
    and _PLAIN_RE.match(text)
    and text.lower() not in _RESERVED
    and not _NUMBER_RE.match(text)
    and not text.endswith(" ")
    and ": " not in text
    and " #" not in text
  ):
    return text
  return json.dumps(text, ensure_ascii=False)


def _is_scalar(value: Any) -> bool:
  return value is None or isinstance(value, (str, int, float, bool))


def _emit(value: Any, indent: int, lines: list[str], key: str) -> None:
  pad = "  " * indent
  if _is_scalar(value):
    lines.append(f"{pad}{key}: {_scalar(value)}")
  elif isinstance(value, list):
    if not value:
      lines.append(f"{pad}{key}: []")
    elif all(_is_scalar(item) for item in value):
      flow = "[" + ", ".join(_scalar(item) for item in value) + "]"
      if len(pad) + len(key) + len(flow) + 2 <= 100:
        lines.append(f"{pad}{key}: {flow}")
      else:
        lines.append(f"{pad}{key}:")
        lines.extend(f"{pad}  - {_scalar(item)}" for item in value)
    else:
      lines.append(f"{pad}{key}:")
      for item in value:
        if isinstance(item, dict):
          first = True
          for sub_key, sub_value in item.items():
            sub_lines: list[str] = []
            _emit(sub_value, indent + 2, sub_lines, sub_key)
            head = sub_lines[0].lstrip()
            prefix = f"{pad}  - " if first else f"{pad}    "
            lines.append(prefix + head)
            lines.extend(sub_lines[1:])
            first = False
          if first:
            lines.append(f"{pad}  - {{}}")
        else:
          lines.append(f"{pad}  - {_scalar(item)}")
  elif isinstance(value, dict):
    if not value:
      lines.append(f"{pad}{key}: {{}}")
    else:
      lines.append(f"{pad}{key}:")
      for sub_key, sub_value in value.items():
        _emit(sub_value, indent + 1, lines, sub_key)
  else:
    raise TypeError(f"cannot emit {type(value).__name__} for key {key!r}")


# The pre-commit hook (.githooks/pre-commit) appends these at the end of the
# frontmatter, so the emitter keeps them last to agree with it.
TRAILING = ("created", "modified")


def dump(data: dict[str, Any], order: tuple[str, ...] = ()) -> str:
  """Emit frontmatter (without fences). Keys in ``order`` come first."""
  keys = [key for key in order if key in data and key not in TRAILING]
  keys += [key for key in data if key not in keys and key not in TRAILING]
  keys += [key for key in TRAILING if key in data]
  lines: list[str] = []
  for key in keys:
    _emit(data[key], 0, lines, key)
  return "\n".join(lines) + "\n"


def compose(data: dict[str, Any] | None, body: str, order: tuple[str, ...] = ()) -> str:
  if data is None:
    return body
  return f"{FENCE}\n{dump(data, order)}{FENCE}\n{body}"


# Key orders for each note type, following the spec's templates.
PAPER_ORDER = (
  "citekey", "title", "published_title", "aliases", "authors", "year", "online", "venue",
  "doi", "version_in_kb", "other_versions", "license", "fulltext", "block_prefix",
  "supplement", "source_pdf", "source_conversion", "data_availability", "funding_coi",
  "status_checks", "fidelity_accept", "annotation_provenance", "topics", "claims",
  "redirect_from", "cssclasses", "tags",
)
CLAIM_ORDER = (
  "id", "type", "status", "evidence_strength", "scope", "topics", "kb_supporting",
  "kb_qualifying", "kb_contradicting", "kb_pending", "independence", "provenance",
  "redirect_from", "publicationHistory", "tags",
)
TOPIC_ORDER = ("type", "aliases", "redirect_from", "tags")
CONCEPT_ORDER = (
  "type", "aliases", "introduced_by", "topics", "provenance", "redirect_from", "tags",
)
DATASET_ORDER = (
  "type", "aliases", "provider", "product", "vintage", "geography", "unit", "access_class",
  "access_route", "url", "terms", "identifiers", "tags",
)
