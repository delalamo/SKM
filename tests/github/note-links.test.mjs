import test from "node:test"
import assert from "node:assert/strict"
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import {
  buildLinkIndex,
  linkNote,
  linkNotes,
  readNoteCatalog,
} from "../../scripts/github/note-links.mjs"

const note = (name, content = "") => ({ path: `content/notes/${name}.md`, content })
const catalog = [
  note("ESM"),
  note("ESMFold"),
  note("Inverse folding"),
  note("Protein language models", "---\ntitle: Protein language models\naliases: [PLM]\n---\n"),
  note(
    "Examples",
    "[[notes/Protein language models|PLMs]] and [[Inverse folding|sequence design]].",
  ),
]
const index = buildLinkIndex(catalog)

test("links only the first mention of each destination across names, aliases and case variants", () => {
  const original = note(
    "New note",
    "Title: ESM and PLMs\r\n\r\n**ESM** and ESMFold use PLMs; esm and PLM help inverse folding and sequence design. ESM!  \r\n",
  )
  const result = linkNote(original, index)
  assert.equal(
    result.content,
    "Title: ESM and PLMs\r\n\r\n**[[ESM]]** and [[ESMFold]] use [[Protein language models|PLMs]]; esm and PLM help [[Inverse folding|inverse folding]] and sequence design. ESM!  \r\n",
  )
  assert.equal(result.links.length, 4)
  assert.equal(linkNote(result, index).content, result.content)
  assert.equal(linkNote(result, index).links.length, 0)
})

test("protects Markdown syntax, existing links, images, citations, code, math and metadata", () => {
  const protectedText = [
    "---\ntitle: ESM\naliases: [ESM]\n---",
    "# ESM",
    "[[Other]] ![[ESM]] [[Other|ESM]] [[Other|**ESM**]]",
    "[ESM](https://example.com/ESM) ![ESM](image.png)",
    "[ESM][ref]\n\n[ref]: https://example.com/ESM 'ESM'",
    "https://example.com/ESM user@ESM.org <https://example.com/ESM>",
    "`ESM`\n\n```md\nESM\n```\n\n    ESM",
    "[@ESM; @other, ESM] and @ESM",
    "$ESM$\n\n$$\nESM\n$$",
    '<a href="/ESM">ESM</a> <span>ESM</span>',
    "<!-- ESM -->\n\n%% ESM %%",
  ].join("\n\n")
  const result = linkNote(note("New note", `${protectedText}\n\nESM`), index)
  assert.equal(result.content, `${protectedText}\n\n[[ESM]]`)
})

test("respects word boundaries and prefers the longest name, including Unicode letters", () => {
  const result = linkNote(
    note("New note", "ESMFold ESM2 xESM ESM_name ESMé αESM ESM-based (ESM)."),
    index,
  )
  assert.equal(result.content, "[[ESMFold]] ESM2 xESM ESM_name ESMé αESM [[ESM]]-based (ESM).")
})

test("does not link to itself or invent missing or ambiguous targets", () => {
  const ambiguous = buildLinkIndex([
    ...catalog,
    note("A", "---\naliases: [ambiguous, ESM]\n---\n"),
    note("B", "---\naliases: [ambiguous]\n---\n"),
  ])
  assert.equal(
    linkNote(note("New note", "ESM ambiguous Unknown"), ambiguous).content,
    "[[ESM]] ambiguous Unknown",
  )
  assert.equal(linkNote(note("ESM", "ESM ESMFold"), index).content, "ESM [[ESMFold]]")
})

test("duplicate basenames use full destinations when a unique title or alias resolves them", () => {
  const nested = buildLinkIndex([
    note("one/Shared", "---\naliases: [First model]\n---\n"),
    note("two/Shared", "---\naliases: [Second model]\n---\n"),
  ])
  assert.equal(
    linkNote(note("New note", "Shared First model Second model"), nested).content,
    "Shared [[notes/one/Shared|First model]] [[notes/two/Shared|Second model]]",
  )
  assert.equal(
    linkNote(note("New note", "[first](./one/Shared.md) First model Second model"), nested).content,
    "[first](./one/Shared.md) First model [[notes/two/Shared|Second model]]",
  )
})

test("new notes can link to each other without modifying their source objects or existing notes", () => {
  const notes = [
    note("First note", "# First note\nSecond note ESM"),
    note("Second note", "Title: Second note\nFirst note ESM ESM"),
  ]
  const originals = structuredClone(notes)
  const before = structuredClone(catalog)
  const linked = linkNotes(notes, catalog)
  assert.equal(linked[0].content, "# First note\n[[Second note]] [[ESM]]")
  assert.equal(linked[1].content, "Title: Second note\n[[First note]] [[ESM]] ESM")
  assert.deepEqual(notes, originals)
  assert.deepEqual(catalog, before)
})

test("links prose in tables with empty cells and lists without reformatting it", () => {
  const content = "| | Purpose |\n| --- | --- |\n| ESM | PLMs |\n\n- ESM\n> ESM"
  assert.equal(
    linkNote(note("New note", content), index).content,
    "| | Purpose |\n| --- | --- |\n| [[ESM]] | [[Protein language models|PLMs]] |\n\n- ESM\n> ESM",
  )
})

test("existing wikilinks suppress new links to their destination regardless of label or location", () => {
  for (const content of [
    "[[ESM]] ESM esm",
    "[[ESM|**model**]] ESM",
    "ESM\n\n#### See also\n- [[notes/ESM#Details|model]]",
    "[[PLM]] PLMs and protein language models",
    "# [[Protein language models|PLMs]]\nPLM and protein language models",
  ]) {
    assert.equal(linkNote(note("New note", content), index).content, content)
  }
})

test("existing internal Markdown links and reference links also count as linked destinations", () => {
  for (const content of [
    "[model](./ESM.md) ESM ESM",
    "[model](../notes/Protein%20language%20models.md#Details) PLMs PLM",
    "[model][ref] ESM\n\n[ref]: /notes/ESM",
  ]) {
    assert.equal(linkNote(note("New note", content), index).content, content)
  }
})

test("wikilinks in code, comments, or images do not consume the first prose mention", () => {
  const content = "`[[ESM]]`\n\n```md\n[[ESM]]\n```\n\n%% [[ESM]] %%\n\n![[ESM]]\n\nESM ESM"
  assert.equal(
    linkNote(note("New note", content), index).content,
    content.replace(/ESM ESM$/, "[[ESM]] ESM"),
  )
})

test("alias examples in code do not become link targets", () => {
  const examples = buildLinkIndex([
    ...catalog,
    note("Code", "```md\n[[ESM|Untrusted alias]]\n```\n"),
  ])
  assert.equal(linkNote(note("New note", "Untrusted alias"), examples).content, "Untrusted alias")
})

test("catalog reads only regular Markdown note files from the base tree", async () => {
  const cwd = process.cwd()
  const directory = await mkdtemp(join(tmpdir(), "note-catalog-"))
  try {
    process.chdir(directory)
    await mkdir("content/notes", { recursive: true })
    await writeFile("content/notes/ESM.md", "# ESM")
    const entries = [
      { path: "content/notes/ESM.md", type: "blob", mode: "100644" },
      { path: "content/notes/symlink.md", type: "blob", mode: "120000" },
      { path: "content/notes/folder.md", type: "tree", mode: "040000" },
      { path: "content/assets/image.png", type: "blob", mode: "100644" },
    ]
    assert.deepEqual(await readNoteCatalog(entries), [note("ESM", "# ESM")])
  } finally {
    process.chdir(cwd)
    await rm(directory, { recursive: true })
  }
})
