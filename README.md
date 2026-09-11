# AI Incident Response Sprint — Proje Dizini

> Apart Research (CeSIA) organizasyonu — 11–13 Eylül 2026 (online + in-person)

## Tek Satırda

Temmuz 2026'da OpenAI ajanlarının test sandbox'ından kaçıp Hugging Face production
sistemlerine otonom sızmasına ("ilk kamuya açık belgelenmiş otonom AI saldırısı") yönelik
bir incident-response sprint'i. Çıktı: **4–8 sayfa PDF rapor + zorunlu artifact**.

## Kritik Bilgiler

| Alan | Değer |
|------|-------|
| Tarih | 11–13 Eylül 2026 (Cuma–Pazar) |
| Teslim | Pazar 13 Eylül 23:59 AoE → **TSİ Pazartesi 14 Eylül 14:59** |
| Takım | 1–5 kişi (ön bilgi/geçmiş şart değil) |
| Format | Resmî şablon PDF, 4–8 sayfa (max 8, ref+ekler hariç) |
| Zorunlu ek | Limitations and Dual-Use Considerations |
| Artifact | Zorunlu (linkli repo veya ek): benchmark, harness, control matrix, detector, dataset, protocol, kit |
| Ödül | 1. $1.000 / 2. $500 / 3. $300 / 4–5. $100 |

## 5 Track

1. **Containment** — sandbox'tan kaçışı önleyen, 3. tarafça doğrulanabilir + lab'ların benimseyeceği containment standardı.
2. **What Happened, and What Breaks Next** — olayı yeniden kur, "kontrol edilecek somut şeyler + izlenecek şeyler" çıkar.
3. **Regulatory Response** — AI Act kapsamında EU Commission icrası için doküman taslağı (CeSIA, regülatörlere iletme imkânı sunuyor).
4. **Communication** — olayın nasıl iletildiğini analiz et, pre-incident comms çerçevesi üret.
5. **Open Track** — yukarıdakilerin dışında her şey.

## Dizin Yapısı

```
ai-incident-response/
├── README.md                # Bu dosya (hızlı özet + index)
├── LICENSE
├── docs/                    # İç çalışma belgeleri: sprint notları, karar kaydı, kaynak özetleri
│   ├── SPRINT-NOTLARI.md    # E-postadan çıkarılmış tüm ayrıntılar
│   ├── proje-karar-kaydi.md # Track/artifact/takım kararları + aksiyon listesi
│   ├── kaynak-ozetleri.md   # Birincil kaynak özetleri + rubrik (HF timeline, OpenAI)
│   └── resources-reading-pack.md  # Resources sekmesi: örnek projeler + okuma listesi
├── artifact/                # Kod ve artifact (standard/matris/harness/...)
└── report/                  # Teslim PDF + resmî şablon
```

## Önemli Linkler

- Sprint sayfası: https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13
- Discord: https://discord.gg/ssZDasNkSE
- HF teknik timeline: https://huggingface.co/blog/agent-intrusion-technical-timeline
- OpenAI açıklaması: https://openai.com/index/hugging-face-model-evaluation-security-incident/