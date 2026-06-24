"""Reconnect to E2B sandbox and install HyperFrames with proper Node 22 path."""
import os, sys
from e2b import Sandbox

E2B_API_KEY = "e2b_e211aca6616cd7e18155af3973539bf7b9bd7772"
os.environ["E2B_API_KEY"] = E2B_API_KEY

SANDBOX_ID = "ijy0tt9cd55nqwjj48gpy"
print(f"=== Reconnecting to sandbox {SANDBOX_ID} ===", flush=True)
sbx = Sandbox.connect(SANDBOX_ID)

# Find all node binaries
print("\n=== Find node binaries ===", flush=True)
r = sbx.commands.run("which -a node npm; ls -la /usr/bin/node /usr/local/bin/node 2>/dev/null; /usr/bin/node --version 2>&1")
print(r.stdout, flush=True)

# Fix PATH so Node 22 is used first
fix_path = 'export PATH=/usr/bin:$PATH && '
print("\n=== Verify Node 22 with PATH fix ===", flush=True)
r = sbx.commands.run(fix_path + "node --version && npm --version")
print(r.stdout, flush=True)

# Install HyperFrames CLI globally
print("\n=== Install HyperFrames CLI globally ===", flush=True)
r = sbx.commands.run(fix_path + "npm install -g hyperframes 2>&1 | tail -20", timeout=300)
print(r.stdout, flush=True)
if r.stderr:
    print("STDERR:", r.stderr[-1000:], flush=True)

# Verify hyperframes
print("\n=== Verify hyperframes ===", flush=True)
r = sbx.commands.run(fix_path + "which hyperframes && hyperframes --version 2>&1 || hyperframes --help 2>&1 | head -40")
print(r.stdout, flush=True)

# Save PATH fix for next steps
print("\n=== Persist PATH in /etc/environment-like file ===", flush=True)
sbx.filesystem.write("/home/user/.bash_paths", "export PATH=/usr/bin:$PATH\n")
print("Done", flush=True)

# Save sandbox ID
with open("/tmp/e2b_sandbox_id.txt", "w") as f:
    f.write(SANDBOX_ID)
print(f"\nSandbox ID: {SANDBOX_ID}", flush=True)
print("Ready for next step: init project + render video", flush=True)
