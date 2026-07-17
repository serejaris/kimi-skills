"""
Reusable accounting helpers for pure-Python backtests.

These helpers cover cash equity / ETF accounting for long-only, short, and
simple margin-style backtests. They are intentionally small: use them to avoid
rewriting lot-level, average-cost, and explicit-liability logic in every
generated strategy script.
"""

from __future__ import annotations

import math
from typing import Any


_BUY_LOT_RESERVED_KEYS = frozenset(
    {
        "lot_id",
        "entry_date",
        "entry_price",
        "size",
        "entry_bar",
        "entry_notional",
        "entry_fee",
        "symbol",
        "margin_borrowed",
    }
)

_SHORT_LOT_RESERVED_KEYS = frozenset(
    {
        "lot_id",
        "side",
        "entry_date",
        "entry_price",
        "size",
        "entry_bar",
        "entry_notional",
        "entry_fee",
        "symbol",
        "margin_rate",
        "initial_margin",
    }
)


def buy_lot(
    cash: float,
    *,
    lot_id: str,
    date: str,
    price: float,
    size: int,
    entry_bar: int,
    buy_commission: float = 0.0,
    symbol: str = "",
    **extra: Any,
) -> tuple[float, dict[str, Any]]:
    """Buy one independent lot and deduct cash including entry fee.

    ``size`` is cast to ``int`` before any cash math so a fractional caller
    cannot deduct cash for shares the lot does not actually hold. ``**extra``
    fields are merged into the returned lot dict but are forbidden from
    overwriting the core accounting fields produced by this helper.
    """
    _require_positive_price(price)
    size = int(size)
    _require_positive_size(size)
    clobbered = _BUY_LOT_RESERVED_KEYS & set(extra)
    if clobbered:
        raise ValueError(
            "buy_lot **extra cannot override reserved lot fields: "
            f"{sorted(clobbered)}"
        )
    entry_notional = size * price
    entry_fee = entry_notional * buy_commission
    cost = entry_notional + entry_fee
    if cost > cash + 1e-9:
        raise ValueError(f"insufficient cash for lot buy: cost={cost}, cash={cash}")

    lot = {
        "lot_id": lot_id,
        "entry_date": date,
        "entry_price": float(price),
        "size": size,
        "entry_bar": int(entry_bar),
        "entry_notional": entry_notional,
        "entry_fee": entry_fee,
        "symbol": symbol,
    }
    lot.update(extra)
    return cash - cost, lot


def buy_lot_with_margin(
    cash: float,
    liabilities: float,
    *,
    lot_id: str,
    date: str,
    price: float,
    size: int,
    entry_bar: int,
    buy_commission: float = 0.0,
    symbol: str = "",
    max_liabilities: float | None = None,
    **extra: Any,
) -> tuple[float, float, dict[str, Any]]:
    """Buy one long lot and borrow any cash shortfall into liabilities.

    This is a small cash-loan helper, not a full broker margin engine. It does
    not enforce maintenance margin or liquidation thresholds; use
    ``compute_required_margin`` and ``check_margin_requirement`` for checks.
    Returns (new_cash, new_liabilities, lot).
    """
    _require_positive_price(price)
    size = int(size)
    _require_positive_size(size)
    _require_non_negative(cash, "cash")
    _require_non_negative(liabilities, "liabilities")
    if max_liabilities is not None:
        _require_non_negative(max_liabilities, "max_liabilities")
    clobbered = _BUY_LOT_RESERVED_KEYS & set(extra)
    if clobbered:
        raise ValueError(
            "buy_lot_with_margin **extra cannot override reserved lot fields: "
            f"{sorted(clobbered)}"
        )

    entry_notional = size * price
    entry_fee = entry_notional * buy_commission
    cost = entry_notional + entry_fee
    cash = float(cash)
    borrowed = max(0.0, cost - cash)
    new_liabilities = float(liabilities) + borrowed
    if max_liabilities is not None and new_liabilities > max_liabilities + 1e-9:
        raise ValueError(
            "margin buy would exceed max_liabilities: "
            f"new_liabilities={new_liabilities}, max_liabilities={max_liabilities}"
        )

    lot = {
        "lot_id": lot_id,
        "entry_date": date,
        "entry_price": float(price),
        "size": size,
        "entry_bar": int(entry_bar),
        "entry_notional": entry_notional,
        "entry_fee": entry_fee,
        "symbol": symbol,
        "margin_borrowed": borrowed,
    }
    lot.update(extra)
    return max(0.0, cash - cost), new_liabilities, lot


