---
title: Architecture — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [CHANGELOG.md, CURSOR.md, BASELINES.md, TROUBLESHOOTING.md]
audience: internal
tags: [yingson-labs, kopia, architecture]
summary: "Kopia repository server on CT 135. Clients push file-level backups to the NAS backups share."
doc_type: architecture
scope: service
service_name: kopia
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# Architecture — Kopia

**Slug:** `kopia` · **Status:** `active` · **Host:** CT 135 / 192.168.30.32 · **Readiness:** R2

---

## Table of Contents

1. [Overview](#1-overview)
2. [Host & Runtime](#2-host--runtime)
3. [Network & Access](#3-network--access)
4. [Components](#4-components)
5. [Dependencies](#5-dependencies)
6. [Data Flow](#6-data-flow)
7. [Storage & Layout](#7-storage--layout)
8. [Configuration & Environment](#8-configuration--environment)
9. [Deployment](#9-deployment)
10. [Backup & Recovery](#10-backup--recovery)
11. [Monitoring & Health](#11-monitoring--health)
12. [API & Automation Profile](#12-api--automation-profile)
13. [Security](#13-security)
14. [Known Issues & Constraints](#14-known-issues--constraints)
15. [Operational Procedures](#15-operational-procedures)
16. [Open Items & Planned Changes](#16-open-items--planned-changes)

---

## 1. Overview

Kopia 0.23.1 holds the lab's file-level backups. Clients push. The server does not dial out to them. The repository is on the NAS `backups` share so it is outside the PBS datastore.

The web UI is for Jason. Backup jobs are systemd timers on each client.

## 2. Host & Runtime

| Item | Value |
|---|---|
| Guest | CT 135, unprivileged, Debian 13, onboot |
| Address | `192.168.30.32/24`, gateway `192.168.30.1` |
| Resources | 2 cores, 2048 MB RAM, 512 MB swap, 8 GB rootfs on local-lvm |
| Package | Kopia 0.23.1 from `packages.kopia.io`, `apt-mark hold` |
| Service | `kopia-server.service` |
| Listen | `0.0.0.0:51515`, TLS, gRPC, HTML UI on |

## 3. Network & Access

| Name | Where it goes |
|---|---|
| `https://kopia.yingson.com` | AdGuard rewrite to NPM `192.168.30.182`, proxy host **51**, certificate `*.yingson.com`, forwards to `https://192.168.30.32:51515` with TLS verify off |
| Direct | `https://192.168.30.32:51515`, self-signed certificate. Clients pin its SHA-256 |
| Cloudflare | None. Internal only |

The browser login is a form served by `kopia-ui-proxy` on port 51516. NPM host 51 forwards there. Username `kopia`. The proxy checks that password with Kopia and keeps the session in a cookie. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Homarr app `m8on29qotzh2pv73vc5zvyua` is on YingsonDash only. It is not on Lab-Dashboard. Ping URL is blank: the UI returns 401 until login, and the guest certificate is self-signed, so a Homarr ping would show the tile down while the service is fine. Kuma owns reachability.

## 4. Components

| Piece | Role |
|---|---|
| `kopia server` | Repository server and UI |
| Repository users | One per client: `kuma@ct100`, `laptop@jason`, `proxmox@host`, `pbs@vm111`, `adguard@ct105`, plus `kopia@kopia` |
| Server basic-auth user | `kopia`. This is the web login. It is not a repository user |

## 5. Dependencies

| Depends on | Why |
|---|---|
| NAS NFS `backups` | The repository directory |
| NPM CT 107 | Name and certificate |
| AdGuard CT 105 | Explicit rewrite |
| UniFi | DHCP reservation for `192.168.30.32` |

Clients that push: CT 100, the Proxmox host, PBS VM 111, CT 105. The laptop client is not installed yet.

## 6. Data Flow

A client connects to `https://192.168.30.32:51515` with its own user password, then snapshots a local path. The server writes packs under `/mnt/nas`. The repository encryption password stays on the server. It is not the web login and not the client password.

The browser connects to the name on port 443. NPM presents the wildcard certificate and proxies to the guest.

## 7. Storage & Layout

| Path | What |
|---|---|
| `/mnt/nas` | Repository. NAS `/volume1/proxmox/backups/kopia` |
| `/etc/kopia/server.env` | Service environment. Mode 600. Not in git |
| `/etc/kopia/*.password` | Password files. Mode 600. Not in git |
| `/etc/kopia/tls.cert` and `tls.key` | Backend certificate |
| `/root/.config/kopia/repository.config` | Server repository config |
| `/etc/systemd/system/kopia-server.service` | Unit |

Retention, global: 10 latest, 0 hourly, 14 daily, 8 weekly, 12 monthly, 3 annual.

## 8. Configuration & Environment

Laptop file: `C:\Users\thedu\.cursor\mcps\kopia.env`. Key names are in [.env.example](.env.example).

| Vault item | Use |
|---|---|
| `vault://dashlane/yingson-labs/kopia/server-password` | Web login. Env `KOPIA_SERVER_PASSWORD` |
| `vault://dashlane/yingson-labs/kopia/laptop-user` | Client `laptop@jason` |
| `vault://dashlane/yingson-labs/kopia/repo-password` | Repository encryption |
| `vault://dashlane/yingson-labs/kopia/control-password` | Server control user `server-control` |

`KOPIA_CERT_SHA256` is the backend certificate, not the wildcard.

## 9. Deployment

The guest was created 2026-10-03. This repo has no deploy checkout on CT 135. Outbound deploy key: n-a.

Changing the unit or `/etc/kopia/server.env` requires `systemctl daemon-reload` and a restart. Adding a repository user needs a restart before that user can connect.

## 10. Backup & Recovery

This service is the file-level backup system. Its own guest disk is in the nightly PBS job. A scratch restore of CT 135 has not been done. That is Gate 7, still open.

Same-night restore proofs on 2026-10-03 compared checksums for the server canary, Kuma's sqlite backup, Proxmox `storage.cfg`, the PBS config tree, and AdGuard's yaml. Restore directories were removed afterward.

A second repository on the external drive does not exist yet. The NAS copy does not survive a dead NAS.

## 11. Monitoring & Health

| Monitor | Check |
|---|---|
| Kuma 113 `kopia (DNS)` | `https://kopia.yingson.com/`, accepts 200–299 and 401 |
| Kuma 114 `kopia (IP)` | TCP `192.168.30.32:51515` |

Both notify Discord `#alerts`. Jason confirmed a down/up on 2026-10-05.

## 12. API & Automation Profile

| Field | Value |
|---|---|
| **API type** | `rest` plus the repository protocol on the same port |
| **Base URL** | `https://192.168.30.32:51515` |
| **OpenAPI spec** | n/a |
| **Auth method** | `login-session` (HTTP basic). Web user `kopia`. Clients use `user@host` |
| **Token generated at** | No API token. Passwords are files on CT 135 and the laptop env |
| **Scope required** | n/a |
| **Vault reference** | `vault://dashlane/yingson-labs/kopia/server-password` |
| **MCP / wrapper status** | `do not add` — a write-capable client can delete snapshots |
| **Baselines** | [BASELINES.md](BASELINES.md) |
| **Permission tier** | `destructive` |

### Tier justification

A logged-in session can delete snapshots. There is no scoped read-only token. No agent token is issued. The tier cannot be enforced by a scope. It is convention: agents do not get the password, and they do not delete snapshots.

### Useful endpoints

| Purpose | Call | Tier |
|---|---|---|
| UI up, login required | `GET https://kopia.yingson.com/` returns 401 with `WWW-Authenticate: Basic realm="Kopia"` | `read-only` |
| UI | Same URL with basic auth user `kopia` returns HTML `KopiaUI` | `destructive` |

## 13. Security

- **Exposure:** LAN and Tailscale via NPM. No Cloudflare hostname.
- **Authentication:** HTTP basic auth in front of the UI. Repository users are separate.
- **Inter-VLAN rules:** The guest is on the IoT network with a DHCP reservation. No extra firewall change was made for this service.
- **Secrets:** vault paths above. Never commit password files.

## 14. Known Issues & Constraints

| Issue | Impact | Workaround | Incident |
|---|---|---|---|
| Unauthenticated UI is the text `Missing credentials.` | Looks like a failed login. The browser prompt is the form | Private window, username `kopia` | none |
| Clients must use the IP and the pinned backend certificate | The public name presents a different certificate | Leave client configs on `192.168.30.32:51515` | none |
| Guest calling its own public name failed from inside CT 135 | Do not health-check the name from the guest | Check from the Proxmox host or the laptop | none |

## 15. Operational Procedures

### Restart

```bash
ssh jason@proxmox "sudo pct exec 135 -- systemctl restart kopia-server"
```

**Tier:** `remediate`. Confirm the service is active and the name still returns 401.

Longer steps are in [docs/RUNBOOK.md](docs/RUNBOOK.md).

## 16. Open Items & Planned Changes

| Item | Status | Why |
|---|---|---|
| Scratch restore of CT 135 | Deferred | Waiting on a PBS snapshot of this guest |
| External-drive repository | Deferred | The drive has to be attached |
| Laptop Kopia client | Deferred | Not installed |
| GitHub mirror | Deferred | Not created in this pass |
| Dashlane copy of the repo encryption password | Deferred | Jason has not confirmed that item |
| NPM, Tailscale, cloudflared, and the remaining service paths | Deferred | First four clients are enrolled |

---

## Related

- [lab-standards LAB-DEC-029](https://gitea.yingson.com/jason/lab-standards)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [docs/RUNBOOK.md](docs/RUNBOOK.md)
