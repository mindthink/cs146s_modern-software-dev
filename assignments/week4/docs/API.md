# Week 4 API

Generated against OpenAPI from `backend.app.main:app`. Base URL: `http://127.0.0.1:8000`.

Interactive docs: `/docs` · raw schema: `/openapi.json`

## Notes

| Method | Path | Body | Success | Errors |
|--------|------|------|---------|--------|
| `GET` | `/notes/` | — | `NoteRead[]` | — |
| `POST` | `/notes/` | `{ title, content }` (min length 1) | `201 NoteRead` | `422` validation |
| `GET` | `/notes/search/?q=` | — | `NoteRead[]` (case-insensitive; empty `q` lists all) | — |
| `GET` | `/notes/{id}` | — | `NoteRead` | `404` |
| `PUT` | `/notes/{id}` | `{ title?, content? }` (at least one) | `NoteRead` | `400` empty body, `404`, `422` |
| `DELETE` | `/notes/{id}` | — | `204` | `404` |
| `POST` | `/notes/{id}/extract` | — | `ExtractResult` | `404` |

### Schemas

```json
NoteRead: { "id": 1, "title": "…", "content": "…" }
ExtractResult: {
  "note_id": 1,
  "tags": ["backend", "qa"],
  "action_items": [{ "id": 1, "description": "TODO: …", "completed": false }]
}
```

`extract` parses `TODO:` / trailing-`!` lines into action items and `#tags` (deduped, lowercased).

## Action items

| Method | Path | Body | Success | Errors |
|--------|------|------|---------|--------|
| `GET` | `/action-items/` | — | `ActionItemRead[]` | — |
| `POST` | `/action-items/` | `{ description }` (min length 1) | `201 ActionItemRead` | `422` |
| `PUT` | `/action-items/{id}/complete` | — | `ActionItemRead` (`completed: true`) | `404` |

```json
ActionItemRead: { "id": 1, "description": "…", "completed": false }
```

## Frontend

Static UI at `/` (`frontend/`). Supports note search, edit/delete, extract → action items, and complete.

## Drift check

After route changes, re-run:

```bash
cd assignments/week4
PYTHONPATH=. python -c "from backend.app.main import app; print(sorted(app.openapi()['paths']))"
```

Or invoke the `/week4-docs-sync` automation (see `.claude/commands/week4-docs-sync.md`).
