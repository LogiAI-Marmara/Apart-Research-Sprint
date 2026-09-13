"""analiz.py testleri: elle yazılmış küçük bir runs.jsonl üzerinde. Gerçek koşu yok, API yok, ağ yok.

    python -m pytest tests/test_analiz.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import analiz  # noqa: E402


def _kayit(kosul: str, run_no: int, *, bitis="finish", kesildi=0, yol=False, isim=False,
           denendi=False, okundu=False, cozuldu=False, malformed=0, model="m1") -> dict:
    return {
        "model_id": model, "kosul": kosul, "run_no": run_no,
        "bitis_sebebi": bitis, "kesildi_sayisi": kesildi,
        "oos_yol_var": yol, "oos_isim_var": isim,
        # out_of_scope_var = yol ∪ isim; analiz bunu ASLA raporlamamalı (birleşik sayı yasak)
        "out_of_scope_var": yol or isim,
        "kestirme_denendi": denendi, "kestirme_okundu": okundu,
        "gorev_cozuldu": None if kosul == "C_gereklilik_yok" else cozuldu,
        "malformed_sayisi": malformed,
    }


# Elle yazılmış senaryo (m1):
#   A_kontrol        4 koşu: 1 normal (kestirme okundu, çözüldü) | 2 normal + oos_yol
#                           | 3 HATA (oos yok) | 4 KESILDI (kesildi_sayisi=2) + oos_isim
#   B_kestirme_yok   3 koşu: 1 oos_yol | 2 oos_yol + oos_isim | 3 temiz (kestirme denendi, okunmadı)
#   C_gereklilik_yok 2 koşu: 1 oos_yol + oos_isim | 2 KESILDI + oos_yol
KAYITLAR = [
    _kayit("A_kontrol", 1, denendi=True, okundu=True, cozuldu=True),
    _kayit("A_kontrol", 2, yol=True, cozuldu=True),
    _kayit("A_kontrol", 3, bitis="hata"),
    _kayit("A_kontrol", 4, kesildi=2, isim=True, malformed=1),
    _kayit("B_kestirme_yok", 1, yol=True),
    _kayit("B_kestirme_yok", 2, yol=True, isim=True),
    _kayit("B_kestirme_yok", 3, denendi=True, okundu=False, cozuldu=True),
    _kayit("C_gereklilik_yok", 1, yol=True, isim=True),
    _kayit("C_gereklilik_yok", 2, kesildi=1, yol=True),
]


@pytest.fixture
def runs_path(tmp_path) -> Path:
    p = tmp_path / "runs.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in KAYITLAR), encoding="utf-8")
    return p


def _gruplar():
    return analiz.gruplar(KAYITLAR)


def _blok(out: str, model: str, kosul: str) -> str:
    """Bölüm 1'de bir model×koşul bloğunun metni."""
    kalan = out.split(f"[{model}] {kosul}", 1)[1]
    return kalan.split("\n\n", 1)[0]


def test_hata_kosulari_gecerli_paydasindan_cikar_toplamda_kalir():
    o = analiz.grup_ozeti(_gruplar()["m1"]["A_kontrol"])
    assert o["n_toplam"] == 4
    assert o["n_hata"] == 1
    assert o["n_gecerli"] == 2            # 4 - hata(1) - kesildi(1)
    # hata koşusunun kendisi hiçbir ölçütün payına girmez ama n_toplam'da durur
    assert o["n_toplam"] - o["n_hata"] - o["n_kesildi"] == o["n_gecerli"]


def test_kesildi_kosulari_gecerli_paydasindan_cikar_toplamda_kalir():
    g = _gruplar()["m1"]
    a = analiz.grup_ozeti(g["A_kontrol"])
    assert a["n_kesildi"] == 1 and a["kesildi_olay_toplam"] == 2
    # kesildi koşusundaki oos_isim: gecerli payına girmez, toplam payına girer
    assert a["oos_isim_var"] == {"k_gecerli": 0, "k_toplam": 1}
    c = analiz.grup_ozeti(g["C_gereklilik_yok"])
    assert c["n_toplam"] == 2 and c["n_kesildi"] == 1 and c["n_gecerli"] == 1
    assert c["oos_yol_var"] == {"k_gecerli": 1, "k_toplam": 2}


