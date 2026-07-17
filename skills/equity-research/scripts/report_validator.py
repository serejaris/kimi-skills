#!/usr/bin/env python3
"""
Report Validator — Equity Research Report

Validates HTML report structure before PDF generation.
Checks: HTML integrity, section sequence, module count, exhibit count, data source presence.

Usage:
    python report_validator.py --html report.html --json
    python report_validator.py --html report.html --output_type equity_report --json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def validate_html(html_content: str, output_type: str = "equity_report") -> dict:
    """Validate HTML report content."""
    errors = []
    warnings = []

    # 1. HTML structure
    body_count = html_content.lower().count("</body>")
    html_count = html_content.lower().count("</html>")
    if body_count != 1:
        errors.append(f"HTML integrity: found {body_count} </body> tags (expected 1)")
    if html_count != 1:
        errors.append(f"HTML integrity: found {html_count} </html> tags (expected 1)")

    # 2. CSS class presence
    if ".report-container" not in html_content and "report-container" not in html_content:
        errors.append("Missing .report-container CSS class")

    # 3. Cover page elements
    if "cover-split" not in html_content:
        errors.append("Missing cover-split element (cover page)")
    if "kimi-brand-bar" not in html_content:
        warnings.append("Missing kimi-brand-bar element (Kimi Research branding)")

    # 4. Section/module count
    module_count = len(re.findall(r'<div class="module-row"', html_content))
    if output_type == "equity_report":
        if module_count < 18:
            errors.append(f"Module count: {module_count} modules (expected ≥18 for equity report)")
    else:  # tear sheet
        if module_count < 8:
            errors.append(f"Module count: {module_count} modules (expected ≥8 for tear sheet)")

    # 5. Exhibit count
    exhibit_count = len(re.findall(r'class="exhibit-label"', html_content))
    if output_type == "equity_report":
        if exhibit_count < 15:
            warnings.append(f"Exhibit count: {exhibit_count} (recommended ≥15)")
    else:
        if exhibit_count < 5:
            warnings.append(f"Exhibit count: {exhibit_count} (recommended ≥5)")

    # 6. Data sources section
    if "references-list" not in html_content:
        warnings.append("Missing references-list (data sources section)")

    # 7. Investment thesis table
    if "debate-table" not in html_content:
        errors.append("Missing debate-table (investment thesis table)")

    # 8. Executive summary
    if "exec-summary" not in html_content:
        errors.append("Missing exec-summary (executive summary)")

    # 9. Chart embedding
    chart_count = html_content.count("data:image/svg+xml;base64,")
    if output_type == "equity_report":
        if chart_count < 3:
            warnings.append(f"Embedded charts: {chart_count} (recommended ≥3)")

    # 10. Mermaid check (no raw Mermaid in PDF output)
    if '<pre class="mermaid">' in html_content:
        errors.append("Raw Mermaid code detected — must pre-render to SVG before embedding")
    if '<script src="mermaid' in html_content:
        errors.append("Mermaid script tag detected — PDF renderers do not execute JavaScript")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "body_count": body_count,
            "html_count": html_count,
            "module_count": module_count,
            "exhibit_count": exhibit_count,
            "chart_count": chart_count,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Validate equity research HTML report")
    parser.add_argument("--html", required=True, help="Path to HTML file")
    parser.add_argument("--output_type", default="equity_report", choices=["equity_report", "tear_sheet"])
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        result = {"valid": False, "errors": [f"File not found: {args.html}"], "warnings": [], "stats": {}}
        if args.json:
            print(json.dumps(result))
        else:
            print(f"Error: {args.html} not found", file=sys.stderr)
        sys.exit(1)

    html_content = html_path.read_text(encoding="utf-8")
    result = validate_html(html_content, args.output_type)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Validation: {'PASSED' if result['valid'] else 'FAILED'}")
        print(f"Errors: {len(result['errors'])}, Warnings: {len(result['warnings'])}")
        for e in result["errors"]:
            print(f"  [ERROR] {e}")
        for w in result["warnings"]:
            print(f"  [WARN] {w}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
