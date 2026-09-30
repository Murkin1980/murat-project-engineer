#!/usr/bin/env bash
# EXP-18 — Pirate Face model resilience: bounded retrieval harness.
#
# Purpose: produce reproducible, machine-readable evidence for the EXP-18 contract
# (experiments/exp-18-pirateface-model-resilience/README.md) without touching
# production systems.
#
# Stages
#   A  pin the Hugging Face repository + exact revision, record license/files
#   B  download the canonical artifact through the normal Hugging Face path
#   C  record the Pirate Face distribution reference for the same repository
#   D  retrieve the model through the Pirate Face path (as advertised)
#   E  bounded simulation of primary-source loss (HF + Pirate Face web blocked,
#      magnet web-seed stripped) -> swarm + tracker only
#   F  deterministic file-set and SHA-256 comparison + piece re-verification
#
# Nothing here is imported by application code; it is a one-off experiment
# harness. It installs nothing into the repository.
#
# Usage: bash run_exp18.sh            (writes evidence/ in the experiment folder)

set -uo pipefail

REPO="sentence-transformers/all-MiniLM-L6-v2"
HF="https://huggingface.co"
PF="https://pirateface.co"
PF_PAGE="${PF}/${REPO}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVID="${ROOT}/evidence"
WORK="${RUNNER_TEMP:-/tmp}/exp18-work"
LOG="${EVID}/00_run_transcript.log"
TORRENT_TIMEOUT=900   # seconds without progress before giving up
RT="${RT:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
MARKET="$(date -u +%s)"

mkdir -p "$EVID" "$WORK"
: > "$LOG"

log() { printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$*" | tee -a "$LOG"; }
hr()  { log "-------------------------------------------------------------"; }

# ---------------------------------------------------------------- environment
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
  } | tee -a "$LOG" > "${EVID}/01_environment.txt"
}

# ------------------------------------------------------- A: pin HF + revision
step_a_pin() {
  hr; log "STAGE A pin repository, revision, license, expected files"
  curl -sS -L --max-time 60 "${HF}/api/models/${REPO}" -o "${EVID}/02_hf_model_metadata.json"
  REV="$(jq -r '.sha' "${EVID}/02_hf_model_metadata.json")"
  log "HF repository      : ${REPO}"
  log "HF pinned revision : ${REV}"

  curl -sS -L --max-time 60 "${HF}/api/models/${REPO}/revision/${REV}" \
    -o "${EVID}/03_hf_model_at_revision.json"

  jq '{id, sha, private, gated, downloads, lastModified, license: (.cardData.license // (.tags[]? | select(startswith("license:")))), tags}' \
    "${EVID}/02_hf_model_metadata.json" > "${EVID}/04_hf_license_evidence.json"
  log "license evidence   : $(jq -c '{license}' "${EVID}/04_hf_license_evidence.json")"

  curl -sS -L --max-time 90 "${HF}/api/models/${REPO}/tree/${REV}?recursive=true&expand=true" \
    -o "${EVID}/05_hf_tree_at_revision.json"
  log "tree entries at revision: $(jq 'length' "${EVID}/05_hf_tree_at_revision.json")"
  echo "$REV" > "${WORK}/REV"
}

# --------------------------------------------- B: canonical HF artifact bytes
step_b_canonical() {
  hr; log "STAGE B download canonical artifact through normal Hugging Face path"
  local rev; rev="$(cat "${WORK}/REV")"
  local dir="${WORK}/canonical"; mkdir -p "$dir"
  cd "$dir" || return 1

  local started; started="$(date -u +%s)"
  jq -r '.[] | select(.type=="file") | .path' "${EVID}/05_hf_tree_at_revision.json" |
  while IFS= read -r p; do
    mkdir -p "$(dirname "$p")"
    local url="${HF}/${REPO}/resolve/${rev}/${p}"
    local code
    code="$(curl -sS -L --retry 3 --retry-delay 2 --max-time 600 -w '%{http_code}' -o "$p" "$url")"
    echo "$p	$code	$(stat -c%s "$p" 2>/dev/null || echo 0)" >> "${WORK}/hf_download_log.tsv"
    log "  hf fetch ${code} ${p} ($(stat -c%s "$p" 2>/dev/null || echo 0) bytes)"
  done
  local ended; ended="$(date -u +%s)"
  log "HF canonical download wall seconds: $((ended - started))"

  python3 "${ROOT}/harness/manifest.py" "$dir" "${EVID}/06_canonical_manifest.json"
  log "canonical files: $(jq '.files | length' "${EVID}/06_canonical_manifest.json")"
  cd "$ROOT" || return 1
}

