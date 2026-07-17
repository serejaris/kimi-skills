#!/usr/bin/env python3
"""
Markdown → Word conversion main pipeline

Pipeline: load → citation conversion → Pandoc → OOXML post-processing → output docx
"""
import sys
import os
import re
from pathlib import Path
import json
import logging
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parent))

from citation_parser import convert_citations, detect_edge_cases
from docx_postprocess import process_word_document_with_hyperlinks
from docx_footnote import process_word_document_with_noteref
from docx_endnote import process_word_document_with_endnotes

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

STYLES = ('footnote', 'endnote', 'hyperlink')
_CJK_RE = re.compile(r'[\u4e00-\u9fff]')
_LEGACY_BYTE_RUN_RE = re.compile(
    r'[\x80-\xff\u20ac\u201a\u0192\u201e\u2026\u2020\u2021\u02c6\u2030'
    r'\u0160\u2039\u0152\u017d\u2018\u2019\u201c\u201d\u2022\u2013\u2014'
    r'\u02dc\u2122\u0161\u203a\u0153\u017e\u0178]{3,}'
)


def load_markdown(path: Path) -> str:
    """Read strict UTF-8 and reject strong signs of CJK mojibake."""
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Invalid UTF-8 in {path.name}: {exc}. "
            "Ensure the Markdown is saved as UTF-8 and retry."
        ) from exc

    affected_paragraphs = 0
    suspicious_runs = 0
    recovered_cjk = 0
    for paragraph in re.split(r'\n\n+', text):
        paragraph_runs = 0
        paragraph_cjk = 0
        for match in _LEGACY_BYTE_RUN_RE.finditer(paragraph):
            cjk_count = 0
            for legacy_encoding in ('latin-1', 'cp1252'):
                try:
                    recovered = match.group(0).encode(legacy_encoding).decode('utf-8')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    continue
                cjk_count = max(cjk_count, len(_CJK_RE.findall(recovered)))
            if cjk_count:
                paragraph_runs += 1
                paragraph_cjk += cjk_count
        if paragraph_runs:
            affected_paragraphs += 1
            suspicious_runs += paragraph_runs
            recovered_cjk += paragraph_cjk

    # A single reversible sequence (for example the literal text "ä¸­") is
    # ambiguous and remains accepted. Multiple recovered CJK characters are a
    # strong signal while still allowing ordinary Latin-1 prose.
    if recovered_cjk >= 2:
        raise ValueError(
            f"Double-encoded UTF-8 mojibake detected in {path.name} "
            f"({affected_paragraphs} paragraph(s), {suspicious_runs} reversible "
            f"Latin-1/CP1252 run(s), {recovered_cjk} recovered CJK character(s)); "
            "refusing to create a DOCX. "
            "Regenerate or repair the Markdown as UTF-8, then retry."
        )
    return text


def load_citation_db(jsonl_path: str) -> dict:
    """Load citation.jsonl → {int_id: entry_dict}"""
    db = {}
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                cid = entry.get('id')
                if cid is not None:
                    db[cid] = entry
    return db


def convert_md_to_docx(
    md_path: str,
    citation_jsonl_path: str = None,
    output_dir: str = None,
    style: str = "footnote",
) -> str:
    """
    Full Markdown → Word conversion pipeline.

    Args:
        md_path:             Path to Markdown file
        citation_jsonl_path: Path to citation.jsonl (required, specify explicitly)
        output_dir:          Output directory (None uses same directory as MD file)
        style:               footnote / endnote / hyperlink

    Returns:
        Path to generated docx file
    """
    if style not in STYLES:
        raise ValueError(f"style must be one of {STYLES}, got: {style}")

    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    if citation_jsonl_path:
        citation_jsonl_path = Path(citation_jsonl_path)
    else:
        raise ValueError("citation_jsonl_path is required. Specify the path to citation.jsonl.")

    if not citation_jsonl_path.exists():
        raise FileNotFoundError(f"Citation file not found: {citation_jsonl_path}")

    # Output directory
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = md_path.parent

    logger.info(f"Document: {md_path.name} | Citation: {citation_jsonl_path.name} | Style: {style}")

    # ── 1. Load data ──
    citation_db = load_citation_db(str(citation_jsonl_path))
    logger.info(f"Loaded {len(citation_db)} citation records")

    markdown_content = load_markdown(md_path)

    # ── 2. Citation conversion (detect + map + replace in one call) ──
    converted_md, id_to_display_num, detection = convert_citations(markdown_content, citation_db)

    # ── 3. Edge case detection ──
    for w in detect_edge_cases(markdown_content):
        logger.warning(w)

    # ── 4. Save intermediate MD (same dir as source MD to keep image relative paths) ──
    converted_md_path = md_path.parent / f"{md_path.stem}.converted.md"
    converted_md_path.write_text(converted_md, encoding='utf-8')

    # ── 5. Pandoc → base.docx ──
    base_docx_path = output_dir / f"{md_path.stem}.base.docx"
    pandoc_cmd = [
        'pandoc', str(converted_md_path),
        '-o', str(base_docx_path),
        '--from=markdown', '--to=docx',
        f'--resource-path={md_path.parent}',
        '--standalone',
    ]
    result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc conversion failed: {result.stderr}")

    # ── 6. OOXML post-processing ──
    output_path = output_dir / f"{md_path.stem}.{style}.docx"

    # display_num → citation_info mapping (for footnote/endnote/hyperlink content)
    display_db = {v: citation_db[k] for k, v in id_to_display_num.items()}

    processors = {
        'footnote':  process_word_document_with_noteref,
        'endnote':   process_word_document_with_endnotes,
        'hyperlink': process_word_document_with_hyperlinks,
    }
    success = processors[style](str(base_docx_path), str(output_path), citation_db=display_db)

    if success:
        logger.info(f"Done: {output_path.name}")
        return str(output_path)
    else:
        raise RuntimeError(f"{style} generation failed")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Markdown → Word conversion (with citation cross-references)')
    parser.add_argument('md_file', help='Path to Markdown file')
    parser.add_argument('--citation', required=True, help='Path to citation.jsonl')
    parser.add_argument('--output-dir', help='Output directory (default: same as MD file)')
    parser.add_argument('--style', choices=STYLES, default='footnote',
                        help='Citation style: footnote / endnote / hyperlink')

    args = parser.parse_args()

    try:
        out = convert_md_to_docx(
            args.md_file,
            citation_jsonl_path=args.citation,
            output_dir=args.output_dir,
            style=args.style,
        )
        print(f"\n{'='*60}\nConversion complete: {out}\n{'='*60}")

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
