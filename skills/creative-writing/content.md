# Content: Drafting Craft

Read before Stage 2. This governs how the actual prose, script, or verse is written. Read the matching `styles/*.md` alongside it for genre conventions, and `anti-ai.md` for anti-AI discipline (中文八股 + cross-language bans + English vocabulary).

**Creative work is not a report.** Do **not** use `[^n^]` citations, do not force comparison tables, do not open with an "Executive Summary," and do not structure creative work like a research report — no 首先/其次 scaffolding, no concluding 综上所述.

## Before Drafting a Section

Resolve these once, up front, and keep them consistent across the whole work:

- **Voice & POV**: narrator distance, person, tense, and the register the piece lives in. Lock it; don't drift.
- **Word target** for this section (from the outline's budget). Draft to land within **±15%** of it; for "at least X" requirements, draft to ~110% of X so one pass suffices.
- **What this section must accomplish**: the beat(s) it advances, the hook it opens on, the hook it closes on, what the reader must feel or learn by the end.
- **Continuity inputs**: for multi-chapter works, re-read the relevant state-file entries and the previous chapter's closing beat before writing.

## Craft Principles

- **Show, don't tell** (where the form allows). Render emotion and change through action, gesture, and sensory detail rather than naming the emotion. "她的手在抖，茶水洒在手背上也没察觉" beats "她非常紧张".
- **Graduated physical beats for emotion.** Escalate through the body, not adjectives: light (clenched jaw, swallowed hard) → medium (hands shaking, voice cracking) → heavy (legs buckled, slammed the table). Match intensity to the moment.
- **Dialogue reveals character.** Each speaker has a distinguishable voice — diction, rhythm, what they avoid saying. Let subtext carry weight. Cut on-the-nose exposition.
- **Specificity creates reality.** One precise, chosen detail outweighs paragraphs of vague atmosphere. Concrete nouns over abstractions.
- **Rhythm.** Vary sentence and paragraph length. Short for impact. Then a longer, flowing line when the scene breathes. Uniform length reads mechanical. (Fragments are a spice, not a diet — see anti-ai.md on 碎片化短句 for the over-use boundary.)
- **Every word earns its place** — while still hitting the length target. Cut filler; let density rise, not word count alone.
- **Causation through sequence, not connectors.** Show why things happen by ordering action and consequence, not by chaining 因为/所以/由于/为了.
- **Stay inside the story.** No lecturer metadiscourse (让我们回到…/要讲X，先得讲讲Y/这个问题千百年来…) — background reaches the reader through scene and viewpoint, not narration-as-essay.

## Continuation / adaptation — align to the source's fingerprint

When continuing or rewriting an existing work, match more than plot:

- **Punctuation style**: curly vs straight quotes (“” vs ""), ellipsis style, dashes, paragraph indentation — sample the source and reproduce it exactly. A continuation pasted back into the original must not show a seam.
- **Tic-word frequency**: measure the source's per-10k-character rates for common tics (像是/仿佛/缓缓/嘴角/微微…) and keep your draft in the same range — a 3–5× drift reads as a different author even when no single sentence is wrong.
- **Chapter length**: default to the source's per-chapter average ±15% unless the brief says otherwise.

These are programmatic checks — run them in review (`scripts/scan_anti_ai.py` compares rates when given a reference file).

## Hooks (especially serialized / web-novel)

- **Open** on motion, tension, or a question — not on weather, throat-clearing, or backstory dumps.
- **Close** each chapter/episode on a hook: a reversal, a threat, a revelation, an unanswered question, a decision pending.
- Plant small open loops early; pay them off later.

## Expanding a thin draft (without padding)

When a section is under target or feels flat, deepen — do not repeat:
1. **Sensory layering** — what the POV character sees/hears/smells/feels physically.
2. **Interiority** — thought, judgment, mixed feeling, memory triggered by the moment.
3. **Beat the dialogue** — action beats and pauses between lines; what hands and eyes do while speaking.
4. **Raise the stakes / sharpen conflict** — make the obstacle costlier, the choice harder.
5. **Scene texture** — a specific object, a bystander, a sound that grounds the place.
Strengthen the relevant scene; never bolt on a disconnected section to hit a number.

## Length Discipline

- Treat the user's stated target as a hard requirement. Counting 口径: 汉字 excluding punctuation unless the user says otherwise; "X字左右" allows ±10%, "以上/以内" are hard bounds. Report the measured count and 口径 at delivery.
- **Draft to budget; adjust by gap.** If a section misses its target, compute the gap first and close it in one deliberate pass (expand per the list above, or cut whole weak beats). No overshoot-then-cut-then-refill oscillation — it burns turns and frays the prose.
- Check counts efficiently: batch the word-count of several finished chapters in one `ipython` call, or run `python /app/.agents/skills/creative-writing/scripts/check_wordcount.py <file> --min N [--max M | --target T --tol 10]` — don't spend a whole turn per chapter just counting.
- There is **no default "long-form" expectation** — a 1800-字 brief gets ~1800 字, not a novella.

## Anti-AI Discipline

**The authoritative checklist is [anti-ai.md](./anti-ai.md) — read it before drafting and scan against it during review (review.md Pass 2).** It covers 中文八股 (§一–§六), cross-language hard bans (§零 — citation/tool artifacts, chatbot tics, Markdown leakage), and the English high-signal vocabulary list. Two natures of tell:

- **Pattern tells** (a phrase or structure that is wrong wherever it appears): citation/tool artifacts, chatbot tics, stray Markdown in prose, AI 腔 vocabulary (助力/彰显/赋能…; tapestry/delve/pivotal…), 首先…其次…最后 scaffolding, "It's not just X, it's Y" — find and rewrite each occurrence.
- **Frequency tells** (fine in isolation, damning in aggregate): em-dashes, similes (像是/仿佛/如同), tic words (缓缓/嘴角/微微), hedging chains (也许是…也许是…), 四字格律, "不是X而是Y". **Your eye normalizes these while drafting — they must be counted programmatically in review**, against the thresholds in anti-ai.md (or against the source's rates for continuations).

**Comply while drafting, then fix in ONE batch — not per-tell.** The cheapest fix is not generating the tell: write the first draft already obeying these rules (sparse em-dashes, few similes, no 心跳/嘴角 clichés, clean punctuation). When the review scan still flags residual frequency tells, fix them in a **single batch pass per file** — one `sed`/`ipython` replacement across the whole file (e.g., replace every `——`) or one rewrite of the few flagged passages — **never dozens of one-at-a-time `edit_file` calls**. That per-tell edit loop is the #1 step-budget sink and starves the later chapters and the review itself. Cap at **2 polish passes per file**; if a tell is still over threshold, rewrite only the worst passages once and move on.

**The antidote — writing with a pulse:**
- Have opinions; let characters hold mixed, contradictory feelings.
- Let mess in: tangents, half-thoughts, things left unsaid.
- Be concrete instead of summarizing ("this was hard" → the specific hard thing).
- Vary rhythm. Allow uncertainty and silence. Use "I" where the genre invites it.

## Self-Check Before Finishing a Section

Before marking a section done, verify:
- Word-count target met (within tolerance); POV/tense consistent; the section advances its intended beat.
- Opening and closing hooks land (for serialized forms).
- Character voices stay distinct; established facts (names, timeline, world rules, uploaded-source canon) are not contradicted.
- Then write the file (or update it in place) before moving to the next section — and update the state files for multi-chapter works.

The full-work review (Stage 3) is separate and mandatory; finishing all sections does not skip it.
