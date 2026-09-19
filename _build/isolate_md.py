#!/usr/bin/env python3
"""
Wrap every Latin/digit run in prose with Unicode bidi isolates (LRI ... PDI)
so mixed Hebrew/English Markdown renders correctly on GitHub.

Same regex as html2md.py.  Skips:
  - fenced code blocks (``` ... ```)          -> left raw
  - HTML tags  (<div ...>, </details> ...)    -> left raw
  - markdown link/image targets  ](...)       -> left raw
  - runs that are already isolated
Applies to inline `code` too (matches the existing chapters' convention).

Usage:  python3 _build/isolate_md.py path/to/file.md [more.md ...]
        (edits in place; idempotent)
"""
import re, sys, io

LRI, PDI = '⁦', '⁩'
_LATIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9 .,:;/()+\-_'\"%&#@|\[\]<>*=]*[A-Za-z0-9)\]'\"/>.])?")
_TAG   = re.compile(r'<[^>\n]+>')
_LINK  = re.compile(r'\]\([^)\n]*\)')

def iso_segment(s):
    return _LATIN.sub(lambda m: LRI + m.group() + PDI, s)

def iso_line(line):
    # protect html tags and link targets, isolate the rest
    out, pos = [], 0
    for m in sorted(list(_TAG.finditer(line)) + list(_LINK.finditer(line)), key=lambda m: m.start()):
        if m.start() < pos: continue
        out.append(iso_segment(line[pos:m.start()])); out.append(m.group()); pos = m.end()
    out.append(iso_segment(line[pos:]))
    return ''.join(out)

def process(text):
    # strip any existing isolates first so the pass is idempotent
    text = text.replace(LRI, '').replace(PDI, '')
    lines, out, in_fence = text.split('\n'), [], False
    for ln in lines:
        if ln.strip().startswith('```'):
            in_fence = not in_fence; out.append(ln); continue
        out.append(ln if in_fence else iso_line(ln))
    return '\n'.join(out)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = io.open(p, encoding='utf-8').read()
        io.open(p, 'w', encoding='utf-8').write(process(s))
        print('isolated:', p)
