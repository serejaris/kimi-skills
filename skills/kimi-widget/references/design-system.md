# Kimi Perspective Widget — Design System

The full visual style for every widget: visual rules, typography, components/motion/layout, the
runtime token map, and the application checklist. Read this before writing widget code unless the
user already fixed the visual decisions for you.

---

## 1. Visual rules

### Core rule

Black and white are the primary colors. Gray is the neutral support system for hierarchy,
separators, disabled states, metadata, hover/active tints, and subtle borders. Accent colors come
only from the runtime tokens (never invented) and are the last resort — use them only after black,
white, and gray are insufficient to express required differences such as status, priority, chart
series, file/category markers, progress groups, or multiple avatars.

Interaction emphasis is dark, not blue: focus rings, hover states, selected items, active tabs,
and primary buttons use `--kimi-color-text-primary` and gray tints. The accent blue
(`--kimi-color-accent`) is reserved for data visualization and true semantic accents — never for
generic "this is interactive" styling. Training data associates blue with interactive; Kimi does
not.

Do not set a page, body, canvas, card, or panel base background color unless explicitly asked.
Preserve the existing background, or use `transparent` / `inherit`; the host provides the
background.

### Visual discipline

- Do not prescribe a visible base fill. No default page, card, panel, or canvas background.
- UI chrome is black/white first: primary text, key values, active states, primary controls,
  high-emphasis icons.
- Use gray only for hierarchy and structure: secondary/tertiary text, borders, separators,
  disabled states, hover/active tints.
- Use accent colors only for multi-color semantics: status (`--kimi-color-danger`,
  `--kimi-color-positive`, `--kimi-color-warning`), priority dots, chart series (`--kimi-chart-*`),
  tags, category chips, progress fills, avatars. For tag/chip/status backgrounds, tint the token to
  10–25% — `color-mix(in srgb, var(--kimi-color-danger) 12%, transparent)` — instead of a solid
  fill. Never use any accent as a dominant fill, page tint, or background theme.
- Avoid colorful gradients. If a gradient is necessary for a data mark, keep it subtle and within
  one hue family (opacity steps of a single token, not hue blends).
- Avoid decorative base fills, gradient orbs, bokeh, heavy color washes, nested decorative cards,
  marketing-page hero treatment, heavy shadows, blur, and glassmorphism. Keep surfaces clean/flat.
- Use fine borders and compact radii: 0.5–1px separators, 6px chips, 8px icon buttons, 10px list
  cards/inputs, 12px elevated panels.

### Chart colors

Color explains data, not decorates it. Sequential is the default; categorical is the exception;
diverging is the last resort. Derive every chart color from the runtime tokens.

- **Categorical** (truly independent series), in this order: `--kimi-chart-1` (blue) →
  `--kimi-chart-2` (red) → `--kimi-chart-3` (green) → `--kimi-chart-4` (purple) →
  `--kimi-chart-5` (neutral gray). Maximum 5 hues; beyond that differentiate with line style
  (solid / dashed / dotted), not new colors.
- **Comparable series** (same metric across categories — revenue by region, temperature by city):
  same-hue opacity instead of categorical. Steps 100 / 70 / 50 / 40 / 25% via
  `color-mix(in srgb, var(--kimi-chart-1) 70%, transparent)`.
- **Positive vs baseline** (actual vs target): blue vs neutral gray. **Positive vs negative**
  (profit/loss, risk): blue vs red. **Deviation from a true midpoint**: red ↔ neutral ↔ blue
  diverging — only when a real zero/break-even center exists.
- Baseline, reference lines, grid, and "no data" use `--kimi-color-text-quaternary`.
- Heatmaps and stacked areas are always sequential, never categorical. Pie/donut prefers blue
  sequential — slices are parts of one whole; use categorical only for independent competitors.
- Colorblind safety: never pair green with red in one chart (`--kimi-chart-3` with
  `--kimi-chart-2`, or `--kimi-color-positive` with `--kimi-color-danger`); colors must stay
  distinguishable in grayscale; never rely on color alone — add labels or patterns.

---

## 2. Typography

Use the Kimi client fonts, not artifact-specific or presentation fonts.

- UI/body must use `font-family: var(--kimi-font-sans)`.
- Every HTML widget starts with a local font reset: set the root wrapper to
  `font-family: var(--kimi-font-sans)`, set `button, input, select, textarea { font: inherit; }`,
  and set `svg text { font-family: var(--kimi-font-sans); }` when using inline SVG text.
