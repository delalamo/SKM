import rehypeCitation from "rehype-citation"
import { PluggableList } from "unified"
import { visit } from "unist-util-visit"
import { QuartzTransformerPlugin } from "../types"

export interface Options {
  bibliographyFile: string
  suppressBibliography: boolean
  linkCitations: boolean
  csl: string
}

const defaultOptions: Options = {
  bibliographyFile: "./bibliography.bib",
  suppressBibliography: false,
  linkCitations: false,
  csl: "apa",
}

const citationShimAttr = "data-citation-shim"
const inlineCitationTextPattern = /(^|[\s(;,\-])@[A-Za-z0-9_{]/

function containsCitationText(node: unknown): boolean {
  if (typeof node !== "object" || node === null) {
    return false
  }

  const maybeNode = node as { type?: string; value?: string; children?: unknown[] }
  if (maybeNode.type === "text" && typeof maybeNode.value === "string") {
    return maybeNode.value.includes("[@") || inlineCitationTextPattern.test(maybeNode.value)
  }

  if (!Array.isArray(maybeNode.children)) {
    return false
  }

  return maybeNode.children.some((child) => containsCitationText(child))
}

function extractTextContent(node: unknown): string {
  if (typeof node !== "object" || node === null) {
    return ""
  }

  const maybeNode = node as { type?: string; value?: string; children?: unknown[] }
  if (maybeNode.type === "text" && typeof maybeNode.value === "string") {
    return maybeNode.value
  }

  if (!Array.isArray(maybeNode.children)) {
    return ""
  }

  return maybeNode.children.map((child) => extractTextContent(child)).join("")
}

function appendClass(node: { properties?: Record<string, unknown> }, className: string): void {
  node.properties = node.properties ?? {}
  const current = node.properties.className
  const classNames = Array.isArray(current)
    ? current.filter((value): value is string => typeof value === "string")
    : typeof current === "string"
      ? [current]
      : []

  if (!classNames.includes(className)) {
    node.properties.className = [...classNames, className]
  }
}

function hasClass(node: { properties?: Record<string, unknown> }, className: string): boolean {
  const current = node.properties?.className
  if (Array.isArray(current)) {
    return current.includes(className)
  }

  return current === className
}

function stripInternetLabel(value: string): string {
  return value
    .replace(/\s+\[Internet\]\./g, ".")
    .replace(/\s+\[Internet\]/g, "")
    .replace(/\.\./g, ".")
    .replace(/\s{2,}/g, " ")
}

export const Citations: QuartzTransformerPlugin<Partial<Options>> = (userOpts) => {
  const opts = { ...defaultOptions, ...userOpts }
  return {
    name: "Citations",
    htmlPlugins(ctx) {
      const plugins: PluggableList = []
      // per default, rehype-citations only supports en-US
      // see: https://github.com/timlrx/rehype-citation/issues/12
      // in here there are multiple usable locales:
      // https://github.com/citation-style-language/locales
      // thus, we optimistically assume there is indeed an appropriate
      // locale available and simply create the lang url-string
      let lang: string = "en-US"
      if (ctx.cfg.configuration.locale !== "en-US") {
        lang = `https://raw.githubusercontent.com/citation-stylelanguage/locales/refs/heads/master/locales-${ctx.cfg.configuration.locale}.xml`
      }
      plugins.push(() => {
        return (tree, _file) => {
          visit(tree, "element", (node, _index, _parent) => {
            if (
              (node.tagName === "em" || node.tagName === "strong") &&
              containsCitationText(node)
            ) {
              node.properties = node.properties ?? {}
              node.properties[citationShimAttr] = node.tagName
              node.tagName = "span"
            }
          })
        }
      })

      // Add rehype-citation to the list of plugins
      plugins.push([
        rehypeCitation,
        {
          bibliography: opts.bibliographyFile,
          suppressBibliography: opts.suppressBibliography,
          linkCitations: opts.linkCitations,
          csl: opts.csl,
          lang,
        },
      ])

      // Transform the HTML of the citattions; add data-no-popover property to the citation links
      // using https://github.com/syntax-tree/unist-util-visit as they're just anochor links
      plugins.push(() => {
        return (tree, _file) => {
          const bibliographyNumberByHref = new Map<string, string>()

          visit(tree, "element", (node, _index, _parent) => {
            const bibliographyId = node.properties?.id
            if (node.tagName !== "div" || typeof bibliographyId !== "string") {
              return
            }

            if (!bibliographyId.startsWith("bib-") || !Array.isArray(node.children)) {
              return
            }

            const leftMarginNode = node.children.find((child: unknown) => {
              if (typeof child !== "object" || child === null) {
                return false
              }

              const maybeChild = child as { type?: string; tagName?: string; properties?: Record<string, unknown> }
              if (maybeChild.type !== "element" || maybeChild.tagName !== "div") {
                return false
              }

              const className = maybeChild.properties?.className
              if (Array.isArray(className)) {
                return className.includes("csl-left-margin")
              }

              return className === "csl-left-margin"
            })

            const bibliographyNumber = extractTextContent(leftMarginNode).match(/\d+/)?.[0]
            if (bibliographyNumber) {
              bibliographyNumberByHref.set(`#${bibliographyId}`, bibliographyNumber)
            }
          })

          visit(tree, "element", (node, _index, _parent) => {
            const citationShim = node.properties?.[citationShimAttr]
            if (node.tagName === "span" && typeof citationShim === "string") {
              node.tagName = citationShim
              delete node.properties[citationShimAttr]
            }

            if (node.tagName === "span" && typeof node.properties?.id === "string") {
              if (node.properties.id.startsWith("citation--")) {
                appendClass(node, "citation")
              }
            }

            if (node.tagName === "a" && node.properties?.href?.startsWith("#bib")) {
              appendClass(node, "citation-link")
              node.properties["data-no-popover"] = true

              const bibliographyNumber = bibliographyNumberByHref.get(node.properties.href)
              if (bibliographyNumber) {
                node.children = [{ type: "text", value: bibliographyNumber }]
              }
            }
          })

          visit(tree, "text", (node, _index, parent) => {
            if (typeof node.value !== "string") {
              return
            }

            if (typeof parent !== "object" || parent === null) {
              return
            }

            const maybeParent = parent as { type?: string; properties?: Record<string, unknown> }
            if (maybeParent.type !== "element" || !hasClass(maybeParent, "csl-right-inline")) {
              return
            }

            node.value = stripInternetLabel(node.value)
          })
        }
      })

      return plugins
    },
  }
}
