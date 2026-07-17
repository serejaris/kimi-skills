# Markdown → Word Citation Reference

Convert Markdown documents with citation markers into Word documents with footnotes, endnotes, or hyperlink cross-references.

## Quick Start

```bash
python3 scripts/md2docx/md2docx_convert.py <markdown_file> \
    --citation /mnt/agents/.store/citation.jsonl \
    --style <footnote|endnote|hyperlink> \
    --output-dir <output-dir>
```

## When to Use

Use this pipeline when Markdown is the intended source for a new Word document. It handles agent-produced Markdown citation markers and is also the required handoff for Orchestrator/Swarm, user-requested md2docx, and Markdown-first upstream skills such as Deep Research. Do not bypass it with a bare `pandoc -o final.docx` call.

Run the command from the DOCX Skill directory or resolve `scripts/md2docx/md2docx_convert.py` from that directory. A supplied `final.md` is the canonical report body; conversion may change presentation but must not rewrite its content or source IDs.

## Style Selection

| Style | Use Case | Citation Location |
|-------|----------|-------------------|
| **footnote** | Research reports, policy analysis, general reports | Page bottom (per page) |
| **endnote** | Academic papers, books, long scholarly documents | End of document (consolidated) |
| **hyperlink** | WPS compatibility only | Reference list at end of body |

**Default**: Use **footnote** for most scenarios. Use **endnote** for academic papers.

## Parameters

```
python3 scripts/md2docx/md2docx_convert.py <md_file> [options]

Required:
  md_file              Path to Markdown file

Required:
  --citation PATH      Path to citation.jsonl

Optional:
  --style STYLE        footnote / endnote / hyperlink (default: footnote)
  --output-dir DIR     Output directory (environment-specific, specify explicitly)
```

## Pre-Invocation Checklist

### 1. citation.jsonl

In the agent container, citation data is stored at:

`/mnt/agents/.store/citation.jsonl`

If a citation JSONL is supplied with the Markdown, pass that exact file. Otherwise, in the agent container use `--citation /mnt/agents/.store/citation.jsonl`. For local regression fixtures or exported workspaces, use the paired `.citation.jsonl` or `citation.jsonl` supplied with the Markdown.

Each line is a JSON object:
```json
{"id": 123, "url": "https://example.com", "page": {"site_name": "Example Site"}}
```

### 2. Image Paths

Agent-produced MD may contain absolute paths (e.g., `/some/container/path/xxx.png`) that don't exist in the current environment. Check and fix before conversion:

```bash
grep -oE '!\[.*?\]\(.*?\)' document.md | head -10
# Replace absolute path prefix with relative — adjust prefix based on your environment
sed -i '' 's|/path/to/remove/||g' document.md
```

### 3. Citation Format

Three formats auto-detected (priority descending):

| Tier | Pattern | Confidence | Behavior |
|------|---------|------------|----------|
| T1 | `[^123^]` | High | Direct conversion |
| T2 | `[^123]` | Medium | Compat conversion |
| T3 | `[123]` | Low | DB cross-validation required (>50% hit rate, >5 matches) |

## Pipeline

```
Markdown + citation.jsonl
    │
    ├─ 1. Citation format detection (T1→T2→T3 tiered fallback)
    ├─ 2. Renumber by first-appearance order → ^N^ superscripts
    ├─ 3. Edge case detection (non-numeric citations → WARNING only)
    │
    ├─ 4. Pandoc → base.docx
    │
    └─ 5. OOXML post-processing (branched by style)
         ├─ footnote: first → footnote object, subsequent → NOTEREF
         ├─ endnote:  first → endnote object, subsequent → NOTEREF
         └─ hyperlink: REF field → bibliography bookmark
```

## Output Files

- `{name}.{style}.docx` — Final Word document
- `{name}.converted.md` — Intermediate Markdown (citations → `^N^` superscripts)
- `{name}.base.docx` — Pandoc raw output (intermediate)

## Technical Details

- **UTF-8 gate**: The converter rejects invalid UTF-8 and CJK Markdown double-encoded through latin-1 before Pandoc runs; repair or regenerate the Markdown instead of forcing a lossy fallback.
- **Numbering**: Source IDs in Markdown remain immutable for lookup. Word note numbers are separate display ordinals assigned by first appearance.
- **Dedup**: Same citation ID appearing multiple times → one note, subsequent uses NOTEREF
- **Clickable**: Superscript numbers link to corresponding footnote/endnote
- **Edge cases**: Non-numeric IDs (`[^Insight6^]`) → escaped in the intermediate Markdown so their visible marker text is preserved; non-numeric footnote definitions render as literal text rather than Pandoc footnotes
- **Missing**: Citation IDs not in DB → preserved in their original marker format and logged as warnings; never silently delete evidence pointers
- **Feedback state**: Errors require a corrected retry. Preserve every warning in context and either resolve it or report it with the delivered file; never fabricate mappings, delete markers, or hide conversion feedback.
- **Validation scope**: Successful md2docx conversion, a cleanly opening DOCX package, and visual rendering are the acceptance checks for this route. Do not call the C# Create route's `./scripts/docx validate` entry point for md2docx output.

## Dependencies

- **Pandoc**: `apt install pandoc`
- **python-docx**: `pip install python-docx`
- **lxml**: `pip install lxml`

## Code Structure

```
scripts/md2docx/
├── md2docx_convert.py   # Main pipeline
├── citation_parser.py   # Citation detection (T1/T2/T3), renumbering, replacement
├── docx_footnote.py     # Footnote OOXML post-processing
├── docx_endnote.py      # Endnote OOXML post-processing
├── docx_postprocess.py  # Hyperlink post-processing (python-docx)
└── docx_utils.py        # Shared: rels/content_types updates
```

---

## Reference Entry Points

- For overall routing: `../SKILL.md`
- For creating new documents: `openxml-sdk-reference.md`
- For editing existing documents: `wir-reference.md`
- For matplotlib charts: `matplotlib-guide.md`
