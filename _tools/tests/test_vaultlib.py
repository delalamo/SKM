from __future__ import annotations

from vaultlib import frontmatter, markdown
from vaultlib.bib import parse_authors


def test_frontmatter_round_trip_keeps_dates_and_links():
  text = (
    "---\n"
    "created: 2024-04-26T11:38:01\n"
    'modified: "2026-04-21T07:28:09"\n'
    'topics: ["[[Widget loops]]"]\n'
    "year: 2020\n"
    "flag: false\n"
    "nested:\n  generated: 2026-11-08\n  human_verified: false\n"
    "---\nBody\n"
  )
  data, body = frontmatter.parse(text)
  assert data["created"] == "2024-04-26T11:38:01"
  assert data["topics"] == ["[[Widget loops]]"]
  assert body == "Body\n"
  emitted = frontmatter.compose(data, body)
  again, _ = frontmatter.parse(emitted)
  assert again == data
  assert frontmatter.compose(again, body) == emitted


def test_scalars_that_need_quotes_are_quoted():
  dumped = frontmatter.dump({"a": "yes", "b": "1.5", "c": "x: y", "d": "[[Link]]", "e": "plain words"})
  assert 'a: "yes"' in dumped and 'b: "1.5"' in dumped and 'c: "x: y"' in dumped
  assert 'd: "[[Link]]"' in dumped and "e: plain words" in dumped


def test_segment_ids_for_paragraphs_tables_and_equations():
  body = (
    "Text here. ^p-1\n\n"
    "| a | b |\n| --- | --- |\n| 1 | 2 |\n\n^t-1\n\n"
    "$$\nx = y\n$$\n\n^e-1\n\n"
    "> [!claim|margin llm supports] Supports\n> - [[A claim]]\n\n"
    "1. Ref one. ^r-1\n2. Ref two. ^r-2\n"
  )
  blocks = markdown.segment(body)
  kinds = [(b.kind, b.id) for b in blocks]
  assert kinds == [
    ("paragraph", "p-1"), ("table", "t-1"), ("math", "e-1"), ("callout", None),
    ("listitem", "r-1"), ("listitem", "r-2"),
  ]
  callout = blocks[3].callout
  assert callout.kind == "claim" and callout.metadata == ["margin", "llm", "supports"] and callout.title == "Supports"


def test_links_parse_alias_block_and_table_pipe():
  links = markdown.find_links("See ![[paper#^blk]] and [[Note|label]] and [[Other\\|x]] and [[#^ref-1|1]].")
  assert [(l.embed, l.target, l.block, l.alias) for l in links] == [
    (True, "paper", "blk", None), (False, "Note", None, "label"), (False, "Other", None, "x"), (False, "", "ref-1", "1"),
  ]


def test_parse_authors_handles_both_name_orders():
  authors = parse_authors("Fernández-Quintero, Monica L. and Jane Smith")
  assert [(a.family, a.initial) for a in authors] == [("Fernández-Quintero", "M"), ("Smith", "J")]
  assert authors[0].key == "fernandez-quintero, m"
