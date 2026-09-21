#!/usr/bin/env python3
"""Reflow Markdown prose so a line never breaks inside a sentence.

A paragraph or list item that fits in the width plus 15 characters stays on one line.
A longer one is packed sentence by sentence onto lines of at most the width.
A sentence longer than the width stays whole.
Width 0 puts each sentence on its own line.

Headings, tables, code blocks, blockquotes, HTML blocks, reference definitions, badges, rules and YAML frontmatter are left as they are.
So is a paragraph or list item that contains a hard line break, and whitespace inside a line is never changed.
A file is skipped when the result would change more than whitespace.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MARKER = re.compile(r"^(\s*)([-*+] |\d+[.)] )")
RULE = re.compile(r"^ {0,3}([-=*_])( *\1){2,} *$")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:")
BLOCK_START = ("#", ">", "<", "|", "[![", "```", "~~~")
BOUNDARY = re.compile(r"(?<!e\.g\.)(?<!i\.e\.)(?<=[.?!]) (?=[A-Z`])(?=(?:[^`]*`[^`]*`)*[^`]*$)")


def sentences(text: str) -> list[str]:
    """Split after ". ", "? " or "! " when the next word starts with a capital or a backtick, outside inline code."""
    return BOUNDARY.split(text)


def pack(sents: list[str], first: str, cont: str, width: int) -> list[str]:
    lines = [first + sents[0]]
    for sent in sents[1:]:
        if len(lines[-1]) + 1 + len(sent) <= width:
            lines[-1] += f" {sent}"
        else:
            lines.append(cont + sent)
    return lines


def continues(line: str, cont: str) -> bool:
    """Report whether a line keeps the current block going instead of starting its own."""
    return bool(
        line.strip()
        and line.startswith(cont)
        and not line[len(cont) :].startswith(("    ", "\t"))
        and not MARKER.match(line)
        and not RULE.match(line)
        and not REFERENCE.match(line)
        and not line.lstrip().startswith(BLOCK_START)
    )


def reflow(text: str, width: int) -> str:
    src = text.split("\n")
    out: list[str] = []
    i = 0
    if src[:1] == ["---"]:
        i = src.index("---", 1) + 1 if "---" in src[1:] else len(src)
        out = src[:i]

    fence = ""
    while i < len(src):
        line = src[i]
        lead = line.lstrip()
        if fence:
            out.append(line)
            i += 1
            if lead.startswith(fence):
                fence = ""
            continue
        if lead.startswith(("```", "~~~")):
            fence = lead[:3]
            out.append(line)
            i += 1
            continue

        if lead.startswith("<"):
            while i < len(src) and src[i].strip():
                out.append(src[i])
                i += 1
            continue

        marker = MARKER.match(line)
        if marker:
            indent, mark = marker.groups()
            first, cont = indent + mark, indent + " " * len(mark)
            block = [line[len(first) :]]
        elif not lead or line.startswith(("    ", "\t")) or lead.startswith(BLOCK_START) or RULE.match(line) or REFERENCE.match(line):
            out.append(line)
            i += 1
            continue
        else:
            first = cont = ""
            block = [line]
        start = i
        i += 1
        while i < len(src) and continues(src[i], cont):
            block.append(src[i])
            i += 1

        if any(part.endswith(("  ", "\\")) for part in block):
            out.extend(src[start:i])
            continue
        prose = " ".join(part.strip() for part in block)
        if len(first + prose) <= width + 15:
            out.append(first + prose)
        else:
            out.extend(pack(sentences(prose), first, cont, width))
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reflow Markdown prose at sentence boundaries, in place.")
    parser.add_argument("--width", type=int, default=135, help="line width to pack sentences to (default: 135)")
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    args = parser.parse_args()

    status = 0
    for path in args.files:
        source = path.read_text(encoding="utf-8")
        result = reflow(source, args.width)
        if result.split() != source.split():
            print(f"skipped {path}: the result would change more than whitespace", file=sys.stderr)
            status = 1
        elif result != source:
            path.write_text(result, encoding="utf-8")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
