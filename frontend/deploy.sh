#!/usr/bin/env bash
# Deploy Astro build to the Frappe site.
#
# Usage:
#   ./deploy.sh                  # build + copy to peaceleagueafrica.localhost (default)
#   ./deploy.sh peaceleagueafrica.org  # ditto, but advertise .org in sitemap/canonical
#   ./deploy.sh --prod           # additionally push mirror nginx configs into
#                                # /etc/nginx/conf.d and reload nginx (needs sudo)
#
# Both copies feed nginx:
#   - sites/<site>/public/       → try_files serves /, /about, /donate, ... directly
#   - apps/<app>/<app>/public/astro_pages/
#                                → bench build-assets links it into sites/assets/
#                                  for /assets/peace_league_website/astro_pages/* paths
set -euo pipefail

# Resolve BENCH_DIR from the script's own location so this works regardless of
# where the bench is mounted.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}"                                      # .../frontend/
APP_DIR="$(cd "${FRONTEND_DIR}/.." && pwd)"                      # .../peace_league_website/
BENCH_DIR="$(cd "${APP_DIR}/../.." && pwd)"                         # .../frappe-bench/ (apps/<app>/../../)
APP_NAME="$(basename "${APP_DIR}")"                              # peace_league_website

PROD=0
if [[ "${1:-}" == "--prod" ]]; then
    PROD=1
    shift
fi

SITE="${1:-peaceleagueafrica.localhost}"
SITE_PUBLIC="${BENCH_DIR}/sites/${SITE}/public"
APP_PUBLIC="${APP_DIR}/${APP_NAME}/public/astro_pages"
MIRROR_DIR="${BENCH_DIR}/scripts"

# Temp file for capturing pnpm stderr so we can decide lockfile-drift vs
# genuine install error. Always cleaned up via the EXIT trap below.
PNPM_ERR="${FRONTEND_DIR}/.pnpm-install.err"
trap 'rm -f "${PNPM_ERR}"' EXIT

echo "🏗️  Building Astro frontend in ${FRONTEND_DIR}..."
cd "${FRONTEND_DIR}"

if pnpm install --frozen-lockfile 2>"${PNPM_ERR}"; then
    echo "pnpm: lockfile in sync"
elif grep -qiE 'lockfile|outdated|frozen' "${PNPM_ERR}" 2>/dev/null; then
    # lockfile drift — explicit message from pnpm. Update lockfile and retry
    # without --frozen-lockfile so the next run starts in a known-good state.
    echo "pnpm: lockfile drift detected, falling back to plain pnpm install"
    # Capture the fallback's stderr too so its failure mode is as loud as
    # the initial run's. `set -e` would otherwise abort the deploy with
    # only bash's terse code, hiding the actual pnpm output.
    if ! pnpm install 2>"${PNPM_ERR}"; then
        echo "pnpm: fallback install also failed:" >&2
        cat "${PNPM_ERR}" >&2 || true
        exit 1
    fi
else
    # Real install failure (network, registry, permission, disk-full, …).
    # Don't swallow it — surface and exit so the deploy fails loudly.
    echo "pnpm: install error (NOT lockfile drift):" >&2
    cat "${PNPM_ERR}" >&2 || true
    exit 1
fi

pnpm run build

echo "📦 Deploying to site public dir: ${SITE_PUBLIC}"
rm -rf "${SITE_PUBLIC:?}"/*  # refuse to rm if the var is empty for safety
cp -r dist/* "${SITE_PUBLIC}/"

echo "📦 Deploying to app public dir: ${APP_PUBLIC}"
rm -rf "${APP_PUBLIC:?}"/*
cp -r dist/* "${APP_PUBLIC}/"

echo "✅ Deployed successfully to site: ${SITE}"

if [[ "${PROD}" == "1" ]]; then
    echo "🔧 Pushing nginx mirror configs into /etc/nginx/conf.d/ and reloading..."
    # These four sudo calls run passwordless via the scoped NOPASSWD rule in
    # /etc/sudoers.d/peace-league-deploy (only these four commands; anything
    # else still asks for the sudo password). Drop that file from
    # /etc/sudoers.d/ if you want to revoke this script's privilege.
    sudo cp "${MIRROR_DIR}/frappe-multitenant.conf" /etc/nginx/conf.d/
    sudo cp "${MIRROR_DIR}/peaceleagueafrica-le.conf" /etc/nginx/conf.d/
    sudo nginx -t
    sudo systemctl reload nginx
    echo "🌐 nginx reloaded. peaceleagueafrica.org serving Astro, Frappe login still at /login."
fi
