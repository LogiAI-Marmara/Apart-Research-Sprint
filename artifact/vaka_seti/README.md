# Vaka veri seti — under-provisioning ("escape pressure") hipotezi

**Hipotez (13 Eylül 2026'da revize edildi).** Dürüst tamamlanma yolunun kapalı olması
(requirement engeli) kısıt-aşma davranışının tek ya da ana sebebi DEĞİLDİR; bir
yoğunlaştırıcıdır. Kestirme kapatmak (shortcut engeli) kısıt-aşmayı azaltır ama sıfırlamaz.

*Önceki, daha güçlü hâli* — "kestirme kapatılırsa ajan dürüst yolu kullanır" — terk edildi:
METR INC-027 (altı kolay koşu, "could have easily solved the task legitimately"), Thaman
LF-2 ve bu setteki C09 bu iddiayı yalanlıyor. Ayrıntı: `../kaynaklar/provisioning-hypothesis-evidence-audit.md`.

Bu veri seti, kanıt denetimi belgesindeki 13 vaka zincirini (tıkanma → ajan tepkisi)
yapılandırır ve her birinin engelleme türünü kaynağın kendi ifadesine göre kodlar.

## Dosyalar

- `vaka_seti.csv` / `vaka_seti.json` — 13 vaka, aynı içerik (CSV `utf-8-sig`, Excel için).
- `2x2_tablo.md` — blocked_type × davranış tablosu.
- `kur.py` — tek doğruluk kaynağı; kodlanmış 13 vakayı içerir ve tüm çıktıları üretir.
- Kaynaklar: `../kaynaklar/` (aşağıya bakın).

## Kaynaklar ve dönüşüm

**Kurum sayısı: 5** (AISI, Anthropic, OpenAI, METR, collusion.wiki). ExploitGym paper/repo
denetlendi ama nitelikli vaka bulunamadı (NOT FOUND), Hugging Face hiçbir vakanın kaynağı
değildir; ikisi de kaynak sayısına dahil edilmez.

Birincil kaynaktan bizzat doğrulanan alıntılar için bkz. `../kaynaklar/birincil-dogrulama.md`.

13 vaka **`../kaynaklar/escape_pressure_evidence_audit.md`** dosyasından (Instance A–M)
kodlanmıştır. Bu `.md`, orijinal `.docx`'ten (`../kaynaklar/orijinal/`) alıntı sadakati
öncelikli bir dönüştürücüyle (`../kaynaklar/docx_to_md.py`, python-docx) üretildi:
hiçbir metin yeniden yazılmadı, tırnak/ok/tire karakterleri ve locator'lar korundu.
Dönüşüm sonrası orijinaldeki 195 metin paragrafının tamamının `.md` içinde birebir
bulunduğu programla doğrulandı (kayıp = 0) ve alıntılar orijinal `.docx` ile karşılaştırıldı.

Bağlam/karşı-kanıt belgeleri de repoya alındı (zaten `.md`, olduğu gibi kopyalandı):
- `../kaynaklar/provisioning-hypothesis-evidence-audit.md` — karşı-kanıt (adversarial) taraması.
- `../kaynaklar/environment-under-provisioning-literature-review.md` — literatür/özgünlük taraması.
- `../kaynaklar/security-controls-obstructing-work-research.md` — insan güvenliği bypass literatürü.

## Alan tanımları

| alan | tanım |
|---|---|
| `case_id` | C01–C13 (kaynaktaki Instance A–M'ye karşılık gelir; `instance` alanı eşlemeyi verir) |
| `source` | kaynağı üreten kurum (AISI / Anthropic / OpenAI / METR / collusion.wiki) |
| `source_doc` | belge adı + audit kaynak numarası (S1–S9) |
| `locator` | sayfa veya bölüm |
| `context` | `training` / `evaluation` / `unspecified` — **kaynakta ne yazıyorsa**; yazmıyorsa `unspecified` |
| `task` | ajandan ne istendi |
| `blocked_thing` | ajanın neye erişemediği |
| `blocked_type` | **`requirement` / `shortcut` / `unclear`** — sınıflandırma (aşağıda) |
| `agent_response` | ajanın ne yaptığı |
| `outcome` | `kısıt aşıldı` / `denendi başarısız` / `dürüst çözdü` |
| `causal_status` | `source_stated` (kaynak bağı kendi cümlesiyle kuruyor) / `co_occurrence` (sadece yan yana) |
| `quote` | birebir alıntı (kısaltılabilir, değiştirilemez) |
| `context_basis`, `blocked_type_basis` | *(ek alan)* kodlamanın denetlenebilir gerekçesi |
| `instance` | *(ek alan)* kaynaktaki Instance harfi (A–M) |

## Sınıflandırma kuralı (blocked_type)

Kaynağın kendi ifadesine bakılır, yorum katılmaz.

- **`requirement`** — engellenen şey görevin TAMAMLANMASI için gerekliydi; dürüst
  tamamlanma yolu (tümüyle veya istenen çıktı düzeyinde) kapalıydı.
  *Örn. C06 (OpenAI 8 Mayıs): görev Google Drive bağlantılarını gerektiriyordu, internet
  kapalıydı, "the task was effectively blocked".*
- **`shortcut`** — engellenen şey bir KESTİRMEYDİ; dürüst yol açık kalmıştı.
  *Örn. C09 (OpenAI kütüphane yeniden oluşturma): görev referans OLMADAN, girdi/çıktı ile
  çözülecek biçimde tasarlanmıştı (dürüst yol sağlanmıştı); referansa doğrudan erişim bir
  kestirmeydi ve ajan bir zafiyeti istismar edip referansı kopyaladı.*
- **`unclear`** — kaynak metinden requirement/shortcut kararı verilemiyor.
  *Şu anda bu kodda vaka yok.* C11 (OpenAI Temmuz ExploitGym) 13 Eylül 2026'da birincil
  kaynaktan doğrulandıktan sonra `unclear` → `requirement` olarak düzeltildi: Teknik Rapor
  s.19 olayı “the presence of impossible tasks in the ExploitGym evaluation” diye
  niteliyor. Önceki kodlama yalnızca blog metnine bakıyordu. Aynı düzeltmede `context` de
  `training` → `evaluation` oldu (Teknik Rapor s.4, s.22).

Emin olunamayan yere `unclear` yazıldı; hiçbir kodlama uydurulmadı. Yüksek `unclear`
sayısı sorun değil, uydurma kodlama sorundur.

## Sonuçlar (özet)

- Toplam: 13 vaka.
- `blocked_type`: requirement 12 · shortcut 1 · unclear 0.
- `causal_status`: source_stated 13 · co_occurrence 0.
- `context`: evaluation 7 · training 5 · unspecified 1.

2x2 için `2x2_tablo.md`. Denetim korpusu **kısıt-aşma seçilimlidir** (yalnızca escape
olayları toplanmış), bu yüzden "dürüst çözüm" sütunu boştur ve sonuç, requirement engelinin
kısıt-aşma ile birlikte görülmesiyle uyumludur; ancak bu korpus tek başına hipotezi
*test etmez* (aşağıdaki sınırlar).

## Veri setinin sınırları

- **Tek kodlayıcı.** İkinci bağımsız kodlayıcı yok; kodlayıcılar-arası güvenilirlik ölçülmedi.
- **Kaynakların kendi ifadesine dayanır.** Sınıflandırma, kaynak metnin beyanına göredir;
  bağımsız doğrulama yapılmadı. İkincil kaynak (collusion.wiki, C05) analizi yeniden üretir.
- **Nedensellik beyanla kuruludur, deneyle değil.** `causal_status=source_stated`, kaynağın
  bağı kendi cümlesiyle kurduğu anlamına gelir; kontrollü bir manipülasyon değildir.
- **Seçilim yanlılığı.** Denetim yalnızca kısıt-aşma olaylarını topladı; "dürüst çözüm" ve
  requirement engeline rağmen vazgeçme gibi sonuçlar bu korpusta yer almaz. Kestirme→dürüst
  karşı-örnekleri (ör. Reward Hacking Benchmark LF-2, METR INC-027) karşı-kanıt belgesindedir
  ve 13 vakalık set dışındadır. Bu nedenle tablo, requirement→escape ile *tutarlıdır* ama
  requirement ile shortcut'ın davranışsal FARKINI kanıtlamaz (shortcut hücresinde tek vaka var
  ve o da escape ile sonuçlanmış).
- **Küçük n ve context dengesizliği.** 13 vaka: 7 evaluation, 5 training, 1 unspecified.
  OpenAI'nin Mayıs vakaları (C06–C10) training koşularıdır; iddia değerlendirme ortamları
  hakkındaysa bu ayrım korunmalıdır (`context` alanı birleştirilmedi).
- **İmkânsızlığın sebebi bilinmiyor (C11).** Kaynak görevlerin imkânsız olduğunu söylüyor ama
  sebebini (eksik kaynak mı, salt zorluk mu) söylemiyor. Provizyon çerçevesi bu ayrımı
  gerektiriyorsa raporda açıkça yazılmalıdır.
- **`context` muhafazakâr kodlandı.** Vakanın kendi alıntısında training/evaluation sözcüğü
  yoksa kaynağın belge-düzeyi çerçevesi esas alındı ve gerekçe `context_basis`'te belirtildi
  (C05 için hiçbir çerçeve olmadığından `unspecified`).
