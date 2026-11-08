"""Rules for claim notes (spec section 8)."""

from __future__ import annotations

import re

from vaultlib import markdown
from vaultlib.vault import link_target

from . import rule
from .papers import callout_targets

STATUSES = ("supported", "tentative", "proposed", "model-derived", "contested")
STRENGTHS = ("strong", "moderate", "weak-to-moderate", "weak")
KB_KEYS = {"kb_supporting": "supports", "kb_qualifying": "qualifies", "kb_contradicting": "contradicts"}
REQUIRED = ("id", "type", "status", "evidence_strength", "scope", "topics", *KB_KEYS, "independence", "provenance", "tags")
ID_RE = re.compile(r"^C-\d{4}$")
BANNED_TITLE = re.compile(r'[#^\[\]|\\/:*?"<>]')
EVIDENCE = "Evidence"
PENDING = "Evidence pending verification"
RETIRED_HEADINGS = {"topics", "falsified by", "see also"}
AUTHOR_CONTEXT = r"(?=\s+et\s+al\b|\s+and\s+[A-Z]|\s*\(\d{4}|['’]s\b|\s+\d{4}\b)"
TOKEN_RE = re.compile(r"\b[A-ZÀ-Ý][\w'’-]*[\w]")


def claims(vault):
  return vault.kind("claim")


def summary_blocks(note):
  out = []
  for block in note.blocks:
    if block.kind == "heading":
      break
    out.append(block)
  return out


def summary_text(note) -> str:
  return "\n".join(block.text for block in summary_blocks(note) if block.kind in ("paragraph", "listitem"))


def sections(note) -> dict[str, list]:
  """Blocks under each level-2 heading, keyed by heading text."""
  out: dict[str, list] = {}
  current = None
  for block in note.blocks:
    if block.kind == "heading" and block.level <= 2:
      current = block.heading
      out.setdefault(current, [])
    elif current is not None:
      out[current].append(block)
  return out


def source_sections(blocks) -> list[tuple[markdown.Block, list]]:
  """(### heading block, blocks under it) within a section."""
  out = []
  for block in blocks:
    if block.kind == "heading" and block.level == 3:
      out.append((block, []))
    elif out:
      out[-1][1].append(block)
  return out


def heading_paper(vault, note, heading_block):
  links = markdown.find_links(heading_block.lines[0])
  if len(links) != 1:
    return None, None
  return vault.resolve(links[0].target, note), links[0]


def kb_papers(note, key) -> list[str]:
  return [link_target(item) for item in note.fm_list(key)]


@rule("CLAIM-FM", "claims", "Required claim frontmatter is present, with allowed values")
def claim_fm(vault):
  for note in claims(vault):
    fm = note.fm or {}
    for key in REQUIRED:
      if key not in fm:
        yield note.rel, 1, f"missing frontmatter field '{key}'"
    if fm.get("type") != "claim":
      yield note.rel, 1, "type must be claim"
    if fm.get("status") not in STATUSES:
      yield note.rel, 1, f"status must be one of {', '.join(STATUSES)}"
    if fm.get("evidence_strength") not in STRENGTHS:
      yield note.rel, 1, f"evidence_strength must be one of {', '.join(STRENGTHS)}"
    if not str(fm.get("scope") or "").strip():
      yield note.rel, 1, "scope is empty"
    if "claim" not in (fm.get("tags") or []):
      yield note.rel, 1, "tags must include claim"
    for target in note.fm_link_targets("topics"):
      found = vault.resolve(target, note)
      if found is not None and found.kind != "topic":
        yield note.rel, 1, f"topic {target} is not a topic page"
    for key in KB_KEYS:
      for target in kb_papers(note, key):
        found = vault.resolve(target, note)
        if found is not None and found.kind != "paper":
          yield note.rel, 1, f"{key} entry {target} is not a paper note"


@rule("CLAIM-TITLE", "claims", "The file name is the claim: no link-breaking characters, at most 150 characters")
def claim_title(vault):
  for note in claims(vault):
    if BANNED_TITLE.search(note.name):
      yield note.rel, 1, "claim title contains a character that breaks links (# ^ [ ] | \\ / : * ? \" < >)"
    if len(note.name) > 150:
      yield note.rel, 1, "claim title is longer than 150 characters"
    if note.name.endswith("."):
      yield note.rel, 1, "claim title ends with a full stop"


