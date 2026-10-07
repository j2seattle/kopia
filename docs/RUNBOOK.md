---
title: Runbook — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-07
parent: ARCHITECTURE.md
children: []
siblings: [TROUBLESHOOTING.md]
audience: ops
tags: [yingson-labs, kopia, runbook]
summary: "Sign-in, restart, and the 2026-10-07 scratch restore for the Kopia guest."
doc_type: runbook
scope: service
service_name: kopia
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: remediate
last_verified: 2026-10-07
---

# Runbook — kopia

## Sign in

1. Open https://kopia.yingson.com.
2. Username `kopia`.
3. Password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env`.

The form is `kopia-ui-proxy` on port 51516. Kopia itself stays on 51515. Restart the form with `systemctl restart kopia-ui-proxy` inside CT 135. An unauthenticated request to the name should be the sign-in page, not the words `Missing credentials.`

Do not paste the password into chat.

## Restart

From the laptop, no sudo on Windows. The remote command uses sudo on the hypervisor:

```bash
ssh jason@proxmox "sudo pct exec 135 -- systemctl restart kopia-server"
```

Then confirm `systemctl is-active kopia-server` and `systemctl is-active kopia-ui-proxy` both print `active`. An unauthenticated request to the name should be the sign-in page.

## Where the repository is

Guest path `/mnt/nas`. NAS path `/volume1/proxmox/backups/kopia`. Do not delete that directory. It is the only copy until the external-drive repository exists.

## Scratch restore

On 2026-10-07, `ct/135/2026-10-07T09:12:34Z` was restored to CT 198. From the laptop this is SSH as `jason@proxmox`, and `pct` needs `sudo`. The copy was unprivileged, hostname `scratch`, onboot 0, NIC down, and `mp0` removed before boot so it could not mount the live repository. It printed `scratch`. `kopia-server` was enabled and `/mnt/nas` was not mounted. CT 198 was destroyed. Live CT 135 stayed running. This did not restore the repository.

## Clients

Timers, America/Los_Angeles: Kuma 03:20, Proxmox host 03:25, PBS 03:30, AdGuard 03:35. Each client uses its own user password, not the web login and not the repository encryption password.
