---
name: interactive-research-report
description: Turn any deep report/research document into a McKinsey/GS-grade interactive research website — theme-native visual grammar, editorial typesetting, four-state animated cover, signature chart library, every number drillable, persistent right-rail dashboard. Use when the user asks for an "interactive research report site / interactive report / turn a report into a website / data-visualization report". Zero-build vanilla JS; delivers a multi-file site plus a single-file version that opens over file://.
---

# Interactive Research Report · site-building skill

Turn one deep report (any topic: chips, the hog cycle, energy, logistics, pharma…) into an interactive, drillable, animated-cover, editorial-grade single-page research site.

The skill has three layers: **invariants** (fonts/palette/layout/components — copy verbatim, see DESIGN.md and assets/), **abstraction rules** (covers generated from the "theme atom", charts selected by "data shape" — see COVER.md and CHARTS.md), and **methodology** (the debug loop and postmortem checklist — see QA.md).

## 0 · File map

| File | When to read |
|---|---|
| `DESIGN.md` | Read fully before starting — design-system hard constraints + editorial components + copy register |
| `CHARTS.md` | Consult before every chart — curated signature graphics, elimination list, and data-shape selection |
| `COVER.md` | When building the cover — four-state cover engine (incl. the D unboxing opener) + the "theme atom" abstraction |
| `QA.md` | After every module + before wrapping up — debug loop, gates, postmortem checklist |
| `assets/theme.css` | Copy directly as the site's `css/style.css` (base theme, use as-is) |
| `assets/fonts.css` | Copy directly (ET Book base64-inlined; external font links forbidden) |
| `templates/utils.js` | Copy directly as `js/utils.js` (canvas/drill-down/tooltip/frame skeleton) |
| `templates/skeleton.html` | Starting skeleton for the site |
| `templates/bundle.py` | Single-file bundling script (just edit the file manifest) |
| `references/gallery/` | One finished screenshot per pattern — check the picture whenever unsure "what it should look like" |
| `references/BUILD_LOG-example.md` | Build log of a complete case (V1→V8.4), the why behind every decision |

## 1 · Input contract (confirm/collect with the user before starting)

