import { readFile } from "node:fs/promises"
import { unified } from "unified"
import remarkParse from "remark-parse"
import remarkGfm from "remark-gfm"
import remarkFrontmatter from "remark-frontmatter"
import remarkMath from "remark-math"
import { load as loadYaml, JSON_SCHEMA } from "js-yaml"

const markdown = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkFrontmatter, ["yaml", "toml"])
  .use(remarkMath)
const normalize = (text) => text.normalize("NFC").toLowerCase()
const stem = (path) => path.slice("content/".length, -3)
const basename = (path) => path.split("/").at(-1).slice(0, -3)
const wikiLinks = /!?\[\[([^\]\n]+)\]\]/g
const wordBefore = /[\p{L}\p{M}\p{N}_]$/u
const wordAfter = /^[\p{L}\p{M}\p{N}_]/u
const skip = new Set([
  "heading",
  "link",
  "image",
  "linkReference",
  "imageReference",
  "definition",
  "code",
  "inlineCode",
  "yaml",
  "toml",
  "html",
  "math",
  "inlineMath",
])

export async function readNoteCatalog(entries) {
  const notes = []
  for (const entry of entries) {
    if (
      entry.type !== "blob" ||
      !["100644", "100755"].includes(entry.mode) ||
      !entry.path.startsWith("content/notes/") ||
      !entry.path.endsWith(".md")
    )
      continue
    // The workflow checks out trusted default-branch files; never follow symlinks.
    notes.push({ path: entry.path, content: await readFile(entry.path, "utf8") })
  }
  return notes
}

function add(map, name, path) {
  const key = normalize(name)
  if (!map.has(key)) map.set(key, new Set())
  map.get(key).add(path)
}

export function buildLinkIndex(notes) {
  const destinations = new Map()
  const names = new Map()
  const aliases = new Map()
  const targets = new Map()
  const trees = new Map()
  for (const note of notes) {
    // These characters have structural meaning in a wikilink destination.
    if (/[\[\]#|^\r\n]/.test(note.path)) continue
    targets.set(note.path, stem(note.path))
    add(destinations, stem(note.path), note.path)
    add(destinations, basename(note.path), note.path)
    add(names, basename(note.path), note.path)
    const tree = markdown.parse(note.content)
    trees.set(note.path, tree)
    const frontmatter = tree.children.find((node) => node.type === "yaml")
    if (frontmatter) {
      const data = loadYaml(frontmatter.value, { schema: JSON_SCHEMA }) ?? {}
      const values = data.aliases ?? data.alias ?? []
      for (const label of [
        data.title,
        ...(Array.isArray(values) ? values : String(values).split(",")),
      ]) {
        if (typeof label === "string") {
          add(aliases, label.trim(), note.path)
          add(destinations, label.trim(), note.path)
        }
      }
    }
  }
  // Reuse the vault's established display aliases, e.g. [[Protein language models|PLMs]].
  for (const note of notes) {
    const tree = trees.get(note.path)
    if (!tree) continue
    for (const range of textRanges(tree)) {
      const text = note.content.slice(range.start, range.end)
      for (const match of text.matchAll(wikiLinks)) {
        if (match[0].startsWith("!")) continue
        const [destination, label] = match[1].split("|")
        if (!label) continue
        const key = normalize(destination.split("#")[0].replace(/\.md$/, ""))
        const paths = destinations.get(key)
        if (paths?.size === 1) add(aliases, label, [...paths][0])
      }
    }
  }
  for (const [path] of targets) {
    if (names.get(normalize(basename(path)))?.size === 1) targets.set(path, basename(path))
  }
  const terms = new Map()
  for (const key of new Set([...names.keys(), ...aliases.keys()])) {
    const paths = names.get(key) ?? aliases.get(key)
    // Prefer exact filenames over aliases; never choose randomly between ambiguous aliases.
    if (paths.size !== 1 || key.length < 2 || /[\[\]#|^/\\\r\n]/.test(key)) continue
    terms.set(key, [...paths][0])
  }
  const escaped = [...terms.keys()]
    .sort((a, b) => b.length - a.length || a.localeCompare(b))
    .map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
  return { terms, targets, pattern: escaped.length ? new RegExp(escaped.join("|"), "giu") : null }
}

function textRanges(tree) {
  const ranges = []
  function visit(node) {
    if (skip.has(node.type)) return
    // GFM can synthesize empty table-cell text with no source position.
    if (node.type === "text" && node.position) {
      ranges.push({ start: node.position.start.offset, end: node.position.end.offset })
    }
    for (const child of node.children ?? []) visit(child)
  }
  visit(tree)
  return ranges
}

function protectedRanges(content) {
  const ranges = []
  // Obsidian links/comments and Pandoc citations are not recognized by CommonMark.
  // Protect paired inline HTML too: its text would otherwise look like ordinary prose.
  for (const pattern of [
    /!?\[\[[\s\S]*?\]\]/g,
    /\[[^\]\n]*@[^\]\n]*\]/g,
    /(?<![\p{L}\p{N}_])@[\p{L}\p{N}_][\p{L}\p{N}_.:/-]*/gu,
    /%%[\s\S]*?%%/g,
    /<([a-z][\w:-]*)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,
    /^\s*(?:\*\*)?Title:[^\n]*/i,
  ]) {
    const matches = pattern.global
      ? content.matchAll(pattern)
      : [pattern.exec(content)].filter(Boolean)
    for (const match of matches)
      ranges.push({ start: match.index, end: match.index + match[0].length })
  }
  return ranges
}

export function linkNote(note, index) {
  if (!index.pattern) return { ...note, links: [] }
  const { content } = note
  const protectedText = protectedRanges(content)
  const edits = []
  for (const range of textRanges(markdown.parse(content))) {
    const text = content.slice(range.start, range.end)
    for (const match of text.matchAll(index.pattern)) {
      const start = range.start + match.index
      const end = start + match[0].length
      if (
        wordBefore.test(content.slice(Math.max(0, start - 2), start)) ||
        wordAfter.test(content.slice(end, end + 2))
      )
        continue
      if (protectedText.some((span) => start < span.end && end > span.start)) continue
      const path = index.terms.get(normalize(match[0]))
      if (!path || path === note.path) continue
      const target = index.targets.get(path)
      const link = target === match[0] ? `[[${target}]]` : `[[${target}|${match[0]}]]`
      edits.push({ start, end, link, target })
    }
  }
  // Apply only insertions around existing prose, from right to left; never reserialize Markdown.
  let linked = content
  for (const edit of [...edits].reverse()) {
    linked = linked.slice(0, edit.start) + edit.link + linked.slice(edit.end)
  }
  return { ...note, content: linked, links: edits.map((edit) => edit.target) }
}

export function linkNotes(notes, catalog) {
  const index = buildLinkIndex([...catalog, ...notes])
  return notes.map((note) => linkNote(note, index))
}
