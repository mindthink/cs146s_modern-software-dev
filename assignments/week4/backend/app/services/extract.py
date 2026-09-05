"""Heuristic extraction of action items and #tags from free-form note text."""

from __future__ import annotations

import re

_TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_-]+)")


def extract_tags(text: str) -> list[str]:
    """Return unique hashtags in appearance order (without the leading #)."""
    seen: set[str] = set()
    tags: list[str] = []
    for match in _TAG_RE.finditer(text or ""):
        tag = match.group(1).lower()
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def extract_action_items(text: str) -> list[str]:
    """Return actionable lines (TODO: … or lines ending with !)."""
    lines = [line.strip("- ").strip() for line in (text or "").splitlines() if line.strip()]
    items: list[str] = []
    for line in lines:
        # Drop trailing tags for cleaner action text while keeping the verb phrase.
        cleaned = _TAG_RE.sub("", line).strip()
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" -")
        if not cleaned:
            continue
        if cleaned.endswith("!") or cleaned.lower().startswith("todo:"):
            items.append(cleaned)
    return items


def extract_note(text: str) -> dict[str, list[str]]:
    """Combined extraction used by the optional extract API."""
    return {"action_items": extract_action_items(text), "tags": extract_tags(text)}