def short_lot(
    cash: float,
    *,
    lot_id: str,
    date: str,
    price: float,
    size: int,
    entry_bar: int,
    short_commission: float = 0.0,
    margin_rate: float = 0.5,
    symbol: str = "",
    **extra: Any,
) -> tuple[float, dict[str, Any]]:
    """Open one independent short lot.

    Opening a short increases cash by sale proceeds net of entry commission.
    ``margin_rate`` is stored as metadata and used by margin helpers; no broker
    margin rule is enforced here.
    """
    _require_positive_price(price)
    size = int(size)
    _require_positive_size(size)
    _require_non_negative(short_commission, "short_commission")
    _require_non_negative(margin_rate, "margin_rate")
    clobbered = _SHORT_LOT_RESERVED_KEYS & set(extra)
    if clobbered:
        raise ValueError(
            "short_lot **extra cannot override reserved lot fields: "
            f"{sorted(clobbered)}"
        )

    entry_notional = size * price
    entry_fee = entry_notional * short_commission
    initial_margin = entry_notional * margin_rate
    lot = {
        "lot_id": lot_id,
        "side": "short",
        "entry_date": date,
        "entry_price": float(price),
        "size": size,
        "entry_bar": int(entry_bar),
        "entry_notional": entry_notional,
        "entry_fee": entry_fee,
        "symbol": symbol,
        "margin_rate": float(margin_rate),
        "initial_margin": initial_margin,
    }
    lot.update(extra)
    return float(cash) + entry_notional - entry_fee, lot


def close_lot(
    lot: dict[str, Any],
    *,
    date: str,
    price: float,
    exit_bar: int | None = None,
    close_size: int | None = None,
    sell_commission: float = 0.0,
    sell_tax: float = 0.0,
    symbol: str | None = None,
    trade_group_id: str | None = None,
) -> tuple[float, dict[str, Any], dict[str, Any] | None]:
    """Close all or part of one lot.

    Returns (cash_proceeds, trade_record, remaining_lot_or_None).
    ``pnl`` and ``pnl_pct`` are net of allocated entry fee and exit fee.
    """
    _require_positive_price(price)
    current_size = int(lot.get("size") or 0)
    _require_positive_size(current_size)
    size = current_size if close_size is None else int(close_size)
    _require_positive_size(size)
    if size > current_size:
        raise ValueError(f"close_size={size} exceeds lot size={current_size}")

    entry_price = float(lot["entry_price"])
    entry_notional = size * entry_price
    current_entry_fee = float(lot.get("entry_fee") or 0.0)
    entry_fee = current_entry_fee * size / current_size
    exit_notional = size * price
    exit_fee = exit_notional * (sell_commission + sell_tax)
    fees = entry_fee + exit_fee
    gross_pnl = exit_notional - entry_notional
    pnl = gross_pnl - fees
    pnl_pct_basis = entry_notional + entry_fee
    pnl_pct = pnl / pnl_pct_basis * 100.0 if pnl_pct_basis else 0.0
    holding_bars = (
        int(exit_bar) - int(lot["entry_bar"])
        if exit_bar is not None and lot.get("entry_bar") is not None
        else None
    )

    trade = {
        "lot_id": lot.get("lot_id"),
        "trade_group_id": trade_group_id,
        "entry_date": lot.get("entry_date"),
        "exit_date": date,
        "side": "long",
        "size": size,
        "entry_price": entry_price,
        "exit_price": float(price),
        "entry_notional": entry_notional,
        "exit_notional": exit_notional,
        "entry_fee": entry_fee,
        "exit_fee": exit_fee,
        "fees": fees,
        "gross_pnl": gross_pnl,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "pnl_pct_basis": pnl_pct_basis,
        "holding_bars": holding_bars,
        "symbol": symbol if symbol is not None else lot.get("symbol", ""),
        "symbol_name": lot.get("symbol_name", ""),
    }

    remaining_size = current_size - size
    if remaining_size <= 0:
        remaining_lot = None
    else:
        remaining_lot = dict(lot)
        remaining_lot["size"] = remaining_size
        remaining_lot["entry_fee"] = current_entry_fee - entry_fee
        remaining_lot["entry_notional"] = remaining_size * entry_price

    proceeds = exit_notional - exit_fee
    return proceeds, trade, remaining_lot


