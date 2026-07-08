#!/home/z/.venv/bin/python3
"""Write 8 custom HTML compositions for Context7 video.
Each HTML has: dark theme, CSS animations, screenshots, Vietnamese text, HyperFrames syntax.
Then render each via hyperframes CLI."""
import os, json, subprocess, shutil

OUT_DIR = "/home/z/my-project/download/context7_html"
os.makedirs(OUT_DIR, exist_ok=True)
SHOTS = "/home/z/my-project/download/context7_shots"

# Copy screenshots to each scene dir
for i in range(1, 5):
    src = f"{SHOTS}/0{i}_{'gh_title' if i==1 else 'gh_files' if i==2 else 'readme' if i==3 else 'website'}.png"
    if os.path.exists(src):
        shutil.copy(src, f"{OUT_DIR}/shot_{i}.png")

# Load durations
with open("/tmp/context7_durations.json") as f:
    durations = json.load(f)["durations"]

scenes = ["s1","s2","s3","s4","s5","s6","s7","s8"]
starts = {}
cum = 0
for s in scenes:
    starts[s] = cum
    cum += durations[s]
total = cum

# Common CSS
COMMON_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; }
body { font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; }
"""

# Scene HTML templates (each is self-contained with animations)
SCENE_HTML = {
    "s1": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a0e1a 0%, #1a1040 50%, #0a0e1a 100%); color: #fff; }}
.orb {{ position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.4; }}
.orb1 {{ width: 400px; height: 400px; background: #4285f4; top: -100px; left: -100px; }}
.orb2 {{ width: 500px; height: 500px; background: #7c5cff; bottom: -150px; right: -150px; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #4285f4; border-radius: 8px; font-size: 34px; font-weight: 700; color: #4285f4; }}
.title {{ position: absolute; top: 280px; left: 50%; transform: translateX(-50%); font-size: 160px; font-weight: 900; background: linear-gradient(135deg, #4285f4, #7c5cff, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }}
.subtitle {{ position: absolute; top: 500px; left: 50%; transform: translateX(-50%); font-size: 48px; color: #cbd5e1; text-align: center; }}
.stats {{ position: absolute; top: 650px; left: 80px; right: 80px; display: flex; justify-content: space-around; }}
.stat {{ text-align: center; }}
.stat .num {{ font-size: 60px; font-weight: 900; color: #fac850; }}
.stat .label {{ font-size: 28px; color: #94a3b8; }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; margin-bottom: 10px; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #4285f4; border-radius: 6px; font-size: 28px; font-weight: 700; color: #4285f4; }}
/* Animations */
@keyframes fadeUp {{ from {{ opacity: 0; transform: translate(-50%, 30px); }} to {{ opacity: 1; transform: translate(-50%, 0); }} }}
@keyframes glow {{ from {{ filter: drop-shadow(0 0 0 transparent); }} to {{ filter: drop-shadow(0 0 40px rgba(124,92,255,0.6)); }} }}
.header {{ animation: fadeUp 0.6s ease-out 0s both; }}
.title {{ animation: fadeUp 0.8s ease-out 0.2s both, glow 1s ease-out 1s both; }}
.subtitle {{ animation: fadeUp 0.6s ease-out 0.6s both; }}
.stats {{ animation: fadeUp 0.6s ease-out 0.9s both; }}
.sub {{ animation: fadeUp 0.6s ease-out 1.2s both; }}
.footer {{ animation: fadeUp 0.4s ease-out 1.5s both; }}
</style></head><body>
<div class="orb orb1"></div><div class="orb orb2"></div>
<div class="header">🚀 58K STARS GITHUB</div>
<div class="title">Context7</div>
<div class="subtitle">Up-to-date docs for AI agents</div>
<div class="stats">
<div class="stat"><div class="num">58.7K</div><div class="label">stars</div></div>
<div class="stat"><div class="num">2.7K</div><div class="label">forks</div></div>
<div class="stat"><div class="num">TS</div><div class="label">language</div></div>
</div>
<div class="sub"><p>MCP Server hàng đầu cho AI coding editors</p><p>Ngăn hallucinations bằng real docs</p></div>
<div class="footer">UPSTASH · MCP · APACHE-2.0</div>
</body></html>''',

    "s2": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a0e1a 0%, #0d1520 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #7c5cff; border-radius: 8px; font-size: 34px; font-weight: 700; color: #7c5cff; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 64px; font-weight: 800; color: #fff; }}
.shot {{ position: absolute; top: 310px; left: 50%; transform: translateX(-50%); width: 950px; border-radius: 24px; border: 4px solid rgba(124,92,255,0.5); box-shadow: 0 20px 60px rgba(124,92,255,0.3); }}
.card {{ position: absolute; top: 820px; left: 80px; right: 80px; background: rgba(20,15,35,0.8); border: 2px solid #7c5cff; border-radius: 18px; padding: 30px; }}
.card h2 {{ font-size: 42px; color: #7c5cff; margin-bottom: 15px; }}
.card p {{ font-size: 36px; color: #e0e7ff; margin-bottom: 10px; }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; margin-bottom: 10px; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #7c5cff; border-radius: 6px; font-size: 28px; font-weight: 700; color: #7c5cff; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translate(-50%, 30px); }} to {{ opacity: 1; transform: translate(-50%, 0); }} }}
@keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-50%) scale(0.95); }} to {{ opacity: 1; transform: translateX(-50%) scale(1); }} }}
.header {{ animation: fadeUp 0.5s ease-out 0s both; }}
.title {{ animation: fadeUp 0.5s ease-out 0.2s both; }}
.shot {{ animation: slideIn 0.6s ease-out 0.4s both; }}
.card {{ animation: fadeUp 0.5s ease-out 0.8s both; }}
.sub {{ animation: fadeUp 0.5s ease-out 1.1s both; }}
.footer {{ animation: fadeUp 0.4s ease-out 1.4s both; }}
</style></head><body>
<div class="header">GITHUB REPO</div>
<div class="title">upstash/context7</div>
<img class="shot" src="shot_1.png" alt="GitHub">
<div class="card">
<h2>📋 Thông tin:</h2>
<p>• 58,698 stars · 2,754 forks</p>
<p>• TypeScript · Apache-2.0</p>
<p>• MCP Server cho AI editors</p>
<p>• Topics: llm, mcp, vibe-coding</p>
</div>
<div class="sub"><p>Repo: github.com/upstash/context7</p><p>Documentation platform cho AI coding</p></div>
<div class="footer">UPSTASH · OPEN SOURCE</div>
</body></html>''',

    "s3": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #1a0510 0%, #0a0e1a 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #f05a46; border-radius: 8px; font-size: 34px; font-weight: 700; color: #f05a46; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 70px; font-weight: 800; text-align: center; }}
.problem {{ position: absolute; top: 380px; left: 80px; right: 80px; }}
.row {{ background: rgba(30,10,15,0.7); border: 2px solid #f05a46; border-radius: 14px; padding: 24px 32px; margin-bottom: 16px; display: flex; align-items: center; gap: 24px; }}
.row .icon {{ font-size: 56px; }}
.row .text {{ font-size: 38px; }}
.row .text strong {{ color: #f05a46; }}
.solution {{ position: absolute; top: 880px; left: 80px; right: 80px; background: rgba(10,30,15,0.8); border: 3px solid #50c878; border-radius: 18px; padding: 30px; }}
.solution h2 {{ font-size: 40px; color: #50c878; margin-bottom: 12px; }}
.solution p {{ font-size: 36px; color: #fff; }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #50c878; border-radius: 6px; font-size: 28px; font-weight: 700; color: #50c878; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes slideRight {{ from {{ opacity: 0; transform: translateX(-30px); }} to {{ opacity: 1; transform: translateX(0); }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.5s 0.2s both; }}
.row {{ animation: slideRight 0.5s both; }}
.row:nth-child(1) {{ animation-delay: 0.4s; }}
.row:nth-child(2) {{ animation-delay: 0.6s; }}
.row:nth-child(3) {{ animation-delay: 0.8s; }}
.solution {{ animation: fadeUp 0.6s 1.2s both; }}
.sub {{ animation: fadeUp 0.5s 1.6s both; }}
.footer {{ animation: fadeUp 0.4s 1.9s both; }}
</style></head><body>
<div class="header">⚠️ VẤN ĐỀ</div>
<div class="title">AI Hallucination</div>
<div class="problem">
<div class="row"><span class="icon">🤖</span><span class="text">AI dùng <strong>docs cũ</strong> → code sai</span></div>
<div class="row"><span class="icon">📚</span><span class="text">API changed → <strong>outdated code</strong></span></div>
<div class="row"><span class="icon">❌</span><span class="text">Không verify → <strong>hallucination</strong></span></div>
</div>
<div class="solution">
<h2>✅ Context7 giải pháp:</h2>
<p>Inject real-time library docs vào AI context</p>
</div>
<div class="sub"><p>Context7 fetch docs mới nhất → chính xác</p></div>
<div class="footer">NO MORE HALLUCINATIONS</div>
</body></html>''',

    "s4": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a1a10 0%, #0a0e1a 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #50c878; border-radius: 8px; font-size: 34px; font-weight: 700; color: #50c878; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 60px; font-weight: 800; color: #fff; }}
.codeblock {{ position: absolute; top: 320px; left: 60px; right: 60px; background: #0d1117; border: 3px solid #50c878; border-radius: 16px; padding: 36px; }}
.codeblock .label {{ font-size: 28px; color: #50c878; font-weight: 700; margin-bottom: 16px; }}
.codeblock .line {{ font-family: 'Courier New', monospace; font-size: 34px; margin-bottom: 12px; }}
.codeblock .prompt {{ color: #50c878; }}
.codeblock .cmd {{ color: #fac850; }}
.codeblock .comment {{ color: #64748b; }}
.steps {{ position: absolute; top: 750px; left: 80px; right: 80px; }}
.step {{ background: rgba(10,30,20,0.7); border: 2px solid #50c878; border-radius: 14px; padding: 20px 30px; margin-bottom: 14px; display: flex; align-items: center; gap: 20px; }}
.step .num {{ font-size: 48px; font-weight: 900; color: #50c878; }}
.step .text {{ font-size: 36px; }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #50c878; border-radius: 6px; font-size: 28px; font-weight: 700; color: #50c878; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes typeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.5s 0.2s both; }}
.codeblock {{ animation: fadeUp 0.5s 0.4s both; }}
.codeblock .line {{ animation: typeIn 0.3s both; }}
.codeblock .line:nth-child(2) {{ animation-delay: 0.6s; }}
.codeblock .line:nth-child(3) {{ animation-delay: 0.8s; }}
.codeblock .line:nth-child(4) {{ animation-delay: 1.0s; }}
.step {{ animation: fadeUp 0.4s both; }}
.step:nth-child(1) {{ animation-delay: 1.2s; }}
.step:nth-child(2) {{ animation-delay: 1.4s; }}
.step:nth-child(3) {{ animation-delay: 1.6s; }}
.sub {{ animation: fadeUp 0.5s 1.8s both; }}
.footer {{ animation: fadeUp 0.4s 2.0s both; }}
</style></head><body>
<div class="header">💡 CÁCH DÙNG</div>
<div class="title">Đơn giản: "use context7"</div>
<div class="codeblock">
<div class="label">💬 Trong prompt:</div>
<div class="line prompt">User: How to use Next.js 15 App Router?</div>
<div class="line prompt">User: use context7</div>
<div class="line comment"># → Context7 auto-injects latest docs</div>
<div class="line cmd">→ AI generates accurate code ✅</div>
</div>
<div class="steps">
<div class="step"><span class="num">1</span><span class="text">Thêm "use context7" vào prompt</span></div>
<div class="step"><span class="num">2</span><span class="text">Config auto-invocation rule</span></div>
<div class="step"><span class="num">3</span><span class="text">Agent tự gọi MCP server</span></div>
</div>
<div class="sub"><p>Chỉ cần "use context7" → docs tự inject</p></div>
<div class="footer">EASY · JUST ADD 2 WORDS</div>
</body></html>''',

    "s5": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a0e2a 0%, #0a0e1a 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #4285f4; border-radius: 8px; font-size: 34px; font-weight: 700; color: #4285f4; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 64px; font-weight: 800; color: #fff; }}
.tools {{ position: absolute; top: 340px; left: 80px; right: 80px; }}
.tool {{ background: rgba(15,20,45,0.8); border: 2px solid #4285f4; border-radius: 18px; padding: 30px; margin-bottom: 20px; }}
.tool .name {{ font-size: 46px; font-weight: 700; color: #4285f4; margin-bottom: 10px; }}
.tool .desc {{ font-size: 36px; color: #cbd5e1; }}
.tool .code {{ font-family: monospace; font-size: 32px; color: #50c878; margin-top: 8px; }}
.shot {{ position: absolute; top: 850px; left: 50%; transform: translateX(-50%); width: 950px; border-radius: 20px; border: 4px solid rgba(66,133,244,0.5); }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #4285f4; border-radius: 6px; font-size: 28px; font-weight: 700; color: #4285f4; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-50%) scale(0.95); }} to {{ opacity: 1; transform: translateX(-50%) scale(1); }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.5s 0.2s both; }}
.tool {{ animation: fadeUp 0.5s both; }}
.tool:nth-child(1) {{ animation-delay: 0.4s; }}
.tool:nth-child(2) {{ animation-delay: 0.7s; }}
.shot {{ animation: slideIn 0.6s 1.0s both; }}
.sub {{ animation: fadeUp 0.5s 1.4s both; }}
.footer {{ animation: fadeUp 0.4s 1.7s both; }}
</style></head><body>
<div class="header">🛠️ HAI TOOL CHÍNH</div>
<div class="title">MCP Tools</div>
<div class="tools">
<div class="tool">
<div class="name">resolve-library-id</div>
<div class="desc">Tìm đúng thư viện trong Context7</div>
<div class="code">→ Returns library ID + metadata</div>
</div>
<div class="tool">
<div class="name">query-docs</div>
<div class="desc">Fetch documentation cụ thể theo ID</div>
<div class="code">→ Returns latest API docs + examples</div>
</div>
</div>
<img class="shot" src="shot_3.png" alt="README">
<div class="sub"><p>resolve-library-id → query-docs → accurate code</p></div>
<div class="footer">2 TOOLS · REAL-TIME DOCS</div>
</body></html>''',

    "s6": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #100a20 0%, #0a0e1a 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #9b72dc; border-radius: 8px; font-size: 34px; font-weight: 700; color: #9b72dc; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 60px; font-weight: 800; color: #fff; }}
.integrations {{ position: absolute; top: 340px; left: 80px; right: 80px; display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
.int {{ background: rgba(25,15,40,0.8); border: 2px solid #9b72dc; border-radius: 16px; padding: 24px 36px; text-align: center; width: 420px; }}
.int .icon {{ font-size: 64px; margin-bottom: 12px; }}
.int .name {{ font-size: 40px; font-weight: 700; color: #9b72dc; }}
.int .desc {{ font-size: 30px; color: #94a3b8; margin-top: 8px; }}
.config {{ position: absolute; top: 850px; left: 60px; right: 60px; background: #0d1117; border: 3px solid #9b72dc; border-radius: 16px; padding: 30px; }}
.config .label {{ font-size: 30px; color: #9b72dc; font-weight: 700; margin-bottom: 12px; }}
.config .code {{ font-family: monospace; font-size: 30px; color: #50c878; line-height: 1.6; }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #9b72dc; border-radius: 6px; font-size: 28px; font-weight: 700; color: #9b72dc; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes popIn {{ from {{ opacity: 0; transform: scale(0.8); }} to {{ opacity: 1; transform: scale(1); }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.5s 0.2s both; }}
.int {{ animation: popIn 0.5s both; }}
.int:nth-child(1) {{ animation-delay: 0.4s; }}
.int:nth-child(2) {{ animation-delay: 0.55s; }}
.int:nth-child(3) {{ animation-delay: 0.7s; }}
.int:nth-child(4) {{ animation-delay: 0.85s; }}
.config {{ animation: fadeUp 0.5s 1.1s both; }}
.sub {{ animation: fadeUp 0.5s 1.4s both; }}
.footer {{ animation: fadeUp 0.4s 1.7s both; }}
</style></head><body>
<div class="header">🔗 TÍCH HỢP</div>
<div class="title">MCP-Compatible Editors</div>
<div class="integrations">
<div class="int"><div class="icon">🖱️</div><div class="name">Cursor</div><div class="desc">AI code editor</div></div>
<div class="int"><div class="icon">🤖</div><div class="name">Claude Code</div><div class="desc">Anthropic CLI</div></div>
<div class="int"><div class="icon">🌊</div><div class="name">Windsurf</div><div class="desc">Codeium IDE</div></div>
<div class="int"><div class="icon">📋</div><div class="name">MCP clients</div><div class="desc">Any MCP editor</div></div>
</div>
<div class="config">
<div class="label">📦 MCP Config:</div>
<div class="code">{{ "mcpServers": {{ "context7": {{ "command": "npx", "args": ["@upstash/context7-mcp"] }} }} }}</div>
</div>
<div class="sub"><p>Tích hợp Cursor, Claude Code, Windsurf + mọi MCP editor</p></div>
<div class="footer">MULTI-EDITOR · MCP NATIVE</div>
</body></html>''',

    "s7": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a1a15 0%, #0a0e1a 100%); color: #fff; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #50c878; border-radius: 8px; font-size: 34px; font-weight: 700; color: #50c878; }}
.title {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); font-size: 64px; font-weight: 800; color: #fff; }}
.cases {{ position: absolute; top: 340px; left: 80px; right: 80px; }}
.case {{ background: rgba(10,30,20,0.7); border: 2px solid #50c878; border-radius: 14px; padding: 24px 32px; margin-bottom: 16px; display: flex; align-items: center; gap: 24px; }}
.case .icon {{ font-size: 56px; }}
.case .text {{ font-size: 38px; }}
.case .text strong {{ color: #50c878; }}
.shot {{ position: absolute; top: 880px; left: 50%; transform: translateX(-50%); width: 950px; border-radius: 20px; border: 4px solid rgba(80,200,120,0.5); }}
.sub {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #50c878; border-radius: 6px; font-size: 28px; font-weight: 700; color: #50c878; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateX(-30px); }} to {{ opacity: 1; transform: translateX(0); }} }}
@keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-50%) scale(0.95); }} to {{ opacity: 1; transform: translateX(-50%) scale(1); }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.5s 0.2s both; }}
.case {{ animation: fadeUp 0.4s both; }}
.case:nth-child(1) {{ animation-delay: 0.4s; }}
.case:nth-child(2) {{ animation-delay: 0.6s; }}
.case:nth-child(3) {{ animation-delay: 0.8s; }}
.case:nth-child(4) {{ animation-delay: 1.0s; }}
.case:nth-child(5) {{ animation-delay: 1.2s; }}
.shot {{ animation: slideIn 0.6s 1.4s both; }}
.sub {{ animation: fadeUp 0.5s 1.8s both; }}
.footer {{ animation: fadeUp 0.4s 2.0s both; }}
</style></head><body>
<div class="header">🎯 USE CASES</div>
<div class="title">Khi nào dùng Context7?</div>
<div class="cases">
<div class="case"><span class="icon">📚</span><span class="text">Viết code với <strong>thư viện mới</strong></span></div>
<div class="case"><span class="icon">🔍</span><span class="text">Tra cứu <strong>API docs</strong> chính xác</span></div>
<div class="case"><span class="icon">🛡️</span><span class="text">Tránh <strong>AI hallucination</strong></span></div>
<div class="case"><span class="icon">⚡</span><span class="text">Học <strong>framework nhanh</strong></span></div>
<div class="case"><span class="icon">🎸</span><span class="text"><strong>Vibe coding</strong> + agent-driven dev</span></div>
</div>
<div class="sub"><p>Đặc biệt hữu ích cho vibe coding</p></div>
<div class="footer">VIBE CODING · ACCURATE · FAST</div>
</body></html>''',

    "s8": f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}
body {{ background: linear-gradient(135deg, #0a0e1a 0%, #1a1040 50%, #0a0e1a 100%); color: #fff; }}
.orb {{ position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.4; }}
.orb1 {{ width: 400px; height: 400px; background: #4285f4; top: -100px; left: -100px; }}
.orb2 {{ width: 500px; height: 500px; background: #7c5cff; bottom: -150px; right: -150px; }}
.header {{ position: absolute; top: 80px; left: 50%; transform: translateX(-50%); padding: 12px 30px; border: 3px solid #50c878; border-radius: 8px; font-size: 34px; font-weight: 700; color: #50c878; }}
.title {{ position: absolute; top: 220px; left: 50%; transform: translateX(-50%); font-size: 100px; font-weight: 900; text-align: center; line-height: 1.1; }}
.title .accent {{ background: linear-gradient(135deg, #4285f4, #7c5cff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.sub {{ position: absolute; top: 480px; left: 50%; transform: translateX(-50%); font-size: 40px; color: #cbd5e1; text-align: center; }}
.links {{ position: absolute; top: 650px; left: 80px; right: 80px; background: rgba(15,12,30,0.8); border: 3px solid #4285f4; border-radius: 18px; padding: 36px; }}
.links .url {{ font-size: 38px; font-weight: 700; color: #4285f4; text-align: center; margin-bottom: 16px; }}
.links .url2 {{ font-size: 38px; font-weight: 700; color: #50c878; text-align: center; margin-bottom: 20px; }}
.links .hash {{ font-size: 36px; font-weight: 700; color: #7c5cff; text-align: center; }}
.sub2 {{ position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%); text-align: center; }}
.sub2 p {{ font-size: 36px; color: #fff; }}
.footer {{ position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border: 2px solid #50c878; border-radius: 6px; font-size: 28px; font-weight: 700; color: #50c878; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translate(-50%, 30px); }} to {{ opacity: 1; transform: translate(-50%, 0); }} }}
@keyframes glow {{ from {{ filter: drop-shadow(0 0 0 transparent); }} to {{ filter: drop-shadow(0 0 40px rgba(124,92,255,0.6)); }} }}
.header {{ animation: fadeUp 0.5s both; }}
.title {{ animation: fadeUp 0.8s 0.2s both, glow 1s 1s both; }}
.sub {{ animation: fadeUp 0.5s 0.6s both; }}
.links {{ animation: fadeUp 0.6s 0.9s both; }}
.sub2 {{ animation: fadeUp 0.5s 1.3s both; }}
.footer {{ animation: fadeUp 0.4s 1.6s both; }}
</style></head><body>
<div class="orb orb1"></div><div class="orb orb2"></div>
<div class="header">TAKEAWAY</div>
<div class="title"><span class="accent">Context7</span><br>cho AI coding</div>
<div class="sub">58K⭐ · MCP Server · Ngăn hallucinations</div>
<div class="links">
<div class="url">github.com/upstash/context7</div>
<div class="url2">context7.com</div>
<div class="hash">#Context7 #MCP #AICoding #VibeCoding</div>
</div>
<div class="sub2"><p>Follow kênh để cập nhật AI tools!</p></div>
<div class="footer">FOLLOW FOR MORE</div>
</body></html>''',
}

# Write all HTML files
for sid, html in SCENE_HTML.items():
    scene_dir = f"{OUT_DIR}/{sid}"
    os.makedirs(scene_dir, exist_ok=True)
    with open(f"{scene_dir}/index.html", "w") as f:
        f.write(html)
    print(f"  {sid}/index.html written")

print(f"\nAll 8 HTML files in: {OUT_DIR}")
