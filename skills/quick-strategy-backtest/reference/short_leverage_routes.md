# Short / Leverage

Use this file only for pure-Python cash equity / ETF strategies that include shorting, margin buys, securities lending, negative cash, explicit liabilities, borrow fees, financing interest, or margin checks. Ordinary long-only strategies should not read this file; use the default long-only lot-level semantics in `SKILL.md`.

## Route Table

| Scenario                                                 | Core helpers                   |
| -------------------------------------------------------- | ------------------------------ |
| Open a short                                             | `short_lot`                    |
| Cover shorts by FIFO                                     | `cover_short_lots_fifo`        |
| Cover one specified short lot / partial cover            | `cover_short_lot`              |
| Margin buy / cash shortfall becomes liability            | `buy_lot_with_margin`          |
| Lot-level equity for long + short + explicit liabilities | `compute_lot_portfolio_equity` |
| Aggregate long/short portfolio equity                    | `compute_portfolio_equity`     |
| Required margin                                          | `compute_required_margin`      |
| Margin sufficiency check                                 | `check_margin_requirement`     |
| Accrue financing interest                                | `accrue_liability_interest`    |
| Borrow fee / financing fee calculation                   | `compute_borrow_fee`           |

## Helper Signature Reference

Do not read the source just to call them; only read on errors or when extending.

```
# Short open / cover
short_lot(cash, *, lot_id, date, price, size, entry_bar,
          short_commission=0.0, margin_rate=0.5, symbol="", **extra)
        → (cash, short_lot)
        # Opening a short increases cash by entry_notional - entry_fee;
        # margin_rate is metadata only — no margin enforcement here;
        # use compute_required_margin to check.
        # **extra is merged into the short lot and propagated by
        # cover_short_lot{,s_fifo} onto the produced trade record.
        # For China A / Hong Kong stocks pass symbol_name="..." here.

cover_short_lots_fifo(open_short_lots, *, cover_size, date, price, exit_bar,
                      cover_commission=0.0, borrow_fee=0.0,
                      symbol="", trade_group_id=None, t_plus_1=False)
        → (cash_delta, trades, remaining_lots, unfilled)
        # borrow_fee is the total fee for this cover order, allocated
        # by close_size/cover_size across covered lots.
        # Multi-asset MUST pass symbol or it raises.

cover_short_lot(lot, *, date, price, exit_bar=None, cover_size=None,
                cover_commission=0.0, borrow_fee=0.0,
                symbol=None, trade_group_id=None)
        → (cash_delta, trade, remaining_lot)
        # Atomic single-lot cover; use it in your own loop for custom matching.

# Margin buy
buy_lot_with_margin(cash, liabilities, *, lot_id, date, price, size,
                    entry_bar, buy_commission=0.0, symbol="",
                    max_liabilities=None, **extra)
        → (cash, liabilities, lot)
        # Cash shortfall is auto-borrowed into liabilities; cash must be ≥ 0
        # or it raises. No maintenance margin / liquidation enforced here;
        # use check_margin_requirement to monitor.

# Equity / margin
compute_lot_portfolio_equity(cash, *, long_lots=None, short_lots=None,
                             prices=None, default_price=None,
                             liabilities=0.0) → equity
        # equity = cash - liabilities + Σ(long_lot.size × price)
        #                              - Σ(short_lot.size × price)
        # Multi-asset: pass prices: dict[symbol, price]; single asset: default_price.

compute_portfolio_equity(cash, positions, prices, *, liabilities=0.0) → equity
        # Aggregate version; positions is dict[symbol, signed_qty];
        # shorts use negative quantities.

compute_required_margin(positions, prices, *,
                        long_margin_rate=0.5, short_margin_rate=0.5)
        → required_margin

check_margin_requirement(equity, required_margin)
        → (is_satisfied, excess_equity)

# Interest / borrow fee
accrue_liability_interest(liabilities, *, annual_rate,
                          days=1, day_count=365)
        → (new_liabilities, interest)

compute_borrow_fee(notional, *, annual_rate, days=1, day_count=365)
        → borrow_fee
```

## Accounting Assumptions Required First

The short / leverage helpers provide basic ledgers, explicit liabilities, interest, and margin checks. They are not a full broker margin engine. Before implementation, define:

- how short exposure is represented and how short / cover changes cash
- whether `liabilities` are tracked separately
- margin rates, whether margin is checked, and what happens on failure
- financing interest, borrow fee, holding days, and day count
- daily equity formula
- PnL convention for `trade_history.side="short"`

If the user has not specified these conditions, trigger the Clarification Gate first.

## Output Fields

Short-cover or financing trades may write:

- `borrow_fee`
- `margin_required`
- `return_on_margin_pct`

`export_results` writes these columns, and `render_dashboard` loads them as numbers. Whether the default dashboard table displays them depends on the table columns.
