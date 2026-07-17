# WIR Editing Reference

This document covers only **editing existing `.docx` files**. The public WIR workflow consists solely of:

1. `open`
2. `read`
3. `edit`
4. `save`

Do not discuss creating new documents here, do not introduce `python-docx`, and do not frame WIR as a tool-use mental model.

## Engine Interface

### Import Setup

The engine is at `docx/scripts/engine/`. Before importing, add `docx/scripts/` to Python path:

```python
import sys
sys.path.insert(0, '<path-to>/docx/scripts')  # same directory as ./scripts/docx
from engine import WIRSession
```

### Primary Interface — WIRSession (Recommended)

```python
from engine import WIRSession
from engine import TextEdit

session = WIRSession.open("/path/to/doc.docx")   # Open
w1, wir, next_cursor = session.read(part="document")  # Read
updated = session.edit(w1, [TextEdit(...)])        # Edit
session.save("/path/to/output.docx")               # Save
```

Context manager:
```python
with WIRSession.open("/path/to/doc.docx") as session:
    w1, wir, _ = session.read()
    session.edit(w1, [TextEdit(old_string="<r>original text</r>", new_string="<r>new text</r>")])
    session.save("/path/to/output.docx")
```

### Low-Level Functions

```python
from engine import (
    open_docx, read_wir, modify_wir, save_docx,
    TextEdit, validate_docx,
    CommentsManager, StyleManager, NumberingManager,
)
```

`StyleManager` exposes only four read-only `default_*_style_id` properties; it is not the entry point for editing style defaults. Use the styles view instead (see *Recipe E* in §6).

| Function | Purpose |
|------|------|
| `open_docx(path)` | Open an existing document, returns `DocxPackage` |
| `read_wir(package, part=..., cursor=..., limit=...)` | Read a WIR window |
| `modify_wir(package, base_wir=..., edits=[TextEdit(...)])` | Apply edits |
| `save_docx(package, output_path, namespace_guard_enabled=...)` | Save the document |
| `validate_docx(package)` | Validate document structure |

**Namespace Issue Handling**:

Some source documents may have incomplete namespace declarations (e.g., using the `w14` prefix without declaring it in `mc:Ignorable`). If you encounter an `E_NAMESPACE_IGNORABLE_MISSING_USED_PREFIX` error on save, you can disable the namespace check:

```python
# Using WIRSession
session.save(output_path, namespace_guard_enabled=False)

# Using low-level functions
save_docx(package, output_path, namespace_guard_enabled=False)
```

**When to Disable**:
- The source document itself has namespace issues
- You are only editing content and not adding new namespaces
- Word can open the source document normally (indicating the issue is minor)

**When NOT to Disable**:
- You are adding new extension features (e.g., Word 2013+ features)
- You need to ensure the document opens correctly in all Word versions

---

## 1. WIR Overview

### Core Purpose

WIR (Word Intermediate Representation) is a simplified representation of OOXML, capable of efficiently handling the vast majority of editing, commenting, and revision tracking tasks. Through `WIRSession`, it preserves template fidelity and complex OOXML structures.

### Hard Rules

1. Do not bypass WIR for manual zip/xml editing on existing business documents
2. Do not perform ad-hoc XML surgery on `word/*.xml`
3. Use absolute paths
4. Preserve user intent and document structure
5. Use incremental window editing for large documents
6. Save after editing
7. On warnings or errors, stop, re-read, then continue

### Core Workflow

```python
session = WIRSession.open(path)
w1, wir, next_cursor = session.read(part="document")
updated = session.edit(w1, [
    TextEdit(old_string="...", new_string="..."),
])
w1_new, wir_new, _ = session.read(part="document")
session.save(output_path)
```

### WIR Editing Guidelines

Follow these for each edit:
1. Default to reading `document` first; start with `<classes>` at the top of the window
2. Read additional parts only when needed: `comments`, `footnotes`, `endnotes`, `header:rIdX`, `footer:rIdX`, `prototypes`, `styles`
3. Group edits by logical intent and window; keep individual `TextEdit` anchors localized
4. Re-read after structural operations or when fresh keys are needed
5. Read `prototypes` for template fidelity; edit `styles` for style defaults across many paragraphs
6. Wrap paragraph text in `<r>...</r>` and save after editing

