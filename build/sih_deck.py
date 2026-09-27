#!/usr/bin/env python3
"""SIH 2026 idea-submission deck generator (raw OOXML, stdlib only).

Reproduces the official SIH template chrome — 12192000x6858000 canvas, blue
footer bar, SIH 2026 logo top-right, Times New Roman bold title, slide number,
"@SIH Idea submission- Template" footer, team-name oval — and adds card /
diagram / chart primitives for dense, readable content slides.
"""
import zipfile, os
from xml.sax.saxutils import escape

EMU = 914400
SW, SH = 12192000, 6858000          # exactly matches basic.pptx
def IN(v): return int(round(v * EMU))

# ---------------------------------------------------------------- palette ----
INK    = "12332A"   # body text
TITLE  = "0B2E20"   # slide titles
GREEN  = "1B7A3D"
GREEN2 = "2E9E57"
BLUE   = "0070C0"   # template accent — keep
NAVY   = "1F4E79"
AMBER  = "C98A00"
RED    = "C0392B"
GREY   = "5A6B63"
WHITE  = "FFFFFF"
# card tints
T_GREEN = "EAF5EE"
T_BLUE  = "E7F1FB"
T_AMBER = "FDF4DE"
T_RED   = "FBEBE8"
T_GREY  = "F1F4F2"

BODY_FONT = "Calibri"
HEAD_FONT = "Times New Roman"


def esc(t): return escape(str(t))


def _r(text, sz=1100, color=INK, b=False, i=False, font=BODY_FONT, u=False):
    bb = ' b="1"' if b else ''
    ii = ' i="1"' if i else ''
    uu = ' u="sng"' if u else ''
    return (f'<a:r><a:rPr lang="en-US" sz="{sz}"{bb}{ii}{uu} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/></a:rPr>'
            f'<a:t>{esc(text)}</a:t></a:r>')


def _p(runs, align="l", bullet=None, lvl=0, before=300, after=0, lnspc=None,
       marL=None, indent=None):
    """bullet: None | '•' | '▸' | '–' | 'num'"""
    if bullet is None:
        bu = '<a:buNone/>'
    else:
        bu = (f'<a:buFont typeface="Arial"/>'
              f'<a:buChar char="{esc(bullet)}"/>')
    if marL is None:
        marL = 0 if bullet is None else 152400 + lvl * 152400
    if indent is None:
        indent = 0 if bullet is None else -152400
    ls = f'<a:lnSpc><a:spcPct val="{lnspc}"/></a:lnSpc>' if lnspc else ''
    return (f'<a:p><a:pPr lvl="0" algn="{align}" marL="{marL}" indent="{indent}">'
            f'{ls}<a:spcBef><a:spcPts val="{before}"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{after}"/></a:spcAft>{bu}</a:pPr>'
            f'{runs}</a:p>')


# ------------------------------------------------------------- primitives ----
_ID = [1]
def nid():
    _ID[0] += 1
    return _ID[0]


def shape(x, y, w, h, paras="", prst="rect", fill=None, line=None, lnw=12700,
          anchor="t", ins=(0.10, 0.06, 0.10, 0.06), name=None, adj=None,
          shadow=False, rot=None):
    """Generic autoshape with optional text. ins = (l,t,r,b) inches."""
    i = nid()
    nm = name or f"sh{i}"
    f = (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
         if fill else '<a:noFill/>')
    l = (f'<a:ln w="{lnw}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
         if line else '<a:ln><a:noFill/></a:ln>')
    sh = ('<a:effectLst><a:outerShdw blurRad="50800" dist="25400" dir="5400000" '
          'rotWithShape="0"><a:srgbClr val="9AA6A0"><a:alpha val="30000"/>'
          '</a:srgbClr></a:outerShdw></a:effectLst>') if shadow else ''
    av = (f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>'
          if adj is not None else '<a:avLst/>')
    rt = f' rot="{rot}"' if rot else ''
    li, ti, ri, bi = [IN(v) for v in ins]
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nm}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm{rt}><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>
<a:prstGeom prst="{prst}">{av}</a:prstGeom>{f}{l}{sh}</p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="{li}" tIns="{ti}" rIns="{ri}" bIns="{bi}" anchor="{anchor}">
<a:normAutofit/></a:bodyPr><a:lstStyle/>{paras or '<a:p><a:endParaRPr/></a:p>'}</p:txBody></p:sp>'''


def tb(x, y, w, h, paras, anchor="t", ins=(0.04, 0.02, 0.04, 0.02), name=None):
    return shape(x, y, w, h, paras, prst="rect", fill=None, line=None,
                 anchor=anchor, ins=ins, name=name)


def pic(x, y, w, h, rid, name="logo"):
    i = nid()
    return f'''<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{name}"/>
