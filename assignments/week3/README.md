# Week 3 — US Equity Options MCP Server

STDIO MCP server that wraps **Yahoo Finance equity options** (via [`yfinance`](https://github.com/ranaroussi/yfinance)). Not the official weather quickstart.

## What it does

| Tool | Purpose |
|------|---------|
| `get_option_expirations` | List available option expiration dates + spot |
| `get_option_chain` | Compact near-ATM call/put chain for one expiration |

Upstream data: Yahoo Finance option chain endpoints (unofficial; **no API key**). Yahoo can throttle; the server retries with short backoff and returns JSON errors instead of crashing.

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- Network access to Yahoo Finance

From the repo root:

```bash
poetry install
```

Dependencies used here: `mcp[cli]`, `yfinance` (already in `pyproject.toml`).

## Run locally (STDIO)

```bash
# from repo root
poetry run python assignments/week3/server/main.py
```

The process speaks MCP over **stdin/stdout**. Logs go to **stderr** only.

### Optional smoke check (helpers only)

```bash
cd assignments/week3/server
poetry run python -c "from options import get_option_expirations as g; print(g('AAPL')['expirations'][:3])"
```

## Configure Cursor (local MCP)

Repo → Settings → MCP → add a server (or edit `~/.cursor/mcp.json`):

Prefer an absolute venv Python path (Cursor may ignore `cwd` for Poetry):

```json
{
  "mcpServers": {
    "us-options": {
      "command": "/ABSOLUTE/PATH/TO/modern-software-dev-assignments/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/modern-software-dev-assignments/assignments/week3/server/main.py"
      ]
    }
  }
}
```

Save, then use MCP panel **Restart** (or reload the window). Confirm tools `get_option_expirations` and `get_option_chain` appear.

### Claude Desktop (same idea)

Edit Claude Desktop config and point `command`/`args`/`cwd` the same way as above.

## Example invocation flow

1. In Cursor chat: *“Use the us-options MCP tools to list AAPL option expirations.”*
2. Client calls `get_option_expirations` with `symbol="AAPL"`.
3. Follow up: *“Show a compact call chain for the nearest expiration, 8 rows.”*
4. Client calls `get_option_chain` with that `expiration`, `option_type="call"`, `max_rows=8`.

### Example outputs (shape)

`get_option_expirations("AAPL")`:

```json
{
  "symbol": "AAPL",
  "spot": 320.0,
  "count": 20,
  "expirations": ["2026-09-09", "2026-09-11", "..."],
  "source": "Yahoo Finance via yfinance (unofficial)"
}
```

`get_option_chain("AAPL", "2026-09-09", "both", 3)` — truncated near ATM:

```json
{
  "symbol": "AAPL",
  "expiration": "2026-09-09",
  "spot": 320.0,
  "option_type": "both",
  "calls": [
    {
      "contractSymbol": "AAPL260909C00320000",
      "strike": 320.0,
      "lastPrice": 4.2,
      "bid": 4.1,
      "ask": 4.3,
      "volume": 1200,
      "openInterest": 5000,
      "impliedVolatility": 0.28,
      "inTheMoney": false
    }
  ],
  "puts": [],
  "note": "Rows are truncated to strikes nearest ATM; IV is decimal (e.g. 0.25 ≈ 25%)."
}
```

Errors return `{"error": "..."}` (invalid ticker, bad expiration, empty chain, Yahoo failures).

## Tool reference

### `get_option_expirations`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | US ticker (`AAPL`, `BRK.B`, …) |

**Behavior:** Validates symbol, fetches Yahoo option dates + spot, retries on transient failures.

### `get_option_chain`

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `symbol` | string | yes | — | US ticker |
| `expiration` | string | yes | — | `YYYY-MM-DD` from expirations tool |
| `option_type` | string | no | `both` | `call` \| `put` \| `both` |
| `max_rows` | int | no | `20` | 1–100 contracts per side, nearest ATM |

**Behavior:** Rejects unknown expirations with nearby date hints; keeps a small field set; truncates to ATM neighborhood so responses stay small.

## Layout

```text
assignments/week3/
  assignment.md
  README.md
  server/
    __init__.py
    main.py      # MCP entry (stdio)
    options.py   # yfinance helpers + retries
```

## Notes / caveats

- Yahoo Finance is unofficial via `yfinance` — no SLA; treat data as educational.
- Do not spam tools in a tight loop; backoff already helps, but be polite.
- STDIO only for this submission (HTTP/auth left as optional future work).
