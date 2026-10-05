# Runbook — kopia

## Sign in

1. Open https://kopia.yingson.com in a new browser tab.
2. When the browser asks, username `kopia`.
3. Password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env`.

Do not paste the password into chat.

## Restart

From the laptop, no sudo on Windows. The remote command uses sudo on the hypervisor:

```bash
ssh jason@proxmox "sudo pct exec 135 -- systemctl restart kopia-server"
```

Then confirm `systemctl is-active kopia-server` prints `active`. An unauthenticated request to the name should be HTTP 401 with `WWW-Authenticate: Basic realm="Kopia"`.

## Where the repository is

Guest path `/mnt/nas`. NAS path `/volume1/proxmox/backups/kopia`. Do not delete that directory. It is the only copy until the external-drive repository exists.

## Clients

Timers, America/Los_Angeles: Kuma 03:20, Proxmox host 03:25, PBS 03:30, AdGuard 03:35. Each client uses its own user password, not the web login and not the repository encryption password.
