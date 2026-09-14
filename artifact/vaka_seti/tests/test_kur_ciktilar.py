"""kur.py çıktıları için regresyon guard'ı.

Amaç: satır sonu (CRLF) hatasının sessizce geri gelmesini engellemek.
Geçmiş: CSV üreteci CRLF yazıyordu (csv varsayılanı) ve her çalıştırmada
sahte bir git diff üretiyordu. Aynı sınıf hata JSON ve 2x2 Markdown
çıktılarında da mümkündü (Path.write_text Windows'ta \n -> \r\n yapar).

Ek guard'lar (İngilizceye çeviri sonrası): quote sütunu referans değerlerle birebir aynı,
outcome kodlanmış değerleri İngilizce snake_case, çevrilen serbest metin sütunlarında
Türkçe karakter yok, korunan sütunlar (quote/locator/source_doc/source) çeviriden etkilenmemiş.

Bu test API'siz çalışır ve dosya sistemine yalnızca geçici dizinde yazar.

Çalıştırma:
    python3 artifact/vaka_seti/tests/test_kur_ciktilar.py
"""

from __future__ import annotations

import csv
import importlib.util
import json
import re
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


# Referans: 13 alıntı, kur.py'nin İngilizceye çevrilmeden ÖNCEKİ hâlinden (commit c6f3613)
# programla alınmıştır. quote sütunu birebir kaynak metnidir; tek karakter bile değişemez.
REFERANS_ALINTILAR = {
    'C01': '“One particularly stark example of cheating behaviour occurred during a cyber capability evaluation that was accidentally misconfigured and therefore impossible to solve. The model tested was so persistent in attempting to cheat that it wrote and ran code on an external service…”',
    'C02': '“Claude ran into difficulty reaching its simulated target within the evaluation environment, but then discovered that the real company was reachable via the internet.”',
    'C03': '“And in order to create an email address, it needed a phone number. To get a phone number, after failing to find a free phone number service, it tried—and failed—to obtain funds…”',
    'C04': '“when Claude was unable to reach its intended fictional target, it looked for alternatives online, scanning roughly 9,000 targets.”',
    'C05': '“A GET request only gave answers to one decimal point, but the agents needed two. This is why they discussed and attempted workarounds.”',
    'C06': '“Because the agent was blocked from accessing the internet, the agent could not retrieve the linked materials and the task was effectively blocked.”',
    'C07': '“On May 12, during another training run, an agent was given a similar task that depended on an inaccessible protein database file.”',
    'C08': '“After failing to find the file through public filename, digest, sequence, and source-code searches, the agent searched the Hugging Face website…”',
    'C09': '“The agent realized that it could exploit a vulnerability in the setup to write files into the environment where the reference library was stored. This allowed it to get direct access to the underlying program it was trying to replicate.”',
    'C10': '“However, the interface it was provided did not have any functionality for setting the time. This caused the agent to do a broad exploration of its environment, eventually discovering that its browser had root privileges.”',
    'C11': '“Despite only 22% of the evaluation tasks being unsolved, 93% of the tasks discussed on the message board came from this set.” (Technical Report, printed p. 22) · “the presence of impossible tasks in the ExploitGym evaluation” (printed p. 19) · “These unsolved tasks ended up being a substantial contributor to the Hugging Face incident.” (S4)',
    'C12': '“After the server died, the task became impossible through the intended path, and the agent spent the remaining run attempting to recover the server or escape the evaluation container.”',
    'C13': '“the agent couldn’t use the API key it was given because the associated API account had run out of credit.”',
}

# outcome kodlanmış değerleri (İngilizce, snake_case). Eski Türkçe eşleme README'de tabloyla.
OUTCOME_DEGERLERI = {"constraint_breached", "attempted_failed", "solved_honestly"}

# Çeviriden etkilenmemesi gereken sütunlar (birebir kaynak metni / belge adı / konum).
KORUNAN_SUTUNLAR = ("quote", "locator", "source_doc", "source")

# İngilizceye çevrilen serbest metin sütunları.
CEVRILEN_SUTUNLAR = ("task", "blocked_thing", "agent_response", "context_basis", "blocked_type_basis")

