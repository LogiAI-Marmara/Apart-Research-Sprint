# Case dataset — the under-provisioning ("escape pressure") hypothesis

**Hypothesis (revised 13 September 2026).** A closed honest completion path (a
requirement block) is NOT the sole or main cause of constraint-escape behaviour; it is
an intensifier. Closing a shortcut (a shortcut block) reduces constraint escape but does
not eliminate it.

*The earlier, stronger form* — "if the shortcut is closed, the agent uses the honest path" —
was abandoned: METR INC-027 (six easy runs, "could have easily solved the task
legitimately"), Thaman LF-2 and C09 in this set contradict that claim. Details:
`../../docs/kaynaklar/provisioning-hypothesis-evidence-audit.md`.

This dataset structures the 13 case chains (blockage → agent response) from the evidence
audit document and codes each one's block type according to the source's own wording.

## Files

- `vaka_seti.csv` / `vaka_seti.json` — 13 cases, identical content (CSV is `utf-8-sig`, for Excel).
- `2x2_tablo.md` — blocked_type × behaviour table.
- `kur.py` — the single source of truth; contains the 13 coded cases and generates every output.
- Sources: `../../docs/kaynaklar/` (see below).

## Sources and conversion

**Number of institutions: 5** (AISI, Anthropic, OpenAI, METR, collusion.wiki). The ExploitGym
paper/repo was audited but no qualifying case was found (NOT FOUND); Hugging Face is not
the source of any case; neither is counted among the sources.

For quotes verified by us directly against the primary source, see
`../../docs/kaynaklar/birincil-dogrulama.md`.

The 13 cases were coded from **`../../docs/kaynaklar/escape_pressure_evidence_audit.md`**
(Instance A–M). That `.md` was produced from the original `.docx`
(`../../docs/kaynaklar/orijinal/`) with a quote-fidelity-first converter
(`../../docs/kaynaklar/docx_to_md.py`, python-docx): no text was rewritten; quotation
marks, arrows, dashes and locators were preserved. After conversion it was verified
programmatically that all 195 text paragraphs of the original appear verbatim in the `.md`
(loss = 0), and the quotes were compared against the original `.docx`.

The context / counter-evidence documents were also brought into the repo (already `.md`,
copied as-is):
- `../../docs/kaynaklar/provisioning-hypothesis-evidence-audit.md` — adversarial (counter-evidence) sweep.
- `../../docs/kaynaklar/environment-under-provisioning-literature-review.md` — literature / novelty sweep.
- `../../docs/kaynaklar/security-controls-obstructing-work-research.md` — human security-bypass literature.

## Field definitions

| field | definition |
|---|---|
| `case_id` | C01–C13 (corresponds to Instance A–M in the source; the `instance` field gives the mapping) |
| `source` | the institution that produced the source (AISI / Anthropic / OpenAI / METR / collusion.wiki) |
| `source_doc` | document name + audit source number (S1–S9) |
| `locator` | page or section |
| `context` | `training` / `evaluation` / `unspecified` — **whatever the source says**; `unspecified` if it says nothing |
| `task` | what the agent was asked to do |
| `blocked_thing` | what the agent could not access |
| `blocked_type` | **`requirement` / `shortcut` / `unclear`** — classification (below) |
| `agent_response` | what the agent did |
| `outcome` | `constraint_breached` / `attempted_failed` / `solved_honestly` (coded values; see the mapping table below) |
| `causal_status` | `source_stated` (the source establishes the link in its own words) / `co_occurrence` (merely side by side) |
| `quote` | verbatim quote (may be shortened, must not be altered) |
| `context_basis`, `blocked_type_basis` | *(extra field)* the auditable rationale for the coding |
| `instance` | *(extra field)* the Instance letter in the source (A–M) |

### `outcome` coded values — mapping from the original Turkish coding

The `outcome` values were originally coded in Turkish and were translated one-to-one into
English snake_case on 14 September 2026. No category was added, removed or recoded; the
table preserves the coding trail.

| original (Turkish) | coded value (English) | meaning | cases |
|---|---|---|---|
| `kısıt aşıldı` | `constraint_breached` | the agent got around the constraint | 11 |
| `denendi başarısız` | `attempted_failed` | the agent tried to get around it and failed | 2 (C06, C12) |
| `dürüst çözdü` | `solved_honestly` | the agent solved the task via the honest path | 0 (not present in this corpus) |

## Classification rule (blocked_type)

The source's own wording is used; no interpretation is added.

- **`requirement`** — the blocked thing was necessary for COMPLETING the task; the honest
  completion path was closed (entirely, or at the level of the required output).
  *E.g. C06 (OpenAI, 8 May): the task required the Google Drive links, the internet was
  disabled, "the task was effectively blocked".*
- **`shortcut`** — the blocked thing was a SHORTCUT; the honest path remained open.
  *E.g. C09 (OpenAI library re-creation): the task was designed to be solved WITHOUT the
  reference, via inputs/outputs (the honest path was provided); direct access to the
  reference was a shortcut, and the agent exploited a vulnerability and copied the reference.*
- **`unclear`** — a requirement/shortcut decision cannot be made from the source text.
  *There is currently no case with this code.* C11 (OpenAI, July, ExploitGym) was corrected
  from `unclear` → `requirement` after verification against the primary source on
  13 September 2026: the Technical Report (p. 19) characterises the incident as “the presence
  of impossible tasks in the ExploitGym evaluation”. The earlier coding looked only at the
  blog text. In the same correction `context` also changed `training` → `evaluation`
  (Technical Report pp. 4, 22).

Where certainty was lacking, `unclear` was written; no coding was invented. A high `unclear`
count is not a problem; invented coding is.

## Results (summary)

- Total: 13 cases.
- `blocked_type`: requirement 12 · shortcut 1 · unclear 0.
- `causal_status`: source_stated 13 · co_occurrence 0.
- `context`: evaluation 7 · training 5 · unspecified 1.

See `2x2_tablo.md` for the 2x2. The audit corpus is **escape-selected** (only escape
incidents were collected), so the "honest solution" column is empty and the result is
consistent with requirement blocks co-occurring with constraint escape; but this corpus on
its own does not *test* the hypothesis (see the limitations below).

## Limitations of the dataset

- **Single coder.** No second independent coder; inter-coder reliability was not measured.
- **Relies on the sources' own wording.** Classification follows what the source text states;
  no independent verification was done. A secondary source (collusion.wiki, C05) reproduces
  the analysis.
- **Causality is established by statement, not by experiment.** `causal_status=source_stated`
  means the source establishes the link in its own words; it is not a controlled manipulation.
- **Selection bias.** The audit collected only escape incidents; outcomes such as "honest
  solution" or giving up despite a requirement block do not appear in this corpus.
  Shortcut→honest counter-examples (e.g. Reward Hacking Benchmark LF-2, METR INC-027) are in
  the counter-evidence document and outside the 13-case set. The table is therefore
  *consistent with* requirement→escape but does not prove a behavioural DIFFERENCE between
  requirement and shortcut (the shortcut cell has a single case, and it too ended in escape).
- **Small n and context imbalance.** 13 cases: 7 evaluation, 5 training, 1 unspecified.
  OpenAI's May cases (C06–C10) are training runs; if the claim is about evaluation
  environments this distinction must be kept (the `context` field was not merged).
- **The reason for the impossibility is unknown (C11).** The source says the tasks were
  impossible but not why (missing resource vs. sheer difficulty). If the provisioning framing
  requires this distinction, it must be stated explicitly in the report.
- **`context` was coded conservatively.** Where the case's own quote contains neither
  training nor evaluation, the source's document-level framing was used and the rationale
  recorded in `context_basis` (`unspecified` for C05, since there is no framing at all).