def close_lots_fifo(
    open_lots: list[dict[str, Any]],
    *,
    sell_size: int,
    date: str,
    price: float,
    exit_bar: int,
    sell_commission: float = 0.0,
    sell_tax: float = 0.0,
    symbol: str = "",
    trade_group_id: str | None = None,
    t_plus_1: bool = False,
) -> tuple[float, list[dict[str, Any]], list[dict[str, Any]], int]:
    """Close lots by FIFO.

    Returns (cash_proceeds, closed_trades, remaining_lots, unfilled_size).
    If ``t_plus_1`` is true, lots bought on ``exit_bar`` are skipped.
    When ``symbol`` is non-empty, lots whose ``lot["symbol"]`` does not match are
    kept untouched in ``remaining_lots`` — the helper closes only matching lots.
    When ``symbol`` is empty and ``open_lots`` contains multiple distinct symbols,
    the call hard-fails to prevent silently selling the wrong lots.
    """
    _require_positive_size(sell_size)

    if not symbol:
        distinct_symbols = {
            str(lot.get("symbol", ""))
            for lot in open_lots
            if int(lot.get("size") or 0) > 0
        }
        if len(distinct_symbols) > 1:
            raise ValueError(
                "open_lots contains multiple symbols but no symbol filter was "
                "passed; either pass symbol=... or split open_lots by symbol "
                f"before calling close_lots_fifo (found: {sorted(distinct_symbols)})"
            )

    proceeds_total = 0.0
    trades: list[dict[str, Any]] = []
    remaining_lots: list[dict[str, Any]] = []
    remaining_to_sell = int(sell_size)

    for lot in open_lots:
        lot_size = int(lot.get("size") or 0)
        if lot_size <= 0:
            continue
        if symbol and str(lot.get("symbol", "")) != symbol:
            remaining_lots.append(dict(lot))
            continue
        if remaining_to_sell <= 0:
            remaining_lots.append(dict(lot))
            continue
        if t_plus_1 and exit_bar <= int(lot.get("entry_bar", -1)):
            remaining_lots.append(dict(lot))
            continue

        close_size = min(lot_size, remaining_to_sell)
        proceeds, trade, remaining_lot = close_lot(
            lot,
            date=date,
            price=price,
            exit_bar=exit_bar,
            close_size=close_size,
            sell_commission=sell_commission,
            sell_tax=sell_tax,
            symbol=symbol or lot.get("symbol", ""),
            trade_group_id=trade_group_id,
        )
        proceeds_total += proceeds
        trades.append(trade)
        remaining_to_sell -= close_size
        if remaining_lot is not None:
            remaining_lots.append(remaining_lot)

    return proceeds_total, trades, remaining_lots, remaining_to_sell


def cover_short_lot(
    lot: dict[str, Any],
    *,
    date: str,
    price: float,
    exit_bar: int | None = None,
    cover_size: int | None = None,
    cover_commission: float = 0.0,
    borrow_fee: float = 0.0,
    symbol: str | None = None,
    trade_group_id: str | None = None,
) -> tuple[float, dict[str, Any], dict[str, Any] | None]:
    """Cover all or part of one short lot.

    Returns (cash_delta, trade_record, remaining_lot_or_None). ``cash_delta``
    is usually negative because covering buys back shares and pays fees.
    """
    _require_positive_price(price)
    _require_non_negative(cover_commission, "cover_commission")
    _require_non_negative(borrow_fee, "borrow_fee")
    current_size = int(lot.get("size") or 0)
    _require_positive_size(current_size)
    size = current_size if cover_size is None else int(cover_size)
    _require_positive_size(size)
    if size > current_size:
        raise ValueError(f"cover_size={size} exceeds short lot size={current_size}")

    entry_price = float(lot["entry_price"])
    entry_notional = size * entry_price
    current_entry_fee = float(lot.get("entry_fee") or 0.0)
    entry_fee = current_entry_fee * size / current_size
    exit_notional = size * price
    exit_fee = exit_notional * cover_commission
    fees = entry_fee + exit_fee + borrow_fee
    gross_pnl = entry_notional - exit_notional
    pnl = gross_pnl - fees
    pnl_pct_basis = entry_notional + entry_fee
    pnl_pct = pnl / pnl_pct_basis * 100.0 if pnl_pct_basis else 0.0
    margin_rate = float(lot.get("margin_rate") or 0.0)
    margin_required = entry_notional * margin_rate
    return_on_margin_pct = (
        pnl / margin_required * 100.0 if margin_required > 0 else None
    )
    holding_bars = (
        int(exit_bar) - int(lot["entry_bar"])
        if exit_bar is not None and lot.get("entry_bar") is not None
        else None
    )

    trade = {
        "lot_id": lot.get("lot_id"),
        "trade_group_id": trade_group_id,
        "entry_date": lot.get("entry_date"),
        "exit_date": date,
        "side": "short",
        "size": size,
        "entry_price": entry_price,
        "exit_price": float(price),
        "entry_notional": entry_notional,
        "exit_notional": exit_notional,
        "entry_fee": entry_fee,
        "exit_fee": exit_fee,
        "borrow_fee": borrow_fee,
        "fees": fees,
        "gross_pnl": gross_pnl,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "pnl_pct_basis": pnl_pct_basis,
        "margin_required": margin_required,
        "return_on_margin_pct": return_on_margin_pct,
        "holding_bars": holding_bars,
        "symbol": symbol if symbol is not None else lot.get("symbol", ""),
        "symbol_name": lot.get("symbol_name", ""),
    }

    remaining_size = current_size - size
    if remaining_size <= 0:
        remaining_lot = None
    else:
        remaining_lot = dict(lot)
        remaining_lot["size"] = remaining_size
        remaining_lot["entry_fee"] = current_entry_fee - entry_fee
        remaining_lot["entry_notional"] = remaining_size * entry_price
        remaining_lot["initial_margin"] = remaining_size * entry_price * margin_rate

    cash_delta = -(exit_notional + exit_fee + borrow_fee)
    return cash_delta, trade, remaining_lot


