# Week 2 — Action Item Extractor

Minimal FastAPI + SQLite app that turns free-form meeting notes into a checklist of action items. Supports heuristic extraction and an optional Ollama-powered LLM extractor, plus a tiny HTML frontend.

## Overview

| Layer | Role |
|-------|------|
| `frontend/index.html` | Paste notes; **Extract** / **Extract LLM** / **List Notes** |
| `app/routers/` | HTTP API for notes and action items |
| `app/services/extract.py` | Heuristic + LLM extraction |
| `app/schemas.py` | Pydantic request/response contracts |
| `app/db.py` | SQLite persistence under `data/app.db` |

## Setup

From the **repository root** (Poetry env already installed per top-level README):

```bash
source .venv/bin/activate   # or: poetry shell / conda activate cs146s
```

For LLM extraction, run [Ollama](https://ollama.com/) locally and pull a model, e.g.:

```bash
ollama pull mistral-nemo:12b
# optional override:
export OLLAMA_MODEL=mistral-nemo:12b
```

## Run the server

```bash
poetry run uvicorn assignments.week2.app.main:app --reload
```

Open http://127.0.0.1:8000/

Interactive API docs: http://127.0.0.1:8000/docs

## API endpoints

### Notes

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/notes` | Create a note (`{"content": "..."}`) |
| `GET` | `/notes` | List all notes |
| `GET` | `/notes/{note_id}` | Get one note |

### Action items

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/action-items/extract` | Heuristic extract (`{"text": "...", "save_note": true}`) |
| `POST` | `/action-items/extract-llm` | LLM extract (same body; requires Ollama) |
| `GET` | `/action-items` | List action items (optional `?note_id=`) |
| `POST` | `/action-items/{id}/done` | Mark done (`{"done": true}`) |

Extract responses look like:

```json
{
  "note_id": 1,
  "items": [{"id": 10, "text": "Set up database"}]
}
```

## Frontend

1. Paste notes into the textarea.
2. Optionally keep **Save as note** checked.
3. **Extract** — rule-based bullets / `TODO:` / checkboxes.
4. **Extract LLM** — Ollama structured JSON extraction (slower).
5. **List Notes** — show saved notes from SQLite.
6. Toggle checkboxes on extracted items to mark them done via the API.

## Tests

From the repository root:

```bash
source .venv/bin/activate
cd assignments
python -m pytest week2/tests/test_extract.py -q
```

LLM unit tests mock `ollama.chat` (no live server required). To run the optional live Ollama test:

```bash
RUN_OLLAMA_TESTS=1 python -m pytest week2/tests/test_extract.py -q
```

## Project layout

```text
assignments/week2/
├── assignment.md
├── writeup.md
├── README.md          ← this file
├── app/
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   ├── routers/
│   └── services/extract.py
├── frontend/index.html
├── tests/test_extract.py
└── data/              ← SQLite DB (created at runtime)
```

## Course notes

Assignment brief: [`assignment.md`](./assignment.md). Submission write-up: [`writeup.md`](./writeup.md).
