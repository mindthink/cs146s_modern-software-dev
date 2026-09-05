"""Yahoo Finance options helpers used by the MCP tools.

Uses the unofficial Yahoo Finance API via ``yfinance`` (no API key).
Yahoo may throttle or block aggressive clients; we retry with short backoff.
"""

from __future__ import annotations

import logging
import math
import time
from typing import Any, Literal

import yfinance as yf

logger = logging.getLogger(__name__)

OptionSide = Literal["call", "put", "both"]

# Compact columns kept for LLM-friendly responses (full Yahoo chain is huge).
_CHAIN_FIELDS = (
    "contractSymbol",
    "strike",
    "lastPrice",
    "bid",
    "ask",
    "volume",
    "openInterest",
    "impliedVolatility",
    "inTheMoney",
)

_MAX_RETRIES = 3
_BACKOFF_SECONDS = (0.5, 1.5, 3.0)


class OptionsError(Exception):
    """User-facing failure fetching or validating options data."""


def _normalize_symbol(symbol: str) -> str:
    cleaned = (symbol or "").strip().upper()
    if not cleaned or not cleaned.replace(".", "").isalnum():
        raise OptionsError(
            f"Invalid symbol {symbol!r}. Use a US ticker like AAPL, MSFT, or BRK.B."
        )
    return cleaned


def _with_retries(label: str, fn):  # type: ignore[no-untyped-def]
    last_exc: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            return fn()
        except OptionsError:
            raise
        except Exception as exc:  # noqa: BLE001 — surface Yahoo/network failures
            last_exc = exc
            logger.warning(
                "%s failed (attempt %s/%s): %s",
                label,
                attempt,
                _MAX_RETRIES,
                exc,
            )
            if attempt >= _MAX_RETRIES:
                break
            time.sleep(_BACKOFF_SECONDS[attempt - 1])
    raise OptionsError(
        f"{label} failed after {_MAX_RETRIES} attempts "
        f"(Yahoo may be rate-limiting or unreachable): {last_exc}"
    )


def _spot_price(ticker: yf.Ticker) -> float | None:
    try:
        price = float(ticker.fast_info.last_price)
        if math.isfinite(price) and price > 0:
            return price
    except Exception:  # noqa: BLE001
        pass
    try:
        info = ticker.info or {}
        for key in ("regularMarketPrice", "currentPrice", "previousClose"):
            value = info.get(key)
            if value is not None:
                price = float(value)
                if math.isfinite(price) and price > 0:
                    return price
    except Exception:  # noqa: BLE001
        pass
    return None


def _row_to_contract(row: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in _CHAIN_FIELDS:
        value = row.get(key)
        if value is None:
            out[key] = None
            continue
        if hasattr(value, "item"):
            try:
                value = value.item()
            except Exception:  # noqa: BLE001
                pass
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            out[key] = None
        elif key == "impliedVolatility" and isinstance(value, (int, float)):
            out[key] = round(float(value), 4)
        else:
            out[key] = value
    return out


def _nearest_strikes(rows: list[dict[str, Any]], spot: float | None, max_rows: int) -> list[dict[str, Any]]:
    if not rows or max_rows <= 0:
        return []
    if spot is None:
        return rows[:max_rows]
    ranked = sorted(rows, key=lambda r: abs(float(r.get("strike") or 0) - spot))
    return ranked[:max_rows]


def get_option_expirations(symbol: str) -> dict[str, Any]:
    """Return available option expiration dates for a US equity symbol."""
    sym = _normalize_symbol(symbol)

    def _fetch() -> dict[str, Any]:
        ticker = yf.Ticker(sym)
        expirations = list(ticker.options or [])
        spot = _spot_price(ticker)
        if not expirations:
            raise OptionsError(
                f"No option expirations found for {sym}. "
                "Confirm it is a US-listed equity with an options market."
            )
        return {
            "symbol": sym,
            "spot": spot,
            "count": len(expirations),
            "expirations": expirations,
            "source": "Yahoo Finance via yfinance (unofficial)",
        }

    return _with_retries(f"get_option_expirations({sym})", _fetch)


def get_option_chain(
    symbol: str,
    expiration: str,
    option_type: OptionSide = "both",
    max_rows: int = 20,
) -> dict[str, Any]:
    """Return a compact option chain slice near the current spot price.

    Full Yahoo chains are large; we keep a small set of fields and truncate to
    contracts nearest ATM so MCP tool responses stay model-friendly.
    """
    sym = _normalize_symbol(symbol)
    expiration = (expiration or "").strip()
    if not expiration:
        raise OptionsError("expiration is required (YYYY-MM-DD from get_option_expirations).")

    side = (option_type or "both").strip().lower()
    if side not in {"call", "put", "both"}:
        raise OptionsError("option_type must be one of: call, put, both.")

    try:
        limit = int(max_rows)
    except (TypeError, ValueError) as exc:
        raise OptionsError("max_rows must be an integer.") from exc
    if limit < 1 or limit > 100:
        raise OptionsError("max_rows must be between 1 and 100.")

    def _fetch() -> dict[str, Any]:
        ticker = yf.Ticker(sym)
        available = list(ticker.options or [])
        if expiration not in available:
            sample = ", ".join(available[:8]) if available else "(none)"
            raise OptionsError(
                f"Expiration {expiration!r} is not available for {sym}. "
                f"Nearby dates: {sample}"
            )

        spot = _spot_price(ticker)
        chain = ticker.option_chain(expiration)
        result: dict[str, Any] = {
            "symbol": sym,
            "expiration": expiration,
            "spot": spot,
            "option_type": side,
            "max_rows": limit,
            "note": "Rows are truncated to strikes nearest ATM; IV is decimal (e.g. 0.25 ≈ 25%).",
            "source": "Yahoo Finance via yfinance (unofficial)",
            "calls": [],
            "puts": [],
        }

        if side in {"call", "both"}:
            call_rows = [_row_to_contract(r) for r in chain.calls.to_dict("records")]
            result["calls"] = _nearest_strikes(call_rows, spot, limit)
            result["calls_available"] = len(call_rows)

        if side in {"put", "both"}:
            put_rows = [_row_to_contract(r) for r in chain.puts.to_dict("records")]
            result["puts"] = _nearest_strikes(put_rows, spot, limit)
            result["puts_available"] = len(put_rows)

        if not result["calls"] and not result["puts"]:
            raise OptionsError(f"Empty option chain for {sym} @ {expiration}.")

        return result

    return _with_retries(f"get_option_chain({sym},{expiration})", _fetch)