### WIR Capability List
- Rich text paragraph/run formatting (`attr`)
- Per-channel CJK + Latin font control (`ascii` / `hAnsi` / `eastAsia` / `cs`)
- Style-default editing via `part="styles"` — propagates to every referencing paragraph
- Batched edits: one `session.edit()` call may carry many `TextEdit`s
- Table structure editing and merging
- TOC insertion/update
- Hyperlink insertion (external/internal)
- Footnote/endnote insertion
- Header/footer story editing
- Comment editing and anchor control
- LaTeX formula to OMML conversion
- Image insertion and geometry updates

---

## 2. Opening a Document

### Open an Existing Document

```python
session = WIRSession.open("/absolute/path/to/doc.docx")
# Or low-level:
package = open_docx("/absolute/path/to/doc.docx")
```

### Key Rules
- Use absolute paths
- After opening (or re-opening), call `read` first to obtain an active cursor
- Cursors are session-scoped; do not reuse cursors from previous sessions
- Default to reading `document` first
- `prototypes` is for high-fidelity reuse
- `styles` is an advanced/debug view only, for when class semantics are insufficient or legacy key tracing is needed

*Formulas* — Write in LaTeX: `$x^2$` (inline) or `$$E=mc^2$$` (display). The engine automatically converts to Word-native OMML.

---

## 3. Reading WIR Windows

### Usage

```python
w1, wir, next_cursor = session.read(part="document")
# Pagination:
if next_cursor:
    w2, wir2, next2 = session.read(part="document", cursor=next_cursor)
```

Low-level:
```python
content, next_cursor = read_wir(package, part="document", cursor=None, limit=50)
```

### Available Parts

| part | Description | Editable? |
|------|------|------|
| `document` | Document body (supports windowed pagination) | Yes |
| `styles` | Style definitions, list/numbering linkage, legacy key map. Edit to change style defaults (see *Recipe E*). | Yes |
| `prototypes` | Reusable proto fragments | Read-only |
| `comments` | Comments | Yes |
| `footnotes` | Footnotes | Yes |
| `endnotes` | Endnotes | Yes |
| `header:rIdX` | Header | Yes |
| `footer:rIdX` | Footer | Yes |

### Workflow
1. Open the document
2. Read the target window/part
3. Edit that window using the cursor
4. Save

### Tips
- Short cursor IDs are stable within the same open session
- Use new cursors after re-opening
- Use `next_cursor` for pagination
- Each WIR fragment is paired with its own cursor
- After edits that insert/delete/move top-level blocks, re-read affected windows
- An empty document under the class-first view typically looks like:
  ```xml
  <classes>
    <class hint="Normal" name="normal" on="p"></class>
  </classes>
  <p k="P1" class="normal"></p>
  ```
  So do not assume the anchor is always a bare `<p k="P1"></p>` on the first edit

### WIR Format Notes
- Root format: `<wfrag v="3" part="..." cursor="...">`
- WIR is normalized: no self-closing tags, stable attribute order, 2-space indentation
- Under the class-first view, `<classes>` appears at the top of story windows
- `document` top-level blocks: `<p>`, `<table>`, `<section>`, `<toc>`, `<keep>`
- `footnotes`/`endnotes` top-level blocks: `<note id="...">`
- `styles` is primarily for debugging and compatibility mapping, not the default first view
- `prototypes` returns `<proto id="...">` fragments

### `<classes>` Metadata

`<classes>` is the core of the class-first view. It describes the most reusable semantic classes in the current window.

Common form:

```xml
<classes>
  <class name="normal" on="p" hint="Normal"></class>
  <class name="heading_2" on="p" hint="Heading 2"></class>
  <class name="run_1" on="r"></class>
</classes>
```

Rules:

- `on="p"` indicates a paragraph class
- `on="r"` indicates an inline class
- `on="tbl"` indicates a table class
- `name` is a class name you may **reference** from a `<p>` / `<r>` (via `class="..."`); it is not a renaming hook
- `hint` is a semantic hint; it may not always be present
- In some views, `<class>` may also carry `attr` / `runAttr` to indicate default block-level and default inline formatting

When editing, prefer reusing semantic classes listed here rather than looking for legacy `P/C/T/L` keys first.

**`<classes>` is read-only.** Modifying it raises `E_CLASSES_METADATA_EDITED`; to change defaults edit `part="styles"` (see *Recipe E* in §6), or edit a specific paragraph/run `attr` directly.

### Inserting Structural Content Without Heading Classes

