---
name: quick-strategy-backtest
description: Convert trading strategy descriptions (including event-driven studies, stock selection, and portfolio) into runnable backtest code, and output backtest results, visual dashboards, and analytical writeups. Trigger this skill when the user describes buy/sell conditions, post-event return questions, or stock-universe screening backtests.
version: 1.0.8
---

# Quick Strategy Backtest

## IMPORTANT: Output-Language Lock

- The final conversation reply and every deliverable (dashboard / charts / tables / custom_html) **must follow the language of the user's latest query, not the market**; if the user explicitly requests a language, follow that request
- Decide a single `output_language = "zh" | "en"` first, and route every user-visible string through it; when generating the dashboard, pass `build_dashboard_data(..., language=output_language)` explicitly
- If the prompt is in English and the symbols are China / Hong Kong stocks, **both the reply and the deliverables must stay in English**; stock references should default to ticker code such as `600519.SH` / `0700.HK`
- If the prompt is in Chinese, **both the reply and the deliverables must stay in Chinese**; when a Chinese stock name is known, prefer the Chinese name
- "Deliverables" covers **every** user-visible field; **commonly missed** ones include `strategy_name` (dashboard top title — always pass it), module title / subtitle, `trades_table` column labels, `text` module body, and matplotlib titles — all follow `output_language`.
- **Do not make this mistake**: the HTML is in English but the actual conversation reply switches back to Chinese
- If the English stock name is uncertain, use the ticker code instead of a Chinese stock name

## IMPORTANT: Reproducible Script and Accounting Semantics

- **A `.py` script is mandatory**: strategy backtests must write the implementation to a `.py` file in cwd and generate results by running `python <script>.py`; do not complete the backtest only through a temporary one-off shell snippet
- **Self-designed strategies: plan before implementing**: when the user asks the agent to "design / find / optimize a strategy" itself, you must first write an internal strategy plan (signals, entry/exit conditions, execution timing, sizing, costs, whether scaling in / partial exits are allowed, multi-symbol vs event study). Then route through the skill, read the relevant reference files, and revise the plan. Only after the plan passes look-ahead, warm-up, accounting, export, and dashboard checks are you allowed to write code
- Default `position_accounting="lot_level"`: every buy uses `buy_lot` to create an independent lot (with `lot_id`), every sell uses `close_lots_fifo` (FIFO). With the default flat-only entry gate and full-exit semantics, the lot count is always ≤ 1 and `trades.csv` rows = full open-close cycles; scaling / grid / rotation strategies get per-lot attribution for free
- **Mandatory long-only rules**: pure-Python cash equity / ETF backtests default to long-only lot-level accounting. Buy / sell / equity calculations must call `buy_lot / close_lots_fifo / close_lot / compute_lot_equity` from `reference.accounting`. `export_results(position_accounting="lot_level")` is only an export-time validator; it does not recompute FIFO, cash, fees, or PnL for you
- **Long-only helper responsibilities**: `buy_lot` creates an independent long lot and deducts entry cost; `close_lots_fifo` sells one or more long lots by FIFO and returns closed-trade records; `close_lot` fully or partially closes one specified long lot for grid / LIFO / custom matching; `compute_lot_equity` marks cash plus open long lots to current equity
- **Sizing responsibility**: `buy_lot` / `buy_average_cost` are not sizing helpers; they only execute the provided `size` and validate cash. Before calling them, compute an affordable round-lot `size` from available `cash`, fill price, commissions, and `lot_size`. For fixed-cash scale-ins, cap the target cash at available cash (for example `target_cash = min(lot_cash, cash)`); after round-lot flooring, skip or record ignored when `size <= 0` instead of using `insufficient cash` as normal control flow
- **Short / leverage routing**: if a strategy includes shorting, margin buys, securities lending, margin requirements, negative cash, borrow fees, or financing interest, do not expand the details in `SKILL.md`; read `reference/short_leverage_routes.md`
- **Flat-position entry gate (default hard rule)**: every buy execution block must be guarded by a flat-position condition (`position == 0` / `not open_lots` / current weight is 0); repeated buy signals while holding may only increment ignored counters and must not change cash / position / open_lots. Add a runtime assert in code: store `prior_position` before the buy block and `assert not (prior_position > 0 and buy_executed)` after it. Strategies that allow scaling (user prompt contains "add-on / scale in / every signal buys / grid / staged entry / overlapping events") may relax this gate
- Opt in to `position_accounting="aggregate_average_cost"` (use `buy_average_cost / sell_average_cost`, no `lot_id`) only when the **user explicitly asks for** "per-trade PnL on average cost" / "alignment with broker statement cost basis" / "pure DCA where every entry is interchangeable". Otherwise stay on `lot_level`
- Strategy backtest export must call `export_results(..., is_flat_at_end=True, position_accounting="lot_level"|"aggregate_average_cost", ...)`; the export layer rejects missing period-end flat confirmation, `lot_level` trades without `lot_id`, or `aggregate_average_cost` trades that contain `lot_id`

## Trigger Conditions

Trigger this skill when **any** of the following is true:

- The user asks for a backtest
- The user provides quantitative descriptions such as entry/exit rules, symbols, frequency, or time range
- The user asks for backtest metrics or a report
- The user describes an event / signal / condition and wants to know the subsequent performance. Typical phrasing:
  - "Buy after XX and hold for N days; how did it perform?"
  - "What was the return after event XX?"
  - "After the signal triggers, hold N days and sell"
  - "Run an event study"
  - "Is this strategy effective?"
  - "Screen stocks that satisfy XX and check later performance"
- The user wants multi-symbol stock-selection backtests or portfolio rebalancing

## Out of Scope

- **Intraday / minute / tick backtesting**: this skill only supports daily or lower-frequency data (daily, weekly, monthly). If the user asks for minute bars, 5-minute bars, ticks, and so on, state directly that it is unsupported
- **Futures / options / perpetuals / convertible bonds and other derivatives**: the accounting helpers only cover cash equity / ETF; margin, contract multipliers, daily mark-to-market, and rollover are out of scope — state directly that it is unsupported
- **Short selling / leverage / margin financing**: still in beta, temporarily unsupported; only cash long positions are covered today, and securities borrowing, margin maintenance, liquidation, and leverage ratios are not handled
- Full cross-sectional factor stock-selection strategies

