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

## Clients

Timers, America/Los_Angeles: Kuma 03:20, Proxmox host 03:25, PBS 03:30, AdGuard 03:35. Each client uses its own user password, not the web login and not the repository encryption password.
