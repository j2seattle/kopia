---
title: Troubleshooting — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-07
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

## Snapshots says "Request failed with status code 401"

The shell loaded, and the API call did not. Kopia requires a CSRF cookie plus the `X-Kopia-Csrf-Token` header on every API call. Reload https://kopia.yingson.com/snapshots after signing in. A reload picks up both. If it still fails, sign out by opening https://kopia.yingson.com/logout and sign in again.

## The prompt appears and then says "Access denied."

The username for the web UI is `kopia`, not `laptop@jason`. `laptop@jason` is the laptop backup client. The repository encryption password is a third value and is not the web login.

## Kuma says the name is up but the page will not load

Kuma 113 treats HTTP 401 as up. A 401 means NPM reached Kopia and Kopia asked for a login. Certificate problems and connection failures are a different Kuma state.

## A client backup fails fingerprint check

Enrolled clients pin the self-signed certificate on `192.168.30.32:51515`. Do not point them at `https://kopia.yingson.com`. That name presents the lab wildcard certificate.

## Discord says a snapshot failed because the file is missing

The Kopia Backup post names the path, then `GetFileAttributesEx` or "The system cannot find the file specified." That failure happens on the client, before a pack is written. Restarting `kopia-server` on CT 135 does not create the file.

`C:\Users\thedu\.cursor\hooks.json` is not a source. The file was deleted. The laptop policy has to drop that source. The folder source is `C:\Users\thedu\.cursor\hooks\`. Leave the 2026-10-06 snapshot until retention. Do not recreate `hooks.json`. Do not delete snapshots to clear the alert.

Hermes reads this alert in `#alerts` and posts the checkup in `#hermes-sre`. For a missing path the proposal is none. The only Kopia case it will ask to start is CT 135, and only when the alert is a connection failure and that guest is stopped.
