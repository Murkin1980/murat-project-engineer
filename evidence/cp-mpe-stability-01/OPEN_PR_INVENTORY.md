# CP-MPE-STABILITY-01 — inventory of 40 pre-existing open PRs

Baseline: main d97278d0, 2026-11-15. Source: GitHub open PR listing + changed-file paths for **all 40**. This is initial triage; complete semantic diff reconciliation and closure authority remain outstanding.
No PR has been closed, merged, rebased, or declared safe to discard.

Codes: **REVIEW** unique proposed work; **RECONCILE** compare preserved unique content vs canonical main; **ID_CONFLICT** old EXP allocation must not be merged; **SUPERSEDED?** requires proof old artifact is redundant; **HOLD** preserve blocked/history or deep-change before action.

| PR | Classification | Reason |
|---|---|---|
| [#130](https://github.com/Murkin1980/murat-project-engineer/pull/130) | REVIEW | Harness² DeepSeek research |
| [#60](https://github.com/Murkin1980/murat-project-engineer/pull/60) | REVIEW | REA reconnaissance evidence |
| [#127](https://github.com/Murkin1980/murat-project-engineer/pull/127) | RECONCILE | FIFO text vs merged #128/#129 |
| [#125](https://github.com/Murkin1980/murat-project-engineer/pull/125) | RECONCILE | HackerTube intake vs EXP-46 |
| [#123](https://github.com/Murkin1980/murat-project-engineer/pull/123) | SUPERSEDED? | CP-09 sync after #115 |
| [#120](https://github.com/Murkin1980/murat-project-engineer/pull/120) | RECONCILE | MCC source vs EXP-45 |
| [#119](https://github.com/Murkin1980/murat-project-engineer/pull/119) | ID_CONFLICT | Process Discovery EXP-30 -> canonical EXP-44 |
| [#118](https://github.com/Murkin1980/murat-project-engineer/pull/118) | ID_CONFLICT | Nodecode EXP-30 candidate |
| [#117](https://github.com/Murkin1980/murat-project-engineer/pull/117) | REVIEW | AGENTS Cloudflare note |
| [#116](https://github.com/Murkin1980/murat-project-engineer/pull/116) | REVIEW | OpenViking scoped proposal |
| [#114](https://github.com/Murkin1980/murat-project-engineer/pull/114) | SUPERSEDED? | CP-09 older instructions |
| [#113](https://github.com/Murkin1980/murat-project-engineer/pull/113) | RECONCILE | Harness² plan vs canonical EXP-41 |
| [#108](https://github.com/Murkin1980/murat-project-engineer/pull/108) | SUPERSEDED? | EXP-29 CP-08 instructions |
| [#105](https://github.com/Murkin1980/murat-project-engineer/pull/105) | REVIEW | OpenMuse unique CP-01 evidence |
| [#104](https://github.com/Murkin1980/murat-project-engineer/pull/104) | RECONCILE | OpenMuse EXP-32 -> canonical EXP-38 |
| [#107](https://github.com/Murkin1980/murat-project-engineer/pull/107) | RECONCILE | Seedance original EXP-33 |
| [#103](https://github.com/Murkin1980/murat-project-engineer/pull/103) | RECONCILE | HtmlVR original EXP-31 |
| [#106](https://github.com/Murkin1980/murat-project-engineer/pull/106) | REVIEW | Arena coding quality plan |
| [#102](https://github.com/Murkin1980/murat-project-engineer/pull/102) | RECONCILE | WaveSpeed proposals |
| [#98](https://github.com/Murkin1980/murat-project-engineer/pull/98) | ID_CONFLICT | Crisp Diagrams EXP-30 |
| [#97](https://github.com/Murkin1980/murat-project-engineer/pull/97) | REVIEW | New brainstorm governance policy |
| [#92](https://github.com/Murkin1980/murat-project-engineer/pull/92) | HOLD | Cloudflare preflight auth missing |
| [#90](https://github.com/Murkin1980/murat-project-engineer/pull/90) | HOLD | Arena secret preflight |
| [#73](https://github.com/Murkin1980/murat-project-engineer/pull/73) | HOLD | EXP-29 multi-file stale recovery |
| [#59](https://github.com/Murkin1980/murat-project-engineer/pull/59) | REVIEW | Refero Styles |
| [#58](https://github.com/Murkin1980/murat-project-engineer/pull/58) | REVIEW | Text-to-CAD |
| [#57](https://github.com/Murkin1980/murat-project-engineer/pull/57) | REVIEW | Pocock skills |
| [#56](https://github.com/Murkin1980/murat-project-engineer/pull/56) | REVIEW | Scene continuity |
| [#43](https://github.com/Murkin1980/murat-project-engineer/pull/43) | HOLD | EXP-13 pilot evidence |
| [#38](https://github.com/Murkin1980/murat-project-engineer/pull/38) | REVIEW | OBS-01 code change |
| [#32](https://github.com/Murkin1980/murat-project-engineer/pull/32) | RECONCILE | EXP-19 trend registry |
| [#27](https://github.com/Murkin1980/murat-project-engineer/pull/27) | HOLD | Strix retry |
| [#25](https://github.com/Murkin1980/murat-project-engineer/pull/25) | RECONCILE | AI search entity registry |
| [#24](https://github.com/Murkin1980/murat-project-engineer/pull/24) | RECONCILE | AnyJev EXP-14 |
| [#19](https://github.com/Murkin1980/murat-project-engineer/pull/19) | REVIEW | Minimalist Entrepreneur |
| [#14](https://github.com/Murkin1980/murat-project-engineer/pull/14) | REVIEW | Presentation change |
| [#10](https://github.com/Murkin1980/murat-project-engineer/pull/10) | HOLD | Large EXP-13 governance diff |
| [#6](https://github.com/Murkin1980/murat-project-engineer/pull/6) | HOLD | Stage 4 gateway |
| [#3](https://github.com/Murkin1980/murat-project-engineer/pull/3) | HOLD | Compute Budget Gate |
| [#2](https://github.com/Murkin1980/murat-project-engineer/pull/2) | HOLD | Developer readiness |

Totals: REVIEW=14, RECONCILE=11, SUPERSEDED?=3, ID_CONFLICT=3, HOLD=9.

**STOP:** No automatic PR closure. Resolve per PR by diff against current main, exact unique evidence, canonical FIFO identity, owner review. B-04 status: **TRIAGED, NOT CLEARED**.
