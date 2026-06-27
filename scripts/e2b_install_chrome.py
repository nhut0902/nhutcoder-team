"""Add swap, install Chrome, then render video with HyperFrames."""
import os, sys
from e2b import Sandbox

os.environ["E2B_API_KEY"] = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
SANDBOX_ID = "ijy0tt9cd55nqwjj48gpy"
sbx = Sandbox.connect(SANDBOX_ID)
sbx.set_timeout(60 * 30)
PATHFIX = "export PATH=/usr/bin:$PATH && "

# Step 1: Create 2GB swap
print("=== Step 1: Create swap ===", flush=True)
r = sbx.commands.run(
    "sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && "
    "sudo mkswap /swapfile && sudo swapon /swapfile && free -h",
    timeout=60,
)
print(r.stdout, flush=True)
if r.stderr:
    print("STDERR:", r.stderr[:500], flush=True)

# Step 2: Install Chrome via hyperframes browser ensure
print("\n=== Step 2: Install Chrome ===", flush=True)
r = sbx.commands.run(PATHFIX + "hyperframes browser ensure 2>&1 | tail -30", timeout=300)
print(r.stdout, flush=True)
if r.stderr:
    print("STDERR:", r.stderr[:500], flush=True)

# Step 3: Verify Chrome
print("\n=== Step 3: Verify Chrome ===", flush=True)
r = sbx.commands.run(PATHFIX + "hyperframes browser path 2>&1 && ls -la $(hyperframes browser path) 2>&1", timeout=30)
print(r.stdout, flush=True)

print(f"\n=== Sandbox ID: {SANDBOX_ID} ===", flush=True)
print("Ready to create composition + render", flush=True)
