# DESIGN.md · Design system (invariant layer — copy verbatim)

`assets/theme.css` is the complete base theme; copy it directly as the site's `css/style.css`.
This file explains its rules and red lines, and gives paste-ready component HTML skeletons.

## 1 · Token table

| Token | Value | Use |
|---|---|---|
| `--paper` | #ffffff | paper background |
| `--paper-hi` | #f7f9fc | panel background (sparingly) |
| `--ink` | #051c2c | primary ink (headings/body/strong lines) |
| `--ink-md` | #42566a | secondary text |
| `--ink-lo` | #8595a6 | auxiliary text/axis labels |
| `--line` / `--line-lo` | #dbe2ea / #eef1f6 | two hairline levels |
| `--red` | **#2251ff** | ⚠ legacy slot name, actually the electric-blue primary accent. In code `PAL.red` = electric blue |
| `--red-hi` | #1233b8 | deep blue (second blue step/links) |
| `--blue-soft` | #7d9bff | light blue (third series) |
| `--neg` | #c22f4e | semantic red: declines/crashes/gaps/missing only |
| `--green` `--copper` | #008a6d / #b07a10 | reserved semantic slots only (e.g. the four source-category badges); not used inside charts |

**One-color-family-per-chart discipline**: a single chart = ink scale + the electric-blue family (#2251ff/#1233b8/#7d9bff shades), with semantic-red accents. The only two exemptions: brand wordmarks at flow-diagram destinations; true material colors on the realistic cover (PCB green, gold solder balls, aluminum, silicon). Before adding a new hex literal, ask yourself whether you're breaking the discipline.

## 2 · Fonts

```css
--serif: "et-book", "Iowan Old Style", Palatino, "Palatino Linotype", "Book Antiqua", Georgia, serif;
--mono:  Menlo, Consolas, "SF Mono", "Liberation Mono", "DejaVu Sans Mono", ui-monospace, monospace;
```
- ET Book via `assets/fonts.css` (base64-inlined, three faces roman/italic/bold). **No external font links.**
- ET Book has only weights 400/700 — writing 600/800 silently falls back; always use 700.
- Body 17px/1.68. Serif handles narrative and headings; mono handles everything "data-flavored": axis labels, kickers (ALL CAPS + `letter-spacing:.1em+`), source lines, table headers, code-style badges.
- Font strings inside canvas/SVG must be the same families as the CSS:
  `'"et-book", Palatino, Georgia, serif'` / `'Menlo, Consolas, monospace'`.

## 3 · Layout grid

- `.prose` 692px centered (padding 0 28px) — the site's single body column, **footer/appendix use it too**; never open a custom column width for one section (this once threw the whole column off, see QA.md postmortem #11).
- `.wide` 800px / `.wide.xl` 924px: symmetric figure bleed. If the figure column's left edge differs from the prose column's by >60px it reads as "broken typesetting".
- Right-rail dashboard: `main { margin-right: 460px }` + `#dash-rail` fixed, borderless, transparent background; at ≤1180px set `--railw:0` and hide the rail. Canvas inside the rail must not have max-height/border-radius/shadow.
- Section kicker `.sec-no`: small mono + 26px blue dash. Cover is full-bleed 100vh.

## 4 · Editorial components (paste the HTML skeletons directly)

**dek (section intro)** — italic serif, no border, no background:
```html
<p class="dek">One-sentence framing of the section, italic serif.</p>
```

**Quote block (quote-card)** — 2px heavy ink top rule + hairline bottom + kicker, no background, no left bar:
```html
<blockquote class="quote-card">
  <p class="q-text">The quote itself, large italic serif.</p>
  <p class="q-who">— <b>SPEAKER, TITLE</b>, 2025-11-03</p>
  <div class="q-why"><span class="q-lab">Context</span> …
    <span class="q-lab why">Why it matters</span> …</div>
</blockquote>
```
(theme.css's `.quote-card::before` automatically prints the "FROM THE RECORD" kicker.)

**Note (note-box)** — hairlines top and bottom + "ANALYST NOTE" kicker:
```html
<div class="note-box"><p><b>Lead-in.</b> body…</p></div>
```

**Concept three-column (term-mag)** — magazine layout, hover overlay expands (never pushes the layout below):
```html
<div class="term-mag">
  <article class="term" tabindex="0">
    <h3 class="t-abbr">ASIC</h3>
    <p class="t-full">SPELLED-OUT NAME (MONO CAPS)</p>
    <p class="t-gist">One-line definition always visible.</p>
    <div class="t-more"><p>The full story, revealed on hover/focus.</p></div>
    <p class="t-hint">Hover for the full story</p>
  </article> ×3
</div>
```

**Chart skeleton** — the trio for every chart (use `U.frame` from utils.js):
```js
const body = U.frame(host, {
  title: "Serif title stating the finding, not the chart type",
  sub:   "MONO SUBTITLE · how to read it · unit legend · click hints",
  src:   "Source class — provider (dated), table key",
});
```

**Data tables** `table.dt`: mono ALL-CAPS header + 1.5px ink bottom rule, hairline rows, `.hl` row blue tint.
Key numbers in the executive summary go into thesis sentences, compact tables, or rail readouts; never spread 6–8 numbers into a "big number wall" grid.
**Source-category badges** `.src-cat.{company|broker|industry|kimi}`: four categories, four colors (reserved semantic slots).
**Drill-down card** `#drill-card`: dark ink background + 3px blue top bar, driven by `U.showDrill()`.

## 5 · Red lines (fix on sight)

1. Left color bar + tinted-background quote/tip cards (the typical AI look).
2. Top color-bar rounded cards; any card taller than one screen.
3. 2+1 orphaned columns from `repeat(auto-fit,…)` — if the column count is fixed, hard-code `repeat(3, minmax(0,1fr))`.
4. Rainbow palettes / semantic-less recoloring inside charts.
5. Paragraphs piled with number-arrow-bracket chains ("$91.4B → $180–190B, $118B → ~$190B (of which…)") — rewrite as plain-language narrative + a compact table.
6. Hand-drawn style, sticker style, emoji paragraph markers.
7. Opacity transitions on full bars (mid-state text bleed-through) — fixed bars slide in opaquely.
8. Decision trees/bridge diagrams made of text boxes + curves; icon-chained wave transmission chains; literal-container reskins like troughs and thermometers; four-dot status lists. Without quantity, time, flow, probability, topology, or real physical units, it does not count as a chart.

## 6 · Copy register

Institutional research English (or the research register of the corresponding language), sentence-case headings. Give a one-sentence definition at each term's first appearance. Preserve hedged wording from the fact source ("third-party media attribution, not company-confirmed", "[derived]", "not a forecast"). Historical analogues only as "the closest historical analogue is X, but this cycle has no true precedent". Every source in the four-category system carries a date. Retracted or basis-mixed numbers must never appear at the render layer.
