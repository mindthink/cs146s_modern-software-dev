def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_notes_case_insensitive(client):
    client.post("/notes/", json={"title": "Alpha", "content": "FindMeLater"})
    r = client.get("/notes/search/", params={"q": "findmelater"})
    assert r.status_code == 200
    assert any(n["content"] == "FindMeLater" for n in r.json())


def test_update_and_delete_note(client):
    r = client.post("/notes/", json={"title": "Old", "content": "body"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "New", "content": "updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["content"] == "updated"

    r = client.put(f"/notes/{note_id}", json={})
    assert r.status_code == 400

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_note_validation(client):
    r = client.post("/notes/", json={"title": "", "content": "x"})
    assert r.status_code == 422

    r = client.get("/notes/99999")
    assert r.status_code == 404


def test_extract_from_note(client):
    payload = {
        "title": "Plan #backend",
        "content": "TODO: write tests #qa\nShip it! #release\nJust chat",
    }
    r = client.post("/notes/", json=payload)
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract")
    assert r.status_code == 200, r.text
    body = r.json()
    assert "backend" in body["tags"]
    assert "qa" in body["tags"]
    assert "release" in body["tags"]
    assert len(body["action_items"]) == 2

    r = client.get("/action-items/")
    assert r.status_code == 200
    assert len(r.json()) >= 2
