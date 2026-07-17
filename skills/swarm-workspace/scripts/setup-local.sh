#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# swarm-workspace: robust per-subagent worktree setup for the two-tier swarm
# filesystem. This is the ONE canonical implementation — webapp-building-swarm
# and backend-building-swarm delegate to it via thin wrappers that only set
# NODE_MODULES_SRC (their skill-specific prebuilt node_modules).
#
# Usage: setup-local.sh <branch> [local-path]
#
# Env overrides (callers/wrappers set these):
#   REPO_PATH         shared coordination repo (default: /mnt/agents/output/app)
#   NODE_MODULES_SRC  dir copied in as ./node_modules for a fast start
#                     (unset/missing → skip the copy, rely on `npm install`)
#   ENV_SRC           a .env file copied into the worktree as ./.env
#                     (default: $REPO_PATH/.env — the .env the backend graft
#                     stages in the shared repo, so EVERY worktree auto-inherits
#                     it; no-op for frontend-only apps with no staged .env)
#
# Two-tier model:
#   - REPO_PATH is the SHARED git repo (coordination hub). Subagents do NOT
#     build or edit there. It has no remote; branches are merged by the main
#     agent directly (the worktrees share its .git object store).
#   - LOCAL_PATH ($HOME/app-<branch>) is a fast LOCAL worktree where a subagent
#     edits and builds. node_modules/dist/.env are gitignored, so they never
#     sync via git — each worktree gets its own copy (hence NODE_MODULES_SRC /
#     ENV_SRC).
#
# IMPORTANT: Each parallel subagent MUST use a unique local-path to avoid
# worktree metadata collisions in the shared git repo. Convention:
#   setup-local.sh <branch> $HOME/app-<branch>
#
# Handles:
#   - Fresh setup: creates worktree, copies node_modules (+ .env), npm install
#   - Re-entry, same branch: reuses worktree (skips npm install); still refreshes
#     .env if ENV_SRC is given
#   - Re-entry, different branch: removes old worktree, creates fresh
#   - Stale non-git dir at local-path: removes and creates fresh
#   - Uses --force to handle stale entries from dead sandboxes
#
# WARNING: Never run `git worktree prune` — in multi-agent setups, other
# agents' worktree entries share the same .git/worktrees/ directory. Pruning
# would destroy their metadata.
# ─────────────────────────────────────────────────────────────────────────────

REPO_PATH="${REPO_PATH:-/mnt/agents/output/app}"
BRANCH="${1:?Usage: setup-local.sh <branch> [local-path]}"
LOCAL_PATH="${2:-$HOME/app-$BRANCH}"
NODE_MODULES_SRC="${NODE_MODULES_SRC:-}"
# Default to the shared repo's staged .env (written by the backend graft) so any
# worktree — including ad-hoc backend passes that don't pass ENV_SRC — inherits
# DATABASE_URL etc. Without this, `npm run db:push` in such a worktree fails with
# "DATABASE_URL is required". copy_env() no-ops when the file is absent.
ENV_SRC="${ENV_SRC:-$REPO_PATH/.env}"

copy_env() {
    if [ -n "$ENV_SRC" ] && [ -f "$ENV_SRC" ]; then
        cp "$ENV_SRC" "$LOCAL_PATH/.env"
        echo "Copied .env from $ENV_SRC"
    fi
}

cd "$REPO_PATH"

# ─────────────────────────────────────────────────────────────────────────────
# Handle existing directory at LOCAL_PATH
# ─────────────────────────────────────────────────────────────────────────────
if [ -d "$LOCAL_PATH" ]; then
    # A worktree's .git is a FILE (gitdir pointer), not a dir — test with -e.
    if [ -e "$LOCAL_PATH/.git" ] || git -C "$LOCAL_PATH" rev-parse --git-dir >/dev/null 2>&1; then
        CURRENT_BRANCH=$(git -C "$LOCAL_PATH" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [ "$CURRENT_BRANCH" = "$BRANCH" ]; then
            echo "Re-entry: worktree at $LOCAL_PATH already on branch '$BRANCH'. Reusing."
            copy_env
            cd "$LOCAL_PATH"
            echo "Ready: $LOCAL_PATH (branch: $BRANCH)"
            exit 0
        else
            echo "Re-entry: worktree at $LOCAL_PATH on branch '$CURRENT_BRANCH', need '$BRANCH'. Recreating."
            git worktree remove --force "$LOCAL_PATH" 2>/dev/null || rm -rf "$LOCAL_PATH"
        fi
    else
        echo "Stale non-git directory at $LOCAL_PATH. Removing."
        rm -rf "$LOCAL_PATH"
    fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Create worktree (--force handles stale entries from dead sandboxes)
# ─────────────────────────────────────────────────────────────────────────────
git worktree add --force "$LOCAL_PATH" "$BRANCH"
cd "$LOCAL_PATH"

# ─────────────────────────────────────────────────────────────────────────────
# Install dependencies
# ─────────────────────────────────────────────────────────────────────────────
if [ -n "$NODE_MODULES_SRC" ] && [ -d "$NODE_MODULES_SRC" ]; then
    cp -r "$NODE_MODULES_SRC" ./node_modules
    echo "Overlaid node_modules from $NODE_MODULES_SRC"
fi
copy_env
npm install

echo "Ready: $LOCAL_PATH (branch: $BRANCH)"
