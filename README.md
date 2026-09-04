# KVD Scout Station Backend

Local-first, proof-gated handoff backend skeleton for the KVD Scout Station.

## Boundary

This service prepares and records handoffs only. It does not publish, upload, send, authenticate to platforms, or store credentials. The public Zapia page is static; this backend must be deployed separately on an approved server before any frontend integration.

## Endpoints

- `GET /health`
- `GET /api/state`
- `POST /api/handoff`

## Status model

`PREPARED -> SENT -> PUBLISHED -> VERIFIED` is not automatic. A destination URL, media ID, receipt, timestamp, and independent verification are required before promotion.

## Backend target

Primary deployment candidate: https://github.com/appwrite/appwrite
Fallback: https://github.com/pocketbase/pocketbase

The local skeleton is intentionally provider-neutral until a separately hosted runtime is authorized and tested. No third-party code is bundled in this repository skeleton.

## Sources reviewed

- https://github.com/appwrite/appwrite
- https://github.com/pocketbase/pocketbase
- https://github.com/earthwalker17/agent-os
- https://github.com/gmickel/flow-next
- https://github.com/Cranot/roam-code
