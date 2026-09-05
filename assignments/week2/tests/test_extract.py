import json
import os
from types import SimpleNamespace

import pytest

from ..app.services import extract as extract_module
from ..app.services.extract import (
    LLMExtractionError,
    extract_action_items,
    extract_action_items_llm,
)


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ---------------------------------------------------------------------------
# TODO 2: unit tests for the LLM-powered extractor.
#
# `ollama.chat` is replaced with a fake so these tests are fast, deterministic,
# and do not require a running Ollama server. The fake records the call so we
# can also assert on how the model was invoked (schema, temperature, prompt).
# ---------------------------------------------------------------------------


def _fake_chat(action_items=None, raw_content=None):
    """Build a stand-in for `ollama.chat` returning the given action items.

    Pass `raw_content` to return arbitrary (possibly malformed) model output.
    """
    calls = []

    def chat(**kwargs):
        calls.append(kwargs)
        content = (
            raw_content
            if raw_content is not None
            else json.dumps({"action_items": action_items or []})
        )
        return SimpleNamespace(message=SimpleNamespace(content=content))

    chat.calls = calls
    return chat


def test_llm_extract_bullet_list(monkeypatch):
    fake = _fake_chat(["Set up database", "Implement API extract endpoint", "Write tests"])
    monkeypatch.setattr(extract_module, "chat", fake)

    text = "- [ ] Set up database\n* implement API extract endpoint\n1. Write tests"
    items = extract_action_items_llm(text)

    assert items == ["Set up database", "Implement API extract endpoint", "Write tests"]
    # The raw notes must be forwarded to the model as the user message.
    assert fake.calls[0]["messages"][-1] == {"role": "user", "content": text}


def test_llm_extract_keyword_prefixed_lines(monkeypatch):
    fake = _fake_chat(["Email the vendor", "Schedule a retro"])
    monkeypatch.setattr(extract_module, "chat", fake)

    text = "TODO: email the vendor\nAction: schedule a retro\nWe discussed budgets."
    assert extract_action_items_llm(text) == ["Email the vendor", "Schedule a retro"]


def test_llm_extract_empty_input_skips_model(monkeypatch):
    fake = _fake_chat(["should never be returned"])
    monkeypatch.setattr(extract_module, "chat", fake)

    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   \n\t ") == []
    assert fake.calls == [], "model must not be called for blank input"


def test_llm_extract_no_action_items(monkeypatch):
    monkeypatch.setattr(extract_module, "chat", _fake_chat([]))
    assert extract_action_items_llm("Just a narrative paragraph with no tasks.") == []


def test_llm_extract_uses_structured_output_and_default_model(monkeypatch):
    fake = _fake_chat(["x"])
    monkeypatch.setattr(extract_module, "chat", fake)

    extract_action_items_llm("- x")
    call = fake.calls[0]
    assert call["model"] == extract_module.DEFAULT_OLLAMA_MODEL
    assert call["format"] == extract_module.ACTION_ITEMS_SCHEMA
    assert call["options"]["temperature"] == 0
    assert call["messages"][0]["role"] == "system"


def test_llm_extract_model_override(monkeypatch):
    fake = _fake_chat(["x"])
    monkeypatch.setattr(extract_module, "chat", fake)

    extract_action_items_llm("- x", model="llama3.2:1b")
    assert fake.calls[0]["model"] == "llama3.2:1b"


def test_llm_extract_cleans_and_dedupes(monkeypatch):
    # Even with a schema, a model may echo list markers or repeat items.
    fake = _fake_chat(["- [ ] Ship v1", "  Ship v1 ", "ship V1", "", "   ", "2. Write docs"])
    monkeypatch.setattr(extract_module, "chat", fake)

    assert extract_action_items_llm("notes") == ["Ship v1", "Write docs"]


def test_llm_extract_ignores_non_string_items(monkeypatch):
    fake = _fake_chat(raw_content=json.dumps({"action_items": ["Real task", 42, None, {"a": 1}]}))
    monkeypatch.setattr(extract_module, "chat", fake)

    assert extract_action_items_llm("notes") == ["Real task"]


def test_llm_extract_invalid_json_raises(monkeypatch):
    monkeypatch.setattr(extract_module, "chat", _fake_chat(raw_content="not json at all"))
    with pytest.raises(LLMExtractionError):
        extract_action_items_llm("notes")


def test_llm_extract_wrong_shape_raises(monkeypatch):
    monkeypatch.setattr(extract_module, "chat", _fake_chat(raw_content=json.dumps(["a", "b"])))
    with pytest.raises(LLMExtractionError):
        extract_action_items_llm("notes")

    monkeypatch.setattr(extract_module, "chat", _fake_chat(raw_content=json.dumps({"items": ["a"]})))
    with pytest.raises(LLMExtractionError):
        extract_action_items_llm("notes")


@pytest.mark.skipif(
    os.getenv("RUN_OLLAMA_TESTS") != "1",
    reason="set RUN_OLLAMA_TESTS=1 to run against a live Ollama server",
)
def test_llm_extract_live_ollama():
    """End-to-end check against the real model (slow; opt-in)."""
    text = "- [ ] Set up database\nTODO: write tests\nThe weather was nice."
    items = extract_action_items_llm(text)
    lowered = " ".join(items).lower()
    assert "database" in lowered
    assert "test" in lowered
    assert "weather" not in lowered
