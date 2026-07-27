#!/usr/bin/env bash
# peace_league_website — Astro closure audit.
# Ponytail: regression-gate for the broken-file failure surface that hit /gallery
# (05838d7) and /events/[slug] (949d7cf). Re-runnable; exit 1 = at least one
# real open/close mismatch; exit 0 = all content pages closed properly.
#
# Usage:  bash frontend/scripts/audit-astro-closures.sh
#         pnpm --dir frontend audit:astro-closures
#
set -euo pipefail

PAGES_DIR="${PAGES_DIR:-frontend/src/pages}"
SKIP_REGEX='/(404|privacy|terms|sitemap)\.astro$'
FAIL=0
declare -a ROWS=()

# grep -c exits 1 on no match; "|| echo 0" lets set -e carry on AND reports truth.
count() { grep -c "$1" "$2" 2>/dev/null || echo "0"; }

while IFS= read -r f; do
  LINES=$(wc -l < "$f")
  HAS_MAIN_OPEN=$(count '<main ' "$f")
  HAS_MAIN_END=$(count '</main>' "$f")
  HAS_LAYOUT_OPEN=$(count '<Layout ' "$f")
  HAS_LAYOUT_END=$(count '</Layout>' "$f")
  HAS_FOOTER=$(count '<Footer[ \t]*/>' "$f")

  STATUS="OK"
  # Real failure: open count > 0 AND open != close. Pages that legitimately omit
  # <main>/<Layout> (e.g. dynamic client-shells fetching their own data) will show
  # 0/0 and stay OK; pages that opened but didn't close FAIL loudly.
  if [ "$HAS_MAIN_OPEN" -gt 0 ] && [ "$HAS_MAIN_OPEN" != "$HAS_MAIN_END" ]; then
    STATUS="MISMATCH </main> ($HAS_MAIN_OPEN open / $HAS_MAIN_END close)"
    FAIL=1
  fi
  if [ "$HAS_LAYOUT_OPEN" -gt 0 ] && [ "$HAS_LAYOUT_OPEN" != "$HAS_LAYOUT_END" ]; then
    STATUS="MISMATCH </Layout> ($HAS_LAYOUT_OPEN open / $HAS_LAYOUT_END close)"
    FAIL=1
  fi
  ROWS+=("$(printf '%-50s %6d %6d %6d %6d %6d %6d  %s' "$f" "$LINES" "$HAS_MAIN_OPEN" "$HAS_MAIN_END" "$HAS_LAYOUT_OPEN" "$HAS_LAYOUT_END" "$HAS_FOOTER" "$STATUS")")
done < <(find "$PAGES_DIR" -name '*.astro' -type f | grep -v -E "$SKIP_REGEX" | sort)

printf "%-50s %6s %6s %6s %6s %6s %6s  %s\n" "PATH" "lines" "opnM" "clsM" "opnL" "clsL" "Footr" "STATUS"
for r in "${ROWS[@]}"; do
  printf "%s\n" "$r"
done

if [ $FAIL -eq 0 ]; then
  echo ""
  echo "  ✓ all content pages closed properly"
  exit 0
else
  echo ""
  echo "  ✗ at least one page has mismatched closing tag; fix before commit"
  exit 1
fi
