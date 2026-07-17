#!/usr/bin/env python3
"""
Anti-AI frequency scanner for Chinese creative prose (anti-ai.md §六).
Stdlib only. Scans the FREQUENCY tells that the eye normalizes while
drafting; pattern tells (§一–§五) still need a manual pass.

Usage:
  python scan_anti_ai.py <file> [--ref <source_file>]

Without --ref: judge against the default thresholds (per 1000 CJK chars /
per work). With --ref (continuation/adaptation tasks): also report the
reference's rates and flag any tell whose rate drifts beyond ±50% of it,
plus quote-style mismatch.

Output: one line per check —  OK / WARN / FAIL  name  measured (threshold)
Exit code: 0 = no FAIL, 1 = any FAIL or error.
"""

import re
import sys
from pathlib import Path

# name, regex, per-1000-char cap (None → per-work cap in WORK_CAPS)
RATE_CHECKS = [
    ('明喻引导词', r'像是|好像|仿佛|如同|宛如|宛若|犹如|好似|(?<![好想象映图])像(?![素章片机样])', 3.0),
    ('破折号', r'——', 2.0),
    ('tic词(缓缓/微微/轻轻/淡淡/嘴角)', r'缓缓|微微|轻轻(?!松)|淡淡|嘴角', 5.0),
    ('不是X而是Y族', r'不是[^。！？\n]{1,18}而是|并非[^。！？\n]{1,18}而是|没有[^。！？\n]{1,18}只有', 1.0),
]
WORK_CAPS = [
    ('hedging连用(也许/或许…)', r'(也许是|或许是)[^。\n]{0,30}(也许|或许)', 2),
    ('四字格律情绪词', r'心潮澎湃|热血沸腾|百感交集|心乱如麻|思绪万千', 2),
]
LEAK_CHECKS = [
    ('Markdown标题泄漏', r'^\s*#{1,6}\s'),
    ('加粗泄漏', r'\*\*[^*\n]+\*\*'),
    ('反引号泄漏', r'`[^`\n]+`'),
    ('引用/工具痕迹', r'oaicite|turn\d+search|\[\^?\d+\^?\]'),
]


def cjk_len(text):
    return len(re.findall(r'[一-鿿㐀-䶿]', text))


def rates(text):
    n = max(cjk_len(text), 1)
    out = {}
    for name, pat, cap in RATE_CHECKS:
        hits = len(re.findall(pat, text))
        out[name] = (hits, hits * 1000.0 / n, cap)
    return out


def quote_style(text):
    curly = len(re.findall(r'[“”]', text))
    straight = len(re.findall(r'"', text))
    return curly, straight


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__.strip())
        sys.exit(0)
    path = Path(args[0])
    ref_path = None
    if '--ref' in args:
        ref_path = Path(args[args.index('--ref') + 1])
    if not path.exists():
        print(f'ERROR file not found: {path}')
        sys.exit(1)

    text = path.read_text(encoding='utf-8')
    n = cjk_len(text)
    print(f'INFO {path.name}: {n} CJK chars')
    failed = False

    ref_rates = None
    if ref_path:
        if not ref_path.exists():
            print(f'ERROR ref not found: {ref_path}')
            sys.exit(1)
        ref_text = ref_path.read_text(encoding='utf-8')
        ref_rates = rates(ref_text)

    for name, (hits, rate, cap) in rates(text).items():
        if ref_rates:
            ref_rate = ref_rates[name][1]
            lo, hi = ref_rate * 0.5, max(ref_rate * 1.5, 0.5)
            ok = lo <= rate <= hi or hits == 0
            tag = 'OK' if ok else 'FAIL'
            failed |= not ok
            print(f'{tag} {name}: {rate:.1f}/千字 (原作 {ref_rate:.1f}, 允许 {lo:.1f}–{hi:.1f})')
        else:
            ok = rate <= cap
            tag = 'OK' if ok else 'FAIL'
            failed |= not ok
            print(f'{tag} {name}: {hits} 处, {rate:.1f}/千字 (上限 {cap}/千字)')

    for name, pat, cap in WORK_CAPS:
        hits = len(re.findall(pat, text))
        ok = hits <= cap
        failed |= not ok
        print(f'{"OK" if ok else "FAIL"} {name}: {hits} 组 (全文上限 {cap})')

    for name, pat in LEAK_CHECKS:
        hits = len(re.findall(pat, text, flags=re.M))
        ok = hits == 0
        failed |= not ok
        print(f'{"OK" if ok else "FAIL"} {name}: {hits} 处 (上限 0)')

    if ref_rates:
        c1, s1 = quote_style(text)
        c2, s2 = quote_style(ref_path.read_text(encoding='utf-8'))
        ref_curly = c2 >= s2
        out_curly = c1 >= s1
        ok = ref_curly == out_curly or (c1 + s1) == 0
        failed |= not ok
        print(f'{"OK" if ok else "FAIL"} 引号风格: 成稿{"弯" if out_curly else "直"}引号为主, '
              f'原作{"弯" if ref_curly else "直"}引号为主')

    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
