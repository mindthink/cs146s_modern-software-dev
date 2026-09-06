async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

async function loadNotes() {
  const list = document.getElementById("notes");
  list.innerHTML = "";
  const notes = await fetchJSON("/api/notes");
  for (const n of notes) {
    const li = document.createElement("li");
    const title = document.createElement("strong");
    title.textContent = n.title;
    const body = document.createElement("div");
    body.textContent = n.content;
    li.appendChild(title);
    li.appendChild(body);

    const edit = document.createElement("button");
    edit.type = "button";
    edit.textContent = "Edit";
    edit.onclick = async () => {
      const nextTitle = prompt("Title", n.title);
      if (nextTitle === null) return;
      const nextContent = prompt("Content", n.content);
      if (nextContent === null) return;
      await fetchJSON(`/api/notes/${n.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: nextTitle, content: nextContent }),
      });
      loadNotes();
    };
    li.appendChild(edit);

    const del = document.createElement("button");
    del.type = "button";
    del.textContent = "Delete";
    del.onclick = async () => {
      if (!confirm(`Delete #${n.id}?`)) return;
      await fetchJSON(`/api/notes/${n.id}`, { method: "DELETE" });
      loadNotes();
    };
    li.appendChild(del);
    list.appendChild(li);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("note-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    await fetchJSON("/api/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: document.getElementById("note-title").value,
        content: document.getElementById("note-content").value,
      }),
    });
    e.target.reset();
    loadNotes();
  });
  loadNotes();
});
