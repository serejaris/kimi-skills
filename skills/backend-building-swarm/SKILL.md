---
name: backend-building-swarm
description: Swarm-aware backend building that grafts tRPC + Drizzle ORM + Hono onto an existing webapp-building-swarm frontend. Grafts in place on a worktree of the shared repo (created via swarm-workspace) and commits on a backend branch the main agent merges. Supports incremental features (db, auth) and fullstack-template provisioning (--template). Use when the user needs a backend, API, database, server, or authentication in a swarm setup. Requires webapp-building-swarm first.
---

# Backend Building Swarm

**Stack**: tRPC + Drizzle ORM + Hono + MySQL + OAuth 2.0

A swarm-aware backend skill that grafts onto an existing `webapp-building-swarm` project. Adds `api/`, `contracts/`, and optionally `db/` directories — but **never replaces or modifies** existing frontend files.

**Prerequisite**: An existing shared repo created by `webapp-building-swarm` at `/mnt/agents/output/app`.

## Architecture

This skill builds on the **swarm-workspace** two-tier filesystem — a shared
coordination repo (branch hub) plus per-subagent worktrees. See
`swarm-workspace/SKILL.md` for the full contract; it is not restated here.

`init.sh` grafts **in place** on `$PROJECT_PATH` and commits on whatever
branch is checked out there — it does NOT manage worktrees or merge. In the
swarm flow the **main agent** creates the `backend` worktree via
swarm-workspace's `setup-local.sh`, runs `init.sh` in it with `PROJECT_PATH`
pointed at the worktree, commits on the `backend` branch, and merges that
branch into the integration line before page branches fork — so all page
agents inherit the tRPC client and contracts. The main agent runs the graft
itself rather than dispatching a subagent because `init.sh` writes a
**gitignored** `.env` that never travels through the merge: it survives only in
the sandbox where it ran, which must be the main agent's own — the one that
later builds and stages `.env` into the other worktrees. Webapp commit history
is preserved because the `backend` branch descends from the scaffolded frontend.

## Features

Features can be installed incrementally. Base infrastructure (Hono server, tRPC, contracts) is always installed automatically on first run.

| Feature | What it provides | Dependencies |
|---------|-----------------|--------------|
| `db` | Drizzle ORM + MySQL — adds `db/`, `api/queries/connection.ts`, `drizzle.config.ts` | — |
| `auth` | Kimi OAuth + user management — adds `api/kimi/`, Login page, useAuth, AuthLayout | requires `db` (auto-included) |

Default: `init.sh "App"` with no `--features` → defaults to `auth` (= db + auth).

## Scripts

All scripts use absolute paths from `/app/.agents/skills/backend-building-swarm/scripts/`.

### `init.sh` — Backend graft (run inside the `backend` worktree)

```bash
# Point PROJECT_PATH at the backend worktree (created by setup-local.sh first):
PROJECT_PATH=$HOME/app-backend \
  bash /app/.agents/skills/backend-building-swarm/scripts/init.sh "<app-title>" [--features db,auth | --template]
```

- Grafts **in place** on `$PROJECT_PATH` and commits on the currently checked-out branch. In the swarm flow `$PROJECT_PATH` is the main-agent-owned `backend` worktree (the graft is the main agent's own job, not a subagent's — see the gitignored-`.env` reason above); the script's bare default (`/mnt/agents/output/app`) exists only for the deterministic structure test. It does NOT create worktrees or merge.
- Re-entry safe: `.backend-features.json` gates re-runs (adding `--features auth` later only installs the delta). Graft-owned auth UI (`Login.tsx`, `useAuth.ts`, `AuthLayout*`) is planted authoritatively each run, while user-extensible files (`schema.ts`, `seed.ts`, `connection.ts`, `drizzle.config.ts`) yield to any version already present.

**Two execution paths depending on which webapp template was used:**

