#!/usr/bin/env bash
# Peace League Astro -> Frappe multitenancy deploy.
# Default target = sites/peaceleagueafrica.localhost/public (crowd:crowd 0775).
# No sudo needed for the copy step. Pass --reload to also sudo-and-reload nginx.
set -euo pipefail

DIST="$(cd "$(dirname "$0")" && pwd)/peace_league_website/public/astro_pages"
SITES_ROOT="/home/crowd/Documents/backend/frappe-bench/sites"
DEFAULT_TARGET="${SITES_ROOT}/peaceleagueafrica.localhost/public"

TARGET="$DEFAULT_TARGET"
DO_BUILD=1
DO_RELOAD=0
DO_HEALTH=1
DRY_RUN=0
DO_CLEAN=0  # --clean: rm -rf _astro/ before copy

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="$2"; shift 2;;
    --no-build) DO_BUILD=0; shift;;
    --no-healthcheck) DO_HEALTH=0; shift;;
    --reload) DO_RELOAD=1; shift;;
    --clean) DO_CLEAN=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    -h|--help) sed -n '4,12p' "$0"; exit 0;;
    *) echo "unknown flag: $1" >&2; exit 2;;
  esac
done

run() { printf '+'; for w in "$@"; do printf ' %q' "$w"; done; printf '\n'; [ "$DRY_RUN" = 1 ] || "$@"; }

echo "[1] build"
[ "$DO_BUILD" = 1 ] && run bash -c "cd \"$(dirname "$0")/frontend\" && pnpm build"

echo "[2] validate dist"
test -f "$DIST/index.html" || { echo "ERROR: $DIST/index.html missing"; exit 1; }

echo "[3] target"
test -d "$TARGET" || { echo "ERROR: $TARGET not a directory"; exit 1; }
[ -w "$TARGET" ] || { echo "ERROR: $TARGET not writable by $(whoami)"; exit 1; }
[ "$(realpath "$TARGET")" = "/" ] && { echo "ERROR: refusing root target"; exit 1; }

echo "[3.5] clean _astro/"
[ "$DO_CLEAN" = 1 ] && run rm -rf "$TARGET/_astro" || echo "  (skipped; --clean not set)"

echo "[4] copy to $TARGET"
run cp -R "$DIST"/. "$TARGET"/

echo "[5] nginx reload"
[ "$DO_RELOAD" = 1 ] && run sudo bash -c 'nginx -t && systemctl reload nginx'

echo "[6] healthcheck"
if [ "$DO_HEALTH" = 1 ]; then
  if ! curl -sI --resolve peaceleagueafrica.com:443:161.97.86.175 https://peaceleagueafrica.com/ | head -6; then
    echo "(healthcheck warning: curl non-zero, but build+copy succeeded)"
  fi
else
  echo "(skipped)"
fi
echo "[done]"
