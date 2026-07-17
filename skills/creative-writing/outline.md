# Outline: Structure Before Prose

Read before Stage 1. Produce a structured, executable outline saved to `/mnt/agents/output/{name}.agent.outline.md`. Scale the effort to the work's length.

Every outline — short or long — opens with two header lines:

```
Language: 中文（依据：brief 与源文均为中文）
Budget: 目标 20000 字 → 5 章 × 3800–4200 字
```

The **word budget** (target total → chapter/section count → per-chapter range) is what drafting writes toward and review checks against. Plan it here so length is engineered, not discovered after assembly — "write first, patch chapters later" causes renumbering and rework.

## Short pieces (short story, essay, single poem, one scene)

A light outline is enough — often a few lines:
- **Premise / controlling idea** (one sentence).
- **Shape**: opening image/hook → 2–5 beats → turn → ending, with a rough word count per beat. For a short story, the central change the protagonist undergoes.
- **Voice & constraints**: POV, tense, tone, length target, any hard requirements from the brief.

Write this, then go straight to drafting.

## Long / serialized works (novel, web-novel, multi-episode)

Build the outline in three passes, writing each artifact to file.

### Pass 1 — Foundation, characters, world

- **Foundation**: genre/subgenre, length target, POV, tense, tone, audience, platform, premise (1 sentence), theme, and the protagonist's core desire + fear.
- **Plot points**: an ordered sequence of 8–15 turning events spanning the whole arc (inciting incident → escalations → midpoint reversal → crisis → climax → resolution).
- **Characters** → `documents/{name}.characters.md`: per character — role, desire, fear, arc (start→end), voice signature, key relationships, and one internal contradiction. Characters should generate conflict with each other.
- **World** → `documents/{name}.world.md`: key locations with sensory detail and a narrative function each; world rules (what is possible/impossible, costs); recurring props. Only as much as the story needs.

### Pass 2 — Volume / arc structure (for very long works)

Divide into volumes (卷) or arcs, each a self-contained arc that feeds the next: title, chapter range, core conflict, character focus, arc trajectory (start→end state), 3–5 key events, turning point. End states chain into the next arc's start.

### Pass 3 — Per-chapter specs

For each chapter, specify:
- **POV** and rough scene count.
- **Word target** (from the budget; chapters of one work stay within a consistent range).
- **Core conflict / goal** of the chapter.
- **Hook-in** (how it opens) and **hook-out** (how it closes).
- **Key beats** (the 2–5 things that happen).
- **Foreshadowing**: what is planted or paid off (track IDs in `documents/{name}.foreshadowing.md`).
- **Dependencies**: which earlier chapters this one relies on (so continuation stays consistent).

Write per-chapter specs into the outline; for big works keep the full spec archive in `documents/{name}.outline_raw.md` and a compact index in `{name}.agent.outline.md`.

## State Files (multi-chapter works) — the consistency + lean-context mechanism

For any work of more than 3 chapters, create `documents/{name}.characters.md` immediately after chapter 1; add the others as complexity warrants. Update after each chapter and re-read the relevant entries before writing the next:

| File | Holds |
|------|-------|
| `{name}.characters.md` | Profiles, current state, what each knows |
| `{name}.world.md` | Locations, rules, props |
| `{name}.foreshadowing.md` | Each setup → where it pays off, status |
| `{name}.threads.md` | Open plot/relationship threads and their status |
| `{name}.chapter_summaries.md` | One-paragraph summary + closing beat per finished chapter |

Re-reading these (rather than every prior chapter's full text) is how a long work stays consistent without flooding the working context.

## Outline End-State

- If the user wants the full piece: state in one line that the outline is ready and proceed to drafting (don't summarize the outline back at length).
- If the user asked for an outline / 大纲 / 框架 / 设定集 only: that document **is** the deliverable — name it `{name}.agent.final.md`, deliver with ARTIFACT_REF, and stop.
- If the user provided an outline: format and lightly complete it without altering its core decisions, then proceed.
