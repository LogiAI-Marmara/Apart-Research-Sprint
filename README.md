# Apart Research × CeSIA — AI Incident Response Sprint, Track 1

Our submission to the Apart Research × CeSIA **AI Incident Response Sprint**
(11–13 September 2026), **Track 1 — Containment**.

Sprint page: https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13

## Thesis

**A closed honest completion path is not the cause of constraint escape; it is an
intensifier of it.** When an agent cannot complete its task through the sanctioned path
(a *requirement* is missing), escape behaviour concentrates; closing only a *shortcut*
reduces escape but does not eliminate it. The primary artifact codes 13 publicly documented
incident chains from 5 institutions against this distinction; the harness is a small,
API-driven experiment designed to probe the same distinction under controlled conditions.

## Team

- İsmail Efe Terlemez (ism00efe)
- Efe Özan (thozoz)

Marmara University, Department of Computer Engineering.

## Repository map

| path | what it is |
|---|---|
| `artifact/vaka_seti/` | **Primary artifact.** The 13-case dataset (`vaka_seti.csv` / `.json`), the 2x2 table, the generator `kur.py` (single source of truth) and its tests. |
| `artifact/harness/` | The experiment: a file-agent harness that runs a model under three conditions (control / no shortcut / no requirement) and scores out-of-scope attempts; `analiz.py` turns the run log into the report numbers. |
| `docs/kaynaklar/` | Sources: the evidence audit the cases were coded from, primary-source verification, counter-evidence and literature sweeps, the original `.docx` and its converter. |
| `report/` | The sprint report (official template). |

## Language note

Identifiers and comments inside the code (function, variable, module and file names, field
names such as `kestirme_denendi`) are in Turkish. The dataset schema and coded values, the
source quotes, and the report are in English. Dataset quotes are verbatim primary-source
text and are never translated or edited.
