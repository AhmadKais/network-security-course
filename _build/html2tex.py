#!/usr/bin/env python3
# Convert guide/src/*.html (my own regular markup) to standalone LaTeX (lualatex/polyglossia, RTL Hebrew).
import re, sys, html
from html.parser import HTMLParser

# ---------- DOM ----------
class Node:
    def __init__(self, tag, attrs=None):
        self.tag=tag; self.attrs=dict(attrs or {}); self.kids=[]
    def cls(self): return self.attrs.get('class','').split()
class Text:
    def __init__(self, s): self.s=s
VOID={'br','img','hr'}
class DOM(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root=Node('root'); self.stack=[self.root]
    def handle_starttag(self,t,a):
        n=Node(t,a); self.stack[-1].kids.append(n)
        if t not in VOID: self.stack.append(n)
    def handle_startendtag(self,t,a):
        self.stack[-1].kids.append(Node(t,a))
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t: del self.stack[i:]; break
    def handle_data(self,d): self.stack[-1].kids.append(Text(d))

# ---------- escaping + LTR wrapping ----------
ESC={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
def esc(s): return re.sub(r'[\\&%$#_{}~^]', lambda m: ESC[m.group()], s)
LATIN=re.compile(r"[(\[]?[A-Za-z0-9](?:[A-Za-z0-9 .,:;/()+\-_='\"%&#@|\[\]<>*]*[A-Za-z0-9)\]'\"%>.])?")
def txt(raw):
    # collapse internal newlines/tabs to spaces for flowing text
    raw=re.sub(r'\s+',' ',raw)
    out=[]; i=0
    for m in LATIN.finditer(raw):
        if m.start()>i: out.append(esc(raw[i:m.start()]))
        out.append(r'\enLR{'+esc(m.group())+'}'); i=m.end()
    if i<len(raw): out.append(esc(raw[i:]))
    return ''.join(out)

# ---------- inline ----------
def inline(node):
    if isinstance(node,Text): return txt(node.s)
    if isinstance(node,Node):
        inner=''.join(inline(k) for k in node.kids)
        raw=''.join(rawtext(k) for k in node.kids)
        t=node.tag
        if t in ('b','strong'): return r'\textbf{'+inner+'}'
        if t in ('i','em'): return r'\emph{'+inner+'}'
        if t=='u': return r'\underline{'+inner+'}'
        if t=='sup': return r'\textsuperscript{'+inner+'}'
        if t=='sub': return r'\textsubscript{'+inner+'}'
        if t=='br': return r'\newline '
        if t=='code': return r'\code{'+esc(raw)+'}'
        if t=='span':
            if 'en' in node.cls(): return r'\enLR{'+esc(raw)+'}'
            return inner
        return inner
    return ''
def rawtext(node):
    if isinstance(node,Text): return re.sub(r'\s+',' ',node.s)
    if isinstance(node,Node): return ''.join(rawtext(k) for k in node.kids)
    return ''
def inline_kids(node): return ''.join(inline(k) for k in node.kids)

# ---------- code block ----------
def codeblock(pre):
    if 'mermaid' in pre.cls():
        return r'\begin{center}\textit{'+esc('[תרשים – ראו את גרסת ה-Markdown]')+r'}\end{center}'
    segs=[]  # (style, text) style in normal/bold/comment
    def walk(n, style):
        if isinstance(n,Text): segs.append((style,n.s)); return
        st=style
        if n.tag=='b': st='bold'
        elif n.tag=='span' and 'c' in n.cls(): st='comment'
        for k in n.kids: walk(k,st)
    for k in pre.kids: walk(k,'normal')
    # build full styled string then split into lines
    text=''.join(s for _,s in segs)
    # rebuild line by line preserving styles
    lines=[[]]  # list of lines; each line list of (style,piece)
    for style,s in segs:
        parts=s.split('\n')
        for j,p in enumerate(parts):
            if j>0: lines.append([])
            if p: lines[-1].append((style,p))
    out=[r'\begin{codebox}\begin{english}\codefont\footnotesize\color{cfg}\setlength{\parindent}{0pt}']
    body=[]
    for ln in lines:
        piece=''
        # leading spaces of first segment
        rendered=''
        first=True
        for style,p in ln:
            if first:
                m=re.match(r'^( +)',p)
                if m: rendered+= '~'*len(m.group(1)); p=p[len(m.group(1)):]
                first=False
            e=esc(p)
            if style=='bold': rendered+=r'\textcolor{cbold}{\textbf{'+e+'}}'
            elif style=='comment': rendered+=r'\textcolor{ccom}{\texthebrew{'+txt(p)+'}}'
            else: rendered+=e
        body.append(rendered if rendered else '~')
    out.append(('\\\\\n').join(body))
    out.append(r'\end{english}\end{codebox}')
    return '\n'.join(out)

# ---------- table ----------
def table(tbl):
    rows=[r for r in tbl.kids if isinstance(r,Node) and r.tag=='tr']
    if not rows: return ''
    ncol=max(sum(1 for c in r.kids if isinstance(c,Node) and c.tag in('td','th')) for r in rows)
    # RTL: each cell forced to right-to-left paragraph direction (\setRTL) so the
    # Hebrew flows correctly, right-aligned; English islands (already \enLR-wrapped)
    # stay left-to-right. Column order is reversed so the first logical column
    # appears on the RIGHT (correct reading order for Hebrew).
    colspec='|'+'|'.join([r'>{\setRTL\raggedleft\arraybackslash}X']*ncol)+'|'
    out=[r'\begin{xltabular}{\linewidth}{'+colspec+'}',r'\hline']
    for ri,r in enumerate(rows):
        cells=[c for c in r.kids if isinstance(c,Node) and c.tag in('td','th')]
        ishdr=any(c.tag=='th' for c in cells)
        rendered=[]
        for c in cells:
            inner=inline_kids(c).strip()
            if c.tag=='th' or ('kv' in tbl.cls() and c is cells[0]):
                inner=r'\textbf{'+inner+'}'
            rendered.append(inner)
        while len(rendered)<ncol: rendered.append('')
        rendered=rendered[::-1]   # reverse for RTL column order
        line=' & '.join(rendered)+r' \\'
        if ishdr: out.append(r'\rowcolor{hdrbg}'+line)
        else: out.append(line)
        out.append(r'\hline')
        if ri==0 and ishdr: out.append(r'\endhead')   # repeat header on page breaks
    out.append(r'\end{xltabular}')
    return '\n'.join(out)

# ---------- list ----------
def lst(node,env):
    out=[r'\begin{'+env+'}']
    for k in node.kids:
        if isinstance(k,Node) and k.tag=='li':
            out.append(r'\item '+inline_kids(k).strip())
    out.append(r'\end{'+env+'}')
    return '\n'.join(out)

BOXENV={'faq':'faqbox','mistake':'mistakebox','tip':'tipbox','exam':'exambox','def':'defbox','story':'storybox','ex':'exbox','lab':'tipbox'}
def box(div):
    classes=div.cls()
    env=None
    for c in classes:
        if c in BOXENV: env=BOXENV[c]
    if env is None: env='defbox'
    # title span .t, answer span .ans
    parts=[]
    for k in div.kids:
        if isinstance(k,Node) and k.tag=='span' and 't' in k.cls():
            parts.append(('title',inline_kids(k).strip()))
        elif isinstance(k,Node) and 'ans' in (k.cls() if isinstance(k,Node) else []):
            parts.append(('ans',inline_kids(k).strip()))
        else:
            parts.append(('body',inline(k)))
    out=[r'\begin{'+env+'}']
    body=''
    for typ,val in parts:
        if typ=='title': out.append(r'\boxtitle{'+val+'}')
        elif typ=='ans': out.append(r'\\[2pt]\hrule\vskip2pt '+val)
        else: body+=val
    # place body after title
    # reconstruct order: title already added; now add body then ans handled inline above
    # simpler: rebuild
    out=[r'\begin{'+env+'}']
    title=[v for t,v in parts if t=='title']
    if title: out.append(r'\boxtitle{'+title[0]+'}'+r'\par ')
    for t,v in parts:
        if t=='body': out.append(v)
        elif t=='ans': out.append(r'\par\vskip2pt\hrule\vskip3pt\textbf{}'+v)
    out.append(r'\end{'+env+'}')
    return ''.join(out)

def meta(div):
    items=[inline_kids(s).strip() for s in div.kids if isinstance(s,Node) and s.tag=='span']
    return r'\begin{metabox}'+r'\\ '.join(items)+r'\end{metabox}'

def flow(div):
    items=[]
    for k in div.kids:
        if isinstance(k,Node):
            if 'n' in k.cls(): items.append(r'\fbox{'+inline_kids(k).strip()+'}')
            elif 'a' in k.cls(): items.append(r'\;'+inline_kids(k).strip()+r'\;')
    return r'\begin{center}'+' '.join(items)+r'\end{center}'

def cover(div):
    out=[r'\begin{titlepage}\centering\vspace*{3cm}']
    for k in div.kids:
        if isinstance(k,Node):
            if k.tag=='h1': out.append(r'{\Huge\bfseries\color{h1}'+inline_kids(k).strip()+r'\par}\vskip8pt')
            elif 'sub' in k.cls(): out.append(r'{\Large '+inline_kids(k).strip()+r'\par}\vskip6pt')
            elif 'note' in k.cls(): out.append(r'\vskip3cm{\large\color{gray}'+inline_kids(k).strip()+r'\par}')
    out.append(r'\end{titlepage}')
    return '\n'.join(out)

# ---------- block dispatch ----------
def block(node):
    if isinstance(node,Text):
        if node.s.strip(): return txt(node.s)
        return ''
    t=node.tag; c=node.cls()
    if t=='h1':
        # separate <small> subtitle
        small=''
        main=''
        for k in node.kids:
            if isinstance(k,Node) and k.tag=='small': small=inline_kids(k).strip()
            else: main+=inline(k)
        s=r'\chapterheading{'+main.strip()+'}'
        if small: s+=r'{\small\color{subgray}'+small+r'\par}\vskip4pt'
        return s
    if t=='h2': return r'\sectionheading{'+inline_kids(node).strip()+'}'
    if t=='h3': return r'\subheading{'+inline_kids(node).strip()+'}'
    if t=='h4': return r'\paragraph{'+inline_kids(node).strip()+'}~\\'
    if t=='p': return txt_p(node)
    if t=='ul': return lst(node,'itemize')
    if t=='ol': return lst(node,'enumerate')
    if t=='table': return table(node)
    if t=='pre': return codeblock(node)
    if t=='div':
        if 'cover' in c: return cover(node)
        if 'meta' in c: return meta(node)
        if 'box' in c: return box(node)
        if 'flow' in c: return flow(node)
        if 'cols' in c:
            return '\n'.join(block(k) for k in node.kids if isinstance(k,Node))
        # generic div: process children
        return '\n\n'.join(b for k in node.kids if (b:=block(k)))
    return ''
def txt_p(node):
    return inline_kids(node).strip()+r'\par'

def convert_body(root):
    parts=[]
    for k in root.kids:
        b=block(k)
        if b: parts.append(b)
    return '\n\n'.join(parts)

PREAMBLE=r'''\documentclass[11pt]{article}
\usepackage{fontspec}
\directlua{luaotfload.add_fallback("hebfb",{"DejaVu Sans:mode=harf"})}
\usepackage{polyglossia}
\setdefaultlanguage{hebrew}
\setotherlanguage{english}
\setmainfont{Noto Sans Hebrew}[Script=Hebrew,RawFeature={fallback=hebfb}]
\newfontfamily\codefont{DejaVu Sans Mono}[RawFeature={fallback=hebfb}]
\usepackage[a4paper,margin=18mm]{geometry}
\usepackage[table]{xcolor}
\usepackage{mdframed}
\usepackage{tabularx}
\usepackage{xltabular}
\usepackage{array}
\usepackage{enumitem}
\usepackage{fancyhdr}
\setlist{leftmargin=1.6em,itemsep=1pt,topsep=2pt}
% colors
\definecolor{h1}{HTML}{1E3A8A}\definecolor{h2}{HTML}{1E40AF}\definecolor{h3}{HTML}{0F172A}
\definecolor{subgray}{HTML}{64748B}\definecolor{hdrbg}{HTML}{E0E7FF}
\definecolor{cfg}{HTML}{E2E8F0}\definecolor{cbg}{HTML}{0F172A}\definecolor{cbold}{HTML}{7DD3FC}\definecolor{ccom}{HTML}{94A3B8}
\definecolor{metabg}{HTML}{F1F5F9}
\newcommand{\enLR}[1]{\textenglish{#1}}
\newcommand{\code}[1]{\textenglish{\codefont #1}}
\newcommand{\chapterheading}[1]{\vspace{2pt}{\LARGE\bfseries\color{h1}#1\par}\vskip2pt{\color{h1}\hrule height 2pt}\vskip6pt}
\newcommand{\sectionheading}[1]{\vskip10pt\penalty-200{\large\bfseries\color{h2}#1\par}\vskip3pt}
\newcommand{\subheading}[1]{\vskip6pt{\bfseries\color{h3}#1\par}\vskip2pt}
\newcommand{\boxtitle}[1]{{\bfseries\color{boxti}#1}}
% box environments (right border, tinted bg)
\newmdenv[topline=false,bottomline=false,leftline=false,rightline=true,linewidth=2pt,innermargin=0pt,skipabove=6pt,skipbelow=6pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt]{genericbox}
\definecolor{faqbg}{HTML}{ECFDF5}\definecolor{faqfr}{HTML}{10B981}\definecolor{faqti}{HTML}{065F46}
\definecolor{misbg}{HTML}{FEF2F2}\definecolor{misfr}{HTML}{EF4444}\definecolor{misti}{HTML}{991B1B}
\definecolor{tipbg}{HTML}{FFFBEB}\definecolor{tipfr}{HTML}{F59E0B}\definecolor{tipti}{HTML}{92400E}
\definecolor{exabg}{HTML}{EFF6FF}\definecolor{exafr}{HTML}{3B82F6}\definecolor{exati}{HTML}{1E3A8A}
\definecolor{defbg}{HTML}{F5F3FF}\definecolor{deffr}{HTML}{8B5CF6}\definecolor{defti}{HTML}{5B21B6}
\definecolor{stobg}{HTML}{FDF4FF}\definecolor{stofr}{HTML}{D946EF}\definecolor{stoti}{HTML}{86198F}
\definecolor{exbg}{HTML}{F0FDFA}\definecolor{exfr}{HTML}{14B8A6}\definecolor{exti}{HTML}{115E59}
\newenvironment{faqbox}{\colorlet{boxti}{faqti}\begin{mdframed}[backgroundcolor=faqbg,linecolor=faqfr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{mistakebox}{\colorlet{boxti}{misti}\begin{mdframed}[backgroundcolor=misbg,linecolor=misfr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{tipbox}{\colorlet{boxti}{tipti}\begin{mdframed}[backgroundcolor=tipbg,linecolor=tipfr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{exambox}{\colorlet{boxti}{exati}\begin{mdframed}[backgroundcolor=exabg,linecolor=exafr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{defbox}{\colorlet{boxti}{defti}\begin{mdframed}[backgroundcolor=defbg,linecolor=deffr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{storybox}{\colorlet{boxti}{stoti}\begin{mdframed}[backgroundcolor=stobg,linecolor=stofr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{exbox}{\colorlet{boxti}{exti}\begin{mdframed}[backgroundcolor=exbg,linecolor=exfr,rightline=true,leftline=false,topline=false,bottomline=false,linewidth=2pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=6pt]}{\end{mdframed}}
\newenvironment{metabox}{\begin{mdframed}[backgroundcolor=metabg,linewidth=0pt,innertopmargin=5pt,innerbottommargin=5pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=4pt,skipbelow=8pt]}{\end{mdframed}}
\newmdenv[backgroundcolor=cbg,linewidth=0pt,innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,skipabove=6pt,skipbelow=8pt]{codebox}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\renewcommand{\thepage}{\enLR{\arabic{page}}}
\pagestyle{fancy}\fancyhf{}\fancyfoot[C]{\thepage}\renewcommand{\headrulewidth}{0pt}
\begin{document}
\sloppy
'''

def main():
    src=sys.argv[1]; out=sys.argv[2]
    h=open(src,encoding='utf-8').read()
    d=DOM(); d.feed(h)
    body=convert_body(d.root)
    tex=PREAMBLE+body+'\n\\end{document}\n'
    open(out,'w',encoding='utf-8').write(tex)
    print('wrote',out)

if __name__=='__main__': main()
