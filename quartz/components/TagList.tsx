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
}

// Maps subtag slugs to the section anchor used in the MOC.
// Must stay in sync with SUBTAG_TITLES in generate_mocs.py.
const SUBTAG_ANCHORS: Record<string, string> = {
  "training":   "Training",
  "execution":  "Execution",
  "antibodies": "Antibodies",
  "datasets":   "Datasets",
  "misc":       "Miscellaneous",
}

function tagToMocUrl(tag: string): string | null {
  const slash  = tag.indexOf("/")
  const root   = slash !== -1 ? tag.slice(0, slash) : tag
  const subtag = slash !== -1 ? tag.slice(slash + 1) : ""

  const mocSlug = MOC_SLUGS[root]
  if (!mocSlug) return null  // unknown root — fall back to default tag page

  const anchor = subtag ? (SUBTAG_ANCHORS[subtag] ?? subtag) : ""
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
