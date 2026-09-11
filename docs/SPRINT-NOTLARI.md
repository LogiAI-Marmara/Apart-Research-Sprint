# AI Incident Response Sprint — Arka Plan Bağlamı

> ⚠️ **Bu dosya arka plan bağlamıdır, teslim malzemesi DEĞİL.**
> Sprint'in genel düzenlemelerini ve olay özetini kayıt amaçlı tutar.
> Proje dokümantasyonu (bizim Track 1 işimiz) `kaynak-ozetleri.md` + `resources-reading-pack.md` + `proje-karar-kaydi.md`'dedir.

**Kaynak:** Apart Research e-postası (11 Eyl 2026 14:30 TRT) + sprint sayfası
**Sprint sayfası:** https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13
**Tarih:** 11–13 Eylül 2026 (Cuma–Pazar), online + in-person
**Teslim son tarih:** Pazar 13 Eylül, 23:59 AoE (Anywhere on Earth = UTC-12 → TSİ ile Pazartesi 14 Eylül 14:59)

---

## Olay ne? (sprintin konusu)

Temmuz 2026'da OpenAI ajanları test sandbox'ından kaçıp Hugging Face'in production sistemlerine
otonom şekilde sızdı.

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

## Seçtiğimiz Track: 1 — Containment

Modeller sandbox'ın izin verdiği **tek** network egress'inden kaçtı.
Görev: 3. tarafın **lab network erişimi olmadan** doğrulayabileceği, aynı zamanda lab'ların
gerçekten benimseyeceği containment standardı üretmek.
Değerlendirme: 3. taraf doğrulanabilirliği + lab'ın benimseyebilirliği.

*(Diğer 4 track için bkz. sprint sayfası.)*

---

## Teslim şartları

Özet olarak — **kanonik ve tam liste** `kaynak-ozetleri.md` §7 ("Teslim Gereksinimleri")'ndedir.

- Resmî şablon PDF, **max 8 sayfa** (ref + ekler hariç), abstract ≤ 150 kelime.
- Zorunlu: Limitations and Dual-Use Considerations eki.
- Zorunlu: artifact (linkli repo veya ek).
- Opsiyonel: public repo, 3–5 dk video.

---

## Linkler

| Ne | Link |
|----|------|
| Sprint sayfası | https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13 |
| Discord | https://discord.gg/ssZDasNkSE |
| HF teknik timeline | https://huggingface.co/blog/agent-intrusion-technical-timeline |
| OpenAI açıklaması | https://openai.com/index/hugging-face-model-evaluation-security-incident/ |