// Merges a table definition file into db/schema.ts.
// Usage: node merge-schema.mjs <project-path> <table-file>
//
// Prepends the table definition. Idempotent: skips if table name already exists.
// Also merges imports from the table file into existing imports.

import fs from "fs";

const projectPath = process.argv[2];
const tableFile = process.argv[3];
if (!projectPath || !tableFile) {
  console.error("Usage: node merge-schema.mjs <project-path> <table-file>");
  process.exit(1);
}

const schemaPath = projectPath + "/db/schema.ts";
if (!fs.existsSync(schemaPath)) {
  console.error("Error: " + schemaPath + " not found");
  process.exit(1);
}

const tableSrc = fs.readFileSync(tableFile, "utf8");
let schemaSrc = fs.readFileSync(schemaPath, "utf8");

// Extract table name from `export const <name> = mysqlTable(`
const tableNameMatch = tableSrc.match(
  /export\s+const\s+(\w+)\s*=\s*mysqlTable\(/
);
if (!tableNameMatch) {
  console.error("Error: Could not find table definition in " + tableFile);
  process.exit(1);
}
const tableName = tableNameMatch[1];

if (schemaSrc.includes("const " + tableName + " ")) {
  process.exit(0);
}

// Extract imports from table file
const tableImports = [];
const tableImportRe = /^import\s+\{([^}]+)\}\s+from\s+["']([^"']+)["'];?\s*$/gm;
let match;
while ((match = tableImportRe.exec(tableSrc)) !== null) {
  const names = match[1].split(",").map((s) => s.trim()).filter(Boolean);
  const from = match[2];
  tableImports.push({ names, from });
}

// Merge imports into schema
for (const { names, from } of tableImports) {
  const existingRe = new RegExp(
    "import\\s*\\{([^}]*)\\}\\s*from\\s*[\"']" +
      from.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
      "[\"']"
  );
  const existingMatch = schemaSrc.match(existingRe);

  if (existingMatch) {
    const existingNames = existingMatch[1]
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const newNames = names.filter((n) => !existingNames.includes(n));
    if (newNames.length > 0) {
      const allNames = [...existingNames, ...newNames];
      const newImport =
        "import {\n  " +
        allNames.join(",\n  ") +
        ',\n} from "' +
        from +
        '";';
      // Replace the matched import statement (including optional semicolon)
      const fullMatchRe = new RegExp(
        "import\\s*\\{[^}]*\\}\\s*from\\s*[\"']" +
          from.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
          "[\"'];?"
      );
      schemaSrc = schemaSrc.replace(fullMatchRe, newImport);
    }
  }
}

// Get table definition body (everything after the last import block)
const tableLines = tableSrc.split("\n");
let lastImportEnd = 0;
for (let i = 0; i < tableLines.length; i++) {
  if (/^\s*from\s+["']/.test(tableLines[i]) || /\bfrom\s+["'][^"']+["']/.test(tableLines[i])) {
    lastImportEnd = i + 1;
  }
}
let tableBody = tableLines.slice(lastImportEnd).join("\n").trim();

// Insert table definition after the last import in schema, before the TODO comment or at the end
const todoIndex = schemaSrc.indexOf("// TODO:");
if (todoIndex !== -1) {
  schemaSrc =
    schemaSrc.slice(0, todoIndex) +
    tableBody +
    "\n\n" +
    schemaSrc.slice(todoIndex);
} else {
  schemaSrc = schemaSrc.trimEnd() + "\n\n" + tableBody + "\n";
}

fs.writeFileSync(schemaPath, schemaSrc);
