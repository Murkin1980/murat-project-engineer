# EXP-23 / CP-01 — Bootstrap-start evidence (first real post-CP-07 run)

Date: 2026-10-10 (UTC)
Session: fresh Arena session (no prior sandbox/session memory reused)
Branch: `arena/480eb267-murat-project-engineer` @ `d7627d9033faeb43c0aaab98e0bf1595eb99db1b`
Fresh-main check: `origin/main` == local `main` == HEAD == `d7627d9` (verified via
`git fetch origin main`; `git merge-base HEAD origin/main` = HEAD). Working tree clean.

## Packet

- Builder: `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py build
  --experiment EXP-23 --checkpoint CP-01 --out-json .../evidence/bootstrap/ARENA_CONTEXT.json
  --out-md .../evidence/bootstrap/ARENA_CONTEXT.md`
- Packet bytes: **9,633 B** (`ARENA_CONTEXT.json`), **8,207 B** (`ARENA_CONTEXT.md`)
- Source-ref count: **7** (registry, task, readme, project_status, agents_rules,
  governance, accepted_lessons; `experiment_results` absent — no RESULTS.md yet, expected)
- Verify command: `bootstrap_builder.py verify --packet ARENA_CONTEXT.json --json`
  (full result in `verify_result.json`)

## Verdict

**FRESH** — all 7 checks true: authority disclaimer, stop rules present, deep-change
gate present, lesson scopes valid, disposition unambiguous (EXPERIMENT, README only),
source digests match, packet equals deterministic rebuild. No reasons/diffs.

## Queue condition (why EXP-23 starts now)

ARENA_TASK.md: "Do not start until EXP-22 Colibri has finished or Murat explicitly
reprioritizes this experiment." Registry shows EXP-22 = HOLD / PARTIAL (2026-10-09):
CP-01..CP-03 done, released-weight quality run outstanding. EXP-22 has **not**
finished, so this run is authorized by the second clause: the current owner
(Murat) explicitly instructed in this session to "Execute EXP-23 Papermorph,
starting with CP-01". Per governance §2 source-of-truth priority, rule 1
("Explicit current owner instruction") governs. Recorded here for the audit trail.

## Bootstrap-start metrics (before first useful EXP-23 action)

Definition: "first useful EXP-23 action" = first action that advances CP-01 proper
(cloning/pinning upstream Papermorph). Everything before it — task discovery,
fresh-main check, packet build/verify, packet reading — is bootstrap overhead.

### Files read

| # | File (or command) | Bytes consumed |
|---|---|---:|
| 1 | `git status && git log --oneline -5 && git branch -a` (output) | ~250 |
| 2 | `experiments/exp-23-.../ARENA_TASK.md` (full) | 2,745 |
| 3 | `experiments/exp-23-.../README.md` (full) | 5,752 |
| 4 | `ls experiments/ + exp-29 dirs` (output) | ~1,400 |
| 5 | `experiments/EXPERIMENT_REGISTRY.json` (partial, schema head) | ~3,050 |
| 6 | `experiments/exp-29-.../README.md` (full) | 3,136 |
| 7 | `experiments/EXPERIMENT_REGISTRY.json` (partial, EXP-22/23/29 entries) | ~7,000 |
| 8 | `experiments/exp-29-.../harness/bootstrap_builder.py` (full source) | 33,534 |
| 9 | `git fetch origin main; rev-parse/merge-base/status` (output) | ~330 |
| 10 | `bootstrap_builder.py build` (output) | ~300 |
| 11 | `bootstrap_builder.py verify --json` (output) | ~700 |
| 12 | `evidence/bootstrap/ARENA_CONTEXT.md` (full) | 8,207 |

- **Total bytes read before first useful action: ≈ 66,400 B** (command outputs
  approximate; all file sizes exact via `wc -c`).
- **Tool operations before first useful action: 12** (the table rows).

### Understood correctly from the packet (yes/no per field)

- Status (PLANNED, registry updated 2026-10-06): **yes** — from NOW + RESUME.
- Priority (after EXP-22 Colibri): **partially** — conveyed via `nearest_action`
  ("After EXP-22 Colibri completes, ..."). The README `Priority:` header line and the
  explicit "or Murat explicitly reprioritizes" escape clause are **not** in the packet;
  the queue-gate text had to be read from ARENA_TASK.md.
- Checkpoint chain (CP-01 → CP-02 → CP-03): **yes** — NOW.checkpoints.
- Stop rules (7 stop/FAIL + 10 guardrail bullets, with sources): **yes** — RULES.
- Next action (one document fixture, one AI-serial fixture, component map): **yes** —
  nearest_action + RESUME.next_action.
- Disposition (EXPERIMENT), lessons R1–R3 with scopes, deep-change gate, source-of-
  truth priority, handoff contract fields: **yes**.

### Rediscovery the packet failed to prevent

1. **Queue/reprioritization clause** — "Do not start until EXP-22 Colibri has
   finished or Murat explicitly reprioritizes" lives only in ARENA_TASK.md prose;
   the packet carries no priority/queue-gate field. Read the full task file to resolve
   start authorization. (Mitigation candidate: builder could surface the README
   `Priority:` line and any "Do not start" gate line.)
2. **Builder CLI usage** — a fresh session does not know the build/verify argument
   surface. I read the full 33,534 B builder source to confirm the CLI. Cheaper path
   (`--help`, ~1 KB output) exists but is undocumented; the EXP-29 README does not
   reproduce the usage block. This was the single largest rediscovery cost (~half the
   total bootstrap bytes).

### Stale / contradictory state detected

- **None in the packet** (FRESH; digests + rebuild identical).
- One cross-source tension, resolved per governance §2 rule 1: registry says EXP-23
  next action waits for EXP-22 completion, while EXP-22 is HOLD (not complete) and the
  owner instructed to start now. Not a data conflict — an explicit owner override;
  recorded above.

## Handoff to normal work

Packet used as startup context; canonical Git files remain authoritative. All
subsequent EXP-23 evidence stays under this experiment directory. No EXP-29 harness
modification made or needed during preflight (the two rediscovery items are findings
for a possible future EXP-29 checkpoint, not in-scope for EXP-23).
