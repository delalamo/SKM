// Parse every equation the validator sends with KaTeX, the renderer Quartz uses.
// Usage: node katex_check.mjs <path-to-katex-package>  (JSON array on stdin)
// Input items: {"id": any, "tex": string, "display": bool}
// Output: JSON array of {"id", "error"} for equations that fail to parse.
import { createRequire } from "node:module"
import path from "node:path"

const katexDir = process.argv[2]
if (!katexDir) {
  console.error("usage: node katex_check.mjs <katex package dir>")
  process.exit(2)
}
const require = createRequire(import.meta.url)
const katex = require(path.resolve(katexDir))

let input = ""
process.stdin.setEncoding("utf8")
for await (const chunk of process.stdin) input += chunk
const items = JSON.parse(input || "[]")
const failures = []
for (const item of items) {
  try {
    katex.renderToString(item.tex, { displayMode: Boolean(item.display), throwOnError: true, strict: "ignore" })
  } catch (error) {
    failures.push({ id: item.id, error: String(error.message || error).split("\n")[0] })
  }
}
process.stdout.write(JSON.stringify(failures))
