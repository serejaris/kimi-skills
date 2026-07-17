---
name: kimi-widget
description: Kimi widget design system. Read this BEFORE rendering any inline widget. Defines when to use a widget and the runtime contract; the full visual style lives in references/design-system.md. Your widget runs in a sandboxed iframe with the Kimi design system pre-loaded — reference the provided CSS variables, never hardcode colors or fonts.
---

# Kimi Widget

A widget is a compact visual or interactive surface rendered inline in the conversation:
diagrams, dashboards, calculators, sliders, comparisons, timelines, state machines, small
simulations. Use one when seeing structure helps the user understand, compare, inspect, or act
on the answer better than prose alone.

## When to generate a widget

- The answer has spatial, sequential, systemic, comparative, numeric, or interactive structure.
- The user does not need to say "show", "visualize", "chart", or "widget" — proactive widgets are
  expected when the structure is there.
- If the user gives a compact visual spec without a verb ("REST vs GraphQL table", "checkout state
  machine", "pricing calculator"), render it as a widget instead of only describing it.

Do **not** use a widget for: ordinary prose answers, routine line-by-line code explanations, file
lists / galleries / final deliverables, blocking input workflows, destructive or native actions,
or large long-lived apps.

## Runtime contract

The widget runs in a **sandboxed iframe with the Kimi design system CSS already loaded**. All CSS
variables, form-element styles, and SVG classes are available at runtime — reference them, do not
redefine them.

- Allowed: HTML, SVG, CSS, inline JavaScript, native browser APIs.
- **Not allowed**: external scripts, modules, stylesheets, images, fonts, CDN libraries, npm
  packages, `fetch`, or WebSocket. For charts/diagrams use SVG, Canvas, CSS, or plain DOM.
- **Text goes in your response, visuals go in the widget.** All explanatory prose, intros, and
  summaries live OUTSIDE the widget.
- **After the widget renders, don't narrate it.** Once you've called the widget tool and the widget
  is done, do not re-summarize or repeat what you just did — the visual speaks for itself. Say only
  what the widget cannot.
- **Sending intent back.** An interactive widget may call `window.sendPrompt(text)` (when the host
  injects it) to push the user's next intent into the conversation. Write `text` as a real user
  message — what the user would actually type — never a robotic confirmation like "I selected
  option A, please proceed."
- Never hardcode colors, fonts, or border-radius — always use `var(--xxx)`. Hardcoded values break
  dark mode and look inconsistent with the host UI.

## ⚠️ Required: read the design system before you design

**Unless the user has given you very explicit, precise styling instructions for this specific
widget, you MUST read [references/design-system.md](references/design-system.md) before writing the
widget code.** It carries the full Kimi Perspective Widget style — visual rules, typography,
component patterns, runtime token map, and the application checklist. Do not decide a widget is too
simple, too static, or too small to need it. Skip it only when the user's instructions already fix
the visual decisions for you.

If the widget uses icons, also read [references/icon-system.md](references/icon-system.md): the
skill ships 105 Kimi icons (`assets/icons/`, indexed in `references/icons/manifest.json`) — pick
from the library and inline the SVG instead of drawing your own or using emoji.
