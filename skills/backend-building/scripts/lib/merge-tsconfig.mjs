// Merges backend tsconfig entries into the existing project tsconfigs.
// Usage: node merge-tsconfig.mjs <project-path>
//
// Patches:
//   tsconfig.json     — adds server reference + @contracts/*, @db/* paths
//   tsconfig.app.json — adds @contracts/*, @db/* paths + "node" types

import fs from "fs";

const dir = process.argv[2];
if (!dir) {
  console.error("Usage: node merge-tsconfig.mjs <project-path>");
  process.exit(1);
}

function readJsonc(path) {
  const text = fs
    .readFileSync(path, "utf8")
    .split("\n")
    .map((line) => {
      const t = line.trimStart();
      if (t.startsWith("//")) return "";
      if (t.startsWith("/*") && t.trimEnd().endsWith("*/")) return "";
      return line;
    })
    .join("\n")
    .replace(/,\s*([\]}])/g, "$1");
  return JSON.parse(text);
}

// 1. Patch root tsconfig.json
const rootPath = dir + "/tsconfig.json";
const root = readJsonc(rootPath);

if (!root.references) root.references = [];
const hasServerRef = root.references.some(
  (r) => r.path === "./tsconfig.server.json"
);
if (!hasServerRef) root.references.push({ path: "./tsconfig.server.json" });

if (!root.compilerOptions) root.compilerOptions = {};
if (!root.compilerOptions.paths) root.compilerOptions.paths = {};
root.compilerOptions.paths["@contracts/*"] = ["./contracts/*"];
root.compilerOptions.paths["@db/*"] = ["./db/*"];

fs.writeFileSync(rootPath, JSON.stringify(root, null, 2) + "\n");

// 2. Patch tsconfig.app.json
const appPath = dir + "/tsconfig.app.json";
if (fs.existsSync(appPath)) {
  const app = readJsonc(appPath);
  if (!app.compilerOptions) app.compilerOptions = {};
  if (!app.compilerOptions.paths) app.compilerOptions.paths = {};
  app.compilerOptions.paths["@contracts/*"] = ["./contracts/*"];
  app.compilerOptions.paths["@db/*"] = ["./db/*"];
  if (!app.compilerOptions.baseUrl) app.compilerOptions.baseUrl = ".";
  // "node" types needed because src/providers/trpc.tsx imports type from
  // api/router.ts, which transitively pulls in Node.js types
  if (!app.compilerOptions.types) app.compilerOptions.types = [];
  if (!app.compilerOptions.types.includes("node")) {
    app.compilerOptions.types.push("node");
  }
  fs.writeFileSync(appPath, JSON.stringify(app, null, 2) + "\n");
}
