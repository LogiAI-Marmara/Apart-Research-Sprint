"""Deney sürücüsü.

  python run.py --smoke      koşul başına 1 koşu, her model; sonunda doğrulama çıktısı
  python run.py --n 10       koşul başına 10 koşu, sadece smoke'u geçen modeller

Smoke sonuçları results/smoke/ altına, tam koşu results/ altına yazılır.
Tam koşu, results/smoke/smoke_ok.json olmadan başlamaz (--force ile geçilebilir).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from deney.agent import run_one
from deney.config import Defaults, SubjectConfig, load_config, load_dotenv
from deney.llm import OpenAICompatClient
from deney.recorder import Recorder
from deney.sandbox import KOSULLAR

ROOT = Path(__file__).resolve().parent


def build_client(s: SubjectConfig, d: Defaults) -> OpenAICompatClient:
    api_key = os.environ.get(s.api_key_env)
    if not api_key:
        raise SystemExit(f"[{s.id}] ortam değişkeni yok: {s.api_key_env} (.env ya da shell)")
    return OpenAICompatClient(
        s.base_url,
        api_key,
        s.model,
        temperature=s.temperature if s.temperature is not None else d.temperature,
        max_tokens=s.max_tokens if s.max_tokens is not None else d.max_tokens,
        timeout=d.timeout,
        max_retries=d.max_retries,
        extra_headers=s.extra_headers,
        extra_body=s.extra_body,
    )


def kosulari_kos(
    subjects: list[SubjectConfig],
    defaults: Defaults,
    n: int,
    rec: Recorder,
    kosullar: list[str],
    *,
    progress: bool,
) -> None:
    mevcut = rec.mevcut_anahtarlar()
    for s in subjects:
        client = build_client(s, defaults)
        for kosul in kosullar:
            for run_no in range(1, n + 1):
                if (s.id, kosul, run_no) in mevcut:
                    continue
                ozet, tr = run_one(client, s.id, kosul, run_no, max_turns=defaults.max_turns)
                rec.kaydet(ozet, tr)
                if progress:
                    print(
                        f"[{s.id}] {kosul} {run_no}/{n} bitis={ozet['bitis_sebebi']} "
                        f"tur={ozet['tur_sayisi']} cozuldu={ozet['gorev_cozuldu']} "
                        f"oos={ozet['out_of_scope_sayisi']} malformed={ozet['malformed_sayisi']}",
                        file=sys.stderr,
                        flush=True,
                    )


def smoke_dogrulama(rec: Recorder, subjects: list[SubjectConfig]) -> dict:
    """Sadece istenen üç şeyi ham olarak basar; geçen/kalan modelleri döner."""
    kayitlar = rec.kayitlar()
    gecen, kalan = [], []
    for s in subjects:
        a = [r for r in kayitlar if r["model_id"] == s.id and r["kosul"] == "A_kontrol"]
        cozuldu = bool(a and a[-1]["gorev_cozuldu"])
        print(f"{s.id} A_kontrol gorev_cozuldu={cozuldu}")
        (gecen if cozuldu else kalan).append(s.id)

    print(f"MALFORMED toplam: {sum(r['malformed_sayisi'] for r in kayitlar)}")

    if kayitlar:
        tr_path = rec.out_dir / kayitlar[0]["transcript_dosyasi"]
        tr = json.loads(tr_path.read_text(encoding="utf-8"))
        print(f"{tr_path.relative_to(rec.out_dir).as_posix()} ilk 3 tur:")
        print(json.dumps(tr["turlar"][:3], ensure_ascii=False, indent=2))

    return {"gecen": gecen, "kalan": kalan}


def main() -> None:
    for stream in (sys.stdout, sys.stderr):  # Windows konsolunda Türkçe karakterler için
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--smoke", action="store_true", help="koşul başına 1 koşu, her model")
    g.add_argument("--n", type=int, help="koşul başına koşu sayısı (tam deney)")
    ap.add_argument("--config", default=str(ROOT / "config" / "models.yaml"))
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--models", help="virgülle ayrılmış subject id listesi (varsayılan: hepsi)")
    ap.add_argument("--conditions", help="virgülle ayrılmış koşul listesi (varsayılan: hepsi)")
    ap.add_argument("--force", action="store_true", help="smoke kapısını atla")
    ap.add_argument("--fresh", action="store_true", help="mevcut kayıtları görmezden gel (üzerine ekler)")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    defaults, subjects = load_config(Path(args.config))
    if args.models:
        istenen = set(args.models.split(","))
        bilinmeyen = istenen - {s.id for s in subjects}
        if bilinmeyen:
            raise SystemExit(f"bilinmeyen model id: {sorted(bilinmeyen)}")
        subjects = [s for s in subjects if s.id in istenen]

    kosullar = list(KOSULLAR)
    if args.conditions:
        kosullar = args.conditions.split(",")
        bilinmeyen = set(kosullar) - set(KOSULLAR)
        if bilinmeyen:
            raise SystemExit(f"bilinmeyen koşul: {sorted(bilinmeyen)}")

    out = Path(args.out)
    smoke_ok_path = out / "smoke" / "smoke_ok.json"

    if args.smoke:
        rec = Recorder(out / "smoke")
        if args.fresh and rec.runs_path.exists():
            rec.runs_path.unlink()
        kosulari_kos(subjects, defaults, 1, rec, kosullar, progress=False)
        sonuc = smoke_dogrulama(rec, subjects)
        smoke_ok_path.write_text(json.dumps(sonuc, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    if args.n < 1:
        raise SystemExit("--n >= 1 olmalı")
    if not args.force:
        if not smoke_ok_path.is_file():
            raise SystemExit("önce `python run.py --smoke` çalıştır (ya da --force)")
        gecen = set(json.loads(smoke_ok_path.read_text(encoding="utf-8"))["gecen"])
        dusen = [s.id for s in subjects if s.id not in gecen]
        subjects = [s for s in subjects if s.id in gecen]
        if dusen:
            print(f"smoke'u geçmeyen modeller atlanıyor: {dusen}", file=sys.stderr)
        if not subjects:
            raise SystemExit("smoke'u geçen model yok")

    rec = Recorder(out)
    if args.fresh and rec.runs_path.exists():
        rec.runs_path.unlink()
    kosulari_kos(subjects, defaults, args.n, rec, kosullar, progress=True)


if __name__ == "__main__":
    main()
