#!/usr/bin/env python3
"""
Word count checker for creative-writing skills.
Minimal, zero-dependency (stdlib only), sandbox-safe.

Usage:
  python check_wordcount.py <file> [--min N] [--max N] [--target N --tol PCT]
                            [--lang zh|en|auto] [--per-chapter]

Chinese counts are pure CJK characters (punctuation excluded) — the default
口径; report it to the user alongside the number.

Modes (combine freely):
  --min N             count must be >= N
  --max N             count must be <= N      (e.g. "5万字以内" → --max 50000)
  --target N --tol P  count within N ± P%     (e.g. "2000字左右" → --target 2000 --tol 10)
  --per-chapter       also split on 第N章/Chapter N headings and report each
                      chapter's count (constraints are applied per chapter)

Output (machine-readable):
  PASS 3200 zh chars
  FAIL 2800 zh chars (min: 3000)
  ch01 第一章 三天: PASS 3612
Exit code: 0 = all PASS, 1 = any FAIL/error.
"""

import re
import sys
from pathlib import Path

CHAPTER_RE = re.compile(
    r'^\s*(第[0-9一二三四五六七八九十百千零两]+[章回卷集]|Chapter\s+\d+)[^\n]*',
    re.M)


def strip_markdown(text: str) -> str:
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text, flags=re.S)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'^\s*[-*+>]\s', '', text, flags=re.M)
    text = re.sub(r'^\s*\d+\.\s', '', text, flags=re.M)
    text = re.sub(r'\|[^\n]*\|', '', text)
    text = re.sub(r'-{3,}', '', text)
    return text


def count_zh(text: str) -> int:
    return len(re.findall(r'[一-鿿㐀-䶿]', text))


def count_en(text: str) -> int:
    return sum(1 for t in text.split() if re.search(r'[a-zA-Z]', t))


def detect_lang(text: str) -> str:
    return 'zh' if count_zh(text) > count_en(text) else 'en'


def judge(count, mn, mx):
    if mn is not None and count < mn:
        return f'FAIL (min: {mn})'
    if mx is not None and count > mx:
        return f'FAIL (max: {mx})'
    return 'PASS'


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__.strip())
        sys.exit(0)

    file_path, mn, mx, target, tol, lang, per_ch = args[0], None, None, None, 10.0, 'auto', False
    i = 1
    while i < len(args):
        a = args[i]
        if a == '--min':
            mn = int(args[i + 1]); i += 2
        elif a == '--max':
            mx = int(args[i + 1]); i += 2
        elif a == '--target':
            target = int(args[i + 1]); i += 2
        elif a == '--tol':
            tol = float(args[i + 1].rstrip('%')); i += 2
        elif a == '--lang':
            lang = args[i + 1]; i += 2
        elif a == '--per-chapter':
            per_ch = True; i += 1
        else:
            i += 1

    if target is not None:
        mn = int(target * (1 - tol / 100))
        mx = int(target * (1 + tol / 100))

    path = Path(file_path)
    if not path.exists():
        print(f'ERROR file not found: {file_path}')
        sys.exit(1)

    raw = path.read_text(encoding='utf-8')
    text = strip_markdown(raw)
    if lang == 'auto':
        lang = detect_lang(text)
    counter = count_zh if lang == 'zh' else count_en
    unit = 'chars' if lang == 'zh' else 'words'

    failed = False
    total = counter(text)
    verdict = judge(total, mn if not per_ch else None, mx if not per_ch else None)
    failed |= verdict.startswith('FAIL')
    print(f'{verdict} {total} {lang} {unit} (口径: {"纯汉字" if lang == "zh" else "english words"})')

    if per_ch:
        marks = list(CHAPTER_RE.finditer(text))
        if not marks:
            print('WARN no chapter headings found for --per-chapter')
        for j, m in enumerate(marks):
            seg = text[m.end(): marks[j + 1].start() if j + 1 < len(marks) else len(text)]
            c = counter(seg)
            v = judge(c, mn, mx)
            failed |= v.startswith('FAIL')
            print(f'{m.group(1)}: {v} {c}')

    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
