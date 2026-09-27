#!/usr/bin/env python3
"""Minimal, dependency-free .pptx generator (raw OOXML via zipfile).
Builds a 16:9 deck from a list of slides. Each slide = title + bullets.
Bullets support a leading level via "-> " (sub-bullet) prefix.
"""
import zipfile
from xml.sax.saxutils import escape

EMU = 914400  # per inch
SW, SH = int(13.333 * EMU), int(7.5 * EMU)  # 16:9

# ---- colors ----
GREEN = "1B7A3D"
DARK = "10391F"
GREY = "3C3C3C"
LIGHT = "F2F7F3"
ACCENT = "E0A800"

def _run(text, sz, color, bold=False, italic=False):
    b = ' b="1"' if bold else ''
    it = ' i="1"' if italic else ''
    return (f'<a:r><a:rPr lang="en-US" sz="{sz}"{b}{it} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="Calibri"/></a:rPr>'
            f'<a:t>{escape(text)}</a:t></a:r>')

def _para(runs_xml, align="l", bullet=True, level=0, space_before=600):
    buch = ('<a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>'
            if bullet else '<a:buNone/>')
    return (f'<a:p><a:pPr lvl="{level}" algn="{align}" marL="{level*300000}">'
            f'<a:spcBef><a:spcPts val="{space_before}"/></a:spcBef>'
            f'{buch}</a:pPr>{runs_xml}</a:p>')


def _textbox(x, y, w, h, paras_xml, sp_id, name, anchor="t"):
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}"/>
<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
<p:txBody><a:bodyPr wrap="square" anchor="{anchor}"><a:normAutofit/></a:bodyPr>
<a:lstStyle/>{paras_xml}</p:txBody></p:sp>'''

def _rect(x, y, w, h, color, sp_id, name):
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}"/>
<p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln>
</p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr/></a:p></p:txBody></p:sp>'''

