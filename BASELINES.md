---
title: Baselines — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [ARCHITECTURE.md, TROUBLESHOOTING.md]
audience: internal
tags: [yingson-labs, kopia, baselines]
summary: "Measured baselines for the Kopia repository server. Empty fields are not yet measured."
doc_type: baselines
scope: service
service_name: kopia
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# Baselines — kopia

| Field | Value |
|---|---|
| Repository size | not yet measured |
| Snapshot duration, Kuma | not yet measured |
| Snapshot duration, Proxmox `/etc/pve` | not yet measured |
| Snapshot duration, PBS config | not yet measured |
| Snapshot duration, AdGuard | not yet measured |
| Restore time | not yet measured. Same-night checksum compares passed on 2026-10-03. Times were not recorded. |
| Guest CPU / RAM under maintenance | not yet measured |

Gate 8 (one idle week) is not started.