| Mode | Webapp template | Backend work |
|------|-----------------|--------------|
| `--features db,auth` (default) | frontend-only (e.g. `0-origin`, `airlens-style`) | full graft: copy api/contracts/db, patch vite/tsconfig, auto-wire main.tsx/App.tsx, portal call, commit |
| `--template` | fullstack (ships `.backend-features.json` + pre-laid `api/`, `db/`, `contracts/`) | provision-only: read manifest, portal call, write `.env`, npm install, commit |

`--features` and `--template` are mutually exclusive. `--template` is selected automatically by the presence of `.backend-features.json` in the project — it reads the feature list from that manifest and skips all file copy/patch/wiring (the fullstack template already laid them out), doing portal provisioning + `.env` only.

### Worktree setup (run by subagents)

Use **swarm-workspace**'s `setup-local.sh`, passing this skill's prebuilt backend
`node_modules` (Hono/tRPC/Drizzle) as `NODE_MODULES_SRC`:

```bash
NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
  bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh <branch> $HOME/app-<branch>
```

- Creates a git worktree from the shared repo at `/mnt/agents/output/app`
- **Each subagent MUST use a unique local path** (`$HOME/app-<branch>`) to avoid worktree metadata collisions
- Overlays the backend `node_modules` so `npm install` is fast, then `npm install`
- Handles re-entry; **never run `git worktree prune`** — it destroys other agents' worktree entries

See `swarm-workspace/SKILL.md` for the full two-tier filesystem contract.

### `.prepare-template.sh` — Image build-time only

Builds `scripts/template/node_modules/` by `npm install`-ing the template `package.json`. Runs once at image build time, not at runtime.

## Workflows

The end-to-end sequencing is owned by **vibecoding-webapp-swarm** (the backend
graft is its Phase 4.5: run once on a `backend` branch forked from scaffold,
merged before page branches fork). This skill provides the graft itself. The
shape of a graft step:

1. `webapp-building-swarm` init + scaffold land a frontend on the shared repo
2. Create the backend worktree via swarm-workspace's `setup-local.sh` (with `NODE_MODULES_SRC` = this skill's `template/node_modules`)
3. `PROJECT_PATH=$HOME/app-backend init.sh "<title>" [--features … | --template]` — graft, provision, commit on `backend`
4. Main agent merges `backend` into the integration line; page agents then inherit the tRPC client + contracts

**Incremental features** (add capabilities over time): re-run `init.sh`
in a worktree with `--features auth` — the `.backend-features.json` manifest
gates it to install only the delta, landing a new commit on that branch.

## Quick Start

### 1. Initialize Frontend First (webapp-building-swarm)

```bash
PROJECT_PATH=$HOME/init REMOTE_PATH=/mnt/agents/output/app \
  bash /app/.agents/skills/webapp-building-swarm/scripts/init-webapp.sh "My App"
```

### 2. Graft Backend

```bash
# Create the backend worktree (swarm-workspace's setup-local.sh + this skill's node_modules), then graft into it:
NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
  bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh backend $HOME/app-backend

# Full stack with auth (default):
PROJECT_PATH=$HOME/app-backend \
  bash /app/.agents/skills/backend-building-swarm/scripts/init.sh "My App"

# Database only (no auth):
PROJECT_PATH=$HOME/app-backend \
  bash /app/.agents/skills/backend-building-swarm/scripts/init.sh "My App" --features db

# Fullstack template (skip scaffolding; provision-only — auto-detected via .backend-features.json):
PROJECT_PATH=$HOME/app-backend \
  bash /app/.agents/skills/backend-building-swarm/scripts/init.sh "My App" --template
```

Then the main agent merges the `backend` branch:
`cd /mnt/agents/output/app && git merge backend --no-edit`. Because `.env` is
gitignored, copy it to the shared repo so later worktrees can pick it up:
`cp $HOME/app-backend/.env /mnt/agents/output/app/.env`.

**What this does (base, always on first run with `--features`):**

