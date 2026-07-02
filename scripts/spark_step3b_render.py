#!/home/z/.venv/bin/python3
"""Step 3b: Fix HTML - use window.__timelines registry + class='clip' on scenes. Then render."""
import os, json, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = open("/tmp/spark_sandbox_id.txt").read().strip()
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

with open("/tmp/spark_durations.json") as f:
    durations = json.load(f)["durations"]

scenes = ["s1","s2","s3","s4","s5","s6","s7","s8"]
starts = {}
cum = 0
for s in scenes:
    starts[s] = cum
    cum += durations[s]
total_dur = cum
print(f"Total duration: {total_dur:.2f}s", flush=True)

# Fix: use window.__timelines (double underscore) + class="clip" on scenes
# Per HyperFrames lint rules
html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Gemini Spark</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: 1080px; height: 1920px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0e1a; color: #fff; overflow: hidden;
  }}
  #root {{
    position: relative; width: 1080px; height: 1920px;
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1a3e 50%, #2d1b69 100%);
  }}
  .orb {{
    position: absolute; border-radius: 50%; filter: blur(60px);
    opacity: 0.4; pointer-events: none;
  }}
  .orb-1 {{ width: 400px; height: 400px; background: #4285f4; top: -100px; left: -100px; }}
  .orb-2 {{ width: 500px; height: 500px; background: #9b72cb; bottom: -150px; right: -150px; }}
  .orb-3 {{ width: 300px; height: 300px; background: #00d4ff; top: 700px; right: -100px; opacity: 0.3; }}

  .clip {{
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 60px; opacity: 0;
  }}
  .spark-icon {{
    font-size: 200px; margin-bottom: 40px;
    filter: drop-shadow(0 0 30px rgba(66, 133, 244, 0.8));
  }}
  h1 {{
    font-size: 130px; font-weight: 900; line-height: 1; text-align: center;
    background: linear-gradient(135deg, #4285f4 0%, #9b72cb 50%, #00d4ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -3px;
    margin-bottom: 30px;
  }}
  h2 {{
    font-size: 80px; font-weight: 800; text-align: center;
    color: #fff; line-height: 1.1; margin-bottom: 25px;
  }}
  .subtitle {{
    font-size: 44px; color: #cbd5e1; text-align: center;
    line-height: 1.4; max-width: 900px;
  }}
  .date-badge {{
    background: rgba(66, 133, 244, 0.2);
    border: 2px solid #4285f4;
    border-radius: 20px;
    padding: 12px 32px;
    font-size: 32px; font-weight: 600;
    color: #4285f4;
    margin-bottom: 40px;
    letter-spacing: 2px;
  }}
  .spark-img {{
    width: 800px; height: auto;
    border-radius: 24px;
    border: 4px solid rgba(66, 133, 244, 0.5);
    box-shadow: 0 20px 60px rgba(66, 133, 244, 0.4);
    margin-bottom: 30px;
    object-fit: cover;
  }}
  .features {{
    display: flex; flex-direction: column;
    gap: 24px; width: 100%;
  }}
  .feature {{
    display: flex; align-items: center; gap: 24px;
    background: rgba(30, 41, 59, 0.7);
    border: 2px solid rgba(66, 133, 244, 0.3);
    border-radius: 18px;
    padding: 24px 32px;
    backdrop-filter: blur(10px);
  }}
  .feature .icon {{ font-size: 56px; }}
  .feature .text {{ font-size: 36px; font-weight: 600; color: #e0e7ff; }}
  .stat-block {{
    background: rgba(30, 41, 59, 0.7);
    border: 2px solid rgba(66, 133, 244, 0.3);
    border-radius: 24px;
    padding: 40px 60px;
    text-align: center;
    backdrop-filter: blur(10px);
  }}
  .stat-block .label {{ font-size: 32px; color: #94a3b8; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 3px; }}
  .stat-block .value {{ font-size: 100px; font-weight: 900; color: #4285f4; line-height: 1; }}
  .stat-block .desc {{ font-size: 32px; color: #cbd5e1; margin-top: 12px; }}
  .footer {{
    position: absolute; bottom: 60px; left: 0; right: 0;
    text-align: center;
    font-size: 28px; color: #64748b;
    font-weight: 500;
  }}
  .source-link {{ color: #4285f4; font-weight: 600; }}
  .hashtags {{
    font-size: 30px; color: #00d4ff;
    font-weight: 600; text-align: center;
    margin-top: 30px;
  }}
</style>
</head>
<body>

<div id="root" data-composition-id="gemini-spark" data-start="0" data-width="1080" data-height="1920">

  <div class="orb orb-1" id="orb1"></div>
  <div class="orb orb-2" id="orb2"></div>
  <div class="orb orb-3" id="orb3"></div>

  <div class="clip" id="scene1" data-start="0" data-duration="{durations['s1']:.2f}" data-track-index="0">
    <div class="date-badge">2/7/2026</div>
    <div class="spark-icon">✨</div>
    <h1>GEMINI<br>SPARK</h1>
    <div class="subtitle">AI Agent 24/7 của Google</div>
  </div>

  <div class="clip" id="scene2" data-start="{starts['s2']:.2f}" data-duration="{durations['s2']:.2f}" data-track-index="0">
    <div class="spark-icon">🤖</div>
    <h2>Gemini Spark là gì?</h2>
    <div class="subtitle">AI agent 24/7 trên cloud<br>Sử dụng Gemini 3.5<br>+ Antigravity harness</div>
  </div>

  <div class="clip" id="scene3" data-start="{starts['s3']:.2f}" data-duration="{durations['s3']:.2f}" data-track-index="0">
    <div class="spark-icon">💻</div>
    <h2>macOS Beta</h2>
    <div class="subtitle">Tương tác file local<br>Tự sắp xếp downloads<br>Tạo spreadsheet từ invoice</div>
  </div>

  <div class="clip" id="scene4" data-start="{starts['s4']:.2f}" data-duration="{durations['s4']:.2f}" data-track-index="0">
    <img class="spark-img" src="gemini_spark.png" alt="Gemini Spark">
    <div class="subtitle">Real-time topic tracking<br>Tin tức · Tài chính · Social media</div>
  </div>

  <div class="clip" id="scene5" data-start="{starts['s5']:.2f}" data-duration="{durations['s5']:.2f}" data-track-index="0">
    <h2>Tích hợp</h2>
    <div class="features">
      <div class="feature"><span class="icon">📋</span><span class="text">Google Tasks · Keep</span></div>
      <div class="feature"><span class="icon">🎨</span><span class="text">Canva · Dropbox</span></div>
      <div class="feature"><span class="icon">🛒</span><span class="text">Instacart · OpenTable</span></div>
      <div class="feature"><span class="icon">🏠</span><span class="text">Zillow Rentals</span></div>
      <div class="feature"><span class="icon">🔌</span><span class="text">Custom MCP Connections</span></div>
    </div>
  </div>

  <div class="clip" id="scene6" data-start="{starts['s6']:.2f}" data-duration="{durations['s6']:.2f}" data-track-index="0">
    <div class="spark-icon">💰</div>
    <h2>Giá &amp; Khả dụng</h2>
    <div class="stat-block">
      <div class="label">Google AI Ultra</div>
      <div class="value">$99.99</div>
      <div class="desc">/tháng · Chỉ US 18+<br>Tiếng Anh</div>
    </div>
  </div>

  <div class="clip" id="scene7" data-start="{starts['s7']:.2f}" data-duration="{durations['s7']:.2f}" data-track-index="0">
    <div class="spark-icon">⚔️</div>
    <h2>So sánh</h2>
    <div class="features">
      <div class="feature"><span class="icon">⚡</span><span class="text">Chạy 24/7 trên cloud</span></div>
      <div class="feature"><span class="icon">🔇</span><span class="text">Không cần thiết bị bật</span></div>
      <div class="feature"><span class="icon">🎯</span><span class="text">Multi-step tự chủ</span></div>
    </div>
  </div>

  <div class="clip" id="scene8" data-start="{starts['s8']:.2f}" data-duration="{durations['s8']:.2f}" data-track-index="0">
    <div class="spark-icon">🚀</div>
    <h2>Tổng kết</h2>
    <div class="subtitle">Bước tiến quan trọng<br>trong cuộc đua AI agent</div>
    <div class="hashtags">#GeminiSpark #GoogleAI #AI2026</div>
  </div>

  <div class="footer">
    Nguồn: <span class="source-link">blog.google · TechCrunch · PCMag</span>
  </div>

</div>

<script>
  // HyperFrames: register GSAP timeline via window.__timelines registry
  window.__timelines = window.__timelines || {{}};
  window.__timelines["gemini-spark"] = function() {{
    const tl = gsap.timeline({{ paused: true }});

    // Animate background orbs
    tl.to("#orb1", {{ x: 50, y: 30, duration: {total_dur:.2f}, ease: "sine.inOut" }}, 0);
    tl.to("#orb2", {{ x: -40, y: -50, duration: {total_dur:.2f}, ease: "sine.inOut" }}, 0);
    tl.to("#orb3", {{ x: -30, y: 40, duration: {total_dur:.2f}, ease: "sine.inOut" }}, 0);

    // Per-scene animations - scene's .clip class handles visibility based on data-start/data-duration
    // Here we add fade-in entrance for each scene
    const scenes = {json.dumps(scenes)};
    const durations = {json.dumps(durations)};
    const starts = {json.dumps(starts)};

    scenes.forEach((sid, i) => {{
      const start = starts[sid];
      const sceneEl = "#scene" + (i + 1);
      // Fade in at scene start
      tl.fromTo(sceneEl, {{ opacity: 0, scale: 0.95, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "power2.out" }}, start);
    }});

    return tl;
  }};
</script>

</body>
</html>
"""

print("=== Write fixed HyperFrames HTML ===", flush=True)
sbx.files.write("/home/user/spark_project/index.html", html)
print("HTML written", flush=True)

# Lint again
print("\n=== Lint ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/spark_project && hyperframes lint . 2>&1 | head -25", timeout=60)
print(r.stdout, flush=True)

# Render
print(f"\n=== Start render (duration {total_dur:.2f}s, fps 24, draft) ===", flush=True)
render_cmd = (
    f"cd /home/user/spark_project && "
    f"nohup bash -c '{PATHFIX} hyperframes render . -o renders/spark.mp4 --quality draft --fps 24 --audio narration.mp3 > /tmp/render.log 2>&1' "
    f"</dev/null > /dev/null 2>&1 & disown; echo PID=$!"
)
try:
    r = sbx.commands.run(render_cmd, timeout=20)
    print(r.stdout, flush=True)
except Exception as e:
    print(f"render start err: {e}", flush=True)

# Poll (max 12 min)
print("\n=== Poll render (max 12 min) ===", flush=True)
start_poll = time.time()
done = False
while time.time() - start_poll < 720:
    time.sleep(30)
    try:
        sbx = Sandbox.connect(SBX_ID)
        sbx.set_timeout(60 * 30)
        r = sbx.commands.run(
            "ls /home/user/spark_project/renders/*.mp4 2>/dev/null && echo MP4_FOUND || echo NO_MP4; "
            "ps aux | grep hyperframes | grep -v grep | wc -l; "
            "tail -1 /tmp/render.log 2>&1",
            timeout=15,
        )
        elapsed = int(time.time() - start_poll)
        out = r.stdout.strip().replace('\n', ' | ')[:250]
        print(f"[{elapsed}s] {out}", flush=True)
        if 'MP4_FOUND' in r.stdout:
            r2 = sbx.commands.run(
                "ls -la /home/user/spark_project/renders/*.mp4 && "
                "ffprobe -v error -show_entries format=duration,size:stream=width,height /home/user/spark_project/renders/spark.mp4 2>&1",
                timeout=15,
            )
            print("MP4 READY:", r2.stdout, flush=True)
            done = True
            break
    except Exception as e:
        print(f"poll err: {e}", flush=True)

if not done:
    print("Render did not finish. Last log:", flush=True)
    try:
        sbx = Sandbox.connect(SBX_ID)
        r = sbx.commands.run('tail -30 /tmp/render.log 2>&1', timeout=15)
        print(r.stdout, flush=True)
    except: pass

print(f"\nSandbox: {SBX_ID}", flush=True)
