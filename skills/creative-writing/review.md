# Review: Verifiable Self-Review

Read before Stage 3. **This stage is the delivery gate: no ARTIFACT_REF may be emitted before it has run and its result is reported in one line of the final reply.** Fix issues **in place** — strengthen the weak passage rather than appending a note or a new section. For long works, run the per-chapter passes as each chapter finishes, and the cross-work passes once all chapters exist.

Two iron rules:

1. **Verify on real files.** Every check reads the actual assembled output (re-read at minimum the opening, a middle section, and the ending; run scans on the file itself). Printing a pre-written ✓ checklist, or "checking" from memory of what you wrote, is not verification.
2. **Replace, don't annotate.** Rewrite offending passages; never leave reviewer notes in the deliverable.

## Pass 1 — Continuity (per chapter)

Check against the brief, the uploaded source canon, and the state files:
- Names, ages, relationships, places, and timeline are consistent with everything established.
- World rules are not violated; props/abilities behave as set up.
- Each character knows only what they could plausibly know at this point.
- Promised setups are still on track; nothing contradicts a prior chapter's closing beat.

Fix any contradiction at its source (and update the state file if the canon itself shifted intentionally).

## Pass 2 — Style & Anti-AI (per chapter)

Scan against [anti-ai.md](./anti-ai.md) — cross-language hard bans and English vocabulary for any prose, 中文八股 for Chinese prose; pattern tells item-by-item, frequency tells **programmatically** (run `scripts/scan_anti_ai.py <file>`, or an equivalent `ipython` scan; for continuations pass the source as reference: `scan_anti_ai.py <file> --ref <source>`):
- No AI vocabulary / 腔, no citation/markdown leakage (`^#`, `**`, backticks) in the prose body, no boldface inflation.
- Frequency tells within thresholds: em-dash density, simile density, tic words, hedging chains, "不是…而是" (anti-ai.md §频率阈值).
- For continuations: punctuation/quote style and tic-word rates match the source; chapter lengths within the source's range.
- Distinct character voices; emotion shown through action, not named; rhythm varies; concrete specifics, not vague summary.

## Pass 3 — Structure & Constraints (whole work)

Read the complete piece and check:
- Every hard constraint from the brief's checklist is satisfied — verify each item against the **verbatim** wording, not your paraphrase of it.
- The central promise (premise/theme) is fulfilled; the protagonist's change actually happens on the page.
- Scenes earn their place; cut or merge any that don't advance character or plot.
- Setups pay off; no dangling threads unless deliberately left open.
- Word count: run the count on the final file, confirm target and 口径, and check **per-chapter balance** — all chapters of one work should sit in the same range; a tail of chapters far thinner than the head means re-drafting them, not shipping.

## Pass 4 — Pacing & Hooks (serialized / long works)

- Opening hooks fast; no slow throat-clearing start.
- Each chapter/episode opens and closes on a hook; tension curve rises across the arc.
- Scene-level rhythm (goal → conflict → outcome) is present; action and reflection are balanced.
- For platform fiction, pacing matches the platform's norms (see the genre style guide).

## Fix Criteria

- **Minor** (a tell, a flat line, a small inconsistency): fix in place immediately. After a small targeted edit succeeds, don't re-read the whole file to confirm — re-read only the edited passage.
- **Major** (broken continuity, a scene that fails its purpose, a missed beat): rewrite the passage/scene with a specific change in mind — not a vague "make it better."
- Re-read the fixed passage once to confirm the issue is gone and nothing new broke.

## Before Delivery

- Output directory is clean: exactly one current final per work; stale intermediate "finals" deleted or overwritten.
- Final reply reports, in one line: measured word count + 口径, constraint checklist result, and scan result (e.g., "实测 20,312 汉字（纯汉字口径），硬约束 6/6 核销，扫描无 Markdown 泄漏、频率项达标").
- Don't ship known continuity breaks or obvious AI tells.