- Copies `api/`, `contracts/` into the worktree
- Patches `vite.config.ts` in-place (adds `@contracts` alias, `envDir`, `build.outDir`)
- Adds `tsconfig.server.json` and merges `@contracts/*` path into existing tsconfigs
- Merges `package.json` (adds backend deps and scripts)
- Generates `.env` with portal credentials
- Runs `npm install`
- Commits the graft on the current branch (main agent merges it; no ff-merge here)

**Additional per feature:**

- **db**: Adds `db/` directory, `drizzle.config.ts`, database connection, `DATABASE_URL` env var, and `db/seed.ts` (scaffold for seeding — run with `npx tsx db/seed.ts`). **Do not overwrite** the generated `api/queries/connection.ts`, `drizzle.config.ts`, or `.env`. Only add your tables to `db/schema.ts`.
- **auth**: Adds `api/kimi/`, auth router, client patches (Login, useAuth, AuthLayout, TRPCProvider), auto-wires Login/NotFound routes into `App.tsx`.

### 3. Verify Auto-Wiring

On first run, `init.sh` auto-wires `TRPCProvider` into `src/main.tsx`. When `auth` feature is installed, it also adds Login/NotFound routes to `src/App.tsx`. Check the init output:

- **"Auto-wired"** — no action needed
- **"Wiring required"** — complete the listed steps manually (see [Post-Init Wiring](docs/Post-Init-Wiring.md))

If manual wiring is needed, do it in a worktree (created via swarm-workspace's `setup-local.sh`, which auto-copies the staged `.env` so `npm run db:*` has `DATABASE_URL`), edit, commit on the branch — the main agent merges it into the shared repo. (No push: worktrees share the shared repo's `.git` object store.)

### 4. Database Setup (if db or auth feature installed)

Run from a worktree, not OSS. **`npm run db:*` needs `DATABASE_URL`, which lives in
`.env`** — `setup-local.sh` auto-copies the graft's staged `.env` (`$REPO_PATH/.env`)
into every worktree, so this works without extra flags. `ENV_SRC` is shown explicitly
below for clarity (and to override the source if ever needed); omitting it falls back
to the same staged `.env`:

```bash
ENV_SRC=/mnt/agents/output/app/.env \
  NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
  bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh main $HOME/app-main
cd $HOME/app-main && npm run db:push
```

### 5. Development & Build

```bash
# Build on a final-build worktree (correctness gate — catch type/build errors)
ENV_SRC=/mnt/agents/output/app/.env \
  NODE_MODULES_SRC=/app/.agents/skills/backend-building-swarm/scripts/template/node_modules \
  bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh final-build $HOME/app-final-build
cd $HOME/app-final-build && npm run build
```

Do **not** copy `dist/` anywhere. The model records a version of the committed
source via `mshtools-website_version_manager` (`action: "build_version"`,
`type: "dynamic"` — `static` serves the frontend only, without the server), and the
platform builds the dynamic app server-side from that version's committed
source in the worktree (`project_dir`) — which is why `node_modules` and `.env`
must be present there (`ENV_SRC` above copies `.env` into the worktree). The
tool is invoked per the system prompt, not by this skill.

## Common Commands

| Command              | Description                                                | Requires |
| -------------------- | ---------------------------------------------------------- | -------- |
| `npm run dev`        | Start development server with HMR at http://localhost:3000 | base |
| `npm run build`      | Build for production (outputs to dist/)                    | base |
| `npm start`          | Start production server                                    | base |
| `npm run check`      | Type-check all TypeScript files                            | base |
| `npm run format`     | Format code with Prettier                                  | base |
| `npm run test`       | Run tests with Vitest                                      | base |
| `npm run db:push`    | Sync schema to DB during development (recommended)         | db |
| `npm run db:generate`| Generate migration SQL for production deployment           | db |
| `npm run db:migrate` | Apply pending migration files to the database              | db |

Run `npm run *` commands inside a **worktree** (`$HOME/app-<branch>`), not on the shared coordination repo. Heavy steps (`install`, `build`, `dev`) would thrash its slow FUSE mount; and even the light `db:*` commands need the worktree's `node_modules` + `.env`, which are gitignored and therefore present only in worktrees — never in the coordination repo.

