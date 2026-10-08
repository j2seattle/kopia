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
| Guest memory | 170 MiB used of 2 GiB, 1.8 GiB available. 2026-10-07 17:39 PDT |
| Kopia process | 0.0% CPU, 183 MB resident |
| Guest swap | 856 KiB used of 512 MiB, read inside the guest |
| Guest disk `/` | 939 MB used of 7.8 GB (13%) |
| Load average | 3.83, 3.60, 3.77. Same numbers on the Proxmox host. Host load, not the Kopia process. No warning limits |

Gate 8 is one reading. It is not an idle week, and warning and critical thresholds are not set.
