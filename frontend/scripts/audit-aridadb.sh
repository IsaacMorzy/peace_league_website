#!/usr/bin/env bash
# peace_league_website — Astro aria-labelledby integrity audit.
# Ponytail: closes the dangling-pointer failure surface that hit /index (multiple iterations)
# and /awards (one iteration). For every built HTML file, asserts that each
# aria-labelledby=\"X\" literal resolves to at least one id=\"X\" element in the same document.
#
# Usage:  bash frontend/scripts/audit-aridadb.sh
#         pnpm --dir frontend audit:aria-db   (with audit:aria-db = "bash scripts/audit-aridadb.sh")
#
# Exit 0 = clean. Exit 1 = at least one dangling aria-labelledby pointing to a non-existent id.
#
set -euo pipefail

PAGES_DIR="${PAGES_DIR:-peace_league_website/public/astro_pages}"
FAIL=0
declare -a ROWS=()

# Collect every distinct aria-labelledby=X target + every distinct id=X for a given file.
# awk + match for fast single-pass file scan.
check_file() {
  local f="$1"
  local dangle
  # Print all aria-labelledby X targets that have NO matching id X on the SAME file.
  dangle=$(awk '
    /aria-labelledby="[^"]+"/ {
      # extract first token of aria-labelledby attrs (gsub comma -> space, then first field)
      line = $0
      n = split(line, arr, /aria-labelledby="/)
      for (i=2; i<=n; i++) {
        # arr[i] starts after the opening quote; take up to next quote
        k = index(arr[i], "\"")
        if (k>1) print substr(arr[i], 1, k-1)
      }
    }
    /id="[^"]+"/ {
      line = $0
      n = split(line, arr, /id="/)
      for (i=2; i<=n; i++) {
        k = index(arr[i], "\"")
        if (k>1) print "+" substr(arr[i], 1, k-1)
      }
    }
  ' "$f" | awk '
    BEGIN{FS=OFS="\n"}
    { if (substr($0,1,1)=="+") ids[substr($0,2)]=1; else targets[$0]=1 }
    END{
      for (t in targets) if (!(t in ids)) print t
    }
  ')
  if [ -n "$dangle" ]; then
    FAIL=1
    ROWS+=("$(printf '%-60s %s' "${f#$PAGES_DIR/}" "$(echo "$dangle" | tr '\n' ' ')")")
  else
    ROWS+=("$(printf '%-60s \xc2\x9c3✓' "${f#$PAGES_DIR/}")")
  fi
}

# Walk every built html file. Skip utility shells (already excluded by sweep convention).
while IFS= read -r f; do
  check_file "$f"
done < <(find "$PAGES_DIR" -type f -name '*.html' \
  ! -name '404.html' \
  ! -name 'privacy.html' \
  ! -name 'terms.html' \
  ! -name 'sitemap*.xml' \
  | sort)

# Show only failing rows for brevity.
DANGLES=()
for row in "${ROWS[@]}"; do
  if [[ "$row" != *✓* ]]; then DANGLES+=("$row"); fi
done

if [ "$FAIL" -eq 0 ]; then
  echo ""
  echo "✓ audit clean - every aria-labelledby points to a real id"
  exit 0
else
  echo ""
  echo "✗ audit dirty - dangling aria-labelledby:" >&2
  for r in "${DANGLES[@]}"; do echo "  $r" >&2; done
  exit 1
fi
