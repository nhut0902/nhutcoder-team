"""Init HyperFrames project + render MP4 about Browser use repo."""
import os, sys, time
from e2b import Sandbox

E2B_API_KEY = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
os.environ["E2B_API_KEY"] = E2B_API_KEY

SANDBOX_ID = "ijy0tt9cd55nqwjj48gpy"
print(f"=== Connecting to sandbox {SANDBOX_ID} ===", flush=True)
sbx = Sandbox.connect(SANDBOX_ID)

PATHFIX = "export PATH=/usr/bin:$PATH && "

# Extend timeout
sbx.set_timeout(60 * 30)  # 30 min
print("Sandbox timeout extended to 30 min", flush=True)

# Init HyperFrames project
print("\n=== Init HyperFrames project: browser-use-video ===", flush=True)
sbx.commands.run("rm -rf /home/user/browser-use-video && mkdir -p /home/user/browser-use-video", timeout=30)
r = sbx.commands.run(PATHFIX + "cd /home/user/browser-use-video && npx --yes hyperframes init . --yes 2>&1", timeout=180)
print("init:", r.stdout[-1500:], flush=True)
if r.stderr:
    print("init stderr:", r.stderr[-500:], flush=True)

# List project files
print("\n=== Project structure ===", flush=True)
r = sbx.commands.run("cd /home/user/browser-use-video && find . -maxdepth 3 -type f | head -30 && echo '---' && cat package.json 2>&1 | head -40")
print(r.stdout, flush=True)

print("\n=== Sandbox ready for composition creation ===", flush=True)
print(f"Sandbox ID: {SANDBOX_ID}", flush=True)
