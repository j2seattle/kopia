# kopia

File-level backup repository server for Yingson Labs. Clients push. The repository sits on the NAS `backups` share, not in the PBS datastore.

**UI:** https://kopia.yingson.com

Sign in on the form. Username `kopia`. The password is `KOPIA_SERVER_PASSWORD` in `C:\Users\thedu\.cursor\mcps\kopia.env` and Dashlane `vault://dashlane/yingson-labs/kopia/server-password`.

**Host:** CT 135, `192.168.30.32`, Kopia 0.23.1 (held).

**Repo path:** `/volume1/proxmox/backups/kopia` (guest bind `/mnt/nas`).

Full detail is in [ARCHITECTURE.md](ARCHITECTURE.md). Lab-wide rules live in [lab-standards](https://gitea.yingson.com/jason/lab-standards).
