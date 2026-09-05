from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _dedupe_preserving_order(extracted)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def _dedupe_preserving_order(items: List[str]) -> List[str]:
    """Drop case-insensitive duplicates while keeping first-seen order.

    Shared by the heuristic and LLM extractors so both return the same shape.
    """
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


# ---------------------------------------------------------------------------
# TODO 1: LLM-powered extraction via Ollama
# ---------------------------------------------------------------------------

# Model is configurable through the OLLAMA_MODEL env var (see .env / load_dotenv above).
# Default matches the model pulled locally with `ollama pull mistral-nemo:12b`.
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral-nemo:12b")

# JSON schema passed to Ollama's `format=` parameter so the model is constrained
# to return structured output (https://ollama.com/blog/structured-outputs).
# Wrapping the list in an object is more reliable than a bare top-level array.
ACTION_ITEMS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action_items": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["action_items"],
}

SYSTEM_PROMPT = (
    "You extract action items from free-form meeting notes. "
    "An action item is a concrete task someone needs to do. "
    "Return each action item as a short imperative sentence without bullet "
    "markers, checkbox markers, numbering, or prefixes such as 'TODO:'. "
    "Include tasks assigned to a specific person (e.g. 'Sarah will update the "
    "docs by Friday' -> 'Update the onboarding docs by Friday (Sarah)'). "
    "Ignore narrative sentences, decisions already made, and background context. "
    "Respond with JSON matching the schema {\"action_items\": [string, ...]}. "
    "If there are no action items, return an empty list."
)


class LLMExtractionError(RuntimeError):
    """Raised when the LLM returns output that cannot be parsed into action items."""


def extract_action_items_llm(text: str, model: str | None = None) -> List[str]:
    """Extract action items from `text` using a local Ollama model.

    Unlike `extract_action_items`, which relies on bullet/keyword heuristics,
    this asks an LLM to identify tasks and forces a JSON response via Ollama's
    structured-output support, then normalizes the result the same way the
    heuristic extractor does (strip, drop empties, dedupe).

    Args:
        text: Raw notes to analyze.
        model: Ollama model name; defaults to `OLLAMA_MODEL` env var or
            `mistral-nemo:12b`.

    Returns:
        Ordered, de-duplicated list of action item strings. Empty input yields
        an empty list without calling the model.

    Raises:
        LLMExtractionError: if the model response is not valid JSON in the
            expected shape.
    """
    if not text or not text.strip():
        return []

    response = chat(
        model=model or DEFAULT_OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        format=ACTION_ITEMS_SCHEMA,
        # Deterministic output makes results reproducible and easier to test.
        options={"temperature": 0},
    )

    content = response.message.content or ""
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMExtractionError(f"model returned non-JSON output: {content!r}") from exc

    raw_items = parsed.get("action_items") if isinstance(parsed, dict) else None
    if not isinstance(raw_items, list):
        raise LLMExtractionError(f"model output missing 'action_items' list: {parsed!r}")

    cleaned: List[str] = []
    for item in raw_items:
        if not isinstance(item, str):
            continue
        # Defensive cleanup in case the model still echoes list markers.
        s = BULLET_PREFIX_PATTERN.sub("", item).strip()
        s = s.removeprefix("[ ]").strip()
        s = s.removeprefix("[todo]").strip()
        if s:
            cleaned.append(s)
    return _dedupe_preserving_order(cleaned)
