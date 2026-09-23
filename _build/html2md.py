#!/usr/bin/env python3
"""Convert _build/_source_html_originals/*.html -> GitHub-flavored Markdown.
Reuses the DOM parser from html2tex."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html2tex import DOM, Node, Text

BOX = {  # class -> (emoji, default label)
 'faq':('❓','שאלת תלמיד'), 'mistake':('⚠️','טעות נפוצה'), 'tip':('💡','טיפ'),
 'exam':('📝','שאלה בסגנון בגרות'), 'def':('📘','רקע / הגדרה'),
 'story':('📖','סיפור מהחיים'), 'ex':('✏️','תרגיל'),
 'lab':('🧪','מעבדה — נסו בעצמכם ב-Kali'),
}

def sp(s): return re.sub(r'\s+',' ',s)

# Wrap each Latin/English run in Unicode bidi isolates (LRI ... PDI) so mixed
# Hebrew/English lines render correctly (English stays a clean LTR unit and its
# punctuation does not leak into the surrounding RTL text). The characters are
# invisible, so the raw Markdown stays readable.
_LRI='\u2066'; _PDI='\u2069'
_LATIN=re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9 .,:;/()+\-_'\"%&#@|\[\]<>*=]*[A-Za-z0-9)\]'\"/>.])?")
def iso(s):
    return _LATIN.sub(lambda m: _LRI+m.group()+_PDI, s)

def inline(n):
    if isinstance(n,Text): return iso(sp(n.s))
    if isinstance(n,Node):
        inner=''.join(inline(k) for k in n.kids)
        raw=sp(''.join(_raw(k) for k in n.kids))
        t=n.tag
        if t in ('b','strong'): return f'**{inner.strip()}**' if inner.strip() else ''
        if t in ('i','em'): return f'*{inner.strip()}*'
        if t=='u': return f'**{inner.strip()}**'
        if t=='sup': return f'^{raw}'
        if t=='sub': return f'~{raw}'
        if t=='br': return '  \n'
        if t=='code': return f'`{raw}`'
        if t=='span': return inner
        return inner
    return ''
def _raw(n):
    if isinstance(n,Text): return iso(sp(n.s))
    if isinstance(n,Node): return ''.join(_raw(k) for k in n.kids)
    return ''
def inl(n): return ''.join(inline(k) for k in n.kids).strip()

def cell(c):
    txt=inl(c).replace('\n',' ').replace('|',r'\|')
    if c.tag=='th': txt=f'**{txt}**'
    return txt

def table(tbl):
    rows=[r for r in tbl.kids if isinstance(r,Node) and r.tag=='tr']
    if not rows: return ''
    def cells(r): return [c for c in r.kids if isinstance(c,Node) and c.tag in ('td','th')]
    ncol=max(len(cells(r)) for r in rows)
    has_th=any(c.tag=='th' for r in rows for c in cells(r))
    out=[]
    body_start=0
    if has_th and any(c.tag=='th' for c in cells(rows[0])):
        hdr=[cell(c) for c in cells(rows[0])]; body_start=1
    else:
        hdr=['']*ncol
    hdr+=['']*(ncol-len(hdr))
    out.append('| '+' | '.join(hdr)+' |')
    out.append('| '+' | '.join(['---']*ncol)+' |')
    for r in rows[body_start:]:
        cs=[cell(c) for c in cells(r)]; cs+=['']*(ncol-len(cs))
        out.append('| '+' | '.join(cs)+' |')
    return '\n'.join(out)

def codeblock(pre):
    # plain text, strip inline styling but keep text (incl. comments)
    txt=''.join(_raw_code(k) for k in pre.kids).strip('\n')
    if 'mermaid' in pre.cls():
        return '```mermaid\n'+txt+'\n```'
    # Force left-to-right: the whole page is wrapped in <div dir="rtl">, and a
    # fenced ``` block inherits that direction on GitHub (right-aligned / flipped).
    # A raw <pre dir="ltr"> is a type-1 HTML block (immune to blank lines) so it
    # stays LTR both at top level AND when prefixed inside a box/blockquote.
    esc=txt.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return '<pre dir="ltr" align="left">\n'+esc+'\n</pre>'
def _raw_code(n):
    if isinstance(n,Text): return n.s
    if isinstance(n,Node): return ''.join(_raw_code(k) for k in n.kids)
    return ''

def lst(node,ordered):
    out=[]; i=1
    for k in node.kids:
        if isinstance(k,Node) and k.tag=='li':
            marker=f'{i}.' if ordered else '-'; i+=1
            out.append(f'{marker} '+inl(k))
    return '\n'.join(out)

def box(div):
    cls=div.cls(); emoji,label='ℹ️',''
    for c in cls:
        if c in BOX: emoji,label=BOX[c]
    title=None; segs=[]; cur=['']
    def flush():
        if cur[0].strip(): segs.append(cur[0].strip())
        cur[0]=''
    def emit(node, prefix=''):
        # inline text (with optional label prefix), then block children as their
        # own segments so <pre>/lists/tables are separated by blank lines
        acc=prefix; blocks=[]
        for kk in node.kids:
            if isinstance(kk,Node) and kk.tag in ('ul','ol','pre','table'):
                blocks.append(block(kk))
            else:
                acc+=inline(kk)
        if acc.strip(): segs.append(acc.strip())
        segs.extend(blocks)
    for k in div.kids:
        if isinstance(k,Node) and k.tag=='span' and 't' in k.cls(): title=inl(k)
        elif isinstance(k,Node) and 'ans' in k.cls(): flush(); emit(k, prefix='**תשובה:** ')
        elif isinstance(k,Node) and k.tag in ('ul','ol','pre','table'): flush(); segs.append(block(k))
        else: cur[0]+=inline(k)
    flush()
    head=f'{emoji} **{title or label}**'
    content='\n\n'.join([head]+[s for s in segs if s])
    # blockquote-prefix every line (blank lines become a bare '>')
    return '\n'.join('> '+l if l else '>' for l in content.split('\n'))

def meta(div):
    items=[inl(s) for s in div.kids if isinstance(s,Node) and s.tag=='span']
    return '> '+'  \n> '.join(items)

def flow(div):
    parts=[]
    for k in div.kids:
        if isinstance(k,Node):
            if 'n' in k.cls(): parts.append('['+inl(k)+']')
            elif 'a' in k.cls(): parts.append(inl(k) or '→')
    return '`'+' '.join(parts)+'`'

def cover(div):
    out=[]
    for k in div.kids:
        if isinstance(k,Node):
            if k.tag=='h1': out.append('# '+inl(k))
            elif 'sub' in k.cls(): out.append('_'+inl(k)+'_')
            elif 'note' in k.cls(): out.append(inl(k))
    return '\n\n'.join(out)

def block(n):
    if isinstance(n,Text):
        return sp(n.s).strip()
    t=n.tag; c=n.cls()
    if t=='h1':
        small=''; main=''
        for k in n.kids:
            if isinstance(k,Node) and k.tag=='small': small=inl(k)
            else: main+=inline(k)
        s='# '+main.strip()
        if small: s+='\n\n_'+small+'_'
        return s
    if t=='h2': return '## '+inl(n)
    if t=='h3': return '### '+inl(n)
    if t=='h4': return '#### '+inl(n)
    if t=='p': return inl(n)
    if t=='ul': return lst(n,False)
    if t=='ol': return lst(n,True)
    if t=='table': return table(n)
    if t=='pre': return codeblock(n)
    if t=='div':
        if 'cover' in c: return cover(n)
        if 'meta' in c: return meta(n)
        if 'box' in c: return box(n)
        if 'flow' in c: return flow(n)
        return '\n\n'.join(b for k in n.kids if isinstance(k,Node) and (b:=block(k)))
    return ''

def convert(root):
    parts=[]
    for k in root.kids:
        b=block(k)
        if b: parts.append(b)
    body='\n\n'.join(parts)
    # Wrap in an RTL container so GitHub renders Hebrew right-to-left
    # (paragraphs, lists and tables all flip correctly).
    return '<div dir="rtl" align="right">\n\n'+body+'\n\n</div>\n'

if __name__=='__main__':
    src,out=sys.argv[1],sys.argv[2]
    d=DOM(); d.feed(open(src,encoding='utf-8').read())
    open(out,'w',encoding='utf-8').write(convert(d.root))
    print('wrote',out)
