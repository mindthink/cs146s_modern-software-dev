from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemCreated,
    ActionItemOut,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import LLMExtractionError, extract_action_items, extract_action_items_llm

# Refactor (TODO 3): typed request/response schemas instead of Dict[str, Any].
router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)

    items = extract_action_items(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemCreated(id=i, text=t) for i, t in zip(ids, items)],
    )


# TODO 4: LLM-powered extract endpoint (same request/response shape as /extract).
@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)

    try:
        items = extract_action_items_llm(payload.text)
    except LLMExtractionError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemCreated(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemOut])
def list_all(note_id: Optional[int] = None) -> list[ActionItemOut]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemOut(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    updated = db.mark_action_item_done(action_item_id, payload.done)
    if not updated:
        raise HTTPException(status_code=404, detail="action item not found")
    return MarkDoneResponse(id=action_item_id, done=payload.done)
