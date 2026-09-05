from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import ExtractResult, NoteCreate, NoteRead, NoteUpdate
from ..services.extract import extract_note

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)) -> list[NoteRead]:
    rows = db.execute(select(Note)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=list[NoteRead])
def search_notes(q: Optional[str] = None, db: Session = Depends(get_db)) -> list[NoteRead]:
    """Case-insensitive search over title and content."""
    if not q or not q.strip():
        rows = db.execute(select(Note)).scalars().all()
    else:
        needle = f"%{q.strip().lower()}%"
        rows = (
            db.execute(
                select(Note).where(
                    or_(
                        func.lower(Note.title).like(needle),
                        func.lower(Note.content).like(needle),
                    )
                )
            )
            .scalars()
            .all()
        )
    return [NoteRead.model_validate(row) for row in rows]


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=400, detail="Provide title and/or content to update")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()


@router.post("/{note_id}/extract", response_model=ExtractResult)
def extract_note_action_items(note_id: int, db: Session = Depends(get_db)) -> ExtractResult:
    """Parse TODOs / bang-lines and #tags; persist new action items."""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    parsed = extract_note(f"{note.title}\n{note.content}")
    created = []
    for description in parsed["action_items"]:
        item = ActionItem(description=description, completed=False)
        db.add(item)
        db.flush()
        db.refresh(item)
        created.append(item)

    return ExtractResult(
        note_id=note.id,
        tags=parsed["tags"],
        action_items=created,
    )
