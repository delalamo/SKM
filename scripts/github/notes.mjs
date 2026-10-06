import { createHash } from "node:crypto"
import { writeFile } from "node:fs/promises"

export function notePath(name) {
  if (!name.endsWith(".md")) name += ".md"
  if (
    name.startsWith(".") ||
    name.trim() !== name ||
    /[/\\<>:"|?*\x00-\x1f\x7f]/.test(name) ||
    Buffer.byteLength(name) > 240
  )
    throw new Error("Use a plain note filename, without directories or reserved characters.")
  return `content/notes/${name}`
}

function noteTitle(content) {
  let first = content.trimStart().split(/\r?\n/, 1)[0].trim()
  if (first.startsWith("**") && first.endsWith("**")) first = first.slice(2, -2)
  const title = /^(?:\*\*Title:\*\*\s*|Title:\s*|#\s+)(.+)$/i.exec(first)?.[1].trim()
  if (!title) throw new Error("Start each Markdown block with Title: Note name or # Note name.")
  return title
}

export function parseNotes(body) {
  const notes = []
  let fence
  for (const line of (body || "").matchAll(/[^\n]*(?:\n|$)/g)) {
    const text = line[0].replace(/\r?\n$/, "")
    if (fence) {
      if (new RegExp(`^ {0,3}${fence.character}{${fence.length},}[ \\t]*$`).test(text)) {
        if (fence.markdown) {
          const content = body.slice(fence.start, line.index)
          if (!content.trim()) throw new Error("Markdown note blocks cannot be empty.")
          notes.push({ path: notePath(noteTitle(content)), content })
        }
        fence = undefined
      }
      continue
    }
    const opening = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(text)
    if (!opening) continue
    const language = opening[2].trim()
    if (/^(markdown|md)\b/i.test(language) && !/^(markdown|md)$/i.test(language)) {
      throw new Error("Use an opening ```markdown or ```md fence on its own line.")
    }
    // Track other code fences too, so Markdown examples nested inside them are ignored.
    if (opening[1][0] === "`" && language.includes("`")) continue
    fence = {
      character: opening[1][0],
      length: opening[1].length,
      markdown: /^(markdown|md)$/i.test(language),
      start: line.index + line[0].length,
    }
  }
  if (fence?.markdown) throw new Error("Close each Markdown note block with a matching fence.")
  return notes
}

export function notesFromComments(comments, commandId) {
  const notes = []
  for (const comment of comments.filter((c) => c.id < commandId).sort((a, b) => a.id - b.id)) {
    if (comment.user?.type !== "User" || comment.user.login.endsWith("[bot]")) continue
    try {
      notes.push(
        ...parseNotes(comment.body).map((note) => ({
          ...note,
          source: comment.html_url,
          updatedAt: comment.updated_at,
        })),
      )
    } catch (error) {
      throw new Error(`${comment.html_url}: ${error.message}`)
    }
  }
  if (!notes.length) throw new Error("No fenced Markdown notes found in earlier issue comments.")
  const names = notes.map((n) => n.path.normalize("NFC").toLowerCase())
  if (new Set(names).size !== names.length) {
    throw new Error("Duplicate note filenames in issue comments. Give each note a unique title.")
  }
  return notes
}

export async function canWrite(github, repo, username) {
  const { data } = await github.rest.repos.getCollaboratorPermissionLevel({ ...repo, username })
  return ["admin", "maintain", "write"].includes(data.permission)
}

export async function importNotes({ github, context, core }) {
  const repo = context.repo
  if (!(await canWrite(github, repo, context.actor)))
    throw new Error("Write permission is required.")
  const { data: issue } = await github.rest.issues.get({
    ...repo,
    issue_number: context.issue.number,
  })
  if (issue.pull_request || issue.state !== "open") throw new Error("Use an open issue.")
  // A repeated delivery or re-run finds the same PR and never resets reviewer edits.
  const branch = `codex/issue-${issue.number}-comment-${context.payload.comment.id}`
  const existing = await github.rest.pulls.list({
    ...repo,
    head: `${repo.owner}:${branch}`,
    state: "all",
  })
  if (existing.data.length) {
    if (existing.data[0].state === "open") core.setOutput("pr", existing.data[0].number)
    return
  }
  const comments = await github.paginate(github.rest.issues.listComments, {
    ...repo,
    issue_number: issue.number,
    per_page: 100,
  })
  const notes = notesFromComments(comments, context.payload.comment.id)
  const { data: repository } = await github.rest.repos.get(repo)
  const base = repository.default_branch
  const { data: ref } = await github.rest.git.getRef({ ...repo, ref: `heads/${base}` })
  const { data: commit } = await github.rest.git.getCommit({ ...repo, commit_sha: ref.object.sha })
  const { data: tree } = await github.rest.git.getTree({
    ...repo,
    tree_sha: commit.tree.sha,
    recursive: "true",
  })
  if (tree.truncated)
    throw new Error("Repository tree is truncated; cannot safely check filename collisions.")
  const paths = new Set(tree.tree.map((t) => t.path.normalize("NFC").toLowerCase()))
  for (const note of notes) {
    const parts = note.path.split("/")
    for (let i = 1; i < parts.length; i++) {
      const parent = parts.slice(0, i).join("/")
      const entry = tree.tree.find((t) => t.path === parent)
      if (entry && entry.type !== "tree") throw new Error(`Not a directory: ${parent}`)
    }
    if (paths.has(note.path.normalize("NFC").toLowerCase()))
      throw new Error(`Already exists: ${note.path}`)
  }
  const entries = []
  for (const note of notes) {
    const { data: blob } = await github.rest.git.createBlob({
      ...repo,
      content: Buffer.from(note.content).toString("base64"),
      encoding: "base64",
    })
    entries.push({ path: note.path, mode: "100644", type: "blob", sha: blob.sha })
  }
  const { data: newTree } = await github.rest.git.createTree({
    ...repo,
    base_tree: commit.tree.sha,
    tree: entries,
  })
  const { data: newCommit } = await github.rest.git.createCommit({
    ...repo,
    message: `Add verbatim notes from comments on issue #${issue.number}`,
    tree: newTree.sha,
    parents: [ref.object.sha],
  })
  try {
    await github.rest.git.createRef({ ...repo, ref: `refs/heads/${branch}`, sha: newCommit.sha })
  } catch (error) {
    if (error.status !== 422) throw error
    // Resume only if a previous interrupted run created exactly this content.
    const { data: oldRef } = await github.rest.git.getRef({ ...repo, ref: `heads/${branch}` })
    const { data: oldCommit } = await github.rest.git.getCommit({
      ...repo,
      commit_sha: oldRef.object.sha,
    })
    if (oldCommit.tree.sha !== newTree.sha)
      throw new Error("Import branch exists with different content; it was preserved.")
  }
  const hashes = notes
    .map(
      (n) =>
        `- \`${n.path}\`: \`${createHash("sha256").update(n.content).digest("hex")}\` — [source comment](${n.source}), last updated ${n.updatedAt}`,
    )
    .join("\n")
  const { data: pr } = await github.rest.pulls.create({
    ...repo,
    head: branch,
    base,
    title: `Add notes from #${issue.number}: ${issue.title}`.slice(0, 240),
    body: `Copies fenced Markdown notes verbatim from comments on ${issue.html_url}.\n\nRequested by ${context.payload.comment.html_url}.\n\nNo summarization, formatting, metadata, citation conversion, or related links were added. Related-note suggestions are posted separately.\n\n### Source comments and imported UTF-8 SHA-256 checksums\n\n${hashes}`,
  })
  core.setOutput("pr", pr.number)
  core.summary.addLink(`Note PR #${pr.number}`, pr.html_url)
  await core.summary.write()
}

export async function prepareRelated({ github, context, core, number, automatic = false }) {
  const repo = context.repo
  if (!(await canWrite(github, repo, context.actor))) {
    if (automatic) return
    throw new Error("Write permission is required.")
  }
  const { data: pr } = await github.rest.pulls.get({ ...repo, pull_number: Number(number) })
  if (pr.state !== "open") throw new Error("The PR is closed.")
  const files = await github.paginate(github.rest.pulls.listFiles, {
    ...repo,
    pull_number: pr.number,
    per_page: 100,
  })
  if (files.length >= 3000) throw new Error("PR file list may be truncated.")
  const candidates = files.filter(
    (f) =>
      f.filename.startsWith("content/notes/") &&
      f.filename.endsWith(".md") &&
      f.status !== "removed",
  )
  if (!candidates.length) return
  const notes = []
  for (const file of candidates) {
    // Read immutable blobs through the API. Never check out or execute PR code.
    const { data: blob } = await github.rest.git.getBlob({ ...repo, file_sha: file.sha })
    if (blob.encoding !== "base64" || blob.size > 200_000)
      throw new Error("Unsupported or oversized note blob.")
    notes.push({
      path: file.filename,
      status: file.status,
      content: Buffer.from(blob.content, "base64").toString("utf8"),
    })
  }
  await writeFile(
    "proposed-notes.json",
    JSON.stringify(
      { repository: `${repo.owner}/${repo.repo}`, pr: pr.number, head: pr.head.sha, notes },
      null,
      2,
    ),
  )
  core.setOutput("pr", pr.number)
  core.setOutput("sha", pr.head.sha)
  core.setOutput("ready", "true")
}
