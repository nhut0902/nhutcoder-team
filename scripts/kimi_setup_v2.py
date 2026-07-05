#!/home/z/.venv/bin/python3
"""Setup fresh sandbox + install everything + start render in ONE script to avoid session issues."""
import os, time, json
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SBX_ID = "ib5t2b0m6cilexs25p097"
print(f"=== Connect to {SBX_ID} ===", flush=True)
sbx = Sandbox.connect(SBX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# 1. Create 4GB swap
print("\n=== Create swap ===", flush=True)
r = sbx.commands.run("sudo fallocate -l 4G /swapfile 2>&1 && sudo chmod 600 /swapfile && sudo mkswap /swapfile 2>&1 | tail -2 && sudo swapon /swapfile && echo SWAP_OK", timeout=60)
print(r.stdout, flush=True)

# 2. Install Node 22 + ffmpeg + deps
print("\n=== Install deps ===", flush=True)
r = sbx.commands.run(
    "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - > /tmp/nodesetup.log 2>&1 && "
    "sudo apt-get install -y nodejs ffmpeg git libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
    "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
    "libxshmfence1 fonts-liberation > /tmp/apt.log 2>&1 && echo INSTALL_OK",
    timeout=300,
)
print(r.stdout[-200:], flush=True)

# 3. Install Remotion CLI
print("\n=== Install Remotion ===", flush=True)
r = sbx.commands.run(PATHFIX + "sudo npm install -g @remotion/cli 2>&1 | tail -3", timeout=240)
print(r.stdout, flush=True)

# 4. Ensure Chromium
print("\n=== Ensure Chromium ===", flush=True)
r = sbx.commands.run(PATHFIX + "remotion browser ensure 2>&1 | tail -3", timeout=300)
print(r.stdout[-300:], flush=True)

# 5. Create project structure
print("\n=== Create project ===", flush=True)
sbx.commands.run("mkdir -p /home/user/kimi_project/src /home/user/kimi_project/public /home/user/kimi_project/out", timeout=15)

# Read index.tsx from local file
with open("/home/z/my-project/scripts/kimi_remotion.py", "r") as f:
    # Extract the index_ts content from the script
    content = f.read()
    # The index_ts variable is too complex to extract. Read from a separate file we'll write
    pass

# We'll write the files separately in next step
print("Project dirs created", flush=True)

# 6. Upload narration + screenshots
print("\n=== Upload narration + screenshots ===", flush=True)
narration_path = "/home/z/my-project/download/kimi_audio/narration.mp3"
with open(narration_path, "rb") as f:
    sbx.files.write("/home/user/kimi_project/public/narration.mp3", f.read())
print("  Uploaded narration.mp3", flush=True)

for f_name in ['01_hf_title.png', '02_hf_readme.png', '03_gh_title.png', '04_gh_files.png']:
    p = f"/home/z/my-project/download/kimi_shots/{f_name}"
    with open(p, "rb") as fh:
        sbx.files.write(f"/home/user/kimi_project/public/{f_name}", fh.read())
    print(f"  Uploaded {f_name}", flush=True)

print(f"\nSandbox {SBX_ID} ready for Remotion composition!", flush=True)
