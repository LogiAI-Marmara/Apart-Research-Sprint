# -*- coding: utf-8 -*-
"""Vaka veri setini kur: 13 vaka zinciri -> CSV + JSON + 2x2 tablo.

Tek doğruluk kaynağı aşağıdaki VAKALAR listesidir. Her satır,
kaynaklar/escape_pressure_evidence_audit.md içindeki bir vaka zincirinden
(Instance A–M) kodlanmıştır. Kodlama kaynağın kendi ifadesine dayanır; yorum
katılmaz. blocked_type için karar kuralı README'de.

    python vaka_seti/kur.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
KAYNAK_MD = "kaynaklar/escape_pressure_evidence_audit.md"

# Alan sırası (CSV başlığı ve JSON anahtar sırası).
ALANLAR = [
    "case_id", "source", "source_doc", "locator", "context", "task",
    "blocked_thing", "blocked_type", "agent_response", "outcome",
    "causal_status", "quote",
]

# context_basis ve blocked_type_basis: kodlamanın DENETLENEBİLİR gerekçesi.
# Çekirdek alanların dışında; CSV'ye de eklenir (şeffaflık için), JSON'da da yer alır.
EK_ALANLAR = ["context_basis", "blocked_type_basis", "instance"]

VAKALAR = [
    {
        "case_id": "C01", "instance": "A",
        "source": "AISI",
        "source_doc": "UK AISI — Cheating behaviour in frontier model evaluations (S2)",
        "locator": "Cheating behaviour on AISI cyber evaluations → A stand-out case",
        "context": "evaluation",
        "context_basis": "Kaynak açıkça 'cyber capability evaluation' diyor.",
        "task": "Simüle ortamda gizli bir 'flag'i (bayrak) bulmak.",
        "blocked_thing": "Görevin çözülebilirliği — değerlendirme yanlış yapılandırıldığı için imkânsızdı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Kaynak görevi 'accidentally misconfigured and therefore impossible to solve' diyor; dürüst tamamlanma yolu tümüyle kapalıydı.",
        "agent_response": "AISI altyapısına ulaşmaya çalışmak için açık internette, harici bir serviste kod yazıp çalıştırdı; güvenlik alarmı tetikledi.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“One particularly stark example of cheating behaviour occurred during a cyber capability evaluation that was accidentally misconfigured and therefore impossible to solve. The model tested was so persistent in attempting to cheat that it wrote and ran code on an external service…”",
    },
    {
        "case_id": "C02", "instance": "B",
        "source": "Anthropic",
        "source_doc": "Anthropic — Investigating three real-world incidents in our cybersecurity evaluations (S1)",
        "locator": "Incident 1, paragraph 2",
        "context": "evaluation",
        "context_basis": "Kaynak 'In four runs of this evaluation' diyor; blog üç olayı da 'cybersecurity evaluations' olarak çerçeveliyor.",
        "task": "Kurgusal hedeften bayrağı ele geçirmek (capture-the-flag).",
        "blocked_thing": "Kurgusal (simüle) hedefe erişim — ulaşmakta zorlandı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Engellenen şey görevin hedefi olan simüle makineydi; bu bir kestirme değil, tamamlanmanın gereğiydi.",
        "agent_response": "İnternet üzerinden erişilebilen GERÇEK aynı-adlı şirketi keşfedip zafiyetlerini istismar etti.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“Claude ran into difficulty reaching its simulated target within the evaluation environment, but then discovered that the real company was reachable via the internet.”",
    },
    {
        "case_id": "C03", "instance": "C",
        "source": "Anthropic",
        "source_doc": "Anthropic — Investigating three real-world incidents in our cybersecurity evaluations (S1)",
        "locator": "Incident 2, paragraphs 3–4",
        "context": "evaluation",
        "context_basis": "Blog üç olayı da 'cybersecurity evaluations' olarak çerçeveliyor; olay-2 alıntıları training/eval sözcüğü içermiyor.",
        "task": "Kurgusal ortamda bir bağımlılık-karışıklığı (dependency confusion) açığını istismar etmek (kendi paketini PyPI'ye yayımlamak).",
        "blocked_thing": "Paket yayımı için gereken hesap/telefon/e-posta ön koşulları; telefon için para gerekiyordu.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Engellenen ön koşullar seçilen saldırı yolunun (paket yayımı) tamamlanması için gerekliydi; ortada atlanan bir dürüst yol yok.",
        "agent_response": "Ön koşul workaround'ları peşinde koştu; para bulmaya çalışıp başaramadı, sonunda ücretsiz bir e-posta sağlayıcı bulup PyPI hesabı açtı ve zararlı yazılım yükledi.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“And in order to create an email address, it needed a phone number. To get a phone number, after failing to find a free phone number service, it tried—and failed—to obtain funds…”",
    },
    {
        "case_id": "C04", "instance": "D",
        "source": "Anthropic",
        "source_doc": "Anthropic — Investigating three real-world incidents in our cybersecurity evaluations (S1)",
        "locator": "Incident 3, paragraph 1",
        "context": "evaluation",
        "context_basis": "Kaynak 'In this evaluation' diyor.",
        "task": "Kurgusal capture-the-flag hedefine ulaşmak.",
        "blocked_thing": "Amaçlanan kurgusal hedefe erişim — ulaşılamadı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Engellenen şey görevin hedefiydi; kestirme değil, tamamlanmanın gereği.",
        "agent_response": "İnternette alternatif aradı, ~9.000 hedefi taradı, gerçek bir şirketin internete açık uygulamasını ele geçirdi.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“when Claude was unable to reach its intended fictional target, it looked for alternatives online, scanning roughly 9,000 targets.”",
    },
    {
        "case_id": "C05", "instance": "E",
        "source": "collusion.wiki",
        "source_doc": "collusion.wiki — Discovery of a new OpenAI agent message board (S3)",
        "locator": "The agents used the wiki to share ways around sandbox restrictions, paragraph 2",
        "context": "unspecified",
        "context_basis": "Kaynak bu alışverişi ne training ne evaluation olarak açıkça belirtmiyor.",
        "task": "Power BI panosundan bir istatistiği iki ondalık basamağa kadar almak.",
        "blocked_thing": "İkinci ondalık basamak — GET tek basamak veriyordu, POST yasaktı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Görev iki ondalık gerektiriyordu; izinli (GET) yol bunu üretemiyordu, yani dürüst yol istenen çıktıyı veremiyordu.",
        "agent_response": "Sandbox kısıtını aşmak için host-yönlendirme bypass'ı üzerinde işbirliği yapıp yöntemi wiki'ye yazdı.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“A GET request only gave answers to one decimal point, but the agents needed two. This is why they discussed and attempted workarounds.”",
    },
    {
        "case_id": "C06", "instance": "F",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5)",
        "locator": "Technical Report, printed p. 6",
        "context": "training",
        "context_basis": "Kaynak 'as part of a training run' diyor.",
        "task": "Google Drive bağlantılı materyal kullanarak bir e-tablo tamamlama görevini çözmek.",
        "blocked_thing": "İnternet erişimi kapalıydı; bağlantılı girdilere erişilemedi.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Kaynak 'the agent could not retrieve the linked materials and the task was effectively blocked' diyor; girdi görev için gerekliydi.",
        "agent_response": "İnternet erişimi elde etmek için Artifactory'ye karşı SSRF denedi.",
        "outcome": "denendi başarısız",
        "causal_status": "source_stated",
        "quote": "“Because the agent was blocked from accessing the internet, the agent could not retrieve the linked materials and the task was effectively blocked.”",
    },
    {
        "case_id": "C07", "instance": "G",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5)",
        "locator": "Technical Report, printed pp. 6–7",
        "context": "training",
        "context_basis": "Kaynak 'during another training run' diyor.",
        "task": "Bir protein-veritabanı dosyasına bağımlı bir görevi tamamlamak.",
        "blocked_thing": "Gerekli protein veritabanı dosyası erişilemezdi.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Dosya görevin bağımlı olduğu girdiydi ('depended on an inaccessible protein database file'); kestirme değil.",
        "agent_response": "Başka bir ortamdaki ajanların dosyaya erişebileceğini düşünüp Artifactory'ye ajanlar-arası bir not dosyası yazdı.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“On May 12, during another training run, an agent was given a similar task that depended on an inaccessible protein database file.”",
    },
    {
        "case_id": "C08", "instance": "H",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5)",
        "locator": "Technical Report, printed p. 7",
        "context": "training",
        "context_basis": "Kaynak 'from the same training experiment' diyor.",
        "task": "Ayrı bir ajanın aynı dosyaya ihtiyaç duyması.",
        "blocked_thing": "Dosya; birden çok arama yöntemiyle bulunamadı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Dosya görevi tamamlamak için gerekliydi ('required the same file to complete its tasks'); kestirme değil.",
        "agent_response": "Hugging Face sitesini aradı ve halka açık şekilde sızmış bir HF kullanıcı token'ını kullandı.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“After failing to find the file through public filename, digest, sequence, and source-code searches, the agent searched the Hugging Face website…”",
    },
    {
        "case_id": "C09", "instance": "I",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5)",
        "locator": "Technical Report, printed p. 20",
        "context": "training",
        "context_basis": "Teknik Rapor'un training-olayları bölümünde; audit bunu 'training task' olarak adlandırıyor. (Bu vakanın kendi alıntısı training/eval sözcüğü içermiyor.)",
        "task": "Referans programa erişmeden bir yazılım kütüphanesini yeniden oluşturmak.",
        "blocked_thing": "Referans programın kendisi; ajan yalnızca girdileri test edip çıktıları gözlemleyebiliyordu.",
        "blocked_type": "shortcut",
        "blocked_type_basis": "Görev referans OLMADAN çözülecek biçimde tasarlanmıştı ve dürüst yol (girdi/çıktı ile kara-kutu tersine mühendislik) SAĞLANMIŞTI; referansa doğrudan erişim gerek değil, bir kestirmeydi.",
        "agent_response": "Kurulumla ilgili bir zafiyeti istismar edip referans kütüphanenin bulunduğu ortama dosya yazdı, referans cevabı birebir kopyaladı.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“The agent realized that it could exploit a vulnerability in the setup to write files into the environment where the reference library was stored. This allowed it to get direct access to the underlying program it was trying to replicate.”",
    },
    {
        "case_id": "C10", "instance": "J",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5)",
        "locator": "Technical Report, printed p. 21",
        "context": "training",
        "context_basis": "Kaynak 'one agent during training was instructed' diyor.",
        "task": "Yerel bir sosyal medya sitesine, güncellenme zamanı tam olarak belirtilen bir değer olacak şekilde gönderi yapmak.",
        "blocked_thing": "Zamanı ayarlama yeteneği — sağlanan arayüzde bu işlev yoktu.",
        "blocked_type": "requirement",
        "blocked_type_basis": "İstenen tam çıktıyı üretmek için gereken yetenek sağlanan arayüzde yoktu ('did not have any functionality for setting the time'); kestirme değil.",
        "agent_response": "Ortamı geniş biçimde keşfetti, tarayıcının root ayrıcalığı olduğunu buldu, /etc/sudoers.d üzerine yazıp root oldu ve ilgili süreci değiştirdi.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“However, the interface it was provided did not have any functionality for setting the time. This caused the agent to do a broad exploration of its environment, eventually discovering that its browser had root privileges.”",
    },
    {
        "case_id": "C11", "instance": "K",
        "source": "OpenAI",
        "source_doc": "OpenAI — Hugging Face Incident: Technical Report (S5), printed pp. 19, 22; OpenAI — Hugging Face incident and the road ahead (S4); METR corroboration (S6)",
        "locator": "Reward hacking, paragraphs 3–5 / Root causes and lessons",
        "context": "evaluation",
        "context_basis": "Teknik Rapor s.4 'During these evaluations' ve s.19 'impossible tasks in the ExploitGym evaluation' diyor; s.22 'the evaluation tasks' ifadesini kullanıyor. Önceki 'training' kodlaması yalnızca bloga dayanıyordu ve Teknik Rapor tarafından düzeltilmiştir (13 Eyl 2026, birincil kaynaktan doğrulandı).",
        "task": "Zorlu ExploitGym capture-the-flag değerlendirmelerini çözmek.",
        "blocked_thing": "Değerlendirmedeki 898 görevin 198'i hiçbir OpenAI modelince çözülememişti; Teknik Rapor bunları 'impossible tasks' olarak adlandırıyor.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Teknik Rapor s.19 olayı 'the presence of impossible tasks in the ExploitGym evaluation' diye niteliyor ve s.22 çözülemeyen kümenin mesaj panosu trafiğindeki payını veriyor; kaynak hem imkânsızlığı hem nedensel katkıyı kendi cümlesiyle kuruyor. UYARI: kaynak imkânsızlığın SEBEBİNİ (eksik kaynak mı, salt zorluk mu) söylemiyor; bu ayrım provizyon çerçevesi için raporda açıkça belirtilmelidir.",
        "agent_response": "Takılan ajanlar dizin adlarına kodlayarak mesaj panosunu yeniden kurdu; zorlanan ajanlar Modal ve Hugging Face gibi üçüncü-taraf servislerde çözüm aradı.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“Despite only 22% of the evaluation tasks being unsolved, 93% of the tasks discussed on the message board came from this set.” (Technical Report, printed p. 22) · “the presence of impossible tasks in the ExploitGym evaluation” (printed p. 19) · “These unsolved tasks ended up being a substantial contributor to the Hugging Face incident.” (S4)",
    },
    {
        "case_id": "C12", "instance": "L",
        "source": "METR",
        "source_doc": "METR — Frontier AI Risk Management Framework: First Look (S7)",
        "locator": "INC-030 → Incident details / Summary",
        "context": "evaluation",
        "context_basis": "Kaynak 'discovered it was inside a METR evaluation environment' diyor.",
        "task": "Bir web uygulaması zafiyetini istismar ederek başka kullanıcının Gmail parolasını çalmak.",
        "blocked_thing": "Görev-kritik sunucu — ajan onu çökertti, amaçlanan yol imkânsızlaştı.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Kaynak 'the task became impossible through the intended path' diyor; erişilemeyen sunucu görevin gereğiydi.",
        "agent_response": "Sunucuyu kurtarmayı denedi, sonra değerlendirme altyapısını yoklayıp istismar etmeye çalıştı.",
        "outcome": "denendi başarısız",
        "causal_status": "source_stated",
        "quote": "“After the server died, the task became impossible through the intended path, and the agent spent the remaining run attempting to recover the server or escape the evaluation container.”",
    },
    {
        "case_id": "C13", "instance": "M",
        "source": "METR",
        "source_doc": "METR — Frontier AI Risk Management Framework: First Look (S7)",
        "locator": "INC-044 → Incident details",
        "context": "evaluation",
        "context_basis": "METR Frontier Risk Report değerlendirme olayı; INC-044 bir değerlendirme koşusudur. (Vakanın alıntıları 'evaluation' sözcüğünü tekrar etmiyor.)",
        "task": "Belirtilen bir API'yi (gpt-3.5-turbo-0125) kullanarak Rust'ta bir CodeContests çözücü yazmak.",
        "blocked_thing": "Verilen API hesabında kredi kalmamıştı; sağlanan anahtar kullanılamıyordu.",
        "blocked_type": "requirement",
        "blocked_type_basis": "Görev belirtilen API erişimini gerektiriyordu; sağlanan kaynak (kredili anahtar) kullanılamaz durumdaydı — kestirme değil, eksik gereklilik.",
        "agent_response": "Birden çok ücretsiz sağlayıcı denedi ve yetkisiz biçimde Pollinations'ı benimsedi.",
        "outcome": "kısıt aşıldı",
        "causal_status": "source_stated",
        "quote": "“the agent couldn’t use the API key it was given because the associated API account had run out of credit.”",
    },
]


def dogrula(vakalar: list[dict]) -> None:
    ids = [v["case_id"] for v in vakalar]
    assert len(ids) == len(set(ids)), "tekrar eden case_id"
    for v in vakalar:
        for alan in ALANLAR + EK_ALANLAR:
            assert alan in v, f"{v['case_id']}: eksik alan {alan}"
        assert v["blocked_type"] in {"requirement", "shortcut", "unclear"}, v["case_id"]
        assert v["causal_status"] in {"source_stated", "co_occurrence"}, v["case_id"]
        assert v["context"] in {"training", "evaluation", "unspecified"}, v["case_id"]


def yaz_csv(vakalar: list[dict], path: Path) -> None:
    basliklar = ALANLAR + EK_ALANLAR
    with path.open("w", encoding="utf-8-sig", newline="") as f:  # utf-8-sig: Excel Türkçe uyumu
        # lineterminator="\n": csv varsayılanı \r\n'dir ve her çalıştırmada sahte
        # git diff üretirdi (repodaki dosya LF). Bkz. kök .gitattributes.
        w = csv.DictWriter(f, fieldnames=basliklar, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for v in vakalar:
            w.writerow(v)


def yaz_json(vakalar: list[dict], path: Path) -> None:
    kayit = {
        "aciklama": "Under-provisioning ('escape pressure') hipotezi için vaka veri seti — 13 vaka zinciri.",
        "kaynak_belge": KAYNAK_MD,
        "vaka_sayisi": len(vakalar),
        "alan_sirasi": ALANLAR,
        "vakalar": [{k: v[k] for k in ALANLAR + EK_ALANLAR} for v in vakalar],
    }
    # newline="": text mode'da \n -> os.linesep (Windows'ta \r\n) çevrilmesini engeller.
    # Aksi halde üreteç Windows'ta CRLF yazıp CSV'deki sahte diff'in eşini üretirdi.
    # (Not: newline="\n" de dokümante edilmiş eşdeğeridir; "" daha yaygın okunuyor.)
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(kayit, ensure_ascii=False, indent=2))


def yaz_2x2(vakalar: list[dict], path: Path) -> str:
    # Sütun: kısıt aşma denemesi (dürüst çözüm dışındaki her outcome) vs dürüst çözüm.
    def denedi(v):
        return v["outcome"] != "dürüst çözdü"

    def hucre(btype, deneme):
        ids = [v["case_id"] for v in vakalar
               if v["blocked_type"] == btype and (denedi(v) == deneme)]
        return ids

    satirlar = []
    satirlar.append("# 2x2 Tablo — blocked_type × ajan davranışı\n")
    satirlar.append("| | kısıt aşma denemesi | dürüst çözüm |")
    satirlar.append("|---|---|---|")
    for btype in ("requirement", "shortcut"):
        a = hucre(btype, True)
        d = hucre(btype, False)
        satirlar.append(
            f"| **{btype}** | {len(a)} — {', '.join(a) or '—'} | {len(d)} — {', '.join(d) or '—'} |"
        )
    # unclear satırı 2x2 dışında ama şeffaflık için ayrı raporlanır.
    unclear = [v["case_id"] for v in vakalar if v["blocked_type"] == "unclear"]
    ss = [v["case_id"] for v in vakalar if v["causal_status"] == "source_stated"]
    co = [v["case_id"] for v in vakalar if v["causal_status"] == "co_occurrence"]
    satirlar.append("")
    satirlar.append(f"- **unclear** (2x2 dışı): {len(unclear)} — {', '.join(unclear) or '—'}")
    satirlar.append(f"- **source_stated**: {len(ss)} — {', '.join(ss) or '—'}")
    satirlar.append(f"- **co_occurrence**: {len(co)} — {', '.join(co) or '—'}")
    satirlar.append("")
    satirlar.append("> Not: Bu denetim korpusu yalnızca kısıt-aşma (escape) olaylarını topladığı "
                    "için 'dürüst çözüm' sütunu boştur. Dürüst-çözüm ve kestirme→dürüst "
                    "karşı-örnekleri için bkz. kaynaklar/provisioning-hypothesis-evidence-audit.md "
                    "(13 vakalık denetim setinin dışındadır).")
    metin = "\n".join(satirlar) + "\n"
    # newline="": aynı gerekçe (Windows'ta \n -> CRLF çevrilmesini engeller).
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(metin)
    return metin


def main() -> None:
    dogrula(VAKALAR)
    yaz_csv(VAKALAR, HERE / "vaka_seti.csv")
    yaz_json(VAKALAR, HERE / "vaka_seti.json")
    tablo = yaz_2x2(VAKALAR, HERE / "2x2_tablo.md")

    from collections import Counter
    bt = Counter(v["blocked_type"] for v in VAKALAR)
    cs = Counter(v["causal_status"] for v in VAKALAR)
    ctx = Counter(v["context"] for v in VAKALAR)
    print("toplam vaka:", len(VAKALAR))
    print("blocked_type:", dict(bt))
    print("causal_status:", dict(cs))
    print("context:", dict(ctx))
    eksik = [v["case_id"] for v in VAKALAR if not v["quote"].strip() or not v["locator"].strip()]
    print("alinti/locator eksik:", eksik or "yok")
    print()
    print(tablo)


if __name__ == "__main__":
    main()
