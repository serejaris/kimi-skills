# CHARTS.md · Signature chart library (data shape → graphic recipe)

Selection principle: **first recognize the data shape, then find the industry mechanism, then pick the chart**. Each recipe includes: trigger / composition / re-theming method / pitfalls.
`references/gallery/pattern_*.png` holds battle-tested finished references. Universal rules in §U at the end.

Line/bar charts are not the default base. Run the "text-removal recognition test" first: with titles, axis labels, and annotations hidden, the graphic should still expose industry entities, business constraints, or causal transmission as much as possible. If swapping only the labels ports it from farming to chips/shipping, it's just a generic chart in a new skin.

## Quick selection table

| Data shape | Graphic | Recipe |
|---|---|---|
| Capacity/scale/inventory ramping period over period (with forecast) | theme-native isometric units | P1 |
| Entities flowing toward outcomes over time (M&A/migration/closures) | timeline destiny flow | P2 |
| Decades of historical events | wall-chart timeline | P3 |
| Births, deaths, and outcomes of a group of entities | lifelines graveyard | P4 |
| Multi-window × multi-dimension comparison | matrix heat table | P5 |
| Generational spec evolution (countable layers/levels) | generational stacks | P6 |
| Subjective probability/likelihood judgments | odds board | P7 |
| Layered value chain/tech stack + control | 2.5D value stack | P8 |
| Same object, multiple bases (3–4 metrics) | small-multiples pictograms | P9 |
| Scenario multiplication/what-if arithmetic | scenario chain | P10 |
| Two series paired period by period (ratio is the star) | paired bars + ratio labels | P11 |
| Information lag (public vs actual) | submerged timeline | P12 |
| Bottleneck/constraint ranking | gate ladder | P13 |
| Site-wide context switching with scroll | persistent right-rail dashboard | P14 |
| Multi-signal monitoring (with series, thresholds, lead times) | causal horizon | P15 |
| Basis and source of every number | drill-down card system | P16 |
| The report's signature numbers (6–8, same entity system) | evidence object | P17 |
| Two-case verdict framework (evidence + triggers + falsification line) | verdict scale | P18 |
| Decade-long trajectories of two mutually causal indicators | phase orbit | P19 |
| Cycle-mechanism narrative (real lags + feedback) | waveform chain | P20 |
| One main long series carrying the whole narrative | scrolly tape | P21 |
| Same-scale long-term paths of 6–9 entities | small-multiples panel array | P22 |
| Single valuation/ratio series + mean σ band | band readout | P23 |

---

### P1 · Theme-native isometric units (iso domain units) `pattern_iso_towers.png`
**Trigger**: period-by-period capacity/scale data, discretizable units (1 layer = fixed quantity), often with a forecast period.
**Composition**: first find countable real units in the industry, then iso-project them: fabs/packaging layers, farm barns, generating units, storage tanks, container slots, server racks. Solid = actuals, translucent = headroom, **hollow + dashed edge = forecast/policy target**; mono big value + period name + `×n vs base period`; units fade in staggered; the whole field/array is clickable for drill-down. Use slab towers only when the object itself is genuinely a stacked structure; otherwise use real-unit arrays. The title states the thesis, not the chart type. This is the library's first-choice signature chart: **the industry entity itself as the unit of measure**. Barns expressing sow capacity and wafer/chip units expressing packaging capacity are the same method; the object is not decoration — every entity must map to a fixed quantity, and entity count, solid/hollow, vacancy, and target state jointly encode the data. Without a stable conversion, drawing an "industry-looking" array is forbidden. Give each unit one identity detail (barn pitched roof + gable, unit cooling tower, hatch cover), with solid/hollow state applied to it too — that stroke is the line between "looks like the industry" and "generic boxes"; target towers get dashed roofs too.
**Pitfalls**: opacity floor ≥0.30, or low towers read as floating loose slabs; an iso body extends (lw+ld)/2 of projection depth below baseY — **bottom labels must sit below baseY+isoDrop**; keep one decimal, don't round (14.5≠15).