def cover_short_lots_fifo(
    open_short_lots: list[dict[str, Any]],
    *,
    cover_size: int,
    date: str,
    price: float,
    exit_bar: int,
    cover_commission: float = 0.0,
    borrow_fee: float = 0.0,
    symbol: str = "",
    trade_group_id: str | None = None,
    t_plus_1: bool = False,
) -> tuple[float, list[dict[str, Any]], list[dict[str, Any]], int]:
    """Cover short lots by FIFO.

    Returns (cash_delta, closed_trades, remaining_lots, unfilled_size).
    ``borrow_fee`` is an absolute amount for this cover order and is allocated
    across covered lots by covered size.
    """
    _require_positive_size(cover_size)
    _require_non_negative(borrow_fee, "borrow_fee")

    if not symbol:
        distinct_symbols = {
            str(lot.get("symbol", ""))
            for lot in open_short_lots
            if int(lot.get("size") or 0) > 0
        }
        if len(distinct_symbols) > 1:
            raise ValueError(
                "open_short_lots contains multiple symbols but no symbol filter "
                "was passed; either pass symbol=... or split short lots by symbol "
                f"before calling cover_short_lots_fifo (found: {sorted(distinct_symbols)})"
            )

    cash_delta_total = 0.0
    trades: list[dict[str, Any]] = []
    remaining_lots: list[dict[str, Any]] = []
    requested_size = int(cover_size)
    remaining_to_cover = requested_size

    for lot in open_short_lots:
        lot_size = int(lot.get("size") or 0)
        if lot_size <= 0:
            continue
        if symbol and str(lot.get("symbol", "")) != symbol:
            remaining_lots.append(dict(lot))
            continue
        if remaining_to_cover <= 0:
            remaining_lots.append(dict(lot))
            continue
        if t_plus_1 and exit_bar <= int(lot.get("entry_bar", -1)):
            remaining_lots.append(dict(lot))
            continue

        close_size = min(lot_size, remaining_to_cover)
        allocated_borrow_fee = borrow_fee * close_size / requested_size
        cash_delta, trade, remaining_lot = cover_short_lot(
            lot,
            date=date,
            price=price,
            exit_bar=exit_bar,
            cover_size=close_size,
            cover_commission=cover_commission,
            borrow_fee=allocated_borrow_fee,
            symbol=symbol or lot.get("symbol", ""),
            trade_group_id=trade_group_id,
        )
        cash_delta_total += cash_delta
        trades.append(trade)
        remaining_to_cover -= close_size
        if remaining_lot is not None:
            remaining_lots.append(remaining_lot)

    return cash_delta_total, trades, remaining_lots, remaining_to_cover


def compute_lot_equity(cash: float, open_lots: list[dict[str, Any]], close_price: float) -> float:
    """Mark lot-level long-only equity to market."""
    _require_positive_price(close_price)
    return float(cash) + sum(int(lot.get("size") or 0) * close_price for lot in open_lots)


