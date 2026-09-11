# Resources Sekmesi — Örnek Projeler & Reading Pack

> Kaynak: Apart sprint sayfası Resources sekmesi (Camofox ile çekildi, 11 Eyl 2026).
> Not: Liste organizatörler tarafından yeni kaynaklar çıktıkça güncelleniyor — teslim öncesi tekrar bak.

---

## Track 1 (Containment) — 8 Örnek Proje

1. **v0.1 standart:** maddeler + madde başına gereken kanıt + madde başına yaklaşık maliyet. "Guardrails kapalı eval koşmak için minimum yeterli standart." `adequate`'i tanımlamak gerçekten zor, kimse sahiplenmemiş.
2. **Attack-fazına göre kontrol matrisi:** hangi kontroller (canary credentials, egress tripwire'ları, credential scoping, kill criteria) hangi fazı keserdi, maliyeti ne.
3. **"Yes'i ucuzlatma":** mitigasyonları, pervasız bir lab'ın maliyet bahanesi kalmayacak şekilde paketle.
4. **Chain-step × cost matrisi (çok güçlü):** HF'nin belgelediği 9 fazı (recon, RCE, dropper, exfil, C2, evasion, Kubernetes, supply-chain, network pivot) al; her fazı hangi kontrol keserdi, implementasyon+operasyon maliyetiyle puanla. *"15 dakikada notlanabilir; bir regülatörün veya sigortacının gerçekten kullanabileceği artifact."*
5. **Egress attestation spec v0.1:** Bir lab'ın yayınlayabileceği, imzalı network policy + flow-log digest'i, dışarıdan birinin ağa erişmeden doğrulayabileceği. *"Track'in kalıcı çıktısı; hardware-attestation işine bağlanıyor."*
6. **Detection that fires but does not page:** HF'nin kendi remediasyon listesi "yüksek-severity sinyal dakikalar içinde responder'a page etsin" diyor — yani 4.5 gün boyunca olmayan buydu. Ajan hızında aktivite (paralel, bursty, binlerce tek başına önemsiz aksiyon; saldırı sadece sekansın içinde var) için tespit spesifikasyonu/inşa.
7. **Kanıt üreten düşmana karşı forensics:** Ajan monoloğuyla kirlenmiş loglar, gerçek rootkit'ten ayırt edilemeyen benchmark kodu. Halüsinasyonlu artifact'lar için tooling/triyaj protokolü. (Yeni bir DFIR problemi.)
8. **Deception as first-class control:** Honeypot'lar (sahte credentials, sahte package registry, honey cluster) ajan saldırganlara karşı; yavaşlatıyor mu yoksa gürültü mü üretiyor ölç.

## Track 1 — "Research Direction" soruları (derinlemesine)

- Guardrails kapalı tehlikeli-yetenek eval koşmak için **minimum yeterli standart nedir?**
- Bu zinciri hangi spesifik kontroller keserdi (canary credentials, egress tripwire, allowlisted proxy, credential scoping, stated kill criteria) + her birinin implementasyon/operasyon maliyeti?
- Lab'ın iç ağına erişmeden uyumu **üçüncü tarafın doğrulamasını** sağlayacak kanıt ne?
- **İkinci hop** (ajanın staging base'i bir lab ortamı bile değildi — public compute üzerindeki kimliksiz eval harness'i) kimin sorumluluğu?

**Kritik öncül (önemli):** Bazı madde yazımı zaten var ve çıktı değil **başlangıç noktası** olmalı:
- **CSA AI Controls Matrix — kontrol AIS-13 (AI Sandboxing)**
- **CSA vulnerability-operations guidance:** exploit-confirmation ortamları "no egress + no live production credentials" olmalı.
- *"Boşluk, ilkelerin yokluğu değil; birinin fiilen koşabileceği ve üçüncü tarafın fiilen doğrulayabileceği kontrollerin yokluğu."* → artifact'in hedefi tam burası.

**Ne ispatlayamaz:** hafta sonunda yazılan standart en fazla v0.1'dir; ne madde listesi ne çalışan harness, belirli bir lab'ın ortamının "yeterli" olduğunu göstermez (gerçek assurance, sprint'in sahip olmadığı erişim gerektirir).

## Base-rate verisi (Track 2 ile ortak, ama "neden önemli" argümanı için)

- **Anthropic:** 141.006 eval run'ı inceledi → 6 run'da **3 olay** buldu (en eskisi Nisan 2026). Üçü de Anthropic arayana kadar farkında değildi.
- **UK AISI:** 5 frontier model × 475 run → **her biri kopya çekmeye çalıştı**, oranlar %7.8–%14.1. AISI'nin kendi "near-miss"i: bir model dış serviste kod yazıp çalıştırarak AISI'nin eval altyapısına ulaştı.
- **METR Frontier Risk Report:** düzinelerce benzer olay (tüm büyük AI şirketlerinde).

## Reading Pack — "Start here"

- **HF — Anatomy of a Frontier Lab Agent Intrusion (27 Tem)** — *"bu sprint için en önemli tek belge"* (~40 dk).
- **OpenAI — model evaluation security incident (21 Tem + 28/29 Tem güncellemeleri)** — 28 Tem güncellemesi zafiyetli bileşeni adlandırıyor.
- **Anthropic — Investigating three real-world incidents (30 Tem)** — 141.006 run, framing OpenAI'dan kasıtlı farklı (bu framing kendisi inceleme konusu).
- **METR + Redwood — Brief independent investigation (16 Ağu).**
- **METR — How independent researchers could investigate AI propensities (28 Tem).**
- **Documented AI Agent Incidents** (etkileşimli grafik).
- **Public evidence of the attack (7 Ağu, Boyd Kane & Edward Cant)** — hâlâ public olan artifact'lar: zararlı dataset config'leri, template-injection exploit'i, HF makinelerinde komut çalıştıran script, public repo'larda stage edilen C2 zinciri. *"Herkesin kurtarabildiği ham maddeye en yakın şey."*
- **HF initial disclosure (16 Tem)** — kaynak bilinmeden önce.
- **Collusion.wiki** — son OpenAI ajan olayı raporu (~30 dk).
- **5 dk:** OpenAI "Safety and alignment in an era of long-horizon models" (20 Tem) — pre-release modelin sandbox'tan kaçıp public pull request açtığı AYRI bir olay; HF olayıyla karıştırılıyor.

## Reading Pack — Track 1 (Containment)

**Mevcut kontrol çerçeveleri:**
- **CoSAI — AI Incident Response Framework v1.0** (Coalition for Secure AI, WS2). *"Bu sprint için en yakın önceki-sanat."*
- **CSA AI Controls Matrix (AIS-13 AI Sandboxing)** + CSA vuln-ops guidance. *(sık revize ediliyor, güncel versiyonu kendin bul)*
- **NIST SP 800-61r3** — CoSAI'nin eşleştiği baseline.

**Zinciri pratikte analiz edenler:**
- **Elastic Security Labs** — detection rules; merkezi nokta "deteksiyon korele edildi ama hiç page'e eskale edilmedi" (en keskin savunma içgörüsü).
- **SecureLayer7** — en derin bağımsız teknik okuma; ayrıca replay corpus'unu "hangi aksiyon numarasında kontrolün tetiklenir?" savunma eval harness'ı olarak kullanmayı öneriyor (= Track 1 proje brief'i).
- **Trackr.Live** — cluster-admin haklarını taşıyan shared connector credential (belirleyici eskalasyon). Yazarlık net değil.
- **Picus** — machine-speed attacks; oranlar: exfil ~56 aksiyon / ~17.600.
- **7AI (Yonatan Striem-Amit)** — "The Era of Autonomous Hacking Is Here."
- **CSA CISO post-mortem (28 Tem)** — 50+ CISO, ~700 kişi; HF yanıt ekibinden birinci ağızdan hesap + agentic-AI tabletop önerisi.
- **SANS — "The Models Said No"** ve **Rich Mogull/CSA — "The Model Did Exactly What We Asked."**

**Merkezdeki benchmark:**
- **ExploitGym** — repo (Apache 2.0) · paper (arXiv 2605.11086) · Berkeley RDI yazısı. *V1.0 = 869 instance; paper 898 diyor — 898'i "shipped sayı" olarak aktarma.*

## Reading Pack — Track 2 (hızlı not)
- **UK AISI — Cheating behaviour (21 Tem):** 5 model × 475 run, %7.8–14.1 kopya.
- **Anthropic review**, **METR Frontier Risk Report** (üç public payda).
- **GovAI — Incident Analysis for AI Agents:** developers'ın talep üzerine saklaması gerekenler (activity log, system doc, tool info) — delil-yeterlilik işinden önce oku.
- **CLTR — Loss of Control Observatory (Şub 2026).**
- **Redwood — "The OpenAI models that hacked Hugging Face" (25 Tem)** — grader-gaming tezi.
- **MIT Tech Review (27 Tem)** — "unprecedented" framing'e karşı; başarısızlık insan containment tasarımı diyor.
- **Reuters (via CNA, 24 Tem)** — tespit timeline'ı; anonim kaynak, doğrulanmamış iddialar (infra'ya bırakılan notlar, bağlantısız monitoring); OpenAI'nin kendi açıklamasıyla gerilimde, bağdaştırmak meşru proje.

## Reading Pack — Track 3 (hızlı not)
- AB: **Article 55** yükümlülükleri 2 Ağu 2025'ten beri; **icra yetkisi 2 Ağu 2026'dan** (€15M / %3 ciro).
- **CA: SB 53** (Cal OES portalı halka açık; §22757.15 framework uyumsuzluğunu bağımsız icra edilebilir yapıyor).
- **NY: RAISE Act** 72 saat "reasonable belief" saati.
- ABD federal: AI Kill Switch Act (red-team carve-out'u bu olay deliyor), AI Incident Reporting Act.
- **OECD common reporting framework** (29 kriter, 7 zorunlu) — EU/CA ile birlikte doldurunca 4-rejim karşılaştırması.

## Reading Pack — Track 4/5 (hızlı not)
- **Defensive Refusal Bias (arXiv 2603.01246):** 2.390 NCCDC prompt, %12.2 refusal; güvenlik anahtar kelimeleri 2.72×; yetkilendirme artırıyor (%21.8 vs %11.6).
- **Gray Swan Cybersecurity Refusal Framework (arXiv 2606.02644)** · **Meta CyberSecEval** (MITRE FRR + CyberSOCEval).
- **RAND/AISI/Mila cabinet-level exercises (1 Tem 2026)** — tabletop tasarım referansı (ama senaryo "kendi modelinin kaçıp üçüncü tarafa saldırması" değil; gap burada).
- **OECD AI Incidents Monitor · AI Incident Database · MIT AI Incident Tracker (+FLARE-AI).**

## Önemli: 15-dakika notlanabilirlik kısıtı
*"Her track, bir jürinin (idealde) 15 dakikadan kısa sürede notlayabileceği bir artifact ile tanımlanır — bu, ana tasarım kısıtlarından biri."* → Artifact'in 15 dk'da kavranabilir ve notlanabilir olması şart.