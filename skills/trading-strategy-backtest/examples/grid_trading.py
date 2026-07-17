"""
Example 3: Grid-strategy sample
(fixed-percentage layered grid, pure Python + pandas)

Example query:
"Backtest a fixed-percentage long-only grid strategy on the CSI 300 ETF.
Use A-share T+1 rules, fill at the next day's open, round to 100-share lots,
start with 150,000 cash, use 3 bps commission on both sides, and 0 stamp duty
for ETF sells.
Open the initial base position with 10,000 cash.
Then run a 4% arithmetic grid with at most 5 add-on layers, each layer also
using 10,000 cash. If the close falls through the next grid level relative to
anchor_price, buy the missing layer at the next day's open. If the close
recovers the take-profit grid for a specific layer, sell only that layer at the
next day's open. Record each grid lot as its own closed trade, never merge
multiple layers into one trade. Force-close any remaining layers at the last
bar's close."

Helper usage demo: lot_matching = strategy_specific (close each layer on its
own), with everything routed through reference.accounting:
  - buy_lot opens a lot (extra `level` field passed via **kwargs)
  - close_lot atomically closes one specific lot (cannot use close_lots_fifo —
    grid matches by layer index, not by FIFO order)
  - compute_lot_equity computes equity
"""

from __future__ import annotations

import pandas as pd

from reference.accounting import buy_lot, close_lot, compute_lot_equity


def _target_open_levels(
    close_price: float,
    anchor_price: float,
    grid_pct: float,
    max_layers: int,
) -> list[int]:
    levels = [0]
    for step in range(1, max_layers + 1):
        threshold = anchor_price * (1 - grid_pct * step)
        if close_price <= threshold:
            levels.append(-step)
        else:
            break
    return levels


def _grid_take_profit_price(anchor_price: float, level: int, grid_pct: float) -> float:
    return anchor_price * (1 + (level + 1) * grid_pct)


def run(
    df: pd.DataFrame,
    initial_cash: float = 150_000,
    lot_cash: float = 10_000,
    grid_pct: float = 0.04,
    max_layers: int = 5,
    buy_commission: float = 0.0003,
    sell_commission: float = 0.0003,
    sell_tax: float = 0.0,
    lot_size: int = 100,
    t_plus_1: bool = True,
    symbol: str = "",
) -> tuple[list, list]:
    df = df.copy().sort_values("date").reset_index(drop=True)

    cash = float(initial_cash)
    anchor_price: float | None = None
    next_lot_seq = 1
    open_lots: list[dict] = []
    pending_buy_levels: list[int] = []
    pending_sell_lot_ids: set[str] = set()

    equity_curve: list[dict] = []
    trade_history: list[dict] = []

    for i in range(len(df)):
        row = df.iloc[i]
        date = str(row["date"])[:10]
        open_price = float(row["open"])
        close_price = float(row["close"])

        # ====== Execute yesterday's pending sells (close each lot by lot_id, not FIFO) ======
        if pending_sell_lot_ids:
            still_pending: set[str] = set()
            remaining_lots: list[dict] = []
            for lot in open_lots:
                lot_id = lot["lot_id"]
                if lot_id not in pending_sell_lot_ids:
                    remaining_lots.append(lot)
                    continue
                if t_plus_1 and i <= int(lot.get("entry_bar", -1)):
                    still_pending.add(lot_id)
                    remaining_lots.append(lot)
                    continue

                proceeds, trade, residual = close_lot(
                    lot,
                    date=date,
                    price=open_price,
                    exit_bar=i,
                    close_size=int(lot["size"]),
                    sell_commission=sell_commission,
                    sell_tax=sell_tax,
                    symbol=symbol,
                )
                trade["matching_note"] = (
                    f"grid level {lot.get('level')} take-profit exit"
                )
                cash += proceeds
                trade_history.append(trade)
                if residual is not None:
                    remaining_lots.append(residual)

            open_lots = remaining_lots
            pending_sell_lot_ids = still_pending

        # ====== Execute yesterday's pending buys (fill at next day's open) ======
        if pending_buy_levels:
            executed_levels = set()
            for level in sorted(set(pending_buy_levels), reverse=True):
                if any(lot["level"] == level for lot in open_lots):
                    executed_levels.add(level)
                    continue

                size = int(lot_cash / (open_price * (1 + buy_commission)))
                size = (size // lot_size) * lot_size
                if size <= 0:
                    executed_levels.add(level)
                    continue

                cost = size * open_price * (1 + buy_commission)
                if cost > cash:
                    executed_levels.add(level)
                    continue

                if not open_lots and level == 0:
                    anchor_price = open_price

                if anchor_price is None:
                    executed_levels.add(level)
                    continue

                cash, lot = buy_lot(
                    cash,
                    lot_id=f"L{next_lot_seq}",
                    date=date,
                    price=open_price,
                    size=size,
                    entry_bar=i,
                    buy_commission=buy_commission,
                    symbol=symbol,
                    level=level,  # extra field stashed into the lot dict
                )
                open_lots.append(lot)
                next_lot_seq += 1
                executed_levels.add(level)

            pending_buy_levels = [
                level for level in pending_buy_levels if level not in executed_levels
            ]

        if not open_lots and not pending_buy_levels:
            anchor_price = None

        # ====== Generate today's signals (execute tomorrow) ======
        if not open_lots and not pending_buy_levels:
            pending_buy_levels.append(0)
        elif anchor_price is not None:
            desired_levels = _target_open_levels(
                close_price=close_price,
                anchor_price=anchor_price,
                grid_pct=grid_pct,
                max_layers=max_layers,
            )
            current_levels = {lot["level"] for lot in open_lots}
            pending_levels = set(pending_buy_levels)
            for level in desired_levels:
                if level not in current_levels and level not in pending_levels:
                    pending_buy_levels.append(level)

            for lot in open_lots:
                target_price = _grid_take_profit_price(
                    anchor_price=anchor_price,
                    level=lot["level"],
                    grid_pct=grid_pct,
                )
                if close_price >= target_price:
                    pending_sell_lot_ids.add(lot["lot_id"])

        equity_curve.append({
            "date": date,
            "value": round(compute_lot_equity(cash, open_lots, close_price), 2),
        })

    # ====== End-of-window force liquidation: close every layer individually via close_lot ======
    if open_lots:
        last = df.iloc[-1]
        last_date = str(last["date"])[:10]
        last_close = float(last["close"])
        for lot in list(open_lots):
            proceeds, trade, _ = close_lot(
                lot,
                date=last_date,
                price=last_close,
                exit_bar=len(df) - 1,
                close_size=int(lot["size"]),
                sell_commission=sell_commission,
                sell_tax=sell_tax,
                symbol=symbol,
            )
            trade["matching_note"] = f"grid level {lot.get('level')} forced close"
            cash += proceeds
            trade_history.append(trade)
        open_lots = []
        equity_curve[-1]["value"] = round(cash, 2)

    return equity_curve, trade_history