@rule("CLAIM-ID", "claims", "Claim IDs are C-NNNN, unique, and registered with the current title")
def claim_id(vault):
  registry = vault.claim_registry
  seen: dict[str, str] = {}
  for note in claims(vault):
    claim_id_value = str((note.fm or {}).get("id", ""))
    if not ID_RE.match(claim_id_value):
      yield note.rel, 1, f"claim id '{claim_id_value}' is not of the form C-0001"
      continue
    if claim_id_value in seen:
      yield note.rel, 1, f"claim id {claim_id_value} is also used by {seen[claim_id_value]}"
    seen[claim_id_value] = note.rel
    entry = registry.get(claim_id_value)
    if entry is None:
      yield note.rel, 1, f"claim id {claim_id_value} is not in claim_ids.json"
    elif entry.get("merged_into"):
      yield note.rel, 1, f"claim id {claim_id_value} was retired into {entry['merged_into']}"
    elif entry.get("title") != note.name:
      yield note.rel, 1, f"claim_ids.json has a different title for {claim_id_value}"


@rule("REGISTRY", "claims", "Every registered claim ID has a note; retired IDs point to live ones")
def registry_rule(vault):
  registry = vault.claim_registry
  live = {str((note.fm or {}).get("id")) for note in claims(vault)}
  for claim_id_value, entry in sorted(registry.items()):
    target = entry.get("merged_into")
    if target:
      if target not in live:
        yield "claim_ids.json", 1, f"{claim_id_value} was merged into {target}, which has no note"
    elif claim_id_value not in live:
      yield "claim_ids.json", 1, f"{claim_id_value} ({entry.get('title')}) has no claim note"


@rule("CLAIM-SUMMARY", "claims", "A claim note opens with a summary paragraph")
def claim_summary(vault):
  for note in claims(vault):
    if not summary_text(note).strip():
      yield note.rel, note.line_no(0), "claim note has no summary paragraph"


def _author_hits(vault, text: str) -> list[str]:
  eponyms = set(vault.data_lines("eponyms.txt"))
  ambiguous = {word.lower() for word in vault.data_lines("ambiguous_surnames.txt")}
  surnames = vault.author_surnames
  hits = []
  if re.search(r"\bet\s+al\b", text):
    hits.append("et al.")
  for match in TOKEN_RE.finditer(text):
    token = match.group(0)
    if token.endswith(("'s", "’s")):
      token = token[:-2]
    if token not in surnames or token in eponyms:
      continue
    if token.lower() in ambiguous and not re.match(AUTHOR_CONTEXT, text[match.start() + len(token):]):
      continue
    hits.append(token)
  return hits


@rule("CLAIM-AUTHORS", "claims", "The summary names no author")
def claim_authors(vault):
  for note in claims(vault):
    text = markdown.strip_markup(summary_text(note))
    for hit in _author_hits(vault, text):
      yield note.rel, note.line_no(0), f"summary names an author: {hit}"


@rule("CLAIM-SUMMARY-LINKS", "claims", "The summary links no paper and no block")
def claim_summary_links(vault):
  for note in claims(vault):
    for block in summary_blocks(note):
      for link in markdown.find_links(block.text):
        target = vault.resolve(link.target, note)
        if link.block or (target is not None and target.kind == "paper"):
          yield note.rel, note.line_no(block.start), f"summary links a paper or block: {link.raw}"


def _plain_with_links(text: str):
  """Plain text plus (start, end, target) spans of the links in it."""
  out, spans, cursor = [], [], 0
  for match in markdown.WIKILINK_RE.finditer(text):
    out.append(markdown.strip_markup(text[cursor:match.start()]))
    target, subpath, alias = markdown.parse_link_inner(match.group(2))
    display = alias if alias is not None else target
    start = sum(len(part) for part in out)
    out.append(display)
    spans.append((start, start + len(display), target, bool(match.group(1))))
    cursor = match.end()
  out.append(markdown.strip_markup(text[cursor:]))
  return "".join(out), spans


def _prose(note) -> str:
  return "\n".join(
    block.text for block in note.blocks
    if block.kind in ("paragraph", "listitem") and block.generated is None
  )


@rule("CLAIM-TOPIC-FIRST", "claims", "Each frontmatter topic is linked exactly once, at its first mention")
def claim_topic_first(vault):
  for note in claims(vault):
    plain, spans = _plain_with_links(_prose(note))
    for topic_name in note.fm_link_targets("topics"):
      topic = vault.resolve(topic_name, note)
      if topic is None:
        continue
      links = [span for span in spans if not span[3] and vault.resolve(span[2], note) is topic]
      if len(links) != 1:
        yield note.rel, 1, f"topic {topic.name} is linked {len(links)} times (must be exactly once)"
        continue
      names = sorted(vault.topic_names(topic), key=len, reverse=True)
      pattern = re.compile(r"\b(" + "|".join(re.escape(name) for name in names) + r")\b", re.IGNORECASE)
      first = pattern.search(plain)
      start, end = links[0][0], links[0][1]
      if first is None:
        continue
      if not (start <= first.start() < end):
        yield note.rel, 1, f"topic {topic.name} is first mentioned before its link"


