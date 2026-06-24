"""Create HyperFrames HTML composition about Browser use repo and render to MP4."""
import os, sys
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SANDBOX_ID = "ijy0tt9cd55nqwjj48gpy"
sbx = Sandbox.connect(SANDBOX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Create project dir + composition HTML
print("=== Create composition HTML ===", flush=True)
sbx.commands.run("mkdir -p /home/user/browser-use-video/renders", timeout=15)

# Minimal HyperFrames composition about Browser use repo
# HyperFrames uses HTML with data-timeline attributes for animation timing
html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Browser Use</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body {
    width: 1080px; height: 1920px;
    font-family: 'Inter', system-ui, sans-serif;
    background: #0a0e1a;
    color: #fff;
    overflow: hidden;
    position: relative;
  }
  .scene {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 80px;
    opacity: 0;
  }
  .scene.show { opacity: 1; transition: opacity 0.4s ease; }

  /* Scene 1: Title */
  .s1 .emoji { font-size: 200px; margin-bottom: 40px; }
  .s1 h1 {
    font-size: 120px; font-weight: 900; line-height: 1.05;
    text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -3px;
  }
  .s1 .subtitle {
    margin-top: 30px; font-size: 42px; font-weight: 600;
    color: #94a3b8; text-align: center;
  }

  /* Scene 2: Stats */
  .s2 .label { font-size: 36px; color: #94a3b8; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 4px; }
  .s2 .stats { display: flex; flex-direction: column; gap: 50px; }
  .s2 .stat { text-align: center; }
  .s2 .stat .num {
    font-size: 130px; font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .s2 .stat .desc { font-size: 36px; color: #cbd5e1; margin-top: 10px; }

  /* Scene 3: Install */
  .s3 .label { font-size: 36px; color: #94a3b8; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 4px; }
  .s3 .code {
    background: #1e293b; border: 3px solid #334155;
    border-radius: 24px; padding: 50px 70px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 56px; font-weight: 600;
    color: #00ff88;
    box-shadow: 0 20px 60px rgba(124, 58, 237, 0.3);
  }
  .s3 .code::before { content: '$ '; color: #94a3b8; }
  .s3 h2 { font-size: 64px; font-weight: 800; margin-top: 50px; text-align: center; color: #fff; }

  /* Scene 4: Features */
  .s4 .label { font-size: 36px; color: #94a3b8; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 4px; }
  .s4 .features { display: flex; flex-direction: column; gap: 36px; width: 100%; }
  .s4 .feature {
    display: flex; align-items: center; gap: 30px;
    background: rgba(30, 41, 59, 0.5);
    border: 2px solid #334155;
    border-radius: 20px;
    padding: 30px 40px;
  }
  .s4 .feature .icon { font-size: 70px; }
  .s4 .feature .text { font-size: 42px; font-weight: 600; }

  /* Scene 5: Outro */
  .s5 .emoji { font-size: 180px; margin-bottom: 30px; }
  .s5 h2 {
    font-size: 90px; font-weight: 900; text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .s5 .url {
    margin-top: 40px; font-size: 38px; color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    background: #1e293b; padding: 20px 40px; border-radius: 12px;
  }
  .s5 .hashtags {
    margin-top: 50px; font-size: 36px; color: #00d4ff; font-weight: 600;
  }
</style>
</head>
<body>

<!-- Scene 1: Title (0-2.5s) -->
<div class="scene s1 show" data-timeline="0-2500">
  <div class="emoji">🌐</div>
  <h1>Browser<br>Use</h1>
  <div class="subtitle">Make websites accessible for AI agents</div>
</div>

<!-- Scene 2: Stats (2.5-6s) -->
<div class="scene s2" data-timeline="2500-6000" data-transition="fade">
  <div class="label">Open Source · MIT</div>
  <div class="stats">
    <div class="stat">
      <div class="num">100K+</div>
      <div class="desc">GitHub Stars</div>
    </div>
    <div class="stat">
      <div class="num">11K+</div>
      <div class="desc">Forks</div>
    </div>
    <div class="stat">
      <div class="num">Python</div>
      <div class="desc">+ Playwright</div>
    </div>
  </div>
</div>

<!-- Scene 3: Install (6-9s) -->
<div class="scene s3" data-timeline="6000-9000" data-transition="fade">
  <div class="label">Quick Start</div>
  <div class="code">pip install browser-use</div>
  <h2>Build AI agents that<br>navigate the web</h2>
</div>

<!-- Scene 4: Features (9-13s) -->
<div class="scene s4" data-timeline="9000-13000" data-transition="fade">
  <div class="label">Key Features</div>
  <div class="features">
    <div class="feature"><span class="icon">🤖</span><span class="text">AI Agent Control</span></div>
    <div class="feature"><span class="icon">🖱️</span><span class="text">Click · Type · Scroll</span></div>
    <div class="feature"><span class="icon">📊</span><span class="text">Data Extraction</span></div>
    <div class="feature"><span class="icon">☁️</span><span class="text">Cloud & Self-hosted</span></div>
  </div>
</div>

<!-- Scene 5: Outro (13-16s) -->
<div class="scene s5" data-timeline="13000-16000" data-transition="fade">
  <div class="emoji">🚀</div>
  <h2>Start Building<br>Today</h2>
  <div class="url">github.com/browser-use</div>
  <div class="hashtags">#AI #BrowserUse #Automation #Python</div>
</div>

</body>
</html>
"""

# Write HTML file
sbx.files.write("/home/user/browser-use-video/index.html", html)
print("Composition HTML written", flush=True)

# Lint composition
print("\n=== Lint composition ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/browser-use-video && hyperframes lint . 2>&1 | head -30", timeout=60)
print(r.stdout, flush=True)

# Render to MP4 (draft quality to save memory)
print("\n=== Render to MP4 ===", flush=True)
r = sbx.commands.run(
    PATHFIX + "cd /home/user/browser-use-video && hyperframes render . -o renders/browser-use.mp4 --quality draft --fps 24 2>&1 | tail -50",
    timeout=600,
)
print("STDOUT:", r.stdout[-3000:], flush=True)
if r.stderr:
    print("STDERR:", r.stderr[-1000:], flush=True)

# Check output
print("\n=== Check output ===", flush=True)
r = sbx.commands.run("ls -la /home/user/browser-use-video/renders/ 2>&1")
print(r.stdout, flush=True)
r = sbx.commands.run("ffprobe -v error -show_entries format=duration,size:stream=width,height,codec_name /home/user/browser-use-video/renders/browser-use.mp4 2>&1")
print(r.stdout, flush=True)

print(f"\n=== Sandbox ID: {SANDBOX_ID} ===", flush=True)
