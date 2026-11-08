"""Rules for paper notes and their margin layer (spec sections 4, 6, 7)."""

from __future__ import annotations

import re

from vaultlib import markdown, paths

from . import rule

RELATIONS = ("supports", "qualifies", "contradicts", "cited", "related")
MARGIN_TYPES = ("claim", "context", "eq", "cite")
REQUIRED_ALL = (
  "citekey", "title", "aliases", "authors", "year", "venue", "doi", "license", "fulltext",
  "block_prefix", "status_checks", "topics", "claims", "cssclasses", "tags",
)
REQUIRED_TEXT = (
  "version_in_kb", "source_pdf", "source_conversion", "data_availability", "funding_coi",
)
STATUS_CHECKS = ("retraction_watch", "crossref_updates", "pubpeer")
CC_RE = re.compile(r"^(CC0|CC BY(-NC)?(-SA|-ND)?)( \d\.\d)?$")
LABEL_RE = re.compile(r"(^|\s)\(?[a-h]\)\s")
REF_ID_RE = re.compile(r"-ref-(\d+)$")


def papers(vault):
  return [note for note in vault.kind("paper")]


def passages(note):
  """Content blocks of a paper with the margin callouts placed before them."""
  return [
    block
    for block in markdown.attach_callouts(note.blocks)
    if block.kind not in ("marker", "blockid", "callout", "heading")
  ]


def orphan_callouts(note):
  return [
    block
    for block in markdown.attach_callouts(note.blocks)
    if block.kind == "callout" and block.callout and "margin" in block.callout.metadata
  ]


def is_reference(note, block) -> bool:
  prefix = (note.fm or {}).get("block_prefix", "")
  return bool(block.id and block.id.startswith(f"{prefix}-ref-"))


def cited_refs(note, block) -> list[str]:
  """Reference block IDs cited in a passage, in order of first citation."""
  prefix = (note.fm or {}).get("block_prefix", "")
  out: list[str] = []
  for link in markdown.find_links(block.text):
    if link.target == "" and link.block and link.block.startswith(f"{prefix}-ref-") and link.block not in out:
      out.append(link.block)
  return out


def claim_relation(callout) -> str | None:
  words = [word for word in callout.metadata if word in RELATIONS]
  return words[0] if len(words) == 1 else None


def claim_links(callout) -> list[markdown.Link]:
  return markdown.find_links("\n".join(callout.body))


def callout_targets(vault, note):
  """(claim note, relation, passage block) for every claim callout in a paper."""
  for block in passages(note):
    for callout_block in block.callouts:
      callout = callout_block.callout
      if callout.kind != "claim":
        continue
      links = claim_links(callout)
      if len(links) != 1:
        continue
      target = vault.resolve(links[0].target, note)
      if target is not None and target.kind == "claim":
        yield target, claim_relation(callout), block


@rule("PAPER-FM", "papers", "Required paper frontmatter is present and well formed")
def paper_fm(vault):
  for note in papers(vault):
    fm = note.fm or {}
    for key in REQUIRED_ALL:
      if key not in fm:
        yield note.rel, 1, f"missing frontmatter field '{key}'"
    if fm.get("fulltext") not in ("full", "digest", "stub"):
      yield note.rel, 1, "fulltext must be full, digest or stub"
    elif fm.get("fulltext") != "stub":
      for key in REQUIRED_TEXT:
        if key not in fm:
          yield note.rel, 1, f"missing frontmatter field '{key}'"
    if fm.get("citekey") != note.name:
      yield note.rel, 1, "citekey must equal the file name"
    if vault.bib and note.name not in vault.bib:
      yield note.rel, 1, f"citekey {note.name} is not in the bibliography"
    if "paper-margin" not in (fm.get("cssclasses") or []):
      yield note.rel, 1, "cssclasses must include paper-margin"
    if "paper" not in (fm.get("tags") or []):
      yield note.rel, 1, "tags must include paper"
    checks = fm.get("status_checks")
    if not isinstance(checks, dict) or any(key not in checks for key in STATUS_CHECKS):
      yield note.rel, 1, "status_checks needs retraction_watch, crossref_updates and pubpeer"
    provenance = fm.get("annotation_provenance")
    if provenance is not None and (
      not isinstance(provenance, dict) or any(key not in provenance for key in ("generator", "generated", "human_verified"))
    ):
      yield note.rel, 1, "annotation_provenance needs generator, generated and human_verified"
    if not re.fullmatch(r"[a-z]{2,4}\d{2}[a-z]?", str(fm.get("block_prefix", ""))):
      yield note.rel, 1, "block_prefix must look like gul23 (letters + two-digit year)"


