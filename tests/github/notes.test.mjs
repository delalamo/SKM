import test from "node:test"
import assert from "node:assert/strict"
import { importNotes, parseNotes, prepareRelated } from "../../scripts/github/notes.mjs"

function harness({
  permission = "write",
  existing = [],
  tree = [],
  body = "  Exact text\r\n\n",
  title = "A note",
} = {}) {
  const calls = []
  const response = (name, data) => async (args) => {
    calls.push({ name, args })
    return { data }
  }
  const github = {
    rest: {
      repos: {
        getCollaboratorPermissionLevel: response("permission", { permission }),
        get: response("repository", { default_branch: "main" }),
      },
      issues: {
        get: response("issue", {
          title,
          body,
          number: 12,
          state: "open",
          html_url: "https://example.com/12",
          updated_at: "2026-09-28",
        }),
      },
      pulls: {
        list: response("prs", existing),
        create: response("pr", { number: 34, html_url: "https://example.com/34" }),
      },
      git: {
        getRef: response("ref", { object: { sha: "base" } }),
        getCommit: response("commit", { tree: { sha: "tree" } }),
        getTree: response("tree", { tree }),
        createBlob: response("blob", { sha: "blob" }),
        createTree: response("newTree", { sha: "newTree" }),
        createCommit: response("newCommit", { sha: "newCommit" }),
        createRef: response("newRef", {}),
      },
    },
  }
  const outputs = {}
  const core = {
    setOutput: (k, v) => {
      outputs[k] = v
    },
    summary: { addLink() {}, async write() {} },
  }
  const context = {
    repo: { owner: "owner", repo: "repo" },
    actor: "writer",
    issue: { number: 12 },
    payload: { comment: { id: 99, html_url: "https://example.com/comment" } },
  }
  return { github, context, core, calls, outputs }
}

test("single note preserves every character, including CRLF and trailing whitespace", () => {
  const body = "\r\n---\r\ntitle: 'Original'\r\n---\r\n\r\nα **claim** [@key]  \r\n\n"
  assert.deepEqual(parseNotes("Filename", body), [
    { path: "content/notes/Filename.md", content: body },
  ])
})

test("multiple blocks preserve code fences, frontmatter, Unicode and whitespace", () => {
  const a = "---\ntitle: A\n---\n\n```python\nprint('α')\n```  \n\n"
  const b = "\r\n[[A]] [@citation]\r\n"
  const body = `Outside prose\n<!-- note: A.md -->\n${a}<!-- /note -->\n\n<!-- note: B.md -->\r\n${b}<!-- /note -->`
  const expected = [
    { path: "content/notes/A.md", content: a },
    { path: "content/notes/B.md", content: b },
  ]
  assert.deepEqual(parseNotes("ignored", body), expected)
  assert.deepEqual(parseNotes("ignored", body), expected)
})

test("unsafe paths, empty notes, duplicate paths, and malformed blocks fail", () => {
  for (const name of ["../bad", "a/b", "a\\b", ".hidden", "a\nb", "a: b", "a\0b"]) {
    assert.throws(() => parseNotes(name, "text"), /filename/)
  }
  for (const body of [
    "",
    " \n",
    "<!-- note: A -->\nx",
    "<!-- note:A -->\nx",
    "<!-- /note -->",
    "<!-- note: A -->\n<!-- /note -->",
    "<!-- note: A -->\nx\n<!-- note: B -->\ny\n<!-- /note -->\n",
    "<!-- note: A -->\nx\n<!-- /note -->\n<!-- /note -->",
  ]) {
    assert.throws(() => parseNotes("title", body))
  }
  assert.throws(
    () =>
      parseNotes(
        "title",
        "<!-- note: A -->\nx\n<!-- /note -->\n<!-- note: a.md -->\ny\n<!-- /note -->",
      ),
    /Duplicate/,
  )
})

