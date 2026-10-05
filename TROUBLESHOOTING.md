---
title: Troubleshooting — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [ARCHITECTURE.md, CURSOR.md]
audience: internal
tags: [yingson-labs, kopia, troubleshooting]
summary: "What the Kopia UI page means, and the first checks when backups stop."
doc_type: troubleshooting
scope: service
service_name: kopia
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# Troubleshooting — kopia

## The site says "Missing credentials."

That sentence is the body of an HTTP 401. Kopia did not receive a username. It does not mean the password in Dashlane was rejected.

The sign-in is the browser's own username/password prompt, not a form on the page. Username is `kopia`. The password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env`. That file matches `/etc/kopia/server.password` on CT 135 (checked 2026-10-05, values not recorded here).

If the prompt never appears, open a private window and go to https://kopia.yingson.com. A cancelled prompt stays cancelled until the tab is closed. A password manager can swallow the prompt and leave this sentence on the page.

A wrong password is a different page: `Access denied.`

## The prompt appears and then says "Access denied."

The username for the web UI is `kopia`, not `laptop@jason`. `laptop@jason` is the laptop backup client. The repository encryption password is a third value and is not the web login.

## Kuma says the name is up but the page will not load

Kuma 113 treats HTTP 401 as up. A 401 means NPM reached Kopia and Kopia asked for a login. Certificate problems and connection failures are a different Kuma state.

## A client backup fails fingerprint check

Enrolled clients pin the self-signed certificate on `192.168.30.32:51515`. Do not point them at `https://kopia.yingson.com`. That name presents the lab wildcard certificate.
