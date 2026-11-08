// Layout test for paper notes (spec section 11.3): open each page of a built
// Quartz site in Chromium at several widths and measure the margin notes.
//
//   node _tools/node/layout_check.mjs <site dir> <out dir> <page path>...
//
// For every page and width it reports margin notes overlapping main-column
// blocks, margin notes overlapping each other, and horizontal scrolling; all
// must be zero. It also writes a screenshot of each page at 1280 px.
import { createRequire } from "node:module"
import http from "node:http"
import fs from "node:fs"
import path from "node:path"

const require = createRequire(import.meta.url)
const { chromium } = require("playwright")

const [siteDir, outDir, ...pages] = process.argv.slice(2)
if (!siteDir || !outDir || pages.length === 0) {
  console.error("usage: node layout_check.mjs <site dir> <out dir> <page path>...")
  process.exit(2)
}
const WIDTHS = [1440, 1280, 1024, 761, 760, 390]
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2" }

function serve(root) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let rel = decodeURIComponent(new URL(req.url, "http://x").pathname)
      let file = path.join(root, rel)
      if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html")
      else if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html"
      if (!fs.existsSync(file)) {
        res.writeHead(404)
        res.end()
        return
      }
      res.writeHead(200, { "content-type": TYPES[path.extname(file)] ?? "application/octet-stream" })
      fs.createReadStream(file).pipe(res)
    })
    server.listen(0, "127.0.0.1", () => resolve(server))
  })
}

const measure = () => {
  const article = document.querySelector("article.paper-margin")
  if (!article) return { error: "no article.paper-margin on the page" }
  const isMargin = (el) => el.matches('.callout[data-callout-metadata~="margin"]')
  const children = [...article.children]
  const notes = children.filter(isMargin)
  const main = children.filter((el) => !isMargin(el) && el.getBoundingClientRect().height > 0)
  const box = (el) => el.getBoundingClientRect()
  const overlap = (a, b) => a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5
  const label = (el) => (el.textContent || "").trim().slice(0, 50)
  const noteText = []
  const noteNote = []
  notes.forEach((note, i) => {
    const a = box(note)
    main.forEach((block) => {
      if (overlap(a, box(block))) noteText.push(`${label(note)} ↔ ${label(block)}`)
    })
    notes.slice(i + 1).forEach((other) => {
      if (overlap(a, box(other))) noteNote.push(`${label(note)} ↔ ${label(other)}`)
    })
  })
  const doc = document.documentElement
  const articleWidth = article.getBoundingClientRect().width
  const floated = notes.length > 0 && getComputedStyle(notes[0]).float === "right"
  return {
    articleWidth: Math.round(articleWidth),
    notes: notes.length,
    floated,
    noteText,
    noteNote,
    horizontalScroll: doc.scrollWidth > doc.clientWidth + 1,
  }
}

const server = await serve(path.resolve(siteDir))
const base = `http://127.0.0.1:${server.address().port}/`
const browser = await chromium.launch()
fs.mkdirSync(outDir, { recursive: true })
let failures = 0
const report = []
for (const pagePath of pages) {
  for (const width of WIDTHS) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1 })
    const errors = []
    page.on("pageerror", (error) => errors.push(String(error)))
    await page.goto(base + pagePath, { waitUntil: "networkidle" })
    const result = await page.evaluate(measure)
    result.page = pagePath
    result.width = width
    result.errors = errors
    const bad = result.error || result.noteText?.length || result.noteNote?.length || result.horizontalScroll || errors.length
    if (bad) failures += 1
    report.push(result)
    console.log(
      `${bad ? "FAIL" : "ok  "} ${pagePath} @${width}px article ${result.articleWidth}px, ${result.notes} notes ${result.floated ? "in margin" : "inline"}` +
        (result.error ? ` — ${result.error}` : "") +
        (result.noteText?.length ? ` — note/text overlaps: ${result.noteText.join("; ")}` : "") +
        (result.noteNote?.length ? ` — note/note overlaps: ${result.noteNote.join("; ")}` : "") +
        (result.horizontalScroll ? " — horizontal scroll" : "") +
        (errors.length ? ` — page errors: ${errors.join("; ")}` : ""),
    )
    if (width === 1280) {
      const name = pagePath.replace(/[^A-Za-z0-9]+/g, "_")
      await page.screenshot({ path: path.join(outDir, `${name}-${width}.png`), fullPage: true })
    }
    await page.close()
  }
}
fs.writeFileSync(path.join(outDir, "layout-report.json"), JSON.stringify(report, null, 1))
await browser.close()
server.close()
console.log(failures ? `${failures} layout failures` : "layout: 0 overlaps, no horizontal scroll")
process.exit(failures ? 1 : 0)