test("import creates only new note blobs with byte-identical text and source attribution", async () => {
  const h = harness()
  await importNotes(h)
  const blob = h.calls.find((c) => c.name === "blob").args
  assert.equal(Buffer.from(blob.content, "base64").toString("utf8"), "  Exact text\r\n\n")
  const entries = h.calls.find((c) => c.name === "newTree").args
  assert.equal(entries.base_tree, "tree")
  assert.deepEqual(entries.tree, [
    { path: "content/notes/A note.md", mode: "100644", type: "blob", sha: "blob" },
  ])
  assert.match(h.calls.find((c) => c.name === "pr").args.body, /https:\/\/example.com\/12/)
  assert.equal(h.outputs.pr, 34)
})

test("readers cannot create branches, invoke Codex preparation, or read issue text", async () => {
  const h = harness({ permission: "read" })
  await assert.rejects(importNotes(h), /Write permission/)
  assert.deepEqual(
    h.calls.map((c) => c.name),
    ["permission"],
  )
  await assert.rejects(prepareRelated({ ...h, number: 34 }), /Write permission/)
  await prepareRelated({ ...h, number: 34, automatic: true })
  assert.equal(h.outputs.ready, undefined)
})

test("repeated delivery reuses a PR without overwriting its branch", async () => {
  const h = harness({ existing: [{ number: 34, state: "open" }] })
  await importNotes(h)
  assert.equal(h.outputs.pr, 34)
  assert.ok(!h.calls.some((c) => c.name === "newRef" || c.name === "blob"))
})

test("closed PRs are never reopened by a retry", async () => {
  const h = harness({ existing: [{ number: 34, state: "closed" }] })
  await importNotes(h)
  assert.equal(h.outputs.pr, undefined)
  assert.ok(!h.calls.some((c) => c.name === "pr"))
})

test("existing names and symlink parents stop import before any writes", async () => {
  for (const tree of [
    [{ path: "content/notes/a NOTE.md", type: "blob" }],
    [{ path: "content/notes", type: "blob", mode: "120000" }],
  ]) {
    const h = harness({ tree })
    await assert.rejects(importNotes(h), /Already exists|Not a directory/)
    assert.ok(!h.calls.some((c) => c.name === "blob"))
  }
})

test("related analysis reads immutable note blobs and ignores non-note changes", async () => {
  const { mkdtemp, readFile, rm } = await import("node:fs/promises")
  const { tmpdir } = await import("node:os")
  const { join } = await import("node:path")
  const h = harness()
  h.github.rest.pulls.get = async () => ({
    data: { number: 34, state: "open", head: { sha: "immutable-head" } },
  })
  h.github.rest.pulls.listFiles = () => {}
  h.github.paginate = async () => [
    { filename: "content/notes/New.md", status: "added", sha: "immutable-blob" },
    { filename: "content/notes/Gone.md", status: "removed" },
    { filename: "scripts/untrusted.sh", status: "modified" },
  ]
  h.github.rest.git.getBlob = async (args) => {
    assert.equal(args.file_sha, "immutable-blob")
    return {
      data: { encoding: "base64", size: 6, content: Buffer.from("Exact\n").toString("base64") },
    }
  }
  const cwd = process.cwd()
  const directory = await mkdtemp(join(tmpdir(), "notes-test-"))
  try {
    process.chdir(directory)
    await prepareRelated({ ...h, number: 34 })
    const result = JSON.parse(await readFile("proposed-notes.json", "utf8"))
    assert.deepEqual(result.notes, [
      { path: "content/notes/New.md", status: "added", content: "Exact\n" },
    ])
    assert.equal(result.head, "immutable-head")
    assert.equal(h.outputs.ready, "true")
  } finally {
    process.chdir(cwd)
    await rm(directory, { recursive: true })
  }
})

test("a truncated repository tree fails before writing blobs", async () => {
  const h = harness()
  h.github.rest.git.getTree = async () => ({ data: { tree: [], truncated: true } })
  await assert.rejects(importNotes(h), /truncated/)
  assert.ok(!h.calls.some((c) => c.name === "blob"))
})
