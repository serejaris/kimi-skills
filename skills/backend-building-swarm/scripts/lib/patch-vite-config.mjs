// Patches vite.config.ts in-place to add backend-required config.
// Usage: node patch-vite-config.mjs <project-path>
//
// Adds: path import, __dirname shim, @contracts alias, envDir, build.outDir,
//       @hono/vite-dev-server plugin, server.port
// Removes: base: "./" (Hono serves from "/")
//
// Exits NON-ZERO if a *critical* transform could neither be found already nor
// applied (e.g. a non-standard vite.config.ts whose anchors don't match), so the
// caller (init.sh) can fall back to a full vite.config.ts replacement.

import fs from "fs";

const projectPath = process.argv[2];
if (!projectPath) {
  console.error("Usage: node patch-vite-config.mjs <project-path>");
  process.exit(1);
}

const dest = projectPath + "/vite.config.ts";
if (!fs.existsSync(dest)) {
  process.exit(0);
}

let src = fs.readFileSync(dest, "utf8");
let changed = false;
const failures = [];

// Apply a transform unless it's already present. `have` detects already-present;
// `fn` returns the transformed source. Sets `changed` only when src actually
// changes; records a failure (for `critical` transforms) when neither present
// nor applied — so we never report success on a no-op patch.
function apply(label, have, fn, { critical = false } = {}) {
  if (have.test(src)) return;
  const next = fn(src);
  if (next !== src) {
    src = next;
    changed = true;
  } else if (critical) {
    failures.push(label);
  }
}

// 1. Ensure `import path from "path"` exists
apply("path-import", /\bimport\s+path\s+from\s+["']path["']/,
  (s) => 'import path from "path"\n' + s);

// 2. ESM __dirname shim — inject after path import if missing
apply("dirname-shim", /\bimport\.meta\.dirname\b/,
  (s) => s.replace(/(import\s+path\s+from\s+["']path["'].*\n)/, "$1const __dirname = import.meta.dirname\n"));

// 3. Remove `base: "./"` (Hono needs default "/")
const baseRe = /^\s*base:\s*["']\.?\/?["'],?[ \t]*\n?/m;
if (baseRe.test(src)) {
  src = src.replace(baseRe, "");
  changed = true;
}

// 4. Add @contracts alias into existing alias block (critical — cross-boundary imports)
apply("contracts-alias", /@contracts/,
  (s) => s.replace(/("@":\s*path\.resolve\([^)]+\)),?\s*\n/,
    '$1,\n      "@contracts": path.resolve(__dirname, "./contracts"),\n'),
  { critical: true });

// 4b. Add @db and db aliases into existing alias block
apply("db-alias", /"@?db"/,
  (s) => s.replace(/("@contracts":\s*path\.resolve\([^)]+\)),?\s*\n/,
    '$1,\n      "@db": path.resolve(__dirname, "./db"),\n      "db": path.resolve(__dirname, "./db"),\n'));

// 5. Add envDir if missing (critical — .env loading)
apply("envDir", /\benvDir\b/,
  (s) => s.replace(/(\n)(}\);?\s*$)/m, "$1  envDir: path.resolve(__dirname),\n$2"),
  { critical: true });

// 6. Add build.outDir if missing (critical — Hono serves dist/public)
apply("build-outDir", /\bbuild\s*:/,
  (s) => s.replace(/(\n)(}\);?\s*$)/m,
    '$1  build: {\n    outDir: path.resolve(__dirname, "dist/public"),\n    emptyOutDir: true,\n  },\n$2'),
  { critical: true });

// 7. Add @hono/vite-dev-server import if missing (critical)
apply("devserver-import", /devServer/,
  (s) => 'import devServer from "@hono/vite-dev-server"\n' + s,
  { critical: true });

// 8. Add devServer plugin to plugins array if missing (critical — dev server entry)
apply("devserver-plugin", /devServer\(/,
  (s) => s.replace(/(plugins:\s*\[)\s*/,
    '$1\n    devServer({ entry: "api/boot.ts", exclude: [/^\\/(?!api\\/).*$/] }),\n    '),
  { critical: true });

// 9. Add server.port if no server block exists
apply("server-port", /\bserver\s*:/,
  (s) => s.replace(/(\n)(}\);?\s*$)/m, '$1  server: {\n    port: 3000,\n    allowedHosts: true,\n  },\n$2'));

if (changed) {
  fs.writeFileSync(dest, src);
}

if (failures.length > 0) {
  console.error("patch-vite-config: critical transforms did not apply: " + failures.join(", "));
  process.exit(1);
}
