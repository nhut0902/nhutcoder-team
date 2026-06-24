"""Render video with valid HyperFrames composition format."""
import os
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SANDBOX_ID = "ijy0tt9cd55nqwjj48gpy"
sbx = Sandbox.connect(SANDBOX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Valid HyperFrames composition: data-composition-id, data-width, data-height, window.__timelines
html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Browser Use</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body {
    width: 1080px; height: 1920px;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
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

  .s1 .emoji { font-size: 200px; margin-bottom: 40px; }
  .s1 h1 {
    font-size: 130px; font-weight: 900; line-height: 1.0;
    text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -4px;
  }
  .s1 .subtitle {
    margin-top: 30px; font-size: 42px; font-weight: 600;
    color: #94a3b8; text-align: center;
  }

  .s2 .label { font-size: 36px; color: #94a3b8; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 4px; }
  .s2 .stats { display: flex; flex-direction: column; gap: 60px; }
  .s2 .stat { text-align: center; }
  .s2 .stat .num {
    font-size: 140px; font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
  }
  .s2 .stat .desc { font-size: 38px; color: #cbd5e1; margin-top: 12px; }

  .s3 .label { font-size: 36px; color: #94a3b8; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 4px; }
  .s3 .code {
    background: #1e293b; border: 3px solid #334155;
    border-radius: 24px; padding: 50px 70px;
    font-family: 'Courier New', monospace;
    font-size: 50px; font-weight: 600;
    color: #00ff88;
    box-shadow: 0 20px 60px rgba(124, 58, 237, 0.3);
  }
  .s3 .code::before { content: '$ '; color: #94a3b8; }
  .s3 h2 { font-size: 60px; font-weight: 800; margin-top: 50px; text-align: center; color: #fff; line-height: 1.2; }

  .s4 .label { font-size: 36px; color: #94a3b8; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 4px; }
  .s4 .features { display: flex; flex-direction: column; gap: 32px; width: 100%; }
  .s4 .feature {
    display: flex; align-items: center; gap: 30px;
    background: rgba(30, 41, 59, 0.5);
    border: 2px solid #334155;
    border-radius: 20px;
    padding: 28px 36px;
  }
  .s4 .feature .icon { font-size: 70px; }
  .s4 .feature .text { font-size: 40px; font-weight: 600; }

  .s5 .emoji { font-size: 180px; margin-bottom: 30px; }
  .s5 h2 {
    font-size: 95px; font-weight: 900; text-align: center; line-height: 1.05;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .s5 .url {
    margin-top: 40px; font-size: 36px; color: #94a3b8;
    font-family: 'Courier New', monospace;
    background: #1e293b; padding: 22px 40px; border-radius: 12px;
  }
  .s5 .hashtags {
    margin-top: 50px; font-size: 34px; color: #00d4ff; font-weight: 700;
  }
</style>
</head>
<body data-composition-id="browser-use-intro" data-width="1080" data-height="1920">

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

<!-- Scene 3: Install (6-9.5s) -->
<div class="scene s3" data-timeline="6000-9500" data-transition="fade">
  <div class="label">Quick Start</div>
  <div class="code">pip install browser-use</div>
  <h2>Build AI agents that<br>navigate the web</h2>
</div>

<!-- Scene 4: Features (9.5-13.5s) -->
<div class="scene s4" data-timeline="9500-13500" data-transition="fade">
  <div class="label">Key Features</div>
  <div class="features">
    <div class="feature"><span class="icon">🤖</span><span class="text">AI Agent Control</span></div>
    <div class="feature"><span class="icon">🖱️</span><span class="text">Click · Type · Scroll</span></div>
    <div class="feature"><span class="icon">📊</span><span class="text">Data Extraction</span></div>
    <div class="feature"><span class="icon">☁️</span><span class="text">Cloud & Self-hosted</span></div>
  </div>
</div>

<!-- Scene 5: Outro (13.5-17s) -->
<div class="scene s5" data-timeline="13500-17000" data-transition="fade">
  <div class="emoji">🚀</div>
  <h2>Start Building<br>Today</h2>
  <div class="url">github.com/browser-use</div>
  <div class="hashtags">#AI #BrowserUse #Automation #Python</div>
</div>

<script>
  // HyperFrames timeline registry
  window.__timelines = window.__timelines || {};
  window.__timelines["browser-use-intro"] = {
    duration: 17000,
    scenes: [
      { id: "s1", start: 0, end: 2500, el: null },
      { id: "s2", start: 2500, end: 6000, el: null },
      { id: "s3", start: 6000, end: 9500, el: null },
      { id: "s4", start: 9500, end: 13500, el: null },
      { id: "s5", start: 13500, end: 17000, el: null }
    ]
  };

  // Scene controller: show/hide based on timeline
  (function() {
    var tl = window.__timelines["browser-use-intro"];
    var scenes = document.querySelectorAll('.scene');
    tl.scenes.forEach(function(s) {
      s.el = document.querySelector('.' + s.id);
    });

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

# Write HTML
sbx.files.write("/home/user/browser-use-video/index.html", html)
print("Composition HTML written", flush=True)

# Lint
print("\n=== Lint ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/browser-use-video && hyperframes lint . 2>&1 | head -20", timeout=60)
print(r.stdout, flush=True)

# Render
print("\n=== Render ===", flush=True)
r = sbx.commands.run(
    PATHFIX + "cd /home/user/browser-use-video && hyperframes render . -o renders/browser-use.mp4 --quality draft --fps 24 2>&1 | tail -60",
    timeout=600,
)
print("STDOUT:", r.stdout[-3000:], flush=True)
if r.stderr:
    print("STDERR:", r.stderr[-1000:], flush=True)

# Check output
print("\n=== Output ===", flush=True)
r = sbx.commands.run("ls -la /home/user/browser-use-video/renders/ 2>&1", timeout=15)
print(r.stdout, flush=True)
r = sbx.commands.run("ffprobe -v error -show_entries format=duration,size:stream=width,height,codec_name /home/user/browser-use-video/renders/browser-use.mp4 2>&1", timeout=15)
print(r.stdout, flush=True)
