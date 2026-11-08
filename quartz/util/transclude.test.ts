import test, { describe } from "node:test"
import assert from "node:assert"
import { Element } from "hast"
import { transcludeElement } from "./transclude"
import { FullSlug } from "./path"

const excerpt = (): Element => ({
  type: "element",
  tagName: "p",
  properties: { id: "alp20-p003" },
  children: [
    { type: "text", value: "Earlier counts " },
    {
      type: "element",
      tagName: "a",
      properties: { href: "#alp20-ref-1", className: ["internal"] },
      children: [{ type: "text", value: "1" }],
    },
    {
      type: "element",
      tagName: "a",
      properties: { href: "../Glossary/Canonical-loop", className: ["internal"] },
      children: [{ type: "text", value: "loop" }],
    },
  ],
})

describe("transcludeElement", () => {
  test("rebases same-page links onto the transcluded note", () => {
    const out = transcludeElement(
      excerpt(),
      "Claims/Widget-loops-are-rigid" as FullSlug,
      "Papers/alpha2020" as FullSlug,
    )
    const links = out.children.filter((c): c is Element => c.type === "element")
    // Resolve as a browser would, from the embedding page.
    const page = "https://example.org/Claims/Widget-loops-are-rigid"
    const resolve = (el: Element) => {
      const url = new URL(String(el.properties.href), page)
      return url.pathname + url.hash
    }
    assert.strictEqual(links[0].properties.href, "../Papers/alpha2020#alp20-ref-1")
    assert.strictEqual(resolve(links[0]), "/Papers/alpha2020#alp20-ref-1")
    assert.strictEqual(resolve(links[1]), "/Glossary/Canonical-loop")
  })

  test("leaves same-page links alone when the note embeds itself", () => {
    const out = transcludeElement(
      excerpt(),
      "Papers/alpha2020" as FullSlug,
      "Papers/alpha2020" as FullSlug,
    )
    const link = out.children[1] as Element
    assert.strictEqual(link.properties.href, "#alp20-ref-1")
  })

  test("does not modify the source tree", () => {
    const source = excerpt()
    transcludeElement(source, "Claims/x" as FullSlug, "Papers/alpha2020" as FullSlug)
    assert.strictEqual((source.children[1] as Element).properties.href, "#alp20-ref-1")
  })
})
