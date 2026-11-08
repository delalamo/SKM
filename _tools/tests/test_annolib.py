from __future__ import annotations

import pytest

from annolib import AnnotationError, Note

REGISTRY = {"C-0001": {"title": "Loops are short"}, "C-0002": {"title": "Old"}, "C-0003": {"title": "New", }}
REGISTRY["C-0002"]["merged_into"] = "C-0003"

BASE = """---
citekey: x2020
block_prefix: xxx20
---

First paragraph says loops are short and loops are many. ^xxx20-p001

Second paragraph cites [[#^xxx20-ref-1|1]]. ^xxx20-p002

$$
a = b
$$

^xxx20-p003

1. A reference. ^xxx20-ref-1
2. Another one. ^xxx20-ref-2
"""


def note() -> Note:
  return Note(BASE, REGISTRY)


def test_sub_requires_exactly_one_match():
  n = note()
  with pytest.raises(AnnotationError):
    n.sub("xxx20-p001", "loops", "rings")
  with pytest.raises(AnnotationError):
    n.sub("xxx20-p001", "absent", "x")
  n.sub("xxx20-p001", "says", "shows")
  assert "First paragraph shows" in n.render()


def test_name_renames_id_and_same_note_links():
  n = note()
  n.name("A reference.", "xxx20-ref-first")
  text = n.render()
  assert "^xxx20-ref-first" in text and "[[#^xxx20-ref-first|1]]" in text
  with pytest.raises(AnnotationError):
    n.name("Second paragraph", "xxx20-p001")


def test_claim_span_must_be_unique_and_link_free():
  n = note()
  with pytest.raises(AnnotationError):
    n.claim("xxx20-p001", "C-0001", "loops", "supports")
  with pytest.raises(AnnotationError):
    n.claim("xxx20-p002", "C-0001", "cites [[#^xxx20-ref-1|1]]", "supports")
  with pytest.raises(AnnotationError):
    n.claim("xxx20-p001", "C-0001", "loops are short", "endorses")


def test_render_orders_callouts_by_highlight_and_follows_merges():
  n = note()
  n.claim("xxx20-p001", "C-0002", "loops are many", "qualifies")
  n.context("xxx20-p001", "Scope", "Only short loops.", "First paragraph")
  n.claim("xxx20-p001", "C-0001", "loops are short", "supports", note="Measured directly.")
  text = n.render()
  context = text.index("[!context")
  supports = text.index("[[Loops are short]]")
  merged = text.index("[[New]]")
  assert context < supports < merged
  assert '<mark class="pm-context">First paragraph</mark>' in text
  assert "> - [[Loops are short]]\n>\n> Measured directly." in text


def test_eq_only_on_display_equations():
  n = note()
  with pytest.raises(AnnotationError):
    n.eq("xxx20-p001", "Symbols", "x")
  n.eq("xxx20-p003", "Symbols", "$a$ is a.")
  text = n.render()
  assert text.index("[!eq|margin llm] Symbols") < text.index("$$\na = b")


def test_list_spacing_is_preserved():
  text = note().render()
  assert "1. A reference. ^xxx20-ref-1\n2. Another one." in text