When `<classes>` has no heading class (common in flat-style contracts/forms), do not fake headings with body-text class + minimal spacing. Use `attr` overrides that create clear visual separation:

```xml
<p attr="spacing-before:360;font-size:28;b:true;outline-level:0"><r>Chapter Title</r></p>
<p attr="spacing-before:240;font-size:24;b:true;outline-level:1"><r>Section Title</r></p>
```

Spacing reference (half-point values for `spacing-before`):
- Body text: 60–120 (3–6pt)
- Section heading: 240–480 (12–24pt)
- Chapter heading: 360–600 (18–30pt)

`font-size` should be 2–4 half-points larger than body text. Set `outline-level` so TOC can pick up the heading. If prototypes exist, prefer `proto` over hand-crafted attr — always check `read(part="prototypes")` first.

### WIR Inline Elements
- `<r>` — Text run. May carry `attr`: `<r attr="b:true;color:#FF0000">text</r>`
- `<img>` / `<image>` — Embedded image
- `<omml>` — OMML math formula. `<omml latex="E=mc^2">`
- `<hyperlink>` — Hyperlink. `url` (external) or `anchor` (internal bookmark)
- `<footnote>` / `<endnote>` — Inline footnote/endnote reference
- `<field>` — Field code
- `<toc>` — Table of contents block
- `<table>` — Table
- `<keep>` — Preserved opaque content (charts, complex drawings)

### Run `attr` Keys
`b` (bold), `i` (italic), `strike`, `font-size` (half-points), `font-size-cs` (complex-script half-points), `font-family`, `ascii` / `hAnsi` / `eastAsia` / `cs` (per-channel font overrides), `color` (`#RRGGBB` or `theme(<name>[,<modifier>])`), `highlight`, `shd`, `u` (underline), `caps`, `smallCaps`, `char-spacing` (twips, see below), `vert`, `rtl`

**Bilingual fonts (e.g. CJK Chinese body + Latin headings).** `font-family` is a shortcut that applies the same family to all four OOXML font channels. To use a different family for Chinese vs. Latin, set the per-channel keys explicitly:

```xml
<r attr="eastAsia:'黑体';ascii:'Times New Roman';hAnsi:'Times New Roman'">中文 plus English</r>
```

`eastAsia` covers CJK code points; `ascii` / `hAnsi` cover Latin; `cs` covers complex scripts (Arabic, Hebrew, etc.). The more-specific channel wins.

`char-spacing`: character spacing in twips (1/20 pt). Positive = expand, negative = condense. CJK large titles: `char-spacing:20` to `char-spacing:60` prevents cramped appearance. Original documents may have extreme negative values (-30 to -66) to force-fit text in narrow cells — when editing such text with longer replacements, consider resetting or widening `char-spacing`.

### Paragraph `attr` Keys
`jc` (alignment), `class` (style), `list`/`list-level`, `ind-left`/`ind-right`/`ind-first`/`ind-first-chars`/`ind-hanging`/`ind-hanging-chars`, `spacing-before`/`spacing-after`, `line-spacing`, `spacing-line-rule`, `keep-next`, `page-break-before`, `shd`, `outline-level`, `border-*`, `bidi`

#### Numeric units

All WIR `attr` numeric values are integer strings in OOXML-native units. Pass them verbatim; do not wrap in `python-docx` helpers (`Pt(...)`, `Cm(...)`, `Emu(...)`).

| Key | Unit | Example |
|---|---|---|
| `font-size`, `font-size-cs` | half-points (1/2 pt) | `24` (12 pt) |
| `spacing-before`, `spacing-after`, `char-spacing` | twips (1/20 pt) | `240` (12 pt) |
| `line-spacing` (with `spacing-line-rule=auto`/`exact`) | twips | `360` (1.5× on auto) |
| `ind-first`, `ind-left`, `ind-right`, `ind-hanging` | twips | `420` |
| `ind-first-chars`, `ind-hanging-chars` | OOXML character-unit indentation | `900` |
| `jc` | enum | `center` / `left` / `right` / `both` / `start` / `end` |
| `b`, `i`, `keep-next`, `page-break-before`, `bidi` | boolean | `true` / `false` |
| `color` | `#RRGGBB` / `theme(<name>[,<modifier>])`; valid names: `dark1`, `dark2`, `light1`, `light2`, `accent1`-`accent6`, `hyperlink`, `followedHyperlink`, `background1`, `background2`, `text1`, `text2` | `#FF6600` / `theme(accent1)` / `theme(accent1,80)` |
| `outline-level` | int 0-8 | `0` (chapter) |