# ---------------------------------------- C: Pirate Face distribution reference
step_c_reference() {
  hr; log "STAGE C record Pirate Face distribution reference"
  curl -sS -L --max-time 60 -w 'http_status=%{http_code}\n' "$PF_PAGE" -o "${EVID}/07_pirateface_page.html" \
    2>&1 | tee -a "$LOG"

  # magnet URIs referenced by the page (HTML-escaped ampersands decoded)
  grep -oE "magnet:\?[^\"'<>[:space:]]+" "${EVID}/07_pirateface_page.html" \
    | sed 's/&amp;/\&/g' | sort -u > "${WORK}/magnets.txt"
  log "magnet URIs found: $(wc -l < "${WORK}/magnets.txt")"
  head -5 "${WORK}/magnets.txt" | tee -a "$LOG"

  grep -oiE '(sha-?256|checksum)[^<]{0,120}' "${EVID}/07_pirateface_page.html" \
    | head -20 > "${WORK}/checksum_mentions.txt" || true
  grep -oiE '[0-9a-f]{64}' "${EVID}/07_pirateface_page.html" | sort -u > "${WORK}/sha256_in_page.txt" || true
  log "sha256-like strings on page: $(wc -l < "${WORK}/sha256_in_page.txt")"

  # probe a few plausible structured endpoints; record status only
  : > "${WORK}/endpoint_probe.txt"
  for u in "${PF}/api/models/${REPO}" "${PF}/api/model/${REPO}" "${PF}/api/v1/models/${REPO}" \
           "${PF}/s/${REPO}" "${PF}/package.sh" "${PF}/how-it-works"; do
    printf '%s\t%s\n' "$u" \
      "$(curl -sS -L --max-time 30 -o /dev/null -w '%{http_code}' "$u" 2>/dev/null)" >> "${WORK}/endpoint_probe.txt"
  done
  cat "${WORK}/endpoint_probe.txt" | tee -a "$LOG"
}

# ------------------------------------------------ D: Pirate Face retrieval
# $1 = magnet, $2 = target dir, $3 = tag
run_torrent() {
  local magnet="$1" dir="$2" tag="$3"
  mkdir -p "$dir"
  log "[${tag}] aria2c start; magnet=${magnet}"
  local t0 t1
  t0="$(date -u +%s)"
  timeout "$((TORRENT_TIMEOUT + 300))" aria2c \
    --dir="$dir" \
    --seed-time=0 \
    --bt-stop-timeout="${TORRENT_TIMEOUT}" \
    --bt-save-metadata=true \
    --bt-enable-lpd=false \
    --enable-dht=true \
    --dht-entry-point=router.bittorrent.com:6881 \
    --dht-entry-point=router.utorrent.com:6881 \
    --dht-entry-point=dht.transmissionbt.com:6881 \
    --dht-listen-port=6881 \
    --listen-port=6881 \
    --enable-rpc=false \
    --bt-tracker-connect-timeout=20 \
    --bt-tracker-timeout=30 \
    --bt-tracker-interval=20 \
    --enable-peer-exchange=true \
    --bt-max-peers=100 \
    --file-allocation=none \
    --max-connection-per-server=16 \
    --split=16 \
    --console-log-level=notice \
    --summary-interval=15 \
    --auto-file-renaming=false \
    --allow-overwrite=true \
    --check-integrity=false \
    "$magnet" > "${WORK}/${tag}_aria2c.log" 2>&1
  local rc=$?
  t1="$(date -u +%s)"
  log "[${tag}] aria2c exit=${rc} wall_seconds=$((t1 - t0))"
  cp "${WORK}/${tag}_aria2c.log" "${EVID}/07_${tag}_aria2c.log"
  echo "$rc" > "${WORK}/${tag}_rc"
  echo "$((t1 - t0))" > "${WORK}/${tag}_seconds"

  # peers observed by the client (mask last two octets)
  grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "${WORK}/${tag}_aria2c.log" 2>/dev/null \
    | sort -u | sed -E 's/^([0-9]+\.[0-9]+)\.[0-9]+\.[0-9]+$/\1.x.x/' | sort -u > "${WORK}/${tag}_peers.txt"
  log "[${tag}] distinct peer networks observed: $(wc -l < "${WORK}/${tag}_peers.txt")"
  grep -icE 'webseed' "${WORK}/${tag}_aria2c.log" > "${WORK}/${tag}_webseed_mentions" 2>/dev/null || echo 0 > "${WORK}/${tag}_webseed_mentions"
  log "[${tag}] log lines mentioning webseed: $(cat "${WORK}/${tag}_webseed_mentions")"
  grep -iE 'download complete|download results|SEEDERS|CN:' "${WORK}/${tag}_aria2c.log" | tail -5 | tee -a "$LOG"
}

step_d_pf_retrieval() {
  hr; log "STAGE D retrieve through Pirate Face (magnet as advertised by the page)"
  local magnet; magnet="$(head -1 "${WORK}/magnets.txt")"
  if [ -z "$magnet" ]; then log "NO MAGNET FOUND ON PAGE"; return 1; fi
  echo "$magnet" > "${WORK}/magnet_page.txt"
  local infohash; infohash="$(echo "$magnet" | grep -oiE 'btih:[0-9a-f]{40}' | cut -d: -f2 | tr 'A-F' 'a-f')"
  echo "$infohash" > "${WORK}/infohash.txt"
  log "infohash: ${infohash}"
  run_torrent "$magnet" "${WORK}/pf_run" "D_pf_normal"
  python3 "${ROOT}/harness/manifest.py" "${WORK}/pf_run" "${EVID}/08_pf_normal_manifest.json"
  log "Pirate Face (normal) files: $(jq '.files | length' "${EVID}/08_pf_normal_manifest.json")"
}

