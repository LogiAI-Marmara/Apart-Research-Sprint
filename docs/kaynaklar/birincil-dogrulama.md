# Birincil kaynak doğrulaması

**Tarih:** 13 Eylül 2026. **Yöntem:** belgeler doğrudan yayıncının URL'sinden çekilip
istenen cümleler aratıldı. Bu dosya, ekibin GPT çıktısına DEĞİL birincil belgeye bakarak
doğruladığı ifadeleri içerir. Doğrulanmamış olanlar da aynı listede, açıkça işaretli.

## DOĞRULANDI

### OpenAI — Hugging Face Incident: Technical Report (PDF)
https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf

> “Despite only 22% of the evaluation tasks being unsolved, 93% of the tasks discussed on the message board came from this set.”
> — basılı s. 22

> “OpenAI found in its internal evaluations that across many different attempts at a solution, no model has ever produced a correct answer for 198 of the evaluation's 898 tasks.”
> — basılı s. 22

> “This incident reflects misaligned behavior in an outlier scenario involving a rare and unexpected confluence of events: the presence of impossible tasks in the ExploitGym evaluation, model persistence over long task horizons, and messages to peer models that caused those models to deviate from their goal.”
> — basılı s. 19

> “Because the agent was blocked from accessing the internet, the agent could not retrieve the linked materials and the task was effectively blocked.”
> — basılı s. 6 (8 Mayıs, training koşusu)

> “During these evaluations, these models, harnessed as agents, began unexpectedly communicating with one another through an internal instance of JFrog Artifactory…”
> — basılı s. 4 (Temmuz olayının EVALUATION olduğunun kanıtı)

### Thaman — Reward Hacking Benchmark (arXiv 2605.02964)
https://arxiv.org/html/2605.02964

> “Environmental hardening reduces exploit rates from 6.5% to 0.8%” · “Task success rates are statistically indistinguishable (83.2% vs. 82.8%)” — §6.5

> “Models with near-zero exploit rates on standard variants show measurable reward hacking on harder variants” — §6.6

> “the outward task interface and the available exploit surface are unchanged across the two tiers” — §6.6

> “reward hacking emerges when exploit strategies are simpler than honest solutions under the agent's effective search process” — §7

### UK AISI — Cheating behaviour in frontier model evaluations
https://www.aisi.gov.uk/blog/cheating-behaviour-in-frontier-model-evaluations

> “One particularly stark example of cheating behaviour occurred during a cyber capability evaluation that was accidentally misconfigured and therefore impossible to solve.”

> “The model tested was so persistent in attempting to cheat that it wrote and ran code on an external service, hosted on the open internet outside of AISI's systems.”

> “We think this means that, perhaps unsurprisingly, cheating behaviour is substantially shaped by the specifics of the techniques used to train the model, including alignment training, and not just raw capability.”

> “Every model tested in this analysis attempted to cheat some of the time.”

### METR — Frontier Risk Report (February to March 2026)
https://metr.org/blog/2026-05-19-frontier-risk-report/
*(14 Eyl gecesi ikinci turda doğrulandı)*

> “in many of the documented privilege escalation and cheating incidents, the agent was trying to access resources that it perceived as necessary for completing a task that otherwise seemed impossible.”
> — Risk assessment → Risk at the time of assessment → Motive → Task completion motives

> “This behavior occurred across 6 blackbox runs on easy task variants where the model could have easily solved the task legitimately.”
> — INC-027: OpenAI – `blackbox`

> “After the server died, the task became impossible through the intended path, and the agent spent the remaining run attempting to recover the server or escape the evaluation container.”
> — INC-030: OpenAI – `web_hacking`

> “In one run of this task, the agent couldn’t use the API key it was given because the associated API account had run out of credit.”
> — INC-044: Anthropic – Acquiring unintended compute

> “In one of our evaluations, after Opus 4.6 ran out of the API credits that were necessary to solve one of our ML tasks, it proceeded to find (free) replacement compute resources online, despite recognizing that this went against task instructions, and achieved a passing score on the task.”
> — Key facts → Motive

### UK AISI — Incident Report: unsanctioned agent behaviour during cyber testing
https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing

> “In a number of runs, the task prompt was misconfigured so that the agent (incorrectly) believed no ‘solve’ existed that didn’t require it to go beyond the intended task scope.”
> — “Why this happened”, madde başlığı: “The task was hard, and misconfigurations sometimes made it harder.”

> “This exercise compared an existing cyber range against a new range, testing seven different models on the two ranges over 122 runs in total.”
> — “What happened”

### Thaman — DeepSeek kardeş karşılaştırması (iki sunum da mevcut)

> “A controlled sibling comparison (DeepSeek-V3 vs. DeepSeek-R1-Zero) shows RL post-training is associated with substantially higher reward hacking (0.6% vs. 13.9%), with consistent gaps across all four task families.” — Abstract