- Primary display values must use `var(--kimi-font-sans)`, including timers, prices, counts,
  percentages, dates, times, generated passwords, BMI values, counters, and chart labels.
- For numeric display values, use
  `font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1;` instead of switching to a
  mono font.
- Reserve `var(--kimi-font-mono)` for code, hashes, raw identifiers, logs, and genuinely technical
  monospace tables only. Keep mono small and secondary; never use mono for large hero metrics,
  timers, generated passwords, BMI values, counters, prices, percentages, or slider values.
- Do not hardcode font stacks (`Inter`, `SF Pro Text`, `PingFang SC`, `system-ui`, `Poppins`,
  `Oswald`, `JetBrains Mono`). Do not introduce decorative display fonts. If a fallback is
  required, keep it inside the variable fallback: `font-family: var(--kimi-font-sans, sans-serif)`.

### Scale

The base body size is **16px (`t2`, line-height 24px)** — the foundation sets this on `body`, so
plain text is already correct; don't shrink it back down.

- Body text: 16px (`t2`), line-height 24px. Emphasized body: 16px weight 500 (`t2Emphasized`).
- Title / page labels: 17–20px, weight 500 (`pageTitle` 17 / `t0` 20).
- Secondary text and dense table cells: 14–15px (`b2` / `b1`).
- Metadata and compact labels: 12px (`c1`).
- Primary display values: usually 28–42px, never larger than 48px in a compact widget; weight
  500, line-height at least 1.08 so glyphs don't crop.
- Letter spacing must be 0 or positive — never negative.
- **Two weights only**: 400 regular and 500 bold. Avoid 600/700 — they look heavy against the host.
- **Sentence case always** — never Title Case or ALL CAPS, including SVG text labels and headings.
- No mid-sentence bolding. Entity, class, and function names go in `code style`, not bold.

---

## 3. Components, motion & layout

### Controls & icons

- Native controls (sliders, switches, checkboxes, radios, progress bars) are UI chrome, not data
  accents. Keep them neutral: `accent-color: var(--kimi-color-text-primary)` or gray
  border/surface tokens. Do not use browser default blue or `accent-color: var(--kimi-color-accent)`
  for generic controls — only when the control itself is a semantic accent/state selector.
- **Destructive and secondary row actions are hover-revealed, not always visible.** Delete,
  remove, clear, and similar per-item actions on list rows, cards, chips, and table rows stay
  hidden by default and appear on the parent's `:hover` (or `:focus-within` for keyboard users):

  ```css
  .row .row-actions { opacity: 0; transition: opacity var(--t-fast) var(--ease-out); }
  .row:hover .row-actions, .row:focus-within .row-actions { opacity: 1; }
  ```

  Use `opacity`/`visibility`, not `display: none`, so the layout doesn't shift and the control
  stays keyboard-reachable. A permanently visible delete button on every row reads as noisy and
  dangerous. Exception: a single, deliberate destructive action that is the widget's point (e.g.
  a confirm dialog's "Delete" button) stays visible.
- Icons: prefer the shipped Kimi icon library — read
  [icon-system.md](icon-system.md) and pick from `references/icons/manifest.json`, then inline the
  SVG from `assets/icons/` with `currentColor`. Only build a custom icon (same 1.8px outlined
  style, 24×24 grid) when no library icon matches. Do not import, link, or fetch external icon
  assets. Do not use emoji as UI icons; if emoji are decorative, set `font-size` explicitly.
  **24px is the maximum icon size** — if a spot seems to need a larger icon (empty state, hero
  mark, big decorative glyph), don't use an icon there at all; solve it with typography or layout.

### Spacing & radius

All spacing snaps to the token scale: **4 / 8 / 12 / 16 / 20 / 24 / 32px**. No values off the
scale — `7px`, `13px`, `17px` read as accidents, not decisions. When a gap needs to sit between
two steps, pick the smaller one; widgets are compact surfaces.

All radii come from the radius scale: **4 / 6 / 8 / 10 / 12 / 16px / full**. Usage mapping: 6px
chips, 8px icon buttons, 10px list cards/inputs, 12px elevated panels, full for pills/avatars.

