"""
E2B sandbox: install HyperFrames + render a short MP4 about Browser use repo.
"""
import os, sys, time, base64, json
from e2b import Sandbox

E2B_API_KEY = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
os.environ["E2B_API_KEY"] = E2B_API_KEY

print("=== Creating E2B sandbox ===", flush=True)
sbx = Sandbox.create(timeout=600)  # 10 minutes
print(f"Sandbox ID: {sbx.sandbox_id}", flush=True)

try:
    # Check baseline
    print("\n=== Check baseline ===", flush=True)
    r = sbx.commands.run("uname -a && cat /etc/os-release | head -5")
    print(r.stdout, flush=True)

    # Install Node.js 22 (via NodeSource)
    print("\n=== Install Node.js 22 ===", flush=True)
    r = sbx.commands.run(
        "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs",
        timeout=300,
    )
    print("STDOUT:", r.stdout[-2000:], flush=True)
    if r.stderr:
        print("STDERR:", r.stderr[-1000:], flush=True)

    r = sbx.commands.run("node --version && npm --version")
    print("Node/npm versions:", r.stdout, flush=True)

    # Install ffmpeg
    print("\n=== Install ffmpeg ===", flush=True)
    r = sbx.commands.run("sudo apt-get install -y ffmpeg", timeout=180)
    print("ffmpeg install done:", r.stdout[-500:], flush=True)
    r = sbx.commands.run("ffmpeg -version | head -1")
    print(r.stdout, flush=True)

    # Install HyperFrames CLI globally
    print("\n=== Install HyperFrames CLI ===", flush=True)
    r = sbx.commands.run("npm install -g hyperframes", timeout=240)
    print("STDOUT:", r.stdout[-2000:], flush=True)
    if r.stderr:
        print("STDERR:", r.stderr[-1000:], flush=True)

    r = sbx.commands.run("which hyperframes && hyperframes --version 2>&1 || hyperframes --help 2>&1 | head -30")
    print("hyperframes:", r.stdout, flush=True)

    # Init a HyperFrames project
    print("\n=== Init HyperFrames project ===", flush=True)
    sbx.commands.run("mkdir -p /home/user/videos && cd /home/user/videos && rm -rf browser-use-video", timeout=30)
    r = sbx.commands.run("cd /home/user/videos && npx --yes hyperframes init browser-use-video --yes 2>&1", timeout=180)
    print("init output:", r.stdout[-2000:], flush=True)
    if r.stderr:
        print("init stderr:", r.stderr[-1000:], flush=True)

    r = sbx.commands.run("ls -la /home/user/videos/browser-use-video/ 2>&1")
    print("project dir:", r.stdout, flush=True)

    # Find the main composition file
    r = sbx.commands.run("find /home/user/videos/browser-use-video -maxdepth 3 -type f \\( -name '*.html' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.json' \\) | head -20")
    print("project files:", r.stdout, flush=True)

    # Read package.json to see scripts
    r = sbx.commands.run("cat /home/user/videos/browser-use-video/package.json 2>&1")
    print("package.json:", r.stdout[:2000], flush=True)

    print("\n=== Sandbox ready for next step ===", flush=True)
    print(f"Sandbox ID: {sbx.sandbox_id}", flush=True)

    # Save sandbox ID for next script
    with open("/tmp/e2b_sandbox_id.txt", "w") as f:
        f.write(sbx.sandbox_id)
    print("Sandbox ID saved to /tmp/e2b_sandbox_id.txt", flush=True)

finally:
    # Keep sandbox alive for next step — don't kill
    print("\n=== Sandbox kept alive ===", flush=True)
    print(f"To resume: Sandbox.reconnect('{sbx.sandbox_id}')", flush=True)
