#!/home/z/.venv/bin/python3
"""Create HyperFrames composition for GLM-5 video + render.
Use proper HyperFrames syntax: data-composition-id, class="clip", data-start, data-duration."""
import os, json, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = open("/tmp/glm5_sandbox_id.txt").read().strip()
print(f"=== Connect to sandbox {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Load durations
with open("/tmp/glm5_durations.json") as f:
    durations = json.load(f)["durations"]

scenes_list = ["s1","s2","s3","s4","s5","s6","s7","s8"]
starts = {}
cum = 0
for s in scenes_list:
    starts[s] = cum
    cum += durations[s]
total_dur = cum
print(f"Total duration: {total_dur:.2f}s", flush=True)

# Build HTML composition with HyperFrames syntax
# Use class="clip" + data-start/data-duration for scene visibility
# Register window.__timelines with simple duration object
html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>GLM-5</title>
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
  .orb {{ position: absolute; border-radius: 50%; filter: blur(60px); opacity: 0.4; pointer-events: none; }}
  .orb-1 {{ width: 400px; height: 400px; background: #4285f4; top: -100px; left: -100px; }}
  .orb-2 {{ width: 500px; height: 500px; background: #9b72cb; bottom: -150px; right: -150px; }}
  .orb-3 {{ width: 300px; height: 300px; background: #00d4ff; top: 700px; right: -100px; opacity: 0.3; }}

  .clip {{
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 60px; opacity: 0;
    transition: opacity 0.3s ease;
  }}
  .spark-icon {{ font-size: 200px; margin-bottom: 40px; filter: drop-shadow(0 0 30px rgba(66, 133, 244, 0.8)); }}
  h1 {{
    font-size: 130px; font-weight: 900; line-height: 1; text-align: center;
    background: linear-gradient(135deg, #4285f4 0%, #9b72cb 50%, #00d4ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -3px; margin-bottom: 30px;
  }}
  h2 {{ font-size: 80px; font-weight: 800; text-align: center; color: #fff; line-height: 1.1; margin-bottom: 25px; }}
  .subtitle {{ font-size: 44px; color: #cbd5e1; text-align: center; line-height: 1.4; max-width: 900px; }}
  .date-badge {{ background: rgba(66, 133, 244, 0.2); border: 2px solid #4285f4; border-radius: 20px; padding: 12px 32px; font-size: 32px; font-weight: 600; color: #4285f4; margin-bottom: 40px; letter-spacing: 2px; }}
  .shot-img {{ width: 800px; height: auto; border-radius: 24px; border: 4px solid rgba(66, 133, 244, 0.5); box-shadow: 0 20px 60px rgba(66, 133, 244, 0.4); margin-bottom: 30px; object-fit: cover; }}
  .features {{ display: flex; flex-direction: column; gap: 24px; width: 100%; }}
  .feature {{ display: flex; align-items: center; gap: 24px; background: rgba(30, 41, 59, 0.7); border: 2px solid rgba(66, 133, 244, 0.3); border-radius: 18px; padding: 24px 32px; backdrop-filter: blur(10px); }}
  .feature .icon {{ font-size: 56px; }}
  .feature .text {{ font-size: 36px; font-weight: 600; color: #e0e7ff; }}
  .stat-block {{ background: rgba(30, 41, 59, 0.7); border: 2px solid rgba(66, 133, 244, 0.3); border-radius: 24px; padding: 40px 60px; text-align: center; backdrop-filter: blur(10px); }}
  .stat-block .label {{ font-size: 32px; color: #94a3b8; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 3px; }}
  .stat-block .value {{ font-size: 100px; font-weight: 900; color: #4285f4; line-height: 1; }}
  .stat-block .desc {{ font-size: 32px; color: #cbd5e1; margin-top: 12px; }}
  .footer {{ position: absolute; bottom: 60px; left: 0; right: 0; text-align: center; font-size: 28px; color: #64748b; font-weight: 500; }}
  .source-link {{ color: #4285f4; font-weight: 600; }}
  .hashtags {{ font-size: 30px; color: #00d4ff; font-weight: 600; text-align: center; margin-top: 30px; }}
</style>
</head>
<body>

<div id="root" class="composition" data-composition-id="glm5" data-start="0" data-duration="{total_dur:.2f}" data-width="1080" data-height="1920">

  <div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div>

  <div class="clip" id="scene1" data-start="0" data-duration="{durations['s1']:.2f}" data-track-index="0">
    <div class="date-badge">5/7/2026 · OPEN SOURCE</div>
    <div class="spark-icon">🚀</div>
    <h1>GLM-5</h1>
    <div class="subtitle">From Vibe Coding to Agentic Engineering<br>by Z.ai</div>
  </div>

  <div class="clip" id="scene2" data-start="{starts['s2']:.2f}" data-duration="{durations['s2']:.2f}" data-track-index="0">
    <img class="shot-img" src="01_title.png" alt="GLM-5 GitHub">
    <div class="subtitle">Repo zai-org/GLM-5<br>6,000+ stars · 700+ forks</div>
  </div>

  <div class="clip" id="scene3" data-start="{starts['s3']:.2f}" data-duration="{durations['s3']:.2f}" data-track-index="0">
    <div class="spark-icon">⚙️</div>
    <h2>Thông số</h2>
    <div class="features">
      <div class="feature"><span class="icon">📊</span><span class="text">744B params (40B active)</span></div>
      <div class="feature"><span class="icon">📚</span><span class="text">28.5T tokens pretrain</span></div>
      <div class="feature"><span class="icon">🎯</span><span class="text">200K context window</span></div>
    </div>
  </div>

  <div class="clip" id="scene4" data-start="{starts['s4']:.2f}" data-duration="{durations['s4']:.2f}" data-track-index="0">
    <img class="shot-img" src="03_files.png" alt="Code structure">
    <div class="subtitle">DeepSeek Sparse Attention<br>+ slime RL infrastructure</div>
  </div>

  <div class="clip" id="scene5" data-start="{starts['s5']:.2f}" data-duration="{durations['s5']:.2f}" data-track-index="0">
    <div class="spark-icon">🏆</div>
    <h2>Benchmark</h2>
    <div class="stat-block">
      <div class="label">Vending Bench 2</div>
      <div class="value">#1</div>
      <div class="desc">$4,432 balance · SOTA open-source</div>
    </div>
  </div>

  <div class="clip" id="scene6" data-start="{starts['s6']:.2f}" data-duration="{durations['s6']:.2f}" data-track-index="0">
    <div class="spark-icon">🧠</div>
    <h2>Thinking Budget</h2>
    <div class="subtitle">reasoning_effort param<br>default: max<br>trade-off: quality vs speed</div>
  </div>

  <div class="clip" id="scene7" data-start="{starts['s7']:.2f}" data-duration="{durations['s7']:.2f}" data-track-index="0">
    <div class="spark-icon">💡</div>
    <h2>Use Cases</h2>
    <div class="features">
      <div class="feature"><span class="icon">🔧</span><span class="text">Complex systems engineering</span></div>
      <div class="feature"><span class="icon">📋</span><span class="text">Long-horizon agentic tasks</span></div>
      <div class="feature"><span class="icon">💻</span><span class="text">Coding · Reasoning</span></div>
    </div>
  </div>

  <div class="clip" id="scene8" data-start="{starts['s8']:.2f}" data-duration="{durations['s8']:.2f}" data-track-index="0">
    <div class="spark-icon">🎯</div>
    <h2>Tổng kết</h2>
    <div class="subtitle">Bước tiến quan trọng của Z.ai<br>trong cuộc đua open-source AI</div>
    <div class="hashtags">#GLM5 #Zai #OpenSource #AI2026</div>
  </div>

  <div class="footer">Nguồn: <span class="source-link">github.com/zai-org/GLM-5</span></div>

</div>

<script>
  window.__timelines = window.__timelines || {{}};
  window.__timelines["glm5"] = {{ duration: {total_dur:.2f} }};
</script>

</body>
</html>
"""

print("=== Write HyperFrames composition HTML ===", flush=True)
sbx.files.write("/home/user/glm5_project/index.html", html)
print("HTML written", flush=True)

# Lint
print("\n=== Lint ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/glm5_project && hyperframes lint . 2>&1 | head -15", timeout=60)
print(r.stdout, flush=True)

# Render
print(f"\n=== Render ({total_dur:.2f}s, fps 24, draft, audio narration.mp3) ===", flush=True)
try:
    r = sbx.commands.run(
        f"cd /home/user/glm5_project && rm -rf renders/* && "
        f"nohup bash -c '{PATHFIX} hyperframes render . -o renders/glm5.mp4 --quality draft --fps 24 --audio narration.mp3 > /tmp/render.log 2>&1' "
        f"</dev/null > /dev/null 2>&1 & disown; echo PID=$!",
        timeout=20,
    )
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
            "ls /home/user/glm5_project/renders/*.mp4 2>/dev/null && echo MP4_FOUND || echo NO_MP4; "
            "ps aux | grep hyperframes | grep -v grep | wc -l; "
            "tail -1 /tmp/render.log 2>&1 | head -c 200",
            timeout=15,
        )
        elapsed = int(time.time() - start_poll)
        out = r.stdout.strip().replace('\n', ' | ')[:250]
        print(f"[{elapsed}s] {out}", flush=True)
        if 'MP4_FOUND' in r.stdout:
            r2 = sbx.commands.run(
                "ls -la /home/user/glm5_project/renders/*.mp4 && "
                "ffprobe -v error -show_entries format=duration,size:stream=width,height /home/user/glm5_project/renders/glm5.mp4 2>&1",
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
