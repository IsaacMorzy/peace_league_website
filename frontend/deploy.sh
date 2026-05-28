#!/usr/bin/env bash
# Deploy Astro build to Frappe site's public directory
# Usage: ./deploy.sh [site]
set -euo pipefail

SITE="${1:-peaceleagueafrica.com}"
BENCH_DIR="/home/crowd/frappe-bench"
APP="peace_league_website"
FRONTEND_DIR="${BENCH_DIR}/apps/${APP}/frontend"
SITE_PUBLIC="${BENCH_DIR}/sites/${SITE}/public"
APP_PUBLIC="${BENCH_DIR}/apps/${APP}/${APP}/public/astro_pages"

echo "🏗️  Building Astro frontend..."
cd "${FRONTEND_DIR}"
npm run build

echo "📦 Deploying to site public dir: ${SITE_PUBLIC}"
rm -rf "${SITE_PUBLIC}"/*
cp -r dist/* "${SITE_PUBLIC}"/

echo "📦 Deploying to app public dir: ${APP_PUBLIC}"
rm -rf "${APP_PUBLIC}"/*
cp -r dist/* "${APP_PUBLIC}"/

echo "✅ Deployed successfully to site: ${SITE}"
echo ""
echo "ℹ️  The site is served from: ${SITE_PUBLIC}"
echo "ℹ️  Hard refresh (Cmd+Shift+R) your browser to see changes"