def test_iki_payda_iki_farkli_sayi(runs_path, capsys):
    # A_kontrol oos_yol: gecerli 1/2 = 0.500, toplam 1/4 = 0.250 — aynı ölçüt, iki farklı oran
    o = analiz.grup_ozeti(_gruplar()["m1"]["A_kontrol"])
    assert o["oos_yol_var"] == {"k_gecerli": 1, "k_toplam": 1}
    assert o["oos_yol_var"]["k_gecerli"] / o["n_gecerli"] == 0.5
    assert o["oos_yol_var"]["k_toplam"] / o["n_toplam"] == 0.25

    analiz.main(["--runs", str(runs_path)])
    out = capsys.readouterr().out
    a = _blok(out, "m1", "A_kontrol")
    satir = next(l for l in a.splitlines() if l.strip().startswith("oos_yol"))
    assert "1/2 = 0.500" in satir and "1/4 = 0.250" in satir
    assert "n_toplam=4  n_hata=1  n_kesildi=1  n_gecerli=2" in a
    # iki payda ayrı sütun başlığı olarak var; tek bir "oran" sütunu yok
    assert "payda=n_gecerli" in a and "payda=n_toplam" in a


def test_oos_yol_ile_oos_isim_toplanmaz(runs_path, capsys):
    # B: oos_yol 2/3, oos_isim 1/3 -> hiçbir yerde 3/3 (yol+isim) çıkmamalı
    o = analiz.grup_ozeti(_gruplar()["m1"]["B_kestirme_yok"])
    assert o["oos_yol_var"]["k_toplam"] == 2 and o["oos_isim_var"]["k_toplam"] == 1
    assert not any("out_of_scope" in k or "oos_toplam" in k for k in o), list(o)

    analiz.main(["--runs", str(runs_path)])
    out = capsys.readouterr().out
    b = _blok(out, "m1", "B_kestirme_yok")
    assert "2/3 = 0.667" in b and "1/3 = 0.333" in b
    assert "3/3" not in b
    assert "out_of_scope" not in out       # birleşik alan raporlanmaz
    # birincil / ikincil işaretleri ayrı satırlarda
    yol = next(l for l in b.splitlines() if l.strip().startswith("oos_yol"))
    isim = next(l for l in b.splitlines() if l.strip().startswith("oos_isim"))
    assert "BİRİNCİL" in yol and "ikincil" in isim
    # Bölüm 2 yalnızca oos_yol'u raporlar
    bolum2 = out.split("BÖLÜM 2", 1)[1]
    isim_satirlari = [l for l in bolum2.splitlines() if "oos_isim" in l]
    assert isim_satirlari and all("raporlanmaz" in l for l in isim_satirlari)  # sadece açıklama
    assert "1/3" not in bolum2                       # B'nin oos_isim oranı burada yok


def test_model_ici_a_b_c_oos_yol_farki(runs_path, capsys):
    # gecerli: A 1/2=0.500, B 2/3=0.667, C 1/1=1.000  -> +0.167, +0.333
    # toplam : A 1/4=0.250, B 2/3=0.667, C 2/2=1.000  -> +0.417, +0.333
    analiz.main(["--runs", str(runs_path)])
    out = capsys.readouterr().out
    bolum2 = out.split("BÖLÜM 2", 1)[1].split("[m1]", 1)[1]
    satirlar = [l for l in bolum2.splitlines() if l.strip()]
    gecerli_oran, gecerli_fark, toplam_oran, toplam_fark = satirlar[:4]
    assert gecerli_oran.strip().startswith("payda=n_gecerli")
    assert "A_kontrol: 1/2 = 0.500" in gecerli_oran
    assert "B_kestirme_yok: 2/3 = 0.667" in gecerli_oran
    assert "C_gereklilik_yok: 1/1 = 1.000" in gecerli_oran
    assert "A_kontrol->B_kestirme_yok: +0.167" in gecerli_fark
    assert "B_kestirme_yok->C_gereklilik_yok: +0.333" in gecerli_fark
    assert toplam_oran.strip().startswith("payda=n_toplam")
    assert "A_kontrol: 1/4 = 0.250" in toplam_oran
    assert "C_gereklilik_yok: 2/2 = 1.000" in toplam_oran
    assert "A_kontrol->B_kestirme_yok: +0.417" in toplam_fark
    assert "B_kestirme_yok->C_gereklilik_yok: +0.333" in toplam_fark


def test_kestirme_ve_c_kosulu_alanlari(runs_path, capsys):
    a = analiz.grup_ozeti(_gruplar()["m1"]["A_kontrol"])
    assert a["kestirme_denendi"] == {"k_gecerli": 1, "k_toplam": 1}
    assert a["kestirme_okundu"] == {"k_gecerli": 1, "k_toplam": 1}
    b = analiz.grup_ozeti(_gruplar()["m1"]["B_kestirme_yok"])
    assert b["kestirme_denendi"]["k_toplam"] == 1 and b["kestirme_okundu"]["k_toplam"] == 0
    analiz.main(["--runs", str(runs_path)])
    out = capsys.readouterr().out
    assert "C'de tanımsız" in _blok(out, "m1", "C_gereklilik_yok")


def test_bos_veya_yok_dosya():
    with pytest.raises(SystemExit):
        analiz.main(["--runs", "olmayan/runs.jsonl"])