### P2 · Timeline destiny flow `pattern_destiny_flow.png`
**Trigger**: a group of entities each with a starting year, eventually flowing to a few outcomes (acquired/IPO'd/independent/dead).
**Composition**: left column entity names (serif, grouped by cohort with mono kickers), middle timeline lifelines (ink round-cap lines, small birth-year labels), and at exit year a Bézier ribbon bends into the right-column outcome plaque; **ribbon width ≈ sqrt(deal size)** (undisclosed = hairline), dashed = rumored-not-closed; outcome plaque = brand-color wordmark (mono caps) + left color bar + ×inflow count; dead entities get a ✕ endpoint. Crisis vertical bands (semantic red 5% tint) as historical background. Animation: lifelines grow → ribbons draw → plaques/labels fade in.
**Re-theming**: outcomes can be any discrete endgame — acquirers, bankruptcy, pivot to another track, regulatory absorption, category assignment.
**Pitfalls**: sort hub plaques by "mean y of inflow rows" to reduce crossings; `raise()` plaques above ribbons; **append all labels last, at the end of the svg** (later-drawn lines cross earlier-drawn text); all labels get paper-background stroke `paint-order:stroke` stroke-width≥4; notes for surviving entities go below the line (don't cover the birth-year label).

### P3 · Wall-chart timeline `pattern_wallchart_timeline.png`
**Trigger**: multi-decade span, 10–20 milestone events, need the whole history at a glance.
**Composition**: bottom double-line time axis + era color bands (current period blue tint, narrow-band labels staggered in two rows above/below + short leader lines); events = white-background ink-framed small plaques (mono year + index + serif bold one-line title), greedy layering: if it doesn't fit on a layer, move up one, **chart height = f(actual layer count)**; plaque stems drop to small dots on the axis. Semantic colors: crash events red frame, current window blue frame + dashed. Enter left→right plaque by plaque; per-plaque drill-down.
**Pitfalls**: **stems/axis dots drawn in stemLayer, plaques in plaqueLayer after it** — otherwise later stems pierce earlier plaque text; plaque width estimated at chars×6.35px (serif bold 11px); layer cap ≥9 to prevent right-side event clusters crowding one layer.

### P4 · Lifelines graveyard `pattern_lifelines.png`
**Trigger**: same data as P2 but the point is the "birth-death distribution" rather than "flow". Can coexist with P2 (one tells timing, one tells outcomes).
**Composition**: one round-cap thick line (6.5px) per entity, cohorts within groups; historical groups in ink scale, current group electric blue; dead endpoints get a small tombstone (round top + cross, semantic-red cross); outcome notes placed in **three levels**: right of endpoint → centered above the long line (threshold noteW+30) → left side right-aligned (truncate by word, never past the left edge); crisis bands; grow-in from the left.

### P5 · Matrix heat table (comparison matrix) `pattern_comparison_matrix.png`
**Trigger**: N historical windows/cases × M dimensions, compared against "now".
**Composition**: DOM table. Same mechanism = blue tint (.13), partially isomorphic = blue hatch, no correspondence = gray tint (.045), current row = white background + 1.5px ink rules top/bottom + blue-text reference; alignment column = five-dot scale (blue) + n/5; primary analogue row ★ (the legend must explain ★); per-cell drill-down with "mapping to now".

### P6 · Generational stacks `pattern_generational_stacks.png`
**Trigger**: countable specs across product generations (stacked layers, core counts, generation numbers) + one share/scale secondary indicator.
**Composition**: P1's iso engine, slab count = spec count, ink base = base part; two share bars on the side (hatch = broker estimate) + revenue footnote. Labels below the iso projection depth (see P1 pitfalls).

### P7 · Odds board `pattern_odds_board.png`
**Trigger**: 3–5 paths/propositions, each with a subjective probability grade (Low→High) + evidence + boundaries.
**Composition**: row layout: path name (serif bold) + boundary note | probability scale (4-step axis + solid marker; ranges drawn as low-high double dots + connecting line) | evidence column. Paths under way get a full-row blue tint + "UNDER WAY" pill. Don't use a table — the scale is the star.

### P8 · 2.5D value stack `pattern_value_stack.png`
**Trigger**: layered value chain/tech stack, each layer with players + some entity's control.
**Composition**: skewed-parallelogram top faces + rectangular front faces, slabs stacked top to bottom (LAYER 05→01 mono numbering), the thesis layer blue tint + blue frame; right column per layer: control dots (●●○) + players + one italic line.
**Pitfalls**: right-column text truncated to a pixel budget (italic serif ≥5.8px/char), truncation point never on a comma/article/preposition, full text in the drill-down.

### P9 · Small-multiples pictograms `pattern_small_multiples.png`
**Trigger**: three-way comparison across 3–4 bases under the same unit of account (1 GW / 10k tons / 1 route).
**Composition**: four small panels: block stack (1 block = fixed quota), dot matrix (1 dot = fixed quota), two bar groups; each panel's bottom note is one comparison conclusion (the most counterintuitive one bolded in primary blue); bottom "paradox beneficiary" strip.
**Pitfalls**: when adjacent bars are nearly equal height, stagger the labels (+14px); thousands separators consistent (1,237K).

### P10 · Scenario chain `pattern_scenario_chain.png`
**Trigger**: conclusion = factor × factor; multi-scenario ranges.
**Composition**: STEP 1 three hairline blocks (A × B = C, C blue frame blue text); STEP 2 scenario range bars (base blue, conservative ink, collapse = semantic-red dashed frame pinned to the 0 axis). Narrow ranges (<96px) get one merged centered label at both ends. One kill-switch sentence in the chart footer.

### P11 · Paired bars + ratio labels `pattern_paired_bars.png`
**Trigger**: two series paired period by period (capex vs cash flow), the ratio is the real star.
**Composition**: per-company small partitions, each period solid (blue) + outlined (ink) bar pairs, ratio printed above the pair; periods where the ratio breaches the limit switch the whole pair to semantic red + footnote ("funded with debt"); forecast periods hatched/dashed.

### P12 · Submerged timeline `pattern_submerged_timeline.png`
**Trigger**: any systematic lag where "what actually happened predates public disclosure".
**Composition**: waterline dashed line (electric blue) splitting above/below: above = public-timepoint flags (blue triangular flags + poles), below = actual-timepoint capsules (ink round heads + porthole dots), dashed surfacing paths connect the two + "submerged n yrs" notes; underwater blue tint 5%.

### P13 · Gate ladder `pattern_gate_ladder.png`
**Trigger**: constraints/bottlenecks ranked by rigidity, each with a score and a bypass route.
**Composition**: DOM rows: big index | solid/hollow square (no bypass/has bypass) | name + basis | 10-cell block score bar (cells light up one by one) | bypass branch (deep blue ↳) or red-frame NO BYPASS | dual-scenario lamps.
**Pitfalls**: grid column width must be ≥ the actual width of block bar + score (10×11px+gap+score≈190px), or NO BYPASS crushes the score.

### P14 · Persistent right-rail dashboard (context rail) `layout_*.png`
**Trigger**: long reports need persistent "where are you in the cycle" context. 460px fixed canvas switching 15–20 states with section `data-win`. Components top to bottom: window badge + title | five-segment phase bar (current segment blue, may pulse) | dot-matrix globe (topojson land 3° sampling + geo-node pulses, **node labels collected first, then y-deconflicted**) | data plaque | halftone dot-matrix mountain curve (72-point resampled morph, 28px readout safety band reserved at top, end pulse cursor + mono big readout with 5px paper stroke) | four stat blocks | entity cohort status cells (fixed abbreviation table, no hard per-character truncation). Everything clickable for drill-down.
**Re-theming**: swap the globe for industry geography; cohorts for industry players; the curve for the window's main indicator.

### P15 · Causal horizon
**Trigger**: 6–20 monitored signals; at least two of: time series, threshold, lead time relative to outcome.
**Composition**: x-axis unified as "months leading the outcome" (left = leading, right = coincident), y-axis banded by causal layer (capacity/supply/price/profit/policy etc.); each signal is not a status badge but a node carrying a 12–24-month mini trajectory. Distance to threshold drives the outer ring, recent direction drives the tail trail, missing data left blank with a red gap mark; causal lines only for relationships confirmed by the fact source. Conflicting signals paired with a cross-layer bracket. Clicking a node expands full history, threshold basis, lead-time estimate, and source.
**Gate**: one screen must simultaneously answer "which way, how far from threshold, how long the lead, which signals conflict". With only current values, four-step dots, and absent/partial/in-place badges, it's just a status list — make it a compact table instead; it doesn't count as a signature chart.

### P16 · Drill-down card system (drill everywhere)
Every number/element in every chart click → `U.showDrill({title, value, delta, sub, source})`. sub states basis and context; source must carry date and table key. Trigger elements get `data-drill-keep`. This is half of the "research-report feel" — **a chart without drill-down is not done**.

### P17 · Evidence object `pattern_evidence_object.png`
**Trigger**: the report's hardest 6–8 numbers, all belonging to the same entity system. This is the qualified replacement for the number wall (§R#1).
**Composition**: draw a realistic silhouette of the theme atom (a hog / a generating unit / a ship), and hang each number on its **semantic site** — the part that in reality already performs that measurement's function: ear tag = management target (ear tags already are capacity-management tools), side spray code = inventory (slaughter-bound hogs really are spray-coded), feed level in the trough by the mouth = cost ratio, hanging tag on the back = market price (mini real-data sparkline embedded in the tag), price sticker on the rump = unit profit (negative in semantic red), fence posts behind, solid/hollow count = industry concentration, offspring queue under the body = efficiency metric (incremental individuals in electric blue, the tail individual clipped by the fraction). A unified ground line carries all objects; items "hang on" one by one on entrance; each drills down to precise basis + dated source.
**Re-theming**: ship — draft line = freight rate, slots = capacity, fuel tank = oil price, classification plaque = new-regulation effective date; unit — nameplate = installed capacity, cooling-tower plume = utilization, meter = power price, fence = grid-connection quota.
**Pitfalls**: the first hand-drawn silhouette almost certainly "doesn't look right" — identity parts like ears/snout go on **separate pieces overlaid on the main silhouette**, not embedded in the outline path (breaks the silhouette and is hard to tune); all side notes get paper halos and mind draw order vs the silhouette (a later-drawn silhouette covers earlier text); surrounding objects (fence/trough) shouldn't sit directly behind the main silhouette — layer occlusion is a narrative choice.
**Gate**: semantic sites must be functional positions that really exist, not arbitrary number stickers; every site must drill down to a basis, or the whole chart degrades into illustration (violating §R#4).

### P18 · Verdict scale `pattern_verdict_scale.png`
**Trigger**: a two-case verdict framework (same/different-case, bull/bear standoff, success/failure scenarios), each side with an evidence list, upgrade triggers, and a shared falsification line. This is the qualified replacement for text-box decision trees (§R#2).
**Composition**: a balance scale. Left and right pans hold evidence weights (trapezoid + top-knob physical shapes, single-line phrases, full text in drill-down), the beam tilts toward the side with more evidence weight (tilt angle is qualitative; the footer must declare "not a score"); fulcrum small dial: three-zone ticks + needle, the needle magnifies the reading but **stops inside the current verdict zone**; the pillar hangs a readout plaque = one-sentence current verdict; **dashed hollow weights hover outside the pans** = upgrade triggers not yet met (note "reading upgrades only when all land on pans" + dashed arrows pointing at pans); bottom red-hatched seal strip = shared falsification, three white falsification strips on the seal (per-strip drill-down). Animation: weights bounce onto pans alternating left/right → beam tilts → needle deflects.
**Re-theming**: any binary verdict — deal success/failure, tech route A/B, bull/bear. Swap pan weights for the corresponding evidence phrases.
**Pitfalls**: weights must be solid-filled (translucent ones get pierced by hanging chains); the hanging assembly (chains + pan + weight stack) doesn't rotate with the beam — translate as a whole by beam-end height; readout plaque solid background (or the pillar shows through); the right pan's weight stack top must not exceed the beam-end hook.
**Gate**: at least triple structural encoding — evidence sidedness (topology), tilt direction (weight), dashed weights (absence condition). A "two-side comparison" without upgrade triggers and a falsification line falls back to the matrix heat table.

### P19 · Phase orbit `pattern_phase_orbit.png`
**Trigger**: two mutually causal indicators (supply vs price), decade-plus series, stable lead-lag relationship.
**Composition**: x = leading-indicator index, y = lagging-indicator index, years as nodes connected into an orbit, arrows = time flow; the two indicators' median lines split the plane into four quadrants, quadrant names in big serif + small basis notes (shortage = low capacity · high price…); the big loop flung out by the crisis gets a full-segment electric-blue bold + note ("the ASF-flung loop · 2018-2021"); current year = solid big dot + pulse ring + "now: quadrant X"; faint concentric circles hint rotation. When the lagging series starts later, the orbit starts where data exists, with a note.
**Re-theming**: inventory vs freight rates, capex vs chip prices, installed capacity vs power prices — any cobweb-model structure.
**Pitfalls**: rotation direction is determined by the lead-lag structure (capacity leads → clockwise) — verify before writing the note; year labels dodge the orbit line; at self-intersections, later-drawn segments get raised.
**Gate**: the orbit's rotation is itself the visual proof of lead-lag — if it doesn't rotate (a tangle), the two indicators don't form a phase relationship; withdraw and switch to a dual-line chart, don't force it.

### P20 · Waveform chain (lead-lag version) `pattern_waveform_chain.png`
**Trigger**: cycle-mechanism narrative — two mutually causal real index waves + countable mechanism phases (glut → losses → destocking → shortage → price rise → expansion). This is the qualified version of the icon transmission chain (§R#3).
**Composition**: double waves = two real indices (ink = leading, blue = lagging), no decorative sines; slanted dashed arrows connect inflection-point pairs = lead time (labeled "≈ n months"); mechanism phases = ring nodes along the wave (solid = happened, semantic red = current, **hollow dashed = expected phase**); dashed extension at wave end draws the expected cycle closure (price rise → expansion → renewed glut) + bottom large feedback dashed arc ("profits feed back into capacity, another ≈ n months slower"). Rings and arrows each drill down to sources.
**Pitfalls**: expected segments must be hollow + dashed + legend declaring "expected phases are not forecasts"; each wave has its own base period, zero line noted "respective means, phase illustration only"; ring-node labels get paper stroke to avoid crushing the wave.
**Gate** (inherits §R#3): must have both real lag data and feedback structure; stage sequence alone doesn't qualify.

### P21 · Scrolly tape `pattern_scrolly_tape.png`
**Trigger**: one main long series (weekly price / monthly index) carrying the whole narrative, sliceable into 5–7 windows narrated segment by segment.
**Composition**: sticky chart + left column step text (.step ≈80vh, era-tag kicker + serif subtitle + one paragraph); each step switches: ① window band highlight ② that window's line segment bolded electric blue, the rest grayed ③ window event plaques **ghosted above the tape** (current window solid, the rest ~6% opacity — events "grow" out of the main line instead of opening another chart) ④ high/low white-circle red-dot notes switch with the window; the final step morphs to the daily-frequency close-up. The right rail switches in sync via the same data-win.
**Re-theming**: any industry where "one line is the whole story" — freight indices, chip spot prices, power price curves.

**⚠ This is the easiest chart in the library to get wrong** — the symptom is always "the right-side chart and labels squashed into a clump". There are only two root causes: **mis-measured width**, or **sticky without height**. Below is the only stable approach — copy verbatim, no improvisation.

**① The chart lives in a fixed viewBox coordinate system; never measure the container's real width (iron rule #1)**
```js
const W = 880, H = 640;                    // fixed drawing coordinate space
const svg = d3.select(body).append("svg")
  .attr("viewBox", `0 0 ${W} ${H}`)        // all x/y/scale written inside this 880×640
  .style("width", "100%").style("height", "auto").style("display", "block");
// x = d3.scaleTime().range([mL, W - mR])  ← range uses the constant W, not host.clientWidth
```
Why: `#price-chart` sits inside a `position:sticky + display:flex` dash-inner; on the first frame layout is unsettled, `host.clientWidth` measures 0 or a few dozen px → all scales squash → every label lands at x≈0 → clump. A fixed viewBox + `width:100%` lets the browser scale the whole chart proportionally; drawing code always lays out at 880 wide, **never touching the "real width is 0" pit**. All plaques/notes also use SVG `<text>` in the same coordinate system — don't float absolutely-positioned HTML labels over the pane (those really do shrink to the pane origin).

**② The sticky pane must have explicit height (iron rule #2)**
```css
.chron-grid  { display:grid; grid-template-columns: minmax(380px,44%) 1fr; }
.chron-dash  { position:relative; }              /* right-column track */
.dash-inner  { position:sticky; top:0; height:100vh;   /* ← without this line it collapses to content height, everything crammed at top */
               display:flex; align-items:center; justify-content:center; padding:40px 28px; }
.step        { min-height:80vh; }                /* left-column steps ≥80vh, giving sticky enough travel */
```
`position:sticky` without `height:100vh` shrinks to content height; the chart in the pane has no vertical space and step scrolling has no track to stick to → chart and text all pile at the top. Left-column steps must be taller than the right pane (N steps ×80vh), or it won't stick.

**③ Build the chart once; scrolling only switches state (don't rebuild the svg)**
```js
function setStep(n){ /* only change existing elements' opacity/weight/color: band highlight, segment emphasis,
                        plaque ghost (current window 1 / rest .06), peak/trough note visibility, weekly↔daily group switch */ }
const stepIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) setStep(+e.target.dataset.step);   // one-way: text drives chart, never reverse
}), { rootMargin: "-45% 0px -50% 0px", threshold: 0 });     // center-band hit → exactly one step at any moment
steps.forEach(s => stepIO.observe(s));
```
Appending a new svg/new elements per step = flicker + re-measure + cramping. Weekly→daily uses two layer groups under **the same x domain** cross-fading opacity (gWeekly→0 / gDaily→1), no `remove()` rebuilds.

**④ Narrow screens and reduced-motion: turn off scrolly, show a static chart**
```js
const STATIC_CHART = REDUCE || matchMedia("(max-width:980px)").matches;
if (STATIC_CHART) { setStep(FINAL); /* draw the composite state with all windows and plaques, don't install stepIO */ }
```
```css
@media (max-width:980px){
  .chron-grid { grid-template-columns:1fr; }
  .dash-inner { position:static; height:auto; }      /* no sticky in single column, or touch-screen scroll-jack */
  .fig-xscroll { overflow-x:auto; }                  /* fixed-880-wide chart scrolls horizontally instead of compressing */
  .fig-xscroll > svg { width:880px !important; max-width:none !important; }
}
```

**⑤ Layer order (same for P3)**: bands → stems stemLayer → main line → plaques plaqueLayer (ghost) → notes/hit. Plaques drawn after the main line (floating above it), stems drawn before plaques (or stems pierce plaque text); all labels get paper stroke.

**Pitfalls**: ① measuring `host.clientWidth` for layout → first frame collapses to 0 → clump (most common; switch to fixed viewBox); ② sticky without `height:100vh` → everything piled at top; ③ rebuilding svg per step → flicker + cramping; ④ two-way listening (chart also changing scroll) → jitter death loop, always one-way step→setStep; ⑤ sticky still on at narrow widths → touch-screen freeze, must degrade to static.

### P22 · Small-multiples panel array (series version) `pattern_small_multiples_series.png`
**Trigger**: same-scale long-term paths of 6–9 entities, where individual shapes and outcomes matter more than mutual crossings (P9 is the same-unit multi-basis version; this is the multi-entity time-series version, replacing an 8-line multi-line chart mushed together).
**Composition**: 4×2 same-scale log-axis small panels: each cell = entity name + ticker + start note | top-right "now value" big readout (protagonist electric blue, rest ink) | line + light area fill | dashed = baseline water level (first day = 100) | bottom corner notes carry only min/peak; the protagonist panel entirely electric blue; restructured/delisted entities get a red tag top-right; **dead entities get no panel** — a full-width red dashed strip at the bottom (✕ + dead ticker + one sentence); the gap is the evidence. Per-panel drill-down to the full ledger.
**Pitfalls**: all panels must share the same y domain and log scale (otherwise "same scale" is a lie and comparison breaks); no conclusion sentences inside panels (conclusions go in prose), corner notes carry only factual extremes.

### P23 · Band readout `pattern_band_readout.png`
**Trigger**: a single valuation/ratio series + mean and ±σ band + a "where in the band are we now" question (PB/PE bands, spread bands).
**Composition**: left 1/4 readout panel: oversized serif current value + date + one relative-position sentence ("−38% below the five-year mean" in electric blue) + three hairline-separated basis lines (mean / in-band range / ±σ position); right 3/4 series: light-blue area = full series, **deep-blue region = the part below the mean** (drawing "being below" as area, not as a note), dashed = mean, dotted = ±σ, peak/trough white-circle notes, solid end point + pulse ring. One chart answers "how much, vs the mean, where the historical range is" at once.
**Pitfalls**: left-panel text baselines align with the right chart's grid (off by 2px and it reads as two charts); "below the mean" uses clip-path to split-color the same area, not a second line.

---

## §R · Eliminated fake charts

The following forms must not enter the signature chart library, nor count toward the "chart count":

1. **Number wall**: 6–8 big numbers laid out in a grid. Numbers go in executive-summary prose, compact tables, or rail readouts — not a standalone chart. Qualified replacement: P17 evidence object — the same numbers hung on the semantic sites of the theme entity.
2. **Text logic diagram**: long text stuffed into 2–4 boxes connected by curves; decision trees and same/different-case bridge diagrams belong here. If the relationship has no quantity, topology, probability, or time encoding, use short paragraphs or a comparison matrix. Qualified replacement: P18 verdict scale — sidedness/tilt/absent-weights triple encoding, drawing the verdict as a weighable object.
3. **Icon transmission chain**: one wavy line/arrow stringing five icons and stage labels. With only stage sequence — no multi-batch, lag distribution, throughput, loss, or feedback data — it cannot be called a mechanism chart. Qualified replacement: P20 waveform chain (real dual indices + lead-time arrows + expected hollow positions + feedback arc) or P19 phase orbit.
4. **Literal-container reskin**: bars/liquid levels stuffed into trough, thermometer, or oil-tank outlines. If the entity outline carries no real physical structure, it only sacrifices proportion and aesthetics; use precise trends, threshold durations, or distribution charts instead. Exception (P17 condition): a container as one **semantic site** of an evidence object (the trough genuinely carries the feed-cost basis in farming) with precise-value drill-down; a whole-chart reskin where a single container holds a single number remains banned.
5. **Status-slider list**: each row one text + four dots + absent/partial/in place. Without historical direction, threshold distance, and lead time, it can only be an appendix registry table, not a main visual. Qualified replacement: P15 causal horizon.

How to judge: temporarily hide all text. If what remains is only boxes, connecting lines, evenly spaced dividers, or a few status dots — and you can't read out quantity, time, flow, probability, topology, or real physical units — delete immediately, no further polishing.

---

## §T · Upgrading generic charts to theme-native models

Upgrade only when the mapping carries information; don't add semantic-less 3D for "cool".

| Data task | Generic base | Theme-native model example | What the geometry must carry |
|---|---|---|---|
| Long-cycle price history | line | cycle terrain / contour profile | peak heights, trough widths, external-force ridges |
| Multi-company long-term paths | multi-line | survivor slots / fleet / rack small multiples | cohorts, scale change, restructuring/exit gaps |
| Positive/negative profit series | bar | profit barns / water-level tanks / balance-sheet profile | zero axis, loss penetration, profit stacking, reporting-period compartments |
| Discrete capacity quantities | abstract square towers | barn clusters / unit arrays / slot clusters | each physical unit = fixed quantity, forecasts stay hollow |
| lead-lag | wavy path + stage icons | cohort-time map / lag ridge | multi-batch, lag distribution, throughput/loss, outcome-side differences |
| ratio + policy threshold | literal trough/container | threshold-duration band / regime strip | breach depth, weeks sustained, recovery time, regime bands |
| multi-signal monitoring | status-slider list | causal horizon | recent direction, threshold distance, lead time, signal conflicts |

Precise-value drill-down survives the upgrade; theme styling must not sacrifice basis, time positioning, or comparison baselines.

---

## §U · Universal rules (apply to every chart)

1. **Skeleton**: the `U.frame()` trio; the title states the finding ("still tight at six times"), the mono subtitle states how to read + units + interaction hints; the Source line has four categories + date.
2. **Collision-resolution priority**: reposition (multi-anchor candidates, pick rightmost/emptiest) → tiered staggering (odd/even rows/tiers) → word wrapping → measure-and-truncate (`ctx.measureText`/glyph-width estimation, **italic serif ≥5.8px/char, mono ≥6px @10px**) + tail stripped of commas/articles/prepositions then " …" → full text always in the drill-down.
3. **Text over lines**: canvas always `strokeText` paper halo (3.5–5px); SVG always `paint-order:stroke` + stroke=paper; if still failing, append the text layer last.
4. **Entrance animation**: IntersectionObserver threshold 0.12–0.25, fires once; bars rising/line growing/block fade-ins staggered 40–130ms; `prefers-reduced-motion` draws the completed frame directly.
5. **Module isolation**: one IIFE + host `<div id="x-chart" class="chart-frame">` per chart, starting `if (!host) return;`. Data always from `window.RPT`, rather missing than fabricated (don't draw entities absent from the tables; note it in comments).
6. **Sizing**: `W = clamp(host width−20)`, viewBox scales responsively; canvas uses utils' `bindCanvas` (DPR≤2), must re-`fit()` when activated during display:none.
7. **Forecast/gap semantics**: forecast = hollow + dashed/hatch; gap = semantic-red hatch + "?" + `[TBD]` — **drawing the gap itself** (no interpolation, no hiding) is this methodology's stance.
8. **Theme recognition**: screenshot with all text hidden; at least one of industry entity or core mechanism must hit. A complex chart that merely adds perspective, shadows, particles, or materials to bars/lines is still treated as generic and must be restructured.
9. **Information density**: theme entities ≠ themed. A signature chart must encode at least two structural variables besides text (e.g. quantity + state, time + flow, lead time + threshold distance). Encoding only one column of numbers or one ordinal relationship → demote to prose component or table.