## User-Facing Communication Rules

**During clarification and in the final reply, do not expose code variable names, implementation details, or framework jargon.** Everything should be communicated in natural language:

- ❌ "Use pandas rolling to compute MA120"
- ✅ "Calculated the 120-day moving average"
- ❌ "Signal is generated on bar i and executed on bar i+1"
- ✅ "After the signal is confirmed, buy at the next day's open"
- ❌ "A-share T+1 is enforced by entry_bar"
- ✅ "In A shares, you cannot sell on the same day you buy; the earliest sell is the next day"

Implementation details are internal. **They must never appear in user-facing text** (clarification or result interpretation).

## Decide First: Do You Need Clarification?

**Principle**: only ask questions that are truly necessary to avoid being wrong. Do not dump eight questions on the user at once. Use defaults whenever that is safe. Keep clarification to 1-3 questions.

**Clarification Gate (hard rule)**: before writing code, running a backtest, exporting CSV/JSON, or generating HTML, pass this section first. If any "Must Ask" item applies and the user has not answered it, stop and ask 1-3 short questions; do not guess with defaults or implement a "probably right" version first. User phrases like "you decide" or "use defaults" do not override questions that would otherwise make the result wrong. If no Must Ask item applies, continue the quick flow and disclose any defaults in the final reply.

### Must Ask (Wrong if You Don't)

If the information below is missing, the result can change completely. **Do not guess; ask.**

- **Signal definition is ambiguous**: the user says "breakout", "volume surge", or "uptrend". Is this a point-in-time event (the instant of crossing) or a persistent state? Without clarification, the generated strategy may be fundamentally different
- **Lifecycle is unclear**: the prompt says "first", "first buy point", or "buy again on the next golden cross" but does not define reset conditions. Is the event one-time only, or repeatable?
- **Compound-exit semantics are unclear**: entry is A and B and C, but the user only says "exit on reverse signal". Does "reverse" mean the full mirror condition, or only one sub-condition?

### Should Ask (Ask if Ambiguous; Otherwise Use Defaults)

- Backtest range — ask if the user did not specify one; if they say "last three years", it can be inferred
- Position sizing — for single-symbol strategy backtests, default to full position and disclose it; for multi-symbol / portfolio tasks, clarify or ask about weights. If the user mentions "partial allocation", "10%", etc., confirm the actual number
- Execution timing — default is next-day open; if the user says "buy the same day", ask whether that means same-day close or next-day open

### Use Defaults Directly (Do Not Ask)

- Fees / slippage: 3 bps for continuous strategies; 0 for event-study style setups
- Data frequency: daily
- T+1 / lot size: enabled automatically for A shares
- Dashboard: generate by default

If the task involves **multiple strategies / multiple symbols** (priority vs secondary, rotation, hedging, switching), **immediately read the "Multi-Strategy Interaction" section in `reference/strategy_parsing.md`** and check priority, preemption, switching timing, and ownership of constraints item by item. If any answer is unclear, ask the user.

**Look-ahead judgment principle**: do not rely only on fixed keywords. The key question is whether an order, rebalance, selection, stop-loss, take-profit, or size decision uses information that was not available at that decision time. Future returns may be used as an **outcome variable** in event studies, but not as the event trigger / selection / sizing / risk-control condition. The next bar's open may be used as the **execution price** after a bar-i signal is confirmed, but it must not feed back into the bar-i signal. **The examples below are only high-risk patterns, not a complete blacklist**; missing those examples does not mean the code is safe. Grep/pattern scans help surface risky code shapes, but they do not replace manual timing review.

The following are common patterns, **not an exhaustive list**. When they appear, point out the issue and confirm how to handle it:

- "Buy when today's return exceeds X%" -> today's return is only known at the close, not at the open. Two reasonable treatments: (1) buy at the next day's open (no look-ahead), or (2) buy at the same-day close (user must explicitly accept this)
- "Buy when the stock hits limit-up / limit-down today" -> same issue; limit-up state is only final at the close
- "Buy when there is a volume breakout today" -> volume is accumulated throughout the day and is not final before the close
- "Select the top N stocks by this year's / this quarter's return" -> cross-sectional look-ahead; you only know the top performers after the fact. This must be rephrased as "use prior-period ranking" or explicitly disclosed as survivor / hindsight bias
- "Buy at today's close when the close moves above the moving average" -> `close > MA` is known only at the close; using the close as execution requires user confirmation
- Full-sample means / percentiles / max-min values, `bfill`, future financial-statement fields, future-N-day returns, `shift(-N)`, and `iloc[i+N]` are all look-ahead risks if they participate in the **current decision**

Handling principle: **do not silently work around the issue**. Tell the user: "Your description cannot avoid look-ahead on daily bars; which approximation do you accept?"

The following cases should not be assumed by default:

- A daily-bar strategy that still requires exact intraday execution -> state directly that it is unsupported
- **A-share symbols with a strategy description that includes short selling / opening shorts / reversing into shorts**: you must ask first. There are three reasonable paths:
  1. The user confirms this is only a theoretical backtest ignoring securities-lending constraints -> implement shorting, but do **not** pass `market="china_a"` into `export_results` (to disable short hard-fail). In the reply, explicitly say: "Naked short selling is not actually allowed in A shares; this backtest ignores borrowing constraints and is for theoretical validation only."
  2. The user wants borrowing semantics -> model borrowing cost, margin requirements, and restrict to borrowable symbols
  3. The user confirms long-only -> reinterpret short signals as exit signals and proceed on the normal `market="china_a"` path

## Quick Flow

**Before entering the quick flow**: pass the clarification section first; if a Must Ask item applies, ask before writing code, exporting data, or generating the dashboard.

