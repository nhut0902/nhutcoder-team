#!/home/z/.venv/bin/python3
"""Spawn fresh sandbox + install Remotion + write composition + render + download. ALL IN ONE."""
import os, time, json, subprocess
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"

print("=== Spawn fresh sandbox ===", flush=True)
sbx = Sandbox.create(timeout=1800)
sbx_id = sbx.sandbox_id
print(f"Sandbox: {sbx_id}", flush=True)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# 1. Create swap + install deps
print("\n=== Install deps ===", flush=True)
r = sbx.commands.run(
    "sudo fallocate -l 4G /swapfile 2>&1 && sudo chmod 600 /swapfile && sudo mkswap /swapfile 2>&1 | tail -1 && sudo swapon /swapfile && "
    "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - > /tmp/nodesetup.log 2>&1 && "
    "sudo apt-get install -y nodejs ffmpeg git libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
    "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
    "libxshmfence1 fonts-liberation > /tmp/apt.log 2>&1 && echo INSTALL_OK",
    timeout=400,
)
print(r.stdout[-200:], flush=True)
if "INSTALL_OK" not in r.stdout:
    raise SystemExit("INSTALL FAILED")

# 2. Install Remotion CLI + Chromium
print("\n=== Install Remotion + Chromium ===", flush=True)
sbx.commands.run(PATHFIX + "sudo npm install -g @remotion/cli 2>&1 | tail -1", timeout=240)
r = sbx.commands.run(PATHFIX + "remotion browser ensure 2>&1 | tail -2", timeout=300)
print(r.stdout[-200:], flush=True)

# 3. Create project structure
print("\n=== Create project ===", flush=True)
sbx.commands.run("mkdir -p /home/user/kimi_project/src /home/user/kimi_project/public /home/user/kimi_project/out", timeout=10)

# 4. Upload narration + screenshots
print("=== Upload assets ===", flush=True)
with open("/home/z/my-project/download/kimi_audio/narration.mp3", "rb") as f:
    sbx.files.write("/home/user/kimi_project/public/narration.mp3", f.read())
print("  narration.mp3 uploaded", flush=True)

for f_name in ['01_hf_title.png', '02_hf_readme.png', '03_gh_title.png', '04_gh_files.png']:
    p = f"/home/z/my-project/download/kimi_shots/{f_name}"
    with open(p, "rb") as fh:
        sbx.files.write(f"/home/user/kimi_project/public/{f_name}", fh.read())
    print(f"  {f_name} uploaded", flush=True)

# 5. Write package.json + tsconfig
print("\n=== Write config files ===", flush=True)
sbx.files.write("/home/user/kimi_project/package.json", '{"name":"kimi","version":"1.0.0","dependencies":{"react":"^19.0.0","react-dom":"^19.0.0","remotion":"^4.0.484","@remotion/cli":"^4.0.484","@remotion/react":"^4.0.484"},"devDependencies":{"@types/react":"^19.0.0","typescript":"^5.0.0"}}')
sbx.files.write("/home/user/kimi_project/tsconfig.json", '{"compilerOptions":{"target":"ES2020","module":"ESNext","moduleResolution":"node","jsx":"react-jsx","strict":false,"esModuleInterop":true,"skipLibCheck":true},"include":["src/**/*"]}')

# 6. Read template + replace placeholders + write index.tsx
print("=== Write index.tsx ===", flush=True)
with open("/tmp/kimi_durations.json") as f:
    d = json.load(f)
durations = d["durations"]
total = d["total"]
FPS = 30
total_frames = int(total * FPS)

scenes = ['s1','s2','s3','s4','s5','s6','s7','s8']
starts = {}
cum = 0
for s in scenes:
    starts[s] = int(cum * FPS)
    cum += durations[s]

with open("/home/z/my-project/scripts/kimi_index_template.tsx") as f:
    template = f.read()

replacements = {"__TOTAL_FRAMES__": str(total_frames)}
for s in scenes:
    replacements[f"__DUR_{s.upper()}__"] = str(int(durations[s] * FPS))
    replacements[f"__START_{s.upper()}__"] = str(starts[s])

