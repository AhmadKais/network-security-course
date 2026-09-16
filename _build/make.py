#!/usr/bin/env python3
"""Build the course into per-chapter folders.

SOURCE OF TRUTH:
 - Study material  = the LaTeX file  Chapter_XX/study_material.tex  (edit this).
 - Slides          = the HTML in     _build/slides_src/  (edit this).

Commands (run from Course_Materials/):
  python3 _build/make.py latex   compile every study_material.tex -> PDF (does NOT touch the .tex)
  python3 _build/make.py slides  rebuild every presentation.html from _build/slides_src
  python3 _build/make.py book    assemble Full_Course.pdf from the chapter .tex files
  python3 _build/make.py all     slides + latex + book
  python3 _build/make.py convert [--force]
                                 (re)generate .tex from the ORIGINAL html drafts in
                                 _build/_source_html_originals/. Skips any .tex that already
                                 exists unless --force is given. This is a bootstrap/reset tool
                                 and will OVERWRITE your LaTeX edits with --force. Normal use
                                 never needs it.
"""
import os, re, sys, subprocess

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, '_build')
GH    = os.path.join(BUILD, '_source_html_originals')   # original HTML drafts (NOT source of truth)
SS    = os.path.join(BUILD, 'slides_src')                # slide sources (source of truth for slides)
sys.path.insert(0, BUILD)

# folder, html-stem (original draft), slide-stem (None if no slides), short title
CH = [
 ("Chapter_00_Overview","00-overview",None,"סקירה ותכנון שנתי"),
 ("Chapter_00b_Networking_Reminder","00b-networking","00b-networking","תזכורת רשתות תקשורת"),
 ("Chapter_01_Network_Threats","01-threats","01-threats","מבוא לאיומי רשת"),
 ("Chapter_02_Device_Security","02-devices","02-devices","אבטחת אביזרי רשת"),
 ("Chapter_03_AAA","03-aaa","03-aaa","מודל ה-AAA"),
 ("Chapter_04_Firewalls","04-firewalls","04-firewalls","חומות אש ו-ACL"),
 ("Chapter_05_IDS_IPS","05-ids-ips","05-ids-ips","IDS / IPS"),
 ("Chapter_06_LAN_Security","06-lan","06-lan","אבטחת הרשת המקומית"),
 ("Chapter_07_Cryptography","07-crypto","07-crypto","הצפנה וקריפטולוגיה"),
 ("Chapter_08_VPN","08-vpn","08-vpn","מערכות VPN"),
 ("Chapter_09_Security_Management","09-management","09-management","ניהול אבטחה מתקדם"),
]

def read(p):
    with open(p, encoding='utf-8') as f: return f.read()
def write(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)

def _lualatex(name, cwd, passes=2):
    for _ in range(passes):
        subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error',name],
                       cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base=os.path.splitext(name)[0]
    for ext in ('aux','log','out','toc'):
        f=os.path.join(cwd, base+'.'+ext)
        if os.path.exists(f): os.remove(f)

# ---------- compile only (the everyday command) ----------
def build_latex():
    for folder,_,_,_ in CH:
        d=os.path.join(ROOT, folder)
        tex=os.path.join(d, 'study_material.tex')
        if not os.path.exists(tex):
            print(f"latex {folder}: SKIP (no study_material.tex — run 'convert' to bootstrap it)")
            continue
        _lualatex('study_material.tex', d)
        ok=os.path.exists(os.path.join(d,'study_material.pdf'))
        print(f"latex {folder}: {'OK' if ok else 'FAILED'}")

# ---------- bootstrap conversion from the original HTML drafts (guarded) ----------
def convert_latex(force=False):
    from html2tex import DOM, convert_body, PREAMBLE
    for folder,stem,_,_ in CH:
        d=os.path.join(ROOT, folder); os.makedirs(d, exist_ok=True)
        tex=os.path.join(d, 'study_material.tex')
        if os.path.exists(tex) and not force:
            print(f"convert {folder}: SKIP (.tex exists; use --force to overwrite)")
            continue
        src=os.path.join(GH, stem+'.html')
        if not os.path.exists(src):
            print(f"convert {folder}: SKIP (no original html at {src})"); continue
        dom=DOM(); dom.feed(read(src))
        write(tex, PREAMBLE+convert_body(dom.root)+'\n\\end{document}\n')
        print(f"convert {folder}: WROTE study_material.tex{' (forced overwrite)' if force else ''}")

