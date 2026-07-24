#!/usr/bin/env bash
# Bootstrap the peace-league-deploy sudoers NOPASSWD rule.
#
# Per docs/plan-substrate/STAGE-4-GATE.md and STANDING-ORDERS.md,
# this file is required for `frontend/deploy.sh --prod` to push nginx
# mirror configs and reload nginx without prompting for a password.
#
# Run manually:
#   sudo bash scripts/install-deploy-sudoers.sh
#
# Verifies mode 0440 root:root allowlist of four commands:
#   - cp frappe-multitenant.conf /etc/nginx/conf.d/
#   - cp peaceleagueafrica-le.conf /etc/nginx/conf.d/
#   - nginx -t
#   - systemctl reload nginx
#
# bootstraps stage 2 of #3 (peace-league-deploy agent init).

set -euo pipefail

RULE_FILE=/etc/sudoers.d/peace-league-deploy

# Refuse to run unless invoked under sudo. Standing Order #2: never embed
# plaintext sudo passwords in any script. EUID probe is stricter than
# `sudo -n true` because it succeeds only when run by the post-escalation shell.
if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "Re-run with 'sudo bash $0'" >&2
    exit 1
fi

# Cover both common systemd paths (older Debian / containers put it in /bin).
SYSTEMCTL_RULE=""
for path in /bin/systemctl /usr/bin/systemctl; do
    if [[ -x "${path}" ]]; then
        SYSTEMCTL_RULE+="%sudo ALL=(root) NOPASSWD: ${path} reload nginx
"
    fi
done

SUDO_CONTENT="%sudo ALL=(root) NOPASSWD: /usr/bin/cp /home/crowd/Documents/backend/frappe-bench/scripts/frappe-multitenant.conf /etc/nginx/conf.d/
%sudo ALL=(root) NOPASSWD: /usr/bin/cp /home/crowd/Documents/backend/frappe-bench/scripts/peaceleagueafrica-le.conf /etc/nginx/conf.d/
%sudo ALL=(root) NOPASSWD: /usr/sbin/nginx -t
${SYSTEMCTL_RULE}"

echo "${SUDO_CONTENT}" | sudo tee "${RULE_FILE}" >/dev/null
sudo chmod 0440 "${RULE_FILE}"
sudo chown root:root "${RULE_FILE}"
sudo visudo -c -f "${RULE_FILE}"

echo "Installed ${RULE_FILE}"
stat -c '%a %U:%G' "${RULE_FILE}"