Conversions: 1 pt = 2 half-points = 20 twips; 1 cm = 567 twips.

### Breaks

```xml
<p><r>first line</r><br /><r>second line</r></p>  <!-- line break -->
<p><br type="page" /></p>                           <!-- page break -->
<p><br type="column" /></p>                         <!-- column break -->
```

`type` supports: `page`, `column`. For layout changes (orientation, margins, columns, page numbering), use `<section>` instead.

### Section Properties

`<section>` controls page layout, pagination, and header/footer binding. It is a top-level story block.

Boundary semantics: each `<section>` starts a layout section; its attributes apply to the following content until the next `<section>` or document end.

```xml
<section sect="nextPage" pgW="11906" pgH="16838" orient="portrait"
         marTop="1440" marBottom="1440" marLeft="1800" marRight="1800" />
<p><r>content of this section</r></p>
```

| Attribute | Purpose | Example |
|---|---|---|
| `sect` | Break type used to enter this section from the previous one | `nextPage`, `continuous`, `evenPage`, `oddPage` |
| `pgW` / `pgH` | Page size (twips) | `11906` / `16838` (A4) |
| `orient` | Orientation | `portrait` / `landscape` |
| `marTop/Bottom/Left/Right` | Margins (twips) | `1440` (1 inch) |
| `pgNumFmt` | Page number format | `decimal`, `upperRoman`, `lowerLetter` |
| `pgNumStart` | Starting page number | `1` |
| `colNum` | Column count | `2` |
| `titlePg` | First page different | `1` |
| `hdrDefault` / `ftrDefault` | Header/footer binding | `rId10` |
| `context` | Set to `"true"` only on the read-only context section injected at the head of a mid-section window | `true` |

Rules:
- Use `<br type="page" />` for simple page breaks; use `<section>` only for layout changes such as orientation, margins, columns, page numbering, or header/footer binding
- To change layout for a block, place `<section attrs />` before that block; the layout continues until the next `<section>` or document end
- `sect` describes how this section is reached from the previous one; on the first `<section>` it has no effect
- Scoped layout changes need explicit section boundaries at both the start and the return point

Title / abstract single-column, body two-column:

```xml
<section colNum="1" />
<p><r>Title / abstract</r></p>
<section sect="continuous" colNum="2" />
<p><r>Body starts here (two columns)</r></p>
```

#### Window Context Section

