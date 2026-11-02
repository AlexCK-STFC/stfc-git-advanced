// Check the Mermaid diagrams in the lesson.
//
//   cd tools/check_diagrams && npm install
//   node check.mjs                  check every diagram (syntax + captions)
//   node check.mjs --render out/    also draw each one to out/<file>-<n>.png
//
// Rendering needs headless Chrome, which needs some system libraries
// (they are installed by .devcontainer/Dockerfile).
import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { JSDOM } from "jsdom";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const renderIdx = process.argv.indexOf("--render");
const renderDir = renderIdx > 0 ? path.resolve(process.argv[renderIdx + 1] || "diagram-images") : null;

// mermaid expects a browser, so give it a fake one
const dom = new JSDOM("<!DOCTYPE html><body></body>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, "navigator", { value: dom.window.navigator, configurable: true });
const mermaid = (await import("mermaid")).default;

// the Carpentries theme builds the figure caption from "accTitle: {...}", braces included
const needs = [
  [/accTitle: \{[^}]+\}/, "accTitle: {...} (with braces)"],
  [/accDescr: \{[^}]+\}/, "accDescr: {...} (with braces)"],
];

const files = ["episodes", "learners", "instructors", "profiles"].flatMap((dir) => {
  const full = path.join(root, dir);
  return fs.existsSync(full) ? fs.readdirSync(full).filter((f) => f.endsWith(".md")).map((f) => path.join(full, f)) : [];
});

if (renderDir) fs.mkdirSync(renderDir, { recursive: true });
let total = 0, failed = 0;

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  const blocks = [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)].map((m) => m[1]);
  const name = path.basename(file, ".md");
  for (const [i, code] of blocks.entries()) {
    total++;
    const label = `${name} #${i + 1}`;
    const problems = [];
    try { await mermaid.parse(code); } catch (e) { problems.push("syntax: " + String(e.message || e).split("\n").slice(0, 3).join(" ")); }
    for (const [re, what] of needs) if (!re.test(code)) problems.push("missing " + what);
    if (problems.length) { failed++; console.log("FAIL ", label, "\n      " + problems.join("\n      ")); continue; }
    console.log("ok   ", label);
    if (renderDir) {
      const mmd = path.join(renderDir, `${name}-${i + 1}.mmd`);
      fs.writeFileSync(mmd, code);
      const cfg = path.join(renderDir, "puppeteer.json");
      fs.writeFileSync(cfg, JSON.stringify({ args: ["--no-sandbox"] }));
      const r = spawnSync(path.join(here, "node_modules", ".bin", "mmdc"),
        ["-q", "-p", cfg, "-i", mmd, "-o", mmd.replace(/\.mmd$/, ".png"), "-b", "white", "-s", "1.5"], { encoding: "utf8" });
      if (r.status !== 0) { failed++; console.log("FAIL  render", label, (r.stderr || "").split("\n")[0]); }
      fs.unlinkSync(mmd);
    }
  }
}
console.log(`\n${total} diagrams, ${failed} problem(s)`);
process.exit(failed ? 1 : 0);
