#!/usr/bin/env bash
set -euo pipefail

PORT="4096"
USERNAME="${OPENCODE_SERVER_USERNAME:-opencode}"
STATE_DIR="$HOME/.opencode-mobile"
CREDENTIALS_FILE="$STATE_DIR/credentials"
LOG_FILE="$STATE_DIR/server.log"
CONNECTION_FILE=".devcontainer/OPENCODE_MOBILE_CONNECTION.txt"

mkdir -p "$STATE_DIR"

if [[ -n "${OPENCODE_SERVER_PASSWORD:-}" ]]; then
  PASSWORD="$OPENCODE_SERVER_PASSWORD"
elif [[ -f "$CREDENTIALS_FILE" ]]; then
  PASSWORD="$(cat "$CREDENTIALS_FILE")"
else
  PASSWORD="$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"
  printf '%s' "$PASSWORD" > "$CREDENTIALS_FILE"
  chmod 600 "$CREDENTIALS_FILE"
fi

export OPENCODE_SERVER_USERNAME="$USERNAME"
export OPENCODE_SERVER_PASSWORD="$PASSWORD"

if ! pgrep -f "opencode serve.*--port ${PORT}" >/dev/null 2>&1; then
  nohup opencode serve --hostname 0.0.0.0 --port "$PORT" >"$LOG_FILE" 2>&1 &
fi

# Wait briefly for the server socket to become available.
python - <<'PY'
import socket, time
for _ in range(30):
    with socket.socket() as s:
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1", 4096)) == 0:
            raise SystemExit(0)
    time.sleep(0.5)
raise SystemExit("OpenCode server did not start on port 4096")
PY

if [[ -n "${CODESPACE_NAME:-}" ]]; then
  SERVER_URL="https://${CODESPACE_NAME}-${PORT}.app.github.dev"

  # Public visibility is required for a standalone mobile REST client.
  # The OpenCode server itself remains protected with HTTP Basic Auth.
  for _ in {1..10}; do
    if gh codespace ports visibility "${PORT}:public" -c "$CODESPACE_NAME" >/dev/null 2>&1; then
      break
    fi
    sleep 2
  done
else
  SERVER_URL="http://127.0.0.1:${PORT}"
fi

cat > "$CONNECTION_FILE" <<EOF
OpenCode Mobile connection

Server URL: $SERVER_URL
Username: $USERNAME
Password: $PASSWORD

This file is generated locally and is ignored by git. Do not commit or share it.
Server log: $LOG_FILE
EOF

chmod 600 "$CONNECTION_FILE"

printf '\nOpenCode Mobile backend is ready.\n'
printf 'Open %s and copy Server URL, Username, and Password into the Android app.\n\n' "$CONNECTION_FILE"
