"""Pydantic API contracts for the Week 2 Action Item Extractor.

Refactor (TODO 3): replace ad-hoc Dict[str, Any] payloads with typed schemas.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)

    @field_validator("content")
    @classmethod
    def strip_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("content is required")
        return cleaned


class NoteOut(BaseModel):
    id: int
    content: str
    created_at: str


# ---------------------------------------------------------------------------
# Action items
# ---------------------------------------------------------------------------


class ExtractRequest(BaseModel):
    """Body for POST /action-items/extract (matches the existing frontend)."""

    text: str = Field(..., min_length=1)
    save_note: bool = False

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text is required")
        return cleaned


class ActionItemCreated(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int] = None
    items: list[ActionItemCreated]


class ActionItemOut(BaseModel):
    id: int
    note_id: Optional[int] = None
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool
