// Merges backend dependencies and scripts into the existing package.json.
// Usage: node merge-package-json.mjs <project-path> <backend-package-json>
//
// - Sets type: "module"
// - Merges scripts (backend overrides existing)
// - Merges deps (additive, does not overwrite existing versions)

import fs from "fs";

const projectPath = process.argv[2];
const backendPkgPath = process.argv[3];
if (!projectPath || !backendPkgPath) {
  console.error(
    "Usage: node merge-package-json.mjs <project-path> <backend-package-json>"
  );
  process.exit(1);
}

const appPkg = JSON.parse(
  fs.readFileSync(projectPath + "/package.json", "utf8")
);
const backend = JSON.parse(fs.readFileSync(backendPkgPath, "utf8"));

appPkg.type = "module";

appPkg.scripts = { ...(appPkg.scripts || {}), ...backend.scripts };

for (const section of ["dependencies", "devDependencies"]) {
  if (!appPkg[section]) appPkg[section] = {};
  if (backend[section]) {
    for (const [pkg, ver] of Object.entries(backend[section])) {
      if (!appPkg[section][pkg]) appPkg[section][pkg] = ver;
    }
  }
}

fs.writeFileSync(
  projectPath + "/package.json",
  JSON.stringify(appPkg, null, 2) + "\n"
);
