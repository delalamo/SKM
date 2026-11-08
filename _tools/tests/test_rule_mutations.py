"""Mutation tests: break the fixture vault on purpose and see each rule fire.

A rule that passes the real vault but has never been seen to fail proves
nothing (spec section 11.3). Every registered rule needs at least one entry
in MUTATIONS; ``test_every_rule_has_a_mutation`` enforces that.
"""

from __future__ import annotations

import json

import pytest

import rules
from conftest import katex_dir

ALPHA = "Papers/alpha2020.md"
GAMMA = "Papers/gamma2021.md"
DELTA = "Papers/delta2019.md"
C1 = "Claims/Short widget loops adopt a small number of canonical shapes.md"
C2 = "Claims/Widget loop shapes interconvert in solution.md"
C3 = "Claims/Widget loops are rigid.md"
CONCEPT = "Concepts/WidgetFold.md"
CONTEXT_CALLOUT = (
  "> [!context|margin llm] Scope\n"
  "> The survey covers [[Canonical loop|canonical loops]] from crystal structures only.\n\n"
)
RIGID_CALLOUT = (
  "> [!claim|margin llm supports] Supports\n"
  "> - [[Widget loops are rigid]]\n"
  ">\n"
  "> Rigidity is inferred from low B-factors, not measured directly.\n\n"
)


def legacy_link(fx):
  fx.write("notes/Old note.md", "---\ntags: []\n---\nOld.\n")
  fx.replace(CONCEPT, "Loops farther", "See [[Old note]]. Loops farther")


def duplicate_name(fx):
  fx.write("Concepts/Canonical loop.md", "---\ntype: concept\naliases: []\nintroduced_by: []\ntopics: []\ntags: [concept]\n---\n\nText.\n")


def misplaced_attachment(fx):
  (fx.vault / "Concepts" / "fig.png").write_bytes((fx.vault / "Papers/attachments/alpha2020-fig1.png").read_bytes())
  fx.replace(CONCEPT, "Loops farther", "![[fig.png]]\n\nLoops farther")


def stub_with_text(fx):
  fx.write(DELTA, fx.read(DELTA) + "\nSome text. ^del19-p001\n")


def orphan_callout(fx):
  fx.write(ALPHA, fx.read(ALPHA) + "\n> [!context|margin llm] Note\n> Dangling.\n")


def registry_ghost(fx):
  path = fx.data / "claim_ids.json"
  registry = json.loads(path.read_text())
  registry["C-0009"] = {"title": "A claim that has no note"}
  path.write_text(json.dumps(registry))


def drop_summary(fx):
  text = fx.read(C3)
  start = text.index("---\n", 4) + len("---\n")
  fx.write(C3, text[:start] + "\n" + text[text.index("## Evidence"):])


def rename_claim_with_full_stop(fx):
  old = fx.path(C3)
  old.rename(old.with_name("Widget loops are rigid..md"))


