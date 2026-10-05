---
title: Changelog — kopia
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-05
parent: README.md
children: []
siblings: [README.md, CURSOR.md, ARCHITECTURE.md]
audience: internal
tags: [yingson-labs, kopia, changelog]
summary: "Changelog for the kopia service repo."
doc_type: changelog
scope: service
service_name: kopia
depends_on: []
depended_on_by: []
agent_context: true
permission_tier: destructive
last_verified: 2026-10-05
---

# Changelog

## [Unreleased]

- The sign-in proxy now forwards Kopia's CSRF cookies and `X-Kopia-Csrf-Token`. Without them the UI shell loaded and every page returned 401.

- Sign-in form in front of the UI. Chrome was showing Kopia's `Missing credentials.` page and never the basic-auth prompt. NPM host 51 now forwards to `kopia-ui-proxy` on port 51516.

## [0.1.0] — 2026-10-05

- Initial service repo. CT 135, NPM host 51, Homarr tile on YingsonDash, Kuma 113 and 114.
- Web sign-in documented as HTTP basic auth. Username `kopia`.
