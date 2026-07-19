# Repository instructions

## Prime directive: preserve the garden's existing voice and structure

This repository is an established personal zettelkasten, not a blank documentation project. Its
existing stylistic choices are authoritative. Respect them even when another Markdown style would
also be valid.

- Make the smallest change that satisfies the request.
- Read the entire target note and a few nearby notes of the same kind before writing.
- Match the target file's heading depth, spacing, bullet marker, emphasis, terminology, and level of
  detail. Local precedent outranks generic style advice.
- Do not bulk copyedit, reformat, rename, reorganize, retag, or "clean up" existing notes unless the
  user explicitly requests that work.
- Do not silently turn terse notes into tutorials or polished essays. The terse, technical,
  claim-first voice is intentional.
- Existing inconsistencies are not permission to normalize unrelated text. In particular, do not
  churn heading levels, list markers, date quoting, image captions, or BibTeX field formatting.
- Preserve the author's scientific meaning, uncertainty, and qualifications. Never strengthen a
  claim beyond its evidence, invent a source, or fill a factual gap from assumption.
- Avoid renaming notes, tags, assets, or citation keys. Those names participate in links and stable
  URLs. If a rename is explicitly required, update every backlink/reference and add an alias or
  redirect where appropriate.

## What lives where

- `content/notes/` contains the authored zettelkasten. These files are the main product.
- `content/tags/` contains curated prose for selected native Quartz tag pages. Quartz generates the
  lists of tagged notes; these files are not hand-maintained indexes.
- `content/assets/` contains note images and other Obsidian attachments.
- `content/index.md` is the public landing page.
- `bibliography.bib` is the single bibliography for authored content.
- `quartz.config.ts`, `quartz.layout.ts`, and selected files under `quartz/` customize the Quartz 4
  site and its rendering.
- `scripts/` contains maintenance and one-time migration utilities. Several scripts document older
  citation or MOC workflows and are not the normal authoring path.
- `docs/` and most of `quartz/` are upstream Quartz source/documentation, not zettelkasten content.
- `public/`, `.quartz-cache/`, `node_modules/`, and Python bytecode are generated. Never edit or
  commit generated output in place of its source.

The root Obsidian vault is configured to expose `content/`, create notes in `content/notes/`, store
attachments in `content/assets/`, and update links when files move. Keep authored Markdown usable in
both Obsidian and Quartz.

## Zettelkasten conventions

### Scope and filenames

There are two common note shapes:

1. **Atomic finding notes** use a sentence-like filename that states one scientific result, for
   example `AlphaFold3 learns intramolecular interactions faster than intermolecular interactions.md`.
   Keep these focused on one defensible claim.
2. **Concept notes** use a canonical term or method name, for example `Boltzmann distribution.md` or
   `Straight-through estimator.md`. They define the concept briefly and may collect examples,
   methods, or mentions.

Do not add an H1 to a note. Quartz supplies the page title from frontmatter or the filename. Prefer a
new atomic note and links to related ideas over appending an unrelated mini-essay to an existing
note.

### Frontmatter

Authored notes normally begin with YAML frontmatter. A typical new finding note looks like:

```yaml
---
tags:
  - protein-design/design
created: "2026-07-19"
modified: "2026-07-19T10:07:27"
---
```

- Use existing lowercase kebab-case tags and established slash hierarchies such as
  `structure-prediction/limitations`. Do not casually invent a competing spelling or taxonomy.
- A slash tag belongs both to its direct page and its root grouping. The custom tag page code groups
  notes by the direct child segment.
- Do not write inline hashtags. Tags live in frontmatter.
- `title` is optional when the filename already provides the intended title. It is common on concept
  notes and required when the displayed title should differ from the filename/slug.
- Put genuine synonyms in an `aliases` YAML list. Do not add aliases merely to repeat a title unless
  matching an existing tag-page pattern.
- Preserve `summary` and `publicationHistory` fields. `publicationHistory` maps publication dates to
  external URLs and is not a general references field.
- Preserve `created` when editing. Update `modified` for a substantive note edit. The configured
  pre-commit hook restamps staged files under `content/notes/`; it does not justify changing dates in
  unrelated files.
