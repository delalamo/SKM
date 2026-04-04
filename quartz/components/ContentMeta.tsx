import { formatDate } from "./Date"
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { JSX } from "preact"
import style from "./styles/contentMeta.scss"

interface ContentMetaOptions {
  showReadingTime: boolean
  showComma: boolean
}

const defaultOptions: ContentMetaOptions = {
  showReadingTime: true,
  showComma: true,
}

export default ((opts?: Partial<ContentMetaOptions>) => {
  const options: ContentMetaOptions = { ...defaultOptions, ...opts }

  function ContentMetadata({ cfg, fileData, displayClass }: QuartzComponentProps) {
    const text = fileData.text
    if (!text) return null

    const segments: (string | JSX.Element)[] = []
    const dates = fileData.dates

    if (dates?.created) {
      segments.push(
        <span class="content-meta-date">
          <span class="content-meta-label">Created </span>
          <time datetime={dates.created.toISOString()}>
            {formatDate(dates.created, cfg.locale)}
          </time>
        </span>,
      )
    }

    if (dates?.modified) {
      // Only show modified if it differs from created by more than a minute
      const diffMs = dates.created
        ? Math.abs(dates.modified.getTime() - dates.created.getTime())
        : Infinity
      if (diffMs > 60_000) {
        segments.push(
          <span class="content-meta-date">
            <span class="content-meta-label">Modified </span>
            <time datetime={dates.modified.toISOString()}>
              {formatDate(dates.modified, cfg.locale)}
            </time>
          </span>,
        )
      }
    }

    return (
      <p show-comma={options.showComma} class={classNames(displayClass, "content-meta")}>
        {segments}
      </p>
    )
  }

  ContentMetadata.css = style

  return ContentMetadata
}) satisfies QuartzComponentConstructor
