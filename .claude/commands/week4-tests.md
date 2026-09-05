---
description: Run Week 4 starter tests (and optional coverage if green)
argument-hint: "[optional path or -k expression]"
---

# Week 4 test runner

You are running the Week 4 starter test workflow.

## Steps

1. `cd` to `assignments/week4` (repo-relative).
2. Run:
   ```bash
   PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x $ARGUMENTS
   ```
   If `$ARGUMENTS` is empty, omit it.
3. If tests **pass**, optionally run coverage:
   ```bash
   PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing
   ```
   Skip coverage if `pytest-cov` is not installed; say so instead of failing the command.
4. If tests **fail**:
   - Summarize the first failure (file, test name, assertion).
   - Suggest the smallest next fix (do not sprawl into unrelated modules).

## Output

- Pass/fail status
- Short failure summary + next steps (or "all green")
- List of tests collected count if available

## Safety

- Do not delete the SQLite DB or modify unrelated weeks.
- Prefer fixing one failing test at a time.
