---
name: creative-writing
type: capability
description: >
  End-to-end creative writing — fiction and web-novels (网文), screenplays and
  storyboards, audio-drama scripts, stage drama, poetry, lyrics, essays, letters,
  and other literary forms. Covers brief analysis, outline design, drafting,
  self-review, and assembly, with genre-specific craft conventions and anti-AI
  discipline. Honors the user's stated length, format, platform, and hard
  constraints. Outputs go to files under /mnt/agents/output/ (Markdown by
  default; .docx via the docx skill).
  Do NOT use for: research reports, market analysis, policy briefs (use
  report-writing); academic papers, surveys, empirical studies (use paper-writing).
---

# Creative Writing

**Read this file in full — never with a line limit; if a read is truncated, keep reading to the end.** Then, at each stage, read its stage file BEFORE starting the stage (put these reads in your todo list):

| Stage | Must read first | Goal |
|-------|----------------|------|
| 0 — Intake | (this file) | Brief understood; large sources indexed into notes |
| 1 — Outline | [outline.md](./outline.md) | A structured, executable outline with a word budget (+ state files for multi-chapter works) |
| 2 — Draft | [content.md](./content.md) + matching [styles/*.md](./styles/) + [anti-ai.md](./anti-ai.md) | The actual prose/script/verse, written to file with craft and a human voice |
| 3 — Review | [review.md](./review.md) | Verifiable self-review passes on the real files; fix in place. **No ARTIFACT_REF before this stage runs.** |
| 4 — Assemble | — | Concatenate parts → `{name}.agent.final.md`; deliver in the genre's format; clean up stale intermediates |

Take a creative brief from request to finished piece: **understand → outline → draft → review → assemble and deliver**, writing every artifact to a file as it is produced.

If the user requests a specific output format (or asks for inline / 对话框 output), honor it. Otherwise default the deliverable by genre, saving under `/mnt/agents/output/`:

- **Web-novel / 网文, fiction, poetry, lyrics → `.txt`** — plain text, no Markdown syntax in the body, chapters concatenated.
- **Screenplay / 剧本, stage drama, audio drama / 有声剧, essay / 散文, letters → `.docx`** — assemble `{name}.agent.final.md`, then convert via `skills/docx/SKILL.md`.

## Workflow Decision Tree

```
Brief
  │
  ├─ Very short (flash fiction, single poem, one scene, < ~1.5k 字)
  │   → light outline in-head → draft → review → deliver
  │
  ├─ Short / medium (short story, essay, 1–3 chapters, 1.5k–15k 字)
  │   → Stage 1 (light outline) → Stage 2 → Stage 3 → Stage 4
  │
  ├─ Long / serialized (novel, web-novel, multi-episode, 15k+ 字 or >3 chapters)
  │   → Stage 1 (full outline + state files) → Stage 2 (chapter-by-chapter) → Stage 3 → Stage 4
  │
  ├─ Continuation / adaptation / rewrite (source uploaded)
  │   → index source into notes first (Step 0) → Stage 1 (fit to source) → Stage 2 → Stage 3 → Stage 4
  │
  ├─ Provides outline + asks for prose → Stage 2 → Stage 3 → Stage 4
  │
  ├─ Asks for outline / 大纲 / 框架 / 设定集 only
  │   → Stage 1 → that document IS the deliverable (name it {name}.agent.final.md) → deliver and stop
  │
  └─ A sequence of requests in one brief ("先给大纲…再写正文", "第一章…第二章…")
      → complete every part in order; persist each part to its own file as it is finished
```

Infer genre/form, **word-count target**, POV, tense, tone, platform conventions, and hard constraints from the brief and uploads. Make reasonable creative choices and begin; do not stall asking questions unless the request is genuinely impossible to proceed on. Before drafting, fix two things in writing (outline or notes):

- **`Language: …`** — deliverable language = the brief's language; continuation/adaptation/rewrite must match the source unless translation is explicitly requested. Format conventions (FADE IN, INT./EXT.) are not language choices.
- **Hard-constraint checklist (rewrite/revision tasks)** — copy the user's revision notes verbatim (never paraphrase; paraphrase softens constraints), mark each must/should, and check every item off before delivery.

## Step 0: Read the brief and uploads — index large sources into notes

Read `/mnt/agents/upload/` before anything else. **Read with discipline so input volume never stalls the work:**

- **Small references** (≲1000 lines or ≲100KB text): read in full with `read_file`, paging as needed.
- **Large or numerous references**: never read them whole into context. Sequence:
  1. **Size-check with the right tool**: `ls -la`; `wc -l` only for `.txt`/`.md`. **`.docx`/`.pdf` are binary — `wc -l`/`grep`/`sed` results on them are meaningless, including numbers that look plausible.** Get authoritative length from `ipython` (`len(Document(f).paragraphs)` via python-docx; pdfplumber page count), or by paging `read_file` to its true end. (`read_file` returns at most the first 1000 lines per call.)
  2. **Map the structure**: `.txt`/`.md` → `grep -nE '第.{1,6}章|第.{1,3}卷|楔子|序章|Chapter [0-9]'`; `.docx`/`.pdf` → `read_file` (auto-converts to markdown) or `ipython` heading scan. Web novels mix Arabic and Chinese chapter numerals — match `第[0-9一二三四五六七八九十百零]+[章卷]` in one pass; if chapters are unnumbered, treat short standalone paragraphs (<20 chars, blank lines around) as heading candidates.
  3. **Read only what matters, one chunk at a time**: for a continuation you usually need the last chapters before the continuation point + character/setting/timeline info — not the whole book. Page with `offset`/`limit`, always advancing `offset`. A file is fully read **only when a page returns fewer lines than `limit` or explicit EOF** — never infer the end from an external count. If `read_file` already showed the file's end, don't spend another call confirming it.
  4. **Write notes BEFORE reading on**: after each segment, append its summary to `/mnt/agents/output/{name}.source_notes.md` — voice/style sample, plot-so-far, character roster + states, world rules, timeline, exact state at the continuation point, hard constraints — plus a coverage line ("已读至第 N 段 / 全文共 M 段"). **The system recycles old tool outputs; anything not on disk is lost and must be re-read.** Once summarized, **treat the raw text as disposable — work from the notes; re-read specific lines on demand.** Notes prevent *loss*, not *peak context*: holding raw "just in case" still overflows the window.
  5. **One big file per turn** — never parallel-read several large files in one turn; that bloat lands in one round and compaction cannot reclaim it. Keep any single tool return under ~30k characters by choosing smaller pages.
  6. **Triage many files**: record "read / skipped + reason" per upload; before Stage 1, confirm nothing the brief depends on was silently skipped.
  7. **Don't front-load — interleave read & write for huge/multi-file sources.** When the source is too large to sit in context alongside the draft (e.g., several full novels for a multi-episode rewrite), read only what the **current** chapter/episode needs → summarize → write that unit → then read the next unit's material. Reading the whole source before drafting overflows the window right at the read→write boundary (this is what sank the 2-novels → rewrite-25-episodes case).

## Genre Routing → styles/

Match the form first; read the matching style guide before drafting and follow its conventions.

| Form / keywords | Style guide |
|-----------------|-------------|
| 网文, web-novel, 番茄/起点, 爽文, serialized 长篇 | [styles/web-novel.md](./styles/web-novel.md) |
| 小说, novel, novella, short story, 短篇/中篇/长篇, 故事, literary/genre fiction | [styles/fiction.md](./styles/fiction.md) |
| 剧本, screenplay, 分镜, storyboard, 电影/电视剧本, FADE IN | [styles/screenplay.md](./styles/screenplay.md) |
| 有声剧, audio drama, 广播剧, 多集音频脚本 | [styles/audio-drama.md](./styles/audio-drama.md) |
| 诗, 词, poem, 律诗/绝句, sonnet, haiku, verse, 歌词, lyrics | [styles/poetry.md](./styles/poetry.md) |
| 散文, 随笔, essay, prose, 议论文, 书信, letter | [styles/essay.md](./styles/essay.md) |
| no clear match | nearest above; infer conventions from the request |

Web-novels are fiction with platform-specific pacing — read **both** `web-novel.md` and `fiction.md` for serialized 长篇网文.

## Output & File Discipline

- **Everything is a file.** Creative output goes to `/mnt/agents/output/`; chat is for brief status only. (Exception: if the user explicitly asks for inline / 对话框 output, honor that — and apply the same plain-text rules to inline prose: 「第N章」 headings, no `**`/`##` in the body; when one of several deliverables is requested inline, all of them must be readable in the chat.)
- **Persist as you go; protect the tail.** For multi-part work, write **each chapter/part to its own file the moment it is finished** (`{name}.ch{NN}.md`) before starting the next. After the first chapter, check per-chapter size × total count against the remaining budget; re-plan immediately if they don't fit. **Never pack multiple chapters into one write** — compress evenly rather than letting later chapters degrade into synopsis. Assemble into `{name}.agent.final.md` when all parts are done.
- **State files for multi-chapter works** (>3 chapters): create `documents/{name}.characters.md` right after chapter 1 and update it after every chapter; add `{name}.world.md`, `{name}.foreshadowing.md`, `{name}.threads.md` when the setting/plot complexity warrants. Re-read the relevant entries before each chapter — this keeps consistency AND a lean context.
- **Naming**: outline `{name}.agent.outline.md`; source notes `{name}.source_notes.md`; chapters `{name}.ch{NN}.md`; final `{name}.agent.final.md`. One `{name}` per work across all its files. Rewrites in place — no `_v2` proliferation. Before delivery, remove or overwrite stale intermediate "finals" so exactly one current final exists.
- **Language follows the user.** Prose, deliverables, AND process narration in the user's language; internal filenames in English.

## Core Principles

1. **Serve the author's vision.** Honor the user's stated intent, style references, length, and hard constraints exactly.
2. **Structure before prose.** Outline first for anything beyond a very short piece — including a word budget (total → chapters → per-chapter range) — and write toward it.
3. **Honor the length target.** Word-count targets are requirements. Count 汉字 excluding punctuation unless told otherwise; report the measured count and 口径 at delivery. No default "long".
4. **Voice over formula.** Genuine human voice and concrete specifics beat template-filling. Follow content.md's anti-AI discipline and scan against [anti-ai.md](./anti-ai.md) while drafting and reviewing (中文八股、cross-language hard bans, and the English vocabulary list). Creative work is never structured like a report — no citations, no executive summary, no 首先/其次 scaffolding.
5. **Consistency is non-negotiable** for multi-chapter works — track state explicitly in files.
6. **Execute to completion.** Once the outline is ready, write through to a finished, delivered piece; don't pause unless the brief asks for outline approval.
7. **Read big, write lean.** Index large sources into notes instead of dumping them into context; write each part to disk as you finish it.
8. **Verify on real files.** Every check (word count, constraints, anti-AI scan) reads the actual output file; printing pre-written conclusions is not verification.

## Reference Files

| File | When to read | Content |
|------|--------------|---------|
| [outline.md](./outline.md) | Before Stage 1 | Outline methodology, word budgeting, state-file templates, per-chapter spec format |
| [content.md](./content.md) | Before Stage 2 | Drafting craft, dialogue, hooks, length discipline, continuation alignment, anti-AI summary |
| [anti-ai.md](./anti-ai.md) | Before drafting **and** during review | The authoritative anti-AI checklist: 中文八股分类大全（频率阈值）、跨语言硬性禁项、English high-signal vocabulary |
| [review.md](./review.md) | Before Stage 3 | Verifiable self-review passes, programmatic scans, pass/fix criteria |
| [styles/*.md](./styles/) | Before drafting | Per-genre voice, structure, format, and prohibited patterns |
| [scripts/](./scripts/) | During review | `check_wordcount.py` (min/max/target), `scan_anti_ai.py` (frequency tells, markdown leakage, quote style) |
