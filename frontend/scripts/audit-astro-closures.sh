#!/usr/bin/env bash
# peace_league_website — Astro closure audit.
# Ponytail: regression-gate for the broken-file failure surface that hit /gallery
# (05838d7) and /events/[slug] (949d7cf). Re-runnable; exit 1 = real open/close
# mismatch on a content page; exit 0 = all content pages closed properly.
#
# Counts OCCURRENCES not lines: `awk gsub` returns per-record replacement
# counts and we sum — two opens collapsed onto one line still count as two.
#
# Skip rules: utility pages (404/privacy/terms/sitemap) are silently allowed
# to have zero opens or zero closes — full-page shells we do not police. Add a
# new utility-mode file to SKIPS as a bare basename (no path, no extension).
#
# Usage:  bash frontend/scripts/audit-astro-closures.sh
#         pnpm --dir frontend audit:astro-closures
#
set -euo pipefail

PAGES_DIR="${PAGES_DIR:-frontend/src/pages}"
SKIPS=(404 privacy terms sitemap)
FAIL=0
declare -a ROWS=()

is_skipped() {
  # Exact basename equality - utility mode only.
  local base
  base="$(basename "$1")"
  for s in "${SKIPS[@]}"; do
    [ "$base" = "${s}.astro" ] && return 0
  done
  return 1
}

# count_occurrences <file> <regex> -> echoes count (0 on no match)
count_occurrences() {
  awk -v pat="$2" 'BEGIN{c=0} {c += gsub(pat, "&")} END {print c+0}' "$1"
}

while IFS= read -r f; do
  if is_skipped "$f"; then continue; fi
  OPENS_MAIN=$(count_occurrences "$f" '<main( |>)')
  CLOSES_MAIN=$(count_occurrences "$f" '</main>')
  OPENS_LAY=$(count_occurrences "$f" '<Layout( |>)')
  CLOSES_LAY=$(count_occurrences "$f" '</Layout>')
  FOOTER=$(count_occurrences "$f" '<Footer[ \t]*/>')

  STATUS='✓'
  # REAL mismatch only: opens > 0 AND opens != closes.
  if { [ "$OPENS_MAIN" -gt 0 ] && [ "$OPENS_MAIN" -ne "$CLOSES_MAIN" ]; } \
  || { [ "$OPENS_LAY"  -gt 0 ] && [ "$OPENS_LAY"  -ne "$CLOSES_LAY" ];  }; then
    STATUS='✗'
    FAIL=1
  fi
  ROWS+=("$(printf '%-44s %2s/%2s %2s/%2s %2s %s' "${f#$PAGES_DIR/}" "$OPENS_MAIN" "$CLOSES_MAIN" "$OPENS_LAY" "$CLOSES_LAY" "$FOOTER" "$STATUS")")
done < <(find "$PAGES_DIR" -type f -name '*.astro' | sort)

printf '%-44s %5s %5s %5s %2s %s\n' "PATH" "<m" "</m" "<L>" "</L" "Ft" "OK?"
printf '%-44s %5s %5s %5s %2s %s\n' "----" "---" "---" "---" "---" "--"
for row in "${ROWS[@]}"; do printf '%s\n' "$row"; done

if [ "$FAIL" -eq 0 ]; then
  echo
  echo "✓ audit clean - all content pages closed properly"
  exit 0
else
  echo
  echo "✗ audit dirty - at least one real open/close mismatch" >&2
  exit 1
fi
