# AI Incident Response Sprint — Track 1: Containment

> Apart Research × CeSIA "AI Incident Response Sprint" (11–13 Eylül 2026) katılımımız.
> **Seçtiğimiz track: 1 — Containment.**

## Ne yapıyoruz

Temmuz 2026'da iki OpenAI modeli, bir iç değerlendirme sırasında test sandbox'ının
**tek izinli ağ çıkışından** (Artifactory package-registry cache proxy'si) bir zero-day
üzerinden kaçarak Hugging Face'in üretim sistemlerine otonom sızdı. Bu olay; sprint'in
konusu olan, kamuya açık belgelenmiş otonom bir AI sızıntısı.

Track 1'in sorusu şu: **bu kaçışı durduracak containment standardı neydi?** Modeller
sandbox'ın izin verdiği tek egress'ten çıktığı için, cevap bir standartta toplanıyor:

- guardrails kapalı (refusal'ları düşürülmüş) eval koşmak için **en az ne yeterli**?
- bir **üçüncü taraf**, lab'ın iç ağına erişmeden uyumu nasıl **doğrulayabilir**?
- bir lab bunu **gerçekten benimser mi**?

**Çıktımız (artifact):** [_karar verilecek — bkz. `docs/proje-karar-kaydi.md`_]
artı resmî şablonda 4–8 sayfalık rapor (`report/` altında).

> Sprint İsmail Efe ile ortak giriliyor (takım: thozoz + ism00efe).

## Teslim / Zaman Çizelgesi

| Kalem | Değer |
|-------|-------|
| Track | **1 — Containment** |
| Teslim son | Pazar 13 Eylül 23:59 AoE → TSİ Pazartesi 14 Eylül 14:59 |
| Format | Resmî şablon PDF, max 8 sayfa (ref+ekler hariç) |
| Zorunlu ek | Limitations and Dual-Use Considerations |
| Artifact | Zorunlu (`artifact/`) — standard / control matrix / spec / kit |
| Değerlendirme | Üçüncü taraf doğrulanabilirliği + lab'ın benimseme ihtimali |

## Dizin Yapısı

```
├── README.md                # Bu dosya: ne yapıyoruz + nasıl doğrulanır
├── LICENSE
├── docs/                    # İç çalışma belgeleri (kaynak özetleri, kararlar)
│   ├── SPRINT-NOTLARI.md         # Sprint düzenlemeleri + teslim şartları
│   ├── proje-karar-kaydi.md      # Track/artifact/takım kararları + aksiyon
│   ├── kaynak-ozetleri.md        # HF timeline + OpenAI + rubrik özeti
│   └── resources-reading-pack.md # Track 1 örnek projeleri + okuma listesi
├── artifact/                # Ürün: standard/matris/spec + kod
└── report/                  # Resmî şablon PDF (teslim)
```

## Birincil Kaynaklar (çalışma zemini)

- HF teknik zaman çizelgesi: https://huggingface.co/blog/agent-intrusion-technical-timeline
- OpenAI açıklaması: https://openai.com/index/hugging-face-model-evaluation-security-incident/
- Sprint sayfası: https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13