# Tasks for Repo

Status: completed for self-study Week 4 (see `writeup.md`, `docs/API.md`).

## 1) Enable pre-commit and fix the repo
- [x] Config at `pre-commit-config.yaml` (run: `pre-commit run --all-files -c pre-commit-config.yaml`)
- Install hooks when desired: `pre-commit install -c pre-commit-config.yaml`

## 2) Add search endpoint for notes
- [x] `GET /notes/search/?q=...` case-insensitive (SQLAlchemy `func.lower` + `like`)
- [x] `frontend/app.js` search form
- [x] tests in `backend/tests/test_notes.py`

## 3) Complete action item flow
- [x] `PUT /action-items/{id}/complete`
- [x] UI Complete button + extra 404/validation tests

## 4) Improve extraction logic
- [x] `#tag` parsing in `services/extract.py`
- [x] tests for tags + combined extract
- [x] `POST /notes/{id}/extract`

## 5) Notes CRUD enhancements
- [x] `PUT /notes/{id}` / `DELETE /notes/{id}`
- [x] frontend edit/delete + tests

## 6) Request validation and error handling
- [x] min-length fields in `schemas.py`
- [x] 400/404/422 coverage in tests

## 7) Docs drift check (manual for now)
- [x] `docs/API.md` aligned with OpenAPI
- Automation: `.claude/commands/week4-docs-sync.md`

