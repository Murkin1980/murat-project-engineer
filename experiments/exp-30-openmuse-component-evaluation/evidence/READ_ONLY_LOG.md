# EXP-30 / CP-01 — Read-only execution log and integrity evidence

Everything in this file is what CP-01 actually did, in order. No OpenMuse code was installed,
built, executed, tested or deployed; no credential, provider key or paid API was touched; no
file outside this experiment directory was modified.

## 1. Session / branch evidence

| Item | Value |
| --- | --- |
| Authorized Arena session branch | `arena/9196ade0-murat-project-engineer` |
| Branch base | `ca16094b373c1b5dccb4988edafe11fcbb525517` (`main` at fetch time) |
| Working tree before any write | `git status` → `On branch arena/9196ade0-murat-project-engineer` / `nothing to commit, working tree clean` |
| Experiment directory before this run | absent on the session branch (`find` → `No such file or directory`); present only in open draft PR #104 |
| Registration PR checked | PR #104 `docs: register EXP-30 OpenMuse component evaluation` (DRAFT, base `main`, head `experiment/exp-30-openmuse-component-evaluation`, head commit `c4bbe940b84cc4f2517e407a8461b339e27d22bb26c492`) — files: `experiments/EXPERIMENT_REGISTRY.json`, `README.md`, `CHECKPOINTS.md`, `CP-01.md` |
| Instruction used (read from PR #104, not rewritten here) | `CP-01.md` blob `5160e5447a115c7c26091db339e27d22bb26c492`; `README.md` blob `8989c872a2f0812d443434f64cf1ecde867d492d`; `CHECKPOINTS.md` blob `04664049d42a7b15a0524fa5aba1434a02b8c3eb` |

`git merge-base --is-ancestor FETCH_HEAD main` → false: PR #104 is **not** merged. Therefore
CP-01 writes only new files under `experiments/exp-30-openmuse-component-evaluation/`
(report + evidence) and deliberately does **not** re-add or edit `README.md`,
`CHECKPOINTS.md`, `CP-01.md` or `experiments/EXPERIMENT_REGISTRY.json`.

## 2. Upstream acquisition (read-only)

```sh
mkdir -p /tmp/scratchpad && cd /tmp/scratchpad
rm -rf OpenMuse
git clone --depth 1 https://github.com/CopilotKit/OpenMuse.git OpenMuse   # source only
cd OpenMuse
git rev-parse HEAD                                    # 1ac68f3909f2478ab6280883f1ab5ea65eb5719d
git log -1 --format='%H %ci %s'                        # perf(server): scope refreshIdeas status queries (#109)
git tag | head -20                                     # (empty → no tags)
git branch -a                                          # main + origin/HEAD only
ls node_modules                                        # No such file or directory → nothing installed
python3 - <<'PY'   # (counting only; see §4)
```

The clone lives **outside the repository** (`/tmp/scratchpad`), so no upstream object, and no
dependency tree, entered the workspace or Git. The shallow clone was never `pnpm install`ed,
never built and never run; all reading was `sed`/`grep`/`wc`/`sha256sum` plus a line-citation
checker.

Pin cross-verification (three independent sources agreed):

| Source | Result |
| --- | --- |
| local clone | `git rev-parse HEAD` = `1ac68f3909f2478ab6280883f1ab5ea65eb5719d` |
| GitHub API | `gh api repos/CopilotKit/OpenMuse/branches/main` → `1ac68f3…2026-10-06T22:39:29Z` |
| git transport | `git ls-remote https://github.com/CopilotKit/OpenMuse.git HEAD refs/heads/main` → both `1ac68f3909f2478ab6280883f1ab5ea65eb5719d` |

## 3. Metadata read through the GitHub API (no repo writes)

Commands used (each read-only):

```sh
gh api repos/CopilotKit/OpenMuse            # created/pushed/stars/forks/license/issues
gh api repos/CopilotKit/OpenMuse/tags       # empty
gh api repos/CopilotKit/OpenMuse/releases   # empty
gh api repos/CopilotKit/OpenMuse/languages
gh api repos/CopilotKit/OpenMuse/contributors?per_page=10
gh api "repos/CopilotKit/OpenMuse/commits?per_page=10"
gh api "repos/CopilotKit/OpenMuse/actions/workflows"
gh api "repos/CopilotKit/OpenMuse/actions/runs?per_page=5"
gh api "repos/CopilotKit/OpenMuse/actions/runs?branch=main&per_page=6"
curl -sI "https://api.github.com/repositories/1371757322/commits?per_page=1"   # → rel="last" page=125
curl -sI "https://api.github.com/repositories/1371757322/contributors?per_page=1&anon=false"  # → page=27
```

Dependency licenses were checked one package/version at a time against the npm registry
(`curl -s https://registry.npmjs.org/<pkg>%2F<name>/<version>` → `.license`). No package
tarball was downloaded or unpacked.

Host baselines were read the same way:
`gh api repos/Murkin1980/minibase-cloudflare/contents/<path>` (decoded read-only) at
`9ab38d832970b3956cf0f831f9b578f7b9fd9001`, plus this repository's own files.

## 4. Measured numbers behind the report

| Measurement | Value | Command shape |
| --- | --- | --- |
| Non-test TS/TSX files under `apps/` + `packages/` | 99 files / **22,807** lines | python `rglob('*.ts'/'*.tsx')` excluding `*test*` |
| Test TS/TSX files | 60 files / 14,465 lines | same |
| Top-level `test(` declarations in `tests/*.test.ts` | **413** | `grep -h "^test(" \| wc -l` |
| …`apps/mobile/test/*.test.ts` | 32 | same |
| …`apps/worker/tests/*.test.ts` | 4 | same |
| …`apps/computer/*.test.ts` | 2 | same |
| `pnpm-lock.yaml` size | 14,137 lines | `wc -l` |
| `package.json` dependency counts | 18 runtime + 7 dev | python `len()` |
| CI jobs | 5 (`quality`, `platform`, `browser`, `browser-container`, `computer-container`) | `grep -n "^  [a-z-]*:$" .github/workflows/ci.yml` |
| Cloudflare/Workers surface in upstream | **0 matches** for `cloudflare\|wrangler\|durable object` in `.ts/.tsx/.md/.json/.yaml/Dockerfile` (lockfile excluded) | `grep -rin` |
| `apps/computer/files.py` | 103 lines | `wc -l` |

## 5. File integrity of the audited upstream files (SHA-256, first 16 hex)

Digests let a reviewer confirm that the citations were read from this exact tree.

```
769ccdc02e3c5aa1  257  apps/server/src/engine/worker.ts
ea8901e4222e6a97 1199  apps/server/src/engine/service.ts
9289e36978f2d132  397  apps/server/src/engine/model.ts
1cb0cb750ac5ae28  507  apps/server/src/engine/conversation.ts
cd2662b6fcf1ac09  242  apps/server/src/engine/tanstack-agent.ts
d1e74b2529f6b2f7   85  apps/server/src/engine/page-diff.ts
0d59b830acf8fe5f  168  apps/server/src/engine/routes.ts
0f17aaa7c91c48af  295  apps/server/src/browser.ts
5b52787ca5a3fbe6   39  apps/server/src/browser-console.ts
e1e69c6df791b0f4  218  apps/server/src/actions.ts
76435f770de71166  180  apps/server/src/db.ts
f4c97d49f6a9658d  183  apps/server/src/config.ts
c66e1af78a2fb0c0   90  apps/server/src/auth.ts
13cbc40de356e999  169  apps/server/src/search.ts
659b50226371352a  391  apps/server/src/jev/service.ts
84704c7e2e62e648   93  apps/server/src/jev/tools.ts
3c3d7dcd5ba74748  166  apps/server/src/computer-tools.ts
135320afb205c4de  396  apps/worker/src/browser.ts
1388bf762cda6680   96  apps/worker/src/network.ts
08481d07b0d6e075  100  apps/worker/src/proxy.ts
47f08548f24cf034  131  apps/worker/src/server.ts
91c0217fd57ffc2f  168  apps/worker/src/downloads.ts
aa0ef3efc3abb5e6  166  packages/domain/src/agent.ts
0501601b2187ce75   92  packages/domain/src/jev.ts
399a9cccf1b228c9   21  LICENSE
b1eb2d41ead969b5   61  package.json
b04439058eb039b5   21  pnpm-workspace.yaml
2995dec40931a629  256  README.md
754b712deeb64536   35  SECURITY.md
7ca6a6e585c0a443   25  docs/FEATURES.md
b26600a2b31897d8   82  docs/VERIFICATION.md
2015cb5aef43e9ce   42  docs/RICH-THREADS.md
8a95522645370e18  114  docs/COMPUTER.md
0f24bb6c06fbcbd2   47  apps/mobile/package.json
6986a72bd3803d7f   18  apps/worker/package.json
196710732ad35325   95  .env.example
e446624fd5def805  100  render.yaml
ee00a48de15073a8   31  infra/compose.yaml
d8e3f9e72d149471   90  .github/workflows/ci.yml
```

Full 64-hex digests for the five most load-bearing files:

```
apps/server/src/engine/worker.ts   769ccdc02e3c5aa14c729cf0f6d745d408d4089e932dcdca71c5b36077642195
apps/server/src/browser.ts         0f17aaa7c91c48afa0490ab7c3891e1b42d4b7c651c86c5d4917c72b0f526420
apps/server/src/actions.ts         e1e69c6df791b0f4f03fb4bc4e4ef7061b3e1b1e671b8f105b4b50171a792b19
apps/server/src/engine/page-diff.ts d1e74b2529f6b2f786bfdc3095a478957b1d0c75f40ed9e85fb03f8190988891
apps/worker/src/proxy.ts           08481d07b0d6e075d00dd1505ef0bc31ea9eb4155ff74e8a34a1a0d84fb4885f
LICENSE                            399a9cccf1b228c9e8ad348ef66a0a5802d438d46735d0d068390925aee5ee36
```

Reproduce: `git clone --depth 1 --branch main https://github.com/CopilotKit/OpenMuse.git` then
`git checkout 1ac68f3909f2478ab6280883f1ab5ea65eb5719d && sha256sum <path>`.

## 6. Repository checks (control, before and after)

CP-01 writes only documentation inside this experiment directory, so the repository's own
deterministic suite was run as a control.

```sh
python3 -m unittest discover -s tests
# before any write (clean tree at ca16094): Ran 432 tests … FAILED (failures=27, skipped=1)
# after the CP-01 files were added:        Ran 432 tests … FAILED (failures=27, skipped=1)
```

The 27 failures are **pre-existing on `main` at the base commit** and unrelated to EXP-30:
16 × `test_dashboard_registry_views::test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps`,
3 × `test_dashboard_registry_views::test_dashboard_exposes_a_mobile_view_for_each_registry_status`,
4 × `test_contracts::test_canonical_experiment_registry_has_required_identity_and_status_fields`
(failures for the `RETIRED` status of `EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`, `EXP-16`, `EXP-26`),
1 × `test_registry_to_reladraw::test_committed_diagram_is_fresh`,
1 × `::test_committed_mobile_views_are_fresh`, 1 × `test_exp29_bootstrap::test_committed_packet_is_fresh` and
1 × `::test_committed_packet_matches_fresh_build`.
CP-01 neither caused them nor attempted to fix them (out of checkpoint scope; fixing them means
touching `experiments/EXPERIMENT_REGISTRY.json`, the allowed-status set in
`murat-project-engineer@ca16094:tests/test_contracts.py` and the committed Reladraw views — the
registry half is PR #104's and the owner's territory).

Scope check:

```sh
git status --short    # only ?? experiments/exp-30-openmuse-component-evaluation/**
```

## 7. Prohibited actions — confirmed not performed

No dependency install (`pnpm`/`npm` were never run); no OpenMuse process, test, container or
Docker build; no `pnpm add`/lockfile change in this repo; no `wrangler` invocation; no deploy;
no credential, cookie, API key or paid call; no write to `CopilotKit/OpenMuse` (read-only
clone + public API GETs only); no write to `main`; no merge; no push of any other branch; no
work on CP-02/03/04.
