#!/usr/bin/env bash
# peace_league_website — install Playwright Chromium binary (one-time).
# Lighthouse + Playwright infra both require a Chromium binary on PATH.
# This script downloads via `pnpm exec playwright install chromium` (~150MB).
#
# Usage:
#   bash frontend/scripts/install-chromium.sh
#
# After install, Lighthouse sweep runs as:
#   pnpm --dir frontend audit:lighthouse
#
set -euo pipefail
cd "$(dirname "$0")/.."
echo "[install-chromium] running pnpm exec playwright install chromium..."
pnpm exec playwright install chromium
echo "[install-chromium] ✓ done"