1. Read `reference/pitfalls/pandas.md` (common pure-Python backtest mistakes) and `reference/common_pitfalls.md` (the checklist).
2. Read `reference/strategy_parsing.md` only when the strategy involves multi-strategy / multi-symbol interactions, priority, switching, hedging, or unclear strategy structure; simple single-strategy tasks can be structured directly.
3. Write the backtest in pure Python + pandas. Do not use external backtesting frameworks. **The implementation must be saved as a `.py` script in cwd** and that script must be run to generate results; do not complete the backtest only through a temporary REPL / notebook / one-off shell snippet. For continuous daily-bar strategies, default to a pending-signal structure that separates signal generation from execution; only deviate if the user explicitly accepts same-bar-close fills or intraday approximation.
4. Load additional references on demand; do not read everything every time.
5. Formal export, dashboard rendering, and strategy-specific modules all follow the later contract sections: strategy backtests use `export_results(...)` under "**Standard Output Files**"; event studies write event-level `trades.csv` directly; dashboards default to the "**HTML Dashboard**" section; strategy-specific content goes into the main dashboard via `custom_html`. **Do not** output a second standalone HTML page. `reference/render_dashboard.py` is a copyable example, not a mandatory library.
6. Assumptions and known bias should be explained directly in the reply to the user (see part A/B of item 9 and the "Assumptions and Bias" section).
7. **Self-check is mandatory after coding** (see the "Self-Check" section): all 4 steps must be completed before delivery — operability (run in cwd + files produced) / pitfalls checklist / sanity check + adversarial review / post-deploy dashboard self-check. **Adversarial review cannot be skipped.**
8. Default deliverables are defined by the three sections "**Standard Output Files / HTML Dashboard / Matplotlib Charts**". Only skip the dashboard if the user explicitly says they do not want one. Only skip charts if the user explicitly says they do not want charts.
9. **The final reply must include result analysis**. This is user-facing text in the conversation. **Do not dump the full reply verbatim into the dashboard**; however, stable and reviewable parts (such as conclusion summary, key assumptions, limitations, and optimization ideas) may be summarized into `text` modules in the dashboard. **Do not list deliverable files** (for example "generated xx.csv / xx.json / xx.html"). Go straight to analysis. The reply must include the following three parts:

   **Language-lock addendum** — Before sending the final reply, check it once: if `output_language="en"`, then sections A/B/C must all be in English, and China / Hong Kong stock references should default to ticker code; if `output_language="zh"`, then sections A/B/C must all be in Chinese, and known Chinese stock names should stay in Chinese.

   **A. Implementation Details** — Tell the user exactly how the code works. It is not enough to say "stop-loss was implemented" without explaining how. **Any parameter that the prompt did not explicitly specify but the code had to choose must also be explained here, not hidden in comments.** You must cover:
   - Which data fields were used for signal evaluation (`close` / `high` / `low` / `open`) and why
   - Execution timing: next-day open or same-day close, and whether that matches the user's likely expectation
   - Stop-loss / take-profit trigger semantics: use `low/high` as an intraday approximation, or only use `close`
   - Position sizing: how size is computed and what the effective exposure becomes after lot rounding
   - The `equity_curve` accounting convention: how single-name / portfolio / short exposure / negative cash / `liabilities` are aggregated; rotation, short, and leverage strategies must explain this explicitly instead of just saying "daily equity was recorded"
   - Other key implementation choices: how T+1 is handled, how compound conditions are combined, how the state machine resets, and so on

   **B. Limitations and Known Bias** — Explain why the backtest should not be taken as reality at face value. Common bias sources include survivor bias, look-ahead, data coverage, and warmup slicing:
   - Daily-bar limitations: stop-loss / take-profit cannot precisely reconstruct intraday order, and the order of `high` vs `low` inside one bar is unknown
   - Execution-assumption bias: next-day-open execution can differ substantially from the signal price in volatile periods
   - Slippage and liquidity: the backtest does not model market impact; large real trades will incur slippage
   - Data bias: adjustment method, survivor bias, data coverage, and so on
   - Strategy-specific weakness: which market environments it may fail in, whether parameters may be overfit, and so on
   - You do not need to list everything. Pick the 2-3 items that matter most for this specific run

   **C. Result Interpretation** — After reading `summary.json` + `trades.csv`, choose the 3-5 most informative angles from the list below (you do not need to use all of them):
   - Return attribution: which trades contributed most? Is it a few large wins with many small losses (trend-following), or a high win-rate / small-profit profile?
   - Drawdown analysis: when did the worst drawdown occur? Did the stop mechanism actually help?
   - Trade frequency: how many buys and sells separately (do not just say "N total trades"; break it into "X buys, Y sells"), and is the holding period sensible? **For scaling / grid / partial-exit strategies, every `trades.csv` row corresponds to one lot slice** (N add-ons + one full exit → N rows) — this is the core value of per-lot attribution. Use the final reply to call out each batch's hit rate, holding period, and PnL ("the second add-on at +20% was held 2 weeks for -8%"); do not bury it as a "technical convention"
   - Signal quality: how many signals fired? How many were skipped because of capital / lot-size / position constraints?
   - Time-segment performance: are there obvious differences by year or quarter?
   - Strategy limitation: in what market regime is it likely to fail?
   - Event-driven specific: which events contributed the best and worst results? Is the return distribution skewed?
   - Portfolio-specific: is the rebalance frequency or deviation threshold sensible?

   Writing requirement: lead with the conclusion -> support it with concrete trade data -> if the result is poor, say so plainly instead of dressing it up. Parts A/B/C are all required; do not only write C and omit A/B. **Keep the answer concise.**

## On-Demand Loading

