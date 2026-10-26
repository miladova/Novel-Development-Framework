#!/usr/bin/env python3
"""Build THE PRICE OF A NAME (Rome AD 112) into a typeset PDF.

Usage:
    python3 build_pdf.py            # build the PDF
    python3 build_pdf.py --check    # word counts only

Manuscript source: 05_Books/Rome_AD_112/Chapters/*.md
Output:            08_Publication/The_Price_of_a_Name.pdf
"""

import argparse
import glob
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(BOOK))
CHAPTERS = os.path.join(BOOK, "Chapters")
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(REPO, "08_Publication", "The_Price_of_a_Name.pdf")

PAGE_W, PAGE_H = 6 * inch, 9 * inch
INK = colors.HexColor("#1a1a1a")
FADE = colors.HexColor("#5b5348")
ACCENT = colors.HexColor("#6d1f1f")

TITLE = "THE PRICE OF A NAME"
SUBTITLE = "A Novel of Rome"
SETTING = "Rome, AD 112"
TAGLINE = "Power is inherited, fortunes are made, and some wounds never heal."


# ---------------------------------------------------------------- fonts
def register_fonts():
    pdfmetrics.registerFont(TTFont("Garamond", os.path.join(FONTS, "EBGaramond-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Garamond-Italic", os.path.join(FONTS, "EBGaramond-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Garamond-Bold", os.path.join(FONTS, "EBGaramond-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Garamond-BoldItalic", os.path.join(FONTS, "EBGaramond-BoldItalic.ttf")))
    pdfmetrics.registerFont(TTFont("Garamond-SemiBold", os.path.join(FONTS, "EBGaramond-SemiBold.ttf")))
    pdfmetrics.registerFontFamily("Garamond", normal="Garamond", bold="Garamond-Bold",
                                  italic="Garamond-Italic", boldItalic="Garamond-BoldItalic")


# ---------------------------------------------------------------- flowables
def tracked_text(c, x, y, text, font, size, tracking, color):
    """Draw text with manual letter-spacing using a text object."""
    c.saveState()
    c.setFillColor(color)
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


class Tracked(Flowable):
    """Letter-spaced (tracked) line of text, drawn directly."""

    def __init__(self, text, size=9, tracking=2.4, font="Garamond-SemiBold",
                 color=INK, align="center", width=None, space_before=0, space_after=0):
        Flowable.__init__(self)
        self.text, self.size, self.tracking = text, size, tracking
        self.font, self.color, self.align = font, color, align
        self._w = width
        self.sb, self.sa = space_before, space_after

    def wrap(self, availWidth, availHeight):
        self.avail = availWidth
        w = pdfmetrics.stringWidth(self.text, self.font, self.size)
        self.tw = w + self.tracking * max(0, len(self.text) - 1)
        self.height = self.size * 1.25 + self.sb + self.sa
        return availWidth, self.height

    def draw(self):
        x = 0 if self.align == "left" else (self.avail - self.tw) / 2.0
        tracked_text(self.canv, x, self.sa, self.text, self.font, self.size,
                     self.tracking, self.color)


class Rule(Flowable):
    """A short hairline rule, optionally centred, with an optional diamond."""

    def __init__(self, width=48, thickness=0.6, color=FADE, space_before=6,
                 space_after=6, ornament=False):
        Flowable.__init__(self)
        self.w, self.t, self.color = width, thickness, color
        self.sb, self.sa, self.ornament = space_before, space_after, ornament

    def wrap(self, availWidth, availHeight):
        self.avail = availWidth
        self.height = self.sb + self.sa + (7 if self.ornament else 0)
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(self.color)
        c.setLineWidth(self.t)
        mid = self.sb + (3 if self.ornament else 0)
        x0 = (self.avail - self.w) / 2.0
        if self.ornament:
            gap = 9
            half = (self.w - gap * 2) / 2.0
            c.line(x0, mid, x0 + half, mid)
            c.line(x0 + self.w - half, mid, x0 + self.w, mid)
            cx = self.avail / 2.0
            c.setFillColor(self.color)
            p = c.beginPath()
            p.moveTo(cx, mid - 2.2)
            p.lineTo(cx + 2.2, mid)
            p.lineTo(cx, mid + 2.2)
            p.lineTo(cx - 2.2, mid)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        else:
            c.line(x0, mid, x0 + self.w, mid)
        c.restoreState()


# ---------------------------------------------------------------- styles
def make_styles():
    s = {}
    s["body"] = ParagraphStyle("body", fontName="Garamond", fontSize=10.9, leading=15.6,
                               alignment=TA_JUSTIFY, firstLineIndent=15, spaceBefore=0,
                               spaceAfter=0, textColor=INK, hyphenationLang="en_GB",
                               embeddedHyphenation=1, uriWasteReduce=0.3)
    s["body_first"] = ParagraphStyle("body_first", parent=s["body"], firstLineIndent=0)
    s["body_open"] = ParagraphStyle("body_open", parent=s["body"], firstLineIndent=0)
    s["quote"] = ParagraphStyle("quote", parent=s["body"], leftIndent=22, rightIndent=22,
                                firstLineIndent=0, fontSize=10.2, leading=14.6,
                                spaceBefore=6, spaceAfter=6, alignment=TA_JUSTIFY)
    s["letter"] = ParagraphStyle("letter", parent=s["body"], leftIndent=26, rightIndent=14,
                                 firstLineIndent=0, fontSize=10.2, leading=14.4,
                                 spaceBefore=8, spaceAfter=8)
    s["chap_title"] = ParagraphStyle("chap_title", fontName="Garamond-Italic", fontSize=17,
                                     leading=21, alignment=TA_CENTER, textColor=INK,
                                     spaceBefore=2, spaceAfter=2)
    s["part"] = ParagraphStyle("part", fontName="Garamond-SemiBold", fontSize=15,
                               leading=20, alignment=TA_CENTER, textColor=INK)
    s["title"] = ParagraphStyle("title", fontName="Garamond-SemiBold", fontSize=27,
                                leading=32, alignment=TA_CENTER, textColor=INK)
    s["sub"] = ParagraphStyle("sub", fontName="Garamond-Italic", fontSize=12.5,
                              leading=18, alignment=TA_CENTER, textColor=FADE)
    s["epi"] = ParagraphStyle("epi", fontName="Garamond-Italic", fontSize=11.5, leading=18,
                              alignment=TA_CENTER, textColor=INK)
    s["front"] = ParagraphStyle("front", fontName="Garamond", fontSize=9.2, leading=13.5,
                                alignment=TA_CENTER, textColor=FADE)
    s["toc1"] = ParagraphStyle("toc1", fontName="Garamond", fontSize=10.4, leading=17,
                               textColor=INK)
    s["toc2"] = ParagraphStyle("toc2", parent=s["toc1"], leftIndent=14, fontSize=10.0,
                               textColor=FADE)
    return s


# ---------------------------------------------------------------- parsing
SCENE = re.compile(r"^\s*(\*\s*\*\s*\*|﹡\s*﹡\s*﹡|-{3,}|_{3,}|\u2014\s*\u2014\s*\u2014)\s*$")


def inline(text):
    """Convert a restricted markdown subset to reportlab markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = text.replace("--", "—")
    # smart quotes and apostrophes
    text = re.sub(r"(?<![A-Za-z])'(?=[A-Za-z0-9])", "\u2018", text)
    text = text.replace("'", "\u2019")
    return text


PARTS = {
    1: ("PART ONE", "THE HOUSE"),
    5: ("PART TWO", "THE PRICE OF A NAME"),
    10: ("PART THREE", "WHAT THE STREETS KNOW"),
    15: ("PART FOUR", "THE JUDGEMENT OF THE CITY"),
    20: ("PART FIVE", "THE RECKONING"),
}

ROMAN = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
         "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN",
         "SEVENTEEN", "EIGHTEEN", "NINETEEN", "TWENTY", "TWENTY-ONE", "TWENTY-TWO",
         "TWENTY-THREE", "TWENTY-FOUR", "TWENTY-FIVE"]


def load_chapters():
    files = sorted(glob.glob(os.path.join(CHAPTERS, "*.md")))
    out = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        lines = raw.split("\n")
        head = None
        body = []
        for line in lines:
            if head is None and line.startswith("# "):
                head = line[2:].strip()
                continue
            body.append(line)
        title = head or os.path.basename(path)
        number, label = None, title
        m = re.match(r"^(\d+)\s*[|:—-]\s*(.+)$", title)
        if m:
            number, label = int(m.group(1)), m.group(2).strip()
        else:
            m = re.match(r"^(Epilogue|Prologue)\s*[|:—-]?\s*(.*)$", title, re.I)
            if m:
                number, label = m.group(1).title(), (m.group(2).strip() or m.group(1).title())
        out.append(dict(path=path, number=number, label=label, body="\n".join(body)))
    return out


def paragraphs(block):
    """Split a chapter body into ('scene', None) / ('p', text) items."""
    items, buf = [], []
    for line in block.split("\n"):
        if SCENE.match(line) or line.strip() == "":
            if buf:
                items.append(("p", " ".join(x.strip() for x in buf)))
                buf = []
            if SCENE.match(line):
                items.append(("scene", None))
        elif line.startswith(">"):
            if buf:
                items.append(("p", " ".join(x.strip() for x in buf)))
                buf = []
            items.append(("quote", line.lstrip("> ").strip()))
        else:
            buf.append(line)
    if buf:
        items.append(("p", " ".join(x.strip() for x in buf)))
    cleaned, prev_scene = [], False
    for kind, text in items:
        if kind == "scene":
            if prev_scene:
                continue
            prev_scene = True
            cleaned.append((kind, text))
        else:
            prev_scene = False
            cleaned.append((kind, text))
    return cleaned


# ---------------------------------------------------------------- document
class Book(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=(PAGE_W, PAGE_H),
                                 leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                                 topMargin=0.86 * inch, bottomMargin=0.9 * inch,
                                 title=TITLE, author="", subject=SUBTITLE,
                                 creator="NDF build_pdf.py", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="plain", frames=[frame], onPage=self._plain),
            PageTemplate(id="body", frames=[frame], onPage=self._start,
                         onPageEnd=self._running),
        ])
        self.running_head = ""
        self.opener_pages = set()

    # page furniture -------------------------------------------------
    def _folio(self, c, y=0.55 * inch):
        c.setFont("Garamond", 9.5)
        c.setFillColor(FADE)
        c.drawCentredString(PAGE_W / 2.0, y, str(self.page))

    def _plain(self, c, doc):
        pass

    def _start(self, c, doc):
        pass

    def _running(self, c, doc):
        if self.page in self.opener_pages:
            self._folio(c, y=0.5 * inch)
            return
        head = TITLE if self.page % 2 == 0 else self.running_head.upper()[:64]
        size, track = 8.2, 1.6
        w = pdfmetrics.stringWidth(head, "Garamond", size) + track * max(0, len(head) - 1)
        tracked_text(c, PAGE_W / 2.0 - w / 2.0, PAGE_H - 0.58 * inch, head,
                     "Garamond", size, track, FADE)
        self._folio(c)

    # toc hooks ------------------------------------------------------
    def afterFlowable(self, flowable):
        if getattr(flowable, "_chapter_opener", False):
            self.opener_pages.add(self.page)
            self.running_head = getattr(flowable, "_head_label", self.running_head)
        if getattr(flowable, "_toc_entry", None):
            level, text = flowable._toc_entry
            key = "ch%d" % id(flowable)
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (level, text, self.page, key))
            self.canv.addOutlineEntry(re.sub(r"<[^>]+>", "", text), key, level=level,
                                      closed=level > 0)


class Heading(Paragraph):
    """Paragraph that also registers a table-of-contents entry."""

    def __init__(self, text, style, level=0, toc_text=None, **kw):
        Paragraph.__init__(self, text, style, **kw)
        self._toc_entry = (level, toc_text if toc_text is not None else text)


# ---------------------------------------------------------------- assembly
def front_matter(st):
    story = []
    story.append(NextPageTemplate("plain"))
    story.append(Spacer(1, 1.55 * inch))
    story.append(Tracked(TITLE, size=20, tracking=5.4, font="Garamond-SemiBold"))
    story.append(Spacer(1, 12))
    story.append(Rule(width=54, color=ACCENT, space_before=4, space_after=10, ornament=True))
    story.append(Paragraph(SUBTITLE, st["sub"]))
    story.append(Spacer(1, 2.3 * inch))
    story.append(Paragraph(SETTING, st["sub"]))
    story.append(PageBreak())

    # copyright / colophon
    story.append(Spacer(1, 4.6 * inch))
    story.append(Paragraph(
        "This is a work of fiction. Its people, houses and quarrels are invented; "
        "the city that contains them is not.", st["front"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Mature content: adult themes, including sexual "
                           "exploitation, slavery and violence. 18+.", st["front"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Set in EB Garamond.", st["front"]))
    story.append(PageBreak())

    # epigraph
    story.append(Spacer(1, 2.1 * inch))
    story.append(Paragraph("\u201c%s\u201d" % TAGLINE, st["epi"]))
    story.append(Spacer(1, 16))
    story.append(Rule(width=36, space_before=2, space_after=2))
    story.append(PageBreak())

    # contents
    story.append(Spacer(1, 0.35 * inch))
    story.append(Tracked("CONTENTS", size=11, tracking=3.6, color=INK))
    story.append(Spacer(1, 18))
    toc = TableOfContents()
    toc.levelStyles = [st["toc1"], st["toc2"]]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    return story


def part_flowables(num, st):
    kicker, name = PARTS[num]
    story = [Spacer(1, 2.6 * inch),
             Tracked(kicker, size=10, tracking=4.2, color=ACCENT, space_after=16),
             Heading(name.title(), st["part"], level=0, toc_text="<b>%s</b> &nbsp;%s" % (kicker.title(), name.title())),
             Rule(width=44, space_before=26, space_after=4, ornament=True)]
    return story


def chapter_flowables(ch, st, first=False):
    story = []
    label = ch["label"]
    num = ch["number"]
    if isinstance(num, int) and 1 <= num <= len(ROMAN):
        kicker = "CHAPTER " + ROMAN[num]
    elif isinstance(num, str):
        kicker = num.upper()
    else:
        kicker = ""
    head_markup = label
    if kicker:
        story.append(Tracked(kicker, size=9.2, tracking=3.2, color=ACCENT,
                             space_before=0, space_after=10))
    h = Heading('<i>%s</i>' % inline(head_markup), st["chap_title"], level=0,
                toc_text="%s&nbsp;&nbsp;&nbsp;%s" % (kicker.title() if kicker else "", inline(head_markup)))
    h._chapter_opener = True
    h._head_label = label
    story.append(h)
    story.append(Rule(width=40, space_before=14, space_after=20, ornament=True))

    items = paragraphs(ch["body"])
    first_para = True
    for kind, text in items:
        if kind == "scene":
            story.append(Rule(width=26, space_before=13, space_after=13))
        elif kind == "quote":
            story.append(Paragraph(inline(text), st["quote"]))
            first_para = True
        else:
            style = st["body_first"] if first_para else st["body"]
            story.append(Paragraph(inline(text), style))
            first_para = False
    return story


def build(check_only=False):
    chapters = load_chapters()
    if check_only:
        total = 0
        for ch in chapters:
            words = len(re.findall(r"\b[\w’'-]+\b", ch["body"]))
            total += words
            print("%-42s %6d" % (os.path.basename(ch["path"]), words))
        print("%-42s %6d" % ("TOTAL", total))
        return

    register_fonts()
    st = make_styles()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = Book(OUT)
    story = front_matter(st)
    for i, ch in enumerate(chapters):
        if i:
            story.append(PageBreak())
        if isinstance(ch["number"], int) and ch["number"] in PARTS:
            story += part_flowables(ch["number"], st)
            story.append(PageBreak())
        story += chapter_flowables(ch, st, first=(i == 0))
    doc.multiBuild(story)
    print("wrote", OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    build(check_only=args.check)
