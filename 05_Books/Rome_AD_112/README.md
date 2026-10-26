# THE PRICE OF A NAME

*A Novel of Rome* — Rome, AD 112

> Power is inherited, fortunes are made, and some wounds never heal.

**Age rating:** Mature (18+). Adult themes are treated with literary seriousness —
sexual exploitation, slavery, violence, corruption and grief. There is no explicit
or gratuitous content.

**Status:** First draft complete. 25 chapters + epilogue, ~136,000 words.

**Deliverable:** [`08_Publication/The_Price_of_a_Name.pdf`](../../08_Publication/The_Price_of_a_Name.pdf)
— 383 pages, 6 × 9 in, EB Garamond, running heads, drop folios on chapter openers,
bookmarked PDF outline, linked table of contents.

---

## Structure

| Part | Chapters | Arc |
| --- | --- | --- |
| One — The House | 1–4 | The world of the household, the first summons from the Palatine, and a debt called in. |
| Two — The Price of a Name | 5–9 | The buried past, the search, the daughter who comes asking, and a public meeting in the rain. |
| Three — What the Streets Know | 10–14 | A death in the house, the machinery of law, and a woman hired to copy the ledgers. |
| Four — The Judgement of the City | 15–19 | The confession, the trial, the verdict, and the truth told to the last person who needs it. |
| Five — The Reckoning | 20–25 | A divided house, a killing in the courtyard, a fire, and a settlement rather than a forgiveness. |
| Epilogue — The Garden | — | Six years on: what is left in the record, and what is not. |

Full cast list and beat sheet: [`Outline/Outline.md`](Outline/Outline.md).

## Manuscript

`Chapters/` holds the source prose, one Markdown file per chapter, in reading order
(`ch01.md` … `ch26.md`, where `ch26.md` is the epilogue). Each file starts with a
level-1 heading in the form `# N | Title`, or `# Epilogue | Title`.

Conventions:

- A paragraph is a line. Blank lines are ignored.
- A line containing only `---` is a scene break (rendered as a centred rule).
- `*italic*` and `**bold**` are supported inline.
- Straight apostrophes and single quotes are converted to typographic quotes at
  build time; double quotes are not used, in keeping with the novel's dialogue style.

## Build

```bash
python3 -m venv .venv && .venv/bin/pip install reportlab
.venv/bin/python 05_Books/Rome_AD_112/Build/build_pdf.py --check   # word counts
.venv/bin/python 05_Books/Rome_AD_112/Build/build_pdf.py           # writes the PDF
```

The build script reads `Chapters/`, typesets the front matter (title page, colophon,
epigraph, contents), inserts part pages, and writes
`08_Publication/The_Price_of_a_Name.pdf`.

Fonts in `Build/fonts/` are EB Garamond (SIL Open Font License, see `OFL.txt`).

## Notes for revision

- Chapter word counts run 4,655–5,913; the brief asked for roughly 5,000–6,000.
  Chapters 3 and 4 sit slightly under and are the first candidates for expansion.
- The narrative uses two devices worth tracking in revision: the recurring "eleven"
  motif, and the two-kinds-of-silence figure introduced in chapter 11 and closed in
  the epilogue.
- Continuity anchors that must not drift: the manumission year (seven years before
  the present), the price of the child (240 sesterces), the price of the mother
  (2,400), and the four things in the strongbox.
