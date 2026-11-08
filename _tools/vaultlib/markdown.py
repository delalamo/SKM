"""Line-based parsing of Obsidian-flavoured Markdown.

The vault's notes follow strict layout rules (spec section 4.3), so a small
line-oriented segmenter is enough: every paragraph, list item, table, display
equation, figure embed, callout and heading becomes one ``Block`` with its
line span and, where present, its block ID.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9][A-Za-z0-9_-]*)\s*$")
BLOCK_ID_LINE_RE = re.compile(r"^\^([A-Za-z0-9][A-Za-z0-9_-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
CALLOUT_RE = re.compile(r"^>\s*\[!([A-Za-z0-9_-]+)(?:\|([^\]]*))?\]([+-]?)\s*(.*?)\s*$")
GENERATED_BEGIN_RE = re.compile(r"^%%\s*begin generated:\s*(.+?)\s*%%\s*$")
GENERATED_END_RE = re.compile(r"^%%\s*end generated\s*%%\s*$")
WIKILINK_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
MARK_RE = re.compile(r"<mark\b([^>]*)>(.*?)</mark>", re.DOTALL)
MARK_OPEN_RE = re.compile(r"<mark\b[^>]*>")
MARK_CLASS_RE = re.compile(r'class="([^"]*)"')
ABBR_RE = re.compile(r'<abbr title="([^"]*)">(.*?)</abbr>', re.DOTALL)
PANDOC_CITE_RE = re.compile(r"\[[^\[\]]*@[A-Za-z0-9_:.-]+[^\[\]]*\]")


@dataclass
class Link:
  embed: bool
  target: str  # note name or path; "" for same-note links
  subpath: str  # "" or "#Heading" or "#^block"
  alias: str | None
  raw: str
  line: int  # line number within the text that was scanned (0-based)
  start: int
  end: int

  @property
  def block(self) -> str | None:
    return self.subpath[2:] if self.subpath.startswith("#^") else None

  @property
  def heading(self) -> str | None:
    if self.subpath.startswith("#") and not self.subpath.startswith("#^"):
      return self.subpath[1:]
    return None

  @property
  def display(self) -> str:
    if self.alias is not None:
      return self.alias
    name = self.target.rsplit("/", 1)[-1]
    return name + (self.subpath if self.subpath and not self.block else "")


def parse_link_inner(inner: str) -> tuple[str, str, str | None]:
  """Split ``target#sub|alias`` (``\\|`` is the table-safe pipe)."""
  alias = None
  for sep in ("\\|", "|"):
    if sep in inner:
      inner, alias = inner.split(sep, 1)
      break
  target, hash_, sub = inner.partition("#")
  subpath = "#" + sub if hash_ else ""
  return target.strip(), subpath.strip(), alias


def find_links(text: str, line_offset: int = 0) -> list[Link]:
  links = []
  for line_no, line in enumerate(text.split("\n")):
    for match in WIKILINK_RE.finditer(line):
      target, subpath, alias = parse_link_inner(match.group(2))
      links.append(
        Link(
          embed=bool(match.group(1)),
          target=target,
          subpath=subpath,
          alias=alias,
          raw=match.group(0),
          line=line_offset + line_no,
          start=match.start(),
          end=match.end(),
        )
      )
  return links


def make_link(target: str, alias: str | None = None, subpath: str = "", embed: bool = False, table: bool = False) -> str:
  pipe = "\\|" if table else "|"
  inner = target + subpath + (pipe + alias if alias is not None else "")
  return ("!" if embed else "") + "[[" + inner + "]]"


def strip_markup(text: str) -> str:
  """Plain reading text: link display text, no highlight/abbr tags or IDs."""
  text = WIKILINK_RE.sub(lambda m: Link(False, *parse_link_inner(m.group(2)), "", 0, 0, 0).display, text)
  text = re.sub(r"</?mark\b[^>]*>", "", text)
  text = re.sub(r"<abbr\b[^>]*>|</abbr>", "", text)
  text = BLOCK_ID_RE.sub("", text)
  return text


@dataclass
class Callout:
  kind: str
  metadata: list[str]
  fold: str
  title: str
  body: list[str]


def parse_callout(lines: list[str]) -> Callout | None:
  match = CALLOUT_RE.match(lines[0]) if lines else None
  if not match:
    return None
  meta = (match.group(2) or "").split()
  body = []
  for line in lines[1:]:
    stripped = line[1:]
    body.append(stripped[1:] if stripped.startswith(" ") else stripped)
  return Callout(match.group(1).lower(), meta, match.group(3), match.group(4), body)


@dataclass
class Block:
  kind: str
  start: int  # first line (0-based, relative to the scanned text)
  end: int  # one past the last line
  lines: list[str]
  id: str | None = None
  id_line: int | None = None  # line holding a standalone ^id, if any
  generated: str | None = None  # name of the enclosing generated section
  callout: Callout | None = None
  level: int = 0  # heading level
  heading: str = ""
  callouts: list["Block"] = field(default_factory=list)  # margin callouts before it

  @property
  def text(self) -> str:
    return "\n".join(self.lines)


_STANDALONE_ID_KINDS = {"table", "math", "callout", "quote", "figure", "code"}


def _starts_block(line: str) -> bool:
  return bool(
    HEADING_RE.match(line)
    or line.startswith(("```", "$$", ">", "|", "%%", "![["))
    or LIST_RE.match(line)
  )


