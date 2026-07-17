# React Development Guide

Implementation reference for React webapp building. Read this before writing any code.

---

## WebGL Implementation

When implementing WebGL effects (shaders, 3D models, particles), use React Three Fiber.

### Key Points

- **Shader effects**: If a reference image is provided, read it to understand the target visual style
- **3D models**: Load GLB from the specified path, set up camera/lighting/materials per design spec
- **Loading overlays**: Tie animations to real asset progress (`useProgress`, `LoadingManager`)
- **Visibility control**: Pause render loops when the WebGL section leaves the viewport
- **Always**: Use `@react-three/fiber`, `@react-three/drei`, `@react-three/postprocessing`

For code involving math, physics, or visual algorithms:

| Domain | Verification Method |
|--------|---------------------|
| **Shader/GLSL** | Check UV coords (0-1), verify color output ranges |
| **Physics** | Validate with known cases, check units |
| **Bezier/easing** | Calculate sample points by hand |
| **Trigonometry** | Test boundary cases (0°, 90°, 180°, 360°) |
| **Matrix transforms** | Verify order (scale → rotate → translate) |
| **Particles** | Validate spawn rates, lifetimes, boundaries |

---

## Guidelines

### TypeScript
- The project uses `verbatimModuleSyntax: true` in tsconfig. Always use `import type` for type-only imports:
  ```tsx
  import type { ReactNode, FC } from 'react';       // types
  import { useState, useEffect } from 'react';       // values
  import type { MotionProps } from 'framer-motion';   // types
  import { motion, AnimatePresence } from 'framer-motion'; // values
  ```
- Use tuple assertions for Framer Motion easing arrays:
  ```tsx
  ease: [0.16, 1, 0.3, 1] as [number, number, number, number];
  ```

### Paths & Assets
- Keep `tsconfig.json` aliases in sync with `vite.config.ts`, import via `@/...`.

### Icons
- Do NOT use emoji as icon replacements unless explicitly required.
- Use icon libraries (lucide-react, etc.) or SVG assets instead.

### Tailwind CSS v3
- Enumerate Tailwind classes explicitly or use `cn()`; avoid template literals for class names.
- If design.md uses arbitrary value syntax like `text-[#1A1A2E]` or `bg-[#F5F5F0]`, use that exact syntax — do NOT replace with undefined custom class names.
- ❌ Do NOT add global resets like `* { margin:0; padding:0; }` (Tailwind Preflight already resets).
- ✅ All base/global styles MUST be inside `@layer base` (no unlayered global CSS).

### Canvas / Container Sizing
- Set canvas dimensions via **inline `style` attributes**, NOT CSS classes. The canvas `useEffect` runs on mount before external CSS may be applied.
  ```tsx
  <canvas ref={canvasRef} style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: 1 }} />
  ```

### GSAP
- Register required plugins once per module (`gsap.registerPlugin(ScrollTrigger, SplitText, ...)`).
- Use `@gsap/react`'s `useGSAP` hook to scope timelines and clean up automatically.
- Animate text with official `SplitText` and call `split.revert()` during teardown.

**Library Isolation [CRITICAL]:**

| Context | Use | Avoid |
|---------|-----|-------|
| UI interactions (buttons, cards, lists) | Framer Motion | GSAP |
| Scroll-driven storytelling, canvas backgrounds | GSAP / Three.js | Framer Motion |

❌ **Forbidden:** Mixing GSAP/Three.js with Framer Motion in the same component tree
✅ **Required:** Isolate GSAP/Three.js in dedicated components with strict `useEffect` cleanup

### Framer Motion
- Wrap conditional renders in `<AnimatePresence>` for exit animations.
- Specify `layout="position"` or `layoutId` for layout changes.

**Performance Rules [CRITICAL]:**

| ❌ Forbidden | ✅ Required | Reason |
|-------------|------------|--------|
| `useState` for high-frequency animations | `useMotionValue` + `useTransform` | `useState` triggers re-render every frame |
| `animate` prop for continuous mouse motion | `style={{ x, y }}` binding to MotionValue | Direct binding bypasses render cycle |

### Smooth Scrolling
- Prefer **Lenis** for page-wide smooth scrolling.
- Sync with GSAP ScrollTrigger if needed.

### Layout & Motion
- **Navbar positioning contract** — the Layout, not individual pages, keeps content below the nav:
  - Default: `sticky top-0 z-50` — the nav stays in normal document flow, so no page needs offset bookkeeping.
  - Use `fixed` only when the design calls for an overlay nav (e.g. transparent over a full-bleed hero). Then the shared `Layout` owns the offset: top padding equal to the nav height on its content slot. Full-bleed hero sections opt out inside the page, not by removing the Layout offset.
  - Page agents: do not add nav-height padding/margins in pages, and do not edit the Navbar — when an offset is needed, it lives in `Layout`.
- Give animated containers explicit height with `overflow-hidden` reveals.
- Pass CSS variables as strings: `style={{ color: "var(--black-60)" }}`.

**Viewport Stability [CRITICAL]:**

