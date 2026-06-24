#!/usr/bin/env bash
# E2B MCP client helper - stateless, single-shot calls
# Usage:
#   ./e2b_mcp.sh tools/list
#   ./e2b_mcp.sh search "sandbox quickstart"
#   ./e2b_mcp.sh query 'rg -il "rate limit" /'
#   ./e2b_mcp.sh raw '{"jsonrpc":"2.0","id":99,"method":"tools/list","params":{}}'

set -euo pipefail

E2B_API_KEY="${E2B_API_KEY:-e2b_e211aca6616cd7e18155af3973539bf7b9bd7772}"
ENDPOINT="https://e2b.dev/mcp"

call() {
  local payload="$1"
  curl -sS --max-time 60 -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Authorization: Bearer $E2B_API_KEY" \
    -H "MCP-Protocol-Version: 2024-11-05" \
    -d "$payload"
}

# Extract just the JSON-RPC data field from SSE response
extract_data() {
  sed -n 's/^data: //p' | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)['result'], ensure_ascii=False, indent=2))" 2>/dev/null || sed -n 's/^data: //p'
}

case "${1:-help}" in
  tools/list|list)
    call '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | extract_data
    ;;
  search)
    shift
    local_query="$*"
    call "$(python3 -c "import json,sys; print(json.dumps({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'search_e2_b_docs','arguments':{'query':sys.argv[1]}}}))" "$local_query")" | extract_data
    ;;
  query)
    shift
    local_cmd="$*"
    call "$(python3 -c "import json,sys; print(json.dumps({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'query_docs_filesystem_e2_b_docs','arguments':{'command':sys.argv[1]}}}))" "$local_cmd")" | extract_data
    ;;
  raw)
    shift
    call "$*"
    ;;
  help|*)
    echo "E2B MCP helper"
    echo "Usage:"
    echo "  $0 tools/list"
    echo "  $0 search <query>"
    echo "  $0 query <shell command on docs fs>"
    echo "  $0 raw <json-rpc payload>"
    ;;
esac
