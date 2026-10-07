---
title: Baselines — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-07
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
| Restore time | Guest scratch restore on 2026-10-07 finished in about 28 seconds. The repository was not restored. Same-night checksum compares passed on 2026-10-03. |
| Guest memory | 171 MiB used of 2 GiB, 1.8 GiB available. 2026-10-07 15:23 PDT |
| Guest swap | 856 KiB used of 512 MiB, read inside the guest |
| Guest disk `/` | 931 MB used of 7.8 GB (13%) |
| Load average | 5.19, 4.89, 4.98 on 2 vCPU. Not an idle reading. No thresholds |

Gate 8 is one reading. It is not an idle week, and warning and critical thresholds are not set.
