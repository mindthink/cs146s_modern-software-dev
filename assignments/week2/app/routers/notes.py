from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteOut

# Refactor (TODO 3): typed request/response schemas instead of Dict[str, Any].
router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteOut)
def create_note(payload: NoteCreate) -> NoteOut:
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=500, detail="failed to load created note")
    return NoteOut(id=note["id"], content=note["content"], created_at=note["created_at"])


# TODO 4: list all saved notes (must be declared before /{note_id}).
@router.get("", response_model=list[NoteOut])
def list_all_notes() -> list[NoteOut]:
    rows = db.list_notes()
    return [
        NoteOut(id=r["id"], content=r["content"], created_at=r["created_at"]) for r in rows
    ]


@router.get("/{note_id}", response_model=NoteOut)
def get_single_note(note_id: int) -> NoteOut:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteOut(id=row["id"], content=row["content"], created_at=row["created_at"])