| ❌ Forbidden | ✅ Required | Reason |
|-------------|------------|--------|
| `h-screen` | `min-h-[100dvh]` | `100vh` includes mobile browser chrome |
| `h-[100vh]` | `min-h-[100dvh]` | `dvh` adapts to browser chrome changes |

### WebGL / React Three Fiber
- Use `React.lazy()` + `<Suspense>` for code-splitting heavy WebGL components.
- Drive motion with `useFrame`; avoid manual `requestAnimationFrame` loops.
- Full-screen shaders: 2×2 plane inside orthographic camera.
- Precompute random positions with `useRef` for stable particle layouts.
- **Mouse interaction with particles**: Never modify base position directly. Use separate displacement with lerp decay:
  ```tsx
  // ✅ Correct
  displacement.x += repelForce;
  displacement.x *= 0.95;  // Lerp decay each frame
  finalPosition = originalPosition + sineWave + displacement;
  ```

### Animation Performance

**Hardware Acceleration [CRITICAL]:**

| ❌ Never Animate | ✅ Always Use | Reason |
|-----------------|--------------|--------|
| `top`, `left`, `right`, `bottom` | `transform: translate()` | Layout properties trigger reflow |
| `width`, `height` | `transform: scale()` | GPU handles transform natively |

**Perpetual Animation Isolation [CRITICAL]:**
- Infinite loops MUST be isolated in dedicated micro-components
- MUST wrap with `React.memo()` to prevent parent re-renders from resetting animation

---

## Project Setup

The template is already pre-configured with these settings. These are reference notes — only modify if the template config is missing or broken.

### No StrictMode

Do NOT wrap in `<React.StrictMode>`. It causes canvas effects to run twice.
```tsx
createRoot(document.getElementById('root')!).render(<App />)
```

### BrowserRouter

Use `BrowserRouter` from `react-router-dom`, not `HashRouter`. The serving layer
provides SPA fallback (rewrites unknown routes to `index.html`), so clean URLs
work for static sites too — and a frontend-only site can later be grafted with a
backend without any router change.

#### Layout + routing contract — pick ONE pattern, never mix

If you add a shared `Layout` (sidebar/header wrapping the pages), its content
slot **must** match how `App.tsx` provides pages. Mixing the two patterns is a
silent killer: the page renders to a **blank `<main>`** with **no error**, and
`npm run build` still passes (it's a runtime bug, not a type error). Pick one:

**A — Children pattern** (Layout wraps `<Routes>`): Layout renders **`{children}`**.
```tsx
// Layout.tsx
export default function Layout({ children }: { children: React.ReactNode }) {
  return <div>{/* sidebar/header */}<main>{children}</main></div>;
}
// App.tsx
<Layout><Routes><Route path="/" element={<Home/>} /></Routes></Layout>
```

**B — Nested-route (layout-route) pattern**: Layout renders **`<Outlet/>`** and is
itself a route element with child routes.
```tsx
// Layout.tsx
import { Outlet } from 'react-router';
export default function Layout() { return <div>{/* sidebar */}<main><Outlet/></main></div>; }
// App.tsx
<Routes>
  <Route element={<Layout/>}>
    <Route index element={<Home/>} />
    <Route path="stats" element={<Stats/>} />
  </Route>
</Routes>
```

**The fatal mistake to avoid:** `Layout` renders `<Outlet/>` (pattern B) but
`App.tsx` passes routes as **children** (`<Layout><Routes>…</Routes></Layout>`,
pattern A). `<Outlet/>` only renders **nested routes** and silently ignores
`children`, so the whole page body disappears. If your Layout uses `<Outlet/>`,
App **must** use nested `<Route>`s; if it uses `{children}`, App **must** wrap the
routes as children. Never one of each.

### Dependencies

Install any page-specific packages (chart libraries, etc.) that your assigned pages require.

---

## Full-Stack Auth Contract

Applies whenever the project has the auth graft (look for `src/hooks/useAuth.ts` + `api/`). Skip for frontend-only projects.

**Owned by the backend graft — do NOT create, modify, or duplicate these files:**
`src/pages/Login.tsx`, `src/hooks/useAuth.ts`, `src/const.ts`, `src/components/AuthLayout.tsx`, `src/components/AuthLayoutSkeleton.tsx`, `src/providers/trpc.tsx`, and anything under `api/` or `db/`.

| Need | ✅ Use | ❌ Avoid |
|------|--------|----------|
| Read auth state | `const { user, isAuthenticated, isLoading, logout } = useAuth()` | Hand-rolled session/cookie checks |
| "Sign in" CTA | `import { LOGIN_PATH } from "@/const"` and navigate/`<Link>` to it | Hand-constructed OAuth URLs, scopes, or `/api/oauth/*` links |
| "Register / Sign up" CTA | Link it to `LOGIN_PATH` too (OAuth auto-provisions users on first login) | A custom Register page with its own OAuth logic |
| Gate a page on login | `isLoading` → skeleton/null; `!isAuthenticated` → prompt linking `LOGIN_PATH` | Redirects to hand-built auth routes |

The template's `Login.tsx` is the only component that constructs the OAuth URL.
