from backend.app.services.extract import extract_action_items, extract_note, extract_tags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_tags_and_combined():
    text = "TODO: fix login #Auth #backend\nShip it! #release\n#auth again"
    assert extract_tags(text) == ["auth", "backend", "release"]
    result = extract_note(text)
    assert result["tags"] == ["auth", "backend", "release"]
    assert "TODO: fix login" in result["action_items"]
    assert "Ship it!" in result["action_items"]
