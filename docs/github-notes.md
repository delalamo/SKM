# Add notes from GitHub

## One note

On an open issue, post a comment containing your note in a fenced `markdown` or
`md` code block. Start the note with `Title: Note name` or `# Note name` on its
first nonblank line. Bold forms such as `**Title: Note name**` and
`**Title:** Note name` also work.

````text
```markdown
Title: My note

This is my note, in my own words. [@existingCitationKey]
```
````

Then post a separate comment containing only:

```text
/codex add-notes
```

The workflow creates one PR adding `content/notes/My note.md`. The title line
determines the filename (the `.md` suffix is optional) and remains in the copied
text. Use a title without slashes or reserved filename characters such as `:`.
A filename collision fails rather than modifying an existing note.

## Several notes in one PR

Put each note in its own fenced block, in one comment or several comments:

````text
```markdown
Title: First note

This is my first note, in my own words. [@existingCitationKey]
```

```md
# Second note
This is my second note.
```
````

Comment `/codex add-notes` to import all the Markdown blocks from earlier human
comments on that issue into one PR. Bot comments, other code-block languages,
ordinary comment text, and the issue body are ignored. Each note needs a unique
title. Missing titles, duplicate filenames, or malformed Markdown fences stop
the import before any files are written. Title and fence errors identify the
source comment.

Put the opening fence, such as three backticks followed by `markdown`, on its own
line. Do not put the closing backticks on that same line. Tilde fences also work;
use a longer outer fence if your note contains nested code blocks.

The opening fence and its newline are excluded, as is the closing fence line.
The command adds inline wikilinks as described below. Apart from those link
wrappers, it retains the original wording, blank lines, line endings, and trailing
whitespace. It does not summarize, fix spelling, convert citations, or add metadata.
Include any desired figure links, tags, dates, and citations inside the blocks
yourself. Images attached outside a block are not imported. Existing bibliography
keys can be used; this command does not fetch papers or add bibliography entries.

Comments are read in their current, possibly edited form when the workflow runs.
Comments posted after the command are excluded. Later edits are not synced.
Each new command comment requests a fresh PR containing all eligible blocks;
this is not an incremental import. Rerunning the same Actions run reuses its PR
and preserves any reviewer edits. Existing filenames still cause a new request
to fail. There is no fallback to the issue body when no comment blocks are found.

## Automatic inline links and backlinks

The importer matches prose against existing note filenames, frontmatter titles
and aliases, and established display aliases in the vault's wikilinks. It also
links between notes in the same import. Examples:

```text
ESM → [[ESM]]
protein language models → [[Protein language models|protein language models]]
PLMs → [[Protein language models|PLMs]]
```

Matching is case-insensitive and favors longer names. It links every matching
mention, including repeats, so you can remove unwanted links in the PR. It keeps
the original visible wording. Exact filenames take priority over aliases;
ambiguous aliases are skipped. It does not invent targets or link a note to
itself. Matches require whole words: `ESM` does not match inside `ESMFold` or `ESM2`.

Existing links and images, code, citations, formulas, HTML, frontmatter, headings,
and the opening `Title:` line are preserved. The parser identifies prose spans
and inserts links without reformatting the Markdown. This step is deterministic
and requires no OpenAI API key.

Quartz generates backlinks automatically from these outgoing links when the
site builds. The importer does not edit existing notes to insert reciprocal links;
Codex can suggest those separately for review.

## Find related notes

After import, Codex searches the existing vault and posts a separate PR comment
with a copy-ready `#### See also` list for each proposed note. Paste the suggested
entries into that note's See Also section after review. If the section already
exists, the suggestions follow its heading level and omit entries already there.

The search favors broad coverage over a short list: it identifies duplicates,
supporting evidence, qualifications, and complementary ideas, explains the
connections, and labels tentative associations. It also suggests contextual
inline links that name/alias matching missed and useful reciprocal links to add
in existing notes. These semantic suggestions require the OpenAI API key. The
search itself does not edit notes or insert a See Also section automatically.

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
   Importing notes and matching inline links need no model or API key.

These are repository commands implemented by GitHub Actions, using the
[official Codex action](https://developers.openai.com/codex/github-action) for
related-note analysis. Use `/codex` exactly; the separate native `@codex`
integration has its own triggers.

Only users whose current GitHub permission is write, maintain, or admin can
request these operations. The search executes trusted default-branch code,
loads PR blobs as data, and gives Codex a read-only sandbox. Posting the result
runs in a separate job. It never checks out or executes a PR's scripts.

The imported PR links its source issue and command, and lists each note's source
comment, last-edit timestamp, number of added inline links, and separate SHA-256
hashes for the original and linked UTF-8 text. It does not close the source issue
or merge itself.
The import run's summary links to the PR. Errors appear in the Actions run.
If the API key is missing or analysis fails, the imported PR remains available;
configure the key and comment `/codex related-notes` on it to retry.

PRs opened using `GITHUB_TOKEN` do not trigger ordinary `pull_request` workflows.
The import therefore calls related-note analysis explicitly. Existing build and
validation workflows may need a human close/reopen of the PR or an appropriate
manual run before merging. No checks are bypassed by this workflow.

## Local validation

```sh
npm ci --ignore-scripts
node --test tests/github/*.test.mjs
```