for k, v in replacements.items():
    template = template.replace(k, v)

sbx.files.write("/home/user/kimi_project/src/index.tsx", template)
print(f"  index.tsx written ({total_frames} frames)", flush=True)

# 7. npm install
print("\n=== npm install ===", flush=True)
r = sbx.commands.run(PATHFIX + "cd /home/user/kimi_project && npm install --no-audit --no-fund 2>&1 | tail -2", timeout=300)
print(r.stdout, flush=True)

# 8. Write render script + start
print("\n=== Start render ===", flush=True)
sbx.files.write("/home/user/start_render.sh", "#!/bin/bash\nexport PATH=/usr/bin:$PATH\ncd /home/user/kimi_project\nrm -rf out\nremotion render src/index.tsx KimiVideo out/kimi.mp4 --codec h264 --crf 23 --concurrency 1 > /tmp/render.log 2>&1\n")
sbx.commands.run("chmod +x /home/user/start_render.sh", timeout=10)
r = sbx.commands.run("nohup /home/user/start_render.sh </dev/null >/dev/null 2>&1 & disown; echo $!", timeout=10)
print(f"  PID: {r.stdout.strip()}", flush=True)

# Wait for bundling to complete (30s)
time.sleep(30)
r = sbx.commands.run("ps aux | grep remotion | grep -v grep | wc -l; tail -3 /tmp/render.log 2>&1 | head -c 400", timeout=15)
print(f"  30s check: {r.stdout.strip()}", flush=True)

# 9. Poll for completion (max 15 min)
print("\n=== Poll render (max 15 min) ===", flush=True)
start_poll = time.time()
done = False
while time.time() - start_poll < 900:
    time.sleep(60)
    try:
        sbx = Sandbox.connect(sbx_id)
        sbx.set_timeout(60 * 30)
        r = sbx.commands.run(
            "ls /home/user/kimi_project/out/*.mp4 2>/dev/null && echo MP4_FOUND || echo NO_MP4; "
            "ps aux | grep remotion | grep -v grep | wc -l; "
            "tail -1 /tmp/render.log 2>&1 | head -c 200",
            timeout=15,
        )
        elapsed = int(time.time() - start_poll)
        out = r.stdout.strip().replace('\n', ' | ')[:250]
        print(f"[{elapsed}s] {out}", flush=True)
        if 'MP4_FOUND' in r.stdout and "0" in r.stdout.split('|')[1] if len(r.stdout.split('|')) > 1 else False:
            # Verify MP4 is complete (no remotion processes running)
            r2 = sbx.commands.run(
                "ls -la /home/user/kimi_project/out/*.mp4 && "
                "ffprobe -v error -show_entries format=duration,size:stream=width,height /home/user/kimi_project/out/kimi.mp4 2>&1",
                timeout=15,
            )
            if "duration" in r2.stdout:
                print("MP4 READY:", r2.stdout, flush=True)
                done = True
                break
    except Exception as e:
        print(f"poll err: {e}", flush=True)

if not done:
    print("Render timeout. Last log:", flush=True)
    try:
        sbx = Sandbox.connect(sbx_id)
        r = sbx.commands.run('tail -20 /tmp/render.log 2>&1', timeout=15)
        print(r.stdout, flush=True)
    except: pass
    raise SystemExit("RENDER TIMEOUT")

# 10. Download MP4
print("\n=== Download MP4 ===", flush=True)
sbx = Sandbox.connect(sbx_id)
sbx.set_timeout(60*30)
mp4_bytes = sbx.files.read("/home/user/kimi_project/out/kimi.mp4", format="bytes")
out = "/home/z/my-project/download/kimi-video.mp4"
with open(out, "wb") as f:
    f.write(mp4_bytes)
print(f"Downloaded: {out} ({len(mp4_bytes)} bytes)", flush=True)

# Verify
r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name,r_frame_rate","-of","default=noprint_wrappers=1", out], capture_output=True, text=True)
print(r.stdout, flush=True)

# Save sandbox ID
with open("/tmp/kimi_sandbox_id.txt", "w") as f:
    f.write(sbx_id)
print(f"\nDone! Sandbox: {sbx_id}", flush=True)
