#!/usr/bin/env python3
"""
Chart Embedding Utility — Equity Research Report

Embeds SVG charts into HTML reports as base64-encoded images.
Also provides chart counting and validation.

Usage:
    python embed_charts.py --html report.html --chart_dir ./charts --json
    python embed_charts.py --html report.html --count_only
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path


def svg_to_base64(svg_path: str) -> str:
    """Read SVG file and return base64-encoded string."""
    with open(svg_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def embed_charts_in_html(html_content: str, chart_dir: str) -> str:
    """Replace chart placeholders in HTML with base64-embedded SVGs."""
    chart_path = Path(chart_dir)
    if not chart_path.exists():
        return html_content

    # Find placeholder patterns like {{C1_IMG_TAG}}, {{chart_name}}, etc.
    placeholder_pattern = re.compile(r"\{\{(\w+)\}\}")

    def replace_placeholder(match):
        name = match.group(1)
        # Look for SVG file with matching name
        svg_candidates = list(chart_path.glob(f"{name}*.svg")) + list(chart_path.glob(f"*{name}*.svg"))
        if svg_candidates:
            svg_file = svg_candidates[0]
            try:
                b64 = svg_to_base64(str(svg_file))
                return f'<img src="data:image/svg+xml;base64,{b64}" alt="{name}" style="max-width:100%;height:auto;" />'
            except Exception:
                return f"<!-- Failed to embed {name}: {svg_file} -->"
        return f"<!-- Chart placeholder not found: {name} -->"

    return placeholder_pattern.sub(replace_placeholder, html_content)


def count_embedded_charts(html_content: str) -> dict:
    """Count embedded charts in HTML content."""
    base64_count = html_content.count("data:image/svg+xml;base64,")
    img_tags = len(re.findall(r'<img[^>]*src="data:image', html_content))
    placeholders = len(re.findall(r"\{\{\w+\}\}", html_content))
    return {
        "base64_embedded": base64_count,
        "img_tags_with_base64": img_tags,
        "unresolved_placeholders": placeholders,
    }


def main():
    parser = argparse.ArgumentParser(description="Embed charts into HTML report")
    parser.add_argument("--html", required=True, help="Path to HTML file")
    parser.add_argument("--chart_dir", default="./charts", help="Directory containing chart SVG files")
    parser.add_argument("--count_only", action="store_true", help="Only count embedded charts")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        result = {"success": False, "error": f"File not found: {args.html}"}
        print(json.dumps(result) if args.json else f"Error: {args.html} not found", file=sys.stderr)
        sys.exit(1)

    html_content = html_path.read_text(encoding="utf-8")

    if args.count_only:
        stats = count_embedded_charts(html_content)
        if args.json:
            print(json.dumps(stats))
        else:
            for k, v in stats.items():
                print(f"{k}: {v}")
        return

    # Embed charts
    updated_html = embed_charts_in_html(html_content, args.chart_dir)
    stats = count_embedded_charts(updated_html)

    # Write updated HTML
    html_path.write_text(updated_html, encoding="utf-8")

    result = {
        "success": True,
        "file": str(html_path),
        "embedded": stats["base64_embedded"],
        "unresolved": stats["unresolved_placeholders"],
    }
    if args.json:
        print(json.dumps(result))
    else:
        print(f"Embedded {result['embedded']} charts. Unresolved placeholders: {result['unresolved']}")


if __name__ == "__main__":
    main()
