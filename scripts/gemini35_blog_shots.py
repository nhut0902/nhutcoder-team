#!/home/z/.venv/bin/python3
"""Capture screenshots of blog pages comparing Gemini 3.5 Pro with other models.
Also capture Google AI pricing page and developer guide."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT_DIR = "/home/z/my-project/download/gemini35_blog_shots"
os.makedirs(OUT_DIR, exist_ok=True)
CHROME_PATH = "/home/z/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome"

# Blog pages to screenshot
PAGES = [
    ("https://andrew.ooo/answers/gemini-3-5-pro-ga-vs-claude-fable-5-vs-gpt-5-6-late-june-2026/", "01_comparison_blog"),
    ("https://theairankings.com/google/gemini-3-5-pro/", "02_airankings"),
    ("https://www.developersdigest.tech/blog/gemini-3-5-pro-developer-guide-2026", "03_devguide"),
    ("https://ai.google.dev/gemini-api/docs/pricing", "04_pricing"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME_PATH, headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=2)
    page = context.new_page()

    for url, name in PAGES:
        print(f"=== {name} ===", flush=True)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            # Capture top portion (most important content)
            page.screenshot(path=f"{OUT_DIR}/{name}.png", clip={"x": 0, "y": 0, "width": 1400, "height": 800})
            print(f"  {name} captured", flush=True)
        except Exception as e:
            print(f"  err: {e}", flush=True)
            # Fallback - try simpler capture
            try:
                page.screenshot(path=f"{OUT_DIR}/{name}.png", full_page=False)
            except:
                pass

    browser.close()

# List
for f in sorted(os.listdir(OUT_DIR)):
    p = os.path.join(OUT_DIR, f)
    img = Image.open(p)
    print(f"  {f} ({os.path.getsize(p)}B, {img.size[0]}x{img.size[1]})")
