---
title: CLAUDE — kopia (AI agent entry point)
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [CURSOR.md, README.md, ARCHITECTURE.md]
audience: internal
tags: [yingson-labs, kopia, agent-briefing, claude]
summary: "Entry point for AI agents working in kopia."
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

# CLAUDE.md — kopia

> **`lab-standards` is the source of truth for this repo's documentation.** This repo is a **child** of it.

Contract: [`lab-standards/LAB-DOC-CONTRACT.md`](https://gitea.yingson.com/jason/lab-standards)

**Slug:** `kopia` · **Host:** CT 135 / 192.168.30.32 · **Tier:** `destructive`

## Lab-standards sync

| Field | Value |
|---|---|
| **Last reconciled** | 2026-10-05 |
| **lab-standards commit** | `3bc5d70` |
| **lab-standards version** | 1.9.37, plus uncommitted 2026-10-05 notes |
| **Reconciled by** | Cursor |
| **Open items flowing up** | External-drive repo. Gate 7, the GitHub mirror, and the Dashlane repo password are done |

## Read order

1. [`lab-standards/LAB-DOC-CONTRACT.md`](https://gitea.yingson.com/jason/lab-standards)
2. [CURSOR.md](CURSOR.md)
3. [ARCHITECTURE.md](ARCHITECTURE.md)
4. [`lab-standards/SERVICE-INVENTORY.md`](https://gitea.yingson.com/jason/lab-standards)
5. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) · [BASELINES.md](BASELINES.md) · [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Stop and alert

If two sources disagree, or a slug does not resolve, stop and alert Jason. Do not guess.

Never print a Kopia password, certificate key, or the contents of `kopia.env`.
