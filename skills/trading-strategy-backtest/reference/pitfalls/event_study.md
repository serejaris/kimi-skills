# Event-study timeline curve guide

## When to read this

Read this only when **all three** apply:

- The current task is an event study (not a strategy backtest)
- The dashboard uses `event_overview_mode="timeline"` or `"both"`
- You need to generate the daily `equity_curve` yourself and pass it to `render_dashboard`

If `event_overview_mode="stats"`, skip this doc — stats mode does not draw a curve.

## Hard rule: source verification

Before writing any event row, you must search the web (news / filings / research reports / exchange announcements) to find a real `source_url` that confirms the event. Do **not** fabricate URLs, do not use placeholder URLs like `https://example.com`, and do not leave `source_url` empty. An event study without verifiable sources is unreliable and must not be delivered. If a search truly cannot locate a source, document the search steps taken in your reply before leaving `source_url` empty.

## Why this is needed

By default an event study only records one `pnl_pct` per event at its `exit_date`. If you do not pass an `equity_curve`, the fallback in `render_dashboard.py` simply connects those exit-day points with straight lines. The result is a "few sharp dots" curve that hides every unrealized P/L during the holding window and looks especially bad with sparse events.

The fix: build a smooth daily mark-to-market curve yourself and pass it explicitly.

## Core idea

The timeline curve answers the question: **"if I had taken every event signal and put an equal-sized position into each one, what would my portfolio look like day by day?"**

- Realized leg: once an event is closed, its return is locked into the curve permanently
- Unrealized leg: while an event is still open, its current price relative to entry contributes to the curve
- Multiple concurrent events: equal-weight average (not sum — sum is equivalent to "max leverage", and any cluster of overlapping events would inflate the curve and misrepresent the strategy)

## Price basis

- **Default: daily close** for both the entry baseline and the daily mark-to-market
- If the user mentions open price / next-day-open / gap filtering / high / VWAP, follow the user; **do not override silently**
- Hard rule: the entry baseline price and the mark-to-market price must use the same field. Mixing close-baseline with open-mark-to-market makes the curve start out of sync with `pnl_pct` in trades.csv

## Formulas

**Per-event normalized return series** (for each trading day t in the holding window):

```
r_i(t) = price_i(t) / entry_price_i - 1
```

`price_i(t)` is event i's symbol price on day t (close by default), `entry_price_i` is the same field on the entry day. Note that `r_i(entry_date) = 0` and `r_i(exit_date) = pnl_pct / 100`; both endpoints must agree with trades.csv.

**Portfolio curve** (for each global trading day t):

```
portfolio(t) = mean(r_i(t) for i in active_at_t)
             + sum(realized_r_j for j closed strictly before t)
```

- `active_at_t`: events whose `[entry_date_i, exit_date_i]` window contains t
- `realized_r_j`: closed event j's `pnl_pct / 100`
- When `active_at_t` is empty, the mean term is 0 (flat day)

**Flat-day handling**: if `active_at_t` is empty and no event closes on day t, the curve value equals the previous day's value (horizontal extension, **not zero**). Resetting to zero would visually wipe out previously realized gains every time the event stream goes quiet.

**Anchor at 100**: convert `portfolio(t)` to value before passing to render:

```
value(t) = 100 * (1 + portfolio(t))
```

`equity_curve[0].value` must equal 100, matching the strategy-backtest dashboard normalization.

## Implementation steps (no code, just sequence)

1. **Pull daily prices**: for each trade, fetch the `[entry_date, exit_date]` daily close series for its symbol. Each symbol has its own series.
2. **Compute r_i series**: normalize each event by the formula above, into a date→r dict or Series.
3. **Build a global trading-day axis**: take the union of all event date ranges, expanded by the trading-day calendar (not natural days).
4. **Aggregate per day**: walk every t, find the active set, take the arithmetic mean of `r_i(t)` over actives, and add the sum of `realized_r_j` for events closed **strictly before** t.
5. **Fill flat days**: when actives is empty and no new event closes that day, carry the previous day's value forward.
6. **Anchor to 100**: convert to `[{date, value}]` and pass via `render_dashboard.build_dashboard_data(equity_curve=...)`.

## Common pitfalls

- **Forward-filling halted days**: do not forward-fill into signal logic, but ffill is fine for curve construction (held but unquoted = unrealized P/L unchanged). Cap the ffill window — a halt of more than 5–10 trading days should warn or truncate.
- **Misaligned multi-symbol calendars**: A-shares, Hong Kong, U.S. all have different trading calendars; even within one market, halts can shift dates. Align each symbol to its own trading days first, then union into the global axis with ffill.
- **Double-counting entry/exit endpoints**: a single event can be both active and just-realized. Filter realized with "strictly before" to avoid the exit day double-counting. Recommended rule: on the exit day, the event is still in actives (using exit-day `r_i`); from the next trading day on, it counts as realized.
- **Delisted / missing data**: when prices cannot be fetched, truncate the event at the last valid price and treat that as the exit; do not silently drop the event.
- **mean vs sum confusion**: default to mean. If the user explicitly says "I would have bought $10k each event / total return is the sum", switch to sum — and **state explicitly in your reply which aggregation you used**.

## Format passed to render

Identical to strategy backtests:

```python
equity_curve = [
    {"date": "2024-01-15", "value": 100.0},
    {"date": "2024-01-16", "value": 100.32},
    ...
]

build_dashboard_data(
    equity_curve=equity_curve,
    trade_history=trades,
    summary=summary,
    meta={"report_kind": "event_study", ...},
    event_overview_mode="timeline",  # or "both"
    language=...,
)
```

When render detects an event study with `equity_curve` already supplied, it skips `_build_event_pnl_curve` and uses your curve directly.

## What to mention in the reply

The user sees both the dashboard curve and the textual reply. The reply should include at least:

- The aggregation used (mean / sum)
- The price basis (close / open / other)
- The peak number of concurrent events (so the user can judge whether the curve is dominated by one dense event cluster)

For example: "The timeline curve uses equal-weight aggregation across concurrent events, with daily close as the price basis; up to 3 events were held at the same time."