When the window starts in the middle of a section (i.e., the section's `<section>` block lives in an earlier window), the engine prepends a read-only copy of that section marked with `context="true"`:

```xml
<section k="S2" context="true" sect="continuous" colNum="2" />
<p k="P10"><r>first paragraph of the window</r></p>
```

Rules for `context="true"` sections:
- Treat it as a snapshot of current layout, not as a newly inserted section
- Attribute edits apply to the underlying logical section; deleting it only omits the context copy
- To start a new section inside the window, add a fresh `<section ...>` block after the context section
- `context="true"` only appears in body window reads; do not handwrite it for full-document writes

### Fields

```xml
<field kind="PAGE"></field>       <!-- current page number -->
<field kind="NUMPAGES"></field>   <!-- total page count -->
```

Use fields in headers/footers for page numbers — never hard-code page numbers as text:

```xml
<p><r>Page </r><field kind="PAGE"></field><r> of </r><field kind="NUMPAGES"></field></p>
```

---

## 4. Editing WIR Content

### Usage

```python
updated = session.edit(w1, [
    TextEdit(old_string="<r>original text</r>", new_string="<r>new text</r>")
])
```

Low-level:
```python
updated_wir = modify_wir(
    package,
    base_wir=wir_content,
    edits=[TextEdit(old_string="...", new_string="...")],
    source_part="word/document.xml",
)
```

### Window Scope Rules
- `edit` only modifies the cached WIR for the given cursor
- Keep each `TextEdit` anchor within one window
- `old_string` approximately 80-400 characters per `TextEdit`; replace complete localized blocks
- Avoid single-character anchors or massive cross-page anchors
- Re-read affected windows after structural edits

#### Edits per `session.edit()` call

A single `edit()` call may carry any number of `TextEdit`s. Two regimes:

- **Localized intent** (fix a paragraph, insert a clause, repair a cell):
  1-3 edits per call, then re-read and verify.
- **Batch policy** (Recipe E, mass attr override, term replacement):
  30-80 edits per call is normal.

All `TextEdit`s in one call are applied in order in a single pass. If any
anchor fails to match, the whole call raises `E_OLD_NOT_FOUND`; no partial
writes.

### WIR Safety Rules
- `new_string` must be a valid XML fragment
- Text within `<p>` must be wrapped in `<r>...</r>`
- Allowed child elements of `<p>`: `<r>`, `<br>`, `<tab>`, `<keep>`, `<img>`, `<omml>`, `<hyperlink>`, `<textbox>`, `<group>`, `<shape>`, `<field>`, `<ins>`, `<del>`, `<footnote>`, `<endnote>`
- `<r>` is plain text: `<r>body text</r>`, do not nest tags inside
- Tags must be closed
- Do not explicitly set the `k` attribute on newly inserted nodes
- Must `save` after editing

### Run Formatting (`attr` on `<r>`)
```xml
<r attr="b:true;color:#FF0000">bold red text</r>
```
See Section 3 "Run `attr` Keys" for the full list of supported attributes.

### Paragraph Formatting (`attr` on `<p>`)
```xml
<p attr="jc:center;ind-first:420;spacing-before:120"><r>centered text</r></p>
```

For CJK documents, Word may store character-unit indentation as `ind-first-chars` or `ind-hanging-chars`. If a centered heading visually drifts, check for these keys. Setting `ind-first` clears stale `ind-first-chars` and hanging-indent residues unless the character-unit key is also explicitly present; setting `ind-hanging` clears stale first-line residues the same way.

### Edit Examples

Empty paragraph -> body text:
```
old: <p k="P1" class="normal"></p>
new: <p k="P1" class="normal"><r>body text</r></p>
```

Bold red:
```xml
<r attr="b:true;color:#FF0000">important content</r>
```

Centered paragraph:
```xml
<p attr="jc:center"><r>centered text</r></p>
```

Insert table:
```xml
<table><tr><td><p><r>A1</r></p></td><td><p><r>B1</r></p></td></tr></table>
```

Insert TOC:
```xml
<toc instr="TOC \o &quot;1-3&quot; \h \z \u"></toc>
```

Insert formula:
```xml
<omml latex="E=mc^2"></omml>
```

Insert image:
```xml
<image path="/path/to/img.png" width="400" height="300"></image>
```

Insert hyperlink:
```xml
<hyperlink url="https://example.com"><r>external link</r></hyperlink>
<hyperlink anchor="Section3"><r>internal bookmark link</r></hyperlink>
```

Insert footnote:
```xml
<p><r>statement text</r><footnote>supporting details.</footnote></p>
```

RTL / bidirectional text (Arabic, Hebrew, Persian, etc.):
The engine automatically preserves `<w:rtl/>` on runs and `<w:bidi/>` on paragraphs, and new runs inserted into an RTL paragraph (`bidi:true`) inherit RTL automatically. Use `rtl:false` only to mark an LTR fragment inside an RTL paragraph (e.g. an English citation):

```xml
<!-- English citation inside an Arabic sentence -->
<p attr="bidi:true"><r>نص عربي.</r><r attr="rtl:false">(Smith 2020)</r></p>
```

Delete a paragraph (replace with empty string):
```python
session.edit(w1, [TextEdit(
    old_string='<p k="P100" class="normal"><r>content to remove</r></p>',
    new_string=''
)])
```

Delete multiple consecutive paragraphs in one call:
```python
session.edit(w1, [
    TextEdit(old_string='<p k="P100" class="normal"><r>unwanted section title</r></p>', new_string=''),
    TextEdit(old_string='<p k="P101" class="normal"><r>unwanted body text</r></p>', new_string=''),
])
```
After deletion, re-read the window to get updated keys before further edits.

Insert list items (do not fake lists with `1.` / `•` text or `<list>` / `<item>` tags):
```xml
<p list="list_decimal" list-level="0"><r>First item</r></p>
<p list="list_decimal" list-level="0"><r>Second item</r></p>
<p list="list_bullet" list-level="1"><r>Sub-item</r></p>
```

Preserve opaque content (charts, complex drawings):
```xml
<keep k="K5" />
```

Clone a block-level keep:
```xml
<keep k="auto" proto="clone:K5" />
```

Reuse a prototype paragraph or table row:
```xml
<p proto="P123"><r>New text following template style</r></p>
<tr proto="R456">...</tr>
```

### Common Mistakes (Wrong → Right)

**Bare text in `<p>`** — text must be wrapped in `<r>`:
```xml
<!-- Wrong --> <p>text</p>
<!-- Right --> <p><r>text</r></p>
```

**Tags inside `<r>`** — inline elements are siblings of `<r>`, not children:
```xml
<!-- Wrong --> <r><hyperlink url="..."><r>link</r></hyperlink></r>
<!-- Right --> <hyperlink url="..."><r>link</r></hyperlink>
```

**Fake list** — use native list attributes, not text numbering:
```xml
<!-- Wrong --> <p><r>1. First item</r></p>
<!-- Right --> <p list="list_decimal" list-level="0"><r>First item</r></p>
```

**Bold body text pretending to be heading** — use heading class or attr overrides (see "Inserting Structural Content Without Heading Classes" in Section 3):
```xml
<!-- Wrong --> <p class="body"><r attr="b:true">Section Title</r></p>
<!-- Right --> <p class="heading_1"><r>Section Title</r></p>
```

**Hard-coded page number** — use fields in headers/footers:
```xml
<!-- Wrong --> <p><r>Page 1</r></p>
<!-- Right --> <p><r>Page </r><field kind="PAGE"></field></p>
```

### Error Handling
- `Unknown cursor id`: Re-`read` and use the new cursor
- `E_OLD_NOT_FOUND`: Re-read the window and use a more unique `old_string`
- `W_MULTI_MATCH_REPLACED_FIRST`: Use a more unique fragment or `replace_all=True`
- `E_XML_INVALID`: Narrow scope and ensure tags are closed

### Comment Editing Pattern

See Section 8 "Comments and Revisions" for full comment operations including adding, replying, resolving, deleting, precise text anchoring (`start_text`/`end_text`), and warning handling.

---

## 5. Saving the Document

```python
session.save("/path/to/output.docx")
# Or low-level:
save_docx(package, "/path/to/output.docx")
```

- Must save after editing
- Save may fail if class/list/proto/url references are invalid
- Omitting the output path overwrites the original file

---

## 6. WIR Editing Handbook

### Operating Pattern

Always follow: open -> read -> edit -> re-read when structure or keys may drift -> save. Read `document` first and use `<classes>` to choose existing semantic styles before editing. Read `prototypes` only when cloning template-shaped content, and read `styles` only when changing style defaults.

### Safe XML Pattern

#### Mixed Formatting in One Paragraph
```xml
<p k="P200">
  <r>normal </r>
  <r attr="b:true;color:#C62828">highlighted</r>
  <r> trailing</r>
</p>
```

### Key Drift After Edits

After structural edits, paragraph keys (`k="..."`) within the affected window may change because the engine re-indexes blocks. Re-read before using keys from that region again.

To minimize re-read overhead, pack up to 3 related localized edits into one call. For uniform policy changes across many paragraphs, batch the window edits or use `replace_all=True` when the replacement is truly identical.

### High-Risk Operation Controls

- Structural insert/delete: keep the batch small, re-read immediately, and verify downstream windows
- Table surgery: preserve table shape unless redesign is requested; separate content edits from row/column schema changes
- Header/footer edits: identify the exact `header:rIdX` or `footer:rIdX` and edit only that story part
- Comments/revisions: see Section 8

### Production Edit Recipes

Common patterns:
- Global term replacement: read target windows, replace localized fragments, then re-read representative windows
- Clause insertion: anchor near the insertion point, reuse nearby classes/prototypes, then re-read for numbering and spacing
- Table update: edit `<td>` content first; change row/column structure in a separate batch
- Header metadata refresh: read both document body and the target `header:rIdX`; verify fields are intact

For a batch formatting refresh across many paragraphs without touching text, combine two passes:

1. **Style-default sweep via `part="styles"`.** Read the styles view, then edit each affected `<style id="...">` entry with `TextEdit`s. Changes propagate to every paragraph that does not carry an inline override. `patch_styles` accepts these keys on `<style>`: `font-size`, `ascii`, `hAnsi`, `eastAsia`, `line-spacing`, `lineRule`, `firstLine`, `firstLineChars`, `hanging`, `hangingChars`, `spacing-before`, `spacing-after`, `jc`, `b`, `i`, `color`, `page-break-before`, plus the usual meta (`name`, `basedOn`, `next`, `uiPriority`, `semiHidden`, `unhideWhenUsed`, `qFormat`, `outline`, `default`, `custom`).

2. **Per-window batched `attr` overrides.** For paragraphs whose visible formatting comes from inline `attr` rather than the style: read each window, classify each paragraph by content, build one `TextEdit` per paragraph, and submit all `TextEdit`s for the window in a single `session.edit(window_id, edits)` call. See §4 for batch sizes and §3 "Numeric units" for value units.

Note: editing `<class>` descriptors in document view does not propagate and raises `E_CLASSES_METADATA_EDITED`; use path 1 instead.

### Pre-Save Re-Read Checklist

Minimum:
- All edited document windows
- All edited non-document parts

Recommended:
- One additional window before and after each edited structural region

### Post-Save Review

Confirm save success, review warnings, and spot-check requested content, table/numbering coherence, and edited headers/footers/footnotes/comments.

---

## 7. Troubleshooting

### First-Response Protocol

When an error occurs:
1. Stop chaining new edits
2. Capture the error code/message
3. Re-read the affected part/window
4. Apply a minimal recovery edit
5. Continue with smaller batches

### Common Errors and Recovery

| Error | Likely cause | Recovery |
|---|---|---|
| Unknown / stale cursor | Cursor came from an old read or stale window | Re-read the same part, use the new cursor, retry with a smaller anchor |
| `E_OLD_NOT_FOUND` | `old_string` does not match cached WIR; text drifted after prior edits | Re-read, copy the exact current fragment, use more unique context |
| `E_XML_INVALID` | Malformed replacement XML or invalid paragraph/run structure | Replace one localized complete block; wrap text in `<r>`; close tags |
| `E_STYLE_NOT_FOUND` / `E_LIST_INVALID` / `E_PROTO_NOT_FOUND` | Referenced key does not exist in this session/view | Re-read `document`, `styles`, or `prototypes` and switch to an existing key |
| `E_CLASSES_METADATA_EDITED` | A `<class ...>` summary line was edited in document view | For style defaults edit `part="styles"`; for local formatting edit the target `<p>` / `<r attr>` |
| `E_URL_INVALID` | URL is not absolute or supported | Use an absolute `https://...` URL |
| `E_READ_TOO_LARGE` | Window request is too broad | Reduce scope using cursor-based pagination |

### Warning Handling Strategy

1. Structural risk warnings: investigate immediately
2. Cosmetic/normalization warnings: verify output and continue
3. Repeated warning patterns: reduce edit batch size and anchor scope

### Safe Recovery Patterns

- Reset and continue: save progress, re-open, re-read the target window, continue with smaller batches
- Isolate risky areas: complete safe sections first, then edit the problematic table/section/header/footer separately
- Roll forward: re-anchor at the current state and apply localized idempotent edits; do not blindly overwrite

### Save-Time Warning Triage

1. Classify: validation warnings, reference warnings, namespace/serialization warnings
2. Re-open and inspect edited parts
3. Non-blocking warnings with sound structure -> report transparently
4. Warnings suggesting corruption risk -> fix before delivery

### Escalation Criteria

Escalate (request the user to narrow scope or constraints) when:
1. Structural errors persist after two retries
2. The document has severe pre-existing corruption
3. User requests conflict with immutable template constraints

---

## 8. Comments and Revisions

### Comment Operations

#### Adding Comments

```python
wc, comments_wir, _ = session.read(part="comments")
session.edit(wc, [TextEdit(
    old_string='</comments>',
    new_string='<comment id="1" start="P10" end="P10" author="Agent" date="2026-03-11T00:00:00Z">comment text</comment>\n</comments>'
)])
```

**Important**: Comment content in WIR is a direct text node; do not include `<p>` or `<r>` child elements.

#### Precise Text Anchoring with `start_text` / `end_text`

By default, a comment anchors to **the entire paragraph**. To select specific text within a paragraph (like highlighting with a mouse), use `start_text` and `end_text`:

```python
wc, comments_wir, _ = session.read(part="comments")
session.edit(wc, [TextEdit(
    old_string='</comments>',
    new_string=(
        '<comment id="auto" start="P10" end="P10"'
        ' start_text="医疗服务价格改革"'
        ' end_text="区域分类路径"'
        ' author="Agent" date="2026-03-19T00:00:00Z">'
        'Comment anchored to specific text range'
        '</comment>\n</comments>'
    ),
)])
```

This selects from "医疗服务价格改革" to "区域分类路径" within paragraph P10.

**Cross-paragraph range**: Use different `start`/`end` keys with text anchors in each:

```python
'<comment id="auto" start="P10" end="P12"'
' start_text="beginning of selection"'
' end_text="end of selection"'
' author="Agent">Spans three paragraphs</comment>'
```

**Text matching behavior**:
- Exact substring match is tried first
- If exact match fails, normalized matching handles CJK punctuation differences (full-width ⇄ half-width, curly quotes ⇄ straight quotes, etc.)
- If both fail, the engine **falls back to whole-paragraph anchoring** and emits a `W_COMMENT_ANCHOR_FALLBACK` warning

**⚠ Verifying P-keys before anchoring**: The `text_only` read view omits paragraphs inside table cells but they still have P-keys. A paragraph you see as "P12" in `text_only` may actually be a different element in the document structure. Before adding comments:

1. Check `session.last_edit_warnings` after each comment edit — if you see `W_COMMENT_ANCHOR_FALLBACK`, your `start_text` did not match the paragraph content, meaning you likely targeted the wrong P-key
2. When the document contains tables, verify P-key content by reading the XML view, not just `text_only`
3. After adding comments, `re-read(part="comments")` — the response now includes `start_text`/`end_text` attributes showing the actual selected text, so you can confirm the anchor is correct

#### Replying to Comments

Omit `start`/`end` for replies — the engine inherits the parent's anchor.

```python
wc, comments_wir, _ = session.read(part="comments")
session.edit(wc, [TextEdit(
    old_string='</comments>',
    new_string='<comment id="auto" parent="1" author="Agent">reply content</comment>\n</comments>'
)])
```

#### Resolving Comments

Mark as resolved by setting `resolved="true"`.

#### Deleting Comments

Remove the corresponding `<comment>` element via an edit.

### Comment Rules

- Top-level comments must include `start`/`end` pointing to valid document block keys
- Replies: set `parent` to the parent comment ID, omit `start`/`end` (engine inherits parent's anchor)
- Do not use `parentId` or nest `<reply>` elements
- `start`/`end` must point to valid document block keys in the current session (typically paragraph keys)
- Do not insert comment marker tags in the document WIR; ranges/references are rebuilt from the comments part
- Appending by replacing `</comments>` is the safest pattern
- `start_text`/`end_text` anchor to specific text within start/end paragraphs (see "Precise Text Anchoring" above)
- After comment edits, document block keys may be rearranged; always re-read `comments` before appending more comments or replies
- Check `session.last_edit_warnings` after each comment edit — `W_COMMENT_ANCHOR_FALLBACK` means your text anchor missed and fell back to whole-paragraph anchoring
- If the body was just modified, re-read `document` first before working on comments

### Revision Marks

Revisions in WIR are represented using `<ins>` and `<del>` tags.

**Important**: `<ins>` and `<del>` must wrap complete `<r>` tags, not be placed inside `<r>`.

**Correct format**:
```xml
<!-- Insertion -->
<p k="P1" class="normal">
  <ins id="1" author="John Doe" date="2026-03-11T00:00:00Z">
    <r class="run_1">newly added content</r>
  </ins>
</p>

<!-- Deletion -->
<p k="P2" class="normal">
  <del id="2" author="John Doe" date="2026-03-11T00:00:00Z">
    <r class="run_1">deleted content</r>
  </del>
</p>
```

**Incorrect format** (will raise `E_XML_INVALID: <r> cannot contain child elements`):
```xml
<!-- Wrong: <ins> cannot be placed inside <r> -->
<p k="P1" class="normal">
  <r class="run_1"><ins>newly added content</ins></r>
</p>
```

### Verification

After saving, manually confirm at minimum:
- Comment anchors are correct
- Revision marks are accurately positioned
- `comments.xml` existing does not equal comments being visible (count mismatch = not saved)

---

## Reference Entry Points

- For overall routing: `../SKILL.md`
- For creating new documents: `openxml-sdk-reference.md`
- For matplotlib charts: `matplotlib-guide.md`
- For Markdown → Word conversion: `md2docx-reference.md`