# ------------------------------ E: bounded simulation of primary-source loss
step_e_source_loss() {
  hr; log "STAGE E simulate primary-source unavailability (bounded, this host only)"
  # 1. Make the normal Hugging Face retrieval path unusable on this host.
  local hosts=("huggingface.co" "www.huggingface.co" "cdn-lfs.huggingface.co"
               "cdn-lfs-us-1.huggingface.co" "cas-bridge.xethub.hf.co" "hf.co")
  for h in "${hosts[@]}"; do
    if ! grep -qE "[[:space:]]${h}$" /etc/hosts; then
      echo "0.0.0.0 ${h}" | sudo tee -a /etc/hosts > /dev/null
    fi
  done
  # 2. Make Pirate Face's web layer unusable too, so only swarm + tracker remain.
  for h in "pirateface.co" "www.pirateface.co"; do
    if ! grep -qE "[[:space:]]${h}$" /etc/hosts; then
      echo "0.0.0.0 ${h}" | sudo tee -a /etc/hosts > /dev/null
    fi
  done
  log "hosts blocklist now:"; grep -E "0\.0\.0\.0" /etc/hosts | tee -a "$LOG"

  log "proof: resolution + fetch of Hugging Face must fail"
  {
    echo "--- getent hosts huggingface.co ---"; getent hosts huggingface.co || echo "no resolution"
    echo "--- curl https://huggingface.co/api/models/${REPO} ---"
    curl -sS -L --max-time 20 "${HF}/api/models/${REPO}" || echo "curl failed (expected)"
    echo "--- curl https://pirateface.co/ (web layer) ---"
    curl -sS -L --max-time 20 "${PF}/" -o /dev/null || echo "curl failed (expected)"
    echo "--- tracker name resolution (must still work) ---"
    getent hosts tracker.pirateface.co || echo "tracker DNS failed"
  } 2>&1 | tee "${EVID}/09_source_loss_proof.txt" | tee -a "$LOG" > /dev/null

  # 3. Strip any web-seed from the magnet: only peers may serve data.
  local magnet; magnet="$(cat "${WORK}/magnet_page.txt")"
  local swarm_magnet; swarm_magnet="$(printf '%s' "$magnet" | sed -E 's/[&?]ws=[^&]*//g')"
  echo "$swarm_magnet" > "${WORK}/magnet_swarm_only.txt"
  log "web-seed stripped magnet: ${swarm_magnet}"

  run_torrent "$swarm_magnet" "${WORK}/swarm_run" "E_swarm_only"
  python3 "${ROOT}/harness/manifest.py" "${WORK}/swarm_run" "${EVID}/10_swarm_only_manifest.json"
  log "swarm-only files: $(jq '.files | length' "${EVID}/10_swarm_only_manifest.json")"
}

# --------------------------- F: piece re-verification + deterministic compare
step_f_compare() {
  hr; log "STAGE F integrity comparison"
  # re-verify all pieces of the swarm-only download against the torrent metadata
  local torrent; torrent="$(find "${WORK}/swarm_run" -name '*.torrent' | head -1)"
  if [ -n "$torrent" ]; then
    mkdir -p "${WORK}/reverify"
    timeout 600 aria2c --dir="${WORK}/swarm_run" --seed-time=0 --check-integrity=true \
      --bt-enable-lpd=false --enable-dht=false --enable-rpc=false --file-allocation=none \
      --console-log-level=notice "$torrent" > "${WORK}/F_piece_reverify.log" 2>&1
    log "piece re-verify exit=$? ; $(grep -icE 'piece|complete|integrity' "${WORK}/F_piece_reverify.log") relevant log lines"
    cp "${WORK}/F_piece_reverify.log" "${EVID}/11_piece_reverify.log"
  else
    log "no .torrent metadata captured; skipping piece re-verification"
    echo "no torrent metadata" > "${EVID}/11_piece_reverify.log"
  fi

  python3 "${ROOT}/harness/compare.py" \
    "${EVID}/06_canonical_manifest.json" \
    "${EVID}/08_pf_normal_manifest.json" \
    "${EVID}/10_swarm_only_manifest.json" \
    "${EVID}/12_comparison.json" 2>&1 | tee -a "$LOG"

  python3 "${ROOT}/harness/torrent_identity.py" "${WORK}/pf_run" "${WORK}/swarm_run" \
    "${EVID}/13_torrent_identity.json" 2>&1 | tee -a "$LOG"
}

# ------------------------------------------------------------------- summary
step_summary() {
  hr; log "SUMMARY"
  python3 "${ROOT}/harness/summarize.py" "${EVID}" "${WORK}" "${REPO}" 2>&1 | tee "${EVID}/14_exp18_run_summary.json" | tee -a "$LOG"
}

env_probe
step_a_pin
step_b_canonical
step_c_reference
step_d_pf_retrieval
step_e_source_loss
step_f_compare
step_summary
log "harness finished"
