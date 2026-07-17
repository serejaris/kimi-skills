// Auto-wires TRPCProvider into src/main.tsx.
// Usage: node wire-main-tsx.mjs <project-path>
//
// Injects `import { TRPCProvider }` and wraps content inside
// <BrowserRouter> with <TRPCProvider>.
// Exits 0 if already wired or successfully patched.
// Exits 1 if <BrowserRouter> anchor not found (manual wiring needed).

import fs from "fs";

const projectPath = process.argv[2];
if (!projectPath) {
  console.error("Usage: node wire-main-tsx.mjs <project-path>");
  process.exit(1);
}

const mainPath = projectPath + "/src/main.tsx";
if (!fs.existsSync(mainPath)) process.exit(1);

let src = fs.readFileSync(mainPath, "utf8");

if (src.includes("TRPCProvider")) process.exit(0);
if (!src.includes("<BrowserRouter>")) process.exit(1);

// Add import before the App import line
const appImportRe = /^(import\s+App\s+from\s+.+)$/m;
if (appImportRe.test(src)) {
  src = src.replace(
    appImportRe,
    'import { TRPCProvider } from "@/providers/trpc"\n$1'
  );
} else {
  src = src.replace(
    /(import\s+.+\n)(?!import)/,
    '$1import { TRPCProvider } from "@/providers/trpc"\n'
  );
}

// Wrap content inside <BrowserRouter> with <TRPCProvider>
const brMatch = src.match(/^(\s*)<BrowserRouter>/m);
const brIndent = brMatch ? brMatch[1] : "    ";
const innerIndent = brIndent + "  ";

src = src.replace(
  /(<BrowserRouter>)\n/,
  "$1\n" + innerIndent + "<TRPCProvider>\n"
);
src = src.replace(
  /\n(\s*)(<\/BrowserRouter>)/,
  "\n" + innerIndent + "</TRPCProvider>\n$1$2"
);

// Re-indent content between <TRPCProvider> and </TRPCProvider>
const lines = src.split("\n");
let inProvider = false;
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("<TRPCProvider>")) { inProvider = true; continue; }
  if (lines[i].includes("</TRPCProvider>")) { inProvider = false; continue; }
  if (inProvider && lines[i].trim()) lines[i] = "  " + lines[i];
}
src = lines.join("\n");

fs.writeFileSync(mainPath, src);
