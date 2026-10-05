# kopia

File-level backup repository server for Yingson Labs. Clients push. The repository sits on the NAS `backups` share, not in the PBS datastore.

**UI:** https://kopia.yingson.com

The page is HTTP basic auth. Username `kopia`. The password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env` and Dashlane `vault://dashlane/yingson-labs/kopia/server-password`. The plain text `Missing credentials.` means the browser did not send a username. It is not a rejected password.

**Host:** CT 135, `192.168.30.32`, Kopia 0.23.1 (held).

**Repo path:** `/volume1/proxmox/backups/kopia` (guest bind `/mnt/nas`).

Full detail is in [ARCHITECTURE.md](ARCHITECTURE.md). Lab-wide rules live in [lab-standards](https://gitea.yingson.com/jason/lab-standards).
