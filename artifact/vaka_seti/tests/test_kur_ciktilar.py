"""kur.py çıktıları için regresyon guard'ı.

Amaç: satır sonu (CRLF) hatasının sessizce geri gelmesini engellemek.
Geçmiş: CSV üreteci CRLF yazıyordu (csv varsayılanı) ve her çalıştırmada
sahte bir git diff üretiyordu. Aynı sınıf hata JSON ve 2x2 Markdown
çıktılarında da mümkündü (Path.write_text Windows'ta \n -> \r\n yapar).

Bu test API'siz çalışır ve dosya sistemine yalnızca geçici dizinde yazar.

Çalıştırma:
    python3 artifact/vaka_seti/tests/test_kur_ciktilar.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../vaka_seti/tests
VAKA_SETI = HERE.parent                          # .../vaka_seti

# kur.py'yi modül olarak yükle (vaka_seti paket değil, düz script).
_spec = importlib.util.spec_from_file_location("kur", VAKA_SETI / "kur.py")
assert _spec is not None and _spec.loader is not None
kur = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kur)


def _crlf_var(p: Path) -> bool:
    """Dosyada ham CRLF (\\r\\n) baytı var mı?"""
    return b"\r\n" in p.read_bytes()


def _cr_var(p: Path) -> bool:
    """Dosyada tek başına CR (\\r) var mı? (LF dışında satır sonu demek)"""
    return b"\r" in p.read_bytes()


def test_csv_lf():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "cikti.csv"
        kur.yaz_csv(kur.VAKALAR, p)
        assert not _cr_var(p), "CSV'de CR var — LF bekleniyordu"
    print("ok test_csv_lf")


def test_json_lf():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "cikti.json"
        kur.yaz_json(kur.VAKALAR, p)
        assert not _cr_var(p), "JSON'da CR var — LF bekleniyordu"
    print("ok test_json_lf")


def test_2x2_lf():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "tablo.md"
        kur.yaz_2x2(kur.VAKALAR, p)
        assert not _cr_var(p), "2x2 Markdown'da CR var — LF bekleniyordu"
    print("ok test_2x2_lf")


def test_idempotent():
    """Aynı içerik iki kez yazılınca bayt-bayt aynı olmalı (sahte diff olmaz)."""
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d) / "a", Path(d) / "b"
        for f in (a, b):
            kur.yaz_csv(kur.VAKALAR, f.with_suffix(".csv"))
        assert a.with_suffix(".csv").read_bytes() == b.with_suffix(".csv").read_bytes(), \
            "İki ardışık üretim aynı baytları vermedi"
    print("ok test_idempotent")


def test_dogrulama_gecer():
    """VAKALAR tutarlı olmalı (kur.dogrula hata vermemeli)."""
    kur.dogrula(kur.VAKALAR)
    print("ok test_dogrulama_gecer")


def main() -> int:
    testler = [test_csv_lf, test_json_lf, test_2x2_lf, test_idempotent, test_dogrulama_gecer]
    basarisiz = 0
    for t in testler:
        try:
            t()
        except AssertionError as e:
            basarisiz += 1
            print(f"FAIL {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            basarisiz += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(testler) - basarisiz}/{len(testler)} geçti")
    return 1 if basarisiz else 0


if __name__ == "__main__":
    sys.exit(main())