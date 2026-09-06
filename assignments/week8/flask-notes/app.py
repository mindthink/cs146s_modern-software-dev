"""Week 8 Version C — Flask notes CRUD + static UI (non-JS backend)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"
FRONTEND = ROOT / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="/static")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_: object | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
    )
    db.commit()
    db.close()


def row_to_note(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "title": row["title"], "content": row["content"]}


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/api/notes")
def list_notes():
    rows = get_db().execute("SELECT id, title, content FROM notes ORDER BY id DESC").fetchall()
    return jsonify([row_to_note(r) for r in rows])


@app.post("/api/notes")
def create_note():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    content = (payload.get("content") or "").strip()
    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400
    if len(title) > 200:
        return jsonify({"error": "title too long"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    db.commit()
    row = db.execute(
        "SELECT id, title, content FROM notes WHERE id = ?",
        (cur.lastrowid,),
    ).fetchone()
    return jsonify(row_to_note(row)), 201


@app.get("/api/notes/<int:note_id>")
def get_note(note_id: int):
    row = (
        get_db()
        .execute(
            "SELECT id, title, content FROM notes WHERE id = ?",
            (note_id,),
        )
        .fetchone()
    )
    if row is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(row_to_note(row))


@app.put("/api/notes/<int:note_id>")
def update_note(note_id: int):
    payload = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT id, title, content FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Note not found"}), 404

    title = payload.get("title", row["title"])
    content = payload.get("content", row["content"])
    if title is not None:
        title = str(title).strip()
    if content is not None:
        content = str(content).strip()
    if not title or not content:
        return jsonify({"error": "title and content cannot be empty"}), 400
    if len(title) > 200:
        return jsonify({"error": "title too long"}), 400

    db.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (title, content, note_id),
    )
    db.commit()
    updated = db.execute(
        "SELECT id, title, content FROM notes WHERE id = ?",
        (note_id,),
    ).fetchone()
    return jsonify(row_to_note(updated))


@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id: int):
    db = get_db()
    cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404
    return ("", 204)


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8009, debug=True)
