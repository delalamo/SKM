# Add notes from GitHub

## One note

Create an issue whose title is the desired note filename (the `.md` suffix is
optional), and whose body is the exact Markdown you want to publish. Comment:

```text
/codex add-notes
```

The workflow creates one PR adding `content/notes/<issue title>.md`. It copies the
entire issue body, including frontmatter if supplied, exactly as GitHub returns
it. It adds no metadata and does not summarize, fix spelling, convert citations,
or reformat whitespace. Use a filename without slashes or reserved characters
such as `:`. A filename collision fails rather than modifying an existing note.

## Several notes in one PR

Put named blocks in the issue body:

```markdown
<!-- note: First note.md -->

This is my first note, in my own words. [@existingCitationKey]
<!-- /note -->

<!-- note: Second note.md -->

---

title: Second note
tags:

- prediction/variant-effects

---

This is my second note.
<!-- /note -->
```

Comment `/codex add-notes` to import all the blocks. Each opening marker and its
newline are excluded, as is the closing marker line. Every character between
those lines is retained, including blank lines and the final newline. Text
outside the blocks is excluded. These marker lines are reserved delimiters and
cannot appear literally inside a note. Put any desired title, tags, dates, and
citations inside the blocks yourself. Existing bibliography keys can be used;
this command does not fetch papers or add bibliography entries.

The source is the current **issue body**, not comments or linked papers. For an
existing paper issue, wrap only your intended note text in blocks. The command
must be the entire comment, with no surrounding text. Issue edits made after the
import are not synced. Each new command comment requests a fresh PR; rerunning
the same Actions run reuses its PR and preserves any reviewer edits. Existing
filenames still cause a new request to fail.

## Find related notes

After import, Codex searches the existing vault and posts a separate PR comment
with up to five useful connections per proposed note. It identifies duplicates,
supporting evidence, qualifications, and complementary ideas, with links and
suggested wikilinks. It does not edit any note.

The search also runs when a writer opens or updates a note PR. To request it on
an existing PR, comment:

```text
/codex related-notes
```

The search reads all added or modified Markdown notes in that PR. Repeated runs
update one bot comment. Results for a commit that changed during analysis are
discarded. Automatic events from users without repository write access are
skipped; a writer can explicitly request analysis on their PR.

## Setup

1. Merge these workflow files and scripts into the repository's default branch.
   Issue comment workflows become available there.
2. In **Settings → Actions → General → Workflow permissions**, enable **Allow
   GitHub Actions to create and approve pull requests**. The import job requests
   contents and pull-request write access explicitly.
3. Add `OPENAI_API_KEY` under **Settings → Secrets and variables → Actions** to
   enable the related-note search. This uses the OpenAI API and its billing.
   Importing notes itself needs no model or API key.

These are repository commands implemented by GitHub Actions, using the
[official Codex action](https://developers.openai.com/codex/github-action) for
related-note analysis. Use `/codex` exactly; the separate native `@codex`
integration has its own triggers.

Only users whose current GitHub permission is write, maintain, or admin can
request these operations. The search executes trusted default-branch code,
loads PR blobs as data, and gives Codex a read-only sandbox. Posting the result
runs in a separate job. It never checks out or executes a PR's scripts.

The imported PR links its source issue and command and includes SHA-256 hashes
of the copied UTF-8 text. It does not close the source issue or merge itself.
The import run's summary links to the PR. Errors appear in the Actions run.
If the API key is missing or analysis fails, the imported PR remains available;
configure the key and comment `/codex related-notes` on it to retry.

PRs opened using `GITHUB_TOKEN` do not trigger ordinary `pull_request` workflows.
The import therefore calls related-note analysis explicitly. Existing build and
validation workflows may need a human close/reopen of the PR or an appropriate
manual run before merging. No checks are bypassed by this workflow.

## Local validation

```sh
node --test tests/github/notes.test.mjs
```