@rule("PAPER-LICENCE", "papers", "Full text only under a Creative Commons licence, stated in the status banner")
def paper_licence(vault):
  for note in papers(vault):
    fm = note.fm or {}
    if fm.get("fulltext") != "full":
      continue
    licence = str(fm.get("license", ""))
    if not CC_RE.match(licence):
      yield note.rel, 1, f"full text needs a Creative Commons licence, not '{licence}'"
    banner = next((b for b in note.blocks if b.kind == "callout" and b.callout.kind == "status"), None)
    if banner is None or "creativecommons.org" not in banner.text:
      yield note.rel, 1, "status banner must link the Creative Commons licence"


@rule("PAPER-STATUS", "papers", "A paper note opens with a full-width status banner")
def paper_status(vault):
  for note in papers(vault):
    first = next((b for b in note.blocks if b.kind not in ("marker", "blockid")), None)
    if first is None or first.kind != "callout" or first.callout.kind != "status":
      yield note.rel, note.line_no(first.start if first else 0), "first block must be a [!status] callout"
    elif "margin" in first.callout.metadata:
      yield note.rel, note.line_no(first.start), "the status banner is full width (no margin)"


@rule("PAPER-STUB", "papers", "A stub holds only its status banner")
def paper_stub(vault):
  for note in papers(vault):
    if (note.fm or {}).get("fulltext") != "stub":
      continue
    for block in note.blocks:
      if not (block.kind == "callout" and block.callout.kind == "status"):
        yield note.rel, note.line_no(block.start), "stub notes hold only the status banner"
        break


@rule("PAPER-BLOCKIDS", "papers", "Every paragraph, table, equation and caption has a block ID with the paper's prefix")
def paper_blockids(vault):
  for note in papers(vault):
    fm = note.fm or {}
    if fm.get("fulltext") == "stub":
      continue
    prefix = str(fm.get("block_prefix", ""))
    for block in note.blocks:
      if block.kind in ("paragraph", "table", "math", "listitem") and block.generated is None:
        if block.lines[0].lstrip().startswith("[^"):
          continue  # footnote definitions
        if not block.id:
          yield note.rel, note.line_no(block.start), f"{block.kind} has no block ID"
          continue
      if block.id and not block.id.startswith(prefix + "-"):
        yield note.rel, note.line_no(block.start), f"block ID ^{block.id} must start with {prefix}-"


@rule("PAPER-MARGIN-WORD", "papers", "Margin callouts carry 'margin' and say who wrote them (llm or human)")
def paper_margin_word(vault):
  for note in papers(vault):
    for block in note.blocks:
      if block.kind != "callout" or block.callout.kind not in MARGIN_TYPES:
        continue
      meta = block.callout.metadata
      if "margin" not in meta:
        yield note.rel, note.line_no(block.start), f"{block.callout.kind} callout must float in the margin"
      if sum(word in meta for word in ("llm", "human")) != 1:
        yield note.rel, note.line_no(block.start), "callout must carry exactly one of llm or human"


@rule("PAPER-ORPHAN-CALLOUT", "papers", "Every margin callout sits directly before the passage it annotates")
def paper_orphan(vault):
  for note in papers(vault):
    for block in orphan_callouts(note):
      yield note.rel, note.line_no(block.start), "margin callout is not followed by a passage"


@rule("PAPER-HIGHLIGHT-COUNT", "papers", "One highlight per claim or context callout in each passage")
def paper_highlight_count(vault):
  for note in papers(vault):
    for block in passages(note):
      classes = markdown.mark_classes(block.text)
      kinds = [c.callout.kind for c in block.callouts]
      for kind, cls in (("claim", "pm-claim"), ("context", "pm-context")):
        if kinds.count(kind) != classes.count(cls):
          yield note.rel, note.line_no(block.start), (
            f"{kinds.count(kind)} {kind} callouts but {classes.count(cls)} {cls} highlights"
          )


@rule("PAPER-CALLOUT-ORDER", "papers", "Callouts follow their highlights' order; equation notes come first")
def paper_callout_order(vault):
  for note in papers(vault):
    for block in passages(note):
      kinds = [c.callout.kind for c in block.callouts]
      if "eq" in kinds and block.kind != "math":
        yield note.rel, note.line_no(block.start), "equation callout must precede a display equation"
      if "eq" in kinds and kinds.index("eq") != 0:
        yield note.rel, note.line_no(block.start), "equation callouts come first"
      highlight_order = [{"pm-claim": "claim", "pm-context": "context"}.get(c, c) for c in markdown.mark_classes(block.text)]
      callout_order = [kind for kind in kinds if kind in ("claim", "context")]
      if sorted(highlight_order) == sorted(callout_order) and highlight_order != callout_order:
        yield note.rel, note.line_no(block.start), "callouts are not in the order of their highlights"
      if "cite" in kinds and kinds[-1] != "cite":
        yield note.rel, note.line_no(block.start), "the reference callout comes after the other callouts"


