# Week 8 — Version C: Flask Notes

Self-study stack: **Flask (Python, non-JS backend) + sqlite3 + vanilla JS**.

## Prerequisites

- Python 3.10+

```bash
cd assignments/week8/flask-notes
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Or from repo root with Poetry (if you add Flask to the project):

```bash
poetry run pip install flask
```

## Run

```bash
cd assignments/week8/flask-notes
source .venv/bin/activate
python app.py
```

Open http://127.0.0.1:8009

## API

Same shape as Version A:

| Method | Path |
|--------|------|
| GET/POST | `/api/notes` |
| GET/PUT/DELETE | `/api/notes/<id>` |

SQL uses **bound parameters** (`?` placeholders). DB: `data/app.db`.

## Manual fixes / notes

- Intentionally simpler than FastAPI: stdlib `sqlite3`, manual JSON validation.
- UI copied from Version A (same flows) with a different accent color so you can tell them apart.
- No AI app generator used for this version (hand-written for stack comparison).
