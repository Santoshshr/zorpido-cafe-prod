#!/usr/bin/env bash
# Safe merge/rebase script
# Usage: ./scripts/git-safe-merge.sh [branch]
# - Stashes uncommitted changes (if any)
# - Fetches origin
# - Rebases current branch onto origin/main
# - If conflicts occur, stops and explains resolution steps
# - Pops stash (if any) and pushes branch to origin

set -euo pipefail

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO_ROOT"

TARGET_BRANCH=${1:-}

# detect current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ -n "$TARGET_BRANCH" ]; then
  git checkout "$TARGET_BRANCH"
  BRANCH="$TARGET_BRANCH"
else
  BRANCH="$CURRENT_BRANCH"
fi

echo "Working on branch: $BRANCH"

# Ensure remote exists
git remote | grep -q origin || { echo "Remote 'origin' not found" >&2; exit 1; }

# Stash local changes if necessary
STASHED=0
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Uncommitted changes detected — creating a stash."
  git stash push -u -m "autosave before safe-merge $(date --iso-8601=seconds)" || true
  STASHED=1
fi

echo "Fetching from origin..."
git fetch origin --prune

# Try rebase onto origin/main
echo "Rebasing $BRANCH onto origin/main..."
set +e
git rebase origin/main
REBASE_EXIT=$?
set -e

if [ $REBASE_EXIT -ne 0 ]; then
  echo "Rebase failed with conflicts. You must resolve conflicts manually."
  echo "Helpful commands:"
  echo "  git status"
  echo "  # edit conflicted files, then: git add <file>"
  echo "  git rebase --continue"
  echo "If you want to abort and return to previous state: git rebase --abort"
  if [ "$STASHED" -eq 1 ]; then
    echo "Your stash is preserved. To restore it after resolving rebase, run: git stash pop"
  fi
  exit 1
fi

echo "Rebase successful."

# Restore stash if there was one
if [ "$STASHED" -eq 1 ]; then
  echo "Popping stash..."
  git stash pop --index || echo "Warning: stash pop failed; check 'git stash list'"
fi

echo "Pushing $BRANCH to origin..."
git push origin "$BRANCH"

echo "Done. If you use GitHub Actions / Render, push will trigger deploys as configured."
