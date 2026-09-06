# Week 8 Write-up

## Submission Details

Name: **self-study (not enrolled)** \
SUNet ID: **N/A** \
Citations: FastAPI / Flask / SQLAlchemy docs; course week8 assignment scope

This assignment took me about **2** hours to do (self-study: **two** stacks — A + C; Bolt/version B skipped).


## App Concept
```
A minimal Notes app: create / list / edit / delete notes with persistent
SQLite storage, basic validation, and a simple browser UI. Same product,
two backends for stack comparison (self-study; no third Bolt version).
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: fastapi-notes
AI app generation platform: none (hand-written with Cursor)
Tech Stack: FastAPI + SQLAlchemy + SQLite + vanilla JS
Persistence: SQLite file data/app.db
Frameworks/Libraries Used: fastapi, uvicorn, sqlalchemy, pydantic
Screenshots: N/A — run README and open http://127.0.0.1:8008

REFLECTIONS:
===============
a. Issues: keeping frontend paths (/static) aligned with FastAPI StaticFiles;
   solved by mounting frontend/ and returning index.html from /.

b. Prompting: asked Cursor for a compact single-file API + shared CRUD UI;
   worked well; little iteration needed.

c. Time-to-first-run: ~10–15 min including README; feature-complete CRUD
   in one pass.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: flask-notes
AI app generation platform: none (hand-written with Cursor)
Tech Stack: Flask (Python non-JS backend) + sqlite3 + vanilla JS
Persistence: SQLite file data/app.db
Frameworks/Libraries Used: flask, stdlib sqlite3
Screenshots: N/A — run README and open http://127.0.0.1:8009

REFLECTIONS:
===============
a. Issues: manual JSON validation vs Pydantic — more boilerplate but clearer
   for learning; used bound SQL parameters from the start (week6 lesson).

b. Prompting: reuse same API shape and UI as FastAPI version for fair
   comparison; accent color changed so versions are visually distinct.

c. Time-to-first-run: ~15–20 min including venv + requirements.txt;
   API parity with Version A by design.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: (skipped — self-study)
AI app generation platform: bolt.new not used
Tech Stack: N/A
Persistence: N/A
Frameworks/Libraries Used: N/A

REFLECTIONS:
===============
a–c. Self-study scope was Versions A + C only (FastAPI vs Flask).
     Full course requires a third stack + Bolt; deferred.
```
