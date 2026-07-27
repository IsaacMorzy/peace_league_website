#!/usr/bin/env bash
# peace_league_website — Astro closure audit.
# Ponytail: closes the broken-file failure surface that hit /gallery (05838d7)
# and /events/[slug] (949d7cf). Re-runnable; exit 0 = clean, exit 1 = at least one gap.
#
# Usage:  bash frontend/scripts/audit-astro-closures.sh
#         pnpm --dir frontend audit:astro-closures
#
set -euo pipefail

PAGES_DIR="${PAGES_DIR:-frontend/src/pages}"
SKIP_REGEX='/(404|privacy|terms|sitemap)\.astro$'
FAIL=0
declare -a ROWS=()

while IFS= read -r f; do
  LINES=$(wc -l < "$f")
  HAS_MAIN_OPEN=$(grep -c '<main' "$f" || true)
  HAS_MAIN_END=$(grep -c '</main>' "$f" || true)
  HAS_LAYOUT_END=$(grep -c '</Layout>' "$f" || true)
  HAS_FOOTER=$(grep -c '<Footer' "$f" || true)
  HAS_LAYOUT_USED=$(grep -cE '<Layout[> ]' "$f" || true)

  STATUS="OK"
  if [ "$HAS_MAIN_END" = "0" ] && [ "$HAS_MAIN_OPEN" -gt "0" ]; then
    STATUS="MISSING </main>"
    FAIL=1
  fi
  if [ "$HAS_LAYOUT_END" = "0" ] && [ "$HAS_LAYOUT_USED" -gt "0" ]; then
    STATUS="MISSING </Layout>"
    FAIL=1
  fi
  ROWS+=("$(printf '%-50s %6d %6d %6d %6d %6d  %s' "$f" "$LINES" "$HAS_MAIN_OPEN" "$HAS_MAIN_END" "$HAS_LAYOUT_END" "$HAS_FOOTER" "$STATUS")")
done < <(find "$PAGES_DIR" -name '*.astro' -type f | grep -v -E "$SKIP_REGEX" | sort)

printf "%-50s %6s %6s %6s %6s %6s  %s\n" "PATH" "lines" "openM" "endM" "endL" "Footr" "STATUS"
for r in "${ROWS[@]}"; do
  printf "%s\n" "$r"
done

if [ $FAIL -eq 0 ]; then
  echo ""
  echo "  ✓ all content pages closed properly"
  exit 0
else
  echo ""
  echo "  ✗ at least one page has a missing closing tag; fix before commit"
  exit 1
fi
