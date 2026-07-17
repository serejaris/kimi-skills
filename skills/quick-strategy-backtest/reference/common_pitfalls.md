# Common Mistakes and Correct Patterns — Checklist

Read [`reference/pitfalls/pandas.md`](./pitfalls/pandas.md) before writing code. After the code is written, use the table below as the delivery gate. This file keeps only the checklist; the detailed explanation and code patterns stay in `pandas.md`.

## Pre-Delivery Checklist

| ID | Check | How to verify | Pass condition | See `pandas.md` |
|---|---|---|---|---|
| `1` | Query alignment | Compare the code line by line with the user's request | Entry/exit rules, sizing, stops, execution timing, and universe all match; every default choice is disclosed in the final reply | `Look-Ahead Bias`, `Trade Records Must Be Written After Execution`, `Warmup Period` |
| `1b` | Script persisted | Confirm a task-specific `.py` exists in cwd and actually run `python <script>.py` | Results come from the script run, not from a temporary REPL / notebook / shell snippet | `Look-Ahead Bias` |
| `2` | No future data | For every order / selection / rebalance / stop-loss / take-profit / sizing decision, walk through the 4 Assessment Questions in `pandas.md` "Look-Ahead Bias" (index / window / cross-section / data visibility) | All four questions are answered "safe" at every decision point; hits are explained or fixed. A clean appendix grep does not equal four passes — the manual walk is still required | `Look-Ahead Bias` |
| `3` | Signal availability time | Confirm `signal_time <= order_time <= fill_time` trade by trade | Decision-time availability holds. The detailed rules (same-bar-open availability, close-fill disclosure, intrabar high/low ordering) live in `pandas.md` "Look-Ahead Bias" → signal availability section | `Look-Ahead Bias`, `Trade Records Must Be Written After Execution` |
| `4` | `size > 0` | Grep all order-placement logic and inspect the guard immediately above it | No path silently skips trades because `size=0` under high price / low capital | `Position Sizing + size > 0` |
| `4b` | `enter_when_flat` gate | Grep `position +=`, `cash -=`, `open_lots.append`, `avg_cost`, and similar buy execution paths | Every buy block is protected by a flat-position condition; repeated buy signals only increment ignored counters; runtime guard exists and is meaningful | `Trade Records Must Be Written After Execution`, `Scaling In / Out Must Not Overwrite Entry State` |
| `5` | Warmup segment is correct | Check data-load start, evaluation-start gate, `export_results(start/end)`, and `is_flat_at_end=True` | Warmup bars do not contaminate trades/equity; indicators have enough lookback; export window and accounting semantics are explicit | `Warmup Period` |
| `6` | Output language is consistent | Read the dashboard, chart titles, custom HTML, and the final reply | Everything follows the query language; an English query about Chinese stocks does not switch back to Chinese | `Trade Records Must Be Written After Execution` |

## How To Use This File

- Use `pandas.md` to learn the rule and the correct code shape.
- Come back to this table and execute the verification step row by row.
- If any row cannot be confidently checked off, do not deliver.
