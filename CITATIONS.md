# Citation Workflow

This site uses Quartz citations backed by `rehype-citation`.

## Adding a citation

1. Add a BibTeX entry to `bibliography.bib`.
2. Cite it in a note with Pandoc citation syntax such as `[@gurev2025]`.

Example:

```md
This claim is supported by prior work [@gurev2025].
```

That renders as a numbered citation and generates a bibliography entry on the page.

## Adding a BibTeX entry

Example:

```bibtex
@article{gurev2025,
  title = {Evaluating variant effect prediction across viruses},
  author = {Gurev, A. and others},
  year = {2025},
  doi = {10.1101/2025.08.04.668549},
  url = {https://doi.org/10.1101/2025.08.04.668549},
  journal = {bioRxiv}
}
```

The citekey must match the key used in notes.

## Citation style

Quartz is configured with the built-in `vancouver` CSL style, so citations render as compact numbered references.

## Notes

- Use `[@key]` for normal citations.
- Reusing the same key in a note should reuse the same reference number.
- Do not create paper citations as manual Markdown footnotes like `[^key]`.
- Ordinary explanatory footnotes can still use standard Markdown footnotes.

## Future automation

This PR keeps bibliography entry creation manual for reliability. The repo already has migration scripts for the older footnote-based citation flow under `scripts/`, and a follow-up can add DOI-to-BibTeX generation once that path is verified in this environment.