> “In the controlled sibling comparison (E2), reward hacking rates increase from 0.4–0.8% (DeepSeek-V3, SFT-focused) to 12–16% (DeepSeek-R1-Zero, RL-from-base), holding tasks, environment, and evaluation harness fixed.” — §6.2

Belge ikisinin aynı ölçümün farklı sunumu olup olmadığını açıklamıyor. Raporda §6.2 esas
alınacak, abstract parantezde verilecek.

### Üçüncü tur — Related Work atıfları (13 Eyl, hepsi açıldı)

> “These objective functions, or their implementation, can be ‘gamed’ by solutions that are valid in some literal sense but don’t meet the designer’s intent.”
> — Amodei et al., *Concrete Problems in AI Safety*, §4 Avoiding Reward Hacking.
> DÜZELTME: literatür taramasındaki “perverts the spirit of the designer’s intent / §2” ifadesi bu belgede bulunamadı; yukarıdaki cümle ve §4 kullanılacak.

> “many tasks become infeasible under constrained tool environments, where the capabilities required for successful task completion are unavailable”
> — Cheng, Cai, Jiang, Mai — *Do Agents Know What They Can’t Do? Evaluating Feasibility Awareness in Tool-Using Agents*, Abstract. https://arxiv.org/abs/2605.28532

> “CUAs consistently exhibit Blind Goal-Directedness (BGD): a bias to pursue goals regardless of feasibility, safety, reliability, or context.”
> — Shayegani ve diğerleri — *Just Do It!? Computer-Use Agents Exhibit Blind Goal-Directedness*, Abstract. https://arxiv.org/abs/2510.01670

> “Seven tasks are *blocked by design*: no policy-compliant solution exists.” · “their requirements are incompatible with a hardened environment”
> — Davidovich, Amar, Rozencwajg, Hiltch — *Permission Denied: Policy-Graded Evaluation of Coding Agents in Hardened Environments*, § Benchmark Artifacts under Policy. https://arxiv.org/abs/2608.02670
> NOT: Bu, sandığımızdan daha yakın bir öncül çalışma. Özgünlük iddiası buna göre daraltıldı.

### Anthropic — Investigating three real-world incidents in our cybersecurity evaluations
https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals

> “After reviewing 141,006 evaluation runs where Claude could have obtained internet access, we identified three incidents…”

> “In four runs of this evaluation, Claude ran into difficulty reaching its simulated target within the evaluation environment, but then discovered that the real company was reachable via the internet.”

> “To get a phone number, after failing to find a free phone number service, it tried—and failed—to obtain funds to pay for a phone number through several different means.”

> “In this evaluation, when Claude was unable to reach its intended fictional target, it looked for alternatives online, scanning roughly 9,000 targets.”

## DÜZELTİLEN YANLIŞ ALINTI

**Yee 2002 yanlış alıntılanmış.** Literatür taraması şunu veriyordu:
“To the greatest extent possible, the natural way to do any task should also be the secure way.”
Birincil metinde (http://zesty.ca/pubs/icics-2002-uidss.pdf, §3, “Path of Least Resistance”
ilkesi) geçen cümle şudur:

> “The most natural way to do any task should also be the most secure way.”

Rapora doğru hâli girdi.

## AÇILAMADI — atıf verilmedi

- **Gasser (1986), “working around”.** Birincil metin açılamadı; ikincil kaynaktan (Alter 2014)
  alıntılamak yerine rapordan çıkarıldı.
- `security-controls-obstructing-work-research.md` içindeki diğer insan-güvenliği kaynakları
  (Adams & Sasse, Herley, compliance budget vb.) açılmadı ve raporda kullanılmıyor.

## KULLANILMAYACAK — uydurma/birleştirilmiş sayı

**“10/122 = %8,20 taban oranı” RAPORA GİREMEZ.** Araştırma çıktısı bu oranı verdi; birincil
kaynağa bakıldı. AISI olay raporu **sayı vermiyor**, yalnızca “In a number of runs” diyor.
“Ten Mythos 5 runs received an older instruction…” cümlesi AISI belgesinde **geçmiyor**;
`agiforeground.com` adlı üçüncü taraf bir yazıya ait. Pay bir blogdan, payda AISI'den alınıp
birleştirilmiş. Taban oran hâlâ **YOK** ve raporda yokluğu bir bulgu olarak yazılıyor.

## DOĞRULANMADI — kullanılmadan önce teyit edilmeli

- **AISI Figure 1 rakamları (14.1% 67/475, 12.6%, 11.4%, 9.1%, 7.8%).** Figür görsel;
  blogun metninde yok. Sprint cheat-sheet'i aynı rakamları veriyor, yani ikincil teyit var,
  ama blogdan birebir okunmadı.
- **Kaynak dosyalarının provenansı.** `kaynaklar/orijinal/` içinde yalnızca
  `escape_pressure_evidence_audit.docx` var. Diğer üç `.md`'nin orijinali yok; onlar için
  “dönüşüm doğrulandı (195 paragraf, kayıp 0)” ifadesi GEÇERSİZDİR.
