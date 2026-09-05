# Week 4 starter app — agent guidance

Use this file when working under `assignments/week4/`.

## Layout

- `backend/app/` — FastAPI app (`main.py`, `routers/`, `models.py`, `schemas.py`, `db.py`, `services/`)
- `frontend/` — static UI (`index.html`, `app.js`, `styles.css`) served at `/` and `/static`
- `data/seed.sql` — SQLite seed applied on first DB create
- `docs/TASKS.md` — practice backlog for agent-driven changes
- `docs/API.md` — human API docs (keep in sync with `/openapi.json`)

## How to run (from `assignments/week4/`)

```bash
make run          # http://127.0.0.1:8000
make test         # pytest backend/tests
make format       # black + ruff --fix
make lint         # ruff check
make seed         # apply seed if needed
```

Poetry from repo root also works if deps are installed:

```bash
cd assignments/week4 && PYTHONPATH=. poetry run uvicorn backend.app.main:app --reload
cd assignments/week4 && PYTHONPATH=. poetry run pytest -q backend/tests
```

## Conventions

- Prefer **failing test → implement → `make test` → `make lint`** for endpoint work.
- Keep responses Pydantic-typed; use `HTTPException` for 404/400.
- SQLite + SQLAlchemy; do not invent a second ORM.
- Frontend is vanilla JS — no build step.
- Pre-commit config lives at `pre-commit-config.yaml` in this folder:
  `pre-commit run --all-files -c pre-commit-config.yaml`

## Safety

- Safe: `make test`, `make lint`, `make format`, reading OpenAPI, editing week4 files.
- Avoid: deleting `data/*.db` without asking; force-push; changing unrelated weeks.
