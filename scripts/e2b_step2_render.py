"""Step 2: Install deps + render in existing sandbox ide96zyofb9tov8aa53bp."""
import os, sys, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SANDBOX_ID = "ide96zyofb9tov8aa53bp"
print(f"=== Connecting to {SANDBOX_ID} ===", flush=True)
sbx = Sandbox.connect(SANDBOX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Step A: install in stages (each command is short to avoid timeout)
print("\n=== A. Create swap ===", flush=True)
r = sbx.commands.run(
    "sudo fallocate -l 2G /swapfile 2>&1 && sudo chmod 600 /swapfile && sudo mkswap /swapfile 2>&1 | tail -2 && sudo swapon /swapfile 2>&1 && free -h | head -3",
    timeout=60,
)
print(r.stdout, flush=True)

print("\n=== B. Install Node 22 ===", flush=True)
r = sbx.commands.run(
    "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - 2>&1 | tail -5 && "
    "sudo apt-get install -y nodejs 2>&1 | tail -5",
    timeout=180,
)
print(r.stdout, flush=True)
r = sbx.commands.run(PATHFIX + "node --version && npm --version", timeout=15)
print("Node:", r.stdout, flush=True)

print("\n=== C. Install ffmpeg + chrome deps ===", flush=True)
r = sbx.commands.run(
    "sudo apt-get install -y ffmpeg libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
    "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
    "2>&1 | tail -5",
    timeout=180,
)
print(r.stdout, flush=True)

print("\n=== D. Install hyperframes ===", flush=True)
r = sbx.commands.run(PATHFIX + "npm install -g hyperframes 2>&1 | tail -3", timeout=180)
print(r.stdout, flush=True)

print("\n=== E. Install Chrome ===", flush=True)
r = sbx.commands.run(PATHFIX + "hyperframes browser ensure 2>&1 | tail -5", timeout=240)
print(r.stdout, flush=True)

print("\n=== F. Write composition HTML ===", flush=True)
html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Browser Use</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body {
    width: 1080px; height: 1920px;
    font-family: 'Arial', sans-serif;
    background: #0a0e1a; color: #fff; overflow: hidden; position: relative;
  }
  .scene {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px; opacity: 0;
  }
  .scene.show { opacity: 1; transition: opacity 0.2s ease; }
  .s1 .emoji { font-size: 200px; margin-bottom: 30px; }
  .s1 h1 {
    font-size: 140px; font-weight: 900; line-height: 1; text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -4px;
  }
  .s1 .subtitle { margin-top: 25px; font-size: 40px; color: #94a3b8; text-align: center; }
  .s2 .label { font-size: 32px; color: #94a3b8; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 4px; }
  .s2 .num {
    font-size: 200px; font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
  }
  .s2 .desc { font-size: 44px; color: #cbd5e1; margin-top: 15px; text-align: center; }
  .s3 .label { font-size: 32px; color: #94a3b8; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 4px; }
  .s3 .code {
    background: #1e293b; border: 3px solid #334155; border-radius: 20px;
    padding: 40px 60px; font-family: 'Courier New', monospace;
    font-size: 48px; font-weight: 600; color: #00ff88;
    box-shadow: 0 20px 60px rgba(124, 58, 237, 0.3);
  }
  .s3 .code::before { content: '$ '; color: #94a3b8; }
  .s4 .features { display: flex; flex-direction: column; gap: 28px; width: 100%; }
  .s4 .feature {
    display: flex; align-items: center; gap: 25px;
    background: rgba(30, 41, 59, 0.5); border: 2px solid #334155;
    border-radius: 18px; padding: 25px 35px;
  }
  .s4 .feature .icon { font-size: 64px; }
  .s4 .feature .text { font-size: 36px; font-weight: 600; }
  .s5 .emoji { font-size: 180px; margin-bottom: 25px; }
  .s5 h2 {
    font-size: 100px; font-weight: 900; text-align: center; line-height: 1.05;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .s5 .url {
    margin-top: 35px; font-size: 34px; color: #94a3b8;
    font-family: 'Courier New', monospace;
    background: #1e293b; padding: 20px 35px; border-radius: 12px;
  }
  .s5 .hashtags { margin-top: 40px; font-size: 32px; color: #00d4ff; font-weight: 700; }
</style>
</head>
<body data-composition-id="browser-use" data-width="1080" data-height="1920">

<div class="scene s1 show" data-timeline="0-1000">
  <div class="emoji">🌐</div>
  <h1>Browser<br>Use</h1>
  <div class="subtitle">Make websites accessible for AI agents</div>
</div>

<div class="scene s2" data-timeline="1000-2000" data-transition="fade">
  <div class="label">Open Source · MIT</div>
  <div class="num">100K+</div>
  <div class="desc">GitHub Stars</div>
</div>

<div class="scene s3" data-timeline="2000-3000" data-transition="fade">
  <div class="label">Quick Start</div>
  <div class="code">pip install browser-use</div>
</div>

<div class="scene s4" data-timeline="3000-4000" data-transition="fade">
  <div class="features">
    <div class="feature"><span class="icon">🤖</span><span class="text">AI Agent Control</span></div>
    <div class="feature"><span class="icon">🖱️</span><span class="text">Click · Type · Scroll</span></div>
    <div class="feature"><span class="icon">📊</span><span class="text">Data Extraction</span></div>
  </div>
</div>

<div class="scene s5" data-timeline="4000-5000" data-transition="fade">
  <div class="emoji">🚀</div>
  <h2>Start Today</h2>
  <div class="url">github.com/browser-use</div>
  <div class="hashtags">#AI #BrowserUse #Python</div>
</div>

<script>
  window.__timelines = window.__timelines || {};
  window.__timelines["browser-use"] = {
    duration: 5000,
    scenes: [
      { id: "s1", start: 0, end: 1000 },
      { id: "s2", start: 1000, end: 2000 },
      { id: "s3", start: 2000, end: 3000 },
      { id: "s4", start: 3000, end: 4000 },
      { id: "s5", start: 4000, end: 5000 }
    ]
  };
  (function() {
    var tl = window.__timelines["browser-use"];
    tl.scenes.forEach(function(s) { s.el = document.querySelector('.' + s.id); });
    window.__renderFrame = function(t) {
      tl.scenes.forEach(function(s) {
        if (t >= s.start && t < s.end) {
          if (!s.el.classList.contains('show')) s.el.classList.add('show');
        } else {
          if (s.el.classList.contains('show')) s.el.classList.remove('show');
        }
      });
    };
  })();
</script>
</body>
</html>
"""
sbx.commands.run("mkdir -p /home/user/browser-use-video/renders", timeout=15)
sbx.files.write("/home/user/browser-use-video/index.html", html)
print("HTML written", flush=True)

# Step G: Render in background
print("\n=== G. Start render (background) ===", flush=True)
r = sbx.commands.run(
    "cd /home/user/browser-use-video && "
    "nohup bash -c 'export PATH=/usr/bin:$PATH && hyperframes render . -o renders/browser-use.mp4 --quality draft --fps 12 > /tmp/render.log 2>&1' </dev/null > /dev/null 2>&1 & disown; echo PID=$!",
    timeout=15,
)
print(r.stdout, flush=True)

# Step H: Poll
print("\n=== H. Poll for completion (max 8 min) ===", flush=True)
start = time.time()
done = False
while time.time() - start < 480:
    time.sleep(20)
    try:
        r = sbx.commands.run(
            "ls /home/user/browser-use-video/renders/*.mp4 2>/dev/null && echo MP4_FOUND || echo NO_MP4; "
            "ps aux | grep hyperframes | grep -v grep | wc -l",
            timeout=15,
        )
        elapsed = int(time.time() - start)
        out = r.stdout.strip().replace('\n', ' | ')
        print(f"[{elapsed}s] {out}", flush=True)
        if "MP4_FOUND" in r.stdout:
            r2 = sbx.commands.run(
                "ls -la /home/user/browser-use-video/renders/*.mp4 && "
                "ffprobe -v error -show_entries format=duration,size:stream=width,height /home/user/browser-use-video/renders/browser-use.mp4 2>&1",
                timeout=15,
            )
            print("MP4 READY:", r2.stdout, flush=True)
            done = True
            break
    except Exception as e:
        print(f"poll err: {e}", flush=True)
        try:
            sbx = Sandbox.connect(SANDBOX_ID)
            sbx.set_timeout(60 * 30)
        except:
            pass

if not done:
    print("Render timeout, last log:", flush=True)
    try:
        r = sbx.commands.run("tail -30 /tmp/render.log 2>&1", timeout=15)
        print(r.stdout, flush=True)
    except:
        pass

with open("/tmp/e2b_sandbox_id.txt", "w") as f:
    f.write(SANDBOX_ID)
print(f"\nSandbox ID saved: {SANDBOX_ID}", flush=True)
