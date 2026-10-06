import test from "node:test"
import assert from "node:assert/strict"
import {
  importNotes,
  notesFromComments,
  parseNotes,
  prepareRelated,
} from "../../scripts/github/notes.mjs"

function comment(id, body, type = "User") {
  return {
    id,
    body,
    user: { login: type === "Bot" ? "codex[bot]" : "writer", type },
    html_url: `https://example.com/12#issuecomment-${id}`,
    updated_at: "2026-10-06T12:00:00Z",
  }
}

const exactNote = "**Title: A note**\r\n\r\nα **claim** [@key]  \r\n\n"

function harness({
  permission = "write",
  existing = [],
  tree = [],
  comments = [comment(50, `Outside prose\n\`\`\`markdown\r\n${exactNote}\`\`\`\nIgnored`)],
  body = "Issue metadata that must never be imported",
  title = "Paper title, not a note filename",
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
        listComments() {},
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
  github.paginate = async (method, args) => {
    assert.equal(method, github.rest.issues.listComments)
    calls.push({ name: "comments", args })
    return comments
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

test("Markdown fences preserve all inner characters, including CRLF and trailing whitespace", () => {
  assert.deepEqual(parseNotes(`Outside\n\`\`\`markdown\r\n${exactNote}\`\`\`\nOutside`), [
    { path: "content/notes/A note.md", content: exactNote },
  ])
})

test("multiple blocks support md, tilde fences and longer fences around nested code", () => {
  const a = "Title: A.md\n\n```python\nprint('α')\n```  \n\n"
  const b = "\r\n# B\r\n[[A]] [@citation]\r\n"
  const body = `Outside prose\n\`\`\`\`markdown\n${a}\`\`\`\`\n\n~~~md\r\n${b}~~~~`
  const expected = [
    { path: "content/notes/A.md", content: a },
    { path: "content/notes/B.md", content: b },
  ]
  assert.deepEqual(parseNotes(body), expected)
})

test("plain, bold and heading titles name notes without changing the title line", () => {
  for (const title of ["Title: Example", "**Title: Example**", "**Title:** Example", "# Example"]) {
    const content = `${title}\nText\n`
    assert.deepEqual(parseNotes(`\`\`\`MD\n${content}\`\`\``), [
      { path: "content/notes/Example.md", content },
    ])
  }
})

test("ordinary prose and other code blocks are ignored, including nested Markdown examples", () => {
  assert.deepEqual(parseNotes("# Not a note\nText"), [])
  assert.deepEqual(parseNotes("````text\n```markdown\n# Example\n```\n````"), [])
  assert.deepEqual(parseNotes("```python\nprint('x')\n```"), [])
})

test("unsafe paths, empty notes, missing titles and malformed Markdown fences fail", () => {
  for (const name of ["../bad", "a/b", "a\\b", ".hidden", "a: b", "a\0b"]) {
    assert.throws(() => parseNotes(`\`\`\`markdown\nTitle: ${name}\nText\n\`\`\``), /filename/)
  }
  for (const body of [
    "```markdown\n```",
    "```markdown\n \n```",
    "```markdown\nText without a title\n```",
    "```markdown\nTitle: \n```",
    "```markdown\n# A\nUnclosed",
    "````markdown\n# A\n```",
    "```markdown```\nTitle: A\nText\n```",
  ]) {
    assert.throws(() => parseNotes(body))
  }
})

test("duplicate names across comments fail, including case and Unicode equivalents", () => {
  for (const titles of [
    ["A", "a.md"],
    ["Café", "Cafe\u0301"],
  ]) {
    assert.throws(
      () =>
        notesFromComments(
          titles.map((title, i) => comment(i, `\`\`\`md\n# ${title}\nText\n\`\`\``)),
          99,
        ),
      /Duplicate/,
    )
  }
})

test("only earlier human comments are selected and each block retains its source", () => {
  const block = (title) => `\`\`\`markdown\n# ${title}\nText\n\`\`\``
  const notes = notesFromComments(
    [
      comment(101, block("Future")),
      comment(99, block("Command")),
      comment(51, block("B")),
      comment(50, block("A")),
      comment(49, block("Bot"), "Bot"),
    ],
    99,
  )
  assert.deepEqual(
    notes.map((n) => n.path),
    ["content/notes/A.md", "content/notes/B.md"],
  )
  assert.equal(notes[0].source, "https://example.com/12#issuecomment-50")
  assert.equal(notes[0].updatedAt, "2026-10-06T12:00:00Z")
})

test("missing blocks and malformed source comments have actionable errors", () => {
  assert.throws(() => notesFromComments([comment(50, "Plain text")], 99), /No fenced Markdown/)
  assert.throws(
    () => notesFromComments([comment(50, "```markdown```\n# A\n```")], 99),
    /issuecomment-50: Use an opening/,
  )
})

test("import creates only new note blobs with byte-identical text and source attribution", async () => {
  const h = harness()
  await importNotes(h)
  const blob = h.calls.find((c) => c.name === "blob").args
  assert.equal(Buffer.from(blob.content, "base64").toString("utf8"), exactNote)
  const entries = h.calls.find((c) => c.name === "newTree").args
  assert.equal(entries.base_tree, "tree")
  assert.deepEqual(entries.tree, [
    { path: "content/notes/A note.md", mode: "100644", type: "blob", sha: "blob" },
  ])
  assert.match(h.calls.find((c) => c.name === "pr").args.body, /https:\/\/example.com\/12/)
  assert.match(h.calls.find((c) => c.name === "pr").args.body, /issuecomment-50/)
  assert.match(h.calls.find((c) => c.name === "pr").args.body, /2026-10-06T12:00:00Z/)
  assert.equal(h.calls.find((c) => c.name === "comments").args.per_page, 100)
  assert.equal(h.outputs.pr, 34)
})

test("multiple comments become one PR; the issue body never becomes a note", async () => {
  const h = harness({
    body: "```markdown\n# Wrong source\nText\n```",
    comments: [comment(50, "```markdown\n# A\nText\n```"), comment(51, "```md\n# B\nText\n```")],
  })
  await importNotes(h)
  assert.deepEqual(
    h.calls.find((c) => c.name === "newTree").args.tree.map((f) => f.path),
    ["content/notes/A.md", "content/notes/B.md"],
  )
  assert.equal(h.calls.filter((c) => c.name === "pr").length, 1)
})

test("missing or malformed comment notes fail before any writes, without body fallback", async () => {
  for (const comments of [[], [comment(50, "```markdown\nNo title\n```")]]) {
    const h = harness({ comments, body: "```markdown\n# Body note\nText\n```" })
    await assert.rejects(importNotes(h), /No fenced Markdown|Start each Markdown/)
    assert.ok(!h.calls.some((c) => c.name === "blob" || c.name === "newRef" || c.name === "pr"))
  }
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
  const h = harness({ existing: [{ number: 34, state: "open" }], comments: [] })
  await importNotes(h)
  assert.equal(h.outputs.pr, 34)
  assert.ok(!h.calls.some((c) => c.name === "newRef" || c.name === "blob" || c.name === "comments"))
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
