---
title: Changelog — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-07
parent: README.md
children: []
siblings: [README.md, CURSOR.md, ARCHITECTURE.md]
audience: internal
tags: [yingson-labs, kopia, changelog]
summary: "Changelog for the kopia service repo."
doc_type: changelog
scope: service
service_name: kopia
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# Changelog

## [Unreleased]

- Jason confirmed the laptop user password, the admin password, and the repo encryption password are in Dashlane. UniFi reservation `kopia-LXC` is verified. Package check: installed and candidate are 0.23.1, so the hold stays. Baseline at 17:39 PDT: process 0% CPU, 183 MB resident, guest 170 MiB used.

- Readiness is R3. PBS snapshot `ct/135/2026-10-07T09:12:34Z` restored to scratch CT 198 with the repository unmounted and the NIC down, then destroyed. Live CT 135 stayed up. Not R4. The repo password is in Dashlane. There is still no external-drive copy.

- Discord snapshot failures for a missing path are a client-policy problem. `hooks.json` stays retired. Hermes proposes no server restart for that alert. The steps are in TROUBLESHOOTING.md.

- Laptop client `laptop@jason` snapshots `C:\Users\thedu\.cursor\mcps\` and `C:\Users\thedu\.cursor\hooks\` as folders, every 24h. `mcps` ignores `comfy-mcp/`. The per-file env policies and the missing `hooks.json` source are removed. Older snapshots of those files stay until retention.

- The sign-in proxy now forwards Kopia's CSRF cookies and `X-Kopia-Csrf-Token`. Without them the UI shell loaded and every page returned 401.

- Sign-in form in front of the UI. Chrome was showing Kopia's `Missing credentials.` page and never the basic-auth prompt. NPM host 51 now forwards to `kopia-ui-proxy` on port 51516.

## [0.1.0] — 2026-10-05

- Initial service repo. CT 135, NPM host 51, Homarr tile on YingsonDash, Kuma 113 and 114.
- Web sign-in documented as HTTP basic auth. Username `kopia`.
