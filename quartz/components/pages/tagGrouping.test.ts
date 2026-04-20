import assert from "node:assert"
import test from "node:test"
import { QuartzPluginData } from "../../plugins/vfile"
import { FullSlug } from "../../util/path"
import { groupFilesByDirectChildTag } from "./tagGrouping"

function file(slug: string, tags?: string[], title?: string): QuartzPluginData {
  return {
    frontmatter: {
      title: title ?? slug,
      ...(tags ? { tags } : {}),
    },
    slug: slug as FullSlug,
  }
}

test("returns null for leaf tag pages", () => {
  const sections = groupFilesByDirectChildTag("antibodies/nanobodies", [
    file("notes/a", ["antibodies/nanobodies"]),
    file("notes/b", ["antibodies"]),
  ])

  assert.strictEqual(sections, null)
})

test("groups root-only notes into General and child tags by direct segment", () => {
  const sections = groupFilesByDirectChildTag("antibodies", [
    file("notes/a", ["antibodies"]),
    file("notes/b", ["antibodies/nanobodies"]),
    file("notes/c", ["antibodies/nanobodies/frameworks"]),
    file("notes/d", ["antibodies/engineering-and-design"]),
  ])

  assert.ok(sections)
  assert.deepStrictEqual(
    sections.map((section) => ({
      pages: section.pages.map((page) => page.slug),
      tag: section.tag,
      title: section.title,
    })),
    [
      {
        pages: ["notes/a"],
        tag: null,
        title: "General",
      },
      {
        pages: ["notes/d"],
        tag: "antibodies/engineering-and-design",
        title: "Engineering and design",
      },
      {
        pages: ["notes/b", "notes/c"],
        tag: "antibodies/nanobodies",
        title: "Nanobodies",
      },
    ],
  )
})

test("sorts child sections by rendered title and uses child tag page titles when present", () => {
  const sections = groupFilesByDirectChildTag("antibodies", [
    file("notes/a", ["antibodies/zebrafish"]),
    file("notes/b", ["antibodies/engineering-and-design"]),
    file("tags/antibodies/engineering-and-design", undefined, "Engineering and design"),
    file("tags/antibodies/zebrafish", undefined, "Affinity in zebrafish"),
  ])

  assert.ok(sections)
  assert.deepStrictEqual(
    sections.map((section) => ({
      contentPage: section.contentPage?.slug,
      tag: section.tag,
      title: section.title,
    })),
    [
      {
        contentPage: "tags/antibodies/zebrafish",
        tag: "antibodies/zebrafish",
        title: "Affinity in zebrafish",
      },
      {
        contentPage: "tags/antibodies/engineering-and-design",
        tag: "antibodies/engineering-and-design",
        title: "Engineering and design",
      },
    ],
  )
})
