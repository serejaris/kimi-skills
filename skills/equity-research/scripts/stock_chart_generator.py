#!/usr/bin/env python3
"""
Stock Chart Generator — Tear Sheet / Equity Report

Generates 52-week stock price chart with benchmark overlay.
Used by both Tear Sheet and Equity Report workflows.

Usage:
    python stock_chart_generator.py --stock_csv stock.csv --benchmark_csv bench.csv --output chart.svg --json

Input CSV format (stock): date, close, volume
Input CSV format (benchmark): date, close
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def generate_stock_chart(stock_csv: str, benchmark_csv: str, output_path: str) -> str:
    """Generate 52-week stock chart with benchmark overlay."""
    # Load data
    stock_df = pd.read_csv(stock_csv, parse_dates=["date"])
    bench_df = pd.read_csv(benchmark_csv, parse_dates=["date"])

    # Rebase benchmark to stock's start price
    stock_start = stock_df["close"].iloc[0]
    bench_start = bench_df["close"].iloc[0]
    bench_df["rebased"] = bench_df["close"] / bench_start * stock_start

    # Merge on date
    merged = pd.merge(stock_df, bench_df[["date", "rebased"]], on="date", how="left")

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Stock price line
    ax1.plot(merged["date"], merged["close"], color="#003366", linewidth=1.8, label="Stock")
    # Benchmark line
    ax1.plot(merged["date"], merged["rebased"], color="#888", linewidth=1.2, linestyle="--", label="Benchmark")

    # 52-week high/low
    w52_high = merged["close"].max()
    w52_low = merged["close"].min()
    ax1.axhline(y=w52_high, color="#2E7D32", linestyle=":", alpha=0.5, label=f"52W High: {w52_high:.2f}")
    ax1.axhline(y=w52_low, color="#B71C1C", linestyle=":", alpha=0.5, label=f"52W Low: {w52_low:.2f}")

    ax1.set_title("Stock Price vs Benchmark (52 Weeks)", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price", fontsize=11)
    ax1.legend(loc="best", fontsize=9)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Volume bars (if available)
    if "volume" in merged.columns and merged["volume"].notna().sum() > 0:
        ax2 = ax1.twinx()
        ax2.bar(merged["date"], merged["volume"], alpha=0.15, color="#888", width=1)
        ax2.set_ylabel("Volume", fontsize=10, color="#888")
        ax2.tick_params(axis="y", labelcolor="#888")

    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate stock price chart")
    parser.add_argument("--stock_csv", required=True, help="Path to stock price CSV")
    parser.add_argument("--benchmark_csv", required=True, help="Path to benchmark CSV")
    parser.add_argument("--output", required=True, help="Output SVG file path")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    for f in [args.stock_csv, args.benchmark_csv]:
        if not Path(f).exists():
            result = {"success": False, "error": f"File not found: {f}"}
            print(json.dumps(result) if args.json else f"Error: {f} not found", file=sys.stderr)
            sys.exit(1)

    try:
        result = generate_stock_chart(args.stock_csv, args.benchmark_csv, args.output)
        if args.json:
            print(json.dumps({"success": True, "output_path": result}))
        else:
            print(f"Chart saved to: {result}")
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Error generating chart: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
