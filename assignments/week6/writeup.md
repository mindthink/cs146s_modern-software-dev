# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **self-study (not enrolled)** \
SUNet ID: **N/A** \
Citations:
- Semgrep CLI + `--config auto` rule packs
- FastAPI CORSMiddleware docs; SQLAlchemy `text()` bound parameters; httpx docs

This assignment took me about **2** hours to do.


## Brief findings overview
> Ran Semgrep CLI (no cloud login):
> `.venv-semgrep/bin/semgrep scan --config auto assignments/week6`
> Initial scan reported **5 blocking SAST** findings (no secrets/SCA hits in that auto pack run):
> 1. Wildcard CORS (`allow_origins=["*"]`) — `main.py`
> 2. SQL injection via f-string into `sqlalchemy.text` — `notes.py` `/unsafe-search`
> 3. `eval()` on user input — `notes.py` `/debug/eval`
> 4. `subprocess.run(..., shell=True)` — `/debug/run`
> 5. Dynamic `urllib.urlopen` — `/debug/fetch`
>
> Ignored for write-up depth (but also mitigated): weak MD5 debug hash and path-read debug endpoint as intentional “bad demo” leftovers / lower priority than RCE & SQLi.
> After fixes, re-scan with the same command reported **0 Code Findings**. Tests: `cd assignments/week6 && PYTHONPATH=. pytest -q backend/tests` → **3 passed**.

## Fix #1
a. File and line(s)
> `assignments/week6/backend/app/main.py` — CORSMiddleware `allow_origins` (was ~line 24)

b. Rule/category Semgrep flagged
> `python.fastapi.security.wildcard-cors.wildcard-cors` (SAST)

c. Brief risk description
> Reflecting `Access-Control-Allow-Origin: *` with credentials enabled lets any website’s browser JS call the API with the user’s cookies/session context (when applicable), enabling CSRF-style data theft or abuse.

d. Your change (short code diff or explanation, AI coding tool usage)
> Replaced `allow_origins=["*"]` with an explicit allowlist for local frontend origins (`http://127.0.0.1:8000`, `http://localhost:8000`) and narrowed `allow_methods`. Implemented with Cursor agent + Semgrep CLI triage.

e. Why this mitigates the issue
> Browsers only attach CORS trust to listed origins; a random evil site can no longer read API responses cross-origin under the app’s credentialed policy.

## Fix #2
a. File and line(s)
> `assignments/week6/backend/app/routers/notes.py` — `unsafe_search` (was f-string SQL ~71–79)

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text` / SQLi via string-built SQL (SAST)

c. Brief risk description
> Interpolating `q` into SQL (`LIKE '%{q}%'`) lets an attacker alter the query (classic SQL injection), reading or modifying data beyond intended search.

d. Your change (short code diff or explanation, AI coding tool usage)
> Kept `text()` for the legacy route but switched to a bound parameter:
> `WHERE title LIKE :pattern OR content LIKE :pattern` with `{"pattern": f"%{q}%"}`.
> Also moved `/unsafe-search` **above** `/{note_id}` so the path is not swallowed by the id route.

e. Why this mitigates the issue
> The DB driver sends `q` as data, not as SQL syntax, so metacharacters cannot break out of the `LIKE` value.

## Fix #3
a. File and line(s)
> `assignments/week6/backend/app/routers/notes.py` — `debug_eval` (was `eval(expr)` ~104)

b. Rule/category Semgrep flagged
> `python.lang.security.audit.eval-detected.eval-detected` (SAST)

c. Brief risk description
> `eval` on a query string is remote code execution: an attacker can run arbitrary Python in the server process.

d. Your change (short code diff or explanation, AI coding tool usage)
> Removed `eval` entirely; the endpoint now returns HTTP 400 explaining that dynamic eval is disabled.
> (Also hardened nearby demos: `subprocess` with `shell=False` + argv split; `urlopen` replaced with `httpx` + http(s)-only URL check — confirmed cleared on re-scan.)

e. Why this mitigates the issue
> No user-controlled string is executed as code; the dangerous sink is gone, so Semgrep no longer flags the path and RCE via this route is closed.
