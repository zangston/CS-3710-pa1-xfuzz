#!/bin/sh

# Use tc to simulate latency
if [ "${TC_ENABLE}" -eq 1 ]; then
    tc qdisc add dev eth0 root netem delay "${TC_LATENCY}" "${TC_JITTER}"
fi


# Start caddy server
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
