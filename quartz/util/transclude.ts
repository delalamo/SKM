import { Element } from "hast"
import { visit } from "unist-util-visit"
import { FullSlug, normalizeHastElement, resolveRelative } from "./path"

// Clone a transcluded element for the embedding page. Same-page links inside it
// (such as a paper's citation links, `#alp20-ref-4`) must keep pointing at the
// source note, so fragment-only hrefs are rebased onto it.
export function transcludeElement(el: Element, slug: FullSlug, target: FullSlug): Element {
  const out = normalizeHastElement(el, slug, target)
  if (target === slug) {
    return out
  }
  const base = resolveRelative(slug, target)
  visit(out, "element", (node) => {
    const href = node.properties?.href
    if (node.tagName === "a" && typeof href === "string" && href.startsWith("#")) {
      node.properties.href = base + href
    }
  })
  return out
}