def buy_average_cost(
    cash: float,
    *,
    position: int,
    avg_cost: float,
    date: str,
    price: float,
    size: int,
    buy_commission: float = 0.0,
) -> tuple[float, int, float, dict[str, Any]]:
    """Buy into an aggregate average-cost position.

    ``size`` is cast to ``int`` before any cash math so a fractional caller
    cannot deduct cash for shares the position does not actually hold.
    ``avg_cost`` includes allocated entry fees, so later sells can compute net
    PnL without per-lot entry-fee allocation.
    """
    _require_positive_price(price)
    size = int(size)
    _require_positive_size(size)
    entry_notional = size * price
    entry_fee = entry_notional * buy_commission
    cost = entry_notional + entry_fee
    if cost > cash + 1e-9:
        raise ValueError(f"insufficient cash for average-cost buy: cost={cost}, cash={cash}")

    new_position = int(position) + size
    existing_cost = int(position) * float(avg_cost)
    new_avg_cost = (existing_cost + cost) / new_position
    info = {
        "date": date,
        "size": size,
        "price": float(price),
        "entry_notional": entry_notional,
        "entry_fee": entry_fee,
        "cost": cost,
        "avg_cost_after": new_avg_cost,
    }
    return cash - cost, new_position, new_avg_cost, info


def sell_average_cost(
    cash: float,
    *,
    position: int,
    avg_cost: float,
    date: str,
    price: float,
    size: int,
    sell_commission: float = 0.0,
    sell_tax: float = 0.0,
    symbol: str = "",
    symbol_name: str = "",
    entry_date: str = "",
    entry_bar: int | None = None,
    exit_bar: int | None = None,
    trade_group_id: str | None = None,
) -> tuple[float, int, float, dict[str, Any]]:
    """Sell from an aggregate average-cost position."""
    _require_positive_price(price)
    size = int(size)
    _require_positive_size(size)
    if size > int(position):
        raise ValueError(f"sell size={size} exceeds position={position}")

    entry_notional = size * float(avg_cost)
    exit_notional = size * price
    exit_fee = exit_notional * (sell_commission + sell_tax)
    gross_pnl = exit_notional - entry_notional
    pnl = gross_pnl - exit_fee
    pnl_pct = pnl / entry_notional * 100.0 if entry_notional else 0.0
    holding_bars = (
        int(exit_bar) - int(entry_bar)
        if exit_bar is not None and entry_bar is not None
        else None
    )
    trade = {
        "trade_group_id": trade_group_id,
        "entry_date": entry_date,
        "exit_date": date,
        "side": "long",
        "size": int(size),
        "entry_price": float(avg_cost),
        "exit_price": float(price),
        "entry_notional": entry_notional,
        "exit_notional": exit_notional,
        "entry_fee": 0.0,
        "exit_fee": exit_fee,
        "fees": exit_fee,
        "gross_pnl": gross_pnl,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "pnl_pct_basis": entry_notional,
        "holding_bars": holding_bars,
        "symbol": symbol,
        "symbol_name": symbol_name,
    }
    proceeds = exit_notional - exit_fee
    new_position = int(position) - int(size)
    new_avg_cost = 0.0 if new_position == 0 else float(avg_cost)
    return cash + proceeds, new_position, new_avg_cost, trade


def compute_position_equity(cash: float, position: int, close_price: float) -> float:
    """Mark aggregate long-only equity to market."""
    _require_positive_price(close_price)
    return float(cash) + int(position) * close_price


def compute_portfolio_equity(
    cash: float,
    positions: dict[str, int | float],
    prices: dict[str, float],
    *,
    liabilities: float = 0.0,
) -> float:
    """Mark a mixed long/short portfolio to market.

    Long positions are positive, short positions are negative. Liabilities are
    explicit margin loans or other debts not already reflected in cash.
    """
    _require_non_negative(liabilities, "liabilities")
    equity = float(cash) - float(liabilities)
    for symbol, position in positions.items():
        price = _price_for_symbol(symbol, prices)
        equity += float(position) * price
    return equity


def compute_lot_portfolio_equity(
    cash: float,
    *,
    long_lots: list[dict[str, Any]] | None = None,
    short_lots: list[dict[str, Any]] | None = None,
    prices: dict[str, float] | None = None,
    default_price: float | None = None,
    liabilities: float = 0.0,
) -> float:
    """Mark long and short lots to market with optional explicit liabilities."""
    _require_non_negative(liabilities, "liabilities")
    equity = float(cash) - float(liabilities)
    for lot in long_lots or []:
        price = _price_for_lot(lot, prices, default_price)
        equity += int(lot.get("size") or 0) * price
    for lot in short_lots or []:
        price = _price_for_lot(lot, prices, default_price)
        equity -= int(lot.get("size") or 0) * price
    return equity


