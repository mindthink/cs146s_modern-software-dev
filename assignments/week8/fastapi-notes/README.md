# Week 8 — Version A: FastAPI Notes

Self-study stack: **FastAPI + SQLAlchemy + SQLite + vanilla JS**.

## Prerequisites

- Python 3.10+
- Poetry (from repo root) **or** `pip install fastapi uvicorn sqlalchemy pydantic`

## Run (from repo root)

```bash
cd assignments/week8/fastapi-notes
poetry run uvicorn app:app --reload --port 8008
```

Open http://127.0.0.1:8008

## API

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/notes` | list |
| POST | `/api/notes` | create `{title, content}` |
| GET | `/api/notes/{id}` | read |
| PUT | `/api/notes/{id}` | update |
| DELETE | `/api/notes/{id}` | delete |

DB file: `data/app.db` (created on first run).

## Manual fixes / notes

- Single-file backend (`app.py`) for easy reading; UI under `frontend/`.
- Validation via Pydantic `min_length`; 404/400 on missing/empty updates.
- XSS-safer list rendering uses `textContent` (not `innerHTML` for note bodies).
