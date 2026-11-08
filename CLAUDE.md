# CLAUDE.md: maintaining the SKM knowledge base

Rules for anyone, human or AI, who edits this repository. The repo publishes
[notes.delalamo.xyz](https://notes.delalamo.xyz) with Quartz, and `content/` is
also an Obsidian vault. It is being rebuilt as an **annotated research
knowledge base** following the owner's *Annotated Research Knowledge Base:
Master Design Specification* (Oct 2026). Where this file and the validator
disagree, fix whichever is wrong.

## Two zones during the migration

| Zone | Folders | Rules |
|---|---|---|
| Knowledge base | `content/Papers`, `Claims`, `Topics`, `Concepts`, `Glossary`, `Datasets`, `Indexes`, `Templates` | Everything below, enforced by `_tools/validate_vault.py` |
| Legacy | `content/notes`, `content/tags`, `content/review` | Frozen: no new files. Notes leave it only by being migrated (`git mv`) into the knowledge base. Knowledge-base notes never link into it. |

Legacy notes keep using Pandoc citations (`[@key]`) and the tag taxonomy in
`docs/tag-taxonomy.md` until they are migrated. When the zone is empty it is
deleted along with the Citations plugin.

## Principles (spec section 2)

1. **A paper note reproduces the paper** word for word, typos included. Corrections fix conversion errors only.
2. **Margin notes help with reading *this* paper.** They never compare papers or mention the vault.
3. **Claim notes carry the broader context.** Papers reach claims only through margin claim callouts.
4. **Claims are paper-agnostic:** a declarative, testable sentence, true given the vault's papers, naming no authors.
5. **Machine-written content is marked** (`llm`, `annotation_provenance`, `human_verified: false`) until a person reviews it.
6. **Generated beats hand-maintained.** Never edit generated output; edit the inputs and re-run the pipeline.
7. **Every rule that can be checked is checked**, and every validator rule has a mutation test.
8. **Less is more in the margin.**
9. **Link once, at first mention.**
10. **Provenance traceable to source data.**
11. **Honesty about limits:** when a source, licence, host or tool blocks a step, say so; never fill a gap with a guess.

## Folder map

```
CLAUDE.md                     this file (maintainers)
_tools/                       scripts, tests, data (outside the vault so Quartz never publishes them)
  builds/build_<citekey>.py   per-paper record of every correction and margin note
  builds/base/<citekey>.md    pristine ingest output (CC-licensed papers only)
  data/                       claim_ids.json, eponyms.txt, ambiguous_surnames.txt, legacy_urls.txt, licences/, sources/
content/                      the vault and the site
  .obsidian/snippets/paper-margin.css   margin layout and colours (Quartz imports the same file)
  Papers/<citekey>.md         one note per paper; figures in Papers/attachments/<citekey>-<name>.png
  Claims/<claim sentence>.md  one note per claim
  Topics/<noun phrase>.md     navigation hubs
  Concepts/<name>.md          models, methods and concepts (field-specific type, see Deviations)
  Glossary/<term>.md          term + one plain definition; Glossary/Acronyms.md holds the acronym table
  Datasets/<name>.md          shared data sources
  Indexes/                    generated only: Claims index, Ingestion queue, Review queue
  Templates/                  note templates (not published, not validated)
.sources/                     gitignored cache of PDFs and JATS, named by SHA-256
```

Citekeys are the existing `bibliography.bib` keys (surname + year + optional
letter or word). Do not rename them: the paperbot's model is keyed on them.

## Paper notes

**Frontmatter** follows `Templates/Paper template.md`. `claims` and `topics` are
generated from the margin callouts; `block_prefix` (e.g. `gul23`) is assigned
once and never changes.

**Three states (`fulltext`):**

| State | When | Body |
|---|---|---|
| `full` | The version held is under any Creative Commons licence (CC BY, BY-SA, BY-NC, BY-NC-SA, BY-ND, BY-NC-ND, CC0). | The full text word for word, plus the margin layer. The status banner states the licence with a link, "© the authors", and the changes made. |
| `digest` | Not openly licensed, but the paper has been read. | The paper's exact headings with summaries in our own words, plus transcribed equations, tables and the reference list. Existing figures from these papers are kept as attachments with their printed captions. |
| `stub` | The text could not be obtained. | Bibliographic frontmatter and the status banner only. Owner-supplied PDFs turn a stub into a digest. |

The licence must be confirmed for the **exact version held** (Crossref, Europe
PMC/PMC, arXiv `arXivRaw`, bioRxiv). `paper_relevance/abstract_provenance.jsonl`
records only the abstract's licence and is a hint, not proof.

**Body rules (spec 4.3):**
- Order and headings exactly as in the source, including front matter, footnotes, CRediT and competing interests.
- A block ID with the paper's prefix on every paragraph, list item, table, equation and caption: `... text. ^gul23-p042`. A table or display equation takes its ID on its own line after a blank line. Linked blocks get semantic IDs (`^gul23-fig3`, `^gul23-h3-ensembles`).
- Citations become numeric links `[[#^gul23-ref-4|4]]`. References read `4. Full reference as printed → [[citekey]] ^gul23-ref-4`, with the arrow link only when the cited work has a vault note.
- Figures `![[<citekey>-fig3.png]]` with the caption as printed; tables as Markdown; display equations in `$$ … $$` with `\tag{N}`; currency escaped as `\$`.
- Paper text links only glossary or concept notes, at first mention. It never links topics or claims.

**Fidelity (spec 5):** a full text is finished only when `check_fulltext.py`,
`check_punct.py` and `check_hyphens.py` report no unexplained difference
against the PDF. Every correction is an exact `(old, new)` pair in the paper's
build script, asserted to occur once. Deliberate exceptions go in
`fidelity_accept` with a reason.

## The margin layer (spec 6 and 7)

A margin callout is written `> [!type|margin <author> <relation>] Title` and
sits immediately **before** the passage it annotates, with blank lines around it.

| Type | Colour | Highlight | Purpose |
|---|---|---|---|
| `claim` | orange | `<mark class="pm-claim">` | Links a passage to one claim it supports, qualifies, contradicts, cites or relates to |
| `context` | dark yellow | `<mark class="pm-context">` | How to read this passage: scope, likely bias, what a measure shows |
| `eq` | blue | none | Symbol key for the equation that follows |
| `cite` | grey, collapsed | none | Generated full references for the passage's citations |
| `status` | steel | none | Full-width banner: version held, licence, status checks |

- **Metadata words:** `margin`, `llm` or `human`, `verified` or `unverified`, and on claim callouts exactly one of `supports`, `qualifies`, `contradicts`, `cited`, `related`.
- **One highlight, one callout.** Each claim callout lists exactly one claim (`> - [[Claim]]`). Callouts follow their highlights' order, with equation notes first and the reference callout last. A highlight is one sentence or clause, occurs once in its passage, and contains no wikilink.
- **`cited`** marks a passage that reports another work's finding without testing it, so a claim never looks supported by many papers when only one tested it.
- **Titles name the relation:** `Supports`, `Qualifies`, `Contradicts`, `Cited, not tested here`, `Related`. They may carry the evidence class: `Supports (benchmark)`, `Supports (model-derived)`.
- **Margin notes are added in code** with `_tools/annolib.py` from a build script, never by hand-editing a large note.
- **Acronyms** get hover definitions from `Glossary/Acronyms.md` via `apply_abbr.py`, never callouts.

## Claim notes (spec 8)

- **Title = file name = the claim**, one declarative, testable sentence. It must avoid `# ^ [ ] | \ / : * ? " < >`, stay within 150 characters, and not end with a full stop.
- **Frontmatter** follows `Templates/Claim template.md`. `id` is `C-0001` style, registered in `_tools/data/claim_ids.json`, and is never reused.
- **Generated fields:** `kb_supporting`, `kb_qualifying`, `kb_contradicting`, `independence` and the excerpts are generated from the papers' margin callouts by `build_claim_evidence.py`.
- **Summary paragraph:** plain language, no author names (checked against every bibliography surname), no links to papers or blocks. Each frontmatter topic is linked exactly once, at its first mention, counting the topic's aliases. Related claims are linked inline. No Topics, See also or Falsified by sections.
- **`## Evidence`:** one `### [[citekey|Author (Year): setting]]` per source with two or three sentences of prose, then the generated excerpt embeds. An optional `## Outside the vault` covers works not yet ingested, marked as unverified.
- **Build scripts** refer to claims by ID (`note.claim(block, "C-0042", span, "supports")`), so renaming or merging a claim never touches a build.

### Status and evidence strength for protein ML

| Class | Meaning |
|---|---|
| E1 | Prospective experiment (DMS, assays, design-and-test) |
| E2 | Retrospective analysis of experimental data (PDB, repertoires, mega-scale stability sets) |
| E3 | Benchmark of models against experimental ground truth |
| E4 | Computation standing in for the physical system (MD, predicted structures used as data, in-silico fitness) |

| Status | Use when |
|---|---|
| `supported` | At least two independent groups at E1–E3 agree, with no unresolved contradiction |
| `tentative` | One independent group |
| `model-derived` | All support is E4 for a claim about the physical world. A claim *about model behaviour* backed by benchmarks is empirical, not model-derived. |
| `contested` | A verified E1–E3 contradiction that scope does not explain |
| `proposed` | A conjecture, or no evidence verified yet |

| Strength | Use when |
|---|---|
| `strong` | At least three independent E1/E2 groups |
| `moderate` | Two groups, or one well-powered E1 study |
| `weak-to-moderate` | One source, or a benchmark at risk of train/test leakage |
| `weak` | Small n, anecdote, or E4 only |

`independence` counts groups, not papers: papers sharing an author or a dataset
fall in one group.

### Migrated claims: `kb_pending`

A claim migrated from `content/notes` keeps its legacy sources as
`kb_pending: [{paper: "[[citekey]]", rel_hint: supports}]` plus a
`## Evidence pending verification` section. A pending entry is legal only
while that paper is not yet annotated (no `annotation_provenance.generated`).
Annotating the paper must resolve every pending entry, either into a margin
callout (the pipeline then moves the section into `## Evidence`) or into an
explicit rejection. Status stays `proposed` until at least one source is verified.

## Topics, glossary, concepts, datasets, indexes

- **Topics:** prose overview, the generated claim list between `%% begin generated: claims %%` and `%% end generated %%`, and `## Related topics`. Never edit inside the markers. No "Papers in the vault" or "Open questions" sections.
- **Glossary:** the file name is the term; the body is one plain paragraph with no frontmatter, links, bold, lists, tables, equations or HTML. `Acronyms.md` holds only `| Acronym | Definition |`.
- **Concepts** (field-specific): models, methods and concepts that need more than a definition, such as AlphaFold2, ProteinMPNN or the Boltzmann distribution. Frontmatter is `type: concept`, `aliases`, `introduced_by` (paper notes) and `topics`. The body may hold equations, architecture details and figures from `Concepts/attachments/`. Findings about a concept belong in claims.
- **Datasets:** provider, access class (`public`, `licensed`, `restricted`, `by agreement`, `unavailable`), URL, identifiers.
- **Indexes:** generated only.

## Deviations from the master spec (owner decisions)

1. **The vault is `content/`** and Quartz still publishes it; `_tools/` lives at the repo root. The margin CSS is one file used by both Obsidian and Quartz.
2. **Full text for any Creative Commons licence**, ND and NC included; the status banner discloses the changes.
3. **The `Concepts/` note type** keeps rich model and concept notes.
4. **Figures already on the site** from non-OA papers stay, attached to digest notes.
5. **A `stub` state** for papers whose text cannot be obtained.
6. **Claim IDs have four digits** (`C-0001`), because the vault will pass 999 claims.
7. **`kb_pending`** is a migration-only state.
8. **Old URLs** are kept with `redirect_from`, not with `aliases`, which are search names here.

## Tools and pipeline

```bash
pip install -r _tools/requirements.txt          # PyYAML, pyspellchecker, pytest
npm ci                                          # Quartz (provides node_modules/katex)
python3 _tools/run_pipeline.py --katex node_modules/katex   # every generator, then the validator
python3 -m pytest _tools/tests -q               # unit, idempotency and mutation tests
python3 _tools/check_layout.py                  # Quartz build + Playwright: 0 overlaps required
```

Pipeline order: `build_paper_stubs` → `builds/build_*.py` → `build_cite_notes` →
`alias_block_links` → `build_claim_evidence` → `build_indexes` → `apply_abbr` →
`validate_vault`. Every step is idempotent: a second run changes nothing (CI
checks with `git diff --exit-code`).

Other tools:
- `build_paper_stubs.py --keys k1 k2` creates stub paper notes from the bibliography.
- `refresh_author_lists.py` refreshes `ambiguous_surnames.txt` after the bibliography grows.
- `check_legacy_urls.py public/ _tools/data/legacy_urls.txt` checks that every URL the site ever published still resolves.

**Adding a validator rule:** register it in `_tools/rules/`, then add a
mutation to `_tools/tests/test_rule_mutations.py` that breaks the fixture vault
and sees the rule fire. A rule without a mutation fails the test suite.

**Do not:**
- run `scripts/reconcile_bibliography.py` (it rewrites the bibliography and drops fields);
- rename citekeys;
- edit inside generated sections;
- add files to `content/notes`;
- set `human_verified: true` on anyone's behalf.

## Checklists (spec Appendix C)

**Adding a paper:**
- It overlaps papers already in the vault, so its claims will recur.
- The licence for the exact version is confirmed and recorded.
- `version_in_kb` is set.
- The source is ingested and front matter, footnotes, short sections and the supplement are present.
- The three fidelity checks report no unexplained differences, and every correction is in the build script.
- Linked blocks have semantic IDs.
- Claims are flagged where the evidence is, one callout per highlighted span, in order.
- Context notes are about this paper only; equation notes give symbol keys.
- Glossary terms are linked at first mention, with no topic or claim links in the text.
- Every `kb_pending` entry naming the paper is resolved.
- `annotation_provenance` is set with `human_verified: false`.
- The pipeline, validator and layout test are clean.

**Adding or editing a claim:**
- The title is one declarative, testable sentence.
- Status and strength follow the rubric; scope and provenance are filled in.
- The summary is plain language, with no authors or paper links.
- Topics are linked at first mention, and nothing is linked twice.
- Each source has a heading and prose.
- Re-run the pipeline.

**Adding a topic:**
- The theme recurs across claims.
- `aliases` lists the other names readers use.
- The overview is plain prose, and the generated markers and Related topics are in place.

## Working practices (spec 14)

- **Verify by running the checks**, not from memory.
- **Distrust a clean result from a new rule** until its mutation test has seen it fail.
- **Look at the rendering:** screenshots from the layout test, and Obsidian desktop and mobile for a new layout.
- **Fix the checker, not the result**, and never weaken a check to make one paper pass.
- **Report outcomes plainly:** what is done, what is left, and what blocks it.
- **Reproduce paper text only with a licence**, keep it out of chat replies, and never commit a PDF.
