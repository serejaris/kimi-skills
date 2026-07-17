#!/usr/bin/env python3
"""
Chart Generator — Equity Research Report

Generates 5 chart types for equity reports:
- revenue_segment: Stacked bar chart of revenue by segment
- margin_trends: Multi-line chart of gross/operating/net margins
- market_share: Pie/donut chart of market share distribution
- pe_band: Historical PE band with percentile shading
- scenario_comparison: Grouped bar chart of Bull/Base/Bear scenarios

Usage:
    python chart_generator.py --chart_type revenue_segment --data '{"labels": [...], "datasets": [...]}' --output chart.svg --json
"""

import argparse
import json
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def generate_revenue_segment(data: dict, output_path: str) -> str:
    """Generate stacked bar chart for revenue by segment."""
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = data.get("labels", [])
    datasets = data.get("datasets", [])
    bottom = np.zeros(len(labels))
    for ds in datasets:
        ax.bar(labels, ds["values"], bottom=bottom, label=ds["label"], width=0.6)
        bottom += np.array(ds["values"])
    ax.set_title("Revenue by Segment", fontsize=14, fontweight="bold")
    ax.set_ylabel("Revenue (M)", fontsize=11)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


def generate_margin_trends(data: dict, output_path: str) -> str:
    """Generate multi-line chart for margin trends."""
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = data.get("labels", [])
    for ds in data.get("datasets", []):
        ax.plot(labels, ds["values"], marker="o", label=ds["label"], linewidth=2)
    ax.set_title("Margin Trends", fontsize=14, fontweight="bold")
    ax.set_ylabel("Margin (%)", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


def generate_market_share(data: dict, output_path: str) -> str:
    """Generate pie chart for market share."""
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = data.get("labels", [])
    values = data.get("values", [])
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    explode = [0.05 if i == 0 else 0 for i in range(len(labels))]
    ax.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, explode=explode, startangle=90)
    ax.set_title("Market Share", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


def generate_pe_band(data: dict, output_path: str) -> str:
    """Generate historical PE band chart."""
    fig, ax = plt.subplots(figsize=(10, 5))
    dates = data.get("dates", [])
    pe = data.get("pe_values", [])
    mean = data.get("mean", [])
    upper = data.get("upper_band", [])
    lower = data.get("lower_band", [])
    ax.fill_between(dates, upper, lower, alpha=0.2, label="±1 SD")
    ax.plot(dates, mean, "--", label="Mean", color="gray")
    ax.plot(dates, pe, label="P/E", color="#003366", linewidth=1.5)
    ax.set_title("Historical PE Band (5Y)", fontsize=14, fontweight="bold")
    ax.set_ylabel("P/E Ratio", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


def generate_scenario_comparison(data: dict, output_path: str) -> str:
    """Generate grouped bar chart for scenario comparison."""
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = data.get("metrics", [])
    scenarios = data.get("scenarios", [])
    x = np.arange(len(labels))
    width = 0.25
    colors = ["#2E7D32", "#003366", "#B71C1C"]
    for i, sc in enumerate(scenarios):
        offset = width * (i - 1)
        ax.bar(x + offset, sc["values"], width, label=sc["name"], color=colors[i % len(colors)])
    ax.set_title("Scenario Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.legend(loc="best", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, format="svg")
    plt.close(fig)
    return output_path


CHART_FUNCTIONS = {
    "revenue_segment": generate_revenue_segment,
    "margin_trends": generate_margin_trends,
    "market_share": generate_market_share,
    "pe_band": generate_pe_band,
    "scenario_comparison": generate_scenario_comparison,
}


def main():
    parser = argparse.ArgumentParser(description="Generate equity research charts")
    parser.add_argument("--chart_type", required=True, choices=list(CHART_FUNCTIONS.keys()))
    parser.add_argument("--data", required=True, help="JSON string with chart data")
    parser.add_argument("--output", required=True, help="Output SVG file path")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON data — {e}", file=sys.stderr)
        sys.exit(1)

    func = CHART_FUNCTIONS[args.chart_type]
    try:
        result = func(data, args.output)
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
