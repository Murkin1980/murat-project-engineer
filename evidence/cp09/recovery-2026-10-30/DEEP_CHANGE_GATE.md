# Deep-change Gate — EXPERIMENT_REGISTRY.schema.json

- Date: 2026-10-30 (UTC)
- Task: MPE PR #115 conflict recovery against `main` @ `db4fff4d3258f57318f8eeb2e883ce29877940fb`
- Decision: `EXTEND_EXISTING`
- Gate result: **BLOCKED_DEEP_CHANGE / HUMAN_REQUIRED**
- Applied in this recovery: **NO**
- Exact proposed diff: [`proposed-schema.diff`](proposed-schema.diff)

## Trigger

`docs/governance/SCOPE-CHANGE-CONTROL.md` §6 requires explicit owner approval before changing a public contract. `contracts/EXPERIMENT_REGISTRY.schema.json` is the public registry contract consumed by `tests/test_contracts.py` and by downstream registry consumers. Adding enum members changes the set of documents accepted by that contract, even though the change is additive.

The current owner instruction explicitly says not to apply a public-contract change without separate explicit owner consent. PR #115's historical body called the enum addition authorized by the older CP-09 instruction; the current instruction is higher priority and supersedes that assumption for this recovery.

## Exact proposed change

```diff
-          "status": {"enum": ["IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "FAIL", "HOLD", "ADOPTED"]},
+          "status": {"enum": ["IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "PARTIAL", "FAIL", "HOLD", "RETIRED", "ADOPTED"]},
```

No other schema field, required key, pattern, or `schema_version` is proposed to change.

## Evidence for the proposed semantics

- `RETIRED` is already canonical for `EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`, and `EXP-16`. Owner commit `6c65a76` changed those records to `RETIRED` with do-not-run / historical-fixture semantics distinct from `HOLD`.
- `PARTIAL` is already canonical for `EXP-26`, whose result is a bounded component-extraction outcome (`PARTIAL / ADOPT_WITH_CHANGES`), not `PASS`, `FAIL`, or `HOLD`.
- The current registry contains 3 `RETIRED` records and 1 `PARTIAL` record.
- The dashboard producer and resolved dashboard already expose all seven observed statuses, including `PARTIAL`, `FAIL`, and `RETIRED`, without changing the schema.

## Consequences if approved

1. The four remaining registry-status subtest failures in `tests.test_contracts.PackageContractTests.test_canonical_experiment_registry_has_required_identity_and_status_fields` are expected to clear without deleting or weakening the test.
2. No registry data migration is required because the canonical registry already uses both values.
3. Validators using the schema will accept the existing canonical `PARTIAL` and `RETIRED` records.
4. Downstream consumers that hard-code the old eight-status enum must be reviewed; widening a public enum can still be a compatibility event for strict consumers.
5. `PARTIAL` and `RETIRED` remain distinct statuses; no collapse into `HOLD`, `FAIL`, or `PASS` is authorized.
6. After approval, apply only this one-line schema change, rerun the full unittest suite, focused EXP-29, validator, dashboard check, and `git diff --check`, then update PR #115. Merge/deploy still require separate authority.

## Consequences while blocked

- The schema file remains byte-identical to current `main`.
- The full unittest suite remains red with exactly four status-enum subtest failures (`EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`, `EXP-16`, `EXP-26`).
- CP-09 cannot be reported as full PASS because the mandatory full-suite gate is not green.
- Dashboard/Reladraw recovery, EXP-23 lifecycle parsing, conflict resolution, and EXP-29 compatibility verification remain valid and independently verified.

## Rejected shortcuts

- Mapping `RETIRED` to `HOLD` or `PARTIAL` to `FAIL`/`HOLD` would destroy canonical status semantics and violate the instruction to preserve existing statuses.
- Changing the contract test to ignore the schema, special-case the four records, or skip the test would weaken verification and is not authorized.
- Changing `schema_version` or adding a migration is outside the observed need and was not proposed.

## Required owner decision

Approve or reject the exact one-line enum addition in `proposed-schema.diff`. Until that decision is recorded, this portion stays stopped; no merge or deploy is authorized.
