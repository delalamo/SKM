#!/usr/bin/env node

import fs from "node:fs/promises"
import path from "node:path"

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..")
const notesDir = path.join(repoRoot, "content", "notes")
const mocsDir = path.join(repoRoot, "content", "MOCs")
const tagsDir = path.join(repoRoot, "content", "tags")

const GENERATED_MARKER = "<!-- generated -->"
const EXCLUDED_ROOTS = new Set(["citation-fix", "citation-needed"])
const STEM_TO_ROOT = new Map([
  ["Developability", "antibody-developability"],
  ["Predicted aligned error", "pae"],
  ["Stability and thermostability", "thermostability"],
])

function slugifyTitle(title) {
  return title
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/&/g, " and ")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-{2,}/g, "-")
    .toLowerCase()
}

function splitFrontmatter(text) {
  const match = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/)
  if (!match) return { body: text, frontmatter: null }

  return {
    body: text.slice(match[0].length),
    frontmatter: match[1],
  }
}

function parseTags(frontmatter) {
  if (!frontmatter) return []

  const lines = frontmatter.split("\n")
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index]

    if (/^tags:\s*$/.test(line)) {
      const tags = []
      for (let child = index + 1; child < lines.length; child += 1) {
        const childLine = lines[child]
        const match = childLine.match(/^\s*-\s*(.+)\s*$/)
        if (!match) break
        tags.push(match[1].trim().replace(/^['"]|['"]$/g, ""))
      }
      return tags
    }

    const inlineList = line.match(/^tags:\s*\[(.*)\]\s*$/)
    if (inlineList) {
      return inlineList[1]
        .split(",")
        .map((tag) => tag.trim().replace(/^['"]|['"]$/g, ""))
        .filter(Boolean)
    }

    const inline = line.match(/^tags:\s*(.+)\s*$/)
    if (inline && inline[1].trim() !== "") {
      return inline[1]
        .split(",")
        .map((tag) => tag.trim().replace(/^['"]|['"]$/g, ""))
        .filter(Boolean)
    }
  }

  return []
}

function stripTagsField(frontmatter) {
  if (!frontmatter) return ""

  const stripped = []
  const lines = frontmatter.split("\n")

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index]

    if (/^tags:\s*$/.test(line)) {
      while (index + 1 < lines.length && /^\s*-\s+/.test(lines[index + 1])) {
        index += 1
      }
      continue
    }

    if (/^tags:\s*(\[[^\]]*\]|.*)\s*$/.test(line)) {
      continue
    }

    stripped.push(line)
  }

  return stripped
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

function extractTitle(frontmatter) {
  if (!frontmatter) return null

  const match = frontmatter.match(/^title:\s*(.+)\s*$/m)
  if (!match) return null
  return match[1].trim().replace(/^['"]|['"]$/g, "")
}

function ensureTitleAlias(frontmatter) {
  const title = extractTitle(frontmatter)
  if (!title) return frontmatter

  const lines = frontmatter.split("\n")
  const aliasBlockIndex = lines.findIndex((line) => /^aliases:\s*$/.test(line))

  if (aliasBlockIndex !== -1) {
    const aliases = []
    let insertAt = aliasBlockIndex + 1
    while (insertAt < lines.length) {
      const match = lines[insertAt].match(/^\s*-\s*(.+)\s*$/)
      if (!match) break
      aliases.push(match[1].trim().replace(/^['"]|['"]$/g, ""))
      insertAt += 1
    }

    if (!aliases.includes(title)) {
      lines.splice(insertAt, 0, `  - ${title}`)
    }
    return lines.join("\n")
  }

  const titleIndex = lines.findIndex((line) => /^title:\s*/.test(line))
  if (titleIndex === -1) return frontmatter

  lines.splice(titleIndex + 1, 0, "aliases:", `  - ${title}`)
  return lines.join("\n")
}

async function collectNoteRoots() {
  const roots = new Set()
  const entries = await fs.readdir(notesDir)

  for (const entry of entries) {
    if (!entry.endsWith(".md")) continue
    const text = await fs.readFile(path.join(notesDir, entry), "utf8")
    const { frontmatter } = splitFrontmatter(text)

    for (const tag of parseTags(frontmatter)) {
      const root = tag.split("/", 1)[0]
      if (!root || EXCLUDED_ROOTS.has(root) || root.includes(":")) continue
      roots.add(root)
    }
  }

  return roots
}

function resolveRoot(stem, frontmatterTags, noteRoots) {
  const taggedRoot = frontmatterTags.find((tag) => noteRoots.has(tag) && !EXCLUDED_ROOTS.has(tag))
  if (taggedRoot) return taggedRoot

  if (STEM_TO_ROOT.has(stem)) return STEM_TO_ROOT.get(stem)

  const normalizedStem = slugifyTitle(stem)
  if (noteRoots.has(normalizedStem)) return normalizedStem

  return null
}

function composeFrontmatter(frontmatter) {
  if (!frontmatter || frontmatter.trim() === "") return ""
  return `---\n${frontmatter.trim()}\n---\n\n`
}

function extractProse(body) {
  return body.split(GENERATED_MARKER, 1)[0].trim()
}

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true })
}

async function main() {
  const dryRun = process.argv.includes("--dry-run")
  const noteRoots = await collectNoteRoots()
  await ensureDir(tagsDir)

  const entries = await fs.readdir(mocsDir)
  const migrated = []
  const removed = []

  for (const entry of entries.sort()) {
    if (!entry.endsWith(".md")) continue

    const mocPath = path.join(mocsDir, entry)
    const text = await fs.readFile(mocPath, "utf8")
    const { body, frontmatter } = splitFrontmatter(text)
    const mocTags = parseTags(frontmatter)
    const stem = path.basename(entry, ".md")
    const root = resolveRoot(stem, mocTags, noteRoots)

    if (!root || EXCLUDED_ROOTS.has(root)) continue

    const prose = extractProse(body)
    const targetPath = path.join(tagsDir, `${root}.md`)
    const existingTarget = await fs
      .readFile(targetPath, "utf8")
      .then((content) => splitFrontmatter(content))
      .catch(() => null)

    if (prose !== "") {
      const targetFrontmatter = ensureTitleAlias(
        stripTagsField(existingTarget?.frontmatter ?? frontmatter),
      )
      const output = `${composeFrontmatter(targetFrontmatter)}${prose}\n`
      if (!dryRun) {
        await fs.writeFile(targetPath, output)
      }
      migrated.push(`${path.relative(repoRoot, mocPath)} -> ${path.relative(repoRoot, targetPath)}`)
    }

    if (!dryRun) {
      await fs.rm(mocPath)
    }
    removed.push(path.relative(repoRoot, mocPath))
  }

  if (dryRun) {
    console.log("Dry run only. No files were written or removed.")
  }
  console.log(`Migrated ${migrated.length} MOC page(s) into content/tags:`)
  for (const entry of migrated) console.log(`  ${entry}`)
  console.log(`Removed ${removed.length} migrated MOC page(s).`)
}

main().catch((error) => {
  console.error(error)
  process.exitCode = 1
})
