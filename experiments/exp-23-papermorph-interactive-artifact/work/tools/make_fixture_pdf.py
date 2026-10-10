#!/usr/bin/env python3
"""Render the canonical MPE governance markdown into a fixture PDF (no bookmarks).

Dev-only helper for EXP-23 CP-01. Produces a clean, text-layer PDF from
docs/governance/SCOPE-CHANGE-CONTROL.md so the stock Papermorph split stage
(outline.py / split_pages.py) has a real PDF to parse. Deliberately NO bookmarks:
exercises the documented "PDF without bookmarks" path.
"""
import re
import sys
from pathlib import Path

import pymupdf

SRC = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
FONT = "helv"

PAGE_W, PAGE_H, MARG = 612, 792, 54
LINE = 15.5
WRAP = 78


def wrap(text, width=WRAP):
    out, cur = [], ""
    for word in text.split(" "):
        if len(cur) + len(word) + (1 if cur else 0) > width and cur:
            out.append(cur)
            cur = word
        else:
            cur = cur + " " + word if cur else word
    if cur:
        out.append(cur)
    return out


def main():
    doc = pymupdf.open()
    page = None
    y = None

    def new_page(first=False):
        nonlocal page, y
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        y = MARG if not first else MARG - 6

    def put(line, size, bold=False, gap=0.0, color=(0.1, 0.1, 0.12)):
        nonlocal y
        fontname = "hebo" if bold else "helv"
        chunks = line if isinstance(line, list) else ([line] if line else [""])
        for chunk in chunks:
            if y > PAGE_H - MARG:
                new_page()
            page.insert_text((MARG, y), chunk, fontsize=size, fontname=fontname, color=color)
            y += LINE + gap * size
        y += size * 0.28

    new_page(first=True)
    for raw in SRC.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip():
            y += 6
            continue
        if line.startswith("## "):
            put(line[3:].replace("**", ""), 15, bold=True, gap=0.9)
            y += 4
        elif line.startswith("# "):
            put(line[2:], 22, bold=True, gap=1.2)
            y += 6
        elif line.strip() == "---":
            y += 8
        elif re.match(r"^\d+\.\s", line.strip()):
            put(line.strip(), 11)
        elif line.strip().startswith("- "):
            put("    " + line.strip()[2:], 11)
        elif line.strip().startswith("`") and line.strip().endswith("`") and len(line.strip()) < 60:
            put(line.strip(), 11)
        elif line.startswith("**") and line.endswith("**") and len(line) < 120:
            put(line.strip("* "), 11, bold=True)
        else:
            for chunk in wrap(line.strip()):
                put(chunk, 11)
    doc.save(OUT, garbage=4, deflate=True)
    print(f"wrote {OUT} ({doc.page_count} pages, no bookmarks)")


if __name__ == "__main__":
    main()
