# Week 4 Write-up

Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **self-study (not enrolled)** \
SUNet ID: **N/A** \
Citations:
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [SubAgents overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Course `assignments/week4/assignment.md` examples (tests / docs-sync slash commands)

This assignment took me about **3** hours to do.


## YOUR RESPONSES
### Automation #1 — `/week4-tests` slash command
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Claude Code best practices emphasize **focused, repeatable slash commands** for verification loops (run tests, summarize failures, suggest next steps) instead of re-prompting the agent with the same Makefile each time. The course example `tests.md` (pytest with `--maxfail=1 -x`, then optional coverage) is the direct template.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** One command to gate Week 4 backend changes.
> **Inputs:** Optional `$ARGUMENTS` (path or `-k` expression).
> **Steps:** `cd assignments/week4` → `pytest -q backend/tests --maxfail=1 -x` → on green, optional coverage → on red, summarize first failure + smallest fix.
> **Outputs:** Pass/fail summary, failure detail, next-step hint.
> **File:** `.claude/commands/week4-tests.md`

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> In Claude Code: `/week4-tests` or `/week4-tests -k search`.
> In Cursor (same workflow by hand or by pasting the command file): from `assignments/week4/`,
> `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x`
> **Expected:** `N passed` or a single truncated failure.
> **Safety:** Does not delete SQLite DB or touch other weeks; prefer fixing one failure at a time.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Remember `PYTHONPATH=.`, cwd, flags, then paste logs back into chat.
> **After:** Invoke `/week4-tests`; agent follows the fixed script and returns a structured summary.

e. How you used the automation to enhance the starter application
> Used the same gate while implementing TASKS: case-insensitive search, note PUT/DELETE, `#tag` extraction + `POST /notes/{id}/extract`, schema validation, and UI wiring. Final run: **10 passed**.


### Automation #2 — Week 4 `CLAUDE.md` + `/week4-docs-sync`
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Best practices recommend a concise project memory (`CLAUDE.md`) for entry points, run commands, and safety rails. The course “docs sync” slash-command example (read OpenAPI → update `API.md` → list deltas) pairs naturally with that guidance so docs do not drift after agent edits. Cursor equivalent: `.cursor/rules/week4-starter.mdc` scoped to `assignments/week4/**`.

b. Design of each automation, including goals, inputs/outputs, steps
> **`assignments/week4/CLAUDE.md`:** layout, `make` targets, TDD-ish endpoint workflow, pre-commit path, safety list.
> **`/week4-docs-sync`:** load OpenAPI (`app.openapi()` or `/openapi.json`) → rewrite `docs/API.md` → report added/removed/changed routes.
> **Files:** `assignments/week4/CLAUDE.md`, `.claude/commands/week4-docs-sync.md`, `.cursor/rules/week4-starter.mdc`

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Claude Code: `/week4-docs-sync` (optional focus in `$ARGUMENTS`).
> Headless OpenAPI peek:
> `cd assignments/week4 && PYTHONPATH=. python -c "from backend.app.main import app; print(sorted(app.openapi()['paths']))"`
> **Expected:** Updated `docs/API.md` + delta summary.
> **Safety:** Only edit `docs/API.md` unless asked; never invent routes not in OpenAPI. Rollback = `git checkout -- assignments/week4/docs/API.md`.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Manually skim routers and hope README matches; easy to miss new extract/search routes.
> **After:** Guidance file keeps agents in the right cwd/tooling; docs-sync regenerates API.md from the live schema.

e. How you used the automation to enhance the starter application
> After adding search/CRUD/extract/validation routes, regenerated `docs/API.md` from OpenAPI and checked route list against routers. Frontend + TASKS backlog updated under the same Week 4 guidance (search UI, edit/delete/extract buttons, complete flow already scaffolded).


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> N/A (two automations completed; Cursor rule is a thin mirror of Automation #2 for this IDE).

b. Design of each automation, including goals, inputs/outputs, steps
> N/A

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> N/A

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

e. How you used the automation to enhance the starter application
> N/A
