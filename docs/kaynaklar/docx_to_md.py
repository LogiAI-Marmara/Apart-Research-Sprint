"""escape_pressure_evidence_audit.docx -> Markdown, alıntı sadakati öncelikli.

Hiçbir metin yeniden yazılmaz: paragraflar belge sırasıyla, stil -> Markdown eşlemesiyle
aktarılır. Kalın run'lar **...** olur, köprüler [metin](url) olur, tırnak/ok/tire karakterleri
olduğu gibi kalır. Tablo yok (belgede tablo bulunmuyor; olsaydı GFM tablosu üretilirdi).

    pip install python-docx
    python kaynaklar/docx_to_md.py kaynaklar/orijinal/escape_pressure_evidence_audit.docx \
        kaynaklar/escape_pressure_evidence_audit.md
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

STYLE_PREFIX = {
    "Title": "# ",
    "Subtitle": "*",  # kapanış eklenir
    "Heading 1": "## ",
    "Heading 2": "### ",
    "Heading 3": "#### ",
    "Evidence Quote": "> ",
    "Source List": "- ",
    "List Bullet": "- ",
    "Normal": "",
}


def _run_md(run_el, rels) -> str:
    """Tek bir <w:r> ya da <w:hyperlink> öğesini Markdown'a çevirir."""
    if run_el.tag == qn("w:hyperlink"):
        rid = run_el.get(qn("r:id"))
        url = rels[rid].target_ref if rid in rels else None
        inner = "".join(_run_md(r, rels) for r in run_el if r.tag == qn("w:r"))
        return f"[{inner}]({url})" if url else inner
    if run_el.tag != qn("w:r"):
        return ""
    text = "".join(
        (t.text or "") if t.tag == qn("w:t") else ("\n" if t.tag == qn("w:br") else "")
        for t in run_el
    )
    if not text:
        return ""
    rpr = run_el.find(qn("w:rPr"))
    bold = rpr is not None and rpr.find(qn("w:b")) is not None
    if bold and text.strip():
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        return f"{lead}**{text.strip()}**{trail}"
    return text


def paragraph_md(p, rels) -> str:
    style = p.style.name if p.style is not None else "Normal"
    body = "".join(_run_md(el, rels) for el in p._p)
    body = body.replace("**  **", "  ")  # ardışık kalın run'lar arasındaki boşluk
    if style == "Subtitle":
        return f"*{body}*"
    prefix = STYLE_PREFIX.get(style, "")
    if style == "Evidence Quote":
        body = body.replace("\n", "\n> ")
    return prefix + body


def convert(src: Path, dst: Path) -> None:
    doc = Document(str(src))
    rels = doc.part.rels
    out: list[str] = []
    for p in doc.paragraphs:
        out.append(paragraph_md(p, rels))
        out.append("")
    dst.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    convert(src, dst)
    print(f"{src} -> {dst}")
