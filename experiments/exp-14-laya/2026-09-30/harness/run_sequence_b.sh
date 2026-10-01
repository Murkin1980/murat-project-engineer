#!/usr/bin/env bash
# EXP-14 Sequence B runner — executes on whatever host can reach the pinned
# Laya checkpoint. Idempotent and evidence-first: every stage writes a file even
# when it fails, so a blocked run still produces a recordable result instead of
# a silent gap.
#
# Usage: bash harness/run_sequence_b.sh [PASSES] [ARMS]
#   PASSES  reproducibility passes per arm (default 3)
#   ARMS    space-separated list: root typed-decisions (default "root typed-decisions")
set -uo pipefail

PASSES="${1:-3}"
ARMS="${2:-root typed-decisions}"
# TAG keeps repeat invocations from overwriting an earlier run's console log or
# host probe. Attempt 1 (arms "root typed-decisions") is preserved as
# raw/sequence_b_console_attempt1.log and
# raw/laya_access_probe_execution_host_attempt1.json.
TAG="${3:-}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$(dirname "$HERE")"
REPO_ROOT="$(cd "$RUN_DIR/../../.." && pwd)"
cd "$RUN_DIR"

PY="${PYTHON:-python3}"
LOG="$RUN_DIR/raw/sequence_b_console${TAG:+_$TAG}.log"
mkdir -p "$RUN_DIR/raw"
: > "$LOG"

log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

log "=== EXP-14 Sequence B ==="
log "run_dir=$RUN_DIR"
log "repo_root=$REPO_ROOT"
log "python=$($PY -V 2>&1)"
log "passes=$PASSES arms=$ARMS tag=${TAG:-<none>}"

# ---------------------------------------------------------------- stage 0
log "--- stage 0: host + egress probe (contrast evidence) ---"
$PY "$HERE/probe_laya_access.py" --timeout 20 \
    --out "$RUN_DIR/raw/laya_access_probe_execution_host${TAG:+_$TAG}.json" \
    --skip-load-probe >> "$LOG" 2>&1
log "probe exit=$?"

# ---------------------------------------------------------------- stage 1
log "--- stage 1: verify the frozen dataset digest is unchanged ---"
$PY - <<'PY' >> "$LOG" 2>&1
import hashlib, json, pathlib, sys
run = pathlib.Path(".").resolve()
blob = (run / "frozen/dataset_v1.json").read_bytes()
actual = hashlib.sha256(blob).hexdigest()
recorded = next((l.split()[0] for l in
                 (run / "frozen/DATASET_SHA256.txt").read_text().splitlines()
                 if l.endswith("dataset_v1.json")), None)
dataset = json.loads(blob)
print("dataset_id:", dataset["dataset_id"])
print("cases:", len(dataset["cases"]))
print("recorded_sha256:", recorded)
print("actual_sha256:  ", actual)
if recorded != actual:
    print("FATAL: frozen dataset digest does not match the recorded freeze digest")
    sys.exit(2)
print("FROZEN DATASET VERIFIED: unchanged since freeze")
PY
if [ $? -ne 0 ]; then
    log "ABORT: frozen dataset verification failed"
    exit 2
fi

# ---------------------------------------------------------------- stage 2
log "--- stage 2: Sequence B arms ---"
OVERALL=0
for ARM in $ARMS; do
    case "$ARM" in
        root)            ARM_NAME="B_laya_zero_shot_root" ;;
        typed-decisions) ARM_NAME="B2_laya_typed_decisions_reference" ;;
        *) log "unknown arm '$ARM', skipping"; continue ;;
    esac
    log ">>> arm $ARM_NAME (checkpoint=$ARM)"
    $PY "$HERE/run_laya.py" --arm "$ARM_NAME" --checkpoint "$ARM" \
        --passes "$PASSES" --device cpu >> "$LOG" 2>&1
    STATUS=$?
    log "<<< arm $ARM_NAME exit=$STATUS"
    if [ $STATUS -ne 0 ]; then OVERALL=$STATUS; fi

    for PASS in $(seq 1 "$PASSES"); do
        RAW="$RUN_DIR/raw/laya_${ARM_NAME}_pass${PASS}.json"
        [ -f "$RAW" ] || continue
        $PY "$HERE/evaluate.py" --raw "$RAW" --arm "$ARM_NAME" \
            --out "$RUN_DIR/raw/metrics_${ARM_NAME}_pass${PASS}.json" >> "$LOG" 2>&1
        log "evaluated pass $PASS exit=$?"
    done
done

# ---------------------------------------------------------------- stage 3
log "--- stage 3: summary ---"
$PY - <<'PY' >> "$LOG" 2>&1
import json, pathlib
raw = pathlib.Path("raw")
rows = []
for path in sorted(raw.glob("metrics_*.json")):
    m = json.loads(path.read_text())
    rows.append((path.name, m["arm"], m["case_count"],
                 m["accuracy"]["exact_case_match_rate"],
                 m["safety"]["protected_false_negatives"],
                 m["safety"]["unsafe_fast_decisions"],
                 m["safety"]["invalid_outputs"],
                 m["safety"]["blocking_safety_gate"],
                 m["routing"]["routine_coverage_fraction"],
                 m["efficiency"]["latency"].get("median_ms"),
                 m["efficiency"]["tokens"]["total"]))
print(f"{'file':<52} {'exact':>6} {'pFN':>4} {'uFAST':>5} {'inv':>4} {'gate':>5} "
      f"{'routine':>7} {'p50ms':>9} {'tokens':>7}")
for r in rows:
    print(f"{r[0]:<52} {r[3]:>6} {r[4]:>4} {r[5]:>5} {r[6]:>4} {r[7]:>5} {r[8]!s:>7} {r[9]!s:>9} {r[10]:>7}")
PY

log "=== Sequence B finished, overall exit=$OVERALL ==="
exit $OVERALL
