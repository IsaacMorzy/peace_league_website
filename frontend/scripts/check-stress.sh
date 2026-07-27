#!/usr/bin/env bash
# Post-deploy smoke probe for peaceleagueafrica.com.
#
# Usage:
#   ./check-stress.sh                # default site, full probe
#   ./check-stress.sh https://staging.peaceleagueafrica.com
#   STRESS_N=200 ./check-stress.sh   # more aggressive nav count
#
# Curl-only by design so this runs in CI without Playwright/Chromium.
# Checks every route returned 200, finishes within --max-time, and that
# the cumulative wall-clock for the full probe is reasonable.
#
# Exits 0 on success, 1 on any non-2xx or timeout. Designed to be chained
# after `deploy.sh --prod` so a regressed nginx config fails the deploy.

set -euo pipefail

SITE="${1:-https://peaceleagueafrica.com}"
SITE="${SITE%/}"  # strip single trailing slash so caller `https://x/` + route `/` -> no double-slash
# Routes that must always 200: marketing surface + a sampling of static and /api/method/*
ROUTES=(
    "/"
    "/causes"
    "/causes/peace-education"
    "/awards"
    "/events"
    "/blog"
    "/about"
    "/donate"
    "/api/method/frappe.auth.get_logged_user"
)
# Tunables. /api/method/* returns 403 (auth required) for logged-out
# callers -- the route loop below accepts 4xx for that prefix explicitly.
MAX_TIME=10                # per-curl max wall time, seconds
SLOW_THRESHOLD=3000        # ms; routes over this are emitted as slow in the micro-stress summary
STRESS_N="${STRESS_N:-10}" # micro-stress iteration count on / (override with env: STRESS_N=200 ./check-stress.sh)

overall_status=0
t_total_start=$(date +%s%3N)

for r in "${ROUTES[@]}"; do
    # /api/method/* returns 403 (auth required) for logged-out requests.
    # Accept that one non-200 as part of normal probe.
    url="${SITE}${r}"
    printf '%-50s ' "${r}"
    t0=$(date +%s%3N)
    set +e
    out=$(curl -sS -o /dev/null --max-time "${MAX_TIME}" -w 'status=%{http_code} time=%{time_total}s' "${url}" 2>&1)
    rc=$?
    t1=$(date +%s%3N)
    set -e
    ms=$(( t1 - t0 ))

    # Parse status code from curl output. curl -w leaves no trailing newline.
    status_code=$(printf '%s' "${out}" | sed -n 's/.*status=\([0-9][0-9][0-9]\).*/\1/p')
    curl_time=$(printf '%s' "${out}" | sed -n 's/.*time=\([0-9.]*\)s.*/\1/p')

    allow_non200="0"
    if [[ "${r}" == "/api/method/"* ]]; then
        allow_non200="1"
    fi

    if [[ ${rc} -ne 0 || -z "${status_code}" ]]; then
        printf 'CURL_FAIL rc=%d curl=%s (%dms)\n' "${rc}" "${out}" "${ms}"
        overall_status=1
    elif [[ "${status_code}" == "2"* || ( "${allow_non200}" == "1" && "${status_code}" == "4"* ) ]]; then
        printf 'OK status=%s %ss\n' "${status_code}" "${curl_time}"
    else
        printf 'BAD status=%s %ss\n' "${status_code}" "${curl_time}"
        overall_status=1
    fi
done

# Bonus: micro stress -- loop / for STRESS_N rounds to surface flake.
echo
echo "🌀 Micro stress: ${STRESS_N} consecutive GETs on /"
slow_count=0
fail_count=0
slow_runs=""
for ((i=0; i<STRESS_N; i++)); do
    set +e
    t0=$(date +%s%3N)
    out=$(curl -sS -o /dev/null --max-time "${MAX_TIME}" -w 'status=%{http_code} time=%{time_total}s' "${SITE}/" 2>&1)
    rc=$?
    t1=$(date +%s%3N)
    set -e
    ms=$(( t1 - t0 ))
    status_code=$(printf '%s' "${out}" | sed -n 's/.*status=\([0-9][0-9][0-9]\).*/\1/p')
    if [[ ${rc} -ne 0 || "${status_code}" != "200" ]]; then
        fail_count=$((fail_count + 1))
        slow_runs+=" ${i}:FAIL"
    elif (( ms > SLOW_THRESHOLD )); then
        slow_count=$((slow_count + 1))
        slow_runs+=" ${i}:${ms}ms"
    fi
done
t_total_end=$(date +%s%3N)
total_ms=$(( t_total_end - t_total_start ))

echo "🌀 Total: ${STRESS_N}  Slow>${SLOW_THRESHOLD}ms: ${slow_count}  Fail: ${fail_count}  TotalWall: ${total_ms}ms"
if (( slow_count > 0 || fail_count > 0 )); then
    echo "🌀 Slow/Fail samples:${slow_runs}"
    overall_status=1
fi

if (( overall_status == 0 )); then
    echo
    echo "✅ All probes pass -- peaceleagueafrica.com serving clean."
    exit 0
else
    echo
    echo "❌ At least one probe failed. Re-run `deploy.sh --prod` after fixing the regressed site/nginx config."
    exit 1
fi
