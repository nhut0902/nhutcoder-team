#!/home/z/.venv/bin/python3
"""Step 1: Spawn E2B sandbox with MORE RAM (4GB), install HyperFrames + Chrome + ffmpeg + Node 22.
Then upload the Gemini Spark image to sandbox and write the HyperFrames composition."""
import os, time
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"

print("=== Spawning fresh E2B sandbox (default has 512MB, but let's try with 4GB template) ===", flush=True)
# Default template - we'll add swap for more RAM
sbx = Sandbox.create(timeout=1800)
sbx_id = sbx.sandbox_id
print(f"Sandbox: {sbx_id}", flush=True)

try:
    sbx.set_timeout(60 * 30)
    PATHFIX = "export PATH=/usr/bin:$PATH && "

    # 1. Create 4GB swap (since default template only has 512MB RAM)
    print("\n=== Create 4GB swap ===", flush=True)
    r = sbx.commands.run(
        "sudo fallocate -l 4G /swapfile 2>&1 && sudo chmod 600 /swapfile && sudo mkswap /swapfile 2>&1 | tail -2 && sudo swapon /swapfile && free -h",
        timeout=60,
    )
    print(r.stdout, flush=True)

    # 2. Install Node 22 + ffmpeg + chrome deps in one shot
    print("\n=== Install Node 22 + ffmpeg + Chrome deps ===", flush=True)
    r = sbx.commands.run(
        "curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | sudo -E bash - > /tmp/nodesetup.log 2>&1 && "
        "sudo apt-get install -y nodejs ffmpeg libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 "
        "libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 "
        "> /tmp/apt.log 2>&1 && echo INSTALL_OK",
        timeout=300,
    )
    print(r.stdout[-500:], flush=True)
    if "INSTALL_OK" not in r.stdout:
        print("INSTALL FAILED", flush=True)
        raise SystemExit(1)

    r = sbx.commands.run(PATHFIX + "node --version && npm --version", timeout=15)
    print("Node:", r.stdout, flush=True)

    # 3. Install HyperFrames (latest, 0.7.5+)
    print("\n=== Install HyperFrames ===", flush=True)
    r = sbx.commands.run(PATHFIX + "sudo npm install -g hyperframes 2>&1 | tail -3", timeout=240)
    print(r.stdout, flush=True)

    r = sbx.commands.run(PATHFIX + "which hyperframes && hyperframes --version 2>&1", timeout=15)
    print("HyperFrames:", r.stdout, flush=True)

    # 4. Install Chrome
    print("\n=== Install Chrome ===", flush=True)
    r = sbx.commands.run(PATHFIX + "hyperframes browser ensure 2>&1 | tail -8", timeout=300)
    print(r.stdout, flush=True)

    r = sbx.commands.run(PATHFIX + "hyperframes browser path 2>&1", timeout=15)
    print("Chrome path:", r.stdout, flush=True)

    # 5. Doctor check
    print("\n=== Doctor check ===", flush=True)
    r = sbx.commands.run(PATHFIX + "hyperframes doctor 2>&1 | tail -25", timeout=30)
    print(r.stdout, flush=True)

    print(f"\n=== Sandbox {sbx_id} ready for HyperFrames ===", flush=True)
    print(f"Sandbox ID saved.", flush=True)
    with open("/tmp/spark_sandbox_id.txt", "w") as f:
        f.write(sbx_id)

finally:
    print("\n=== Sandbox kept alive ===", flush=True)