def compute_required_margin(
    positions: dict[str, int | float],
    prices: dict[str, float],
    *,
    long_margin_rate: float = 0.5,
    short_margin_rate: float = 0.5,
) -> float:
    """Compute caller-defined margin requirement for long and short exposure."""
    _require_non_negative(long_margin_rate, "long_margin_rate")
    _require_non_negative(short_margin_rate, "short_margin_rate")
    required = 0.0
    for symbol, position in positions.items():
        price = _price_for_symbol(symbol, prices)
        notional = abs(float(position) * price)
        if float(position) >= 0:
            required += notional * long_margin_rate
        else:
            required += notional * short_margin_rate
    return required


def check_margin_requirement(
    equity: float,
    required_margin: float,
) -> tuple[bool, float]:
    """Return (is_satisfied, excess_equity)."""
    _require_non_negative(required_margin, "required_margin")
    excess = float(equity) - float(required_margin)
    return excess >= -1e-9, excess


def accrue_liability_interest(
    liabilities: float,
    *,
    annual_rate: float,
    days: int | float = 1,
    day_count: int | float = 365,
) -> tuple[float, float]:
    """Accrue simple interest on explicit margin liabilities."""
    _require_non_negative(liabilities, "liabilities")
    interest = compute_borrow_fee(
        liabilities,
        annual_rate=annual_rate,
        days=days,
        day_count=day_count,
    )
    return float(liabilities) + interest, interest


def compute_borrow_fee(
    notional: float,
    *,
    annual_rate: float,
    days: int | float = 1,
    day_count: int | float = 365,
) -> float:
    """Compute simple borrow fee or financing interest for a holding period."""
    _require_non_negative(notional, "notional")
    _require_non_negative(annual_rate, "annual_rate")
    _require_non_negative(days, "days")
    if float(day_count) <= 0:
        raise ValueError(f"day_count must be positive: {day_count}")
    return float(notional) * float(annual_rate) * float(days) / float(day_count)


def validate_trade_pnl_pct(trade: dict[str, Any], *, tolerance_pct: float = 0.05) -> None:
    """Ensure pnl_pct uses the same net PnL basis as the trade record."""
    pnl = _safe_float(trade.get("pnl"))
    pnl_pct = _safe_float(trade.get("pnl_pct"))
    if pnl is None or pnl_pct is None:
        return

    basis = _safe_float(trade.get("pnl_pct_basis"))
    if basis is None:
        entry_notional = _safe_float(trade.get("entry_notional"))
        if entry_notional is None:
            size = _safe_float(trade.get("size"))
            entry_price = _safe_float(trade.get("entry_price"))
            if size is None or entry_price is None:
                return
            entry_notional = abs(size * entry_price)
        entry_fee = _safe_float(trade.get("entry_fee")) or 0.0
        basis = entry_notional + entry_fee

    if basis <= 0:
        return
    expected = pnl / basis * 100.0
    if not math.isclose(expected, pnl_pct, abs_tol=tolerance_pct):
        raise ValueError(
            "pnl_pct must be net pnl divided by entry cost basis. "
            f"expected={expected:.6f}, got={pnl_pct:.6f}, trade={trade}"
        )


def _require_positive_price(price: float) -> None:
    if not math.isfinite(float(price)) or float(price) <= 0:
        raise ValueError(f"price must be positive and finite: {price}")


def _require_positive_size(size: int) -> None:
    if int(size) <= 0:
        raise ValueError(f"size must be positive: {size}")


def _require_non_negative(value: float, name: str) -> None:
    if not math.isfinite(float(value)) or float(value) < 0:
        raise ValueError(f"{name} must be non-negative and finite: {value}")


def _price_for_symbol(symbol: str, prices: dict[str, float]) -> float:
    if symbol not in prices:
        raise KeyError(f"missing price for symbol: {symbol}")
    price = float(prices[symbol])
    _require_positive_price(price)
    return price


def _price_for_lot(
    lot: dict[str, Any],
    prices: dict[str, float] | None,
    default_price: float | None,
) -> float:
    if prices is not None:
        return _price_for_symbol(str(lot.get("symbol", "")), prices)
    if default_price is None:
        raise ValueError("prices or default_price must be provided")
    price = float(default_price)
    _require_positive_price(price)
    return price


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result
