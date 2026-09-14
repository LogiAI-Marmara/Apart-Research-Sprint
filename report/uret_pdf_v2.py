#!/usr/bin/env python3
"""rapor-taslak-v1.md -> apart-research-sprint-report-v2.pdf

PDF v1'in yerini ALMAZ; yanına ikinci bir dosya üretir (istenen davranış).
Amaç: issue #9 (yanlış alıntı), #10 ("five" sayısı), T1 (Yee), T2 ("four evaluators")
düzeltmelerini PDF'e yansıtmak.

Kullanım:  python3 report/uret_pdf_v2.py
Gereksinim: pdflatex (texlive), Türkçe/Unicode için fontspec+lualatex tercih edilir;
            lualatex yoksa pdflatex + inputenc kullanılır (rapor gövdesi çoğunlukla ASCII).
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
MD = KOK / "report" / "rapor-taslak-v1.md"
CIKTI = KOK / "report" / "apart-research-sprint-report-v2.pdf"
TEX = KOK / "report" / "uretim_v2.tex"


def _lateks_kacis(s: str) -> str:
    """LaTeX özel karakterlerini kaçır (kod/URL parçaları hariç kaba kaçış)."""
    for a, b in [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        s = s.replace(a, b)
    return s


def _satir_ici(s: str) -> str:
    """Satır içi markdown -> LaTeX (kalın, italik, kod).

    Sıra önemli: önce kod span'lerini korumaya al, sonra DÜZ METNİ kaçır,
    en son kalın/italik dönüşümlerini uygula.
    """
    kodlar: list[str] = []

    def _kod_koru(m: re.Match[str]) -> str:
        kodlar.append(m.group(1))
        return f"\x00KOD{len(kodlar) - 1}\x00"

    s = re.sub(r"`([^`]+)`", _kod_koru, s)
    s = _lateks_kacis(s)                                   # düz metni kaçır
    s = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", s)
    # korunan kodları geri koy
    for i, kod in enumerate(kodlar):
        s = s.replace(f"\x00KOD{i}\x00", r"\texttt{" + _lateks_kacis(kod) + "}")
    return s


def md_to_latex(md: str) -> str:
    out: list[str] = []
    tablo: list[list[str]] = []
    liste: list[str] = []          # ardışık madde imlerini biriktir
    liste_tur = ""                 # "itemize" | "enumerate"

    def tablo_bosalt() -> None:
        if not tablo:
            return
        genislik = max(len(r) for r in tablo)
        out.append(r"\begin{center}\small")
        out.append(r"\begin{tabular}{" + "l" * genislik + "}")
        out.append(r"\hline")
        for i, satir in enumerate(tablo):
            hucreler = [_satir_ici(c.strip()) for c in satir]
            hucreler += [""] * (genislik - len(hucreler))
            out.append(" & ".join(hucreler) + r" \\")
            if i == 0:
                out.append(r"\hline")
        out.append(r"\hline")
        out.append(r"\end{tabular}")
        out.append(r"\end{center}")
        tablo.clear()

    def liste_bosalt() -> None:
        if not liste:
            return
        out.append(r"\begin{" + liste_tur + r"}\setlength\itemsep{2pt}")
        for madde in liste:
            out.append(r"\item " + madde)
        out.append(r"\end{" + liste_tur + "}")
        liste.clear()

    for satir in md.splitlines():
        # Tablo satırı topla
        if satir.strip().startswith("|"):
            liste_bosalt()
            hucreler = [c for c in satir.strip().strip("|").split("|")]
            if all(re.fullmatch(r"\s*:?-{2,}:?\s*", c) for c in hucreler):
                continue  # ayraç satırı
            tablo.append(hucreler)
            continue
        tablo_bosalt()

        s = satir.rstrip()
        if not s.strip():
            liste_bosalt()
            out.append("")
            continue
        if s.startswith("---"):
            liste_bosalt()
            out.append(r"\medskip\hrule\medskip")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            liste_bosalt()
            seviye = len(m.group(1))
            baslik = _satir_ici(m.group(2))
            if seviye == 1:
                out.append(r"\begin{center}{\LARGE\bfseries " + baslik + r"}\end{center}")
            elif seviye == 2:
                out.append(r"\section*{" + baslik + r"}")
            elif seviye == 3:
                out.append(r"\subsection*{" + baslik + r"}")
            else:
                out.append(r"\subsubsection*{" + baslik + r"}")
            continue
        if re.match(r"^\s*[-*]\s+", s):
            if liste_tur and liste_tur != "itemize":
                liste_bosalt()
            liste_tur = "itemize"
            liste.append(_satir_ici(re.sub(r"^\s*[-*]\s+", "", s)))
            continue
        if re.match(r"^\s*\d+\.\s+", s):
            if liste_tur and liste_tur != "enumerate":
                liste_bosalt()
            liste_tur = "enumerate"
            # numarayı koru ama LaTeX'in kendi sayacını kullan (ardışık grup)
            liste.append(_satir_ici(re.sub(r"^\s*\d+\.\s+", "", s)))
            continue
        # Liste öğesinin DEVAM satırı (girintili, imsiz): önceki maddeye ekle.
        # Yoksa çok satırlı maddeler listeyi bölüp her maddeyi yeniden 1'den başlatırdı.
        if liste and re.match(r"^[ \t]+\S", satir):
            liste[-1] += " " + _satir_ici(s)
            continue
        liste_bosalt()
        out.append(_satir_ici(s))

    tablo_bosalt()
    liste_bosalt()
    return "\n".join(out)


def main() -> int:
    if not MD.exists():
        print(f"HATA: kaynak yok: {MD}", file=sys.stderr)
        return 1

    gövde = md_to_latex(MD.read_text(encoding="utf-8"))
    # pdflatex + T1 + lmodern: Türkçe karakterler (İ, ğ, ş) T1 encoding ile doğru gider.
    onsoz = r"""\documentclass[10pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[english,turkish]{babel}
\usepackage[a4paper,margin=2.2cm]{geometry}
\usepackage{parskip}
\usepackage{hyperref}
\hypersetup{hidelinks}
\usepackage{longtable}
\usepackage{array}
\setlength{\parskip}{0.5em}
\usepackage{textcomp}
\title{}
\date{}
\begin{document}
"""
    tex = onsoz + gövde + "\n\\end{document}\n"
    TEX.write_text(tex, encoding="utf-8")

    isim, motor = "pdflatex", shutil.which("pdflatex")
    if not motor:
        print("HATA: pdflatex bulunamadı", file=sys.stderr)
        return 1

    for _ in range(2):  # referanslar için iki geçiş
        r = subprocess.run(
            [motor, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={TEX.parent}", TEX.name],
            cwd=TEX.parent, capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(r.stdout[-4000:], file=sys.stderr)
            print(f"HATA: {isim} başarısız", file=sys.stderr)
            return 1

    uretilen = TEX.with_suffix(".pdf")
    if not uretilen.exists():
        print("HATA: PDF üretilemedi", file=sys.stderr)
        return 1
    shutil.move(str(uretilen), str(CIKTI))
    for ek in (".aux", ".log", ".out", ".tex"):
        p = TEX.with_suffix(ek)
        if p.exists():
            p.unlink()
    print(f"OK: {CIKTI} ({CIKTI.stat().st_size} bayt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())