# ---------- slides ----------
def build_slides():
    css=read(os.path.join(SS,'slides.css')); js=read(os.path.join(SS,'slides.js'))
    def title_of(html,default):
        m=re.search(r"<h1[^>]*>(.*?)</h1>",html,re.S)
        if not m: return default
        t=re.sub(r"<br\s*/?>"," ",m.group(1))
        return re.sub(r"\s+"," ",re.sub("<[^>]+>","",t)).strip()
    for folder,_,slide,_ in CH:
        if not slide: continue
        body=read(os.path.join(SS,slide+'.html')); t=title_of(body,slide)
        page=f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title>
<style>{css}</style></head><body>
<div id="deck">{body}</div>
<div id="hud"><button id="prev" title="הקודם">‹</button><span id="counter"></span><button id="next" title="הבא">›</button>
<button id="notesBtn" title="הערות למורה (N)">✎</button><button id="fsBtn" title="מסך מלא (F)">⛶</button></div>
<div id="progress"></div><div id="notes"></div>
<script>{js}</script></body></html>'''
        d=os.path.join(ROOT,folder); os.makedirs(d,exist_ok=True)
        write(os.path.join(d,'presentation.html'),page)
        print(f"slides {folder}: OK")

# ---------- book: assembled FROM THE CHAPTER .tex FILES ----------
def _extract_body(tex):
    i=tex.find(r'\begin{document}')
    j=tex.rfind(r'\end{document}')
    if i<0 or j<0: return tex
    return tex[i+len(r'\begin{document}'):j]

def _extract_chapterheading(body):
    key=r'\chapterheading{'
    k=body.find(key)
    if k<0: return None
    i=k+len(key); depth=1; out=[]
    while i<len(body) and depth>0:
        c=body[i]
        if c=='{': depth+=1
        elif c=='}': depth-=1
        if depth>0: out.append(c)
        i+=1
    return ''.join(out)

def build_book():
    from html2tex import PREAMBLE
    titlepage=r"""\begin{titlepage}\centering\vspace*{4cm}
{\Huge\bfseries\color{h1} אבטחת מידע\par}\vskip10pt
{\Huge\bfseries\color{h1} ספר הקורס המלא\par}\vskip20pt
{\Large תכנית הלימודים – מגמת תקשוב, משרד החינוך\par}\vskip6pt
{\large\color{subgray} 9 פרקים \enLR{$\cdot$} חומר עיון, סיפורים, תרגילים ושאלות בסגנון בגרות (שאלון \enLR{735001})\par}
\vfill{\large\color{subgray} מדריך למורה\par}\end{titlepage}
\tableofcontents\clearpage
"""
    bodies=[]
    for folder,_,_,short in CH:
        tex=os.path.join(ROOT, folder, 'study_material.tex')
        if not os.path.exists(tex):
            print(f"book: SKIP {folder} (no .tex)"); continue
        body=_extract_body(read(tex))
        body=re.sub(r"\\begin\{titlepage\}.*?\\end\{titlepage\}","",body,flags=re.S)  # drop cover
        title=_extract_chapterheading(body) or short
        bodies.append(r"\clearpage"+"\n"+r"\phantomsection\addcontentsline{toc}{section}{"+title+"}\n"+body)
    pre=PREAMBLE.replace(r"\begin{document}",
        r"\usepackage[hidelinks,unicode]{hyperref}"+"\n"+r"\usepackage{bookmark}"+"\n"+r"\begin{document}")
    write(os.path.join(ROOT,'Full_Course.tex'), pre+titlepage+"\n\n".join(bodies)+"\n\\end{document}\n")
    _lualatex('Full_Course.tex', ROOT, passes=3)
    print("book:", "OK" if os.path.exists(os.path.join(ROOT,'Full_Course.pdf')) else "FAILED")


def build_md():
    import html2md
    from html2md import DOM as _D  # ensure import path
    from html2md import convert as _conv
    from html2tex import DOM
    for folder,stem,_,_ in CH:
        src=os.path.join(GH, stem+'.html')
        if not os.path.exists(src):
            print(f"md {folder}: SKIP (no html)"); continue
        d=os.path.join(ROOT, folder); os.makedirs(d, exist_ok=True)
        dom=DOM(); dom.feed(read(src))
        write(os.path.join(d,'study_material.md'), _conv(dom.root))
        print(f"md {folder}: OK")

if __name__=='__main__':
    args=sys.argv[1:]
    what=args[0] if args else 'all'
    force='--force' in args
    if what=='convert':      convert_latex(force=force)
    elif what=='slides':     build_slides()
    elif what=='latex':      build_latex()
    elif what=='book':       build_book()
    elif what=='md':         build_md()
    elif what=='all':        build_slides(); build_latex(); build_book(); build_md()
    else: print(__doc__)