def segment(text: str) -> list[Block]:
  """Split a note body into blocks. Blank lines are not returned."""
  lines = text.split("\n")
  blocks: list[Block] = []
  generated: str | None = None
  i = 0
  n = len(lines)
  while i < n:
    line = lines[i]
    if not line.strip():
      i += 1
      continue
    start = i
    begin = GENERATED_BEGIN_RE.match(line)
    if begin or GENERATED_END_RE.match(line):
      blocks.append(Block("marker", i, i + 1, [line], generated=begin.group(1) if begin else None))
      generated = begin.group(1) if begin else None
      i += 1
      continue
    id_only = BLOCK_ID_LINE_RE.match(line)
    if id_only:
      blocks.append(Block("blockid", i, i + 1, [line], id=id_only.group(1)))
      i += 1
      continue
    heading = HEADING_RE.match(line)
    if heading:
      block = Block("heading", i, i + 1, [line], level=len(heading.group(1)), heading=heading.group(2))
      id_match = BLOCK_ID_RE.search(block.heading)
      if id_match:
        block.id = id_match.group(1)
        block.heading = block.heading[: id_match.start()].rstrip()
      i += 1
    elif line.startswith("```"):
      i += 1
      while i < n and not lines[i].startswith("```"):
        i += 1
      i = min(i + 1, n)
      block = Block("code", start, i, lines[start:i])
    elif line.startswith("$$"):
      rest = line[2:]
      if rest.rstrip().endswith("$$") and rest.strip() not in ("", "$$"):
        i += 1
      else:
        i += 1
        while i < n and not lines[i].rstrip().endswith("$$"):
          i += 1
        i = min(i + 1, n)
      block = Block("math", start, i, lines[start:i])
    elif line.startswith(">"):
      i += 1
      while i < n and lines[i].startswith(">"):
        i += 1
      chunk = lines[start:i]
      callout = parse_callout(chunk)
      block = Block("callout" if callout else "quote", start, i, chunk, callout=callout)
    elif line.startswith("|"):
      i += 1
      while i < n and lines[i].startswith("|"):
        i += 1
      block = Block("table", start, i, lines[start:i])
    elif line.startswith("![[") and line.rstrip().endswith("]]"):
      i += 1
      block = Block("figure", start, i, [line])
    elif LIST_RE.match(line):
      indent = len(LIST_RE.match(line).group(1))
      i += 1
      while i < n and lines[i].strip() and not LIST_RE.match(lines[i]) and lines[i].startswith(" " * (indent + 1)):
        i += 1
      block = Block("listitem", start, i, lines[start:i])
    elif line.startswith("%%"):
      i += 1
      while i < n and not lines[i - 1].rstrip().endswith("%%"):
        i += 1
      block = Block("comment", start, i, lines[start:i])
    else:
      i += 1
      while i < n and lines[i].strip() and not _starts_block(lines[i]):
        i += 1
      block = Block("paragraph", start, i, lines[start:i])
    if block.kind in ("paragraph", "listitem") and block.id is None:
      id_match = BLOCK_ID_RE.search(block.lines[-1])
      if id_match:
        block.id = id_match.group(1)
    block.generated = generated
    blocks.append(block)

  # Attach standalone ^id lines to the block above them (tables, equations…).
  result: list[Block] = []
  for block in blocks:
    if block.kind == "blockid" and result and result[-1].kind in _STANDALONE_ID_KINDS and result[-1].id is None:
      result[-1].id = block.id
      result[-1].id_line = block.start
      continue
    result.append(block)
  return result


def attach_callouts(blocks: list[Block]) -> list[Block]:
  """Group margin callouts with the content block that follows them.

  Returns the content blocks (callouts removed); each carries ``callouts``.
  A callout that is not followed by a content block is returned as is.
  """
  out: list[Block] = []
  pending: list[Block] = []
  for block in blocks:
    if block.kind == "callout" and block.callout and "margin" in block.callout.metadata:
      pending.append(block)
      continue
    if block.kind in ("marker", "blockid"):
      out.append(block)
      continue
    block.callouts = pending
    pending = []
    out.append(block)
  out.extend(pending)
  return out


def mark_classes(text: str) -> list[str]:
  """Classes of each <mark> in order of appearance ("" when unclassed)."""
  classes = []
  for match in MARK_OPEN_RE.finditer(text):
    cls = MARK_CLASS_RE.search(match.group(0))
    classes.append(cls.group(1) if cls else "")
  return classes


def generated_section(text: str, name: str) -> tuple[int, int] | None:
  """Character span of the content between a named pair of markers."""
  lines = text.split("\n")
  offset = 0
  begin = None
  for line in lines:
    match = GENERATED_BEGIN_RE.match(line)
    if match and match.group(1) == name and begin is None:
      begin = offset + len(line) + 1
    elif begin is not None and GENERATED_END_RE.match(line):
      return begin, offset
    offset += len(line) + 1
  return None


def replace_generated(text: str, name: str, content: str) -> str:
  span = generated_section(text, name)
  if span is None:
    raise KeyError(f"no generated section {name!r}")
  start, end = span
  if content and not content.endswith("\n"):
    content += "\n"
  return text[:start] + content + text[end:]


def generated_block(name: str, content: str) -> str:
  if content and not content.endswith("\n"):
    content += "\n"
  return f"%% begin generated: {name} %%\n{content}%% end generated %%\n"
