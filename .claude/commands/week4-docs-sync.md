---
description: Sync assignments/week4/docs/API.md from live OpenAPI
argument-hint: "[optional note about focus endpoints]"
---

# Week 4 docs sync

Refresh human API docs for the Week 4 starter so they match the running app.

## Steps

1. Ensure you can inspect OpenAPI for the Week 4 app:
   - Prefer starting the app (`cd assignments/week4 && make run`) and fetching `http://127.0.0.1:8000/openapi.json`, **or**
   - Import `backend.app.main:app` and call `app.openapi()` in a short Python snippet (no server required).
2. Read current `assignments/week4/docs/API.md` (create it if missing).
3. Update `API.md` to document every route: method, path, request body fields, response shape, notable errors (400/404).
4. Compare previous vs new routes; list **added / removed / changed** endpoints.
5. Mention `$ARGUMENTS` focus if provided (e.g. only notes routes).

## Output

- Diff-like summary of route deltas
- Confirmation that `API.md` was updated
- TODOs if OpenAPI and code disagree

## Safety

- Only edit `assignments/week4/docs/API.md` unless asked otherwise.
- Do not invent endpoints that are not in OpenAPI.
