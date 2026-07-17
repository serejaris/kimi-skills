---
name: vibecoding-webapp-swarm
description: >
  Build any web-based project: websites, landing pages, web apps, dashboards,
  browser games, portfolios, and interactive experiences. Design-first
  React workflow. Skip if the user explicitly requests a non-React
  framework (Vue, Svelte, Angular, vanilla HTML) or the task is unrelated to
  web UI (CLI tools, scripts, data pipelines).
---

# Vibecoding — Multi-Agent Webapp Building

Design-first, multi-agent workflow for building rich, multi-page React webapps. We aim for **sophisticated, content-rich websites** — not minimal demos. Think 5-10+ pages with rich content, interactive features, animations, and polish.

**Full-stack requests** (backend APIs, databases, auth, persistence): supported via the **backend-building-swarm** companion skill, which grafts a tRPC + Drizzle + Hono backend (see Phase 5 — Backend Graft). Use the full-stack path when the app genuinely needs server-side data, auth, or persistence. For purely presentational sites, stay frontend-only with realistic mock data — it's simpler and faster. (Next.js specifically is not the stack here — we use React + Vite + Hono.)

**Default tech stack (pinned versions — communicate to all subagents):**
- Node.js 20 · Tailwind CSS v3.4.19 · Vite v7.2.4 · React 19 + TypeScript · shadcn/ui

Use this stack unless the user explicitly specifies a different one (e.g. Vue, Svelte, vanilla JS, Python+Flask). If the user specifies a different stack, follow their choice first — but you can still borrow the orchestration principles from this skill (design-first workflow, multi-agent decomposition, parallel page agents, octopus merge).

## Companion Skills

### design-guide (`/app/.agents/skills/vibecoding-webapp-swarm/design-guide.md`)

Design reference for the Pro_Designer subagent. Covers visual capabilities (GSAP, Framer Motion, Three.js, Lenis, Google Fonts), design document format, animation spec requirements, and asset manifest format. **Read by the Designer subagent** at the start of Phase 2.

### react-dev (`/app/.agents/skills/vibecoding-webapp-swarm/react-dev.md`)

React implementation guide. Covers GSAP, Framer Motion, Three.js/R3F, Tailwind v3, animation performance, layout patterns. **Read by all implementation subagents** (scaffold + page agents). Not read by Designer or main agent.

### webapp-building (`/app/.agents/skills/webapp-building-swarm/SKILL.md`)

