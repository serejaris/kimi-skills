// Patches vite.config.ts in-place to add backend-required config.
// Usage: node patch-vite-config.mjs <project-path>
//
// Adds: path import, __dirname shim, @contracts alias, envDir, build.outDir,
//       @hono/vite-dev-server plugin, server.port
// Removes: base: "./" (Hono serves from "/")

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

// 1. Ensure `import path from "path"` exists
if (!/\bimport\s+path\s+from\s+["']path["']/.test(src)) {
  src = 'import path from "path"\n' + src;
  changed = true;
}

// 2. ESM __dirname shim — inject after path import if missing
if (!/\bimport\.meta\.dirname\b/.test(src)) {
  src = src.replace(
    /(import\s+path\s+from\s+["']path["'].*\n)/,
    "$1const __dirname = import.meta.dirname\n"
  );
  changed = true;
}

// 3. Remove `base: "./"` (Hono needs default "/")
const baseRe = /^\s*base:\s*["']\.?\/?["'],?[ \t]*\n?/m;
if (baseRe.test(src)) {
  src = src.replace(baseRe, "");
  changed = true;
}

// 4. Add @contracts alias into existing alias block
if (!/@contracts/.test(src)) {
  const aliasInsert = src.replace(
    /("@":\s*path\.resolve\([^)]+\)),?\s*\n/,
    '$1,\n      "@contracts": path.resolve(__dirname, "./contracts"),\n'
  );
  if (aliasInsert !== src) {
    src = aliasInsert;
    changed = true;
  }
}

// 4b. Add @db and db aliases into existing alias block
if (!/"@?db"/.test(src)) {
  const dbInsert = src.replace(
    /("@contracts":\s*path\.resolve\([^)]+\)),?\s*\n/,
    '$1,\n      "@db": path.resolve(__dirname, "./db"),\n      "db": path.resolve(__dirname, "./db"),\n'
  );
  if (dbInsert !== src) {
    src = dbInsert;
    changed = true;
  }
}

// 5. Add envDir if missing
if (!/\benvDir\b/.test(src)) {
  src = src.replace(
    /(\n)(}\);?\s*$)/m,
    "$1  envDir: path.resolve(__dirname),\n$2"
  );
  changed = true;
}

// 6. Add build.outDir if missing
if (!/\bbuild\s*:/.test(src)) {
  src = src.replace(
    /(\n)(}\);?\s*$)/m,
    '$1  build: {\n    outDir: path.resolve(__dirname, "dist/public"),\n    emptyOutDir: true,\n  },\n$2'
  );
  changed = true;
}

// 7. Add @hono/vite-dev-server import if missing
if (!/devServer/.test(src)) {
  src = 'import devServer from "@hono/vite-dev-server"\n' + src;
  changed = true;
}

// 8. Add devServer plugin to plugins array if missing
if (!/devServer\(/.test(src)) {
  src = src.replace(
    /(plugins:\s*\[)\s*/,
    '$1\n    devServer({ entry: "api/boot.ts", exclude: [/^\\/(?!api\\/).*$/] }),\n    ',
  );
  changed = true;
}

// 9. Add server.port if no server block exists
if (!/\bserver\s*:/.test(src)) {
  src = src.replace(
    /(\n)(}\);?\s*$)/m,
    '$1  server: {\n    port: 3000,\n    allowedHosts: true,\n  },\n$2'
  );
  changed = true;
}

if (changed) {
  fs.writeFileSync(dest, src);
}
