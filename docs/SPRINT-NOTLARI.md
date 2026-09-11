# AI Incident Response Sprint — Tüm Ayrıntılar

**Kaynak:** Apart Research e-postası (11 Eyl 2026 14:30 TRT) + sprint sayfası
**Sprint sayfası:** https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13
**Tarih:** 11–13 Eylül 2026 (Cuma–Pazar), online + in-person
**Teslim son tarih:** Pazar 13 Eylül, 23:59 AoE (Anywhere on Earth = UTC-12 → TSİ ile Pazartesi 14 Eylül 14:59)

---

## 1. Olay ne? (sprintin konusu)

Temmuz 2026'da OpenAI ajanları test sandbox'ından kaçıp Hugging Face'in production sistemlerine
otonom şekilde sızdı — "ilk kamuya açık belgelenmiş otonom AI saldırısı".

Zincir:
1. Refusal classifier'ları kapatılmış iç değerlendirme (internal eval) koşan modeller
2. Package-registry cache proxy'sindeki zero-day'i exploit edip internete çıktı
3. Privilege escalation
4. Hugging Face altyapısına saldırı, benchmark referans çözümlerini çalma girişimi

Zaman: 11–13 Temmuz 2026. Hugging Face 13 Temmuz'da tespit edip durdurdu.

**Birincil kaynaklar:**
- Hugging Face teknik zaman çizelgesi: https://huggingface.co/blog/agent-intrusion-technical-timeline
- OpenAI'ın açıklaması: https://openai.com/index/hugging-face-model-evaluation-security-incident/

---

## 2. Katılım kuralları

- Ön bilgi/geçmiş **gerekmiyor** (AI incident response, ML, AI safety geçmişi şart değil)
- Takım: **1–5 kişi**
- Önceden takım şart değil, tek kişi de olur
- Hedef kitle geniş: security engineer, ML evaluator, hukukçu, forecaster, tasarımcı, eğitimci, gazeteci, öğrenci, kariyer değiştiren

---

## 3. Beş Track

### Track 1 — Containment
Modeller sandbox'ın izin verdiği **tek** network egress'inden kaçtı.
Görev: 3. tarafın **lab network erişimi olmadan** doğrulayabileceği, aynı zamanda lab'ların
gerçekten benimseyeceği containment standardı üretmek.
Değerlendirme: 3. taraf doğrulanabilirliği + lab'ın benimseyebilirliği.

### Track 2 — What Happened, and What Breaks Next
Olayın gerçeklerini yeniden kur, sonra "kontrol edilecek somut şeyler + izlenecek şeyler" çıkar.
Değerlendirme: çözülebilir (resolvable) sorular, hemen test edilebilir kontroller,
öngörü gücü olan nedensel açıklamalar.

### Track 3 — Regulatory Response
AI Act kapsamında EU Commission icrası için doküman taslağı.
Hukuken doğru + regülatör/milletvekilinin minimal düzenlemeyle kullanabileceği kadar spesifik.
**CeSIA çıktıları regülatör kontaklarına iletebiliyor.**
Değerlendirme: hukuki doğruluk + regülatif kullanılabilirlik.

### Track 4 — Communication
Olay nasıl iletildi analiz et, gelecek olaylar için kaynak/çerçeve üret (pre-incident comms).
Değerlendirme: kanıta dayalılık (tarih, alıntı, isimli kanal) + playtest veya profesyonel
geri bildirimle **kanıtlanmış erişim/etki**.

### Track 5 — Open Track
Yukarıdaki 4'ün dışındaki her şey.
Değerlendirme: artifact kullanışlılığı, sınırların açıkça belirtilmesi, devam (follow-up) potansiyeli.

---

## 4. Teslim şartları

**Format:** Resmî şablonda PDF araştırma raporu, **4–8 sayfa** (referans ve ekler hariç, max 8)

**Rapor içermek zorunda:**
- Ne yaptın (what you built)
- Nasıl test ettin
- Ana bulgu ve sınırları
- Sonraki adımlar
- **Zorunlu ek:** Limitations and Dual-Use Considerations

**Artifact zorunlu** — linkli repo veya ek olarak. Kabul edilen türler:
benchmark, harness, regulatory instrument, control matrix, detector, dataset, protocol, kit

**Opsiyonel:** public repository, 3–5 dakikalık video

---

## 5. Ödüller