@rule("PAPER-NO-LABELS", "papers", "No labelled items (a), (b) in callouts and no data-label on highlights")
def paper_no_labels(vault):
  for note in papers(vault):
    for block in note.blocks:
      if "data-label" in block.text:
        yield note.rel, note.line_no(block.start), "data-label attributes are not allowed"
      if block.kind == "callout" and block.callout.kind in ("claim", "context"):
        if any(LABEL_RE.search(" " + line) for line in block.callout.body + [block.callout.title]):
          yield note.rel, note.line_no(block.start), "labelled items such as (a) and (b) are not allowed"


@rule("PAPER-SPAN", "papers", "A highlight excludes wikilinks and occurs exactly once in its passage")
def paper_span(vault):
  for note in papers(vault):
    for block in passages(note):
      plain = markdown.strip_markup(block.text)
      for match in markdown.MARK_RE.finditer(block.text):
        span = match.group(2)
        if "[[" in span:
          yield note.rel, note.line_no(block.start), "highlight contains a wikilink"
          continue
        span_plain = markdown.strip_markup(span).strip()
        if not span_plain:
          yield note.rel, note.line_no(block.start), "empty highlight"
        elif plain.count(span_plain) != 1:
          yield note.rel, note.line_no(block.start), f"highlight text occurs {plain.count(span_plain)} times in its passage"


@rule("PAPER-CLAIM-ONE", "papers", "Each claim callout links exactly one claim as a single list item, with one relation")
def paper_claim_one(vault):
  for note in papers(vault):
    for block in note.blocks:
      if block.kind != "callout":
        continue
      callout = block.callout
      line = note.line_no(block.start)
      relation_words = [word for word in callout.metadata if word in RELATIONS]
      if callout.kind != "claim":
        if relation_words:
          yield note.rel, line, "relation words belong on claim callouts only"
        continue
      if len(relation_words) != 1:
        yield note.rel, line, "claim callout needs exactly one relation word"
      links = claim_links(callout)
      items = [row for row in callout.body if row.strip()]
      if len(links) != 1 or not items or not re.fullmatch(r"- \[\[[^\]]+\]\]", items[0].strip()):
        yield note.rel, line, "claim callout must list exactly one claim as '- [[Claim]]'"
        continue
      target = vault.resolve(links[0].target, note)
      if target is not None and target.kind != "claim":
        yield note.rel, line, f"claim callout links {target.rel}, which is not a claim note"


def _definitional(target) -> bool:
  return target is not None and target.kind in ("glossary", "concept")


@rule("PAPER-MARGIN-LINKS", "papers", "Context and equation notes link only glossary or concept notes, or blocks of the same note")
def paper_margin_links(vault):
  for note in papers(vault):
    for block in note.blocks:
      if block.kind != "callout" or block.callout.kind not in ("context", "eq"):
        continue
      for link in markdown.find_links("\n".join(block.lines)):
        if link.target == "" or _definitional(vault.resolve(link.target, note)):
          continue
        yield note.rel, note.line_no(block.start), f"{block.callout.kind} note links {link.raw}"


@rule("PAPER-TEXT-LINKS", "papers", "Paper text links only glossary terms; reference lines may link vault papers")
def paper_text_links(vault):
  for note in papers(vault):
    for block in note.blocks:
      if block.kind in ("callout", "marker") or block.generated:
        continue
      reference = is_reference(note, block)
      for link in markdown.find_links(block.text):
        if link.target == "" or (link.embed and re.search(r"\.\w{2,4}$", link.target)):
          continue
        target = vault.resolve(link.target, note)
        if _definitional(target):
          continue
        if reference and target is not None and target.kind == "paper":
          continue
        yield note.rel, note.line_no(block.start), f"paper text may not link {link.raw}"


@rule("PAPER-CITE-CALLOUT", "papers", "Each reference callout lists every citation in its passage, with a matching count")
def paper_cite_callout(vault):
  for note in papers(vault):
    for block in passages(note):
      if is_reference(note, block):
        continue
      refs = cited_refs(note, block)
      cites = [c for c in block.callouts if c.callout.kind == "cite"]
      line = note.line_no(block.start)
      if not refs:
        if cites:
          yield note.rel, line, "reference callout on a passage that cites nothing"
        continue
      if len(cites) != 1:
        yield note.rel, line, f"passage cites {len(refs)} references but has {len(cites)} reference callouts"
        continue
      callout = cites[0].callout
      listed = [link.block for link in claim_links(callout) if link.target == "" and link.block]
      if listed != refs:
        yield note.rel, line, "reference callout does not list the passage's citations in order"
      if callout.title != f"References ({len(refs)})":
        yield note.rel, line, f"reference callout title should be 'References ({len(refs)})'"


@rule("PAPER-CLAIMS-FM", "papers", "Frontmatter claims match the claims linked from margin callouts exactly")
def paper_claims_fm(vault):
  for note in papers(vault):
    linked = []
    for target, _, _ in callout_targets(vault, note):
      if target.name not in linked:
        linked.append(target.name)
    listed = note.fm_link_targets("claims")
    if sorted(listed) != sorted(linked):
      yield note.rel, 1, "frontmatter claims do not match the margin claim callouts"
