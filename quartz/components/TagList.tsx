import { FullSlug, resolveRelative } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

// Maps top-level tag roots to their MOC page slug (relative to content/).
// Must stay in sync with MOC_TITLES in generate_mocs.py.
const MOC_SLUGS: Record<string, string> = {
  "inverse-folding": "MOCs/Inverse-Folding",
  "protein-folding":  "MOCs/Protein-Folding",
  "protein-design":   "MOCs/Protein-Design",
  "antibodies":       "MOCs/Antibodies",
  "diffusion-models": "MOCs/Diffusion-models",
  "diffusion-guidance": "MOCs/Diffusion-guidance",
}

// Maps subtag slugs to the rendered MOC section title.
// Must stay in sync with SUBTAG_TITLES in generate_mocs.py.
const SUBTAG_TITLES: Record<string, string> = {
  "training":   "Training",
  "design":     "Design",
  "implementation": "Implementation",
  "protein-design": "Protein Design",
  "structure-prediction": "Structure Prediction",
  "execution":  "Execution",
  "antibodies": "Antibodies",
  "datasets":   "Datasets",
  "misc":       "Miscellaneous",
}

function subtagToSectionTitle(subtag: string): string {
  return (
    SUBTAG_TITLES[subtag] ??
    subtag
      .split("-")
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(" ")
  )
}

function tagToMocUrl(tag: string): string | null {
  const slash  = tag.indexOf("/")
  const root   = slash !== -1 ? tag.slice(0, slash) : tag
  const subtag = slash !== -1 ? tag.slice(slash + 1) : ""

  const mocSlug = MOC_SLUGS[root]
  if (!mocSlug) return null  // unknown root — fall back to default tag page

  const anchor = subtag ? subtagToSectionTitle(subtag) : ""
  return anchor ? `${mocSlug}#${anchor}` : mocSlug
}

const TagList: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const tags = fileData.frontmatter?.tags
  if (tags && tags.length > 0) {
    return (
      <ul class={classNames(displayClass, "tags")}>
        {tags.map((tag) => {
          const mocUrl  = tagToMocUrl(tag)
          const linkDest = mocUrl
            ? resolveRelative(fileData.slug!, mocUrl as FullSlug)
            : resolveRelative(fileData.slug!, `tags/${tag}` as FullSlug)
          return (
            <li>
              <a href={linkDest} class="internal tag-link">
                {tag}
              </a>
            </li>
          )
        })}
      </ul>
    )
  } else {
    return null
  }
}

TagList.css = `
.tags {
  list-style: none;
  display: flex;
  padding-left: 0;
  gap: 0.4rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.section-li > .section > .tags {
  justify-content: flex-end;
}

.tags > li {
  display: inline-block;
  white-space: nowrap;
  margin: 0;
  overflow-wrap: normal;
}

a.internal.tag-link {
  border-radius: 8px;
  background-color: var(--highlight);
  padding: 0.2rem 0.4rem;
  margin: 0 0.1rem;
}
`

export default (() => TagList) satisfies QuartzComponentConstructor
