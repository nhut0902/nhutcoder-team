# E2B MCP Server — Cấu hình & Hướng dẫn sử dụng

## Tổng quan

- **Endpoint:** `https://e2b.dev/mcp`
- **Transport:** Streamable HTTP (SSE-style response)
- **Auth:** `Authorization: Bearer <E2B_API_KEY>`
- **Server name:** `E2B Docs` (v1.0.0)
- **Protocol version:** `2024-11-05`
- **Stateless:** mỗi request độc lập, không cần giữ session

> ⚠️ **Bảo mật:** API key trong các snippet dưới đây là placeholder `<E2B_API_KEY>`. Hãy thay bằng key thật của bạn và **không commit** vào git. Khuyến nghị đặt trong biến môi trường.

## Các tool có sẵn (read-only)

| Tool | Mô tả |
|---|---|
| `search_e2_b_docs` | Tìm kiếm ngữ nghĩa trong kho tài liệu E2B. Trả về tiêu đề, link và nội dung tóm tắt. |
| `query_docs_filesystem_e2_b_docs` | Chạy câu lệnh shell-like (rg, head, cat, tree, ls, jq...) trên filesystem ảo chứa toàn bộ docs E2B. Dùng để đọc trang đầy đủ theo path `.mdx`. |

Lưu ý: đây là MCP **tài liệu E2B** (search/retrieve docs), KHÔNG phải MCP để tạo/spawn sandbox. Nếu muốn tạo sandbox từ MCP, dùng `Sandbox.create({ mcp: {...} })` trong SDK E2B — xem `docs/mcp/quickstart`.

---

## 1. Claude Desktop (claude_desktop_config.json)

**Vị trí file:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "e2b-docs": {
      "url": "https://e2b.dev/mcp",
      "headers": {
        "Authorization": "Bearer <E2B_API_KEY>"
      }
    }
  }
}
```

Khởi động lại Claude Desktop → sẽ thấy icon 🔌 với 2 tool `search_e2_b_docs` và `query_docs_filesystem_e2_b_docs`.

## 2. Cursor (mcp.json)

**Vị trí:** `~/.cursor/mcp.json` (toàn bộ user) hoặc `.cursor/mcp.json` trong project.

```json
{
  "mcpServers": {
    "e2b-docs": {
      "url": "https://e2b.dev/mcp",
      "headers": {
        "Authorization": "Bearer <E2B_API_KEY>"
      }
    }
  }
}
```

Trong Cursor: `Settings → Cursor Settings → Features → MCP` để verify server đã connected.

## 3. VS Code (GitHub Copilot Chat / MCP extension)

**Vị trí:** `.vscode/mcp.json` trong workspace hoặc `settings.json`.

```json
{
  "servers": {
    "e2b-docs": {
      "url": "https://e2b.dev/mcp",
      "headers": {
        "Authorization": "Bearer <E2B_API_KEY>"
      }
    }
  }
}
```

## 4. Cline / Roo Code / Continue

Cùng định dạng `url` + `headers`:

```json
{
  "mcpServers": {
    "e2b-docs": {
      "url": "https://e2b.dev/mcp",
      "headers": {
        "Authorization": "Bearer <E2B_API_KEY>"
      }
    }
  }
}
```

---

## 5. Test bằng Python (MCP SDK)

```bash
pip install "mcp[cli]" httpx
```

```python
# /home/z/my-project/scripts/test_e2b_mcp.py
import asyncio, os
from datetime import timedelta
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

E2B_API_KEY = os.environ["E2B_API_KEY"]  # export E2B_API_KEY=...

async def main():
    async with streamablehttp_client(
        url="https://e2b.dev/mcp",
        headers={"Authorization": f"Bearer {E2B_API_KEY}"},
        timeout=timedelta(seconds=60),
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            result = await session.call_tool(
                "search_e2_b_docs",
                {"query": "sandbox quickstart"},
            )
            for block in result.content:
                print("---")
                print(block.text)

asyncio.run(main())
```

Chạy:
```bash
export E2B_API_KEY=e2b_xxx...
python /home/z/my-project/scripts/test_e2b_mcp.py
```

## 6. Test bằng Node.js / TypeScript

```bash
npm i @modelcontextprotocol/sdk
```

```typescript
// /home/z/my-project/scripts/test_e2b_mcp.ts
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const apiKey = process.env.E2B_API_KEY!;

const transport = new StreamableHTTPClientTransport(
  new URL("https://e2b.dev/mcp"),
  { requestInit: { headers: { Authorization: `Bearer ${apiKey}` } } }
);

const client = new Client({ name: "e2b-test", version: "1.0.0" });
await client.connect(transport);

const tools = await client.listTools();
console.log("Tools:", tools.tools.map((t) => t.name));

const r = await client.callTool({ name: "search_e2_b_docs", arguments: { query: "sandbox quickstart" } });
console.log(JSON.stringify(r.content, null, 2));

await client.close();
```

Chạy:
```bash
export E2B_API_KEY=e2b_xxx...
npx tsx /home/z/my-project/scripts/test_e2b_mcp.ts
```

## 7. Test nhanh bằng curl (1 dòng)

```bash
curl -sS -X POST https://e2b.dev/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $E2B_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

---

## Kết quả test đã chạy (2026-06-24)

- ✅ `initialize` → HTTP 200, server `E2B Docs v1.0.0`, protocol `2024-11-05`
- ✅ `tools/list` → 2 tool: `search_e2_b_docs`, `query_docs_filesystem_e2_b_docs`
- ✅ `tools/call search_e2_b_docs({query:"sandbox quickstart"})` → trả về 8 đoạn docs với link `e2b.mintlify.app/...`

API key bạn cung cấp **hợp lệ và hoạt động**.
