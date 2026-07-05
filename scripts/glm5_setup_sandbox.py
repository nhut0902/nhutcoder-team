#!/home/z/.venv/bin/python3
"""Spawn E2B sandbox + install HyperFrames + Chrome + Node 22 + ffmpeg."""
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

# 2. Install Node 22 + ffmpeg + chrome deps + git
print("\n=== Install Node 22 + ffmpeg + chrome deps ===", flush=True)
r = sbx.commands.run(
    "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - > /tmp/nodesetup.log 2>&1 && "
    "sudo apt-get install -y nodejs ffmpeg git libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
    "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
    "> /tmp/apt.log 2>&1 && echo INSTALL_OK",
    timeout=300,
)
print(r.stdout[-300:], flush=True)
if "INSTALL_OK" not in r.stdout:
    print("INSTALL FAILED", flush=True)
    raise SystemExit(1)

# 3. Install HyperFrames CLI globally
print("\n=== Install HyperFrames ===", flush=True)
r = sbx.commands.run(PATHFIX + "sudo npm install -g hyperframes 2>&1 | tail -3", timeout=240)
print(r.stdout, flush=True)

r = sbx.commands.run(PATHFIX + "which hyperframes && hyperframes --version 2>&1", timeout=15)
print("HyperFrames:", r.stdout, flush=True)

# 4. Install Chrome
print("\n=== Install Chrome ===", flush=True)
r = sbx.commands.run(PATHFIX + "hyperframes browser ensure 2>&1 | tail -5", timeout=300)
print(r.stdout[-300:], flush=True)

# 5. Doctor
print("\n=== Doctor ===", flush=True)
r = sbx.commands.run(PATHFIX + "hyperframes doctor 2>&1 | tail -20", timeout=30)
print(r.stdout, flush=True)

# Save sandbox ID
with open("/tmp/glm5_sandbox_id.txt", "w") as f:
    f.write(sbx_id)
print(f"\nSandbox {sbx_id} ready!", flush=True)