Tech stack reference: project scaffolding via `init-webapp.sh`, design templates, build pipeline. **Read by main agent** to understand init and build. (Worktree setup uses swarm-workspace's `setup-local.sh`.)

### backend-building (`/app/.agents/skills/backend-building-swarm/SKILL.md`)

Backend graft — tRPC + Drizzle + Hono + MySQL + optional Kimi auth. Provides
`init.sh` (full graft via `--features`, or `--template` provision-only).
**Read by the main agent only, for full-stack apps** — the main agent runs the
graft itself in Phase 5 (see Phase 5 — Backend Graft).

### swarm-workspace (`/app/.agents/skills/swarm-workspace/SKILL.md`)

The two-tier filesystem contract (shared coordination repo + per-subagent
worktrees) and the canonical `setup-local.sh` for spinning up a worktree — call
it with `NODE_MODULES_SRC` pointing at the stack's prebuilt `node_modules`.
**Reference** for the worktree lifecycle and gotchas (e.g. never `git worktree prune`).

## Core Principles

1. **Design-first.** `design.md` is written before any implementation begins. It is the single source of truth.
2. **Design fidelity.** Subagents implement `design.md` faithfully — exact colors, exact values, exact text. No "improving" or substituting.
3. **Main agent owns init, merge, versioning.** Sub-agents implement and commit on their branches.
4. **Parallelism by pages AND features.** Each sub-agent can own pages (About, Services) or features (shopping cart, search system, interactive calculator). Group related work into one agent.
5. **Aim for richness.** We have multi-agent parallelism — use it. Build content-rich, feature-complete websites rather than minimal ones. 5-10+ pages, interactive features, animations.
6. **Git worktrees isolate work.** Heavy work (editing, builds) happens on local filesystems via `setup-local.sh`; the OSS repo is the coordination hub. Branches and worktrees are per-operation and disposable; `master` on the shared repo is the only durable lineage.
7. **Create the version once per delivery and STOP.** One `mshtools-website_version_manager` `build_version` call per delivery, then no verification loop: do NOT open the URL, take screenshots, or review. Each delivery merges its branch back into master; later fixes and rollbacks fork fresh branches from master (see "Iterating After Delivery").
8. **Full-stack is opt-in.** When the app needs real data/auth/persistence, graft a backend (tRPC+Drizzle+Hono) via backend-building-swarm in Phase 5 — run once, before page branches fork, so all page agents inherit the tRPC client. Otherwise build a frontend with mock data.

## Mode Selection

| Condition | Mode |
|-----------|------|
| Building a website/webapp IS the primary task | **Mode A** (multi-agent) |
| Building a website/webapp is sophisticated or content-rich | **Mode A** (multi-agent) |
| Cloning/replicating an existing website | **Mode A** (multi-agent) |
| Website is a side deliverable AND simple (1-3 pages, no complex interactions) AND the primary task already requires multi-agent work | **Mode B** (single agent) |
| When in doubt | **Mode A** (multi-agent) |

---

## Mode A — Webapp as Main Task (Multi-Agent)

### Phase 1: Plan & Init (Main Agent)

1. **Read skills**: Read this SKILL.md and `webapp-building-swarm/SKILL.md`.
2. **Init project**:
   ```bash
   PROJECT_PATH=$HOME/init REMOTE_PATH=/mnt/agents/output/app bash /app/.agents/skills/webapp-building-swarm/scripts/init-webapp.sh "<website-title>"
   ```
   Creates the project locally at `$HOME/init`, initializes git, clones to `/mnt/agents/output/app` (shared OSS hub).
   Use the default template (`0-origin`) unless the user explicitly requests a specific template by name.
3. **Research** (if needed): Browse URLs, search for content. Write findings to `/mnt/agents/output/info.md`.
4. **Decide build type** (a capability decision — NOT design): does the app need real server-side data, auth, or persistence?
   - **Frontend-only** (default for presentational sites): mock data.
   - **Full-stack**: read `backend-building-swarm/SKILL.md`; Phase 5 grafts the backend. Backend mode follows the template — a frontend template (e.g. `0-origin`) → full graft via `--features db,auth`; a `*-fullstack` template → provision-only via `--template`.

   Either way, scaffold with **`BrowserRouter`** — the server provides SPA fallback (so it works for a pure-static site too), and a frontend-only site can later be grafted with a backend without any router change.

**Important:** Do NOT plan page structure, page count, visual direction, or design details in this phase. Those decisions belong entirely to the Designer in Phase 2. Your task here is to init the project, gather research, and pick the build type (capability only).

### Phase 2: Design (Pro_Designer Subagent)

Create a subagent named **"Pro_Designer"** (name must contain "designer" — case-insensitive — for model routing).

**Designer system prompt** — use this exact text (do NOT customize per query):
> "You are a world-class web designer. You create comprehensive, detailed design documents for websites. You have deep expertise in modern web design, typography, color theory, animation, and responsive layouts."

**Designer task prompt** — use this exact template, filling in only {USER_QUERY} and {RESEARCH} placeholders:

```
Read `/app/.agents/skills/vibecoding-webapp-swarm/design-guide.md` in full. Follow it as your design reference.

## User Request

"{USER_QUERY}"

{RESEARCH — include this section only if /mnt/agents/output/info.md exists:
## Research Findings
[paste contents of info.md]
}

## Instructions

Read the user's request and create a complete design. Determine the appropriate page count, structure, and visual direction based on the request. Aim for a content-rich, ambitious website with interactive features and visual polish. For clone/replicate requests, faithfully capture the main page's design and expand into additional sub-pages the original site would have.

Write all design files to `/mnt/agents/output/design/`:
- `design.md` — Global design document
- `[page].md` — One per page, named by topic (e.g. `home.md`, `about.md`, `services.md`)
```

**Rules — the prompt must be exactly the template above:**
- Do NOT add sections like "Key Context", "Design Guidelines", "Important Notes", or "Output Requirements".
- Do NOT add your own creative interpretation of the user's request (color suggestions, style directions, reference companies, mock data instructions).
- Do NOT paraphrase the user request — copy it character-for-character.
- The Designer reads the design guide and user request; it makes ALL creative decisions independently.

### Phase 3: Read Design & Delegate (Main Agent)

After the Designer completes:

1. **Read `design/design.md`** — the global design and page list. You do NOT need to read per-page designs.
2. **Decide grouping**: Based on **the page list in design.md** (not your own assumptions), group pages/features into 3-6 parallel agents. Each agent can own multiple related pages or features (e.g., "Services + Pricing" → one agent, "Shopping cart + checkout" → one agent). Full-stack auth: the backend graft owns the Login page (`src/pages/Login.tsx`), and OAuth auto-provisions users on first login (no Register flow) — exclude login/register pages from grouping; register CTAs link to the login flow.
4. **Create scaffold branch only** (page branches are created AFTER scaffold merge — see Phase 5):
   ```bash
   cd /mnt/agents/output/app
   git branch scaffold
   ```
5. **Launch Scaffold subagent**.

### Phase 4: Scaffold (Single Subagent)

Launch one subagent. Its prompt MUST include:

1. "Run `NODE_MODULES_SRC=/app/.agents/skills/webapp-building-swarm/scripts/template/node_modules bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh scaffold $HOME/app-scaffold`"
2. "Read `/app/.agents/skills/vibecoding-webapp-swarm/react-dev.md` in full."
3. "Read `/mnt/agents/output/design/design.md` in full."
4. "Read `/mnt/agents/output/design/home.md` in full (the landing page design)."
5. Tech stack versions: Node.js 20, Tailwind CSS v3.4.19, Vite v7.2.4.
6. The original user request.
7. **"Generate media assets: Read the Assets section in design.md. For each image asset listed, use the image generation tool with the description as the prompt. For each video asset listed, use the video generation tool with the description as the prompt. Save all generated media to `$HOME/app-scaffold/public/<filename>`. After generating all media, commit: `cd $HOME/app-scaffold && git add public/ && git diff --cached --quiet || git commit -m 'assets: add generated media'`"**
8. "Implement the COMPLETE landing/home page following `design/home.md`."
9. "Create shared components at these EXACT paths (page agents depend on them): `src/components/Navbar.tsx` (with links to all routes), `src/components/Footer.tsx`, `src/components/Layout.tsx`. Navbar positioning: default to `sticky top-0 z-50` (in normal flow). Use `fixed` only if design.md calls for an overlay nav, and then `Layout` adds matching top padding to its content slot so every page starts below the nav (full-bleed heroes opt out inside the page). Page agents do not compensate for nav height — see react-dev.md 'Navbar positioning contract'."
10. Set up **`BrowserRouter`** with route stubs for all sub-pages (the server provides SPA fallback; the backend graft's wiring also keys on `<BrowserRouter>` / `</Routes>`). For a `*-fullstack` template the router is already wired — don't change it. **If you introduce a shared `Layout`, its content slot and `App.tsx` MUST use the same routing pattern** — `<Outlet/>` ⇒ nested `<Route>`s, OR `{children}` ⇒ `<Layout><Routes>…</Routes></Layout>`. Mixing them renders a blank page that still builds clean — see react-dev.md “Layout + routing contract.”"
11. For full-stack/auth apps, the Phase 5 backend graft owns and plants the auth files (`src/pages/Login.tsx`, `src/hooks/useAuth.ts`, `src/const.ts`, `src/components/AuthLayout.tsx`, `src/components/AuthLayoutSkeleton.tsx`). Leave these to the graft. Make `src/pages/Login.tsx` a plain placeholder page (e.g. a centered "Login" heading) so its route resolves during scaffold — Phase 5 overwrites it with the real OAuth page. Keep `useAuth`, `const.ts`, `AuthLayout*`, and any OAuth URL/scope/callback logic out of the scaffold; they arrive with the graft. In the Navbar, the account area is a single static "Sign in" link to `/login` marked `{/* AUTH-SLOT: rewired to useAuth() in Phase 5 */}` — no profile dropdowns or mocked logged-in state.
12. "Configure Tailwind theme, global CSS, Google Fonts per design.md."
13. "Install additional packages from design.md Dependencies."
14. "Reference generated media via `/<filename>` (e.g. `<img src="/hero-bg.png" />`, `<video src="/hero-loop.mp4" />`) — these are served from `public/` at build time."
15. "`cd $HOME/app-scaffold && git add -A && git commit -m 'scaffold: landing page + shared infra'`"
16. "After committing, return immediately. No need to run the dev server, open a browser, take screenshots, or verify your work. The main agent handles building and deployment."

### Phase 5: Merge Scaffold, Graft Backend (full-stack), & Create Page Branches (Main Agent)

1. **Merge scaffold**:
   ```bash
   cd /mnt/agents/output/app && git merge scaffold --no-edit
   ```

2. **Backend graft/product pass — FULL-STACK ONLY** (skip entirely for frontend-only). The main agent runs this pass itself, in its own `$HOME/app-backend` worktree — not via a separate subagent, because `init.sh` writes a gitignored `.env` that never travels through the merge: it survives only in the sandbox where it ran, which must be the main agent's own so the build can read it and the staging step below (`cp … .env`) can copy it into later worktrees. Run the backend graft **once, here**, then add the app-specific schema/query functions/routers implied by `design.md` before page branches fork. After backend work, revise scaffold-created shared frontend surfaces so they are compatible with the full-stack environment, then page agents inherit and consume the tRPC client + contracts. Read `backend-building-swarm/SKILL.md` first.

   **Auth-enabled apps — this pass owns the Navbar rewiring** (shared components are frozen once page branches fork):
   - Rewire the scaffold Navbar's `{/* AUTH-SLOT */}` (and any login/profile UI in `Layout`/`Footer`) to `useAuth()`: while `isLoading` render a neutral placeholder; unauthenticated → "Sign in" linking to `LOGIN_PATH` from `@/const`; authenticated → user name/avatar + a logout action calling `logout()`.
   - Replace every static login/register CTA: they link to `LOGIN_PATH` (OAuth auto-provisions users; there is no Register flow).
   - Consume the graft-installed auth files as-is (`src/pages/Login.tsx`, `src/hooks/useAuth.ts`, `src/const.ts`, `AuthLayout*`) — do not modify them.
   - Verify before committing: `grep -rn "useAuth" src/components/Navbar.tsx` hits, and `grep -rn "oauth/authorize" src/ | grep -v src/pages/Login.tsx` is empty (only the template Login page constructs the OAuth URL).
   ```bash
   cd /mnt/agents/output/app && git branch backend
   NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
     bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh backend $HOME/app-backend
   # graft mode (frontend template):
   PROJECT_PATH=$HOME/app-backend \
     bash /app/.agents/skills/backend-building-swarm/scripts/init.sh "<app-title>" --features db,auth
   #   (OR, if a *-fullstack template was used, provision-only — auto-detected via .backend-features.json:)
   #   PROJECT_PATH=$HOME/app-backend bash .../init.sh "<app-title>" --template
   # Add app-specific tables/queries/routers from design.md here.
   # Revise scaffold-created shared frontend surfaces for the full-stack environment.
   # For auth-enabled apps, wire shared shell/auth-dependent UI to the generated useAuth/login/logout contract.
   # Then sync DB schema before page branches fork.
   cd $HOME/app-backend && npm run db:push
   cd $HOME/app-backend && git add -A && (git diff --cached --quiet || git commit -m 'backend: add app data model and API')
   cd /mnt/agents/output/app && git merge backend --no-edit
   cp $HOME/app-backend/.env /mnt/agents/output/app/.env   # .env is gitignored — stage it for later worktrees
   ```

3. **Create page branches** — they must branch from master (now scaffold + optional backend) so page agents inherit scaffold code (Navbar, Footer, Layout, shared styles) AND, for full-stack, the tRPC client:
   ```bash
   cd /mnt/agents/output/app
   git branch <group1>
   git branch <group2>
   # ... one branch per agent group
   ```

### Phase 6: Parallel Subagents

Launch **all** subagents simultaneously (single message, multiple `task` tool calls).

Each subagent prompt MUST include:

1. "Run `NODE_MODULES_SRC=/app/.agents/skills/webapp-building-swarm/scripts/template/node_modules bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh <branch> $HOME/app-<branch>`" (each subagent MUST use a unique path — `$HOME/app-<branch>`)
2. "Read `/app/.agents/skills/vibecoding-webapp-swarm/react-dev.md` in full."
3. "Read `/mnt/agents/output/design/design.md` in full."
4. "Read `/mnt/agents/output/design/[page].md` for your assigned page(s)."
5. Tech stack versions: Node.js 20, Tailwind CSS v3.4.19, Vite v7.2.4.
6. Clear assignment — pages AND/OR features. A subagent can own a feature like "shopping cart system" or "interactive quiz", not just named pages.
7. "Read the existing design system from the scaffold: `cat src/components/Navbar.tsx src/components/Footer.tsx src/index.css src/App.tsx`"
8. "ONLY create/modify files for your assigned scope. Must NOT modify: `src/App.tsx`, `src/index.css`, shared components, `public/`. **Full-stack: also must NOT modify `api/router.ts` or `db/schema.ts`** — these are merge-conflict seams owned by the backend graft/product pass. Consume existing tRPC procedures via `trpc` from `@/providers/trpc`. **Auth apps: also must NOT create or modify `src/pages/Login.tsx`, `src/hooks/useAuth.ts`, `src/const.ts`, `src/components/AuthLayout*.tsx`, `src/providers/trpc.tsx`, or anything under `api/`.** Follow react-dev.md 'Full-Stack Auth Contract': read auth state via `useAuth()`, point every sign-in/register CTA at `LOGIN_PATH` from `@/const`, do not hand-construct OAuth URLs."
9. "Install any additional packages your pages require that aren't already in the project."
10. "Export each page as a default React component."
11. "Reference generated media via `/<filename>` as specified in your page design files (e.g. `<img src="/hero-bg.png" />`, `<video src="/hero-loop.mp4" />`). The Scaffold agent has already generated and committed them."
12. "`cd $HOME/app-<branch> && git add -A && git commit -m '<scope>: implement'`"
13. "After committing, return immediately. No need to run the dev server, open a browser, take screenshots, or verify your work. The main agent handles building and deployment."

### Phase 7: Merge, Build & Create Version (Main Agent)

1. **Merge all branches** in a final-build worktree:
   ```bash
   cd /mnt/agents/output/app && git branch final-build
   # NODE_MODULES_SRC: backend template for full-stack (Hono/tRPC/Drizzle), webapp template for frontend-only.
   # ENV_SRC brings in .env (gitignored — needed for the server-side build); it's a no-op for frontend-only.
   ENV_SRC=/mnt/agents/output/app/.env \
     NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
     bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh final-build $HOME/app-final-build
   cd $HOME/app-final-build
   git merge <group1> <group2> ... --no-edit
   ```
   (Frontend-only: use `NODE_MODULES_SRC=/app/.agents/skills/webapp-building-swarm/scripts/template/node_modules` and drop `ENV_SRC`.)
   If octopus merge fails (conflicts), merge branches one at a time: `git merge <group1> --no-edit`, resolve, then `git merge <group2> --no-edit`, etc.

2. **Wire routes** in `src/App.tsx`: import page components, add `<Route>` entries inside `<BrowserRouter>` / `<Routes>`. **Check the `Layout` contract:** if the scaffold's `Layout` renders `<Outlet/>`, wire pages as nested `<Route>`s under `<Route element={<Layout/>}>` — do NOT pass `<Routes>` as `<Layout>`'s children (it silently renders blank). If `Layout` renders `{children}`, wrap `<Layout><Routes>…</Routes></Layout>`. See react-dev.md “Layout + routing contract.”

3. **Contract checks** (run before building):
   ```bash
   cd $HOME/app-final-build
   grep -nw "fixed" src/components/Navbar.tsx   # if it matches, Layout's content slot must carry the matching top offset (react-dev.md "Navbar positioning contract")
   ```
   Full-stack auth additionally:
   ```bash
   grep -rn "oauth/authorize" src/ | grep -v "src/pages/Login.tsx"   # expect: empty
   grep -n 'scope' src/pages/Login.tsx                               # expect: scope is "profile"
   grep -n "useAuth" src/components/Navbar.tsx                       # expect: a match (nav is auth-aware)
   ```
   If a check fails, fix in the final-build worktree: restore graft-owned files from the backend branch (`git checkout backend -- <file>`), point sign-in CTAs at `LOGIN_PATH` from `@/const`, apply the Phase 5 Navbar wiring, or add the missing Layout offset.

4. **Build** (correctness gate — catch type/build errors):
   ```bash
   cd $HOME/app-final-build && npm run build 2>&1
   ```
   If build fails: fix, rebuild (up to 3 retries).

5. **Commit the final source**:
   ```bash
   cd $HOME/app-final-build && git add -A && (git diff --cached --quiet || git commit -m 'final: wire routes')
   ```
   **Do NOT copy `dist/` anywhere.** `mshtools-website_version_manager` (`build_version`) records the committed source and the platform builds it (full-stack apps are built **server-side** from the project dir — that's why `node_modules` + `.env` must be present in the build worktree).

6. **Create a version** of the committed app via `mshtools-website_version_manager`:
   - `action: "build_version"`
   - `type`: `"dynamic"` for full-stack (backend graft present), `"static"` for frontend-only (after `npm run build`). Full-stack apps require `dynamic` — `static` serves the frontend only, without the server (tRPC, OAuth callback, DB).
   - `project_dir`: the final-build worktree (`$HOME/app-final-build`)
   - `message`: concise summary (shown as the version card title)

   Follow the tool's own schema for anything not listed here. Present the resulting URL to the user.

7. **Merge the delivery branch into master** — the tool commits the version on the worktree's branch, and master must contain every delivered version because all later work forks from it (see "Iterating After Delivery"):
   ```bash
   cd /mnt/agents/output/app && git merge final-build --no-edit
   ```

8. **STOP.** No verification after creating the version.

---

## Mode B — Webapp as Side Task (Single Agent)

1. **Main agent**: Read `webapp-building-swarm/SKILL.md`. Run `init-webapp.sh` with `REMOTE_PATH`:
   ```bash
   PROJECT_PATH=$HOME/init REMOTE_PATH=/mnt/agents/output/app bash /app/.agents/skills/webapp-building-swarm/scripts/init-webapp.sh "<website-title>"
   ```
   Then create a work branch:
   ```bash
   cd /mnt/agents/output/app && git branch work
   ```
2. **Single subagent**: Its prompt MUST include:
   - "Read `/app/.agents/skills/vibecoding-webapp-swarm/design-guide.md` for design inspiration and `/app/.agents/skills/vibecoding-webapp-swarm/react-dev.md` for implementation reference."
   - "Run `NODE_MODULES_SRC=/app/.agents/skills/webapp-building-swarm/scripts/template/node_modules bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh work $HOME/app-work`"
   - Tech stack versions: Node.js 20, Tailwind CSS v3.4.19, Vite v7.2.4.
   - The original user request.
   - "Write a single `/mnt/agents/output/design/design.md` (no per-page files needed — one comprehensive document). Then implement the entire site. Commit."
3. **Main agent**: Merge, build (correctness gate), create version:
   ```bash
   cd /mnt/agents/output/app && git merge work --no-edit && git branch final
   NODE_MODULES_SRC=/app/.agents/skills/webapp-building-swarm/scripts/template/node_modules \
     bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh final $HOME/app-final
   cd $HOME/app-final && npm run build 2>&1
   ```
   Do NOT copy `dist/`. Create a version of the committed app via `mshtools-website_version_manager` (`action: "build_version"`, `type: "static"`, `project_dir: $HOME/app-final`, `message`: concise title), then merge the delivery branch back: `cd /mnt/agents/output/app && git merge final --no-edit`. **No verification after.** Later fixes and rollbacks follow "Iterating After Delivery".

> Mode B is frontend-only by design (simple side deliverables). If a side-task site genuinely needs a real backend, use Mode A and its Phase 5 backend graft.

---

## Iterating After Delivery (Fixes & Rollback)

`master` on the shared repo is the only durable lineage; branches and worktrees are per-operation and disposable. Every post-delivery operation — a user-requested fix, a rollback — has the same shape: **fork a fresh branch from master, work in a fresh worktree, call the version tool there, merge the branch back into master.** Do not reuse an earlier operation's worktree or branch: a reused worktree is stale relative to master once anything else merged (delivering from it silently drops later work), it can fold leftover debris into the version tool's commits, and one branch supports exactly one worktree.

The version tool is git-native: `build_version` commits the state of `project_dir` (the version ID is that commit's short hash); `rollback` restores the tree from a version commit and commits the restored state (roll forward, no history rewrite). Either way the tool's commit lands on the branch checked out in `project_dir` — the merge back is what keeps master equal to the delivered version. Worktrees share the shared repo's object store, so any version ID resolves in any fresh worktree.

### Fix iteration

```bash
cd /mnt/agents/output/app && git branch fix-<n>
# Same NODE_MODULES_SRC as the Phase 7 final-build worktree (the staged .env is auto-copied):
NODE_MODULES_SRC=... bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh fix-<n> $HOME/app-fix-<n>
cd $HOME/app-fix-<n>
# ... edit ...
git add -A && git commit -m 'fix: <summary>'
```

Re-run Phase 7's contract checks and build (steps 3-4) in this worktree, call `build_version` with `project_dir: $HOME/app-fix-<n>`, then merge:

```bash
cd /mnt/agents/output/app && git merge fix-<n> --no-edit
```

### Rollback

When the user asks to restore a previous version, use `action: "rollback"` with the `version_id` from the target version card:

```bash
cd /mnt/agents/output/app && git branch rollback-<version-id>
# Same NODE_MODULES_SRC as the Phase 7 final-build worktree (the staged .env is auto-copied):
NODE_MODULES_SRC=... bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh rollback-<version-id> $HOME/app-rollback-<version-id>
# mshtools-website_version_manager: action="rollback", version_id="<id>", project_dir="$HOME/app-rollback-<version-id>"
# (the tool itself commits the restored state on this branch — no manual add/commit, no rebuild)
cd /mnt/agents/output/app && git merge rollback-<version-id> --no-edit
```

- Like a `build_version` target, the worktree must be delivery-capable (full-stack apps are built server-side from `project_dir`, so `node_modules` and `.env` must be present) — the coordination repo carries no `node_modules`, so never point the tool at `/mnt/agents/output/app`.
- This is the same delivery-capable build worktree shape used for a fix or a Phase 7 final build — one consistent pattern for every operation that calls the version tool, so a follow-up forward fix just continues here.
- Use the tool rather than raw `git restore`/`revert` — the rollback call is also the platform's record of which version is current.

---

## Actor Reference

| Action | Actor |
|--------|-------|
| Read vibecoding-webapp-swarm SKILL.md | Main agent |
| Run init-webapp.sh | Main agent |
| Research (browse, search) | Main agent |
| Create Pro_Designer subagent | Main agent |
| Read design-guide.md, write design.md + per-page designs + asset manifest | Pro_Designer subagent |
| Read design.md | Main agent |
| Decide build type (frontend vs full-stack) | Main agent |
| Decide grouping, create branches | Main agent |
| Read react-dev.md | All implementation subagents |
| Generate & commit media assets from design.md asset manifest | Scaffold subagent |
| Implement landing page + shared infra | Scaffold subagent |
| Merge scaffold | Main agent |
| Backend graft (full-stack only) + merge backend branch | Main agent |
| Implement pages/features (consume tRPC for full-stack) | Parallel subagents |
| Merge all branches | Main agent |
| Wire routes in App.tsx | Main agent |
| Build + create version (via `mshtools-website_version_manager`) + merge into master | Main agent |
| Post-delivery iterations — fix / rollback (fresh branch off master → worktree → version tool → merge) | Main agent |

## File Layout

```
/mnt/agents/output/
├── design/                       # Design documents
│   ├── design.md                 # Global design (fonts, colors, spacing, style)
│   ├── home.md                   # Landing page design
│   ├── about.md                  # Per-page design (named by topic)
│   └── ...
├── info.md                       # Research findings (if applicable)
├── app/                          # Shared coordination git repo
│   ├── .git/
│   ├── public/
│   │   └── *.png/jpg/mp4/...     # Generated & committed by Scaffold subagent
│   ├── src/
│   ├── api/ db/ contracts/       # Full-stack only — grafted by backend-building-swarm
│   ├── .backend-features.json    # Full-stack only — installed-features manifest
│   └── .env                      # Full-stack only — staged here (gitignored) for build worktrees
│   # NOTE: no dist/ here — the platform builds from the committed version
│
$HOME/app-<branch>/               # Local worktree (unique per subagent)
├── public/
│   └── *.png/jpg/mp4/...         # Available to all agents; reference as /<file>
├── src/
├── api/ db/ contracts/           # Full-stack only
├── node_modules/                 # gitignored — copied in by setup-local.sh
├── .env                          # Full-stack only — gitignored; copied via ENV_SRC
├── dist/                         # built locally as a correctness gate (not shipped)
└── ...
```
