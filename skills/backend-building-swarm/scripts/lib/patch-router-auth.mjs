// Patches router.ts to add auth sub-router.
// Usage: node patch-router-auth.mjs <project-path>
//
// Inserts import and auth route. Idempotent.

import fs from "fs";

const projectPath = process.argv[2];
if (!projectPath) {
  console.error("Usage: node patch-router-auth.mjs <project-path>");
  process.exit(1);
}

const routerPath = projectPath + "/api/router.ts";
if (!fs.existsSync(routerPath)) {
  console.error("Error: " + routerPath + " not found");
  process.exit(1);
}

let src = fs.readFileSync(routerPath, "utf8");

if (src.includes("authRouter")) {
  process.exit(0);
}

// Add import for authRouter after last import line
const lastImportIndex = src.lastIndexOf("\nimport ");
if (lastImportIndex === -1) {
  // No imports found, add at beginning
  src = 'import { authRouter } from "./auth-router";\n' + src;
} else {
  const lineEnd = src.indexOf("\n", lastImportIndex + 1);
  src =
    src.slice(0, lineEnd + 1) +
    'import { authRouter } from "./auth-router";\n' +
    src.slice(lineEnd + 1);
}

// Add auth route after the ping line
// Find the line with `ping:` and insert auth route on the next line
const lines = src.split("\n");
const pingIdx = lines.findIndex((l) => /^\s*ping:/.test(l));
if (pingIdx !== -1) {
  // Ensure ping line has trailing comma
  lines[pingIdx] = lines[pingIdx].replace(/,?\s*$/, ",");
  lines.splice(pingIdx + 1, 0, "  auth: authRouter,");
  src = lines.join("\n");
}

fs.writeFileSync(routerPath, src);
