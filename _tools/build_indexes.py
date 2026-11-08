#!/usr/bin/env python3
"""Write the generated indexes and every topic page's claim list.

- ``Indexes/Claims index.md``: one row per claim (ID, claim, status,
  evidence strength, number of supporting papers, topics).
- ``Indexes/Ingestion queue.md``: works cited by two or more vault papers
  whose text is not in the vault (not a note, or only a stub), ranked by how
  many papers cite them, with the reference as printed.
- ``Indexes/Review queue.md``: what a person should review first.
- The ``claims`` generated block of each topic page.
- ``_tools/data/claim_ids.json``: current titles of live claim IDs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import edit, markdown, paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

STATUS_RANK = {"contested": 0, "supported": 1, "model-derived": 2, "tentative": 3, "proposed": 4}
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\]\)>,;]+", re.IGNORECASE)
ARROW_RE = re.compile(r"→\s*\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")


def cell(text: str) -> str:
  return text.replace("|", "\\|")


def link(name: str) -> str:
  return f"[[{name}]]"


def index_note(name: str, content: str) -> str:
  return markdown.generated_block(name, content)


def claims_index(vault: Vault) -> str:
  rows = ["| ID | Claim | Status | Strength | Supporting | Topics |", "| --- | --- | --- | --- | --- | --- |"]
  for note in sorted(vault.kind("claim"), key=lambda n: str((n.fm or {}).get("id", ""))):
    fm = note.fm or {}
    topics = ", ".join(link(t) for t in note.fm_link_targets("topics"))
    rows.append(
      f"| {fm.get('id', '')} | {link(note.name)} | {fm.get('status', '')} | {fm.get('evidence_strength', '')} "
      f"| {len(note.fm_list('kb_supporting'))} | {topics} |"
    )
  if len(rows) == 2:
    return "No claims yet.\n"
  return "\n".join(rows) + "\n"


def _normalise(text: str) -> str:
  return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def ingestion_queue(vault: Vault) -> str:
  groups: dict[str, dict] = {}
  for paper in sorted(vault.kind("paper"), key=lambda n: n.name):
    fm = paper.fm or {}
    if fm.get("fulltext") == "stub":
      continue
    prefix = fm.get("block_prefix", "")
    for block in paper.blocks:
      if block.kind != "listitem" or not (block.id or "").startswith(f"{prefix}-ref-"):
        continue
      text = markdown.BLOCK_ID_RE.sub("", " ".join(line.strip() for line in block.lines)).strip()
      text = re.sub(r"^\d+[.)]\s+", "", text)
      arrow = ARROW_RE.search(text)
      if arrow:
        target = vault.resolve(arrow.group(1), paper)
        if target is None or target.kind != "paper" or (target.fm or {}).get("fulltext") != "stub":
          continue  # already in the vault with its text
        key, label = f"note:{target.name}", link(target.name)
      else:
        doi = DOI_RE.search(text)
        key = f"doi:{doi.group(0).lower().rstrip('.')}" if doi else f"text:{_normalise(text)}"
        label = ""
      group = groups.setdefault(key, {"text": ARROW_RE.sub("", text).strip(), "label": label, "papers": []})
      if paper.name not in group["papers"]:
        group["papers"].append(paper.name)
  ranked = sorted(
    (g for g in groups.values() if len(g["papers"]) >= 2), key=lambda g: (-len(g["papers"]), g["text"].lower())
  )
  if not ranked:
    return "No work is cited by two or more vault papers without being in the vault.\n"
  rows = ["| Cited by | Reference | Stub | Citing papers |", "| --- | --- | --- | --- |"]
  for group in ranked:
    citing = ", ".join(link(name) for name in group["papers"])
    rows.append(f"| {len(group['papers'])} | {cell(group['text'])} | {group['label']} | {citing} |")
  return "\n".join(rows) + "\n"


def review_queue(vault: Vault) -> str:
  out = ["## Claims", ""]
  claims = [n for n in vault.kind("claim") if "not reviewed" in str((n.fm or {}).get("provenance", "")).lower() or not (n.fm or {}).get("provenance")]
  claims.sort(key=lambda n: (STATUS_RANK.get(str((n.fm or {}).get("status")), 9), str((n.fm or {}).get("id"))))
  if claims:
    out += ["| ID | Claim | Status | Pending sources |", "| --- | --- | --- | --- |"]
    for note in claims:
      fm = note.fm or {}
      out.append(f"| {fm.get('id', '')} | {link(note.name)} | {fm.get('status', '')} | {len(note.fm_list('kb_pending'))} |")
  else:
    out.append("Every claim has been reviewed.")
  out += ["", "## Papers with unreviewed annotations", ""]
  papers = []
  for note in sorted(vault.kind("paper"), key=lambda n: n.name):
    provenance = (note.fm or {}).get("annotation_provenance")
    if isinstance(provenance, dict) and provenance.get("generated") and not provenance.get("human_verified"):
      papers.append(f"- {link(note.name)}")
  out += papers or ["None."]
  return "\n".join(out) + "\n"


def topic_claims(vault: Vault, topic) -> str:
  names = []
  for note in vault.kind("claim"):
    targets = [vault.resolve(t, note) for t in note.fm_link_targets("topics")]
    if topic in targets:
      names.append((note.name, (note.fm or {}).get("status", "")))
  lines = ["## Claims", ""]
  if names:
    lines += [f"- {link(name)} ({status})" for name, status in sorted(names, key=lambda x: x[0].lower())]
  else:
    lines.append("No claims yet.")
  return "\n".join(lines) + "\n"


def sync_registry(vault: Vault) -> bool:
  path = vault.data_dir / "claim_ids.json"
  registry = dict(vault.claim_registry)
  for note in vault.kind("claim"):
    claim_id = str((note.fm or {}).get("id", ""))
    if not re.fullmatch(r"C-\d{4}", claim_id):
      continue
    entry = registry.get(claim_id)
    if entry is None:
      registry[claim_id] = {"title": note.name}
    elif not entry.get("merged_into") and entry.get("title") != note.name:
      registry[claim_id] = {**entry, "title": note.name}
  text = json.dumps(dict(sorted(registry.items())), indent=2, ensure_ascii=False) + "\n"
  if not registry and not path.exists():
    return False
  return edit.write_if_changed(path, text)


def run(vault_dir: Path, bib_path: Path, data_dir: Path) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  changed = int(sync_registry(vault))
  indexes = vault_dir / paths.INDEXES
  has_kb = bool(vault.kind("claim") or vault.kind("paper"))
  if has_kb:
    changed += edit.write_if_changed(indexes / "Claims index.md", index_note("claims index", claims_index(vault)))
    changed += edit.write_if_changed(indexes / "Ingestion queue.md", index_note("ingestion queue", ingestion_queue(vault)))
    changed += edit.write_if_changed(indexes / "Review queue.md", index_note("review queue", review_queue(vault)))
  for topic in vault.kind("topic"):
    if markdown.generated_section(topic.body, "claims") is None:
      continue
    body = markdown.replace_generated(topic.body, "claims", topic_claims(vault, topic))
    changed += edit.save(topic, topic.fm, body)
  return changed


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  args = parser.parse_args(argv)
  print(f"build_indexes: {run(args.vault, args.bib, args.data)} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