- For new metadata, prefer quoted ISO dates. Do not normalize older quoted/unquoted dates as drive-by
  cleanup.

### Prose and section structure

The house voice is concise, factual, technically literate, and evidence-led. It assumes familiarity
with protein science and machine learning; `content/index.md` explicitly says the garden is not
introductory or comprehensive.

- Lead finding notes with the main claim in bold, then place its citation immediately after it.
- Keep useful qualifiers, counterexamples, experimental conditions, numerical results, and limits.
  The notes often contrast studies rather than forcing a false consensus.
- Prefer direct scientific language over scene-setting, motivational prose, rhetorical conclusions,
  or generic "importance" paragraphs.
- Use the terminology already present in linked notes, including established abbreviations such as
  PLM, MSA, CDRH3, pLDDT, PAE, ipTM, and ddG.
- Most atomic notes use optional fourth-level sections in this order:

  ```markdown
  #### Summary

  **The central finding** [@citekey]. Supporting detail and qualifications.

  #### Details

  Additional evidence when needed.

  #### Figures

  ![[asset.png]]

  _Figure 2 from [@citekey]_

  #### See also

  - [[Related note]]
  ```

- Omit sections that add no value. Short concept notes often contain only one definition paragraph;
  short finding notes may contain only `#### Summary`.
- `#### Summary`, `#### Details`, `#### Figures`, and `#### See also` are the dominant current form.
  Some established notes use `##`; preserve that local choice rather than mechanically converting it.
- Do not add a manual `References` section. The citation plugin renders one automatically.
- Both `*` and `-` list markers exist. Continue the marker already used in the file. For a new file,
  use one marker consistently.
- Use Markdown tables only when the tabular comparison itself matters; retain quantitative precision
  and existing emphasis within cells.
- Use fenced code blocks with a language. Keep commands minimal and reproducible.
- Use `$...$` and `$$...$$` for KaTeX math. Follow the notation of the source note and define symbols
  when the surrounding note does so.

### Wikilinks and knowledge-graph structure

Internal links are part of the argument, not decorative cross-references.

- Use Obsidian wikilinks: `[[Exact note title]]`, `[[Exact note title|display text]]`, and
  `[[Exact note title#Section|display text]]`.
- When linking a curated tag page, the existing style often uses its slug as the target and natural
  prose as the alias, for example `[[protein-language-models|protein language models]]`.
- Match the exact existing target spelling and case. Search before creating a new concept note or link;
  Quartz is configured with shortest-path link resolution, but ambiguity is still undesirable.
- Link meaningful concepts at their first useful occurrence. Do not replace clear prose with an
  excessive chain of links, and do not add a redundant "See also" entry when the relationship is not
  useful.
- Do not reintroduce generated MOC files. The repository migrated from `content/MOCs/` to native,
  hierarchical tag pages.

### Figures and assets

- Put note attachments in `content/assets/` and use the Obsidian form `![[filename.ext]]`. This is the
  prevailing format and renders in both Obsidian and Quartz.
- An optional width uses `![[filename.ext|600]]`.
- Keep filenames exact, including spaces, hyphens, capitalization, and extension. Do not rename an
  existing asset without updating all embeds.
- Put a short italic source line directly below the relevant figure or group of figures. Established
  forms include `*Ref [@key]*`, `*Figure S4E from [@key]*`, and `*Figures from [@key]*`.
- Do not add an image without an attributable source when the image comes from a paper. Do not invent
  a figure number.
- Reuse an identical tracked asset rather than committing a duplicate; CI checks byte-identical files
  and Markdown duplicates.

## Bibliography and citations

The active citation system is centralized and bibliography-backed:

- `quartz.config.ts` loads `bibliography.bib` through `Plugin.Citations`.
- The configured CSL style is Vancouver, citations are linked, and per-note bibliographies are not
  suppressed. Rendered citations are compact superscript numbers, with a generated References block.
- The custom citation transformer and `quartz/styles/custom.scss` deliberately handle citations inside
  bold/italic text, citation link numbering, and bibliography presentation. Do not remove that logic as
  an apparent simplification.

Use Pandoc citation syntax in authored Markdown:

