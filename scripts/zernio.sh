#!/usr/bin/env bash
# Zernio REST API helper
# Usage:
#   ./zernio.sh profiles
#   ./zernio.sh accounts
#   ./zernio.sh posts
#   ./zernio.sh get /posts
#   ./zernio.sh post /posts '{"content":"hi","publishNow":true,"platforms":[{"platform":"facebook","accountId":"6a39ecf25f7d1751ab57b722"}]}'

set -euo pipefail

ZERNIO_API_KEY="${ZERNIO_API_KEY:-sk_bb6c27fe7e26d4c5a24ffed5d1c8969ffed0cdfb1592264c01cc7739a4a6ba05}"
BASE="https://zernio.com/api/v1"

req() {
  local method="$1" path="$2" body="${3:-}"
  local args=(-X "$method" "$BASE$path"
    -H "Authorization: Bearer $ZERNIO_API_KEY"
    -H "Accept: application/json"
    -w "\n---HTTP:%{http_code}---\n"
    --max-time 30 -sS)
  [ -n "$body" ] && args+=(-H "Content-Type: application/json" -d "$body")
  curl "${args[@]}" | python3 -c "
import sys, json
raw = sys.stdin.read()
parts = raw.rsplit('---HTTP:', 1)
body = parts[0].rstrip()
status = parts[1].rstrip('---\n') if len(parts) > 1 else '?'
try:
    print(json.dumps(json.loads(body), ensure_ascii=False, indent=2))
except Exception:
    print(body)
print(f'---HTTP:{status}---', file=sys.stderr)
"
}

case "${1:-help}" in
  profiles)    req GET /profiles ;;
  accounts)    req GET /accounts ;;
  posts)       req GET /posts ;;
  get)         shift; req GET "$1" "${2:-}" ;;
  post)        shift; req POST "$1" "$2" ;;
  put)         shift; req PUT "$1" "$2" ;;
  delete)      shift; req DELETE "$1" ;;
  help|*)
    cat <<EOF
Zernio API helper
  $0 profiles              - list profiles
  $0 accounts              - list connected accounts
  $0 posts                 - list posts
  $0 get <path> [body]     - GET request
  $0 post <path> <body>    - POST request
  $0 put <path> <body>     - PUT request
  $0 delete <path>         - DELETE request
EOF
    ;;
esac
