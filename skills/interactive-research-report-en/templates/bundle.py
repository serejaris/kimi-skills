#!/usr/bin/env python3
"""Bundle the site into a single self-contained HTML (for artifact/preview delivery).
Inlines css/style.css, all <script src> files (vendor + js), in original order.
Usage: python3 tools/bundle.py [outfile]
"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# inline stylesheets (any <link rel="stylesheet" href="css/...">)
def css_repl(m):
    css = open(os.path.join(ROOT, m.group(1)), encoding="utf-8").read()
    return "<style>\n" + css + "\n</style>"
html = re.sub(r'<link rel="stylesheet" href="(css/[^"]+)">', css_repl, html)

# inline land topojson as a global (dashboard fetches it at runtime)
land = open(os.path.join(ROOT, "vendor/land-110m.json"), encoding="utf-8").read()
html = html.replace('<script src="vendor/d3.min.js"></script>',
                    '<script src="vendor/d3.min.js"></script>\n<script>window.__LAND110M=' + land + ';</script>')

# inline scripts in order
def repl(m):
    src = m.group(1)
    p = os.path.join(ROOT, src)
    code = open(p, encoding="utf-8").read()
    if src.endswith("dashboard.js"):
        code = code.replace('fetch("vendor/land-110m.json").then(r => r.json())',
                            'Promise.resolve(window.__LAND110M || fetch("vendor/land-110m.json").then(r => r.json()))')
    return "<script>\n" + code + "\n</script>"

html = re.sub(r'<script src="([^"]+)"></script>', repl, html)

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist-single.html")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
open(out, "w", encoding="utf-8").write(html)
print(out, len(html), "bytes")