- `reference/pitfalls/pandas.md` — **mandatory read** (before writing code; strategy-backtest path)
- `reference/pitfalls/event_study.md` — mandatory for event studies when `event_overview_mode in {timeline, both}` (build the daily equity_curve)
- `reference/common_pitfalls.md` — **mandatory read** (self-check after coding)
- `reference/china_a_rules.md` — for A shares / ETFs / ST / T+1 / lot size / price limits / adjustment
- `reference/us_stock_rules.md` — for U.S. stocks
- `reference/hong_kong_rules.md` — for Hong Kong stocks
- `reference/accounting.py` — call rules in the top "Accounting Semantics" section; read the source only when something errors or you need to extend it
- `reference/short_leverage_routes.md` — mandatory only when the strategy includes shorting / leverage / margin / securities lending / explicit liabilities / borrow fees / financing interest
- `reference/export_results.py` — called by default after the backtest
- `examples/*.py` — when the query is clearly a known pattern such as moving averages / grid strategy
- `reference/dashboard_schema.md` — when generating a dashboard (JSON format, module types, replacement method)
- `reference/render_dashboard.py` — copyable dashboard example
- `reference/dashboard_locales.py` — **usually not needed**; it is an internal copy dependency of `render_dashboard.py`. Only look at it when adding custom copy or extending modules
- `reference/dashboard_template.html` — **do not read** (2000+ lines of CSS/JS intended for the browser; code only needs `open + replace`)

## Core Rules

### First Decide: Strategy Backtest or Event Study?

|                       | Strategy backtest                                                  | Event study                                                                      |
| --------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Typical query         | "Buy on MA golden cross and sell on death cross"                   | "Buy on the second day after a podcast release and hold for 30 days"             |
| Capital / positions   | Yes, e.g. 1,000,000 initial cash, compute portfolio equity         | **No**, compute price-change percentage directly                                 |
| Commission / lot size | Yes                                                                | **Default = no commission**, otherwise "average return" gets distorted           |
| Core metrics          | Portfolio-level: total return, annualized return, Sharpe, drawdown | **Event-level**: average return, median, win rate, max / min single-event result |
| `equity_curve`        | Portfolio NAV over time                                            | Can be omitted (or replaced with a virtual equal-weight curve)                   |
| `trades.csv`          | Paired entry/exit trades with monetary PnL                         | One row = one event; **`pnl_pct` is the core field**, not monetary PnL           |

### Mandatory Checklist by Scenario (Missing Items = Unreliable Results / Broken Dashboard)

After classifying the task, check the list below item by item. Each item points to where the detailed rule lives.

**Mandatory for strategy backtests**:

- [ ] Handle warmup exactly as defined in the "Warmup vs Evaluation Window" section: load earlier data, gate the evaluation start, and pass `export_results(..., start=..., end=...)`
- [ ] Handle suspension NaNs (see the suspension / mid-sample NaN section in `pitfalls/pandas.md`)
- [ ] Parameterize commissions and deduct them from PnL / equity (see the fees section in `pitfalls/pandas.md`)
- [ ] Force liquidation at the end of the sample (see the open-position handling section in `pitfalls/pandas.md`)
- [ ] Execute signals at next-day open (pending-signal pattern; prevents look-ahead)
- [ ] For A shares, pass `market="china_a"` so short trades hard-fail

**Mandatory for event studies**:

- [ ] **Every event must have a non-empty `label` field** (for example "PBOC rate cut by 25bp") — by default the main chart draws one marker per event row; without a label the user cannot interpret it
- [ ] **Every event must have a `source_url`** (news / filing / research-report link); leave empty only when no source can be found
- [ ] Do not simulate orders / commissions / pending signals; each event should directly become one trade row, with `pnl_pct` and `label` as the core fields, where `pnl_pct = (sell/buy - 1) * 100`
- [ ] Both the reply and the dashboard must use event-level metrics: average / median / win rate / best / worst event; **do not** report Sharpe / annualized return / max drawdown
- [ ] Use event-level metrics in `metric_table`, and custom `columns` in `trades_table` (event / buy date / sell date / return)
- [ ] **Event-study dashboards must pass `event_overview_mode` explicitly** instead of relying on inference: for average / median / win rate / best / worst event questions, pass `event_overview_mode="stats"`; for cumulative performance / curve / time-evolution questions, pass `event_overview_mode="timeline"`; if you want both stats and time evolution visible, pass `event_overview_mode="both"`
- [ ] **`timeline` / `both` modes must build a daily `equity_curve` yourself and pass it to render** (mark-to-market over each holding window + horizontal carry on flat days). Do not rely on the fallback that just connects exit-day points — see `pitfalls/event_study.md`
- [ ] **Default aggregation across concurrent events is equal-weight mean**. Only switch to sum when the user explicitly implies "equal dollar per event / total = sum / leverage / fully invested", and **state explicitly in your reply which aggregation you used**
- [ ] If the user's first question **did not** explicitly ask for cumulative / curve / time-evolution output and the current reply stays in `stats` mode, add one final sentence offering it: for example, "If you also want cumulative performance / a curve / time evolution, I can add a timeline view as well."
- [ ] If an `overview_chart` exists, validate before rendering that **the number of displayable event markers equals the number of event rows where `show_marker != False`**. If not, it means `event_date` (default = `entry_date`, but it may also be explicitly anchored to `exit_date`) does not align to chart `points.date`
- [ ] Do not call `export_results`; export requirements are defined in the "Standard Output Files" section and the event-study section of `dashboard_schema.md`

### How to Write Strategy-Backtest Code

- Use pure Python + pandas; do not use any backtesting framework
- The LLM is free to choose the code structure, but it **must** follow the patterns below:

**Separate signal generation from execution** (the core anti-look-ahead mechanism):

```text
bar i: generate signals using current and past data -> store in pending_buy / pending_sell
bar i+1: execute pending signals using the open price
```

**Signal-availability check (hard rule)**: every trade must satisfy `signal_time <= order_time <= fill_time`. If a condition uses `close`, full-day volume, daily `high/low`, or data released after the close, that condition is not available at the same bar's open or early intraday period, so it cannot justify same-bar-open execution. If the user asks for same-day-close execution, disclose it as a close-confirmed / close-fill assumption. If daily bars use `high` to trigger entry and `low` to trigger stop-loss on the same bar, disclose that the intrabar order is unknown and do not silently assume the favorable sequence.

**Script header contract (hard rule)**: every continuous-strategy script must declare `SIGNAL_TIMING`, `EXECUTION_TIMING`, and `EXECUTION_NOTE` at file top. The default is `bar_close / next_bar_open / "Signals are confirmed on bar close and filled on the next bar open."`; if the user explicitly accepts same-bar-close fills or intraday approximation, change the values and describe the assumption in `EXECUTION_NOTE`.