<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'''


# ------------------------------------------------------------------ cards ----
def _item_paras(items, bsz, accent, lead_color=None, tight=False):
    """Item syntax:
       'Label :: rest'  -> bold coloured lead-in, then normal text
       '#Heading'       -> inline sub-heading (bold, no bullet)
       '>text'          -> sub-bullet
       '!text'          -> plain line, no bullet
    """
    lead_color = lead_color or accent
    out = []
    for it in items:
        lvl, bullet, sz = 0, "▪", bsz
        before = 110 if tight else 170
        if it.startswith("#"):
            it, bullet, before = it[1:], None, 210
            out.append(_p(_r(it, bsz + 50, accent, b=True), bullet=None,
                          before=before))
            continue
        if it.startswith("!"):
            it, bullet = it[1:], None
        elif it.startswith(">"):
            it, bullet, lvl, sz = it[1:], "–", 1, bsz - 50
        if " :: " in it:
            head, rest = it.split(" :: ", 1)
            runs = (_r(head + " ", sz, lead_color, b=True) +
                    _r(rest, sz, INK))
        else:
            runs = _r(it, sz, INK)
        out.append(_p(runs, bullet=bullet, lvl=lvl, before=before,
                      lnspc=92000 if tight else 96000))
    return "".join(out)


def card(x, y, w, h, heading, items, accent=GREEN, tint=T_GREEN, hsz=1250,
         bsz=1000, tight=False, icon=None):
    """Rounded card: tinted body, accent heading strip, bulleted items."""
    out = []
    out.append(shape(x, y, w, h, prst="roundRect", adj=6000, fill=tint,
                     line=accent, lnw=9525, shadow=True))
    hb = IN(0.40)
    out.append(shape(x, y, w, hb, prst="roundRect", adj=22000, fill=accent))
    out.append(shape(x, y + hb - IN(0.12), w, IN(0.14), fill=accent))
    ht = (icon + "  " if icon else "") + heading
    out.append(tb(x + IN(0.14), y + IN(0.02), w - IN(0.24), hb - IN(0.02),
                  _p(_r(ht, hsz, WHITE, b=True, font=BODY_FONT), bullet=None),
                  anchor="ctr"))
    out.append(tb(x + IN(0.13), y + hb + IN(0.05), w - IN(0.26),
                  h - hb - IN(0.12),
                  _item_paras(items, bsz, accent, tight=tight)))
    return "".join(out)


def pill(x, y, w, h, text, fill, color=WHITE, sz=950, b=True, prst="roundRect"):
    return shape(x, y, w, h, _p(_r(text, sz, color, b=b), align="ctr",
                                bullet=None), prst=prst, adj=25000, fill=fill,
                 anchor="ctr", ins=(0.04, 0.02, 0.04, 0.02))


# ------------------------------------------------------------- diagram kit ----
def flow(x, y, w, h, steps, fill=GREEN, sub_color=GREY, sz=900, ssz=750,
         gap=0.03):
    """Chevron pipeline. steps = [(label, sublabel), ...]"""
    out, n = [], len(steps)
    g = IN(gap)
    sw = (w - g * (n - 1)) / n
    for k, (lab, sub) in enumerate(steps):
        cx = x + k * (sw + g)
        prst = "homePlate" if k == 0 else "chevron"
        out.append(shape(cx, y, sw, h, prst=prst, adj=None, fill=fill,
                         ins=(0.16, 0.02, 0.10, 0.02)))
        paras = _p(_r(lab, sz, WHITE, b=True), align="ctr", bullet=None)
        if sub:
            paras += _p(_r(sub, ssz, "D8ECDF"), align="ctr", bullet=None,
                        before=30)
        out.append(tb(cx + IN(0.14), y, sw - IN(0.22), h, paras, anchor="ctr"))
    return "".join(out)


def bars(x, y, w, h, series, title=None, maxv=100, unit="%", bsz=850):
    """Vertical bar chart. series = [(label, value, colour), ...]"""
    out = []
    th = IN(0.30) if title else 0
    if title:
        out.append(tb(x, y, w, th, _p(_r(title, 950, TITLE, b=True),
                                      bullet=None)))
    lh = IN(0.42)                        # x-axis label band
    vh = IN(0.26)                        # value label above bar
    pt = y + th
    ph = h - th - lh                     # plot height
    n = len(series)
    slot = w / n
    bw = min(slot * 0.52, IN(1.15))
    # baseline + gridlines
    for f in (0.25, 0.5, 0.75, 1.0):
        gy = pt + ph - ph * f
        out.append(shape(x, gy, w, IN(0.008), fill="DCE4DF"))
    out.append(shape(x, pt + ph, w, IN(0.014), fill=GREY))
    for k, (lab, val, col) in enumerate(series):
        bh = max(IN(0.10), (ph - vh) * (val / float(maxv)))
        bx = x + k * slot + (slot - bw) / 2
        by = pt + ph - bh
        out.append(shape(bx, by, bw, bh, fill=col))
        out.append(tb(bx - IN(0.15), by - vh, bw + IN(0.30), vh,
                      _p(_r(f"{val:g}{unit}", 1000, col, b=True), align="ctr",
                         bullet=None), anchor="b"))
        out.append(tb(x + k * slot, pt + ph + IN(0.04), slot, lh,
                      _p(_r(lab, bsz, INK), align="ctr", bullet=None,
                         lnspc=90000)))
    return "".join(out)


def stat(x, y, w, h, big, label, accent=GREEN, tint=T_GREEN, bsz=2000,
         lsz=880):
    out = [shape(x, y, w, h, prst="roundRect", adj=9000, fill=tint,
                 line=accent, lnw=9525, shadow=True)]
    out.append(shape(x, y, IN(0.09), h, fill=accent))
    out.append(tb(x + IN(0.18), y + IN(0.06), w - IN(0.30), IN(0.52),
                  _p(_r(big, bsz, accent, b=True, font=HEAD_FONT),
                     align="ctr", bullet=None), anchor="ctr"))
    out.append(tb(x + IN(0.16), y + IN(0.56), w - IN(0.28), h - IN(0.60),
                  _p(_r(label, lsz, INK), align="ctr", bullet=None,
                     lnspc=90000), anchor="t"))
    return "".join(out)


def grid(x, y, w, rows, cols_w, hsz=880, bsz=850, rh=0.32, hdr_fill=NAVY,
         zebra="F4F8F5", accent_col=0, accent=GREEN):
    """Fake table: rows[0] is the header. cols_w = fractional widths."""
    out = []
    tot = float(sum(cols_w))
    ws = [w * c / tot for c in cols_w]
    hh = IN(rh + 0.06)
    out.append(shape(x, y, w, hh, fill=hdr_fill))
    cx = x
    for j, cell in enumerate(rows[0]):
        out.append(tb(cx + IN(0.08), y, ws[j] - IN(0.10), hh,
                      _p(_r(cell, hsz, WHITE, b=True), bullet=None),
                      anchor="ctr"))
        cx += ws[j]
    ry = y + hh
    for i, row in enumerate(rows[1:]):
        h = IN(rh)
        if i % 2 == 0:
            out.append(shape(x, ry, w, h, fill=zebra))
        out.append(shape(x, ry + h - IN(0.008), w, IN(0.008), fill="DCE4DF"))
        cx = x
        for j, cell in enumerate(row):
            hi = (j == accent_col)
            out.append(tb(cx + IN(0.08), ry, ws[j] - IN(0.10), h,
                          _p(_r(cell, bsz, accent if hi else INK, b=hi),
                             bullet=None), anchor="ctr"))
            cx += ws[j]
        ry += h
    return "".join(out), ry - y


# ----------------------------------------------------------------- chrome ----
FOOT_Y, FOOT_H = 6354762, 503238
TEAM = "Team Name"
LOGO_RID = "rId2"


def chrome(idx, total, title=None):
    out = []
    # blue footer bar (template)
    out.append(shape(0, FOOT_Y, SW, FOOT_H, fill=BLUE))
    out.append(tb(IN(0.35), FOOT_Y + IN(0.10), IN(6.0), IN(0.34),
                  _p(_r("@SIH Idea submission- Template", 900, "DCEBF7"),
                     bullet=None)))
    out.append(tb(SW - IN(1.1), FOOT_Y + IN(0.10), IN(0.7), IN(0.34),
                  _p(_r(str(idx), 1000, WHITE, b=True), align="r",
                     bullet=None)))
    # SIH 2026 logo, top-right
    out.append(pic(IN(11.02), IN(0.12), IN(1.98), IN(0.935), LOGO_RID))
    if title is not None:
        # team-name oval, top-left
        out.append(shape(IN(0.30), IN(0.20), IN(1.55), IN(0.58),
                         _p(_r(TEAM, 900, NAVY, b=True), align="ctr",
                            bullet=None), prst="ellipse", fill=WHITE,
                         line=NAVY, lnw=9525, anchor="ctr"))
        out.append(tb(IN(1.95), IN(0.14), IN(9.0), IN(0.72),
                      _p(_r(title, 2600, TITLE, b=True, font=HEAD_FONT),
                         align="ctr", bullet=None), anchor="ctr"))
        out.append(shape(IN(0.30), IN(0.94), IN(12.73), IN(0.045), fill=GREEN))
    return out


SLD_HEAD = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/>'
    '<p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/>'
    '<a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>'
    '</a:xfrm></p:grpSpPr>')
SLD_TAIL = ('</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/>'
            '</p:clrMapOvr></p:sld>')


def wrap(shapes):
    return SLD_HEAD + "".join(shapes) + SLD_TAIL


# ---------------------------------------------------------------- package ----
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
OD = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _ct(n):
    o = "".join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType='
                '"application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                for i in range(1, n + 1))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
        '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
        + o + '</Types>')


def _theme():
    cols = [("dk1", "000000"), ("lt1", "FFFFFF"), ("dk2", TITLE), ("lt2", T_GREY),
            ("accent1", GREEN), ("accent2", BLUE), ("accent3", AMBER),
            ("accent4", GREEN2), ("accent5", NAVY), ("accent6", RED),
            ("hlink", "0563C1"), ("folHlink", "954F72")]
    sc = "".join(
        (f'<a:{k}><a:sysClr val="{"windowText" if k=="dk1" else "window"}" '
         f'lastClr="{v}"/></a:{k}>') if k in ("dk1", "lt1")
        else f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in cols)
    fs = ('<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
          '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
          '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
          '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="KisanEdge">'
        f'<a:themeElements><a:clrScheme name="KisanEdge">{sc}</a:clrScheme>'
        '<a:fontScheme name="KisanEdge">'
        f'<a:majorFont><a:latin typeface="{HEAD_FONT}"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
        f'<a:minorFont><a:latin typeface="{BODY_FONT}"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
        '</a:fontScheme>'
        f'<a:fmtScheme name="KisanEdge">{fs}</a:fmtScheme>'
        '</a:themeElements></a:theme>')


_MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
    '<a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
    '<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/>'
    '<a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>'
    '</p:grpSpPr></p:spTree></p:cSld>'
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1"'
    ' accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5"'
    ' accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
    '</p:sldMaster>')

_LAYOUT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    ' type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr>'
    '<p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr>'
    '<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
    '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>'
    '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def write_pptx(slides, path, media):
    """slides: list of slide XML strings. media: {filename: bytes}."""
    n = len(slides)
    z = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED)
    z.writestr("[Content_Types].xml", _ct(n))
    z.writestr("_rels/.rels",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{PKG}"><Relationship Id="rId1" Type="{OD}/officeDocument"'
        ' Target="ppt/presentation.xml"/></Relationships>')
    sids = "".join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(n))
    z.writestr("ppt/presentation.xml",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{sids}</p:sldIdLst>'
        f'<p:sldSz cx="{SW}" cy="{SH}"/><p:notesSz cx="6858000" cy="9144000"/>'
        '</p:presentation>')
    rels = [f'<Relationship Id="rId1" Type="{OD}/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(n):
        rels.append(f'<Relationship Id="rId{i+2}" Type="{OD}/slide" Target="slides/slide{i+1}.xml"/>')
    rels.append(f'<Relationship Id="rId{n+2}" Type="{OD}/theme" Target="theme/theme1.xml"/>')
    rels.append(f'<Relationship Id="rId{n+3}" Type="{OD}/presProps" Target="presProps.xml"/>')
    z.writestr("ppt/_rels/presentation.xml.rels",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{PKG}">' + "".join(rels) + '</Relationships>')
    z.writestr("ppt/presProps.xml",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
    z.writestr("ppt/theme/theme1.xml", _theme())
    z.writestr("ppt/slideMasters/slideMaster1.xml", _MASTER)
    z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{PKG}">'
        f'<Relationship Id="rId1" Type="{OD}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        f'<Relationship Id="rId2" Type="{OD}/theme" Target="../theme/theme1.xml"/>'
        '</Relationships>')
    z.writestr("ppt/slideLayouts/slideLayout1.xml", _LAYOUT)
    z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{PKG}">'
        f'<Relationship Id="rId1" Type="{OD}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
        '</Relationships>')
    for fn, data in media.items():
        z.writestr(f"ppt/media/{fn}", data)
    for i, xml in enumerate(slides, 1):
        z.writestr(f"ppt/slides/slide{i}.xml", xml)
        z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{PKG}">'
            f'<Relationship Id="rId1" Type="{OD}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            f'<Relationship Id="rId2" Type="{OD}/image" Target="../media/sihlogo.png"/>'
            '</Relationships>')
    z.close()
    print(f"wrote {path} ({n} slides)")