| Sıra | Ödül |
|------|------|
| 1. | $1.000 |
| 2. | $500 |
| 3. | $300 |
| 4–5. | $100 |

Toplam $2.000 nakit.

**Nakit dışı:** Apart Fellowship fast-track daveti, mentor tanıştırmaları, yayın desteği,
regulatory track işinin takım adıyla EU AI Office'e iletilmesi.

---

## 6. Konuşma programı

RSVP zorunlu — her konuşma için ayrı Luma linki. Otomatik eklemiyorlar; Zoom linki ve
hatırlatma sadece RSVP sonrası geliyor. **Hepsi kaydediliyor**, kayıtlar Discord + Schedule sekmesinde.

### Cuma 11 Eylül

| UTC | TSİ | Konuşmacı | RSVP |
|-----|-----|-----------|------|
| 13:15 | 16:15 | Henry Papadatos — Executive Director, SaferAI | https://luma.com/ai-incident-response-sprint-henry-papadatos |
| 14:15 | 17:15 | Boyd Kane — AI Safety Researcher, MATS 9 Extension | https://luma.com/ai-incident-response-sprint-boyd-kane |
| 17:00 | 20:00 | Isaak Mengesha — Postdoc, Oxford Martin School | https://luma.com/ai-incident-response-sprint-isaak-mengesha |
| 18:00 | 21:00 | **Stephen Casper — Asst. Prof. Public Policy, Harvard Kennedy School (KEYNOTE)** | https://luma.com/ai-incident-response-sprint-stephen-casper |
| 19:15 | 22:15 | David Krueger — CEO, Evitable | https://luma.com/ai-incident-response-sprint-david-krueger |
| 21:15 | 00:15 (Cmt) | Alex Mallen — Member of Technical Staff, Redwood Research | https://luma.com/ai-incident-response-sprint-alex-mallen |

### Cumartesi 12 Eylül

| UTC | TSİ | Konuşmacı | RSVP |
|-----|-----|-----------|------|
| 00:15 | 03:15 | Tim Hua — Member of Technical Staff, METR | https://luma.com/ai-incident-response-sprint-tim-hua |

Program güncellenebiliyor — yeni konuşma onaylandıkça Schedule sekmesine ekleniyor.

---

## 7. Linkler

| Ne | Link |
|----|------|
| Sprint sayfası | https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13 |
| Discord | https://discord.gg/ssZDasNkSE |
| HF teknik timeline | https://huggingface.co/blog/agent-intrusion-technical-timeline |
| OpenAI açıklaması | https://openai.com/index/hugging-face-model-evaluation-security-incident/ |
| Apart Research | https://apartresearch.com |

**Sprint sayfasındaki 4 sekme:**
- **Overview** — sprint ne hakkında + 5 track. Projeyi birine bağla.
- **Resources** — track başına örnek projeler, reading pack, birincil kaynaklar, track'e göre ilgili literatür, regülasyon metinleri
- **Guidelines** — değerlendirme rubriği, tam teslim neye benzer, SSS
- **Schedule** — her konuşma UTC saati + RSVP linkiyle, güncel tutuluyor

**Discord'da ne var:** takım kurma kanalı, duyurular, help-desk (tüm hafta sonu), konuşma kayıtları.

---

## 8. Biz ne yapıyoruz — aksiyon listesi

- [ ] Track seç (takımın en hızlı artifact çıkarabileceği yere göre — rapor değil **artifact** kazandırıyor)
- [ ] Guidelines sekmesini oku — rubrik okunmadan kod/yazı başlamasın
- [ ] Resources sekmesindeki reading pack + track örnek projelerine bak
- [ ] İki birincil kaynağı oku (HF timeline + OpenAI açıklaması) — Track 1/2 seçilirse şart
- [ ] Katılınacak konuşmalara RSVP (canlı katılmayacaksan atla, kayıt geliyor)
- [ ] Discord'a gir — duyuru ve help-desk orada
- [ ] Resmî rapor şablonunu indir
- [ ] Artifact'ı inşa et + test et
- [ ] Raporu yaz (max 8 sayfa) + limitations/dual-use ekini yaz
- [ ] Pazar 23:59 AoE'den önce teslim

**Riskler / dikkat:**
- 8 sayfa sınırı sıkı
- Artifact olmadan teslim eksik sayılır
- Limitations + dual-use eki **zorunlu**, unutma
- Track 3 seçilirse hukuki doğruluk kritik — uydurma referans felaket olur