## Stack Overview

### Backend (added by this skill)

- Hono + tRPC 11.x
- End-to-end type safety
- Public query procedure (base); authenticated/admin procedures (auth feature)

### Database (db feature)

- Drizzle ORM with MySQL
- Lazy `getDb()` connection
- Type-safe queries ([Guide](docs/Database.md))
- Schema migrations

### Authentication (auth feature)

- OAuth 2.0 ([Details](docs/Authentication.md))
- JWT sessions, admin role support

### Frontend (from webapp-building-swarm, untouched)

- React 19 + TypeScript + Vite (HMR)
- Tailwind CSS + shadcn/ui components
- Dark/light mode

## Common Mistakes

- **Don't run `init.sh` against `/mnt/agents/output/app` in a swarm setup** — set `PROJECT_PATH` to the `backend` worktree created by `setup-local.sh`. Grafting directly in the shared repo edits/builds in the coordination hub.
- **Don't forget to merge the `backend` branch** — `init.sh` commits the graft on the branch but does not merge. The main agent must `git merge backend` before page branches fork, or page agents won't inherit the tRPC client.
- **Don't run `npm install` / `npm run build` on `/mnt/agents/output/app`** — it's coordination only. Use a worktree.
- **Don't run `git worktree prune`** in any worktree — it destroys other agents' worktree metadata in the shared `.git/worktrees/` directory.
- **Don't hand-write TypeScript interfaces for DB entities** — use `typeof table.$inferSelect` from `db/schema.ts`. Hand-written `createdAt: string` will conflict with the actual `Date` objects delivered by superjson.
- **Don't write raw SQL** — always use Drizzle's type-safe query API (`getDb().query.*`, `getDb().select()`, `getDb().insert()`).
- **Don't modify `api/lib/` or `api/kimi/`** — framework internals. Build on top of them.
- **Don't modify or re-create the auth client files** — `src/pages/Login.tsx`, `src/hooks/useAuth.ts`, `src/const.ts`, `src/components/AuthLayout*.tsx` are installed by the auth graft and consumed as-is. The template `Login.tsx` is the only OAuth entry point; sign-in CTAs navigate to `LOGIN_PATH` from `@/const` rather than constructing OAuth URLs.
- **Don't build a Register page** — OAuth auto-provisions users on first login; there is no registration flow. Register/sign-up CTAs link to `LOGIN_PATH`.
- **Don't import `api/` from frontend code** — use `@contracts/` for types/constants that cross the boundary. The only exception is the type import in `src/providers/trpc.tsx`.
- **Don't use `api` as the tRPC client name** — it's `trpc` (imported from `@/providers/trpc`).
- **Don't skip Zod validation** on tRPC inputs — always use `.input(z.object({...}))` for mutations and parameterized queries.
- **Don't use `serial()` for foreign key columns** — `serial()` is `bigint unsigned auto_increment`, MySQL only allows one auto-increment column per table. FK columns must use `bigint("col", { mode: "number", unsigned: true })`.
- **Don't use `int()` for foreign keys referencing `serial()` PKs** — type mismatch.
- **NEVER drop tables to fix a failed migration** — the database may contain user data. Fix `schema.ts` and run `npm run db:push` to sync. See Troubleshooting.
- **NEVER use `db:push --force`** — auto-accepts destructive changes.
- **NEVER modify `.env` values** — generated by `init.sh` with valid credentials. Do not overwrite or placeholder-ify.
- **NEVER overwrite init-generated infrastructure files** — `api/queries/connection.ts`, `api/middleware.ts`, `api/lib/`, `drizzle.config.ts`, `src/providers/trpc.tsx`, `.env`. Build on top.
- **Don't change the default port (3000)**.

## AI Agent Instructions

