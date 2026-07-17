---
name: swarm-workspace
description: >
  Foundation for swarm coding workflows: the two-tier filesystem contract (a
  shared coordination git repo + fast per-subagent git worktrees) and the
  canonical setup-local.sh that spins up a worktree. Use its setup-local.sh
  whenever a swarm subagent needs an isolated, fast local checkout of the shared
  repo to edit and build in.
---

# Swarm Workspace

Owns the per-subagent git-worktree lifecycle over a two-tier filesystem, so swarm
subagents can edit and build in parallel without colliding.

## Two-tier filesystem

| Path | Role | Rules |
|------|------|-------|
| `/mnt/agents/output/app` | **Shared coordination repo.** A plain git repo (no remote). The branch-creation / merge hub. | Do NOT build or edit code here. |
| `$HOME/app-<branch>` | **Local worktree.** Fast filesystem where a subagent edits and builds. | Each subagent uses a **unique** path. |

Key facts that follow from this layout:

- **No remote, no push.** All worktrees share the shared repo's `.git` object
  store, so a commit on any branch is immediately visible to the main agent — it
  just `git merge <branch>` from inside the shared repo. There is no `git push`.
- **`node_modules`, `dist`, and `.env` are gitignored.** They never sync via
  git, so `git worktree add` does NOT carry them into a new worktree. Each
  worktree gets its own copy — that is why `setup-local.sh` copies
  `node_modules` (and optionally `.env`) in.
- **Never run `git worktree prune`.** Every agent's worktree metadata lives in
  the shared repo's `.git/worktrees/` directory; pruning destroys peers'
  worktrees.
- Each parallel subagent MUST pass a **unique** `$HOME/app-<branch>` path — a
  collision corrupts shared worktree metadata.

## `setup-local.sh` — per-subagent worktree setup

```bash
[REPO_PATH=<shared-repo>] [NODE_MODULES_SRC=<prebuilt-node_modules>] [ENV_SRC=<.env-file>] \
  bash /app/.agents/skills/swarm-workspace/scripts/setup-local.sh <branch> <local-path>
```

| Var | Meaning | Default |
|-----|---------|---------|
| `REPO_PATH` | shared coordination repo | `/mnt/agents/output/app` |
| `NODE_MODULES_SRC` | a prebuilt `node_modules` dir copied into the worktree for a fast start | unset → rely on `npm install` |
| `ENV_SRC` | a `.env` file copied into the worktree | unset → `$REPO_PATH/.env` (the graft's staged `.env`), so backend/db/build worktrees auto-inherit `DATABASE_URL`; no-op when that file is absent (frontend-only) |

Pass `NODE_MODULES_SRC` pointing at the prebuilt `node_modules` for your stack
(e.g. `…/scripts/template/node_modules`) so the worktree starts with the right
dependencies overlaid; `npm install` then reconciles anything else.

Behavior:

- Fresh: `git worktree add --force`, copy `NODE_MODULES_SRC` (+ `.env` if
  `ENV_SRC` set), then `npm install`.
- Re-entry on the same branch: reuse the worktree, skip `npm install`, still
  refresh `.env` if `ENV_SRC` is given.
- Re-entry on a different branch / stale dir: recreate cleanly.
- `--force` tolerates stale worktree entries left by dead sandboxes.

## Prerequisite

`setup-local.sh` assumes the shared coordination repo already exists at
`REPO_PATH`. Creating it (laying down the initial project and `git clone`-ing it
there) is the job of whatever workflow lays the first template — not this skill.
