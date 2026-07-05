#!/home/z/.venv/bin/python3
"""Spawn E2B sandbox + install Remotion + Chromium + ffmpeg."""
import os, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"

print("=== Spawn E2B sandbox ===", flush=True)
sbx = Sandbox.create(timeout=1800)
sbx_id = sbx.sandbox_id
print(f"Sandbox: {sbx_id}", flush=True)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# 1. Create 4GB swap
print("\n=== Create 4GB swap ===", flush=True)
r = sbx.commands.run(
    "sudo fallocate -l 4G /swapfile 2>&1 && sudo chmod 600 /swapfile && sudo mkswap /swapfile 2>&1 | tail -2 && sudo swapon /swapfile && free -h",
    timeout=60,
)
print(r.stdout, flush=True)

# 2. Install Node 22 + ffmpeg + Chromium deps
print("\n=== Install Node 22 + ffmpeg + Chromium deps ===", flush=True)
r = sbx.commands.run(
    "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - > /tmp/nodesetup.log 2>&1 && "
    "sudo apt-get install -y nodejs ffmpeg git libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
    "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
    "libxshmfence1 fonts-liberation > /tmp/apt.log 2>&1 && echo INSTALL_OK",
    timeout=300,
)
print(r.stdout[-300:], flush=True)
if "INSTALL_OK" not in r.stdout:
    print("INSTALL FAILED", flush=True)
    raise SystemExit(1)

r = sbx.commands.run(PATHFIX + "node --version && npm --version", timeout=15)
print("Node:", r.stdout, flush=True)

# 3. Install Remotion CLI globally
print("\n=== Install Remotion CLI ===", flush=True)
r = sbx.commands.run(PATHFIX + "sudo npm install -g @remotion/cli 2>&1 | tail -3", timeout=240)
print(r.stdout, flush=True)

r = sbx.commands.run(PATHFIX + "which remotion && remotion --version 2>&1", timeout=15)
print("Remotion:", r.stdout, flush=True)

# 4. Ensure Chromium for Remotion (it has its own browser installer)
print("\n=== Install Remotion Chromium ===", flush=True)
r = sbx.commands.run(PATHFIX + "npx -y remotion browser ensure 2>&1 | tail -5", timeout=300)
print(r.stdout[-400:], flush=True)

# Save sandbox ID
with open("/tmp/kimi_sandbox_id.txt", "w") as f:
    f.write(sbx_id)
print(f"\nSandbox {sbx_id} ready!", flush=True)
