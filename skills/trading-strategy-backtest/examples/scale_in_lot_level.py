"""
Example: every buy signal opens a new lot; every sell signal closes half
of the open exposure via FIFO.

Demonstrates lot-level accounting: each buy creates an independent lot,
and partial sells fragment lots into slices that go into trade_history
one row each. ``df`` must contain ``date, open, close, buy_signal,
sell_signal``; signals are confirmed at bar close and filled at the next
bar's open.
"""

from __future__ import annotations

import pandas as pd

from reference.accounting import buy_lot, close_lots_fifo, compute_lot_equity


def run(
    df: pd.DataFrame,
    *,
    initial_cash: float = 1_000_000,
    lot_cash: float = 100_000,
    lot_size: int = 100,
    buy_commission: float = 0.0003,
    sell_commission: float = 0.0003,
    sell_tax: float = 0.0,
    symbol: str = "",
    t_plus_1: bool = True,
) -> tuple[list[dict], list[dict]]:
    df = df.copy().sort_values("date").reset_index(drop=True)
    cash = float(initial_cash)
    open_lots: list[dict] = []
    trade_history: list[dict] = []
    equity_curve: list[dict] = []
    pending_buy = False
    pending_sell_size = 0
    next_lot_id = 1

    for i, row in df.iterrows():
        date = str(row["date"])[:10]
        open_price = float(row["open"])
        close_price = float(row["close"])

        if pending_sell_size > 0 and open_lots:
            proceeds, trades, open_lots, unfilled = close_lots_fifo(
                open_lots,
                sell_size=pending_sell_size,
                date=date,
                price=open_price,
                exit_bar=i,
                sell_commission=sell_commission,
                sell_tax=sell_tax,
                symbol=symbol,
                trade_group_id=f"S{i}",
                t_plus_1=t_plus_1,
            )
            cash += proceeds
            trade_history.extend(trades)
            pending_sell_size = unfilled

        if pending_buy:
            target_cash = min(lot_cash, cash)
            size = int(target_cash / (open_price * (1 + buy_commission)))
            size = (size // lot_size) * lot_size
            if size > 0:
                cash, lot = buy_lot(
                    cash,
                    lot_id=f"L{next_lot_id}",
                    date=date,
                    price=open_price,
                    size=size,
                    entry_bar=i,
                    buy_commission=buy_commission,
                    symbol=symbol,
                )
                open_lots.append(lot)
                next_lot_id += 1
            pending_buy = False

        if bool(row.get("buy_signal", False)):
            pending_buy = True
        if bool(row.get("sell_signal", False)):
            total_size = sum(int(lot["size"]) for lot in open_lots)
            sell_size = ((total_size // 2) // lot_size) * lot_size
            pending_sell_size += sell_size

        equity_curve.append({
            "date": date,
            "value": round(compute_lot_equity(cash, open_lots, close_price), 2),
        })

    if open_lots:
        last = df.iloc[-1]
        last_date = str(last["date"])[:10]
        last_close = float(last["close"])
        total_size = sum(int(lot["size"]) for lot in open_lots)
        proceeds, trades, open_lots, _ = close_lots_fifo(
            open_lots,
            sell_size=total_size,
            date=last_date,
            price=last_close,
            exit_bar=len(df) - 1,
            sell_commission=sell_commission,
            sell_tax=sell_tax,
            symbol=symbol,
            trade_group_id="forced_close",
            t_plus_1=False,
        )
        cash += proceeds
        trade_history.extend(trades)
        equity_curve[-1]["value"] = round(cash, 2)

    return equity_curve, trade_history
