#!/bin/sh

IFACE="eth0"

echo "TC_ENABLE = ${TC_ENABLE}"

# Use tc to simulate latency
if [ "${TC_ENABLE}" -eq 1 ]; then
    echo "Adding latency and jitter..."
    tc qdisc add dev "${IFACE}" root netem delay "${TC_LATENCY}" "${TC_JITTER}"
fi


# Start caddy server
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