MUTATIONS = {
  "FM-PARSE": [lambda fx: fx.replace(CONCEPT, "type: concept", "type: [concept")],
  "LINK-RESOLVE": [
    lambda fx: fx.replace("Topics/Widget loops.md", "- [[Loop dynamics]]", "- [[Loop dynamix]]"),
    lambda fx: fx.replace(C1, "![[alpha2020#^alp20-shapes]]", "![[alpha2020#^alp20-nope]]"),
  ],
  "LINK-LEGACY": [legacy_link],
  "NAME-DUP": [duplicate_name],
  "BLOCKID-DUP": [lambda fx: fx.replace(GAMMA, "^gam21-p001", "^gam21-p002")],
  "BLOCKLINK-LABEL": [lambda fx: fx.replace(CONCEPT, "Loops farther", "See [[alpha2020#^alp20-shapes]]. Loops farther")],
  "ATTACH-PLACE": [misplaced_attachment],
  "CALLOUT-TYPE": [
    lambda fx: fx.replace(GAMMA, "[!claim|margin llm qualifies]", "[!claim|margin llm qualifies wow]"),
    lambda fx: fx.replace(GAMMA, "[!claim|margin llm qualifies] Qualifies", "[!note|margin llm] Qualifies"),
  ],
  "CALLOUT-BLANK": [lambda fx: fx.replace(ALPHA, "only.\n\n> [!claim", "only.\n> [!claim")],
  "DOLLAR-DIGIT": [lambda fx: fx.replace(CONCEPT, "Loops farther", "It costs $5 to run. Loops farther")],
  "TAG-BALANCE": [
    lambda fx: fx.replace(GAMMA, "nanoseconds</mark>", "nanoseconds"),
    lambda fx: fx.replace(GAMMA, '<mark class="pm-claim">shapes', '<mark class="pm-other">shapes'),
  ],
  "NO-PANDOC": [lambda fx: fx.replace(CONCEPT, "Loops farther", "As shown [@alpha2020]. Loops farther")],
  "KATEX": [lambda fx: fx.replace(CONCEPT, "\\sum_i", "\\sum_i \\frac{1}{")],
  "PAPER-FM": [lambda fx: fx.replace(GAMMA, "venue: Journal of Widget Science\n", "")],
  "PAPER-LICENCE": [lambda fx: fx.replace(ALPHA, "license: CC BY 4.0", "license: All rights reserved")],
  "PAPER-STATUS": [lambda fx: fx.replace(GAMMA, "> [!status] About this note", "> [!context] About this note")],
  "PAPER-STUB": [stub_with_text],
  "PAPER-BLOCKIDS": [
    lambda fx: fx.replace(GAMMA, "shapes [[#^gam21-ref-1|1]]. ^gam21-p001", "shapes [[#^gam21-ref-1|1]]."),
    lambda fx: fx.replace(GAMMA, "^gam21-p001", "^xyz99-p001"),
  ],
  "PAPER-MARGIN-WORD": [lambda fx: fx.replace(GAMMA, "[!claim|margin llm qualifies]", "[!claim|margin qualifies]")],
  "PAPER-ORPHAN-CALLOUT": [orphan_callout],
  "PAPER-HIGHLIGHT-COUNT": [
    lambda fx: fx.replace(
      GAMMA,
      '<mark class="pm-claim">no loop stayed in one shape for the whole run</mark>',
      "no loop stayed in one shape for the whole run",
    )
  ],
  "PAPER-CALLOUT-ORDER": [lambda fx: fx.replace(ALPHA, CONTEXT_CALLOUT + RIGID_CALLOUT, RIGID_CALLOUT + CONTEXT_CALLOUT)],
  "PAPER-NO-LABELS": [
    lambda fx: fx.replace(GAMMA, '<mark class="pm-claim">shapes', '<mark class="pm-claim" data-label="a">shapes'),
    lambda fx: fx.replace(ALPHA, "> Rigidity is inferred", "> (a) Rigidity is inferred"),
  ],
  "PAPER-SPAN": [
    lambda fx: fx.replace(GAMMA, "12 loops showed", "12 loops showed shapes switching within nanoseconds and"),
    lambda fx: fx.replace(GAMMA, "the whole run</mark>", "the whole run [[Canonical loop|x]]</mark>"),
  ],
  "PAPER-CLAIM-ONE": [
    lambda fx: fx.replace(
      GAMMA,
      "> - [[Short widget loops adopt a small number of canonical shapes]]",
      "> - [[Short widget loops adopt a small number of canonical shapes]]\n> - [[Widget loops are rigid]]",
    ),
    lambda fx: fx.replace(GAMMA, "[!claim|margin llm qualifies]", "[!claim|margin llm qualifies supports]"),
  ],
  "PAPER-MARGIN-LINKS": [lambda fx: fx.replace(ALPHA, "structures only.", "structures only. See [[Widget loops]].")],
  "PAPER-TEXT-LINKS": [lambda fx: fx.replace(GAMMA, "a handful of loop shapes", "a handful of [[Widget loops|loop]] shapes")],
  "PAPER-CITE-CALLOUT": [
    lambda fx: fx.replace(ALPHA, "References (2)", "References (3)"),
    lambda fx: fx.replace(ALPHA, "> - [[#^alp20-ref-2|2]] Omega O. Loops in gadgets. Gadget Journal. 2015.\n", ""),
  ],
  "PAPER-CLAIMS-FM": [lambda fx: fx.replace(GAMMA, '  - "[[Widget loops are rigid]]"\n', "")],
  "CLAIM-FM": [
    lambda fx: fx.replace(C3, "status: contested", "status: debated"),
    lambda fx: fx.replace(C3, "evidence_strength: weak\n", ""),
  ],
  "CLAIM-TITLE": [rename_claim_with_full_stop],
  "CLAIM-ID": [lambda fx: fx.replace(C3, "id: C-0003", "id: C-3"), lambda fx: fx.replace(C3, "id: C-0003", "id: C-0001")],
  "REGISTRY": [registry_ghost],
  "CLAIM-SUMMARY": [drop_summary],
  "CLAIM-AUTHORS": [
    lambda fx: fx.replace(C1, "one crystal survey,", "one crystal survey by Alpha et al.,"),
    lambda fx: fx.replace(C1, "one crystal survey,", "one crystal survey (Gamma 2021),"),
  ],
  "CLAIM-SUMMARY-LINKS": [lambda fx: fx.replace(C1, "one crystal survey,", "[[alpha2020|one crystal survey]],")],
  "CLAIM-TOPIC-FIRST": [
    lambda fx: fx.replace(C3, "studies of [[Loop dynamics|loop dynamics]] in solution", "studies of loop dynamics in solution"),
    lambda fx: fx.replace(C1, "Most short [[Widget loops|widget loops]]", "Widget loops vary. Most short [[Widget loops|widget loops]]"),
  ],
  "CLAIM-LINK-ONCE": [
    lambda fx: fx.replace(C1, "describes.", "describes. See [[Widget loop shapes interconvert in solution]]."),
    lambda fx: fx.write(C1, fx.read(C1) + "\n## Topics\n\n- [[Widget loops]]\n"),
  ],
  "CLAIM-EVIDENCE": [
    lambda fx: fx.replace(C3, "No simulated loop stayed in one shape, which contradicts rigidity in solution.\n\n", ""),
    lambda fx: fx.replace(C3, "%% begin generated: excerpts gamma2021 %%\n![[gamma2021#^gam21-p002]]\n", "%% begin generated: excerpts gamma2021 %%\n"),
  ],
  "CLAIM-KB-MARGIN": [
    lambda fx: fx.replace(C3, 'kb_contradicting: ["[[gamma2021]]"]', "kb_contradicting: []"),
    lambda fx: fx.replace(C3, 'kb_qualifying: []', 'kb_qualifying: ["[[gamma2021]]"]'),
  ],
  "CLAIM-PENDING": [
    lambda fx: fx.replace(C2, 'paper: "[[delta2019]]"', 'paper: "[[gamma2021]]"'),
    lambda fx: fx.replace(C2, "### [[delta2019|Delta (2019): early loop census]]", "### Somewhere else"),
  ],
  "TOPIC-FM": [lambda fx: fx.replace("Topics/Loop dynamics.md", "type: topic", "type: hub")],
  "TOPIC-MARKERS": [
    lambda fx: fx.replace("Topics/Loop dynamics.md", "## Related topics", "## See also"),
    lambda fx: fx.replace("Topics/Loop dynamics.md", "%% end generated %%\n", ""),
  ],
  "TOPIC-RETIRED": [lambda fx: fx.write("Topics/Loop dynamics.md", fx.read("Topics/Loop dynamics.md") + "\n## Open questions\n\nMany.\n")],
  "GLOSSARY-PLAIN": [
    lambda fx: fx.replace("Glossary/Canonical loop.md", "backbone conformation", "**backbone** conformation"),
    lambda fx: fx.replace("Glossary/Canonical loop.md", "by shape", "by [[Widget loops|shape]]"),
  ],
  "ACRONYMS-TABLE": [lambda fx: fx.replace("Glossary/Acronyms.md", "| Acronym | Definition |", "| Short | Long |")],
  "CONCEPT-FM": [lambda fx: fx.replace(CONCEPT, 'introduced_by: ["[[alpha2020]]"]', "introduced_by: alpha2020")],
  "DATASET-FM": [lambda fx: fx.replace("Datasets/Widget Structure Bank.md", "access_class: public", "access_class: open")],
  "INDEX-GENERATED": [lambda fx: fx.write("Indexes/Claims index.md", fx.read("Indexes/Claims index.md") + "Hand-written note.\n")],
}


def fired(fx, rule_id: str) -> set[str]:
  vault = fx.load()
  return {problem.rule for problem in rules.run(vault, katex=katex_dir())}


def test_fixture_vault_is_clean(fixture_vault):
  problems = rules.run(fixture_vault.load(), katex=katex_dir())
  assert problems == [], "\n".join(map(str, problems))


def test_every_rule_has_a_mutation():
  missing = sorted(set(rules.load_all()) - set(MUTATIONS))
  assert not missing, f"rules without a mutation test: {missing}"
  unknown = sorted(set(MUTATIONS) - set(rules.load_all()))
  assert not unknown, f"mutations for unknown rules: {unknown}"


CASES = [(rule_id, index) for rule_id, mutations in MUTATIONS.items() for index in range(len(mutations))]


@pytest.mark.parametrize("rule_id,index", CASES, ids=[f"{r}-{i}" for r, i in CASES])
def test_mutation_fires_rule(fixture_vault, rule_id, index):
  if rules.load_all()[rule_id].needs_katex and katex_dir() is None:
    pytest.skip("node and node_modules/katex are needed for the KaTeX rule")
  MUTATIONS[rule_id][index](fixture_vault)
  assert rule_id in fired(fixture_vault, rule_id)