1. **Prose fact source**: one report md/pdf (the single source of truth; the website prose transcribes it faithfully, preserving hedged wording).
2. **Data tables**: structured data (csv/json/tables all fine). You compile it into a `js/data.js` exposing `window.RPT = { key: [...] }`, with snake_case English keys.
3. **Source register**: source + date for every key number. Compile into `js/sources.js` (a K1–Kn anchor table). Sources without dates must be graded (company primary > cross-check > broker relay > derived).
4. **Theme atom** (one question suffices): what is the most physical, decomposable, instantly recognizable entity in this industry? Chips = the package/die; hogs = the industrial farm; shipping = the container ship; power = the generating unit. All four cover states are different views of this **same physical object**. A recurses the **object itself** (draw the recognizable object directly, zooming out until it becomes one cell of a larger array of its kind) — not "some causal/mechanism logic" (that's a flowchart with a zoom slapped on, a classic failure). See COVER.md.
5. Language (default: institutional research English, sentence case) and delivery width baseline (default: dual acceptance at 1680/1280).

## 2 · Build pipeline

```
① Data layer      data.js (window.RPT) + sources.js (K anchors) — before everything
② Skeleton        skeleton.html + theme.css + fonts.css + utils.js + vendor (d3/topojson local)
③ Section plan    Cover → §0 executive summary (evidence object P17 or core-conflict hero chart + total timeline) → concept cards →
                  history/mechanism (waveform chain / phase orbit / scrolly tape) → current state (core chart cluster) →
                  players (destiny flow + small-multiples panels) → verdict (verdict scale P18 + causal horizon / evidence matrix) →
                  appendix → Sources (K table)
④ Cover           COVER.md four-state engine (A infinite object recursion / B physical exploded view / C engineering blueprint / D unboxing opener · impact version)
⑤ Charts          Every chart goes through the CHARTS.md selection table; after each one, enter the QA loop (screenshot → critique → fix → re-verify)
⑥ Right rail      Persistent canvas switching with scroll (optional but strongly recommended, CHARTS.md P14)
⑦ Full regression All QA.md gates pass → bundle.py single file → re-verify over file://
```

Scale reference: a full site is ~20 js modules, 4000–6000 lines; the minimum viable version (cover B + 5 signature charts + K table) is ~1500 lines. Each chart module is an independent IIFE + host div; one failure doesn't affect the others.

## 3 · Invariants (copy verbatim, no "improvising")

- **Fonts**: body/headings ET Book serif (weights 400/700 only); data/axis labels/kickers/source lines Menlo mono ALL CAPS + letter-spacing. Font strings inside canvas/SVG match the CSS exactly.
- **Palette**: white paper + ink scale (#051c2c/#42566a/#8595a6) + electric blue #2251ff primary accent + semantic red #c22f4e (declines/gaps/missing only). **One color family per chart**: any single chart uses only the ink scale + electric-blue family (light blue #7d9bff allowed as a third series), with semantic-red accents. Only two exceptions: brand wordmarks in flow diagrams, and true material colors on the realistic cover.
- **Layout**: prose 692px centered; figure plates 800px symmetric bleed, extra-wide 924px; right rail 460px persistent dashboard (borderless, same background as the page, hidden ≤1180px); everything aligns to the same vertical grid (footer included).
- **Editorial components** (full CSS in DESIGN.md): italic serif dek, "FROM THE RECORD" quote blocks, "ANALYST NOTE" notes, magazine three-column concept cards (hover overlay expands without pushing layout), the chart-frame trio (serif title + mono subtitle "how to read + interaction hints" + Source line).
- **Red lines (the "AI card" ban)**: no left color bar + tinted-background quote cards, no top color bar rounded cards, no cards taller than one screen, no 2+1 orphaned columns from auto-fit grids, no semantic-less rainbow palettes.
- **Interaction trio**: every number inside a chart is clickable → dark drill-down card (value + basis + dated source); IntersectionObserver entrance animations; prefers-reduced-motion gets the static completed frame.

## 4 · Abstraction rules (how to swap themes)

- **Cover**: all four states are views of the **same physical atom**. A = infinite self-similar recursion of the object (**draw the recognizable object directly**, zooming out into one cell of a larger array of its kind; what recurses is the object itself, not a logic/causal chain); B = layered explosion of the physical entity + thesis annotations; C = engineering-drawing wireframe of B; D = B's explosion + unboxing animation (the unrestrained impact version, an unboxing opener). A has its own geometry; B/C/D share geometry (D uses B's engine plus an unboxing timeline). See COVER.md.
- **Chart selection**: don't think "what chart libraries do I have" — look up the selection table in CHARTS.md by "what shape is the data": capacity/scale ramps prefer industry-entity isometric units (barns, wafer/chip units, generating units — each entity maps to a fixed quantity); entities flowing toward outcomes over time → destiny flow; historical events → wall-chart timeline; multi-window × multi-dimension comparison → matrix heat table; layered value chain → 2.5D value stack; probability judgments → odds board… Each recipe states "when to use / composition / collision rules / how to re-theme".
- **Theme-native modeling**: first ask "with all text removed, can you still tell the industry and the mechanism from this chart?" If not, pick a different model. Line/bar charts are not the default base; use them only when precisely reading a trend or a paired comparison is itself the task. Otherwise map to the industry's real structure. Complexity doesn't mean adding 3D — geometry must carry causality, business constraints, or real physical units.
- **Don't force-draw things that aren't charts**: number walls, text-box decision trees, same/different-case bridge diagrams, icon wave transmission chains, literal trough/thermometer reskins, and four-state slider lists are all retired from the signature library. At most they are prose components or appendix tables. A signature chart encodes at least two structural variables besides text; if it encodes only one column of numbers or one ordinal relationship, demote it. Every eliminated category has a verified qualified replacement: number wall → evidence object (P17), decision tree/bridge → verdict scale (P18), transmission chain → waveform chain (P20)/phase orbit (P19), slider list → causal horizon (P15). The ban exists to force out replacements, not to draw fewer charts.
- **Semantic-site principle** (the idea behind P17/P18): numbers hang on the part of the theme object that **actually performs that measurement's function in reality** — ear tags already are capacity-management tools, spray codes already are slaughter marks, hanging tags already are pricing acts. The object is not decoration; it is the physical metaphor of the measurement basis. Numbers with no semantic site are not force-hung — they go into prose or tables.
- **Copy**: number-dense passages are always rewritten in plain language; company×year data goes into compact tables; cycle/analogue judgments always use the sentence pattern "the closest historical analogue is X, but this cycle has no true precedent" — never an equals-sign conclusion.

## 5 · QA gates (all must pass; details in QA.md)

- `node --check` all pass; playwright full-page slow-scroll scans at both 1680 and 1280 widths: 0 pageerrors · 0 console errors · 0 horizontal overflow · (English sites) 0 visible residual Chinese
- `document.fonts.check('16px et-book') === true`; reduced-motion shows static frames for all animations
- All labels: zero overlap, zero out-of-bounds (collision-resolution priority: reposition > wrap > measure-and-truncate + drill-down fallback)
- Cover and signature charts pass the "text-removal recognition test" and the "theme-swap test": with labels hidden the industry/mechanism is still recognizable; if the chart ports to another industry by changing only the copy, it fails as over-templated
- Signature charts pass the "fake-chart test": with text hidden they still encode at least two of quantity/time/flow/probability/topology/physical units; if only boxes, connecting lines, status dots, or container outlines remain, delete
- Single-file version opens over file:// with 0 errors; spot-check 5 number drill-downs tracing back to sources.js and the original text
- Every module enters the "screenshot → critique → fix → re-verify" loop on completion; after the full site is done, you may dispatch 3–4 parallel review agents for sharded human review (sharding and prompt template in QA.md §4)
