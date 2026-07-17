"""
Example 1: Moving-average strategy sample
(trend filter + dual EMA + trailing stop, pure Python + pandas)

Example query:
"Backtest a trend-filtered moving-average strategy on the CSI 300 ETF.
Only allow long entries when close > SMA120.
Buy when EMA20 crosses above EMA60.
Sell when EMA20 crosses below EMA60, or close < SMA120, or the position draws
down 8% from the highest close seen since entry.
Use A-share T+1 rules, fill at the next day's open, round to 100-share lots,
start with 1,000,000 cash, use 3 bps commission on both sides, and 0 stamp
duty for the ETF example (pass 5 bps if you switch to an A-share stock).
Return equity_curve and closed trade_history,
and force-close any remaining position at the last bar's close."

Helper usage demo: even single-position strategies use the lot_level default
(lot count is always <= 1), with everything routed through reference.accounting:
  - buy_lot opens a lot
  - close_lots_fifo flat-closes (FIFO)
  - compute_lot_equity computes equity
"""

from __future__ import annotations

import pandas as pd

from reference.accounting import buy_lot, close_lots_fifo, compute_lot_equity


def run(
    df: pd.DataFrame,
    initial_cash: float = 1_000_000,
    buy_commission: float = 0.0003,
    sell_commission: float = 0.0003,
    sell_tax: float = 0.0,
    lot_size: int = 100,
    t_plus_1: bool = True,
    fast_span: int = 20,
    slow_span: int = 60,
    trend_window: int = 120,
    trailing_stop_pct: float = 0.08,
    symbol: str = "",
) -> tuple[list, list]:
    """
    df must contain date, open, high, low, close, volume columns, sorted ascending.
    Returns (equity_curve, trade_history).
    """
    df = df.copy().sort_values("date").reset_index(drop=True)
    df["ema_fast"] = df["close"].ewm(span=fast_span, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=slow_span, adjust=False).mean()
    df["sma_trend"] = df["close"].rolling(trend_window).mean()

    df["cross_up"] = (
        (df["ema_fast"].shift(1) <= df["ema_slow"].shift(1))
        & (df["ema_fast"] > df["ema_slow"])
    )
    df["cross_down"] = (
        (df["ema_fast"].shift(1) >= df["ema_slow"].shift(1))
        & (df["ema_fast"] < df["ema_slow"])
    )

    cash = float(initial_cash)
    open_lots: list[dict] = []
    next_lot_id = 1
    highest_close_since_entry: float | None = None
    pending_buy = False
    pending_sell = False

    equity_curve: list[dict] = []
    trade_history: list[dict] = []

    for i in range(len(df)):
        row = df.iloc[i]
        date = str(row["date"])[:10]
        open_price = float(row["open"])
        close_price = float(row["close"])
        low_price = float(row["low"])

        # ====== Execute yesterday's pending signal (fill at next day's open) ======
        if pending_buy and not open_lots:
            size = int(cash / (open_price * (1 + buy_commission)))
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
                highest_close_since_entry = None
            pending_buy = False

        if pending_sell and open_lots:
            total_size = sum(int(lot["size"]) for lot in open_lots)
            proceeds, trades, open_lots, _ = close_lots_fifo(
                open_lots,
                sell_size=total_size,
                date=date,
                price=open_price,
                exit_bar=i,
                sell_commission=sell_commission,
                sell_tax=sell_tax,
                symbol=symbol,
                t_plus_1=t_plus_1,
            )
            cash += proceeds
            trade_history.extend(trades)
            if not open_lots:
                highest_close_since_entry = None
            pending_sell = False

        indicators_ready = (
            pd.notna(row["ema_fast"])
            and pd.notna(row["ema_slow"])
            and pd.notna(row["sma_trend"])
        )

        # ====== Generate today's signal (executes tomorrow) ======
        if indicators_ready:
            if not open_lots:
                if close_price > float(row["sma_trend"]) and bool(row["cross_up"]):
                    pending_buy = True
            else:
                entry_bar = open_lots[0]["entry_bar"]
                stop_price = None
                if i > entry_bar and highest_close_since_entry is not None:
                    stop_price = highest_close_since_entry * (1 - trailing_stop_pct)

                if stop_price is not None and low_price <= stop_price:
                    pending_sell = True
                elif bool(row["cross_down"]):
                    pending_sell = True
                elif close_price < float(row["sma_trend"]):
                    pending_sell = True

        # Check stop against the prior peak first, then update the peak — avoids
        # a same-bar look-ahead where the peak would already include today's close.
        if open_lots:
            if highest_close_since_entry is None:
                highest_close_since_entry = close_price
            else:
                highest_close_since_entry = max(highest_close_since_entry, close_price)

        equity_curve.append({
            "date": date,
            "value": round(compute_lot_equity(cash, open_lots, close_price), 2),
        })

    # ====== End-of-window force liquidation: close any remaining lots at the last bar's close ======
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
            t_plus_1=False,
        )
        cash += proceeds
        trade_history.extend(trades)
        equity_curve[-1]["value"] = round(cash, 2)

    return equity_curve, trade_history
