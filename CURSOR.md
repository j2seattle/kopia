---
title: CURSOR — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [ARCHITECTURE.md, CHANGELOG.md, CLAUDE.md]
audience: internal
tags: [yingson-labs, kopia, agent-briefing]
summary: "Agent briefing for the Kopia repository server."
doc_type: agent-briefing
scope: service
service_name: kopia
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# CURSOR — kopia

CT 135 (`192.168.30.32`) runs Kopia 0.23.1. The repository is `/volume1/proxmox/backups/kopia`. Do not put secrets in this repo.

## Current state

- UI: `https://kopia.yingson.com` (NPM host 51 forwards to port 51516). Sign-in form, username `kopia`. `kopia-ui-proxy` adds basic auth toward Kopia on 51515.
- Homarr app `m8on29qotzh2pv73vc5zvyua` is on YingsonDash. Ping is blank because the UI returns 401 until login. Kuma 113 and 114 are the reachability checks.
- No git checkout on the guest. Outbound deploy key is n-a.
- No agent token. Snapshot delete is destructive.

## Do not

- Print passwords from `/etc/kopia/` or from `kopia.env`.
- Point a Kopia client at `https://kopia.yingson.com` while pinning the backend certificate fingerprint. Clients use `https://192.168.30.32:51515` and `KOPIA_CERT_SHA256`.
- Fire another Kuma down/up test. Jason confirmed the alert on 2026-10-05.