def build_slide_xml(slide, idx, total):
    shapes = []
    sid = 2
    kind = slide.get("kind", "content")
    if kind == "title":
        shapes.append(_rect(0, 0, SW, SH, DARK, sid, "bg")); sid += 1
        shapes.append(_rect(0, int(4.9*EMU), SW, int(0.06*EMU), ACCENT, sid, "line")); sid += 1
        t = _para(_run(slide["title"], 4000, "FFFFFF", bold=True), bullet=False, space_before=0)
        shapes.append(_textbox(int(0.9*EMU), int(2.3*EMU), int(11.5*EMU), int(2.4*EMU), t, sid, "title", "b")); sid += 1
        subs = "".join(_para(_run(s, 1800, "CFE3D6"), bullet=False, space_before=300) for s in slide["bullets"])
        shapes.append(_textbox(int(0.95*EMU), int(5.15*EMU), int(11.5*EMU), int(2.0*EMU), subs, sid, "sub", "t")); sid += 1
    elif kind == "section":
        shapes.append(_rect(0, 0, SW, SH, GREEN, sid, "bg")); sid += 1
        t = _para(_run(slide["title"], 3600, "FFFFFF", bold=True), align="l", bullet=False, space_before=0)
        shapes.append(_textbox(int(0.9*EMU), int(3.0*EMU), int(11.5*EMU), int(1.6*EMU), t, sid, "title", "ctr")); sid += 1
        if slide.get("bullets"):
            subs = "".join(_para(_run(s, 1800, "E8F3EC"), bullet=False, space_before=200) for s in slide["bullets"])
            shapes.append(_textbox(int(0.95*EMU), int(4.6*EMU), int(11.5*EMU), int(1.8*EMU), subs, sid, "sub")); sid += 1
    else:
        # header band
        shapes.append(_rect(0, 0, SW, int(1.15*EMU), GREEN, sid, "band")); sid += 1
        t = _para(_run(slide["title"], 2400, "FFFFFF", bold=True), bullet=False, space_before=0)
        shapes.append(_textbox(int(0.5*EMU), int(0.18*EMU), int(12.3*EMU), int(0.9*EMU), t, sid, "title", "ctr")); sid += 1
        # body
        paras = []
        for b in slide["bullets"]:
            lvl = 0; txt = b
            if isinstance(b, tuple):
                lvl, txt = b
            if txt.startswith("-> "):
                lvl, txt = 1, txt[3:]
            bold = txt.endswith(" ::")
            if bold: txt = txt[:-3]
            col = DARK if bold else GREY
            sz = 1500 if lvl == 0 else 1300
            paras.append(_para(_run(txt, sz, col, bold=bold), level=lvl,
                               space_before=500 if lvl == 0 else 200))
        body = "".join(paras)
        shapes.append(_textbox(int(0.6*EMU), int(1.45*EMU), int(12.1*EMU), int(5.6*EMU), body, sid, "body")); sid += 1
    # footer
    foot = _para(_run(f"SIH 2026  |  PS 26180  |  Smart Farming Assistant", 900, "9AA0A6"), bullet=False, space_before=0)
    shapes.append(_textbox(int(0.5*EMU), int(7.05*EMU), int(9*EMU), int(0.4*EMU), foot, sid, "foot")); sid += 1
    pg = _para(_run(f"{idx}/{total}", 900, "9AA0A6", ), align="r", bullet=False, space_before=0)
    shapes.append(_textbox(int(11.8*EMU), int(7.05*EMU), int(1.2*EMU), int(0.4*EMU), pg, sid, "pg")); sid += 1
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{"".join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sld>'''


CT = lambda n: f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'

def content_types(n):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
    '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
    '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
    '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
    + "".join(CT(i) for i in range(1, n+1)) + '</Types>')

ROOT_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '</Relationships>')

def presentation_xml(n):
    sids = "".join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(n))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1">'
    '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
    f'<p:sldIdLst>{sids}</p:sldIdLst>'
    f'<p:sldSz cx="{SW}" cy="{SH}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/>'
    '</p:presentation>')

def presentation_rels(n):
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(n):
        rels.append(f'<Relationship Id="rId{i+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')
    rels.append(f'<Relationship Id="rId{n+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    rels.append(f'<Relationship Id="rId{n+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + '</Relationships>')

PRESPROPS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')


def theme_xml():
    def scheme():
        cols = [("dk1","000000"),("lt1","FFFFFF"),("dk2",DARK),("lt2",LIGHT),
                ("accent1",GREEN),("accent2",ACCENT),("accent3","4C9A2A"),
                ("accent4","2E7D32"),("accent5","8BC34A"),("accent6","C0CA33"),
                ("hlink","0563C1"),("folHlink","954F72")]
        out=[]
        for name,val in cols:
            if name in ("dk1","lt1"):
                sysv = "windowText" if name=="dk1" else "window"
                out.append(f'<a:{name}><a:sysClr val="{sysv}" lastClr="{val}"/></a:{name}>')
            else:
                out.append(f'<a:{name}><a:srgbClr val="{val}"/></a:{name}>')
        return "".join(out)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Kisan">'
    '<a:themeElements><a:clrScheme name="Kisan">'+scheme()+'</a:clrScheme>'
    '<a:fontScheme name="Kisan"><a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
    '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
    '<a:fmtScheme name="Kisan">'
    '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
    '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
    '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
    '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
    '</a:fmtScheme></a:themeElements></a:theme>')

MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
    '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '</p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')

MASTER_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
    '</Relationships>')

LAYOUT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">'
    '<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sldLayout>')

LAYOUT_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
    '</Relationships>')

def slide_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    '</Relationships>')

def build(slides, path):
    n = len(slides)
    z = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED)
    z.writestr("[Content_Types].xml", content_types(n))
    z.writestr("_rels/.rels", ROOT_RELS)
    z.writestr("ppt/presentation.xml", presentation_xml(n))
    z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(n))
    z.writestr("ppt/presProps.xml", PRESPROPS)
    z.writestr("ppt/theme/theme1.xml", theme_xml())
    z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
    z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", MASTER_RELS)
    z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
    z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", LAYOUT_RELS)
    for i, s in enumerate(slides, 1):
        z.writestr(f"ppt/slides/slide{i}.xml", build_slide_xml(s, i, n))
        z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())
    z.close()
    print(f"wrote {path} ({n} slides)")
