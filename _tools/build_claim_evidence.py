#!/usr/bin/env python3
"""Derive every claim's evidence lists from the papers' margin callouts.

Margin claim callouts in paper notes are the single record of which paper
bears on which claim. From them this script writes, for each claim note:

- ``kb_supporting``, ``kb_qualifying`` and ``kb_contradicting``;
- ``independence``: how many independent groups (no shared authors or
  datasets) the evidence comes from;
- one ``### [[paper|label]]`` section per source under ``## Evidence``,
  with the highlighted passages embedded in a generated excerpts block.
  The two or three sentences of prose under each heading are written by a
  person or a model; a pending-evidence section for the same paper is moved
  into ``## Evidence`` once the paper's margin links the claim.

It also writes each paper's ``claims`` (exactly the claims its callouts link)
and ``topics`` (the topics of those claims).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rules.papers import callout_targets  # noqa: E402
from vaultlib import bib as biblib  # noqa: E402
from vaultlib import edit, markdown, paths  # noqa: E402
from vaultlib.vault import Vault, link_target  # noqa: E402

KB_KEYS = (("kb_supporting", "supports"), ("kb_qualifying", "qualifies"), ("kb_contradicting", "contradicts"))
EVIDENCE = "## Evidence"
PENDING = "## Evidence pending verification"
H2_RE = re.compile(r"^## ")
H3_RE = re.compile(r"^### ")


def split(lines: list[str], pattern: re.Pattern) -> tuple[list[str], list[tuple[str, list[str]]]]:
  pre: list[str] = []
  sections: list[tuple[str, list[str]]] = []
  fence = False
  for line in lines:
    if line.startswith("```"):
      fence = not fence
    if not fence and pattern.match(line):
      sections.append((line, []))
    elif sections:
      sections[-1][1].append(line)
    else:
      pre.append(line)
  return pre, sections


def join(pre: list[str], sections: list[tuple[str, list[str]]]) -> str:
  parts = ["\n".join(pre).strip("\n")]
  for heading, lines in sections:
    content = "\n".join(lines).strip("\n")
    parts.append(heading + ("\n\n" + content if content else ""))
  return "\n\n".join(part for part in parts if part)


def heading_target(heading: str) -> str | None:
  links = markdown.find_links(heading)
  return links[0].target if links else None


def strip_generated(lines: list[str], name: str) -> list[str]:
  out, skipping = [], False
  for line in lines:
    begin = markdown.GENERATED_BEGIN_RE.match(line)
    if begin and begin.group(1) == name:
      skipping = True
      continue
    if skipping and markdown.GENERATED_END_RE.match(line):
      skipping = False
      continue
    if not skipping:
      out.append(line)
  return out


def source_section(heading: str, lines: list[str], paper: str, block_ids: list[str]) -> tuple[str, list[str]]:
  name = f"excerpts {paper}"
  prose = "\n".join(strip_generated(lines, name)).strip("\n")
  embeds = "\n\n".join(f"![[{paper}#^{block_id}]]" for block_id in block_ids)
  generated = markdown.generated_block(name, embeds).rstrip("\n")
  content = (prose + "\n\n" if prose else "") + generated
  return heading, content.split("\n")


def independence(vault: Vault, papers: list[str]) -> str:
  if not papers:
    return "No verified evidence yet."
  parent = list(range(len(papers)))

  def find(i: int) -> int:
    while parent[i] != i:
      parent[i] = parent[parent[i]]
      i = parent[i]
    return i

  def authors(name: str) -> set[str]:
    entry = vault.bib.get(name)
    if entry is not None:
      return {author.key for author in entry.authors}
    note = vault.note(paths.PAPERS, name)
    found = set()
    for value in (note.fm_list("authors") if note else []):
      for author in biblib.parse_authors(str(value)):
        found.add(author.key)
    return found

  def datasets(name: str) -> set[str]:
    note = vault.note(paths.PAPERS, name)
    return set(note.fm_link_targets("datasets")) if note else set()

  shared_notes = []
  for i in range(len(papers)):
    for j in range(i + 1, len(papers)):
      common_authors = authors(papers[i]) & authors(papers[j])
      common_data = datasets(papers[i]) & datasets(papers[j])
      if common_authors or common_data:
        parent[find(i)] = find(j)
        what = []
        if common_authors:
          what.append("authors " + ", ".join(sorted(key.split(", ")[0].title() for key in common_authors)))
        if common_data:
          what.append("data " + ", ".join(sorted(common_data)))
        shared_notes.append(f"{papers[i]} and {papers[j]} share {' and '.join(what)}")
  groups = len({find(i) for i in range(len(papers))})
  text = f"{len(papers)} paper{'s' if len(papers) != 1 else ''} from {groups} independent group{'s' if groups != 1 else ''}"
  return text + ("; " + "; ".join(shared_notes) if shared_notes else "")


def paper_order(vault: Vault):
  def key(name: str):
    entry = vault.bib.get(name)
    return (entry.year if entry else "", name)

  return key


def run(vault_dir: Path, bib_path: Path, data_dir: Path) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  relations: dict[str, dict[str, list[str]]] = {}
  excerpts: dict[str, dict[str, list[str]]] = {}
  linked_any: dict[str, set[str]] = {}
  paper_claims: dict[str, list[str]] = {}
  for paper in vault.kind("paper"):
    for claim, relation, block in callout_targets(vault, paper):
      paper_claims.setdefault(paper.rel, [])
      if claim.name not in paper_claims[paper.rel]:
        paper_claims[paper.rel].append(claim.name)
      linked_any.setdefault(claim.rel, set()).add(paper.name)
      if relation in ("supports", "qualifies", "contradicts"):
        names = relations.setdefault(claim.rel, {}).setdefault(relation, [])
        if paper.name not in names:
          names.append(paper.name)
        ids = excerpts.setdefault(claim.rel, {}).setdefault(paper.name, [])
        if block.id and block.id not in ids:
          ids.append(block.id)
  order = paper_order(vault)
  changed = 0

  claim_topics = {note.name: note.fm_link_targets("topics") for note in vault.kind("claim")}
  for paper in vault.kind("paper"):
    fm = dict(paper.fm or {})
    names = paper_claims.get(paper.rel, [])
    topics = sorted({topic for name in names for topic in claim_topics.get(name, [])}, key=str.lower)
    fm["claims"] = [f"[[{name}]]" for name in names]
    fm["topics"] = [f"[[{topic}]]" for topic in topics]
    changed += edit.save(paper, fm, paper.body)

  for note in vault.kind("claim"):
    fm = dict(note.fm or {})
    rel = relations.get(note.rel, {})
    papers_in_order: list[str] = []
    for key, relation in KB_KEYS:
      names = sorted(rel.get(relation, []), key=order)
      fm[key] = [f"[[{name}]]" for name in names]
      papers_in_order += [name for name in names if name not in papers_in_order]
    fm["independence"] = independence(vault, papers_in_order)
    now_linked = linked_any.get(note.rel, set())
    pending = [item for item in note.fm_list("kb_pending") if not (isinstance(item, dict) and link_target(item.get("paper")) in now_linked)]
    if pending:
      fm["kb_pending"] = pending
    else:
      fm.pop("kb_pending", None)

    pre, sections = split(note.body.split("\n"), H2_RE)
    moved: dict[str, tuple[str, list[str]]] = {}
    for index, (heading, lines) in enumerate(sections):
      if heading.strip() == PENDING:
        intro, subs = split(lines, H3_RE)
        kept = []
        for sub_heading, sub_lines in subs:
          target = heading_target(sub_heading)
          if target in now_linked:
            moved[target] = (sub_heading, sub_lines)
          else:
            kept.append((sub_heading, sub_lines))
        sections[index] = (heading, join(intro, kept).split("\n")) if kept else (heading, ["__drop__"])
    sections = [(h, l) for h, l in sections if l != ["__drop__"]]

    if papers_in_order:
      evidence_index = next((i for i, (h, _) in enumerate(sections) if h.strip() == EVIDENCE), None)
      if evidence_index is None:
        pending_index = next((i for i, (h, _) in enumerate(sections) if h.strip() == PENDING), len(sections))
        sections.insert(pending_index, (EVIDENCE, []))
        evidence_index = pending_index
      intro, subs = split(sections[evidence_index][1], H3_RE)
      by_target = {heading_target(h): (h, l) for h, l in subs}
      new_subs = []
      for heading, lines in subs:
        target = heading_target(heading)
        if target in papers_in_order:
          new_subs.append(source_section(heading, lines, target, excerpts[note.rel].get(target, [])))
        else:
          new_subs.append((heading, lines))
      for name in papers_in_order:
        if name in by_target:
          continue
        entry = vault.bib.get(name)
        heading, lines = moved.get(name, (f"### [[{name}|{entry.short_label() if entry else name}]]", []))
        new_subs.append(source_section(heading, lines, name, excerpts[note.rel].get(name, [])))
      sections[evidence_index] = (EVIDENCE, join(intro, new_subs).split("\n"))

    body = "\n" + join(pre, sections) + "\n"
    changed += edit.save(note, fm, body)
  return changed


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  args = parser.parse_args(argv)
  print(f"build_claim_evidence: {run(args.vault, args.bib, args.data)} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
