#!/usr/bin/env bash
# scripts/worktree_cleanup.sh
# Remove stale Claude Code subagent/worktree checkouts under .claude/worktrees/
# that have NO uncommitted changes, NO untracked files, and NO unpushed commits.
# Safe by default: never force-removes dirty worktrees; print-only without --apply.
#
# What this script does (in order):
#   1. Pull each worktree's commits into the main branch BEFORE removing the worktree
#      (so subagent work is not lost). Uses a file lock (.claude/worktrees/.cleanup.lock)
#      to prevent concurrent runs racing on the same worktrees.
#   2. Archive any artifacts (build outputs, eval results, tmp files matching ARCHIVE_PAT)
#      into docs/archive/<timestamp>-<wt-name>/ before removing the worktree.
#   3. Remove clean worktrees (no dirty files, no unpushed commits after pull).
#   4. Run `git worktree prune` to remove stale administrative metadata.
#
# Usage:
#   scripts/worktree_cleanup.sh            # dry-run: list what WOULD happen
#   scripts/worktree_cleanup.sh --apply    # actually remove clean worktrees + prune
#   scripts/worktree_cleanup.sh --apply --force-dirty   # also remove DIRTY (DESTRUCTIVE)
#   scripts/worktree_cleanup.sh --apply --skip-pull     # skip pull step (faster; may lose commits)
set -euo pipefail

APPLY=0
FORCE_DIRTY=0
SKIP_PULL=0
for arg in "$@"; do
  case "$arg" in
    --apply)       APPLY=1 ;;
    --force-dirty) FORCE_DIRTY=1 ;;
    --skip-pull)   SKIP_PULL=1 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *)
      echo "unknown arg: $arg" >&2
      exit 64 ;;
  esac
done

# Must be inside a git repo; resolve its root.
if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  echo "ERROR: not inside a git repository" >&2
  exit 65
fi
cd "$REPO_ROOT"

WT_DIR="$REPO_ROOT/.claude/worktrees"
if [ ! -d "$WT_DIR" ]; then
  echo "no worktree dir at $WT_DIR — nothing to do"
  exit 0
fi

# ---------------------------------------------------------------------------
# FILE LOCK: prevent concurrent cleanup runs from racing on the same worktrees.
# Uses mkdir atomicity (POSIX). Lock dir is removed in EXIT trap.
# ---------------------------------------------------------------------------
LOCK_DIR="$WT_DIR/.cleanup.lock"
LOCK_PID_FILE="$LOCK_DIR/pid"

_acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    echo $$ > "$LOCK_PID_FILE"
    return 0
  fi
  # Lock exists: check if holding process is still alive.
  if [ -f "$LOCK_PID_FILE" ]; then
    LOCK_PID="$(cat "$LOCK_PID_FILE" 2>/dev/null || echo 0)"
    if kill -0 "$LOCK_PID" 2>/dev/null; then
      echo "ERROR: cleanup lock held by PID $LOCK_PID — another run is in progress" >&2
      exit 66
    else
      echo "WARNING: stale lock (PID $LOCK_PID gone) — removing and proceeding" >&2
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR"
      echo $$ > "$LOCK_PID_FILE"
    fi
  else
    echo "ERROR: lock dir exists but no PID file — remove $LOCK_DIR manually if safe" >&2
    exit 66
  fi
}

_release_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}

trap '_release_lock' EXIT

_acquire_lock

# ---------------------------------------------------------------------------
# ARCHIVE PATTERN: files in worktrees that should be preserved before removal.
# These are non-source artifacts (eval outputs, tmp build dirs, log files).
# Adjust ARCHIVE_PAT to your project's artifact conventions.
# ---------------------------------------------------------------------------
ARCHIVE_PAT="${ARCHIVE_PAT:-evals/results/*.json evals/results/*.jsonl *.log tmp/}"
ARCHIVE_BASE="$REPO_ROOT/docs/archive"

_archive_worktree_artifacts() {
  local wt_path="$1"
  local wt_name
  wt_name="$(basename "$wt_path")"
  local ts
  ts="$(date +%Y%m%d-%H%M%S)"
  local dest="$ARCHIVE_BASE/${ts}-${wt_name}"

  local found_any=0
  for pat in $ARCHIVE_PAT; do
    # Expand glob relative to the worktree root.
    for item in "$wt_path"/$pat; do
      [ -e "$item" ] || continue
      if [ "$APPLY" = "1" ]; then
        mkdir -p "$dest"
        cp -r "$item" "$dest/" 2>/dev/null && found_any=1 || true
      else
        echo "  WOULD ARCHIVE: $item -> $dest/"
        found_any=1
      fi
    done
  done

  if [ "$found_any" = "1" ] && [ "$APPLY" = "1" ]; then
    echo "  ARCHIVED artifacts to $dest"
  fi
}

