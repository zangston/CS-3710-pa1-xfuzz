#!/bin/bash

set -euo pipefail

SECRETS_DIR="$(dirname $0)"

remove_secret() {
    if docker secret inspect "$1" >/dev/null 2>&1; then
        docker secret rm "$1" >/dev/null 2>&1
        echo "Removed old value of: $1"
    fi
}

remove_secret gf_admin_password
echo

# Create Docker secrets
head -c 24 /dev/urandom | base64 | tee "${SECRETS_DIR}/gf_admin_password" | cat <(echo -n "Setting gf_admin_password: ")
docker secret create gf_admin_password "${SECRETS_DIR}/gf_admin_password"
echo
