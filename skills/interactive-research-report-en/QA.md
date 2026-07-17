# QA.md · Debug loop, acceptance gates, and postmortem checklist

## 1 · Module-level debug loop (the core way of working)

Enter the loop immediately after each module; move to the next only after convergence:

```
Screenshot (playwright headless; slow-scroll first to trigger IO entrance animations, element-level screenshot)
→ Critique (read the screenshot visually, like a demanding design director: overlap/out-of-bounds/edge-hugging/blank/font fallback/
   color discipline/spacing imbalance/orphaned columns/"would this look out of place in a McKinsey report?")
→ Text-removal screenshot (temporarily hide SVG text / canvas labels): can you still recognize the industry entity or core mechanism?
→ Theme-swap test: if changing only the copy makes it usable for another industry, it fails; semantic-less 3D/particles/shadows don't count as theming
→ Fake-chart test: with text hidden, does it still encode at least two structural variables; if only boxes/lines/status dots/container outlines remain, delete
→ Fix → re-verify screenshot
```

Slow-scroll template: `while y < scrollHeight: scrollTo(0,y); wait 140ms; y += 700`; after reaching the target element, wait another 0.9–1.6s (for entrance animations to finish) before shooting.

## 2 · Wrap-up gates (all must pass before finishing)

- `node --check` passes for all js; modules independent (one module's exception doesn't affect others)
- playwright **dual-width 1680 and 1280** full-page slow-scroll scan: 0 pageerrors · 0 console errors · `scrollWidth == clientWidth` (0 horizontal overflow) · 0 residual non-target-language text
- `document.fonts.check('16px et-book') === true`
- Under `prefers-reduced-motion: reduce`, all animations (incl. the multi-state cover) show static completed frames
- All labels zero-overlap zero-out-of-bounds; retracted or basis-mixed numbers must not appear at the render layer
- Cover A's recursion object matches the report's mechanism; motion direction must explain causality, not just pattern zooming
- Every signature chart passes the text-removal recognition test; the graphic carries at least one industry entity, business constraint, or causal relationship
- Signature charts encode at least two structural variables besides text; number walls, text logic diagrams, icon transmission chains, literal-container reskins, and status-slider lists must not enter main visuals, nor count toward the chart count
- bundle.py single file opens over file:// with 0 errors
- Spot-check 5 in-chart number drill-downs → values and sources trace back to sources.js and the prose fact source

## 3 · Postmortem checklist (every pit predecessors stepped into; read once before starting)

**Canvas / SVG**
1. Canvas not in the CSS size selector (e.g. a new `#cover-canvas-w` missing from the `position:absolute; inset:0; width/height:100%` rule) → 0×0 all blank.
2. Canvas initialized during `display:none` measures 0×0 → must re-`fit()` on `setActive(true)`.
3. An iso body extends `(lw+ld)/2` of projection depth below baseY → bottom labels go below `baseY+isoDrop`.
4. Later-drawn lines pierce earlier-drawn text → draw lines into stemLayer/bottom layer, append the text layer last; canvas text always gets a paper halo (strokeText 3.5–5px / SVG paint-order:stroke ≥4).
5. Iso tower opacity floor <0.3 → low towers read as floating loose slabs.

**Text and truncation**
6. ET Book has only 400/700; writing 600/800 silently falls back → always 700; canvas/SVG fonts synced with CSS.
7. Italic serif glyph width ≥5.8px/char (at 10px); underestimate and you get edge-hugging clipping. SVG text truncated to a pixel budget.
8. Summary sentence-splitting regex must require `[.;]` followed by whitespace, or it truncates at decimal points ("diluting 65.").
9. Truncation tails strip commas/articles/prepositions before adding " …" ("the profit base,…" reads badly).
10. Thousands separators consistent across the whole chart (1,237K not 1237K); when two numbers sit side by side at nearly equal height, stagger the labels.

**Layout**
11. Any section (incl. footer) leaving the prose grid to open its own column width → whole column off + right dead zone. Everything uses the three steps .prose/.wide/.wide.xl.
12. `repeat(auto-fit,…)` collapsing into a 2+1 orphaned column at mid widths → hard-code fixed column counts.
13. Concept-card hover expanding in document flow → whole section +200px page twitch → switch to absolute overlay.
14. Fixed top bar transitioning with whole-bar opacity → mid-state text bleed-through → switch to opaque transform slide-in.
15. Cover exploded view leftBound 0.545W collides with the left-column chips row → 0.585W.
16. Grid column narrower than actual content (block bar + score 190px) → badge crushes the number.
17. Appendix numbering skipping (C.1/C.2/C.4) reads as a typesetting error → on-page numbering must be continuous.

**Animation and acceptance**
18. Screenshot taken before IO entrance animations trigger → misdiagnosed as "blank chart". Slow-scroll the full page first.
19. The top reading-progress bar gets stitched into playwright long-element screenshots → looks like a "full-width horizontal line"; re-check with a viewport screenshot before diagnosing — don't fix it as a layout bug.
20. No wavefront shockwave rings on the recursion cover / no time-flickering viewfinder — flicker reads cheap.
21. Status copy must switch with interaction (after the exploded view assembles, caption/signature strip must be rewritten).

**Data discipline**
22. Don't draw entities absent from the tables (rather missing than fabricated, with a comment); draw gaps as gaps (red hatch + ? + [TBD]), no interpolation.
23. Dual-basis numbers shown side by side are not divided into each other (bases differing by 8× in units need an in-chart warning).
24. `PAL.red` in this token set is electric blue (legacy slot name) — true red is `PAL.neg`; don't mix them up.
25. Drawing an industry entity ≠ theme-native: barns/wafers/units without a fixed-quantity conversion are just stickers; a trough/thermometer merely wrapping a bar or liquid level is just a reskin. Entities must participate in data encoding or real business constraints.
26. Five icons strung on one path ≠ a transmission model: without multi-batch, lag distribution, throughput/loss, or feedback data, fall back to prose or a precise statistical chart — don't add wavy lines for "mechanism feel".

## 4 · Multi-agent parallel human review (after the full site is done)

Dispatch 3–4 diagnose-only review agents in shards: ① all cover variants + first two chapters; ② all mid-section charts (incl. drill-down spot checks); ③ back sections through Sources; ④ responsive (1280/1100/820 three viewports, full human review of viewport screenshots every 1000px + scrollWidth probe).

Prompt essentials (usable verbatim): give the site URL and the assigned section; require slow-scrolling to trigger animations before scrollIntoView + screenshot per object into a designated directory; **visually review each screenshot by hand**; produce a structured list (one-sentence problem / location selector + screenshot name / severity P0 broken · P1 obvious · P2 polish / one-sentence fix); "passes" must also be listed item by item; modify no files, paste no base64. After receiving reports, triage fixes P1→P2, run one full-site regression, then wrap up.

## 5 · Delivery

1. Multi-file site (index.html + css/ + js/ + vendor/)
2. `python3 bundle.py` single-file version (css/js/fonts/topo JSON all inlined, opens over file://)
3. BUILD_LOG.md: record only each round's goal, key decisions, files touched, validation results, and residual risks; use the minimal template in `references/BUILD_LOG-example.md`