Do not "see the signal and fill immediately on the same bar" — on daily bars, that is effectively using the close as an execution price and is a look-ahead shortcut. The code structure should look like this:

```python
for i in range(len(df)):
    row = df.iloc[i]
    # 1. Execute yesterday's pending signal first
    if pending_buy:
        price = row['open']  # next-day-open fill
        ...
        pending_buy = False
    # 2. Generate today's signal (to be executed tomorrow)
    if buy_condition:
        pending_buy = True
    # 3. Record equity
    equity_curve.append({"date": date, "value": cash + position * row['close']})
```

**Indicator calculation**: use pandas vectorization. Do not hand-write `for` loops for MA / RSI / ATR:

```python
df['ma20'] = df['close'].rolling(20).mean()
df['rsi'] = ...  # can be written by hand or via ta-lib
```

`rolling()` creates NaNs for the first N-1 rows. Signal generation must skip them (for example `if pd.isna(row['ma20']): continue`).

**Equity calculation**: record account equity at the end of every bar. For simple single-name long-only strategies, `cash + position * close` is fine; for **cash equity / ETF** rotation, portfolio, rebalancing, short, and leverage strategies, prefer the unified form `cash + Σ(position_i × close_i)`. Represent short exposure with negative position size. If margin borrowing, stock borrow, or other leverage-related liabilities are **not already reflected in `cash`**, rewrite it as `cash + Σ(position_i × close_i) - liabilities`. Financing interest, borrow fee, and other costs must be explicitly reflected in `cash` or `liabilities`; do not leave them implicit. **This convention does not automatically cover futures, options, perpetuals, or other derivatives.** **Do not just write "record daily equity" without explaining the accounting convention.**

**Fees**: subtract `buy_commission` at buy time, and `sell_commission + sell_tax` at sell time. Use parameterized design (do not hardcode market-specific rates). PnL must be net of fees. See the fee section in `pitfalls/pandas.md`.

**Trade records**: every time a position is closed, append to `trade_history`. Fields must include: `entry_date, exit_date, side, size, entry_price, exit_price, pnl, pnl_pct, holding_bars, symbol`. PnL is net after commission. **Records must be written after execution, not when the signal is generated** (see `pitfalls/pandas.md`). For A shares / Hong Kong stocks, if the stock name is known, **prefer writing `symbol_name` inside `trade_history.append({...})` in the generated code**; if the code only has `name` / `stock_name` / `security_name` / `display_name`, `export_results` will normalize those aliases into the standard display fields, but do not rely on that fallback instead of the standard key. **Final dashboard display still follows the language lock**: under English output, China / Hong Kong stocks should default to ticker code; under Chinese output, known Chinese names should stay in Chinese.

**Lot-level implementation details** (constraints / triggers see top "Accounting Semantics" section):

- Lot fields produced by `buy_lot`: `lot_id, entry_date, entry_price, size, entry_bar, entry_fee`
- `buy_lot` does not auto-shrink an order; first estimate affordable shares with `cash / (price * (1 + buy_commission))`, floor by `lot_size`, and for fixed-cash buys use `target_cash = min(lot_cash, cash)` to avoid overdrawing cash
- Default sell uses `close_lots_fifo`; LIFO / grid per-level exit / custom matching uses `close_lot` in your own loop, and trade dict carries a `matching_note` field describing the rule
- A-share T+1 is checked per lot via `entry_bar`
- Multi-asset rotation uses `open_lots_by_symbol: dict[str, list[lot]]`, one list per symbol; `close_lots_fifo` MUST receive `symbol` or it raises
- Scaling / staged keyword recognition: user prompt "buy every signal / add / scale in / grid / staged entry / overlapping events" → relax the flat-position gate (still `lot_level + FIFO`); "sell half / reduce / staged take-profit / reduce to X%" → call `close_lots_fifo` with partial size in the sell block
- `position_accounting` stays `lot_level` — do not flip to `aggregate` just to keep the trade count looking small

**`enter_when_flat` assert template**: before the buy block save `prior_position` / `had_open_lots`; set `buy_executed=True` on an actual fill; immediately `assert not (prior_position > 0 and buy_executed)`. Repeated buy signals while holding may only increment `ignored_buy_signals`; never run `position +=` / `cash -= buy_cost` / `open_lots.append(...)` while exposed.

**`aggregate_average_cost` field details**: opt-in path uses `buy_average_cost / sell_average_cost / compute_position_equity`; trades carry no `lot_id`; `entry_price` is the average cost of the closed quantity; win rate is counted by aggregated close rows.

**Event studies do not call accounting.py** (no cash / position concept) — follow the event-study section under "Standard Output Files" and write each event's `trades.csv` row directly.

**Shorting / leverage**: see top "Short / leverage routing" — this section does not expand them.

**Helper signature reference** (do not read the source just to call them; only read on error or when extending):

```
# lot-level path
buy_lot(cash, *, lot_id, date, price, size, entry_bar,
        buy_commission=0.0, symbol="", **extra) → (cash, lot)
        # Compute an affordable size before calling (cash / fees / lot_size);
        # shrink or skip when cash is insufficient; helpers do not auto-shrink
        # **extra is merged into the lot dict and propagated by
        # close_lot / close_lots_fifo onto the produced trade record.
        # For China A / Hong Kong stocks with a known Chinese name, pass
        # symbol_name="..." here so the dashboard can display the name.
        # Also accepts trade_group_id / matching_note etc.

close_lots_fifo(open_lots, *, sell_size, date, price, exit_bar,
                sell_commission=0.0, sell_tax=0.0,
                symbol="", trade_group_id=None, t_plus_1=False)
        → (proceeds, trades, remaining_lots, unfilled)
        # When symbol is non-empty, filter lots by symbol; multi-asset MUST pass symbol or it raises

close_lot(lot, *, date, price, exit_bar, close_size,
          sell_commission=0.0, sell_tax=0.0,
          symbol="", trade_group_id=None)
        → (proceeds, trade, remaining_lot)
        # Atomic single-lot close; use it in your own loop for LIFO / sell-latest / grid-style
        # strategy-specific matching — do not use close_lots_fifo for those

compute_lot_equity(cash, open_lots, close_price) → equity

# aggregate-average-cost path
buy_average_cost(cash, *, position, avg_cost, date, price, size,
                 buy_commission=0.0)
        → (cash, new_position, new_avg_cost, info)

sell_average_cost(cash, *, position, avg_cost, date, price, size,
                  sell_commission=0.0, sell_tax=0.0,
                  symbol="", symbol_name="", entry_date="", entry_bar=None,
                  exit_bar=None, trade_group_id=None)
        → (cash, new_position, new_avg_cost, trade)

compute_position_equity(cash, position, close_price) → equity
```

