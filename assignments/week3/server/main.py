"""STDIO MCP server exposing US equity options tools via Yahoo Finance.

Logging goes to stderr only — stdout is reserved for the MCP JSON-RPC transport.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Literal

from mcp.server.mcpserver import MCPServer

# Alias helpers so @mcp.tool names do not shadow the options.py imports.
try:
    from .options import OptionsError
    from .options import get_option_chain as fetch_option_chain
    from .options import get_option_expirations as fetch_option_expirations
except ImportError:  # script entry: poetry run python .../server/main.py
    from options import OptionsError
    from options import get_option_chain as fetch_option_chain
    from options import get_option_expirations as fetch_option_expirations

# STDIO servers must log to stderr; stdout is the protocol stream.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("us-options-mcp")

# mcp 2.x: FastMCP was renamed to MCPServer.
mcp = MCPServer(
    "us-options",
    title="US Equity Options",
    description="Lookup US equity option expirations and compact near-ATM chains via Yahoo Finance.",
    instructions=(
        "Use get_option_expirations first to discover YYYY-MM-DD dates, "
        "then get_option_chain for a compact near-ATM slice. Data comes from "
        "Yahoo Finance through yfinance (unofficial; may rate-limit)."
    ),
    version="0.1.0",
)


def _json(payload: object) -> str:
    """Serialize tool results as JSON for the MCP client."""
    return json.dumps(payload, indent=2, default=str)


@mcp.tool()
def get_option_expirations(symbol: str) -> str:
    """List available option expiration dates for a US equity ticker.

    Args:
        symbol: US ticker symbol, e.g. AAPL, MSFT, TSLA, BRK.B
    """
    try:
        data = fetch_option_expirations(symbol)
        logger.info("expirations %s -> %s dates", data["symbol"], data["count"])
        return _json(data)
    except OptionsError as exc:
        # Expected failures (bad ticker, no options) → structured error, keep server up.
        logger.warning("get_option_expirations error: %s", exc)
        return _json({"error": str(exc)})
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected get_option_expirations failure")
        return _json({"error": f"Unexpected failure: {exc}"})


@mcp.tool()
def get_option_chain(
    symbol: str,
    expiration: str,
    option_type: Literal["call", "put", "both"] = "both",
    max_rows: int = 20,
) -> str:
    """Fetch a compact option chain near the current spot (ATM-focused).

    Prefer calling get_option_expirations first so expiration is a real date.

    Args:
        symbol: US ticker symbol, e.g. AAPL
        expiration: Expiration date YYYY-MM-DD from get_option_expirations
        option_type: Which side to return: call, put, or both
        max_rows: Max contracts per side (1-100), nearest to spot first
    """
    try:
        data = fetch_option_chain(
            symbol=symbol,
            expiration=expiration,
            option_type=option_type,
            max_rows=max_rows,
        )
        logger.info(
            "chain %s %s type=%s calls=%s puts=%s",
            data["symbol"],
            data["expiration"],
            data["option_type"],
            len(data.get("calls") or []),
            len(data.get("puts") or []),
        )
        return _json(data)
    except OptionsError as exc:
        logger.warning("get_option_chain error: %s", exc)
        return _json({"error": str(exc)})
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected get_option_chain failure")
        return _json({"error": f"Unexpected failure: {exc}"})


def main() -> None:
    """Run the MCP server over STDIO (protocol on stdin/stdout, logs on stderr)."""
    logger.info("starting us-options MCP server (stdio)")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
