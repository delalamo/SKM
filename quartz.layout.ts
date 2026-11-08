import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { QuartzComponentProps } from "./quartz/components/types"

const isPaperNote = (page: QuartzComponentProps) =>
  (page.fileData.frontmatter?.cssclasses ?? []).includes("paper-margin")

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jackyzha0/quartz",
      "Discord Community": "https://discord.gg/cRFFHYye7t",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ConditionalRender({
      component: Component.ContentMeta(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer(),
    Component.ConditionalRender({
      component: Component.DesktopOnly(Component.TableOfContents()),
      condition: isPaperNote,
    }),
  ],
  right: [
    // Paper notes use the page width for their margin notes; their links to
    // claims live in those notes, so the graph and backlinks are left out.
    Component.ConditionalRender({
      component: Component.Graph({
        localGraph: { showTags: false, fontSize: 0.85 },
        globalGraph: { showTags: false, fontSize: 0.85 },
      }),
      condition: (page) => !isPaperNote(page),
    }),
    Component.ConditionalRender({
      component: Component.DesktopOnly(Component.TableOfContents()),
      condition: (page) => !isPaperNote(page),
    }),
    Component.ConditionalRender({
      component: Component.Backlinks(),
      condition: (page) => !isPaperNote(page),
    }),
  ],
  afterBody: [
    Component.ConditionalRender({
      component: Component.RecentNotes({
        title: "Recently Updated",
        limit: 10,
        showTags: false,
        dateType: "modified",
        filter: (f) => f.slug?.startsWith("notes/") ?? false,
      }),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.RecentNotes({
        title: "Recently Added",
        limit: 10,
        showTags: false,
        dateType: "created",
        filter: (f) => f.slug?.startsWith("notes/") ?? false,
      }),
      condition: (page) => page.fileData.slug === "index",
    }),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer(),
  ],
  right: [],
}
