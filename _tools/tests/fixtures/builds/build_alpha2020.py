"""Build record for alpha2020: every correction and margin note, in code."""


def build(ctx):
  note = ctx.load("alpha2020")
  note.fm["annotation_provenance"] = {"generator": "fixture", "generated": "2026-11-08", "human_verified": False}

  # Corrections: none needed beyond this example of a semantic block ID.
  note.name("Most short widget loops", "alp20-shapes")
  note.name("k = \\log_2 n", "alp20-eq1")
  note.name("**Fig. 1.**", "alp20-fig1")
  note.name("| Shape | Count |", "alp20-tab1")

  note.claim("alp20-shapes", "C-0001", "Most short widget loops fall into five recurring shapes.", "supports")
  note.context("alp20-p003", "Scope", "The survey covers [[Canonical loop|canonical loops]] from crystal structures only.", "loops from crystal structures")
  note.claim(
    "alp20-p003", "C-0003", "Loop backbones showed uniformly low B-factors.", "supports",
    note="Rigidity is inferred from low B-factors, not measured directly.",
  )
  note.eq("alp20-eq1", "Symbols", "$k$ is the number of shapes and $n$ the loop length.")
  return ctx.write(note, "alpha2020")
