#!/home/z/.venv/bin/python3
"""Capture README + install screenshots - scroll into view first, then capture."""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/pony_shots"
REPO_URL = "https://github.com/DietrichGebert/ponytail"
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH,
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
    page = context.new_page()
    page.goto(REPO_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # === Shot 4: README intro - scroll to README ===
    print("=== Shot 4: README intro ===", flush=True)
    readme = page.locator('article.markdown-body').first
    readme.scroll_into_view_if_needed()
    page.wait_for_timeout(2000)
    readme_box = readme.bounding_box()
    print(f"README bounding box: {readme_box}", flush=True)
    # Use element screenshot instead of clip
    readme.screenshot(path=f"{OUT_DIR}/04_readme.png")
    print("  README captured via element.screenshot", flush=True)

    # === Shot 5: Install section - scroll down more, find code block ===
    print("\n=== Shot 5: Install section ===", flush=True)
    # Look for code blocks (pre/code)
    code_blocks = page.locator('pre, .markdown-body pre, .highlight pre').all()
    print(f"Found {len(code_blocks)} code blocks", flush=True)
    if code_blocks:
        # Take first code block (usually install)
        first_code = code_blocks[0]
        first_code.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        # Use element screenshot
        first_code.screenshot(path=f"{OUT_DIR}/05_install.png")
        print("  Install captured via element.screenshot", flush=True)
    else:
        # Fallback - scroll and capture a section
        page.evaluate("window.scrollTo(0, 1500)")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"{OUT_DIR}/05_install.png", clip={"x": 0, "y": 1500, "width": 1280, "height": 500})

    browser.close()

# List
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    print(f"  {f} ({os.path.getsize(p)} bytes)")
