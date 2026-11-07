#!/usr/bin/env python3
"""Generate the course illustrations as SVG (assets/img/*.svg).

The SVGs are embedded in the Markdown chapters (GitHub renders them as images)
and exported to PNG by  _build/svg2png.js  for the LaTeX worksheets.

All labels inside the figures are English (same rule as the ASCII drawings);
the Hebrew explanation lives in the caption under each image.

Usage (from Course_Materials/):
    python3 _build/figures.py            # writes assets/img/*.svg
    node _build/svg2png.js               # writes Worksheets/img/*.png
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')
FONT = "Segoe UI, Arial, Helvetica, sans-serif"
MONO = "Consolas, 'DejaVu Sans Mono', monospace"

# palette: (stroke/dark, fill/light)
BLUE = ('#1D4ED8', '#DBEAFE'); GREEN = ('#047857', '#D1FAE5'); RED = ('#B91C1C', '#FEE2E2')
AMBER = ('#B45309', '#FEF3C7'); PURPLE = ('#6D28D9', '#EDE9FE'); SLATE = ('#334155', '#F1F5F9')
TEAL = ('#0F766E', '#CCFBF1'); PINK = ('#BE185D', '#FCE7F3'); INK = '#0F172A'; MUTED = '#64748B'
ARROW_COLORS = {'ink': INK, 'blue': BLUE[0], 'green': GREEN[0], 'red': RED[0], 'amber': AMBER[0],
                'purple': PURPLE[0], 'slate': '#64748B', 'teal': TEAL[0]}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def svg(w, h, body, title=None, subtitle=None):
    defs = ''.join(
        f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for k, c in ARROW_COLORS.items())
    head = ''
    if title:
        head += text(w / 2, 34, title, 20, weight='700', fill=INK)
    if subtitle:
        head += text(w / 2, 56, subtitle, 13, fill=MUTED)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" xml:space="preserve" style="white-space:pre">\n<defs>{defs}</defs>\n'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>\n'
            f'{head}{body}</svg>\n')


def text(x, y, s, fs=14, anchor='middle', weight='400', fill=INK, mono=False, italic=False):
    fam = f' font-family="{MONO}"' if mono else ''
    it = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}"{fam}{it} dominant-baseline="middle">{esc(s)}</text>\n')


def lines(x, y, rows, fs=14, gap=None, **kw):
    gap = gap or fs * 1.3
    y0 = y - gap * (len(rows) - 1) / 2
    return ''.join(text(x, y0 + i * gap, r, fs, **kw) for i, r in enumerate(rows))


def box(x, y, w, h, col=SLATE, label=None, fs=14, rx=10, weight='600', sw=2, dash=False, fill=None, tcol=None, mono=False):
    d = ' stroke-dasharray="6 4"' if dash else ''
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or col[1]}" '
         f'stroke="{col[0]}" stroke-width="{sw}"{d}/>\n')
    if label is not None:
        rows = label if isinstance(label, (list, tuple)) else [label]
        s += lines(x + w / 2, y + h / 2, rows, fs, weight=weight, fill=tcol or INK, mono=mono)
    return s


def arrow(x1, y1, x2, y2, color='ink', sw=2.5, dash=False, label=None, lfs=12, loff=(0, -10), both=False, lcol=None):
    d = ' stroke-dasharray="7 5"' if dash else ''
    st = f' marker-start="url(#ah-{color})"' if both else ''
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ARROW_COLORS[color]}" stroke-width="{sw}"'
         f'{d} marker-end="url(#ah-{color})"{st}/>\n')
    if label:
        s += text((x1 + x2) / 2 + loff[0], (y1 + y2) / 2 + loff[1], label, lfs, weight='600', fill=lcol or ARROW_COLORS[color])
    return s


def line(x1, y1, x2, y2, color=INK, sw=2.5, dash=False):
    d = ' stroke-dasharray="7 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>\n'


def path(d, stroke=INK, fill='none', sw=2.5, dash=False, marker=None):
    ds = ' stroke-dasharray="7 5"' if dash else ''
    m = f' marker-end="url(#ah-{marker})"' if marker else ''
    return f'<path d="{d}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}"{ds}{m}/>\n'


# ---------- icons (centered at cx, cy) ----------
def pc(cx, cy, label=None, sub=None, col=BLUE):
    s = (f'<rect x="{cx-26}" y="{cy-24}" width="52" height="36" rx="4" fill="{col[1]}" stroke="{col[0]}" stroke-width="2.5"/>'
         f'<rect x="{cx-20}" y="{cy-18}" width="40" height="24" rx="2" fill="#FFFFFF" stroke="{col[0]}" stroke-width="1"/>'
         f'<rect x="{cx-5}" y="{cy+12}" width="10" height="8" fill="{col[0]}"/>'
         f'<rect x="{cx-18}" y="{cy+20}" width="36" height="5" rx="2" fill="{col[0]}"/>\n')
    if label: s += text(cx, cy + 40, label, 13, weight='700')
    if sub: s += text(cx, cy + 57, sub, 12, fill=MUTED, mono=True)
    return s


def server(cx, cy, label=None, sub=None, col=SLATE):
    s = f'<rect x="{cx-22}" y="{cy-30}" width="44" height="60" rx="5" fill="{col[1]}" stroke="{col[0]}" stroke-width="2.5"/>'
    for i in range(3):
        yy = cy - 22 + i * 17
        s += (f'<rect x="{cx-16}" y="{yy}" width="32" height="11" rx="2" fill="#FFFFFF" stroke="{col[0]}" stroke-width="1.2"/>'
              f'<circle cx="{cx+10}" cy="{yy+5.5}" r="2.2" fill="#22C55E"/>')
    s += '\n'
    if label: s += text(cx, cy + 46, label, 13, weight='700')
    if sub: s += text(cx, cy + 63, sub, 12, fill=MUTED, mono=True)
    return s


def router(cx, cy, label=None, sub=None, col=BLUE):
    s = (f'<ellipse cx="{cx}" cy="{cy+8}" rx="34" ry="12" fill="{col[0]}"/>'
         f'<rect x="{cx-34}" y="{cy-8}" width="68" height="16" fill="{col[0]}"/>'
         f'<ellipse cx="{cx}" cy="{cy-8}" rx="34" ry="12" fill="#3B82F6" stroke="{col[0]}" stroke-width="2"/>'
         f'<path d="M{cx-18},{cy-8} L{cx+18},{cy-8} M{cx},{cy-16} L{cx},{cy}" stroke="#FFFFFF" stroke-width="2.5"/>'
         f'<path d="M{cx+12},{cy-12} L{cx+18},{cy-8} L{cx+12},{cy-4} M{cx-12},{cy-12} L{cx-18},{cy-8} L{cx-12},{cy-4}" '
         f'stroke="#FFFFFF" stroke-width="2.2" fill="none"/>\n')
    if label: s += text(cx, cy + 36, label, 13, weight='700')
    if sub: s += text(cx, cy + 53, sub, 12, fill=MUTED, mono=True)
    return s


def switch(cx, cy, label=None, sub=None, col=TEAL, w=90):
    s = (f'<rect x="{cx-w/2}" y="{cy-16}" width="{w}" height="32" rx="6" fill="{col[0]}"/>'
         f'<path d="M{cx-22},{cy-6} L{cx+18},{cy-6} M{cx+12},{cy-11} L{cx+18},{cy-6} L{cx+12},{cy-1} '
         f'M{cx+22},{cy+6} L{cx-18},{cy+6} M{cx-12},{cy+1} L{cx-18},{cy+6} L{cx-12},{cy+11}" '
         f'stroke="#FFFFFF" stroke-width="2.4" fill="none"/>\n')
    if label: s += text(cx, cy + 32, label, 13, weight='700')
    if sub: s += text(cx, cy + 49, sub, 12, fill=MUTED, mono=True)
    return s


def cloud(cx, cy, label='Internet', sc=1.0, col=SLATE):
    k = sc
    d = (f'M{cx-60*k},{cy+25*k} C{cx-95*k},{cy+25*k} {cx-95*k},{cy-20*k} {cx-58*k},{cy-18*k} '
         f'C{cx-55*k},{cy-50*k} {cx-5*k},{cy-52*k} {cx+5*k},{cy-28*k} '
         f'C{cx+25*k},{cy-50*k} {cx+70*k},{cy-40*k} {cx+62*k},{cy-10*k} '
         f'C{cx+95*k},{cy-8*k} {cx+95*k},{cy+28*k} {cx+60*k},{cy+25*k} Z')
    return path(d, stroke=col[0], fill=col[1], sw=2.5) + (text(cx, cy, label, 15, weight='700') if label else '')


def attacker(cx, cy, label='Attacker', sub=None):
    s = (f'<path d="M{cx-26},{cy+28} C{cx-26},{cy+2} {cx+26},{cy+2} {cx+26},{cy+28} Z" fill="#7F1D1D"/>'
         f'<circle cx="{cx}" cy="{cy-12}" r="17" fill="#7F1D1D"/>'
         f'<path d="M{cx-11},{cy-15} L{cx+11},{cy-15} L{cx+9},{cy-8} L{cx-9},{cy-8} Z" fill="#111827"/>'
         f'<circle cx="{cx-5}" cy="{cy-12}" r="2" fill="#F87171"/><circle cx="{cx+5}" cy="{cy-12}" r="2" fill="#F87171"/>\n')
    if label: s += text(cx, cy + 44, label, 13, weight='700', fill=RED[0])
    if sub: s += text(cx, cy + 61, sub, 12, fill=MUTED, mono=True)
    return s


def person(cx, cy, label=None, sub=None, col=BLUE):
    s = (f'<path d="M{cx-22},{cy+26} C{cx-22},{cy+2} {cx+22},{cy+2} {cx+22},{cy+26} Z" fill="{col[0]}"/>'
         f'<circle cx="{cx}" cy="{cy-10}" r="14" fill="{col[0]}"/>\n')
    if label: s += text(cx, cy + 42, label, 13, weight='700')
    if sub: s += text(cx, cy + 59, sub, 12, fill=MUTED, mono=True)
    return s


def lock(cx, cy, col=GREEN, sc=1.0, open_=False):
    k = sc
    arc = (f'M{cx-9*k},{cy-2*k} L{cx-9*k},{cy-10*k} A{9*k},{9*k} 0 0 1 {cx+9*k},{cy-10*k} L{cx+9*k},{cy-6*k}'
           if open_ else
           f'M{cx-9*k},{cy-2*k} L{cx-9*k},{cy-10*k} A{9*k},{9*k} 0 0 1 {cx+9*k},{cy-10*k} L{cx+9*k},{cy-2*k}')
    return (path(arc, stroke=col[0], sw=3.2 * k) +
            f'<rect x="{cx-13*k}" y="{cy-3*k}" width="{26*k}" height="{20*k}" rx="{3*k}" fill="{col[0]}"/>'
            f'<circle cx="{cx}" cy="{cy+6*k}" r="{3*k}" fill="#FFFFFF"/>\n')


def firewall(cx, cy, label='Firewall', sub=None, col=RED):
    s = f'<rect x="{cx-30}" y="{cy-28}" width="60" height="56" rx="4" fill="{col[1]}" stroke="{col[0]}" stroke-width="2.5"/>'
    for r in range(4):
        yy = cy - 28 + r * 14
        s += line(cx - 30, yy, cx + 30, yy, col[0], 1.5)
        off = 0 if r % 2 == 0 else 15
        for c in range(-1, 3):
            xx = cx - 30 + off + c * 30
            if cx - 30 < xx < cx + 30:
                s += line(xx, yy, xx, yy + 14, col[0], 1.5)
    s += '\n'
    if label: s += text(cx, cy + 44, label, 13, weight='700')
    if sub: s += text(cx, cy + 61, sub, 12, fill=MUTED, mono=True)
    return s


def badge(cx, cy, n, col=BLUE, r=13):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col[0]}"/>' + text(cx, cy + 1, str(n), 13, weight='700', fill='#FFFFFF'))


def cross(cx, cy, col=RED, r=11):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="#FFFFFF" stroke="{col[0]}" stroke-width="2.5"/>'
            + path(f'M{cx-r/2},{cy-r/2} L{cx+r/2},{cy+r/2} M{cx+r/2},{cy-r/2} L{cx-r/2},{cy+r/2}', stroke=col[0], sw=3))


def check(cx, cy, col=GREEN, r=11):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="#FFFFFF" stroke="{col[0]}" stroke-width="2.5"/>'
            + path(f'M{cx-r/2},{cy} L{cx-r/8},{cy+r/2} L{cx+r/1.6},{cy-r/2}', stroke=col[0], sw=3))


FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# =====================================================================
# PART 1 - NETWORKING
# =====================================================================
@fig('p1_osi_tcpip')
def _():
    W, H = 900, 560
    osi = [('7', 'Application', 'HTTP, DNS, SMTP', PURPLE), ('6', 'Presentation', 'TLS, JPEG, ASCII', PURPLE),
           ('5', 'Session', 'NetBIOS, RPC', PURPLE), ('4', 'Transport', 'TCP, UDP', BLUE),
           ('3', 'Network', 'IP, ICMP, OSPF', GREEN), ('2', 'Data Link', 'Ethernet, ARP, 802.1Q', AMBER),
           ('1', 'Physical', 'Cables, Wi-Fi radio, bits', SLATE)]
    pdu = {3: 'Segment', 4: 'Packet', 5: 'Frame', 6: 'Bits'}
    dev = {4: 'Router', 5: 'Switch', 6: 'Hub / cable'}
    b = text(250, 92, 'OSI model (7 layers)', 15, weight='700', fill=MUTED)
    b += text(560, 92, 'TCP/IP model', 15, weight='700', fill=MUTED)
    b += text(740, 92, 'Data unit (PDU)', 15, weight='700', fill=MUTED)
    y0, hh = 110, 60
    for i, (n, nm, ex, col) in enumerate(osi):
        y = y0 + i * hh
        b += box(80, y + 3, 340, hh - 6, col, None)
        b += badge(110, y + hh / 2, n, col)
        b += text(140, y + hh / 2 - 9, nm, 16, 'start', '700')
        b += text(140, y + hh / 2 + 12, ex, 12.5, 'start', fill=MUTED)
        if i in dev:
            b += text(410, y + hh / 2, dev[i], 12, 'end', '700', fill=col[0])
        b += text(740, y + hh / 2, pdu.get(i, 'Data'), 15, weight='600', fill=col[0])
    groups = [(0, 3, 'Application', PURPLE), (3, 1, 'Transport', BLUE), (4, 1, 'Internet', GREEN), (5, 2, 'Network Access', AMBER)]
    for s0, n, nm, col in groups:
        y = y0 + s0 * hh
        b += box(470, y + 3, 180, n * hh - 6, col, nm, 15)
        b += path(f'M425,{y+n*hh/2} L465,{y+n*hh/2}', stroke=col[0], sw=2, dash=True)
    b += text(W / 2, H - 22, 'Mnemonic (top-down): All People Seem To Need Data Processing', 13, italic=True, fill=MUTED)
    return svg(W, H, b, 'Network layers: OSI vs TCP/IP')


@fig('p1_encapsulation')
def _():
    W, H = 980, 420
    b = ''
    rows = [('Application', [('DATA', 360, PURPLE)], 'Data'),
            ('Transport', [('TCP hdr', 100, BLUE), ('DATA', 360, PURPLE)], 'Segment'),
            ('Network', [('IP hdr', 100, GREEN), ('TCP hdr', 100, BLUE), ('DATA', 360, PURPLE)], 'Packet'),
            ('Data Link', [('ETH hdr', 100, AMBER), ('IP hdr', 100, GREEN), ('TCP hdr', 100, BLUE), ('DATA', 360, PURPLE), ('FCS', 60, AMBER)], 'Frame')]
    for i, (layer, parts, name) in enumerate(rows):
        y = 85 + i * 75
        total = sum(p[1] for p in parts)
        x = 860 - total
        b += text(30, y + 25, layer, 15, 'start', '700')
        for lab, w, col in parts:
            b += box(x, y, w - 4, 50, col, lab, 14)
            x += w
        b += box(872, y + 10, 90, 30, SLATE, name, 13, rx=15, weight='700', tcol=MUTED)
    b += text(40, 395, 'Sender: each layer ADDS its header (encapsulation).  Receiver: each layer REMOVES it (de-encapsulation).', 13.5, 'start', fill=MUTED)
    return svg(W, H, b, 'Encapsulation: every layer wraps the one above it')


@fig('p1_switch_learning')
def _():
    W, H = 900, 470
    b = switch(330, 240, 'SW1', w=150)
    hosts = [(110, 110, 'PC-A', 'AAAA  Fa0/1'), (550, 110, 'PC-B', 'BBBB  Fa0/2'),
             (110, 360, 'PC-C', 'CCCC  Fa0/3'), (550, 360, 'PC-D', 'DDDD  Fa0/4')]
    ends = [(285, 224), (375, 224), (285, 256), (375, 256)]
    for (x, y, n, m), (ex, ey) in zip(hosts, ends):
        b += line(x + (30 if x < 330 else -30), y + (22 if y < 240 else -28), ex, ey, '#94A3B8', 3)
        b += pc(x, y, n, m)
    b += arrow(165, 150, 262, 210, 'blue', 3.5)
    b += badge(205, 168, 1, BLUE)
    for (tx, ty) in [(495, 150), (165, 330), (495, 330)]:
        b += arrow(330 + (45 if tx > 330 else -45), 240 + (-22 if ty < 240 else 22), tx, ty, 'amber', 3, dash=True)
    b += badge(452, 175, 2, AMBER)
    b += box(625, 95, 255, 300, SLATE, None, fill='#FFFFFF')
    b += text(752, 117, 'MAC address table', 14, weight='700')
    b += line(635, 133, 870, 133, '#CBD5E1', 1.5)
    b += text(700, 150, 'MAC', 13, weight='700', fill=MUTED) + text(810, 150, 'Port', 13, weight='700', fill=MUTED)
    b += box(637, 163, 231, 30, GREEN, None, rx=4, sw=1.5)
    b += text(700, 178, 'AAAA', 14, mono=True) + text(810, 178, 'Fa0/1', 14, mono=True)
    b += text(752, 210, '(BBBB not learned yet)', 12, fill=MUTED, italic=True)
    b += badge(650, 250, 1, BLUE, 11) + text(668, 250, 'A sends to B: switch LEARNS', 12.5, 'start', '700')
    b += text(668, 270, 'source AAAA on port Fa0/1', 12.5, 'start')
    b += badge(650, 310, 2, AMBER, 11) + text(668, 310, 'Destination BBBB unknown:', 12.5, 'start', '700')
    b += text(668, 330, 'FLOOD out all other ports', 12.5, 'start')
    b += text(668, 360, 'When B replies, BBBB is', 12.5, 'start', fill=MUTED)
    b += text(668, 378, 'learned too -> no more flood', 12.5, 'start', fill=MUTED)
    b += text(450, 445, 'Learn the SOURCE  ->  forward by the DESTINATION  ->  unknown = flood  ->  forget after 300 s', 13.5, fill=MUTED)
    return svg(W, H, b, 'How a switch learns MAC addresses')

@fig('p1_ip_anatomy')
def _():
    W, H = 900, 400
    octs = ['192', '168', '10', '37']
    bins = [format(int(o), '08b') for o in octs]
    b = ''
    x0, cw = 70, 190
    for i, (o, bn) in enumerate(zip(octs, bins)):
        x = x0 + i * cw
        col = BLUE if i < 3 else GREEN
        b += box(x, 85, cw - 20, 52, col, o, 26, weight='700')
        b += text(x + (cw - 20) / 2, 152, f'octet {i+1}', 12, fill=MUTED)
        for k, bit in enumerate(bn):
            bx = x + 2 + k * 20.7
            b += box(bx, 172, 18, 30, col, bit, 15, rx=3, sw=1.4, mono=True, weight='700')
        if i < 3:
            b += text(x + cw - 10, 112, '.', 30, weight='700')
    b += path(f'M{x0},222 L{x0},236 L{x0+3*cw-22},236 L{x0+3*cw-22},222', stroke=BLUE[0], sw=2.5)
    b += text(x0 + (3 * cw - 22) / 2, 258, 'NETWORK part = first 24 bits  (/24)', 15, weight='700', fill=BLUE[0])
    b += path(f'M{x0+3*cw},222 L{x0+3*cw},236 L{x0+4*cw-22},236 L{x0+4*cw-22},222', stroke=GREEN[0], sw=2.5)
    b += text(x0 + 3 * cw + (cw - 22) / 2, 258, 'HOST part (8 bits)', 15, weight='700', fill=GREEN[0])
    b += box(70, 285, 760, 90, SLATE, None, fill='#F8FAFC')
    b += text(90, 308, 'Mask /24  =  255.255.255.0  =  11111111.11111111.11111111.00000000', 14, 'start', mono=True)
    b += text(90, 332, 'Network  =  192.168.10.0      Broadcast  =  192.168.10.255', 14, 'start', mono=True)
    b += text(90, 356, 'Usable hosts  =  2^8 - 2  =  254   (192.168.10.1  ...  192.168.10.254)', 14, 'start', mono=True)
    return svg(W, H, b, 'Anatomy of an IPv4 address: 192.168.10.37/24')


@fig('p1_subnet_blocks')
def _():
    W, H = 900, 400
    b = text(450, 80, 'Split 192.168.10.0/24 into 4 equal subnets -> borrow 2 bits -> /26 -> block size 64', 14.5, fill=MUTED)
    cols = [BLUE, GREEN, AMBER, PURPLE]
    x0, ww = 50, 200
    for i in range(4):
        x = x0 + i * ww
        n = i * 64
        b += box(x, 110, ww - 4, 120, cols[i], None)
        b += text(x + ww / 2 - 2, 132, f'Subnet {i+1}', 15, weight='700', fill=cols[i][0])
        b += text(x + ww / 2 - 2, 158, f'.{n}/26', 18, weight='700', mono=True)
        b += text(x + ww / 2 - 2, 186, f'hosts .{n+1} - .{n+62}', 13, mono=True)
        b += text(x + ww / 2 - 2, 210, f'broadcast .{n+63}', 13, mono=True, fill=RED[0])
        b += text(x, 250, str(n), 13, 'start', weight='700', fill=MUTED, mono=True)
    b += text(x0 + 4 * ww - 4, 250, '255', 13, 'end', weight='700', fill=MUTED, mono=True)
    b += line(x0, 240, x0 + 4 * ww - 4, 240, MUTED, 2)
    b += box(50, 280, 796, 95, SLATE, None, fill='#F8FAFC')
    b += text(70, 302, 'The 4-step method:', 14, 'start', '700')
    b += text(70, 326, '1) how many subnets / hosts?   2) bits to borrow: 2^n >= 4  ->  n = 2', 14, 'start', mono=True)
    b += text(70, 350, '3) new prefix: /24 + 2 = /26   4) block size: 256 - 192 = 64  ->  0, 64, 128, 192', 14, 'start', mono=True)
    return svg(W, H, b, 'Subnetting: one /24 becomes four /26')


@fig('p1_vlan_trunk')
def _():
    W, H = 900, 440
    b = switch(260, 220, 'SW1', w=130) + switch(640, 220, 'SW2', w=130)
    b += line(325, 220, 575, 220, AMBER[0], 7)
    b += text(450, 196, 'TRUNK (802.1Q)', 14, weight='700', fill=AMBER[0])
    b += box(365, 236, 80, 26, BLUE, 'tag 10', 12, rx=13)
    b += box(455, 236, 80, 26, GREEN, 'tag 20', 12, rx=13)
    for x, y, nm, col, v in [(150, 100, 'PC1', BLUE, 'VLAN 10'), (150, 350, 'PC2', GREEN, 'VLAN 20'),
                             (750, 100, 'PC3', BLUE, 'VLAN 10'), (750, 350, 'PC4', GREEN, 'VLAN 20')]:
        sx = 260 if x < 450 else 640
        b += line(x + ((30 if x < 450 else -30) if y < 220 else 0), y + (0 if y < 220 else -26), sx + (-30 if x < 450 else 30), 220 + (-16 if y < 220 else 16), col[0], 3.5)
        b += pc(x, y, nm, None, col)
        b += box(x - 135 if x < 450 else x + 45, y - 12, 90, 24, col, v, 12, rx=12)
    b += text(450, 300, 'access ports: one VLAN each, frames leave untagged', 13, fill=MUTED)
    b += text(450, 322, 'trunk port: carries many VLANs, each frame gets a 4-byte tag', 13, fill=MUTED)
    b += text(450, 410, 'PC1 <-> PC3 talk (same VLAN 10).  PC1 <-> PC2 need a ROUTER (different VLANs).', 14, weight='700')
    return svg(W, H, b, 'VLANs and a trunk between two switches')


@fig('p1_8021q_frame')
def _():
    W, H = 900, 330
    b = text(40, 90, 'Normal Ethernet frame', 14, 'start', '700', fill=MUTED)
    parts = [('Dest MAC', 130, SLATE), ('Src MAC', 130, SLATE), ('Type', 80, SLATE), ('Data (payload)', 320, PURPLE), ('FCS', 70, SLATE)]
    x = 40
    for lab, w, c in parts:
        b += box(x, 105, w - 4, 44, c, lab, 14); x += w
    b += text(40, 185, 'Tagged 802.1Q frame (on a trunk)', 14, 'start', '700', fill=MUTED)
    parts = [('Dest MAC', 130, SLATE), ('Src MAC', 130, SLATE), ('802.1Q TAG', 110, AMBER), ('Type', 80, SLATE), ('Data', 210, PURPLE), ('FCS', 70, SLATE)]
    x = 40
    for lab, w, c in parts:
        b += box(x, 200, w - 4, 44, c, lab, 14, weight='700' if c == AMBER else '600'); x += w
    b += path('M300,246 L250,280 M406,246 L560,280', stroke=AMBER[0], sw=1.8, dash=True)
    b += box(250, 278, 310, 36, AMBER, 'TPID 0x8100 | PRI 3b | VLAN ID 12 bits', 12.5, fill='#FFFBEB', mono=True)
    b += text(590, 296, '12 bits -> VLANs 1..4094', 13, 'start', '700', fill=AMBER[0])
    return svg(W, H, b, 'The 4-byte 802.1Q tag')


@fig('p1_stp_loop')
def _():
    W, H = 900, 430
    b = ''
    A, B, C = (450, 120), (230, 320), (670, 320)
    b += line(*A, *B, GREEN[0], 5) + line(*A, *C, GREEN[0], 5) + line(*B, *C, '#94A3B8', 5, dash=True)
    b += switch(*A, None, w=110) + switch(*B, None, w=110) + switch(*C, None, w=110)
    b += box(380, 62, 140, 28, AMBER, 'ROOT BRIDGE', 13, rx=14, weight='700')
    b += text(515, 122, 'SW1  priority 4096', 13, 'start', '700')
    b += text(230, 358, 'SW2  priority 32768', 13, weight='700')
    b += text(670, 358, 'SW3  priority 32768', 13, weight='700')
    b += text(305, 272, 'RP', 13, weight='700', fill=GREEN[0]) + text(595, 272, 'RP', 13, weight='700', fill=GREEN[0])
    b += text(430, 172, 'DP', 13, weight='700', fill=BLUE[0]) + text(470, 172, 'DP', 13, weight='700', fill=BLUE[0])
    b += text(298, 305, 'DP', 13, weight='700', fill=BLUE[0])
    b += cross(595, 320)
    b += text(595, 293, 'BLOCKED', 12, weight='700', fill=RED[0])
    b += box(40, 380, 820, 36, SLATE, 'RP = Root Port (best path to root)   DP = Designated Port (forwards)   X = blocked -> no loop', 13, fill='#F8FAFC', weight='600')
    return svg(W, H, b, 'Spanning Tree breaks the loop by blocking one port')


@fig('p1_nat')
def _():
    W, H = 900, 420
    b = box(30, 80, 300, 300, BLUE, None, dash=True, fill='#F8FBFF')
    b += text(180, 102, 'INSIDE (private)', 14, weight='700', fill=BLUE[0])
    b += pc(110, 170, 'PC1', '10.0.0.11') + pc(250, 170, 'PC2', '10.0.0.12')
    b += pc(180, 300, 'PC3', '10.0.0.13')
    b += router(430, 230, 'R1 (NAT)', None)
    b += text(430, 300, 'public: 203.0.113.5', 12, fill=MUTED, mono=True)
    b += line(330, 230, 396, 230, BLUE[0], 3)
    b += cloud(760, 140, 'Internet', 0.9)
    b += line(466, 222, 690, 150, '#94A3B8', 3)
    b += box(510, 250, 365, 140, SLATE, None, fill='#FFFFFF')
    b += text(692, 270, 'NAT / PAT translation table', 14, weight='700')
    b += line(520, 285, 865, 285, '#CBD5E1', 1.5)
    b += text(600, 302, 'Inside local', 12, weight='700', fill=MUTED) + text(780, 302, 'Inside global', 12, weight='700', fill=MUTED)
    for i, (a, g) in enumerate([('10.0.0.11:5001', '203.0.113.5:5001'), ('10.0.0.12:5002', '203.0.113.5:5002'), ('10.0.0.13:5003', '203.0.113.5:5003')]):
        b += text(600, 325 + i * 22, a, 12.5, mono=True) + text(780, 325 + i * 22, g, 12.5, mono=True)
    b += text(560, 210, 'src 10.0.0.11 -> 203.0.113.5', 12, 'start', '700', fill=AMBER[0], mono=True)
    return svg(W, H, b, 'NAT/PAT: many private hosts share one public address')


@fig('p1_ios_modes')
def _():
    W, H = 900, 440
    b = box(40, 80, 820, 310, SLATE, None, fill='#F8FAFC')
    b += text(60, 102, 'User EXEC   Router>', 15, 'start', '700', mono=True)
    b += text(840, 102, 'look only (ping, show)', 13, 'end', fill=MUTED)
    b += box(80, 125, 760, 250, BLUE, None)
    b += text(100, 147, 'Privileged EXEC   Router#', 15, 'start', '700', mono=True)
    b += text(820, 147, 'all show + copy, reload, debug', 13, 'end', fill=MUTED)
    b += box(120, 170, 700, 190, GREEN, None)
    b += text(140, 192, 'Global config   Router(config)#', 15, 'start', '700', mono=True)
    b += text(800, 192, 'changes the whole device', 13, 'end', fill=MUTED)
    for i, (p, d) in enumerate([('Router(config-if)#', 'one interface'), ('Router(config-line)#', 'console / vty lines'), ('Router(config-router)#', 'routing protocol')]):
        y = 215 + i * 46
        b += box(160, y, 620, 38, AMBER, None)
        b += text(180, y + 19, p, 14, 'start', '700', mono=True) + text(760, y + 19, d, 13, 'end', fill=MUTED)
    b += text(450, 415, 'enable  ->  configure terminal  ->  interface g0/0     |     exit = one level up,  end / Ctrl+Z = back to #', 13, mono=True, fill=INK)
    return svg(W, H, b, 'Cisco IOS command modes (each mode lives inside the previous one)')


@fig('p1_routing_table')
def _():
    W, H = 900, 380
    b = router(130, 200, 'R1', None)
    b += text(130, 260, 'dest = 10.10.5.5', 13, weight='700', fill=AMBER[0], mono=True)
    b += box(250, 90, 610, 250, SLATE, None, fill='#FFFFFF')
    b += text(555, 112, 'R1 routing table', 15, weight='700')
    hdr = ['Code', 'Prefix', 'AD/metric', 'Next hop']
    xs = [290, 420, 600, 760]
    for x, h in zip(xs, hdr): b += text(x, 140, h, 13, weight='700', fill=MUTED)
    rows = [('C', '10.1.1.0/24', '0/0', 'directly'), ('S', '10.0.0.0/8', '1/0', '192.168.1.2'),
            ('O', '10.10.0.0/16', '110/20', '192.168.2.2'), ('S*', '0.0.0.0/0', '1/0', '203.0.113.1')]
    for i, r in enumerate(rows):
        y = 172 + i * 36
        win = i == 2
        if win: b += box(262, y - 15, 586, 30, GREEN, None, rx=6, sw=1.5)
        for x, c in zip(xs, r): b += text(x, y, c, 14, mono=True, weight='700' if win else '400')
    b += arrow(170, 200, 258, 244, 'green', 2.5)
    b += text(555, 318, 'Longest prefix match wins: /16 is more specific than /8 and /0', 13.5, weight='700', fill=GREEN[0])
    return svg(W, H, b, 'How a router picks a route')


@fig('p1_arp')
def _():
    W, H = 900, 430
    b = switch(450, 230, 'SW1', w=130)
    hosts = [(110, 120, 'PC-A', '192.168.1.10', BLUE), (790, 120, 'PC-B', '192.168.1.20', GREEN),
             (110, 340, 'PC-C', '192.168.1.30', SLATE), (790, 340, 'PC-D', '192.168.1.40', SLATE)]
    for x, y, n, ip, col in hosts:
        b += line(x + (32 if x < 450 else -32), y, 450 + (-50 if x < 450 else 50), 230 + (-16 if y < 230 else 16), '#94A3B8', 3)
        b += pc(x, y, n, ip, col)
    b += box(170, 160, 230, 46, BLUE, ['1. ARP Request (broadcast)', 'Who has 192.168.1.20?'], 12.5)
    b += box(520, 160, 230, 46, GREEN, ['2. ARP Reply (unicast)', '192.168.1.20 is at BB:BB'], 12.5)
    b += text(110, 410, 'C and D also receive the request, see it is not for them, and drop it', 12.5, 'start', fill=MUTED)
    b += box(560, 270, 300, 40, SLATE, 'PC-A ARP cache: 192.168.1.20 -> BB:BB', 12.5, fill='#FFFFFF', mono=True, weight='700')
    return svg(W, H, b, 'ARP: finding the MAC address of an IP address')


# =====================================================================
# PART 2 - SECURITY
# =====================================================================
@fig('s1_cia_triad')
def _():
    W, H = 900, 470
    b = path('M450,95 L215,395 L685,395 Z', stroke=INK, fill='#F8FAFC', sw=3)
    b += box(345, 70, 210, 64, BLUE, ['Confidentiality', 'only the right people read'], 13)
    b += box(90, 360, 250, 64, GREEN, ['Integrity', 'data is not changed'], 13)
    b += box(560, 360, 250, 64, AMBER, ['Availability', 'service works when needed'], 13)
    b += lock(450, 255, BLUE, 1.6)
    b += text(450, 310, 'CIA', 24, weight='800')
    b += text(150, 140, 'Attack: eavesdropping', 12.5, 'start', '700', fill=RED[0])
    b += text(150, 160, 'Defense: encryption, ACL', 12.5, 'start', fill=MUTED)
    b += text(40, 260, 'Attack: tampering', 12.5, 'start', '700', fill=RED[0])
    b += text(40, 280, 'Defense: hash, signature', 12.5, 'start', fill=MUTED)
    b += text(860, 260, 'Attack: DoS / DDoS', 12.5, 'end', '700', fill=RED[0])
    b += text(860, 280, 'Defense: redundancy, backups', 12.5, 'end', fill=MUTED)
    return svg(W, H, b, 'The CIA triad - the three goals of security')


@fig('s1_ddos')
def _():
    W, H = 900, 430
    b = attacker(90, 210, 'Attacker', 'C&C commands')
    bots = [(330, 90), (330, 170), (330, 250), (330, 330)]
    for i, (x, y) in enumerate(bots):
        b += arrow(130, 210, x - 32, y, 'slate', 2, dash=True)
        b += pc(x, y - 4, None, None, RED)
        b += text(x + 40, y - 6, f'bot {i+1}', 12, 'start', '700', fill=RED[0])
        b += arrow(x + 80, y - 4, 640, 210, 'red', 3)
    b += server(700, 210, 'Victim web server', 'shop.example')
    b += box(600, 300, 230, 50, RED, ['service down', '(Availability lost)'], 13)
    b += text(450, 395, 'Botnet = thousands of infected devices flood one target at the same time', 14, weight='700')
    return svg(W, H, b, 'DDoS: a botnet floods one victim')


@fig('s1_risk_terms')
def _():
    W, H = 900, 300
    items = [('Asset', 'what we protect', 'customer DB', BLUE), ('Vulnerability', 'a weakness', 'unpatched server', AMBER),
             ('Threat', 'who / what can exploit it', 'ransomware gang', RED), ('Risk', 'chance x damage', 'HIGH', PURPLE),
             ('Control', 'what reduces risk', 'patch + backup', GREEN)]
    for i, (n, d, ex, col) in enumerate(items):
        x = 30 + i * 172
        b = '' if i == 0 else b
        b += box(x, 90, 150, 120, col, None)
        b += text(x + 75, 115, n, 16, weight='700', fill=col[0])
        b += text(x + 75, 145, d, 12.5)
        b += text(x + 75, 182, 'e.g. ' + ex, 12, fill=MUTED, italic=True)
        if i < 4: b += arrow(x + 152, 150, x + 170, 150, 'ink', 2.5)
    b += text(450, 250, 'Risk exists only when a THREAT can exploit a VULNERABILITY of a valuable ASSET', 14, weight='700')
    return svg(W, H, b, 'The language of risk')


@fig('s2_telnet_ssh')
def _():
    W, H = 900, 420
    b = ''
    for row, (proto, port, col, secure) in enumerate([('Telnet', 'TCP 23', RED, False), ('SSH', 'TCP 22', GREEN, True)]):
        y = 140 + row * 170
        b += pc(90, y, 'Admin', None)
        b += router(800, y, 'R1', None)
        b += line(130, y, 760, y, col[0], 4)
        b += box(330, y - 22, 240, 44, col, None, fill='#FFFFFF')
        if secure:
            b += text(450, y, 'x9#Qa!7Lk2@pZ...', 15, mono=True, weight='700', fill=GREEN[0])
            b += lock(310, y, GREEN, 1.3)
        else:
            b += text(450, y, 'password: cisco123', 15, mono=True, weight='700', fill=RED[0])
            b += lock(310, y, RED, 1.3, open_=True)
        b += text(450, y - 48, f'{proto}  ({port})  -  {"encrypted" if secure else "clear text"}', 15, weight='700', fill=col[0])
        if not secure:
            b += attacker(450, y + 70, None)
            b += text(530, y + 72, 'sniffer reads everything', 13, 'start', '700', fill=RED[0])
            b += arrow(450, y + 45, 450, y + 25, 'red', 2.5)
    return svg(W, H, b, 'Telnet vs SSH: the same login, seen by an eavesdropper')


@fig('s2_hardening')
def _():
    W, H = 900, 380
    items = [('Physical', 'locked room, console password', SLATE), ('Passwords', 'enable secret, min-length, service password-encryption', BLUE),
             ('Remote access', 'SSH only, ACL on vty, exec-timeout', GREEN), ('Login protection', 'login block-for, banner motd', AMBER),
             ('Monitoring', 'Syslog + NTP + SNMPv3', PURPLE), ('Services', 'disable unused (CDP, HTTP), AutoSecure', RED)]
    for i, (n, d, col) in enumerate(items):
        y = 80 + i * 47
        b = '' if i == 0 else b
        b += box(60 + i * 18, y, 780 - i * 36, 40, col, None)
        b += text(80 + i * 18, y + 20, n, 15, 'start', '700', fill=col[0])
        b += text(820 - i * 18, y + 20, d, 13, 'end', mono=True)
    return svg(W, H, b, 'Device hardening - layers of protection for a router')


@fig('s3_aaa_flow')
def _():
    W, H = 900, 420
    b = person(80, 200, 'User', 'admin') + router(390, 200, 'NAS / Router', None) + server(760, 200, 'AAA server', 'RADIUS / TACACS+')
    b += arrow(115, 180, 345, 180, 'blue', 2.5, label='1. ssh: user + password')
    b += arrow(430, 180, 725, 180, 'blue', 2.5, label='2. Access-Request')
    b += arrow(725, 222, 430, 222, 'green', 2.5, label='3. Accept + privilege 15', loff=(0, 14))
    b += arrow(345, 222, 115, 222, 'green', 2.5, label='4. prompt R1#', loff=(0, 14))
    for i, (a, d, col) in enumerate([('Authentication', 'WHO are you?', BLUE), ('Authorization', 'WHAT may you do?', GREEN), ('Accounting', 'WHAT did you do?', AMBER)]):
        x = 60 + i * 270
        b += box(x, 300, 250, 80, col, None)
        b += text(x + 125, 325, a, 16, weight='700', fill=col[0])
        b += text(x + 125, 355, d, 14)
    return svg(W, H, b, 'AAA: three questions answered by one central server')


@fig('s4_dmz')
def _():
    W, H = 900, 475
    b = firewall(450, 200, None, None) + text(450, 156, 'Firewall', 13, weight='700')
    b += box(30, 90, 260, 230, GREEN, None, dash=True, fill='#F0FDF4')
    b += text(160, 112, 'INSIDE (trusted)', 14, weight='700', fill=GREEN[0])
    b += pc(100, 190, 'PC') + server(210, 190, 'File srv')
    b += box(330, 330, 240, 130, AMBER, None, dash=True, fill='#FFFBEB')
    b += text(345, 348, 'DMZ (semi-trusted)', 14, 'start', '700', fill=AMBER[0])
    b += server(400, 400, None) + server(500, 400, None)
    b += text(450, 446, 'Web + Mail servers', 12, weight='700')
    b += cloud(760, 200, 'OUTSIDE', 0.9, RED)
    b += line(290, 200, 418, 200, GREEN[0], 3) + line(482, 200, 680, 200, RED[0], 3) + line(450, 230, 450, 330, AMBER[0], 3)
    b += text(355, 185, 'inside -> any: ALLOW', 11.5, weight='700', fill=GREEN[0])
    b += text(585, 182, 'outside -> DMZ web 80/443: ALLOW', 11.5, weight='700', fill=AMBER[0])
    b += text(580, 235, 'outside -> inside: DENY', 11.5, weight='700', fill=RED[0])
    b += text(720, 330, 'DMZ -> inside: DENY', 12, weight='700', fill=RED[0])
    b += text(720, 350, '(a hacked web server', 11.5, fill=MUTED) + text(720, 366, 'cannot reach the LAN)', 11.5, fill=MUTED)
    return svg(W, H, b, 'Three zones: inside, DMZ, outside')


@fig('s4_acl_process')
def _():
    W, H = 900, 430
    b = box(40, 80, 200, 60, BLUE, ['packet arrives', 'src 10.1.1.50'], 14)
    rules = [('10', 'deny host 10.1.1.66', False), ('20', 'permit 10.1.1.0 0.0.0.255', True), ('30', 'deny any', None)]
    for i, (n, r, hit) in enumerate(rules):
        y = 90 + i * 90
        col = GREEN if hit else SLATE
        b += box(330, y, 330, 50, col, f'{n}  {r}', 14, mono=True, weight='700' if hit else '400')
        if hit is False: b += text(690, y + 25, 'no match -> next line', 13, 'start', fill=MUTED)
        if hit: b += text(690, y + 25, 'MATCH -> PERMIT, stop', 13, 'start', '700', fill=GREEN[0])
        if i < 2: b += arrow(495, y + 52, 495, y + 88, 'slate', 2)
    b += arrow(240, 110, 326, 115, 'blue', 2.5)
    b += box(330, 360, 330, 46, RED, 'implicit deny any (invisible)', 14, dash=True)
    b += text(690, 383, 'always the last line', 13, 'start', fill=RED[0])
    b += text(160, 230, 'Top -> down', 16, weight='700')
    b += text(160, 255, 'first match wins', 14, fill=MUTED)
    b += text(160, 280, 'order matters!', 14, fill=MUTED)
    return svg(W, H, b, 'How an ACL is processed')


@fig('s5_ids_ips')
def _():
    W, H = 900, 430
    b = text(450, 82, 'IDS - promiscuous (copy of traffic)', 15, weight='700', fill=AMBER[0])
    b += cloud(110, 150, 'Internet', 0.6) + switch(450, 150, None, w=100) + server(780, 150, None)
    b += line(160, 150, 400, 150, INK, 3) + line(500, 150, 750, 150, INK, 3)
    b += box(390, 200, 120, 40, AMBER, 'IDS sensor', 14)
    b += arrow(450, 168, 450, 198, 'amber', 2.5, dash=True)
    b += text(530, 220, 'SPAN copy -> alert only, attack still reaches server', 12.5, 'start', fill=MUTED)
    b += line(30, 265, 870, 265, '#E2E8F0', 2)
    b += text(450, 290, 'IPS - inline (traffic passes through it)', 15, weight='700', fill=GREEN[0])
    b += cloud(110, 360, 'Internet', 0.6) + box(390, 335, 120, 50, GREEN, 'IPS', 16) + server(780, 360, None)
    b += line(160, 360, 390, 360, INK, 3) + line(510, 360, 750, 360, INK, 3)
    b += cross(450, 318)
    b += text(530, 405, 'can DROP the malicious packet in real time', 12.5, 'start', fill=MUTED)
    return svg(W, H, b, 'IDS vs IPS - where they sit and what they can do')


@fig('s5_outcomes')
def _():
    W, H = 900, 400
    b = text(520, 85, 'Was there a real attack?', 15, weight='700', fill=MUTED)
    b += text(390, 112, 'YES (attack)', 14, weight='700') + text(650, 112, 'NO (normal traffic)', 14, weight='700')
    b += text(130, 190, 'Alarm', 15, weight='700') + text(130, 210, 'raised', 15, weight='700')
    b += text(130, 300, 'No alarm', 15, weight='700')
    cells = [(260, 130, GREEN, 'True Positive', 'correct alert'), (520, 130, AMBER, 'False Positive', 'false alarm - annoying'),
             (260, 250, RED, 'False Negative', 'MISSED attack - dangerous!'), (520, 250, GREEN, 'True Negative', 'correctly quiet')]
    for x, y, c, t, d in cells:
        b += box(x, y, 250, 105, c, None)
        b += text(x + 125, y + 40, t, 17, weight='700', fill=c[0])
        b += text(x + 125, y + 70, d, 13.5)
    return svg(W, H, b, 'IDS/IPS alarm outcomes')


@fig('s6_mac_flooding')
def _():
    W, H = 900, 440
    b = attacker(110, 200, 'Attacker', 'macof')
    b += switch(420, 200, 'SW1', w=130)
    b += arrow(150, 190, 352, 196, 'red', 3, label='thousands of fake source MACs')
    b += box(330, 260, 180, 130, RED, None, fill='#FFFFFF')
    b += text(420, 278, 'MAC table: FULL', 13, weight='700', fill=RED[0])
    for i, m in enumerate(['0a:1f:..  Fa0/1', '7c:22:..  Fa0/1', '91:e4:..  Fa0/1', '... 8000 entries']):
        b += text(420, 302 + i * 21, m, 12, mono=True)
    for i, y in enumerate([110, 290]):
        b += pc(760, y, f'PC{i+1}', None)
        b += arrow(488, 200, 718, y + (20 if i == 0 else -20), 'amber', 2.5, dash=True)
    b += text(700, 205, 'switch now FLOODS everything', 13, weight='700', fill=AMBER[0])
    b += text(700, 225, '= acts like a hub, attacker sniffs', 12.5, fill=MUTED)
    b += box(40, 395, 280, 34, GREEN, 'Defense: Port Security', 14)
    return svg(W, H, b, 'MAC flooding attack')


@fig('s6_arp_spoofing')
def _():
    W, H = 900, 470
    b = pc(110, 130, 'Victim', '10.0.0.10') + router(780, 130, 'Gateway', '10.0.0.1')
    b += attacker(450, 300, 'Attacker', 'MAC EE:EE')
    b += line(150, 130, 740, 130, '#CBD5E1', 3, dash=True)
    b += text(450, 112, 'original direct path', 12.5, fill=MUTED)
    b += arrow(420, 290, 155, 165, 'red', 2.5)
    b += arrow(480, 290, 745, 165, 'red', 2.5)
    b += box(90, 250, 200, 30, RED, '"10.0.0.1 is at EE:EE"', 12.5, fill='#FFFFFF', mono=True)
    b += box(610, 250, 210, 30, RED, '"10.0.0.10 is at EE:EE"', 12.5, fill='#FFFFFF', mono=True)
    b += text(450, 395, 'Traffic now flows: Victim -> Attacker -> Gateway  =  Man-in-the-Middle', 14, weight='700', fill=RED[0])
    b += box(330, 418, 240, 32, GREEN, 'Defense: DHCP Snooping + DAI', 13)
    return svg(W, H, b, 'ARP spoofing: gratuitous ARP lies -> MITM')


@fig('s6_dhcp_snooping')
def _():
    W, H = 900, 400
    b = switch(450, 200, None, w=150) + text(450, 172, 'SW1 (snooping ON)', 13, weight='700')
    b += server(110, 200, 'Real DHCP', '10.0.0.5')
    b += attacker(790, 200, 'Rogue DHCP', None)
    b += pc(450, 330, 'Client', None)
    b += line(140, 200, 375, 200, GREEN[0], 4) + line(525, 200, 760, 200, RED[0], 4)
    b += line(450, 216, 450, 300, BLUE[0], 3)
    b += box(190, 140, 140, 30, GREEN, 'TRUSTED port', 13)
    b += box(570, 140, 150, 30, RED, 'UNTRUSTED port', 13)
    b += cross(640, 200)
    b += text(600, 245, 'OFFER from untrusted = DROPPED', 12.5, weight='700', fill=RED[0])
    b += text(260, 245, 'OFFER/ACK allowed', 12.5, weight='700', fill=GREEN[0])
    return svg(W, H, b, 'DHCP snooping: only trusted ports may answer')


@fig('s7_sym_asym')
def _():
    W, H = 900, 470
    b = text(450, 82, 'Symmetric: ONE shared secret key', 15, weight='700', fill=BLUE[0])
    b += person(80, 150, 'Alice') + person(820, 150, 'Bob')
    b += box(170, 125, 140, 50, SLATE, 'Hello', 15, fill='#FFFFFF')
    b += arrow(312, 150, 368, 150, 'blue', 2.5)
    b += box(370, 125, 160, 50, BLUE, 'k#9Lq..', 15, mono=True)
    b += arrow(532, 150, 588, 150, 'blue', 2.5)
    b += box(590, 125, 140, 50, SLATE, 'Hello', 15, fill='#FFFFFF')
    b += text(340, 196, 'encrypt with K', 12, fill=MUTED) + text(560, 196, 'decrypt with K', 12, fill=MUTED)
    b += text(450, 222, 'AES, 3DES - fast, but how do we share K safely?', 13, weight='700')
    b += line(30, 245, 870, 245, '#E2E8F0', 2)
    b += text(450, 272, 'Asymmetric: key PAIR (public + private)', 15, weight='700', fill=GREEN[0])
    b += person(80, 345, 'Alice') + person(820, 345, 'Bob')
    b += box(170, 320, 140, 50, SLATE, 'Hello', 15, fill='#FFFFFF')
    b += arrow(312, 345, 368, 345, 'green', 2.5)
    b += box(370, 320, 160, 50, GREEN, 'Zx7!p..', 15, mono=True)
    b += arrow(532, 345, 588, 345, 'green', 2.5)
    b += box(590, 320, 140, 50, SLATE, 'Hello', 15, fill='#FFFFFF')
    b += text(340, 391, "Bob's PUBLIC key", 12, fill=MUTED) + text(560, 391, "Bob's PRIVATE key", 12, fill=MUTED)
    b += text(450, 425, "RSA, ECC - no shared secret needed, but ~1000x slower", 13, weight='700')
    b += text(450, 450, 'Real life (HTTPS): asymmetric to exchange a key, then symmetric for the data = HYBRID', 12.5, fill=MUTED)
    return svg(W, H, b, 'Symmetric vs asymmetric encryption')


@fig('s7_hash')
def _():
    W, H = 900, 330
    b = ''
    rows = [('"Pay 100 NIS"', '3f2a9c...e71b', BLUE), ('"Pay 900 NIS"', 'b81d04...2c9a', RED)]
    for i, (m, h, col) in enumerate(rows):
        y = 110 + i * 100
        b += box(40, y, 220, 54, SLATE, m, 15, fill='#FFFFFF', mono=True)
        b += arrow(262, y + 27, 340, y + 27, 'ink', 2.5)
        b += box(342, y, 160, 54, PURPLE, 'SHA-256', 16)
        b += arrow(504, y + 27, 582, y + 27, 'ink', 2.5)
        b += box(584, y, 260, 54, col, h, 15, mono=True)
    b += text(450, 290, 'One small change -> completely different digest.  One-way: you cannot get the message back.', 13.5, weight='700')
    return svg(W, H, b, 'Hashing protects INTEGRITY')


@fig('s8_vpn_tunnel')
def _():
    W, H = 900, 440
    b = box(30, 80, 190, 170, BLUE, None, dash=True, fill='#F8FBFF') + text(125, 100, 'Site A  10.1.0.0/16', 13, weight='700', fill=BLUE[0])
    b += pc(90, 170, None) + router(180, 170, None)
    b += box(680, 80, 190, 170, BLUE, None, dash=True, fill='#F8FBFF') + text(775, 100, 'Site B  10.2.0.0/16', 13, weight='700', fill=BLUE[0])
    b += router(720, 170, None) + server(815, 170, None)
    b += cloud(450, 165, None, 1.25)
    b += text(450, 228, 'Internet (untrusted)', 13, weight='700', fill=MUTED)
    b += f'<rect x="215" y="152" width="470" height="34" rx="17" fill="{GREEN[1]}" stroke="{GREEN[0]}" stroke-width="3"/>'
    b += lock(450, 166, GREEN, 0.9)
    b += text(330, 169, 'IPsec tunnel', 13, weight='700', fill=GREEN[0]) + text(575, 169, 'ESP encrypted', 13, weight='700', fill=GREEN[0])
    b += text(450, 290, 'ESP tunnel mode - what travels on the Internet:', 14, weight='700')
    parts = [('New IP hdr', 130, AMBER, 'public IPs'), ('ESP hdr', 90, GREEN, ''), ('Original IP hdr', 150, BLUE, '10.1.x -> 10.2.x'),
             ('TCP + Data', 170, BLUE, ''), ('ESP trailer', 100, GREEN, ''), ('ESP auth', 90, GREEN, '')]
    x = 40
    for lab, w, col, sub in parts:
        b += box(x, 310, w - 4, 46, col, lab, 13); x += w
    b += path('M176,368 L176,380 L646,380 L646,368', stroke=GREEN[0], sw=2.5)
    b += text(411, 398, 'encrypted (confidentiality)', 13, weight='700', fill=GREEN[0])
    b += path('M130,368 L130,412 L736,412 L736,368', stroke=PURPLE[0], sw=2, dash=True)
    b += text(433, 425, 'authenticated (integrity + origin)', 12.5, weight='700', fill=PURPLE[0])
    return svg(W, H, b, 'Site-to-site VPN: a private tunnel over a public network')


@fig('s9_risk_matrix')
def _():
    W, H = 900, 470
    b = ''
    lv = ['Low', 'Medium', 'High']
    colors = [[GREEN, GREEN, AMBER], [GREEN, AMBER, RED], [AMBER, RED, RED]]
    names = [['Accept', 'Accept', 'Mitigate'], ['Accept', 'Mitigate', 'Mitigate / Transfer'], ['Mitigate', 'Transfer / Mitigate', 'AVOID']]
    x0, y0, cw, ch = 220, 90, 170, 95
    for r in range(3):          # likelihood: top = high
        for c in range(3):      # impact
            L = 2 - r
            col = colors[L][c]
            b += box(x0 + c * cw, y0 + r * ch, cw - 6, ch - 6, col, None)
            b += text(x0 + c * cw + cw / 2 - 3, y0 + r * ch + 36, ['LOW', 'MEDIUM', 'HIGH', 'HIGH', 'CRITICAL'][L + c], 15, weight='700', fill=col[0])
            b += text(x0 + c * cw + cw / 2 - 3, y0 + r * ch + 62, names[L][c], 12, fill=INK)
        b += text(x0 - 15, y0 + r * ch + ch / 2, lv[2 - r], 14, 'end', '700')
    for c in range(3):
        b += text(x0 + c * cw + cw / 2, y0 + 3 * ch + 18, lv[c], 14, weight='700')
    b += text(x0 + 1.5 * cw, y0 + 3 * ch + 48, 'IMPACT (damage)  ->', 15, weight='700', fill=MUTED)
    b += f'<text x="70" y="{y0+1.5*ch}" font-size="15" font-weight="700" fill="{MUTED}" text-anchor="middle" transform="rotate(-90 70 {y0+1.5*ch})">LIKELIHOOD  -></text>'
    b += box(740, 100, 135, 250, SLATE, None, fill='#F8FAFC')
    for i, (t, d) in enumerate([('Mitigate', 'add controls'), ('Transfer', 'insurance'), ('Avoid', 'stop activity'), ('Accept', 'live with it')]):
        b += text(807, 128 + i * 58, t, 14, weight='700') + text(807, 148 + i * 58, d, 12, fill=MUTED)
    return svg(W, H, b, 'Risk matrix: Risk = Likelihood x Impact')


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(os.sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        with open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(fn())
        print('wrote', name)


if __name__ == '__main__':
    main()
