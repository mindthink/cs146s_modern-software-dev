# Agent Instructions

This repo is a personal CS146S learning workspace:

- `assignments/` — weekly homework
- `notes/` — course notes and reading list

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(optional-scope): <description>

[optional body]
```

### Rules

- Imperative mood; keep the subject concise (≤ 72 chars when practical)
- Do **not** add `Co-authored-by: Cursor` or any Cursor / tool attribution trailers
- Prefer a short body only when the why is not obvious from the subject

### Types

| type | when |
|------|------|
| `feat` | new feature / completed assignment prompt |
| `fix` | bug fix |
| `docs` | README, notes, reading list |
| `refactor` | restructure without behavior change |
| `chore` | tooling, deps, config |
| `test` | add or update tests |
| `style` | formatting only |

### Scopes (optional)

`week1`, `week2`, … `notes`, `repo`

### Examples

```text
feat(week1): add chain-of-thought system prompt
docs(notes): add prompting guide to reading list
refactor(repo): move weeks under assignments/
chore(repo): add agent instruction files
```