Full usage example: `examples/scale_in_lot_level.py`. Hand-write accounting only when the helper cannot express a strategy-specific matching rule, and explain why.

**Forced liquidation at the end**: if there is still an open position on the final bar, **by default close it at the final bar's `close`**, record a trade, and subtract fees. In the final reply, explicitly say "the last trade is an end-of-sample forced close".

**Golden cross / death cross**: use the `(shift(1) <=) & (current >)` pattern to detect the crossing moment. Do not mistake a persistent state for an event.

### Strategy Logic

#### Warmup Segment vs Evaluation Segment (Mandatory for Indicator Strategies)

If the user says "Backtest the 2024 MA120 strategy", then `2024-01-01` is the **evaluation start**, not the **data-load start**. The first 119 rows of MA120 are NaN, so if you only load from the evaluation start, the first four months will have no valid signal. You **must** load an earlier warmup segment.

1. **Data-load start = evaluation start - max(indicator_window) × 1.5** (rule of thumb; MA120 -> 180 days earlier; EMA200 -> 300 days earlier; MA5 / MA10 only -> 15 days earlier). When calling the data source, `start_date` must use this earlier date, not the user-facing backtest range start
2. **Warmup bars must not create trading side effects, but they are not forbidden from updating all state**. Before the evaluation start, bars may continue to update indicators, streak counters, `highest_since_entry`, and similar **pure historical state**. But they **must not** create trades / equity records, and they must not create future-changing side effects such as `pending_buy/pending_sell=True` or cash/position changes
3. **`equity_curve` and `trade_history` should only record evaluation-window data**. When calling `export_results()`, you **must** pass `start / end` (= the evaluation window), so Sharpe / annualized return / total return / max drawdown are recomputed on the sliced evaluation window and not polluted by warmup

See `reference/pitfalls/pandas.md` for the full code skeleton and three typical wrong patterns.

#### Other Strategy Rules

- Under compound entry conditions, "reverse signal / reverse position" should by default be interpreted as the full mirrored condition. If ambiguous, clarify first
- When the user asks to "write the .py file and run it", the deliverable should be self-contained and runnable in the current environment. Do not hardcode personal paths and do not silently depend on undeclared external CSV files
- If the script depends on existing local CSV files, **do not assume the filename must equal `symbol`**; maintain an explicit `symbol -> file_path` mapping, or read the symbol from file contents
- **Short naming convention**: strategies that contain short exposure (U.S. / Hong Kong compliant shorting, or theoretical A-share shorting) must use the following field conventions. Otherwise dashboard rendering and export validation break:
  - `trade_history[i].side`: `"long"` for long trades (default), `"short"` for short trades
  - dashboard marker `action`: `"buy"` for opening a long, `"sell"` for closing a long, `"short"` for opening a short, `"cover"` for closing a short
  - the dashboard template recognizes these four actions and renders the corresponding marker types; `side="short"` is displayed as a short-side pill in `trades_table`

## Assumptions and Bias (Disclose in the Reply)

Any assumption the prompt did not specify but the code had to choose — and that affects how the result should be read — must be stated in plain language in the final reply. Do not bury it in code comments. Do not list internal field names / values, and do not default to expanding entry / accounting semantics.

High-frequency items to disclose:

- Position-sizing rule
- Fees / slippage / stamp duty
- Execution timing (next-day open / same-day close)
- Stop-loss / take-profit trigger semantics (intraday `high/low` approximation vs `close`-only)
- Warmup length vs evaluation length
- Whether A-share lot size / T+1 is enabled
- Adjustment method
- Universe source and data coverage

## Self-Check (Mandatory After Coding)

All 4 steps must be completed before delivery. **Step 3 cannot be skipped** — the checklist always lags behind, and adversarial review is there to catch bugs the checklist did not cover. **Step 4 cannot be skipped** — code without bugs still does not guarantee a correct dashboard.

### Step 1: Operability

1. **Script exists**: a task-specific `.py` file must exist in cwd; the run must not rely only on temporary command history
2. **Run in cwd**: `python <script>.py`. Fix any error immediately
3. **Three files exist**: `ls *_equity.csv *_trades.csv *_summary.json`. All must exist and be non-empty

### Step 2: The Checklist Table

Run the checklist table in `reference/common_pitfalls.md` row by row. Match item `1` against the user's original words, then execute the verification action described in each remaining row.

### Step 3: Sanity Check + Adversarial Review

If a number is outside common sense, you must find the root cause before delivery:

| Metric                                | Alarm threshold                               | Typical root cause                                                   |
| ------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| Sharpe / annualized return / win rate | > 3 / > 50% / > 70% (single symbol)           | missed look-ahead; forgot commission                                 |
| Max drawdown / Calmar                 | = 0 / > 5                                     | almost never in position; broken `equity_curve`; warmup pollution    |
| Total trades                          | < 3 or > 252 (per year)                       | signals never trigger (indicator NaN); treating a state as an event  |
| Average PnL                           | every trade exactly = ± stop or take-profit % | using `close` as the implementation price with no slippage variation |

**Inspect the first 5 and last 5 rows of `trades.csv`**: entry-price magnitude (Moutai should be around 1500, not 13000, or size may silently round to zero), holding-period distribution (all 1s or all identical values are suspicious), `side` (A-share long-only should not have `short`), and whether the first trade date falls inside the evaluation window.

**If there is a buy-and-hold baseline**: total return should be in the same order of magnitude as buy-and-hold (a 10x difference almost always means a bug). If the strategy is much better than buy-and-hold, you must be able to explain why.