@rule("CLAIM-LINK-ONCE", "claims", "No topic or claim is linked twice; no Topics, See also or Falsified by section")
def claim_link_once(vault):
  for note in claims(vault):
    counts: dict[str, int] = {}
    for link in note.links:
      if link.embed:
        continue
      target = vault.resolve(link.target, note)
      if target is not None and target.kind in ("topic", "claim") and target is not note:
        counts[target.rel] = counts.get(target.rel, 0) + 1
    for rel, count in sorted(counts.items()):
      if count > 1:
        yield note.rel, 1, f"{rel} is linked {count} times"
    for block in note.blocks:
      if block.kind == "heading" and block.heading.strip().lower() in RETIRED_HEADINGS:
        yield note.rel, note.line_no(block.start), f"retired section '{block.heading}'"


@rule("CLAIM-EVIDENCE", "claims", "An Evidence section has a heading, prose and excerpts for each source")
def claim_evidence(vault):
  for note in claims(vault):
    wanted = []
    for key in KB_KEYS:
      for target in kb_papers(note, key):
        if target not in wanted:
          wanted.append(target)
    found_sections = sections(note)
    if EVIDENCE not in found_sections:
      if wanted:
        yield note.rel, 1, "claim has evidence but no '## Evidence' section"
      continue
    covered = set()
    for heading, blocks in source_sections(found_sections[EVIDENCE]):
      paper, link = heading_paper(vault, note, heading)
      line = note.line_no(heading.start)
      if paper is None or paper.kind != "paper":
        yield note.rel, line, "evidence heading must link one paper note"
        continue
      if not (link.alias or "").strip():
        yield note.rel, line, "evidence heading link needs a readable label"
      if paper.name not in wanted:
        yield note.rel, line, f"evidence section for {paper.name}, which is not in the kb lists"
      covered.add(paper.name)
      prose = [b for b in blocks if b.kind == "paragraph" and b.generated is None and b.text.strip()]
      embeds = [
        link for b in blocks if b.generated
        for link in markdown.find_links(b.text) if link.embed and link.block
        and vault.resolve(link.target, note) is paper
      ]
      if not prose:
        yield note.rel, line, f"evidence from {paper.name} needs two or three sentences"
      if not embeds:
        yield note.rel, line, f"evidence from {paper.name} needs embedded excerpts"
    for name in wanted:
      if name not in covered:
        yield note.rel, 1, f"no evidence section for {name}"


@rule("CLAIM-KB-MARGIN", "claims", "kb lists match the papers' margin claim callouts exactly")
def claim_kb_margin(vault):
  expected: dict[str, dict[str, set[str]]] = {}
  for paper in vault.kind("paper"):
    for target, relation, _ in callout_targets(vault, paper):
      for key, rel in KB_KEYS.items():
        if relation == rel:
          expected.setdefault(target.rel, {}).setdefault(key, set()).add(paper.name)
  for note in claims(vault):
    for key in KB_KEYS:
      listed = set(kb_papers(note, key))
      linked = expected.get(note.rel, {}).get(key, set())
      for name in sorted(listed - linked):
        yield note.rel, 1, f"{key} lists {name}, but {name} has no '{KB_KEYS[key]}' callout for this claim"
      for name in sorted(linked - listed):
        yield note.rel, 1, f"{name} {KB_KEYS[key]} this claim in its margin but is not in {key}"


@rule("CLAIM-PENDING", "claims", "kb_pending names only papers not yet annotated, each with a pending-evidence section")
def claim_pending(vault):
  for note in claims(vault):
    pending = []
    for item in note.fm_list("kb_pending"):
      paper_name = link_target(item.get("paper")) if isinstance(item, dict) else None
      if not paper_name:
        yield note.rel, 1, "kb_pending entries need a paper"
        continue
      paper = vault.resolve(paper_name, note)
      if paper is None or paper.kind != "paper":
        yield note.rel, 1, f"kb_pending paper {paper_name} is not a paper note"
        continue
      if vault.paper_state(paper) == "annotated":
        yield note.rel, 1, f"{paper_name} is annotated; resolve its pending evidence into a margin callout or drop it"
      pending.append(paper.name)
    found_sections = sections(note)
    if PENDING in found_sections and not pending:
      yield note.rel, 1, f"'## {PENDING}' section without kb_pending entries"
    if pending:
      if PENDING not in found_sections:
        yield note.rel, 1, f"kb_pending entries need a '## {PENDING}' section"
        continue
      covered = set()
      for heading, _ in source_sections(found_sections[PENDING]):
        paper, _ = heading_paper(vault, note, heading)
        if paper is not None:
          covered.add(paper.name)
      for name in pending:
        if name not in covered:
          yield note.rel, 1, f"no pending-evidence section for {name}"