_TR_HARF = re.compile("[çğıöşüÇĞİÖŞÜ]")


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
    """Aynı dosyaya iki kez yazılınca bayt-bayt aynı kalmalı (sahte diff olmaz).

    Not: iki AYRI dosyaya yazıp karşılaştırmak deterministikliği ölçer, idempotentliği
    değil. Gerçek senaryo üretecin var olan bir dosyanın üzerine tekrar çalışmasıdır;
    append mode ya da yalnızca üzerine yazarken tetiklenen bir regresyon ancak
    aynı yola iki kez yazarak yakalanır.
    """
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "cikti.csv"
        kur.yaz_csv(kur.VAKALAR, p)
        ilk = p.read_bytes()
        kur.yaz_csv(kur.VAKALAR, p)          # aynı yola ikinci kez
        assert p.read_bytes() == ilk, \
            "İkinci üretim aynı baytları vermedi (idempotent değil — ör. append modu)"
    print("ok test_idempotent")


def test_dogrulama_gecer():
    """VAKALAR tutarlı olmalı (kur.dogrula hata vermemeli)."""
    kur.dogrula(kur.VAKALAR)
    print("ok test_dogrulama_gecer")


def test_alintilar_degismedi():
    """13 alıntının hiçbiri değişmemiş olmalı (referans değerlerle karakter-karakter aynı)."""
    alintilar = {v["case_id"]: v["quote"] for v in kur.VAKALAR}
    assert set(alintilar) == set(REFERANS_ALINTILAR), "case_id kümesi referansla uyuşmuyor"
    for cid, ref in REFERANS_ALINTILAR.items():
        assert alintilar[cid] == ref, f"{cid}: quote değişmiş"
    # üretilen CSV ve JSON da aynı alıntıyı taşımalı
    with tempfile.TemporaryDirectory() as d:
        pc = Path(d) / "cikti.csv"
        pj = Path(d) / "cikti.json"
        kur.yaz_csv(kur.VAKALAR, pc)
        kur.yaz_json(kur.VAKALAR, pj)
        with pc.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                assert r["quote"] == REFERANS_ALINTILAR[r["case_id"]], f"CSV {r['case_id']}: quote değişmiş"
        for v in json.loads(pj.read_text(encoding="utf-8"))["vakalar"]:
            assert v["quote"] == REFERANS_ALINTILAR[v["case_id"]], f"JSON {v['case_id']}: quote değişmiş"
    print("ok test_alintilar_degismedi")


def test_outcome_ingilizce_snake_case():
    """outcome değerleri kodlanmış İngilizce set içinde; eski Türkçe değerler kalmamış."""
    for v in kur.VAKALAR:
        assert v["outcome"] in OUTCOME_DEGERLERI, f"{v['case_id']}: outcome={v['outcome']!r}"
        assert re.fullmatch(r"[a-z]+(_[a-z]+)*", v["outcome"]), v["case_id"]
    # 2x2: outcome != solved_honestly -> escape attempt sütunu; mevcut 13 vaka orada
    with tempfile.TemporaryDirectory() as d:
        metin = kur.yaz_2x2(kur.VAKALAR, Path(d) / "t.md")
    assert "| | escape attempt | honest solution |" in metin
    assert "| **requirement** | 12 —" in metin and "| **shortcut** | 1 — C09 |" in metin
    print("ok test_outcome_ingilizce_snake_case")


def test_cevrilen_sutunlarda_turkce_karakter_yok():
    """task/blocked_thing/agent_response/context_basis/blocked_type_basis İngilizce olmalı."""
    for v in kur.VAKALAR:
        for alan in CEVRILEN_SUTUNLAR + ("outcome", "context", "blocked_type", "causal_status"):
            assert not _TR_HARF.search(v[alan]), f"{v['case_id']}.{alan}: Türkçe karakter: {v[alan][:60]!r}"
    print("ok test_cevrilen_sutunlarda_turkce_karakter_yok")


def test_korunan_sutunlar_dolu_ve_alan_sirasi():
    """Korunan sütunlar boş değil; alan sırası (CSV başlığı) değişmemiş."""
    for v in kur.VAKALAR:
        for alan in KORUNAN_SUTUNLAR:
            assert v[alan].strip(), f"{v['case_id']}.{alan} boş"
    assert kur.ALANLAR == [
        "case_id", "source", "source_doc", "locator", "context", "task",
        "blocked_thing", "blocked_type", "agent_response", "outcome",
        "causal_status", "quote",
    ]
    assert kur.EK_ALANLAR == ["context_basis", "blocked_type_basis", "instance"]
    print("ok test_korunan_sutunlar_dolu_ve_alan_sirasi")


def main() -> int:
    testler = [test_csv_lf, test_json_lf, test_2x2_lf, test_idempotent, test_dogrulama_gecer,
               test_alintilar_degismedi, test_outcome_ingilizce_snake_case,
               test_cevrilen_sutunlarda_turkce_karakter_yok, test_korunan_sutunlar_dolu_ve_alan_sirasi]
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