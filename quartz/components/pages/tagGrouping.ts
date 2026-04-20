import { QuartzPluginData } from "../../plugins/vfile"

export interface TagSection {
  contentPage?: QuartzPluginData
  pages: QuartzPluginData[]
  tag: string | null
  title: string
}

function humanizeTagSegment(segment: string): string {
  const text = segment.replaceAll("-", " ")
  return text.charAt(0).toUpperCase() + text.slice(1)
}

function pageKey(file: QuartzPluginData): string {
  return file.slug ?? file.frontmatter?.title ?? ""
}

export function groupFilesByDirectChildTag(
  tag: string,
  allFiles: QuartzPluginData[],
): TagSection[] | null {
  const general = new Map<string, QuartzPluginData>()
  const childSections = new Map<string, Map<string, QuartzPluginData>>()
  const tagPages = new Map<string, QuartzPluginData>()

  for (const file of allFiles) {
    if (file.slug?.startsWith("tags/")) {
      tagPages.set(file.slug, file)
      continue
    }

    for (const rawTag of file.frontmatter?.tags ?? []) {
      if (rawTag === tag) {
        general.set(pageKey(file), file)
        continue
      }

      if (!rawTag.startsWith(`${tag}/`)) continue

      const remainder = rawTag.slice(tag.length + 1)
      const directChild = remainder.split("/", 1)[0]
      if (!directChild) continue

      const childTag = `${tag}/${directChild}`
      const pages = childSections.get(childTag) ?? new Map<string, QuartzPluginData>()
      pages.set(pageKey(file), file)
      childSections.set(childTag, pages)
    }
  }

  if (childSections.size === 0) return null

  const sections: TagSection[] = []

  if (general.size > 0) {
    sections.push({
      pages: [...general.values()],
      tag: null,
      title: "General",
    })
  }

  const childResults = [...childSections.entries()]
    .map(([childTag, pages]) => {
      const contentPage = tagPages.get(`tags/${childTag}`)
      const fallbackTitle = humanizeTagSegment(childTag.slice(tag.length + 1))

      return {
        contentPage,
        pages: [...pages.values()],
        tag: childTag,
        title: contentPage?.frontmatter?.title ?? fallbackTitle,
      }
    })
    .sort((a, b) => a.title.localeCompare(b.title))

  sections.push(...childResults)
  return sections
}