# ---------------------------------------------------------------------------
# PULL SUBAGENT COMMITS: merge or fast-forward each worktree branch into the
# main branch so that commits created by the subagent are not lost when the
# worktree is removed.
# ---------------------------------------------------------------------------
# MAIN_BRANCH: the integration branch that subagent commits are merged into.
# Defaults to 'main'. Do NOT default to the current HEAD (which may be a feature
# branch). Override by setting MAIN_BRANCH=<branch> before running this script.
MAIN_BRANCH="${MAIN_BRANCH:-main}"

_pull_subagent_commits() {
  local wt_path="$1"
  local wt_branch
  wt_branch="$(git -C "$wt_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"

  if [ -z "$wt_branch" ] || [ "$wt_branch" = "HEAD" ]; then
    echo "  SKIP pull: detached HEAD in $wt_path"
    return 0
  fi
  if [ "$wt_branch" = "$MAIN_BRANCH" ]; then
    echo "  SKIP pull: worktree already on main branch ($MAIN_BRANCH)"
    return 0
  fi

  local ahead
  ahead="$(git rev-list --count "$MAIN_BRANCH..$wt_branch" 2>/dev/null || echo 0)"
  if [ "$ahead" = "0" ]; then
    echo "  SKIP pull: $wt_branch has no commits ahead of $MAIN_BRANCH"
    return 0
  fi

  if [ "$APPLY" = "1" ]; then
    echo "  PULL: merging $wt_branch ($ahead commits) -> $MAIN_BRANCH"
    # Fast-forward if possible, else create a merge commit.
    if git merge --ff-only "$wt_branch" 2>/dev/null; then
      echo "  PULL: fast-forward ok"
    else
      git merge --no-ff -m "chore(worktree): merge subagent branch $wt_branch" "$wt_branch"
      echo "  PULL: merge commit created"
    fi
  else
    echo "  WOULD PULL: $wt_branch ($ahead commits ahead of $MAIN_BRANCH)"
  fi
}

# ---------------------------------------------------------------------------
# MAIN LOOP: enumerate registered worktrees, evaluate, archive, pull, remove.
# ---------------------------------------------------------------------------
removed=0
kept=0

while IFS= read -r line; do
  case "$line" in
    worktree\ *) WT_PATH="${line#worktree }" ;;
    "")
      # end of one record -> evaluate WT_PATH
      [ -n "${WT_PATH:-}" ] || continue
      case "$WT_PATH" in
        "$WT_DIR"/*) : ;;            # in scope
        *) WT_PATH=""; continue ;;   # skip main checkout & out-of-tree worktrees
      esac

      # Is this worktree clean? dirty = any porcelain status line.
      if [ -n "$(git -C "$WT_PATH" status --porcelain 2>/dev/null)" ]; then
        DIRTY=1
      else
        DIRTY=0
      fi

      # Pull subagent commits BEFORE checking unpushed count (pull changes it).
      if [ "$SKIP_PULL" = "0" ]; then
        _pull_subagent_commits "$WT_PATH"
      fi

      # Unpushed commits relative to upstream (if an upstream exists).
      UNPUSHED=0
      if git -C "$WT_PATH" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' >/dev/null 2>&1; then
        if [ "$(git -C "$WT_PATH" rev-list --count '@{upstream}'..HEAD 2>/dev/null || echo 0)" != "0" ]; then
          UNPUSHED=1
        fi
      fi

      if [ "$DIRTY" = "1" ] || [ "$UNPUSHED" = "1" ]; then
        if [ "$FORCE_DIRTY" = "1" ] && [ "$APPLY" = "1" ]; then
          echo "REMOVE (forced, DIRTY): $WT_PATH"
          _archive_worktree_artifacts "$WT_PATH"
          git worktree remove --force "$WT_PATH"
          removed=$((removed+1))
        else
          echo "KEEP  (dirty/unpushed): $WT_PATH"
          kept=$((kept+1))
        fi
      else
        _archive_worktree_artifacts "$WT_PATH"
        if [ "$APPLY" = "1" ]; then
          echo "REMOVE (clean): $WT_PATH"
          git worktree remove "$WT_PATH"
          removed=$((removed+1))
        else
          echo "WOULD REMOVE (clean): $WT_PATH"
          removed=$((removed+1))
        fi
      fi
      WT_PATH=""
      ;;
  esac
done < <(git worktree list --porcelain; printf '\n')

if [ "$APPLY" = "1" ]; then
  git worktree prune
  echo "pruned stale administrative files"
fi

echo "summary: removed/would-remove=$removed kept=$kept (apply=$APPLY force_dirty=$FORCE_DIRTY skip_pull=$SKIP_PULL)"