**Nested radii: outer is always larger than inner.** When a rounded element sits inside another
rounded container, the inner radius must be smaller — compute it as
`inner = outer − padding` (e.g. a 12px panel with 8px padding holds 4px-radius children), and
never let it go below 4px or above the container's radius. Equal radii inside each other, or an
inner element rounder than its container, read as broken corners. Concentric corners are the
check: the two curves should share a center.

### Animation & layout

- Use small CSS transitions or inline JavaScript with native browser APIs only. No Motion, GSAP,
  React, Vue, npm packages, CDN scripts, or external modules. Keep motion purposeful and short;
  avoid loops that don't communicate progress or state. Use the shared motion tokens instead of
  arbitrary values: durations `--t-micro` / `--t-fast` / `--t-normal` / `--t-slow` (60–300ms),
  easings `--ease-out` / `--ease-in` / `--ease-standard`.
- Responsive, natural width `100%`; the host card fills the content column. No `position: fixed` —
  everything stays in normal document flow. Avoid nested scrolling; let height follow content,
  don't reserve empty vertical space. Keep text readable in both light and dark mode.

### Spatial depth (optional)

Use only when it helps; keep it subtle, no visible base backgrounds.

```css
.scene  { perspective: 1400px; transform-style: preserve-3d; }
.layer-bg  { background: transparent; transform: translateZ(-100px) rotateX(3deg); }
.layer-mid { background: transparent; transform: translateZ(-50px) rotateX(1.5deg); }
.widget    { background: transparent; transform: rotateX(5deg) rotateY(-3deg); transform-style: preserve-3d; }
```

Optional parallax (low intensity); guide lines / isometric grids stay extremely low opacity and
neutral gray — they support spatial reading, not decoration.

### Streaming-friendly authoring order

Output streams token by token; scripts run only after markup is complete. Structure code so useful
content appears early:

1. `<style>` (short) and static HTML/SVG that looks useful immediately.
2. Local data inlined into the HTML.
3. `<script>` last for interactivity.

Prefer inline `style="..."` over `<style>` blocks so controls look correct mid-stream. Keep
`<style>` short (~15 lines). No `<!-- comments -->` or `/* comments */` (waste tokens, hurt
streaming). For SVG, put `<defs>` (markers) first, then visual elements immediately. Use solid flat
fills — gradients, shadows, and blur flash during streaming DOM diffs.

---

## 4. Runtime token mapping

The iframe has the Kimi design system pre-loaded. Map the style onto these runtime variables;
prefer runtime variables over hardcoded values.

- Text: `--kimi-color-text-primary`, `--kimi-color-text-secondary`, `--kimi-color-text-tertiary`,
  `--kimi-color-text-quaternary`
- Surfaces: `--kimi-color-surface`, `--kimi-color-surface-muted`, `--kimi-color-surface-raised`,
  `--kimi-color-surface-strong`
- Structure: `--kimi-color-border`
- Status: `--kimi-color-danger`, `--kimi-color-positive`, `--kimi-color-warning`
- Accent (data visualization and semantic accents only, never generic interaction):
  `--kimi-color-accent`
- Chart series: `--kimi-chart-1` … `--kimi-chart-5` (blue, red, green, purple, neutral)
- Motion: `--t-micro`, `--t-fast`, `--t-normal`, `--t-slow`, `--ease-out`, `--ease-in`,
  `--ease-standard`
- Fonts: `--kimi-font-sans`, `--kimi-font-mono`

Raw client tokens (`--seo-chat-*`) and compatibility aliases (`--color-text-primary`,
`--color-background-secondary`, `--color-border-tertiary`) are also available when they fit better.
Do not use `prefers-color-scheme` or maintain a separate light/dark token table — the client syncs
the active theme into the iframe. 

---

## 5. Application checklist

1. Preserve the existing background.
2. Convert main UI color decisions to black/white first; interaction emphasis uses
   `--kimi-color-text-primary`, never accent blue.
3. Use gray for hierarchy and structure.
4. Add accent tokens only for required multi-state or multi-category distinctions (status,
   priority, chart series, tags) — tinted 10–25% for backgrounds, following the chart color rules
   for data marks.
5. Replace presentation typography with `var(--kimi-font-sans)` / `var(--kimi-font-mono)`.
6. Tighten large decorative spacing into app-like density; every gap and padding snaps to the
   4 / 8 / 12 / 16 / 20 / 24 / 32 scale, nested radii are outer-large-inner-small.
7. Verify no accent color has become a base fill or dominant theme color.