```markdown
**A supported claim** [@abramson2024].
**A claim supported by several papers** [@qiao2022; @krishna2024].
_Figure from [@matthews2023]_
```

- Separate multiple keys with semicolons: `[@first; @second]`.
- Place a citation next to the exact claim or figure it supports, usually before the sentence's final
  punctuation as in the existing notes.
- Reuse a bibliography entry when the DOI/title is already present. Search both the citekey and DOI
  before adding anything.
- Citekeys are lowercase and normally begin with first-author surname plus year, with an economical
  disambiguator when needed: `chen2024b`, `jing2026switchcraft`, `liu2026robust`.
- When adding an entry, append a complete BibTeX record that follows nearby records and includes stable
  DOI/URL metadata when available. Do not reorder or normalize the entire bibliography; its older
  normalized region and newer appended records have intentionally been left without wholesale churn.
- Never cite a key that is absent from `bibliography.bib`.
- Do not author paper citations as Markdown footnote definitions, raw DOI URLs, author-year DOI
  wikilinks, or a hand-written reference list. Those are legacy representations.

The scripts named `format_notes.py`, `fix_inline_citations.py`, `migrate_*citations*`,
`reconcile_bibliography.py`, and `audit_citation_migration_against_main.py` exist for earlier bulk
migrations or audits. They can rewrite hundreds of files and some contact external metadata services.
Do not run them during ordinary note editing. Use dry-run/audit modes first and obtain an explicit
request before any repository-wide migration.

## Tag pages

`content/tags/` contains curated introductions for selected tag roots, not one file for every tag.

- A tag page normally has a human-readable `title`, an alias, and dates, followed by concise overview
  prose, definitions, methods, or examples.
- Do not hand-write lists of every tagged note. `TagContent.tsx` discovers them and, for hierarchical
  tags, groups them into `General` and direct-child sections.
- An otherwise empty curated tag page may retain the existing auto-generated-info callout. Do not add
  filler prose just to remove it.
- Do not create a new tag page or reorganize the taxonomy unless the requested content genuinely needs
  a curated root or child page.

## Quartz implementation conventions

Treat the site as a customized Quartz 4 installation rather than generic application code.

- Preserve the transformer ordering in `quartz.config.ts` unless the task specifically requires a
  pipeline change. Obsidian-flavored Markdown, GFM, citations, links, descriptions, and KaTeX interact.
- Preserve the content-page layout: title/meta/tags, explorer and search, local graph, table of
  contents, backlinks, and homepage `Recently Updated`/`Recently Added` lists.
- Preserve hierarchical tag grouping and the distinction between created and modified sorting.
- TypeScript is strict and formatted with Prettier: 2 spaces, double quotes, no semicolons, trailing
  commas, and a 100-column width. Follow surrounding Preact/Quartz component patterns.
- Keep tests close to the implementation and use the existing `node:test`/`node:assert` style.
- Do not fork or broadly rewrite upstream Quartz code for a content-only request.
- Do not run a repository-wide formatter merely to format a touched file; that risks unrelated note
  churn.

## Validation

Validate in proportion to the change and inspect the final diff for stylistic drift.

For note, tag, bibliography, or asset changes:

1. Confirm every new wikilink target and image embed resolves with exact spelling.
2. Confirm every `@citekey` exists in `bibliography.bib` and clustered citations use semicolons.
3. Run `python3 scripts/check_duplicate_files.py` when adding or moving notes/assets.
4. Run `npx quartz build` for meaningful content, bibliography, tag, layout, or rendering changes.

For TypeScript, SCSS, configuration, or component changes:

1. Run `npm run check`.
2. Run `npm test`.
3. Run `npx quartz build` when rendering or plugin behavior may change.

If a check fails because of a pre-existing issue, report it clearly and do not hide it with unrelated
changes. Before handing off, use `git diff --check` and verify that only intended files changed.

## Change discipline

- Preserve unrelated user changes in a dirty worktree.
- Do not commit, push, deploy, or rewrite history unless explicitly asked.
- Avoid destructive or broad maintenance commands. Prefer targeted edits and reversible operations.
- If the user's request conflicts with these conventions, follow the explicit request but keep the
  deviation narrow and call it out.
