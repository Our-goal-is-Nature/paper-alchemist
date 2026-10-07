---
profile: ipm
mode: bilingual
target_language_weight: 0.7
secondary_language_weight: 0.3
---
# Cross-lingual academic structure profile

Align high-level rhetorical functions across English and Chinese. Do not translate or reuse source sentences.

## Aligned modules

| Module | English sources | Chinese sources | Transfer rule |
|---|---:|---:|---|
| abstract | 45 | 0 | single-language fallback |
| introduction | 45 | 0 | single-language fallback |
| related-work | 45 | 0 | single-language fallback |
| problem-definition | 37 | 0 | single-language fallback |
| methodology | 41 | 0 | single-language fallback |
| experiment-setup | 31 | 0 | single-language fallback |
| results-analysis | 46 | 0 | single-language fallback |
| conclusion | 43 | 0 | single-language fallback |

## Transfer boundaries

- Transfer problem framing, gap placement, contribution ordering, evidence chains, and conclusion closure.
- Keep terminology, grammar, voice, citation punctuation, and sentence rhythm under the target-language profile.
- When evidence exists in one language only, mark the generation brief as degraded rather than blocking.

## Reviewed expanded synthesis and evidence boundaries

- 47 normalized publication sources (1998–2026); 46 included, comprising 44 empirical/evaluated-system and two conceptual/reflection. The CACM 2006 unheaded narrative is excluded for insufficient-paper-structure and retained for separate section learning. All 10 original sources/70 completed observations are unchanged.
- The expanded evidence is principally Web searching/log analysis, sponsored advertising, HCI, audience/persona analytics and measurement—not routing optimization/science. Travel queries and airline behaviors do not establish routing models or benchmark practices.
- Genre-aware transfer: early descriptive log abstracts often list analysis levels; structured abstracts separate purpose/design/findings/value; controlled studies foreground protocol; advertising journals connect theory and KPI hypotheses; short conference/magazine genres compress or omit sections. Do not impose a full modern empirical template on absent sections.
- Match question/design/unit → evidence → interpretation → limitation. Differentiate record/query/session/user/machine/tweet/persona; evaluated relevance/clicking/conversion; revenue/profit/ROA; overlap/stability/validity. Use practical effect magnitude, not p-value alone.
- Publication coverage is not independent replication count. Same Excite/AltaVista/Dogpile data, retailer campaigns, conference/journal variants and APG development streams recur; do not pool repeated outcomes or count them as independent confirmations. Unverified relationships are explicitly possible, not asserted disjoint.
- All eight Chinese modules have zero sources and low confidence. Configured 70/30 weights do not supply Chinese evidence; use English-supported functions only with degraded-single-language disclosure and user/journal rules for Chinese surface realization. No Chinese style contrast is observable.
- Text recovery uses existing text layers, no OCR. Poppler syntax/xref warnings and legacy glyph errors affect the 2000 Excite journal PDF; older multimedia also retains encoding artifacts. Tables, equations, captions, column order and paragraph metrics are not certified reconstructions. Verify source numbers/equations against PDFs, never guess.
- Historical platform/engine features and empirical prevalences are study-period evidence, not current defaults. Same-author writing is aggregate functional guidance, not a persona to imitate. New manuscript facts/citations come only from confirmed context, not this corpus.
