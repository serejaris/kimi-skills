// Patches api/lib/env.ts to add new environment variable properties.
// Usage: node patch-env-ts.mjs <project-path> '<json-fragment>'
//
// Example: node patch-env-ts.mjs /app '{"databaseUrl":"required(\"DATABASE_URL\")"}'
// Idempotent: skips properties that already exist.

import fs from "fs";

const projectPath = process.argv[2];
const jsonFragment = process.argv[3];
if (!projectPath || !jsonFragment) {
  console.error(
    'Usage: node patch-env-ts.mjs <project-path> \'<json-fragment>\''
  );
  process.exit(1);
}

const envPath = projectPath + "/api/lib/env.ts";
if (!fs.existsSync(envPath)) {
  console.error("Error: " + envPath + " not found");
  process.exit(1);
}

let src = fs.readFileSync(envPath, "utf8");
const props = JSON.parse(jsonFragment);
let changed = false;

for (const [key, value] of Object.entries(props)) {
  if (src.includes(key + ":")) continue;

  // Find the last `};` in the file (closes the env object)
  const lastClosingIdx = src.lastIndexOf("};");
  if (lastClosingIdx === -1) continue;

  src =
    src.slice(0, lastClosingIdx) +
    "  " + key + ": " + value + ",\n" +
    src.slice(lastClosingIdx);
  changed = true;
}

if (changed) {
  fs.writeFileSync(envPath, src);
}
