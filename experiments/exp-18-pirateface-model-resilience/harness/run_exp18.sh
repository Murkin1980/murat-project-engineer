#!/usr/bin/env bash
# EXP-18 — Pirate Face model resilience: bounded retrieval harness.
#
# Produces reproducible, machine-readable evidence for the EXP-18 contract
# (experiments/exp-18-pirateface-model-resilience/README.md) without touching
# production systems. Experiment tooling only: nothing in the repository
# imports it and it adds no dependency to the project.
#
# Stages
#   A  pin the Hugging Face repository + exact revision, record license/files
#   B  download the canonical artifact through the normal Hugging Face path
#   C  record the Pirate Face distribution reference (page, magnet, tracker view)
#   D  retrieve the model through the Pirate Face path (advertised magnet)
#   E  bounded primary-source loss: HF + Pirate Face web blocked, web-seed
#      stripped -> swarm + Pirate Face tracker + DHT
#   E2 same, but with the tracker blocked too -> DHT/PEX swarm only
#   F  deterministic file-set + SHA-256 comparison, torrent identity, piece check
#
# Usage: bash run_exp18.sh

set -uo pipefail

REPO="sentence-transformers/all-MiniLM-L6-v2"
HF="https://huggingface.co"
PF="https://pirateface.co"
PF_PAGE="${PF}/${REPO}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVID="${ROOT}/evidence"
WORK="${RUNNER_TEMP:-/tmp}/exp18-work"
LOG="${EVID}/00_run_transcript.log"
TORRENT_TIMEOUT="${TORRENT_TIMEOUT:-300}"  # seconds without progress before giving up (per stage)
HARNESS_BUDGET="${HARNESS_BUDGET:-1500}"   # total seconds for the recorded stages
RT="${RT:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
STARTED_EPOCH="$(date -u +%s)"
SKIPPED_STAGES=""

mkdir -p "$EVID" "$WORK"
: > "$LOG"

log() { printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$*" | tee -a "$LOG"; }
hr()  { log "-------------------------------------------------------------"; }
H="$ROOT/harness"

# The harness must always end by writing evidence, even when a retrieval stage
# stalls. Stages are skipped (and the skip is recorded) rather than overrunning
# the recorded-run budget.
budget_left() { echo $(( HARNESS_BUDGET - ( $(date -u +%s) - STARTED_EPOCH ) )); }
have_budget() { [ "$(budget_left)" -gt "${1:-45}" ]; }
skip_stage() { SKIPPED_STAGES="${SKIPPED_STAGES}${1} (budget exhausted) "; log "SKIPPED ${1}: only $(budget_left)s of harness budget left"; }
stage_timeout() {
  local want="$1" left; left="$(budget_left)"
  if [ "$left" -lt $(( want + 30 )) ]; then echo $(( left > 60 ? left - 30 : 30 )); else echo "$want"; fi
}

env_probe() {
  hr; log "STAGE 0 environment"
  {
    echo "run_utc=${RT}"
    echo "repo=${REPO}"
    echo "harness_host=$(uname -srm)"
    echo "runner_name=${RUNNER_NAME:-unknown}"
    echo "github_run_id=${GITHUB_RUN_ID:-unknown}"
    echo "github_sha=${GITHUB_SHA:-unknown}"
    echo "github_ref=${GITHUB_REF:-unknown}"
    python3 --version 2>&1
    curl --version 2>&1 | head -1
    jq --version 2>&1
    aria2c --version 2>&1 | head -1
    echo "euid=$(id -u)"
    echo "torrent_stage_timeout_s=${TORRENT_TIMEOUT}"
    echo "harness_budget_s=${HARNESS_BUDGET}"
  } | tee -a "$LOG" > "${EVID}/01_environment.txt"
}

step_a_pin() {
  hr; log "STAGE A pin repository, revision, license, expected files"
  curl -sS -L --max-time 60 "${HF}/api/models/${REPO}" -o "${EVID}/02_hf_model_metadata.json"
  REV="$(jq -r '.sha' "${EVID}/02_hf_model_metadata.json")"
  log "HF repository      : ${REPO}"
  log "HF pinned revision : ${REV}"
  curl -sS -L --max-time 60 "${HF}/api/models/${REPO}/revision/${REV}" -o "${EVID}/03_hf_model_at_revision.json"
  jq '{id, sha, private, gated, downloads, lastModified, license: (.cardData.license // (.tags[]? | select(startswith("license:")))), tags}' \
    "${EVID}/02_hf_model_metadata.json" > "${EVID}/04_hf_license_evidence.json"
  log "license evidence   : $(jq -c '{license}' "${EVID}/04_hf_license_evidence.json")"
  curl -sS -L --max-time 90 "${HF}/api/models/${REPO}/tree/${REV}?recursive=true&expand=true" \
    -o "${EVID}/05_hf_tree_at_revision.json"
  log "tree entries at revision: $(jq 'length' "${EVID}/05_hf_tree_at_revision.json")"
  echo "$REV" > "${WORK}/REV"
}

step_b_canonical() {
  hr; log "STAGE B download canonical artifact through normal Hugging Face path"
  if ! have_budget 180; then skip_stage "B_canonical_hf_download"; return 0; fi
  local rev; rev="$(cat "${WORK}/REV")"
  local dir="${WORK}/canonical"; mkdir -p "$dir"
  cd "$dir" || return 1
  local started; started="$(date -u +%s)"
  : > "${WORK}/hf_download_log.tsv"
  jq -r '.[] | select(.type=="file") | .path' "${EVID}/05_hf_tree_at_revision.json" |
  while IFS= read -r p; do
    mkdir -p "$(dirname "$p")"
    local code
    code="$(curl -sS -L --retry 3 --retry-delay 2 --max-time 900 -w '%{http_code}' \
      -o "$p" "${HF}/${REPO}/resolve/${rev}/${p}")"
    echo "$p	$code	$(stat -c%s "$p" 2>/dev/null || echo 0)" >> "${WORK}/hf_download_log.tsv"
    log "  hf fetch ${code} ${p} ($(stat -c%s "$p" 2>/dev/null || echo 0) bytes)"
  done
  log "HF canonical download wall seconds: $(( $(date -u +%s) - started ))"
  python3 "$H/manifest.py" "$dir" "${EVID}/06_canonical_manifest.json"
  cd "$ROOT" || return 1
}

step_c_reference() {
  hr; log "STAGE C record Pirate Face distribution reference"
  if ! have_budget 60; then skip_stage "C_pirateface_reference"; return 0; fi
  curl -sS -L --max-time 60 -w 'http_status=%{http_code}\n' "$PF_PAGE" -o "${EVID}/07_pirateface_page.html" 2>&1 | tee -a "$LOG"
  grep -oE "magnet:\?[^\"'<>[:space:]]+" "${EVID}/07_pirateface_page.html" | sed 's/&amp;/\&/g' | sort -u > "${WORK}/magnets.txt"
  log "magnet URIs found: $(wc -l < "${WORK}/magnets.txt")"
  head -2 "${WORK}/magnets.txt" | tee -a "$LOG"
  grep -oiE '[0-9a-f]{64}' "${EVID}/07_pirateface_page.html" | sort -u > "${WORK}/sha256_in_page.txt"
  log "sha256-like strings on page: $(wc -l < "${WORK}/sha256_in_page.txt")"
  : > "${WORK}/endpoint_probe.txt"
  for u in "${PF}/api/models/${REPO}" "${PF}/api/model/${REPO}" "${PF}/s/${REPO}" "${PF}/how-it-works"; do
    printf '%s\t%s\n' "$u" "$(curl -sS -L --max-time 30 -o /dev/null -w '%{http_code}' "$u" 2>/dev/null)" >> "${WORK}/endpoint_probe.txt"
  done
  cat "${WORK}/endpoint_probe.txt" | tee -a "$LOG"
}

# $1 = magnet, $2 = target dir, $3 = tag, $4 = extra aria2 options (optional)
run_torrent() {
  local magnet="$1" dir="$2" tag="$3"; local -a extra=()
  if [ -n "${4:-}" ]; then read -r -a extra <<< "$4"; fi
  mkdir -p "$dir"
  local stage_seconds; stage_seconds="$(stage_timeout "$TORRENT_TIMEOUT")"
  log "[${tag}] aria2c start (stage budget ${stage_seconds}s, harness budget left $(budget_left)s)"
  local rpc=6800
  [ "$tag" = "E_swarm_only" ] && rpc=6801
  [ "$tag" = "E2_dht_only" ] && rpc=6802
  python3 "$H/peer_sample.py" "$rpc" "${WORK}/${tag}_peers.json" $((stage_seconds + 20)) \
    > "${WORK}/${tag}_peers.txt" 2>&1 &
  local poller=$!
  local t0 t1
  t0="$(date -u +%s)"
  timeout "$((stage_seconds + 30))" aria2c \
    --dir="$dir" --seed-time=0 --bt-stop-timeout="${stage_seconds}" \
    --bt-save-metadata=true --bt-enable-lpd=false \
    --enable-dht=true \
    --dht-entry-point=router.bittorrent.com:6881 --dht-entry-point=router.utorrent.com:6881 \
    --dht-entry-point=dht.transmissionbt.com:6881 \
    --dht-listen-port=6881 --listen-port=6881 \
    --enable-rpc=true --rpc-listen-port="$rpc" --rpc-listen-all=false \
    --file-allocation=none --max-connection-per-server=16 --split=16 \
    --bt-tracker-connect-timeout=20 --bt-tracker-timeout=30 --bt-tracker-interval=20 \
    --enable-peer-exchange=true --bt-max-peers=100 \
    --console-log-level=notice --summary-interval=15 --auto-file-renaming=false --allow-overwrite=true \
    "${extra[@]}" "$magnet" > "${WORK}/${tag}_aria2c.log" 2>&1
  local rc=$?
  t1="$(date -u +%s)"
  # belt and braces: aria2c in RPC mode does not always terminate by itself
  pkill -f "rpc-listen-port=${rpc}" 2>/dev/null || true
  wait "$poller" 2>/dev/null
  cat "${WORK}/${tag}_peers.txt" | tee -a "$LOG"
  cp "${WORK}/${tag}_peers.json" "${EVID}/07_${tag}_peers.json" 2>/dev/null
  log "[${tag}] aria2c exit=${rc} wall_seconds=$((t1 - t0))"
  cp "${WORK}/${tag}_aria2c.log" "${EVID}/07_${tag}_aria2c.log"
  # Truth about whether the client finished the payload lives in the client log,
  # not in the exit code: a magnet first completes a metadata-only job
  # ([MEMORY][METADATA] ...), which is NOT the payload, and a stage stopped at
  # its budget also exits non-zero.
  local payload_done="no" ok_lines inpr_lines sampler_completed sampler_total
  if grep -E 'Download complete: ' "${WORK}/${tag}_aria2c.log" | grep -qv '\[MEMORY\]'; then
    payload_done="yes"
  fi
  ok_lines="$(grep -cE '\|OK  \|' "${WORK}/${tag}_aria2c.log" || true)"
  inpr_lines="$(grep -cE '\|INPR\|' "${WORK}/${tag}_aria2c.log" || true)"
  sampler_completed="$(jq -r '.last_completed_bytes // "n/a"' "${WORK}/${tag}_peers.json" 2>/dev/null || echo n/a)"
  sampler_total="$(jq -r '.last_total_bytes // "n/a"' "${WORK}/${tag}_peers.json" 2>/dev/null || echo n/a)"
  {
    echo "tag=${tag}"
    echo "aria2c_exit_code=${rc}"
    echo "wall_seconds=$((t1 - t0))"
    echo "client_reported_payload_download_complete=${payload_done}"
    echo "download_result_lines_ok=${ok_lines}"
    echo "download_result_lines_in_progress=${inpr_lines}"
    echo "sampler_last_completed_bytes=${sampler_completed}"
    echo "sampler_last_total_bytes=${sampler_total}"
    echo "webseed_mentions_in_client_log=$(grep -ci 'web seed' "${WORK}/${tag}_aria2c.log" || true)"
  } > "${EVID}/07_${tag}_client_status.txt"
  log "[${tag}] client reported payload 'Download complete': ${payload_done} (exit=${rc}, ok_result_lines=${ok_lines}, in_progress_lines=${inpr_lines}, sampler=${sampler_completed}/${sampler_total} bytes)"
  echo "$rc" > "${WORK}/${tag}_rc"; echo "$((t1 - t0))" > "${WORK}/${tag}_seconds"
  local t
  t="$(find "$dir" -maxdepth 1 -name '*.torrent' | head -1)"
  [ -n "$t" ] && cp "$t" "${EVID}/07_${tag}.torrent" && log "[${tag}] metainfo captured: $(basename "$t")"
  grep -iE 'download complete|SEED\(|avg speed|Download Results' "${WORK}/${tag}_aria2c.log" | tail -4 | tee -a "$LOG"
}

step_d_pf_retrieval() {
  hr; log "STAGE D retrieve through Pirate Face (magnet as advertised)"
  if ! have_budget 150; then skip_stage "D_pirateface_normal_retrieval"; return 0; fi
  local magnet; magnet="$(head -1 "${WORK}/magnets.txt")"
  [ -z "$magnet" ] && { log "NO MAGNET FOUND"; return 1; }
  echo "$magnet" > "${WORK}/magnet_page.txt"
  local infohash; infohash="$(echo "$magnet" | grep -oiE 'btih:[0-9a-f]{40}' | cut -d: -f2 | tr 'A-F' 'a-f')"
  echo "$infohash" > "${WORK}/infohash.txt"
  log "infohash: ${infohash}"
  python3 "$H/tracker_announce.py" "$infohash" "${EVID}/07b_tracker_announce_before.json" 2>&1 | tee -a "$LOG"
  run_torrent "$magnet" "${WORK}/pf_run" "D_pf_normal"
  python3 "$H/manifest.py" "${WORK}/pf_run" "${EVID}/08_pf_normal_manifest.json"
}

step_e_source_loss() {
  hr; log "STAGE E simulate primary-source unavailability (this host only)"
  if ! have_budget 180; then skip_stage "E_primary_source_loss"; return 0; fi
  local hosts=("huggingface.co" "www.huggingface.co" "cdn-lfs.huggingface.co"
               "cdn-lfs-us-1.huggingface.co" "cas-bridge.xethub.hf.co" "hf.co"
               "pirateface.co" "www.pirateface.co")
  for h in "${hosts[@]}"; do
    grep -qE "[[:space:]]${h}$" /etc/hosts || echo "0.0.0.0 ${h}" | sudo tee -a /etc/hosts > /dev/null
  done
  log "hosts blocklist:"; grep -E "0\.0\.0\.0" /etc/hosts | tee -a "$LOG"
  {
    echo "--- getent hosts huggingface.co ---"; getent hosts huggingface.co || echo "no resolution"
    echo "--- curl ${HF}/api/models/${REPO} ---"
    curl -sS -L --max-time 20 "${HF}/api/models/${REPO}" || echo "curl failed (expected)"
    echo "--- curl ${PF}/ (web layer) ---"
    curl -sS -L --max-time 20 "${PF}/" -o /dev/null || echo "curl failed (expected)"
    echo "--- tracker name resolution (must still work) ---"
    getent hosts tracker.pirateface.co || echo "tracker DNS failed"
  } 2>&1 | tee "${EVID}/09_source_loss_proof.txt" > /dev/null
  cat "${EVID}/09_source_loss_proof.txt" | tee -a "$LOG"

  local magnet swarm
  magnet="$(cat "${WORK}/magnet_page.txt")"
  swarm="$(printf '%s' "$magnet" | sed -E 's/[&?]ws=[^&]*//g')"
  echo "$swarm" > "${WORK}/magnet_swarm_only.txt"
  log "web-seed stripped magnet: ${swarm}"
  run_torrent "$swarm" "${WORK}/swarm_run" "E_swarm_only"
  python3 "$H/manifest.py" "${WORK}/swarm_run" "${EVID}/10_swarm_only_manifest.json"
}

step_e2_dht_only() {
  hr; log "STAGE E2 tracker unavailable too: DHT/PEX swarm only"
  if ! have_budget 180; then skip_stage "E2_trackerless_dht"; return 0; fi
  grep -qE "[[:space:]]tracker\.pirateface\.co$" /etc/hosts || echo "0.0.0.0 tracker.pirateface.co" | sudo tee -a /etc/hosts > /dev/null
  getent hosts tracker.pirateface.co || echo "tracker DNS blocked (expected)"
  local swarm; swarm="$(cat "${WORK}/magnet_swarm_only.txt")"
  run_torrent "$swarm" "${WORK}/dht_run" "E2_dht_only" "--bt-exclude-tracker=*"
  python3 "$H/manifest.py" "${WORK}/dht_run" "${EVID}/11_dht_only_manifest.json"
}

step_f_compare() {
  hr; log "STAGE F integrity comparison"
  if ! have_budget 120; then skip_stage "F_integrity_comparison"; return 0; fi
  local torrent
  torrent="$(find "${WORK}/swarm_run" "${WORK}/pf_run" -name '*.torrent' | head -1)"
  if [ -n "$torrent" ]; then
    timeout "$(stage_timeout 420)" aria2c --dir="${WORK}/swarm_run" --seed-time=0 --check-integrity=true \
      --bt-enable-lpd=false --enable-dht=false --enable-rpc=false --file-allocation=none \
      --console-log-level=notice "$torrent" > "${WORK}/F_piece_reverify.log" 2>&1
    cp "${WORK}/F_piece_reverify.log" "${EVID}/12_piece_reverify.log"
    grep -iE 'Verification finished|Download complete' "${EVID}/12_piece_reverify.log" | tee -a "$LOG"
  fi
  python3 "$H/page_hashes.py" "${EVID}/05_hf_tree_at_revision.json" "${EVID}/06_canonical_manifest.json" \
    "${EVID}/07_pirateface_page.html" "${EVID}/06b_hash_crosscheck.json" 2>&1 | tee -a "$LOG"
  python3 "$H/compare.py" "${EVID}/06_canonical_manifest.json" "${EVID}/08_pf_normal_manifest.json" \
    "${EVID}/10_swarm_only_manifest.json" "${EVID}/13_comparison.json" 2>&1 | tee -a "$LOG"
  if [ -f "${EVID}/11_dht_only_manifest.json" ]; then
    python3 "$H/compare.py" "${EVID}/06_canonical_manifest.json" "${EVID}/10_swarm_only_manifest.json" \
      "${EVID}/11_dht_only_manifest.json" "${EVID}/13b_dht_only_comparison.json" 2>&1 | tee -a "$LOG"
  fi
  python3 "$H/torrent_identity.py" "${WORK}/pf_run" "${WORK}/swarm_run" "${EVID}/14_torrent_identity.json" 2>&1 | tee -a "$LOG"
}

step_summary() {
  hr; log "SUMMARY"
  python3 "$H/summarize.py" "${EVID}" "${WORK}" "${REPO}" 2>&1 | tee "${EVID}/15_exp18_run_summary.json" | tee -a "$LOG"
}

env_probe
step_a_pin
step_b_canonical
step_c_reference
step_d_pf_retrieval
step_e_source_loss
step_e2_dht_only
step_f_compare
step_summary
if [ -n "${SKIPPED_STAGES}" ]; then log "stages skipped: ${SKIPPED_STAGES}"; else log "all stages executed"; fi
log "harness finished; wall seconds=$(( $(date -u +%s) - STARTED_EPOCH ))"
