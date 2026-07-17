// Auto-wires Login and NotFound routes into src/App.tsx.
// Usage: node wire-app-tsx.mjs <project-path>
//
// Adds import statements and <Route> entries for Login and NotFound pages.
// Exits 0 if already wired or successfully patched.
// Exits 1 if </Routes> anchor not found (manual wiring needed).

import fs from "fs";

const projectPath = process.argv[2];
if (!projectPath) {
  console.error("Usage: node wire-app-tsx.mjs <project-path>");
  process.exit(1);
}

const appPath = projectPath + "/src/App.tsx";
if (!fs.existsSync(appPath)) process.exit(1);

let src = fs.readFileSync(appPath, "utf8");

if (src.includes("Login")) process.exit(0);
if (!src.includes("</Routes>")) process.exit(1);

// Add imports: find the last existing page import and add after it
const pageImportRe =
  /^(import\s+\w+\s+from\s+["']\.\/pages\/.+["'].*\n)(?!import\s+\w+\s+from\s+["']\.\/pages\/)/m;
if (pageImportRe.test(src)) {
  src = src.replace(
    pageImportRe,
    '$1import Login from "./pages/Login"\nimport NotFound from "./pages/NotFound"\n'
  );
} else {
  src = src.replace(
    /(import\s+.+\n)(?!import)/,
    '$1import Login from "./pages/Login"\nimport NotFound from "./pages/NotFound"\n'
  );
}

// Add routes before </Routes>
const routeIndentMatch = src.match(/^(\s*)<Route\s/m);
const routeIndent = routeIndentMatch ? routeIndentMatch[1] : "      ";
src = src.replace(
  /(\n)(\s*<\/Routes>)/,
  "$1" +
    routeIndent +
    '<Route path="/login" element={<Login />} />\n' +
    routeIndent +
    '<Route path="*" element={<NotFound />} />\n$2'
);

fs.writeFileSync(appPath, src);
