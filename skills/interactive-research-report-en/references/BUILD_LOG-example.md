# BUILD_LOG · Minimal decision record

The BUILD_LOG serves only the next person who takes over: current state, key decisions, scope of changes, and validation results.
Don't write the full creative process, discussion records, or one-off operations into the deliverable.

## What the successor reads first

1. **Current state**: whether the latest round is complete, where the deliverables are, whether anything is blocking.
2. **Fact layer**: whether prose, structured data, and the source table agree; which numbers are still unconfirmed.
3. **Scope of changes**: which files or modules this round touched, and which were explicitly not touched.
4. **Key decisions**: keep only choices that affect later implementation, with a one-sentence reason.
5. **Validation results**: whether syntax, page errors, dual widths, offline version, fonts, and drill-down spot checks passed.
6. **Residual risks**: unsolved problems, reproduction conditions, and next actions.

## What not to write

- Sentence-by-sentence creative process, abandoned drafts, and aesthetic discussions.
- Local paths, temp directories, copy commands, and publish URLs.
- Old-project migration history, chat logs, platform changelogs, or model names.
- Replaced internal codenames, version nicknames, and precise animation parameters with no reuse value.
- Information directly available from git diff, source code, or test output.
- Personal memos irrelevant to the successor.

## Fixed format per round

```md
### [R01] One sentence on this round's purpose

- Goal: the user problem this round solves.
- Decisions: what was ultimately adopted; why.
- Changes: files or modules involved.
- Data: numbers and sources added, modified, or retracted; "none" if none.
- Validation: checks actually run and their results.
- Open: unsolved problems, trigger conditions, and next steps; "none" if none.
```

## Decision-index example

The following shows granularity only; the content need not be copied.

### [R01] Pin the fact source

- Goal: prevent prose, charts, and the source table from showing different numbers.
- Decisions: report prose is the fact backbone; structured data drives rendering; the source table handles traceability.
- Changes: `js/data.js`, `js/sources.js`, and the chart modules using these fields.
- Data: basis, units, dates, and source grades recorded; retracted values enter the banned list.
- Validation: spot-checked prose, charts, drill-down cards, and the source table — same number everywhere.
- Open: fields still lacking a primary source, listed.

### [R02] Converge visual semantics

- Goal: make color, fonts, and components mean the same thing site-wide.
- Decisions: primary accent separated from negative semantic color; true materials only on cover entities.
- Changes: design tokens, shared utilities, and affected chart modules.
- Data: none.
- Validation: per-chart checks of color usage, font loading, label readability, and screenshot consistency.
- Open: modules still depending on legacy token names, listed; the migration process is not expanded in the log.

### [R03] Adjust sections and charts

- Goal: make each section answer one question; delete duplicate or text-only fake charts.
- Decisions: charts chosen by data shape; signature charts encode at least two structural variables.
- Changes: section skeleton, chart entries, and corresponding modules.
- Data: field references changed by chart deletion or merging, recorded.
- Validation: text-removal screenshots, theme-swap tests, interaction spot checks, and full-page slow scroll.
- Open: charts needing more data to qualify, listed; rejected alternatives' creative process not recorded.

### [R04] Complete delivery regression

- Goal: confirm the multi-file site and the single-file version behave identically.
- Decisions: marking complete is allowed only when all gates pass.
- Changes: bundle manifest and necessary compatibility fixes.
- Data: none.
- Validation: `node --check`, page errors and console errors, 1680/1280 dual widths, `prefers-reduced-motion`, font check, key-number drill-downs, and the `file://` single-file version.
- Open: failed items must be written down; "basically complete" is not a substitute.

## Current-state block

Always keep this section at the end of the log; successors read it first:

```md
## Current state

- Latest round: Rxx — complete / in progress / blocked
- Deliverables: multi-file site; single-file version
- Validation: PASS/FAIL + failed items
- Open risks: none, or listed by priority
- Next action: one executable action
```

Keep the log short and executable. A successor reading only "Current state" and the latest round can judge where to continue; trace decisions upward to the corresponding round when needed.
