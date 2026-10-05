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

That text is Kopia's own 401 page. Chrome on this laptop does not show the browser login box, so that page was all there was to see. It does not mean the password was rejected.

https://kopia.yingson.com now serves a sign-in form (CT 135, `kopia-ui-proxy` on port 51516, NPM host 51). Username `kopia`. Password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env`, vault `vault://dashlane/yingson-labs/kopia/server-password`. A wrong password stays on the form and says the credentials were not accepted.

Reload the tab. The old 401 text is not the form.

## The prompt appears and then says "Access denied."

The username for the web UI is `kopia`, not `laptop@jason`. `laptop@jason` is the laptop backup client. The repository encryption password is a third value and is not the web login.

## Kuma says the name is up but the page will not load

Kuma 113 treats HTTP 401 as up. A 401 means NPM reached Kopia and Kopia asked for a login. Certificate problems and connection failures are a different Kuma state.

## A client backup fails fingerprint check

Enrolled clients pin the self-signed certificate on `192.168.30.32:51515`. Do not point them at `https://kopia.yingson.com`. That name presents the lab wildcard certificate.