**Required reading before implementing features** — read these docs (under `docs/`):
- **db feature**: [Database.md](docs/Database.md), [tRPC.md](docs/tRPC.md)
- **auth feature**: [Authentication.md](docs/Authentication.md), [tRPC.md](docs/tRPC.md)
- **All features**: [Development-Guide.md](docs/Development-Guide.md), [Project-Structure.md](docs/Project-Structure.md)

When building features on this stack:

1. **Read existing frontend code** in `src/` to understand the app structure (from a worktree)
2. **Design tRPC routers** that match the frontend's data needs
3. **Add DB tables** in `db/schema.ts`, then run `npm run db:push` from the worktree
4. **Create new routers** in `api/` and register them in `api/router.ts`
5. **Use type-safe queries** via Drizzle ORM — never raw SQL
6. **Frontend components** go in `src/` using the existing `@/` alias

**When to use which features:**
- Database only: `--features db`
- User login: `--features auth` (includes db automatically)
- Default (no flag): `auth`
- Fullstack template: `--template` (features come from the template's `.backend-features.json`)

### Key Paths

| Path | What to do |
|------|-----------|
| `src/main.tsx` | TRPCProvider auto-wired here (verify after init) |
| `src/App.tsx` | Login/NotFound routes auto-wired here (auth feature only) |
| `src/pages/` | Route-level page components |
| `src/sections/` | Visual sections within a page (from webapp-building templates) |
| `src/components/` | New UI components |
| `api/router.ts` | Register new tRPC routers |
| `api/queries/` | Add query functions for new tables (db feature) |
| `db/schema.ts` | Add new database tables (db feature) |
| `contracts/` | Shared types/constants (frontend + backend) |
| `api/lib/` | Framework internals — don't modify |
| `api/kimi/` | Kimi SDK modules — don't modify (auth feature) |

Full directory tree: [Project Structure](docs/Project-Structure.md)

## Detailed Documentation

- [Project Structure](docs/Project-Structure.md) - Directory layout and where to put things
- [Development Guide](docs/Development-Guide.md) - Component development, API patterns, workflows
- [Authentication](docs/Authentication.md) - OAuth 2.0 implementation details
- [Database Guide](docs/Database.md) - Drizzle ORM configuration, schema design, migrations
- [tRPC Best Practices](docs/tRPC.md) - Router patterns and type safety
- [Post-Init Wiring](docs/Post-Init-Wiring.md) - Manual wiring fallback when auto-wire fails

## Routing (react-router)

This template uses **react-router** v7.

```typescript
import { useNavigate, useLocation, useParams, Link, Routes, Route, BrowserRouter } from "react-router";
```

See [tRPC Best Practices](docs/tRPC.md) and the frontend's `App.tsx` for current route definitions.

## Troubleshooting

**Port 3000 already in use** — `lsof -ti:3000 | xargs kill`.

**Database connection refused** — Check `DATABASE_URL` in `.env`. Run `npm run db:push` before `npm run dev`.

**User reports login failing** — Verify `VITE_KIMI_AUTH_URL` and `VITE_APP_ID` in `.env` match the portal app config, and that `src/pages/Login.tsx` still matches the template (the only OAuth entry point).

**`npm run db:migrate` fails** — NEVER drop tables. Fix `schema.ts`, run `npm run db:push`, delete the broken migration file and its entry in `db/migrations/meta/_journal.json`, then `npm run db:generate` for a clean baseline.

**`init.sh` errors that `$PROJECT_PATH/src` is missing** — the worktree wasn't created or points at the wrong place. Create it first with swarm-workspace's `setup-local.sh` (`NODE_MODULES_SRC=…/backend-building-swarm/scripts/template/node_modules … setup-local.sh backend $HOME/app-backend`), and pass `PROJECT_PATH=$HOME/app-backend`.

**`git merge backend` conflicts** — the `backend` branch must fork from the merged scaffold; merge it before page branches fork (Phase 4.5, before Phase 5). If it diverged, re-graft on a fresh `backend` worktree off the current integration head.

**Type errors after adding a new router** — Make sure you registered it in `api/router.ts` inside `appRouter`.