**Adversarial review**: look for bugs the checklist did not cover. Temporarily forget the checklist and assume there is exactly one bug somewhere in the code. Read through the code from the top and ask four questions on every line:

- **Production realism**: could this data be known at decision time tomorrow? Is any time `t` decision using information from time `> t`?
- **Boundary values**: what happens when a variable is `None` / `0` / `nan` / negative / empty list? Is it silently swallowed or does it raise?
- **Mental arithmetic**: can the result of this line be checked by hand? If PnL = 100, can you reverse it from entry price / exit price / size?
- **Prompt sensitivity**: if one word in the prompt changes ("open" -> "close", "daily" -> "weekly", "liquidate fully" -> "sell half"), is this line still correct?

**High-risk auxiliary logic** (the signal itself is often fine; the bug usually hides here):

- Is size calculation using future data (`shift(-N)` / `iloc[i+1]`)? It should estimate size using the current bar's `close`
- Is stop-loss / take-profit based on `close` or `high/low`? Is the basis the entry price? Is simultaneous-trigger priority defined for the same bar?
- Is trailing-stop highest price updated before the stop check? That would miss valid triggers
- Warmup segment: are gating and `start/end` slicing handled exactly as defined in "Warmup vs Evaluation Window"?
- Does lot rounding produce `size = 0` with no explicit guard?
- Multi-strategy switching: when the higher-priority signal triggers, is the lower-priority holding handled correctly?
- Does a rebalance-frequency constraint belong to one strategy, or was it accidentally applied globally?

**If in doubt, verify**: run a minimal reproduction, grep it, compare with examples. Do not rely on mental confidence alone.

**Hard constraint**: if adversarial review concludes "I did not find anything", you must still list **at least 3 things you suspected and ruled out**. If you cannot list 3, redo the review.

**Bottom line**: if any step fails, do not deliver.

### Step 4: Post-Deploy Dashboard Self-Check

If a dashboard is part of the deliverable, then after `mshtools deploy` you **must complete** the "**[Mandatory] Post-Deploy Self-Check**" checklist from the HTML Dashboard section (rendering integrity + content compliance + performance). You must not hand the link to the user before this is done. This is an extension of self-check: bug-free code does not guarantee correct presentation.

- If `output_language="en"`, add one more check: both the final reply and the dashboard must contain **no Chinese user-visible text**; China / Hong Kong stocks can simply be displayed as ticker codes.

## Standard Output Files (Formal Export Contract)

First distinguish the scenario:

- **Strategy backtest**: after the backtest completes, always generate 3 files into the current working directory (`cwd`). Use a prefix such as `ma_cross_600519`
- **Event study**: do **not** use the portfolio-style summary export. Write `trades.csv` manually, and compute event-level metrics from `pnl_pct`. Do not fabricate Sharpe / annualized return / max drawdown

The 3 standard files for strategy backtests are:

| File                    | Content                | Columns / fields                                                                                                                                                                                                                                                              |
| ----------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<prefix>_equity.csv`   | per-bar equity         | `date, value`                                                                                                                                                                                                                                                                 |
| `<prefix>_trades.csv`   | closed trades          | required (default lot_level): `entry_date, exit_date, side, size, entry_price, exit_price, pnl, pnl_pct, holding_bars, symbol, lot_id`; optional: `symbol_name`, `display_symbol`, `trade_group_id`, `matching_note`, `borrow_fee`, `margin_required`, `return_on_margin_pct` |
| `<prefix>_summary.json` | summary metrics + meta | `meta: {strategy_name, symbol, start, end, initial_cash, window_start_value, final_value, market, position_accounting, position_accounting_note, generated_at}`<br>`summary: {total_return_pct, annual_return_pct, max_drawdown_pct, sharpe, win_rate_pct, total_trades}`     |

Implementation for strategy backtests: call `reference/export_results.py` via `export_results(equity_curve, trade_history, prefix, initial_cash, start, end, market, is_flat_at_end=True, ...)`:

- `equity_curve`: `[{"date": "2024-01-02", "value": 1000000.0}, ...]`
- `trade_history`: `[{"entry_date": ..., "exit_date": ..., "side": "long", "size": 100, "symbol": "600519.SH", "symbol_name": "Kweichow Moutai", ...}, ...]`
- If warmup exists, the `start/end` logic is defined in the "Warmup vs Evaluation Window" section. Export will slice to the evaluation window and recompute Sharpe / annualized return / total return / max drawdown
- For A shares, pass `market="china_a"` to trigger short hard-fail
- You must pass `is_flat_at_end=True`; `position_accounting` defaults to `"lot_level"`, opt in to `"aggregate_average_cost"` only with explicit user request
- Files must be written directly into `cwd`; do not create a subdirectory

## HTML Dashboard

### Unified UI Iron Rules (Violation = Invalid Output)

| #   | Rule                                                                                   | Violation example                                                                                                           |
| --- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | **All HTML must be rendered through `render_dashboard()` + `dashboard_template.html`** | Handwritten index.html navigation page, custom landing page, or any HTML file not generated through `render_dashboard()`    |
| 2   | **The visual system is entirely provided by the template**                             | Custom CSS/JS, custom overall styling, or a layout / color system that departs from the template                            |
| 3   | **Standalone visual-style pages are forbidden**                                        | Any HTML page that is not rendered from `dashboard_template.html`, including navigation pages, index pages, or router pages |

**The model does not need to read `dashboard_template.html` itself** (2000+ lines of CSS/JS are for the browser). It only needs to build the `report_data` dict and call `render_dashboard(report_data, output_path, template_path)`.

**Naming rule**:

- In the single-HTML case, the final main dashboard file name is fixed to `index.html`
- If multiple HTML files are truly needed, the entry page must still be named `index.html`; only the detail pages may use per-symbol / per-strategy names

### Single HTML vs Multiple HTML Files

This section is **layout strategy** and takes precedence here. `reference/dashboard_schema.md` mainly defines module schema, field semantics, and recipes for non-typical backtests.

**Default recommendation: single HTML + tabs**

- Use `ui.tabs` to configure multiple tabs, one per symbol
- Main-chart choice: for **portfolio-style / natural-mainline** cases (position weights, rebalancing, **multi-symbol rotation** — dynamically rotating across N symbols under one strategy), use `overview_chart` to draw the **portfolio NAV** as the main line, optionally with `overlay_series` as supporting lines. For **peer comparison / no natural main line** cases (one strategy across many stocks, or many strategies on one stock), use `line_chart` (peer lines) + `metric_table` (one comparison object per column). **Do not force such cases into `overview_chart`**, because that visually promotes one series into the "main line." Rotation strategies must not be misread as peer comparisons; the portfolio-level NAV is the true mainline
- **Standard layout for peer-comparison scenarios (hard rule)** — applies to both "many stocks, one strategy" and "many strategies, one stock":
  - Tab 1 `"Comparison"` (`ui.active_tab` by default): `line_chart` multi-line comparison + `metric_table` KPI comparison by column (event studies use event-level metrics; strategy backtests use Sharpe / return / drawdown, etc.)
  - Tab 2+ **one tab per comparison target**: `overview_chart` for that target's equity curve (with buy/sell markers and drawdown pane) + `trades_table` for its detailed trades
  - **You may not provide only the comparison chart without per-target detail**, because users will want to click into one specific line
- Best fit when the number of symbols is `<= 10`, content complexity is moderate, and the file stays under 5 MB

**Multiple HTML files are allowed (model decides)**

- When the symbol count is large, a single page is overloaded, or each symbol requires a fully independent detailed view
- **Each symbol HTML** must still be rendered through `dashboard_template.html`
- **Navigation / index page (if needed)** must also be rendered through `dashboard_template.html`, using standard modules such as:
  - `metric_table` — side-by-side comparison across symbols
  - `custom_html` — card grid, link list (DOM class names must use the `bt-custom-` prefix)
  - `overview_chart` + `overlay_series` — overlay multiple equity curves
- **Do not** handwrite a custom navigation page, and do not link multiple HTML pages together via raw `<a href>`

### Implementation Notes

- The dashboard is **only a display layer**; the formal export contract is defined in the "Standard Output Files" section
- The default base dashboard contains: equity curve, PnL curve, drawdown curve, trade history, Sharpe, win rate, and buy/sell markers on the main chart
- `reference/render_dashboard.py` is a **copyable example** — it demonstrates the minimal path of "read standard output files -> build dict -> replace `dashboard_template.html` placeholders -> output HTML"; if you copy it, copy `reference/dashboard_locales.py` too
- When calling `render_dashboard(...)`, default the main dashboard `output_path` to `index.html`
- Default sequence: complete formal export first, then render the HTML
- As long as the backtest actually ran and the user did not explicitly opt out of the dashboard, generate a local HTML dashboard by default
- After generating the HTML dashboard, you **must** call `mshtools deploy` so the user can access it by link

#### **[Mandatory] Post-Deploy Self-Check — No Self-Check = No Delivery**

After deployment, you **must** open the deployed link in a browser / screenshot tool and confirm the following items one by one. All must pass before delivery. If any item fails, fix it immediately, redeploy, and recheck.

**Rendering integrity checks (mandatory)**:

- [ ] The main chart (equity / PnL) has real data and is not blank or a single flat line
- [ ] KPI cards (total return, max drawdown, number of trades, win rate, Sharpe) contain values and are not `"--"`
- [ ] The browser console has no errors

**Content compliance checks (mandatory)**:

- [ ] No irrelevant modules are present for the current query (for example, no Sharpe / annualized return / max drawdown in an event study)
- [ ] `trades_table` column names match the task (event studies should use "Event / Buy Date / Sell Date / Return", not the default "Entry / Exit")
- [ ] All text is consistent with the dashboard `language`, and that language matches the user's query (an English question about Chinese stocks must not produce Chinese module titles)
- [ ] **All HTML files are rendered from `dashboard_template.html`** — grep the code and confirm every `.html` is generated through `render_dashboard()`, with no handwritten page
- [ ] There is no handwritten standalone navigation / index page — if navigation is needed, it must be injected through standard `custom_html` / `metric_table` modules

**Performance checks (mandatory when file size > 5 MB)**:

- [ ] The page loads smoothly and does not white-screen. If `equity_curve` has too many points (`>5000`) or markers are too many (`>200`), you **must** downsample or simplify and regenerate before redeploying

**Mandatory rerun chain after bug fixes**:
fix code -> rerun backtest -> regenerate 3 files -> rerender -> redeploy via `mshtools deploy` -> **rerun the full self-check**. Skipping any step means the user still sees the old broken version.

### Scenario-Specific Notes

- Event-driven / stock-selection / portfolio-allocation tasks **must also produce dashboards**. Do not skip the dashboard just because you cannot build a continuous NAV; recipes are defined in the "Non-Typical Backtests" section of `reference/dashboard_schema.md`
- ⚠️ **Hard rule (violation = invalid dashboard)**: in an event study, each entry in `trade_history` **must include a non-empty `label` field** (event description). Without `label`, the event markers on the main chart are unreadable and the dashboard loses the core value of an event study
- Other event-study adaptations are not repeated here. Follow the earlier "Event Study Must-Do Checklist", and use `reference/dashboard_schema.md` for concrete module recipes

## Matplotlib Charts (Standalone PNG)

After the backtest, generate standalone PNGs into cwd: file names `<prefix>_<name>.png`, titles and labels follow the user's language. Typically 3-6 charts covering equity, drawdown, trade distribution, and strategy-specific views; call `plt.show()` before `plt.savefig()`; do not embed static charts into the HTML.

## Data Sources (Mandatory)

- **Market data**: prefer `mshtools` datasource; do not hardcode prices
- **Universe / screening**: prefer `ifind` inside `mshtools`; do not hand-craft the universe, and do not use CSI 300 / CSI 500 as a whole-market proxy
- **Reuse local data when complete**: cwd-resident CSV / parquet can be read directly; if dates or fields are incomplete, fall back to the real source instead of silently substituting
- If `mshtools` / `ifind` truly cannot provide what you need, fall back and disclose in the reply
